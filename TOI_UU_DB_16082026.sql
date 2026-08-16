/* =========================================================================
   IACC_CHULONG — Tối ưu hiệu năng phía DATABASE
   Ngày lập: 16/08/2026 — dựa trên số liệu ĐO THẬT trên chính máy chủ này.

   CÁCH CHẠY: mở SQL Server Management Studio, chọn database IACC_CHULONG
              ở ô dropdown, mở file này, bấm Execute (F5).

   ⚠️ PHẦN 3 và 4 (tạo index) KHOÁ BẢNG khi chạy — SQL Express không có
      ONLINE rebuild. Hai bảng này nhỏ (VOUCHER 244.653 dòng,
      VOUCHER_DETAIL 881.249 dòng) nên chỉ mất vài giây, chạy giờ nghỉ
      trưa là được. KHÔNG cần chờ tới đêm.

   ⚠️ ĐỌC MỤC "KHÔNG LÀM" Ở CUỐI FILE trước khi tự thêm index cho LEDGER.

   ĐÃ KIỂM TRA TRƯỚC trên máy chủ ngày 16/08/2026:
     - Mục 1 (AUTO_SHRINK / AUTO_CLOSE): CẢ 3 DATABASE VÀ 'model' ĐÃ TẮT SẴN
       → chạy vào sẽ không đổi gì, giữ lại để lỡ sau này ai bật lại thì bắt được.
     - Mục 2 (optimize for ad hoc workloads): ĐÃ BẬT SẴN (= 1) → cũng không đổi gì.
     - Mục 3, 4: hai index này CHƯA CÓ, chạy vào sẽ tạo mới. Đã xác nhận mọi cột
       dùng trong index đều tồn tại thật và không có cột LOB (nên nén PAGE chạy được).
     - Mục 6: tempdb đang là 4 file × 1024 MB = 4 GB.
   ========================================================================= */

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

/* Khoá đích: khỏi phụ thuộc ô dropdown chọn database của SSMS. Chọn nhầm DB thì
   mục 3-5 sẽ tạo index lên nhầm chỗ. */
USE IACC_CHULONG;
GO

IF DB_NAME() <> N'IACC_CHULONG'
BEGIN
    DECLARE @cur SYSNAME = DB_NAME();
    RAISERROR(N'SAI DATABASE! Dang o [%s], phai la IACC_CHULONG. DA NGAT KET NOI, khong chay gi.',
              20, 1, @cur) WITH LOG;
END
GO

PRINT '=== BAT DAU — database: ' + DB_NAME() + ' ===';
GO

/* -------------------------------------------------------------------------
   1) TẮT AUTO_SHRINK VÀ AUTO_CLOSE  ← VIỆC RẺ NHẤT, HIỆU QUẢ NHẤT

   AUTO_CLOSE bật khiến database ĐÓNG LẠI khi không còn ai kết nối. Người
   vào sau phải chờ mở lại cả database — đúng triệu chứng "lúc nhanh lúc chậm".
   AUTO_SHRINK khiến SQL tự co file rồi lại phình ra, vừa tốn CPU vừa làm
   dữ liệu nằm rải rác trên đĩa.

   Cả hai đổi tức thì, không khoá bảng, không mất dữ liệu.
   ------------------------------------------------------------------------- */
DECLARE @db SYSNAME, @sql NVARCHAR(MAX);
DECLARE c CURSOR LOCAL FAST_FORWARD FOR
    SELECT name FROM sys.databases
    WHERE database_id > 4 AND state = 0 AND is_read_only = 0;
OPEN c;
FETCH NEXT FROM c INTO @db;
WHILE @@FETCH_STATUS = 0
BEGIN
    IF EXISTS (SELECT 1 FROM sys.databases WHERE name = @db AND is_auto_shrink_on = 1)
    BEGIN
        SET @sql = N'ALTER DATABASE ' + QUOTENAME(@db) + N' SET AUTO_SHRINK OFF;';
        EXEC sp_executesql @sql;
        PRINT '  [' + @db + '] AUTO_SHRINK -> OFF';
    END
    IF EXISTS (SELECT 1 FROM sys.databases WHERE name = @db AND is_auto_close_on = 1)
    BEGIN
        SET @sql = N'ALTER DATABASE ' + QUOTENAME(@db) + N' SET AUTO_CLOSE OFF;';
        EXEC sp_executesql @sql;
        PRINT '  [' + @db + '] AUTO_CLOSE -> OFF';
    END
    FETCH NEXT FROM c INTO @db;
END
CLOSE c; DEALLOCATE c;
GO

/* Database 'model' — nếu nó bật AUTO_SHRINK thì mọi DB tạo mới sau này lại bật lại */
IF EXISTS (SELECT 1 FROM sys.databases WHERE name = 'model' AND is_auto_shrink_on = 1)
BEGIN
    ALTER DATABASE [model] SET AUTO_SHRINK OFF;
    PRINT '  [model] AUTO_SHRINK -> OFF (chan DB tao moi bi bat lai)';
END
GO

/* -------------------------------------------------------------------------
   2) OPTIMIZE FOR AD HOC WORKLOADS

   Ứng dụng iPOS bắn câu lệnh SQL thô không tham số hoá, nên mỗi lần chạy đẻ
   ra một kế hoạch thực thi mới nằm lì trong bộ nhớ. Máy này chỉ có 1.410 MB
   bộ nhớ đệm (trần cứng của bản Express) — để plan rác chiếm chỗ là phí.
   ------------------------------------------------------------------------- */
IF EXISTS (SELECT 1 FROM sys.configurations WHERE name = 'optimize for ad hoc workloads' AND value_in_use = 0)
BEGIN
    EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
    EXEC sp_configure 'optimize for ad hoc workloads', 1; RECONFIGURE;
    PRINT '  optimize for ad hoc workloads -> 1';
END
GO

/* -------------------------------------------------------------------------
   3) INDEX CHO VOUCHER_DETAIL  ← ĐO ĐƯỢC LỢI ÍCH LỚN NHẤT

   VOUCHER_DETAIL chỉ có mỗi khoá chính trên PR_KEY, KHÔNG có index nào trên
   FR_KEY — mà FR_KEY chính là cột nối về chứng từ cha. Mọi lần mở danh sách
   chứng từ tiền, SQL phải quét toàn bộ 881.249 dòng để ghép.

   Đây đúng là loại index mà IX_SALE_DETAIL_FR_KEY đã chứng minh hiệu quả
   trên SALE_DETAIL. Cố ý KHÔNG thêm INCLUDE: bản có INCLUDE dài đã đo trên
   SALE_DETAIL là lỗ (phình 700 MB, lợi ích kém hơn bản trần 8 lần).

   Kích thước dự kiến: ~15 MB.
   ------------------------------------------------------------------------- */
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_VOUCHER_DETAIL_FR_KEY'
                 AND object_id = OBJECT_ID('dbo.VOUCHER_DETAIL'))
BEGIN
    CREATE NONCLUSTERED INDEX IX_VOUCHER_DETAIL_FR_KEY
        ON dbo.VOUCHER_DETAIL (FR_KEY)
        WITH (DATA_COMPRESSION = PAGE, SORT_IN_TEMPDB = ON);
    PRINT '  Da tao IX_VOUCHER_DETAIL_FR_KEY';
END
ELSE PRINT '  IX_VOUCHER_DETAIL_FR_KEY da co san, bo qua';
GO

/* -------------------------------------------------------------------------
   4) INDEX CHO VOUCHER (lọc + sắp xếp theo ngày chứng từ)

   VOUCHER cũng chỉ có khoá chính trên PR_KEY. Mọi báo cáo và danh sách đều
   lọc theo TRAN_DATE rồi sắp theo TRAN_DATE DESC, TRAN_NO — hiện phải quét
   cả bảng. INCLUDE các cột phần đầu chứng từ để khỏi phải quay lại bảng gốc.

   Kích thước dự kiến: ~35 MB.
   ------------------------------------------------------------------------- */
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_VOUCHER_TRAN_DATE_NO'
                 AND object_id = OBJECT_ID('dbo.VOUCHER'))
BEGIN
    CREATE NONCLUSTERED INDEX IX_VOUCHER_TRAN_DATE_NO
        ON dbo.VOUCHER (TRAN_DATE DESC, TRAN_NO)
        INCLUDE (PR_KEY, ORGANIZATION_ID, TRAN_ID, CONTACT_PERSON, ADDRESS, STATUS)
        WITH (DATA_COMPRESSION = PAGE, SORT_IN_TEMPDB = ON);
    PRINT '  Da tao IX_VOUCHER_TRAN_DATE_NO';
END
ELSE PRINT '  IX_VOUCHER_TRAN_DATE_NO da co san, bo qua';
GO

/* -------------------------------------------------------------------------
   5) HAI INDEX CHO BÁO CÁO NẶNG: BC005, BC006, BC001

   ⛔ CHẠY NGOÀI GIỜ LÀM VIỆC. Hai index này nằm trên LEDGER (18,5 triệu dòng).
      SQL Express không có ONLINE rebuild nên trong lúc tạo, bảng LEDGER BỊ KHOÁ:
      nhân viên KHÔNG lưu được chứng từ. Dự kiến 3-8 phút mỗi index.

   ✅ AN TOÀN DỮ LIỆU: index không sửa, không xoá một dòng dữ liệu nào. Nó chỉ là
      bản sắp xếp sẵn để tìm cho nhanh. Không vừa ý thì DROP là xong, dữ liệu
      nguyên vẹn (lệnh gỡ ở cuối file).

   Ý ĐỒ: mấy index sẵn có đều sắp theo NGÀY, nên khi báo cáo gom nhóm theo
   tài khoản / đối tượng / đơn vị thì SQL phải dựng bảng băm cho cả 17 triệu
   dòng — đó chính là chỗ tốn 29 giây. Hai index dưới đây sắp sẵn ĐÚNG THỨ TỰ
   mà báo cáo gom nhóm, để SQL cộng thẳng theo dòng, khỏi dựng bảng băm.

   Tốn thêm khoảng 700 MB dung lượng. Lưu chứng từ chậm thêm ước ~15%
   (2 giây -> khoảng 2,3 giây).
   ------------------------------------------------------------------------- */

-- 5a) Cho BC005 (Bảng cân đối kế toán) và BC006 (Bảng cân đối phát sinh):
--     cả hai đều cộng dồn số dư theo (tài khoản, đối tượng, đơn vị).
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_LEDGER_RPT_BALANCE'
                 AND object_id = OBJECT_ID('dbo.LEDGER'))
BEGIN
    PRINT '  Dang tao IX_LEDGER_RPT_BALANCE (3-8 phut, LEDGER bi khoa)...';
    CREATE NONCLUSTERED INDEX IX_LEDGER_RPT_BALANCE
        ON dbo.LEDGER (ACCOUNT_ID, PR_DETAIL_ID, ORGANIZATION_ID, TRAN_DATE)
        INCLUDE (DEBIT_CREDIT, AMOUNT)
        WITH (DATA_COMPRESSION = PAGE, SORT_IN_TEMPDB = ON, MAXDOP = 2);
    PRINT '  Da tao IX_LEDGER_RPT_BALANCE';
END
ELSE PRINT '  IX_LEDGER_RPT_BALANCE da co san, bo qua';
GO

-- 5b) Cho BC001/BC002/BC003/BC004 (Kết quả kinh doanh):
--     gom nhóm theo (tài khoản, tài khoản đối ứng, nợ/có) trong một khoảng ngày.
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_LEDGER_RPT_KQKD'
                 AND object_id = OBJECT_ID('dbo.LEDGER'))
BEGIN
    PRINT '  Dang tao IX_LEDGER_RPT_KQKD (3-8 phut, LEDGER bi khoa)...';
    CREATE NONCLUSTERED INDEX IX_LEDGER_RPT_KQKD
        ON dbo.LEDGER (TRAN_DATE, ACCOUNT_ID, ACCOUNT_ID_CONTRA, DEBIT_CREDIT)
        INCLUDE (ITEM_ID, EXPENSE_ID, ORGANIZATION_ID, JOB_ID, AMOUNT)
        WITH (DATA_COMPRESSION = PAGE, SORT_IN_TEMPDB = ON, MAXDOP = 2);
    PRINT '  Da tao IX_LEDGER_RPT_KQKD';
END
ELSE PRINT '  IX_LEDGER_RPT_KQKD da co san, bo qua';
GO

/* -------------------------------------------------------------------------
   6) CẬP NHẬT THỐNG KÊ

   Thống kê cũ khiến SQL chọn nhầm cách chạy. Chạy nhanh, không khoá bảng.
   ------------------------------------------------------------------------- */
UPDATE STATISTICS dbo.VOUCHER        WITH FULLSCAN;
UPDATE STATISTICS dbo.VOUCHER_DETAIL WITH FULLSCAN;
PRINT '  Da cap nhat thong ke VOUCHER, VOUCHER_DETAIL';
GO
UPDATE STATISTICS dbo.LEDGER WITH SAMPLE 30 PERCENT;
PRINT '  Da cap nhat thong ke LEDGER';
GO

/* -------------------------------------------------------------------------
   7) THU TEMPDB VỀ

   SORT_IN_TEMPDB ở trên làm tempdb phình ra rồi GIỮ NGUYÊN kích thước vĩnh
   viễn. Chạy phần này SAU KHI đã tạo xong index ở mục 3-4.
   ------------------------------------------------------------------------- */
USE tempdb;
GO
/* tempdb ở máy này có 4 file dữ liệu, mỗi file 1024 MB (tổng 4 GB) — phải thu CẢ BỐN,
   thu mỗi file đầu là không ăn thua. */
DECLARE @f SYSNAME, @s NVARCHAR(300);
DECLARE cf CURSOR LOCAL FAST_FORWARD FOR
    SELECT name FROM sys.database_files WHERE type_desc = 'ROWS' ORDER BY file_id;
OPEN cf;
FETCH NEXT FROM cf INTO @f;
WHILE @@FETCH_STATUS = 0
BEGIN
    SET @s = N'DBCC SHRINKFILE (' + QUOTENAME(@f) + N', 512);';
    EXEC sp_executesql @s;
    PRINT '  Da thu tempdb file ' + @f + ' ve 512 MB';
    FETCH NEXT FROM cf INTO @f;
END
CLOSE cf; DEALLOCATE cf;
GO
USE IACC_CHULONG;
GO

/* -------------------------------------------------------------------------
   8) KIỂM TRA LẠI — chạy phần này để xác nhận mọi thứ đã đúng
   ------------------------------------------------------------------------- */
PRINT '';
PRINT '=== KIEM TRA ===';
GO

SELECT name AS [Database],
       is_auto_shrink_on AS [AUTO_SHRINK con bat?],
       is_auto_close_on  AS [AUTO_CLOSE con bat?]
FROM sys.databases WHERE database_id > 4;

SELECT i.name AS [Index moi tao],
       CAST(SUM(ps.used_page_count) * 8.0 / 1024 AS DECIMAL(10,1)) AS [Kich thuoc MB]
FROM sys.dm_db_partition_stats ps
JOIN sys.indexes i ON i.object_id = ps.object_id AND i.index_id = ps.index_id
WHERE i.name IN ('IX_VOUCHER_DETAIL_FR_KEY', 'IX_VOUCHER_TRAN_DATE_NO',
                 'IX_LEDGER_RPT_BALANCE', 'IX_LEDGER_RPT_KQKD')
GROUP BY i.name;

/* Dung luong database sau khi them index — Express 2025 tran 50 GB */
SELECT CAST(SUM(size) * 8.0 / 1024 / 1024 AS DECIMAL(10,2)) AS [Dung luong DB (GB)]
FROM sys.database_files WHERE type_desc = 'ROWS';
GO

PRINT '=== XONG ===';
GO

/* =========================================================================
   ❌ KHÔNG LÀM — đã đo và loại bỏ ngày 16/08/2026

   1. KHÔNG thêm index nào NỮA cho LEDGER ngoài hai cái ở mục 5, và cũng đừng
      kỳ vọng chúng cứu được nhiều. Đã đo trên chính máy chủ này, kỳ
      01/01–31/07/2026 (17,3 triệu dòng):
        - Quét trọn index IX_LEDGER_TRAN_DATE_NO (727 MB) chỉ mất 2,8 giây
          → đọc đĩa KHÔNG phải nút thắt.
        - Cùng khoảng đó, GROUP BY + SUM mất 29 giây → nút thắt là CPU.
        - Ép chạy qua từng index SẴN CÓ: 28,3s / 30,0s / 36,0s — không cái
          nào cứu được.
        - OPTION (MAXDOP 4) không đổi (15,5s so với 15,8s).
        - SÀN TUYỆT ĐỐI đo được: gom nhóm 1 cột trên index đã sắp sẵn vẫn
          mất 15,8 giây. Không index nào đưa BC005 xuống dưới ~16 giây.
      Hai index ở mục 5 KHÁC ở chỗ chúng sắp sẵn đúng thứ tự gom nhóm, để SQL
      khỏi dựng bảng băm. Đây là phép thử CHƯA ĐO ĐƯỢC TRƯỚC (muốn đo thì phải
      tạo thật). Chạy xong bấm lại báo cáo tháng 7 rồi so với số ở mục 9.
      Không cải thiện thì gỡ ra (mục 10), dữ liệu không hề gì.

   2. KHÔNG drop IX_LEDGER_ACC_DATE dù nó to nhất (442 MB). Đã đo là có lợi:
      giảm 95% số trang đọc, báo cáo cân đối từ 10-11 giây xuống 2,7-5,8 giây.

   3. KHÔNG tạo indexed view tổng hợp sẵn LEDGER. Về lý thuyết đây là thứ
      duy nhất phá được nút thắt CPU (gom 17,3 triệu dòng xuống ~500 nghìn).
      Nhưng indexed view bắt MỌI kết nối ghi vào LEDGER phải đặt đúng bộ
      SET options (ARITHABORT, ANSI_NULLS, QUOTED_IDENTIFIER...). Ứng dụng
      iPOS đặt sai một cái là NHÂN VIÊN KHÔNG LƯU ĐƯỢC CHỨNG TỪ. Chưa test
      được rủi ro này nên không đưa vào đây.

   4. KHÔNG nâng cấu hình IIS để chữa báo cáo chậm. Đã thử, không ăn thua:
      Express khoá 4 nhân, tăng hàng đợi chỉ làm nhiều người cùng đứng chờ.

   =========================================================================
   9) SỐ ĐO TRƯỚC KHI CHẠY SCRIPT — báo cáo tháng 7/2026, đo ngày 16/08/2026
      (đã bao gồm phần tối ưu code ở bản EXE mới)

        BC005 Bang can doi ke toan        44,6 giay
        BC006 Bang can doi phat sinh      28,0 giay
        BC001 KQKD theo thang             25,1 giay
        BC012 So tien mat & ngan hang     17,3 giay
        BC009 LCTT truc tiep               9,7 giay
        BC011 LCTT Chu Long                9,3 giay
        BC007 So nhat ky chung             8,7 giay
        BC013 Tong hop cong no             8,5 giay
        Danh sach chung tu tien            1,0 giay

      Chạy xong script, mở lại đúng các báo cáo này cho tháng 7 rồi so.

   =========================================================================
   10) LỆNH GỠ — nếu index không giúp được gì thì gỡ ra cho nhẹ database.
       Gỡ index KHÔNG mất dữ liệu. Cũng khoá bảng vài giây, nên chạy ngoài giờ.

DROP INDEX IX_LEDGER_RPT_BALANCE ON dbo.LEDGER;
DROP INDEX IX_LEDGER_RPT_KQKD    ON dbo.LEDGER;

       Hai index của VOUCHER thì GIỮ LẠI — chúng chắc chắn có lợi:
       DROP INDEX IX_VOUCHER_DETAIL_FR_KEY ON dbo.VOUCHER_DETAIL;   -- dung khi bat dac di
       DROP INDEX IX_VOUCHER_TRAN_DATE_NO  ON dbo.VOUCHER;          -- dung khi bat dac di
   ========================================================================= */
