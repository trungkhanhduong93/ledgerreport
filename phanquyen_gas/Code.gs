/**
 * TOOL_CHULONG — Tài khoản & phân quyền cho iPOS_Accounting_Report (LedgerReport)
 * ============================================================================
 * Sheet: bảng tính TOOL_CHULONG — link nằm trong ghi chú nội bộ, KHÔNG ghi vào repo công khai.
 *
 * NGUYÊN TẮC BẢO MẬT (đã chốt 19/09/2026):
 *  - Mật khẩu ĐƯỢC KIỂM NGAY TẠI ĐÂY. Bảng hash KHÔNG BAO GIỜ rời khỏi Google Sheet.
 *    App chỉ gửi lên user+mật khẩu, nhận về danh sách quyền. Ai moi được TOKEN trong EXE
 *    cũng chỉ thử đăng nhập được, KHÔNG tải được bảng hash về bẻ offline.
 *  - MẬT KHẨU THẬT KHÔNG BAO GIỜ ĐƯỢC GỬI LÊN ĐÂY. App băm trước 200.000 vòng
 *    (PBKDF2-HMAC-SHA256, salt = "TOOL_CHULONG|<tài khoản>") rồi gửi CHUỖI ĐÃ BĂM.
 *    Script này coi chuỗi đó như "mật khẩu" và băm tiếp 1.000 vòng với salt riêng.
 *    ⇒ Google không bao giờ thấy mật khẩu gốc, và bảng lưu ở đây vẫn được bảo vệ
 *      bằng đủ 200.000 vòng nếu bị trộm. Xem _dan_xuat_dk() trong server.py.
 *  - Mọi lệnh GHI đều bắt buộc kèm tài khoản admin + mật khẩu admin trong cùng request.
 *    TOKEN chỉ là lớp chắn bot, KHÔNG phải thứ quyết định quyền.
 *
 * CẤU TRÚC SHEET — 3 hàng tiêu đề, dữ liệu từ hàng 4:
 *    hàng 1 = nhóm cột (gộp ô, chỉ để nhìn)
 *    hàng 2 = tên tiếng Việt (chỉ để nhìn)
 *    hàng 3 = MÃ — script đọc ĐÚNG hàng này để dò cột
 *             ⇒ chèn cột / đổi chỗ cột / đổi màu thoải mái, không gãy.
 *
 * ⚠️ DEPLOY: sửa file này xong phải vào  Triển khai → Quản lý bản triển khai →
 *    bấm bút chì → Phiên bản: "Mới" → Triển khai.  BẤM "Triển khai mới" SẼ SINH URL KHÁC
 *    và mọi EXE đã phát cho nhân viên sẽ chết.
 */

// ====================== CẤU HÌNH — ĐẠI CA SỬA 2 DÒNG NÀY ======================
/** Chuỗi bí mật app gửi kèm mọi request. Đổi thành chuỗi ngẫu nhiên dài ≥ 32 ký tự. */
/** Mã bản của chính file này. `ping` trả về chuỗi này để biết **bản đang chạy
 *  trên Google có phải bản mới nhất không** — trước đây không có cách nào biết,
 *  sửa xong quên Triển khai là ngồi đoán. Đổi file này thì đổi luôn chuỗi này. */
const BAN_CODE = '2026-09-21b';

const TOKEN = 'DAN_TOKEN_NGAU_NHIEN_VAO_DAY';

/** Số vòng lặp băm PHÍA GOOGLE.
 *
 *  ⚠️ ĐỪNG NÂNG SỐ NÀY LÊN. Đo thật 19/09/2026: Apps Script chạy chậm hơn Python
 *  khoảng 2.500 lần — 10.000 vòng ở đây ngốn 9 GIÂY, đăng nhập mất 15 giây.
 *
 *  Sức mạnh chống bẻ khoá KHÔNG nằm ở con số này: app đã quay sẵn 200.000 vòng
 *  ở máy người dùng (hết 74 mili-giây) rồi mới gửi kết quả lên. Google chỉ băm
 *  thêm 1.000 vòng với salt riêng để đừng lưu thẳng cái nhận được.
 *  Kẻ trộm được cả bảng này vẫn phải trả đủ 200.000 + 1.000 vòng cho MỖI lần đoán.
 *
 *  KHÔNG đổi số này sau khi đã có người dùng — đổi là mọi mật khẩu cũ hết dùng được. */
const PBKDF2_ITER = 1000;
// ==============================================================================

/** Chuỗi băm sẵn của mật khẩu khởi tạo "admin@123" cho tài khoản "admin".
 *  App tính sẵn bằng 200.000 vòng (Apps Script quay chừng đó mất ~3 phút nên không tự tính được).
 *  Chỉ dùng đúng một lần lúc khoiTao() tạo tài khoản quản trị đầu tiên.
 *  Muốn đổi: chạy ở máy có Python —
 *    python -c "import hashlib,base64;print(base64.b64encode(hashlib.pbkdf2_hmac('sha256',b'<mat khau>',b'TOOL_CHULONG|<tai khoan>',200000)).decode())" */
const ADMIN_DK_BOOTSTRAP = 'DAN_CHUOI_BAM_ADMIN_VAO_DAY';

const SH_USER = 'User đăng nhập';
const SH_ROLE = 'Chức vụ';
const SH_LOG  = 'Nhật ký';

/** 24 mục quyền — TRÙNG KHỚP PERM_ALL_ITEMS trong server.py.
 *  Thêm báo cáo mới: thêm 1 dòng ở đây, chạy lại khoiTao() để nó chèn cột. */
const PERM = [
  { ma: 'ledger',            nhom: 'DANH SÁCH',  ten: 'Chứng từ tổng hợp' },
  { ma: 'sale',              nhom: 'DANH SÁCH',  ten: 'Chứng từ bán hàng' },
  { ma: 'voucher',           nhom: 'DANH SÁCH',  ten: 'Chứng từ tiền' },
  { ma: 'purchase',          nhom: 'DANH SÁCH',  ten: 'Chứng từ nhập kho' },
  { ma: 'warehouse',         nhom: 'DANH SÁCH',  ten: 'Chứng từ kho' },
  { ma: 'warehouse_balance', nhom: 'DANH SÁCH',  ten: 'Tồn kho thực tế' },
  { ma: 'btp_reconcile',     nhom: 'DANH SÁCH',  ten: 'Đối chiếu xuất SX BTP' },
  { ma: 'BC001', nhom: 'BÁO CÁO', ten: 'BC001 · KQKD theo tháng' },
  { ma: 'BC002', nhom: 'BÁO CÁO', ten: 'BC002 · KQKD theo công việc' },
  { ma: 'BC003', nhom: 'BÁO CÁO', ten: 'BC003 · KQKD theo tháng (tùy chỉnh)' },
  { ma: 'BC004', nhom: 'BÁO CÁO', ten: 'BC004 · KQKD theo công việc (tùy chỉnh)' },
  { ma: 'BC005', nhom: 'BÁO CÁO', ten: 'BC005 · Bảng cân đối kế toán (TT200)' },
  { ma: 'BC006', nhom: 'BÁO CÁO', ten: 'BC006 · Bảng cân đối phát sinh' },
  { ma: 'BC007', nhom: 'BÁO CÁO', ten: 'BC007 · Sổ nhật ký chung' },
  { ma: 'BC008', nhom: 'BÁO CÁO', ten: 'BC008 · Sổ chi tiết tài khoản' },
  { ma: 'BC009', nhom: 'BÁO CÁO', ten: 'BC009 · LCTT trực tiếp' },
  { ma: 'BC010', nhom: 'BÁO CÁO', ten: 'BC010 · LCTT gián tiếp' },
  { ma: 'BC011', nhom: 'BÁO CÁO', ten: 'BC011 · LCTT gián tiếp (Chú Long)' },
  { ma: 'BC012', nhom: 'BÁO CÁO', ten: 'BC012 · Sổ tiền mặt và tiền ngân hàng' },
  { ma: 'BC013', nhom: 'BÁO CÁO', ten: 'BC013 · Tổng hợp phát sinh công nợ' },
  { ma: 'BC014', nhom: 'BÁO CÁO', ten: 'BC014 · Bảng kê hóa đơn bán ra' },
  { ma: 'BC015', nhom: 'BÁO CÁO', ten: 'BC015 · Bán hàng theo nguồn đơn' },
  { ma: 'BC016', nhom: 'BÁO CÁO', ten: 'BC016 · Nhập xuất tồn Nhà hàng' },
  { ma: 'perm_admin', nhom: 'QUẢN TRỊ', ten: 'Tab Phân quyền' }
];

/** Cột của sheet "User đăng nhập" (hàng 3 = mã). */
const COT_USER = [
  { ma: 'USER_ID',       nhom: 'ĐỊNH DANH', ten: 'Tài khoản đăng nhập', rong: 130 },
  { ma: 'HO_TEN',        nhom: 'ĐỊNH DANH', ten: 'Họ và tên',            rong: 180 },
  { ma: 'CHUC_VU',       nhom: 'ĐỊNH DANH', ten: 'Chức vụ',              rong: 110 },
  { ma: 'ACTIVE',        nhom: 'ĐỊNH DANH', ten: 'Còn dùng (x)',         rong:  90 },
  { ma: 'DON_VI',        nhom: 'ĐỊNH DANH', ten: 'Đơn vị được xem (trống = tất cả)', rong: 220 },
  { ma: 'MAT_KHAU_MOI',  nhom: 'MẬT KHẨU',  ten: 'KHÔNG gõ ở đây — đặt trong app', rong: 190 },
  { ma: 'PW_HASH',       nhom: 'MẬT KHẨU',  ten: 'Hash — KHÔNG SỬA TAY', rong: 180 },
  { ma: 'SALT',          nhom: 'MẬT KHẨU',  ten: 'Salt — KHÔNG SỬA TAY', rong: 140 },
  { ma: 'DOI_MK_LUC',    nhom: 'THEO DÕI',  ten: 'Đổi mật khẩu lúc',     rong: 140 },
  { ma: 'DANG_NHAP_LUC', nhom: 'THEO DÕI',  ten: 'Đăng nhập lần cuối',   rong: 140 },
  { ma: 'GHI_CHU',       nhom: 'THEO DÕI',  ten: 'Ghi chú',              rong: 220 }
];

/** 10 chức vụ bơm sẵn — đúng PERM_MATRIX trong server.py:106. */
const CHUC_VU_MAU = [
  ['ADMIN', 'Admin (toàn quyền)',  '*'],
  ['G02',   'Kế toán tổng hợp',    'TABS,BC001-BC014'],
  ['OM',    'OM',                  'TABS,BC001-BC014'],
  ['KT01',  'Kế toán doanh thu',   'ledger,sale,BC008,BC013,BC014'],
  ['KT02',  'Kế toán tiền',        'ledger,voucher,BC008,BC012,BC013'],
  ['KT',    'Kho tổng',            'purchase,warehouse,warehouse_balance,btp_reconcile'],
  ['XSX',   'Xưởng sản xuất',      'warehouse,warehouse_balance,btp_reconcile'],
  ['TM',    'Thu mua',             'purchase,warehouse,warehouse_balance'],
  ['QLYC',  'Quản lý chuỗi',       ''],
  ['XBC',   'Xem báo cáo',         '']
];

// ============================== KHỞI TẠO SHEET ==============================

/**
 * CHẠY MỘT LẦN (trình đơn Apps Script → chọn khoiTao → Chạy).
 * Dựng tiêu đề 2 sheet, bơm 10 chức vụ mẫu, tạo sheet Nhật ký, tạo tài khoản admin đầu tiên.
 * Chạy lại lần nữa thì CHỈ thêm cột quyền còn thiếu, KHÔNG xóa dữ liệu đang có.
 */
function khoiTao() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  _dungSheetChucVu(ss);   // phải dựng TRƯỚC: dropdown Chức vụ bên sheet User trỏ vào đây
  _dungSheetUser(ss);
  _dungSheetLog(ss);
  const xong = 'Dựng xong 3 sheet. Bước tiếp: đổi TOKEN + ADMIN_DK_BOOTSTRAP ở đầu Code.gs, ' +
               'rồi Triển khai → Ứng dụng web (Thực thi: Tôi · Truy cập: Bất kỳ ai).';
  Logger.log(xong);
  // ⚠️ getUi() CHỈ gọi được khi bảng tính đang mở trong một tab. Chạy hàm này từ trình
  //    soạn thảo lúc không mở bảng tính thì nó NÉM LỖI ở đây — mà lúc đó 3 sheet đã dựng
  //    xong rồi, người dùng lại tưởng hỏng. Đã trả giá 20/09/2026.
  try { SpreadsheetApp.getUi().alert(xong); } catch (e) { /* không mở bảng tính — bỏ qua */ }
}

function _dungSheetUser(ss) {
  let sh = ss.getSheetByName(SH_USER) || ss.insertSheet(SH_USER);
  const maHienCo = _docMaCot(sh);
  if (Object.keys(maHienCo).length === 0) {
    sh.getRange(1, 1, 3, COT_USER.length).setValues([
      COT_USER.map(c => c.nhom),
      COT_USER.map(c => c.ten),
      COT_USER.map(c => c.ma)
    ]);
    COT_USER.forEach((c, i) => sh.setColumnWidth(i + 1, c.rong));
  }
  _dinhDangTieuDe(sh, COT_USER.length);
  sh.setFrozenRows(3);
  sh.setFrozenColumns(2);
  // Ô mật khẩu/hash tô xám cho biết là vùng không gõ tay
  const c = _docMaCot(sh);
  [['PW_HASH', '#efefef'], ['SALT', '#efefef']].forEach(function (p) {
    if (c[p[0]]) sh.getRange(4, c[p[0]], 200, 1).setBackground(p[1]).setFontSize(7);
  });
  // Dropdown chức vụ lấy thẳng từ sheet Chức vụ
  if (c['CHUC_VU']) {
    const rule = SpreadsheetApp.newDataValidation()
      .requireValueInRange(ss.getRangeByName('DS_CHUC_VU') ||
        (ss.getSheetByName(SH_ROLE) ? ss.getSheetByName(SH_ROLE).getRange('A4:A100') : sh.getRange('A4')), true)
      .setAllowInvalid(false).build();
    sh.getRange(4, c['CHUC_VU'], 200, 1).setDataValidation(rule);
  }
  // Tài khoản admin đầu tiên — chỉ tạo khi CHƯA CÓ dòng nào tên "admin".
  // (Đừng dựa vào getLastRow(): sheet có thể đã có tài khoản khác mà vẫn thiếu admin.)
  const b = _docBang(SH_USER);
  if (!_timUser(b, 'admin')) {
    const salt = _taoSalt();
    const row = new Array(COT_USER.length).fill('');
    row[c['USER_ID'] - 1] = 'admin';
    row[c['HO_TEN'] - 1] = 'Quản trị';
    row[c['CHUC_VU'] - 1] = 'ADMIN';
    row[c['ACTIVE'] - 1] = 'x';
    // Băm CHUỖI ĐÃ BĂM SẴN, không băm mật khẩu gốc — app cũng gửi lên đúng chuỗi này.
    row[c['PW_HASH'] - 1] = _pbkdf2(ADMIN_DK_BOOTSTRAP, salt, PBKDF2_ITER);
    row[c['SALT'] - 1] = salt;
    row[c['DOI_MK_LUC'] - 1] = _bayGio();
    row[c['GHI_CHU'] - 1] = 'Tài khoản khởi tạo — ĐỔI MẬT KHẨU NGAY (admin@123)';
    sh.getRange(sh.getLastRow() + 1, 1, 1, COT_USER.length).setValues([row]);
  }
}

function _dungSheetChucVu(ss) {
  let sh = ss.getSheetByName(SH_ROLE) || ss.insertSheet(SH_ROLE);
  const dau = [
    { ma: 'MA_CHUC_VU',  nhom: 'ĐỊNH DANH', ten: 'Mã chức vụ' },
    { ma: 'TEN_CHUC_VU', nhom: 'ĐỊNH DANH', ten: 'Tên chức vụ' }
  ];
  const tatCa = dau.concat(PERM);
  const maHienCo = _docMaCot(sh);

  if (Object.keys(maHienCo).length === 0) {
    sh.getRange(1, 1, 3, tatCa.length).setValues([
      tatCa.map(c => c.nhom), tatCa.map(c => c.ten), tatCa.map(c => c.ma)
    ]);
    sh.setColumnWidth(1, 110); sh.setColumnWidth(2, 190);
    for (let i = 3; i <= tatCa.length; i++) sh.setColumnWidth(i, 44);
    sh.getRange(2, 3, 1, PERM.length).setTextRotation(90).setVerticalAlignment('bottom');
    sh.setRowHeight(2, 200);
    // Bơm 10 chức vụ mẫu
    const rows = CHUC_VU_MAU.map(function (cv) {
      const tick = _giaiMaMau(cv[2]);
      return [cv[0], cv[1]].concat(PERM.map(p => tick.indexOf(p.ma) >= 0 ? 'x' : ''));
    });
    sh.getRange(4, 1, rows.length, tatCa.length).setValues(rows);
  } else {
    // Chạy lại: chỉ CHÈN THÊM cột quyền mới, không đụng dữ liệu cũ
    let them = 0;
    PERM.forEach(function (p) {
      if (maHienCo[p.ma]) return;
      const cot = sh.getLastColumn() + 1;
      sh.getRange(1, cot).setValue(p.nhom);
      sh.getRange(2, cot).setValue(p.ten).setTextRotation(90).setVerticalAlignment('bottom');
      sh.getRange(3, cot).setValue(p.ma);
      sh.setColumnWidth(cot, 44);
      them++;
    });
    if (them) SpreadsheetApp.getActiveSpreadsheet().toast('Đã thêm ' + them + ' cột quyền mới.');
  }
  _dinhDangTieuDe(sh, sh.getLastColumn());
  sh.setFrozenRows(3);
  sh.setFrozenColumns(2);
  // Đặt tên vùng để dropdown chức vụ bên sheet User bám theo
  try { ss.setNamedRange('DS_CHUC_VU', sh.getRange('A4:A100')); } catch (e) {}
}

function _dungSheetLog(ss) {
  let sh = ss.getSheetByName(SH_LOG);
  if (sh) return;
  sh = ss.insertSheet(SH_LOG);
  sh.getRange(1, 1, 1, 5).setValues([['Thời gian', 'Tài khoản', 'Hành động', 'Chi tiết', 'Máy']]);
  sh.getRange(1, 1, 1, 5).setFontWeight('bold').setBackground('#37474f').setFontColor('#ffffff');
  sh.setFrozenRows(1);
  [150, 130, 130, 420, 160].forEach((w, i) => sh.setColumnWidth(i + 1, w));
}

function _dinhDangTieuDe(sh, soCot) {
  sh.getRange(1, 1, 1, soCot).setFontWeight('bold').setBackground('#1e3a5f')
    .setFontColor('#ffffff').setHorizontalAlignment('center').setFontSize(9);
  sh.getRange(2, 1, 1, soCot).setFontWeight('bold').setBackground('#dbe9f6').setFontSize(8);
  sh.getRange(3, 1, 1, soCot).setFontSize(7).setFontColor('#9e9e9e')
    .setBackground('#f5f5f5').setHorizontalAlignment('center');
}

/** '*' = tất cả · 'TABS' = 7 tab danh sách · 'BC001-BC014' = dải · còn lại liệt kê thẳng. */
function _giaiMaMau(mau) {
  if (mau === '*') return PERM.map(p => p.ma);
  const out = [];
  (mau || '').split(',').forEach(function (t) {
    t = t.trim();
    if (!t) return;
    if (t === 'TABS') { PERM.filter(p => p.nhom === 'DANH SÁCH').forEach(p => out.push(p.ma)); return; }
    const m = t.match(/^BC(\d+)-BC(\d+)$/);
    if (m) {
      for (let i = +m[1]; i <= +m[2]; i++) out.push('BC' + ('00' + i).slice(-3));
      return;
    }
    out.push(t);
  });
  return out;
}

// ============================== BĂM MẬT KHẨU ==============================

/** Chuỗi → mảng byte UTF-8.
 *  ⚠️ BẮT BUỘC: Utilities.computeHmacSha256Signature chỉ có 2 dạng hợp lệ —
 *  (String, String) hoặc (Byte[], Byte[]). Trộn Byte[] với String là ném lỗi
 *  "The parameters (number[],String) don't match the method signature".
 *  Đã trả giá 19/09/2026 khi chạy khoiTao lần đầu. */
function _byteCuaChuoi(s) {
  return Utilities.newBlob(String(s == null ? '' : s)).getBytes();
}

/** PBKDF2-HMAC-SHA256, dkLen = 32 byte (đúng 1 block ⇒ không cần vòng ngoài). */
function _pbkdf2(matKhau, saltB64, soVong) {
  const khoa = _byteCuaChuoi(matKhau);
  const salt = Utilities.base64Decode(saltB64);
  let u = Utilities.computeHmacSha256Signature(salt.concat([0, 0, 0, 1]), khoa);
  const t = u.slice();
  for (let i = 1; i < soVong; i++) {
    u = Utilities.computeHmacSha256Signature(u, khoa);
    for (let j = 0; j < 32; j++) t[j] ^= u[j];
  }
  return Utilities.base64Encode(t);
}

function _taoSalt() {
  const hex = (Utilities.getUuid() + Utilities.getUuid()).replace(/-/g, '').slice(0, 32);
  const b = [];
  for (let i = 0; i < 32; i += 2) {
    let v = parseInt(hex.substr(i, 2), 16);
    b.push(v > 127 ? v - 256 : v);
  }
  return Utilities.base64Encode(b);
}

/** So sánh không lệ thuộc thời gian (chống dò từng ký tự). */
function _soBang(a, b) {
  a = String(a || ''); b = String(b || '');
  if (a.length !== b.length) return false;
  let kq = 0;
  for (let i = 0; i < a.length; i++) kq |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return kq === 0;
}

/**
 * CHẠY TAY để chốt PBKDF2_ITER. In ra thời gian băm ở vài mức vòng lặp,
 * rồi gợi ý mức cao nhất mà vẫn ≤ 800 mili-giây.
 */
function doTocDo() {
  const salt = _taoSalt();
  const mucThu = [1000, 5000, 10000, 20000, 50000];
  let goiY = mucThu[0], dong = ['Số vòng\tThời gian'];
  mucThu.forEach(function (n) {
    const t0 = Date.now();
    _pbkdf2('mat_khau_thu_nghiem_123', salt, n);
    const ms = Date.now() - t0;
    dong.push(n + '\t' + ms + ' ms');
    if (ms <= 800) goiY = n;
  });
  const kq = dong.join('\n') + '\n\n➡️ Điền vào PBKDF2_ITER: ' + goiY;
  Logger.log(kq);
  try { SpreadsheetApp.getUi().alert(kq); } catch (e) {}
  return goiY;
}

// ============================== ĐỌC / GHI SHEET ==============================

/** hàng 3 → { MÃ: số thứ tự cột (bắt đầu từ 1) } */
function _docMaCot(sh) {
  const map = {};
  if (sh.getLastRow() < 3 || sh.getLastColumn() < 1) return map;
  const hang = sh.getRange(3, 1, 1, sh.getLastColumn()).getValues()[0];
  hang.forEach(function (v, i) {
    v = String(v || '').trim();
    if (v) map[v] = i + 1;
  });
  return map;
}

function _docBang(ten) {
  const sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(ten);
  if (!sh) throw new Error('Không tìm thấy sheet "' + ten + '"');
  const cot = _docMaCot(sh);
  const soDong = Math.max(0, sh.getLastRow() - 3);
  const dulieu = soDong ? sh.getRange(4, 1, soDong, sh.getLastColumn()).getValues() : [];
  return { sh: sh, cot: cot, rows: dulieu };
}

function _o(bang, dong, ma) {
  const c = bang.cot[ma];
  return c ? String(dong[c - 1] == null ? '' : dong[c - 1]).trim() : '';
}

function _bayGio() {
  return Utilities.formatDate(new Date(), 'Asia/Ho_Chi_Minh', 'dd/MM/yyyy HH:mm:ss');
}

function _ghiLog(taiKhoan, hanhDong, chiTiet, may) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let sh = ss.getSheetByName(SH_LOG);
    if (!sh) { _dungSheetLog(ss); sh = ss.getSheetByName(SH_LOG); }
    sh.appendRow([_bayGio(), taiKhoan || '?', hanhDong, chiTiet || '', may || '']);
  } catch (e) { /* log hỏng thì thôi, không được làm chết request */ }
}

/** Quyền của 1 chức vụ = danh sách mã có đánh dấu trên sheet Chức vụ. */
function _quyenChucVu(maChucVu) {
  const b = _docBang(SH_ROLE);
  for (let i = 0; i < b.rows.length; i++) {
    if (_o(b, b.rows[i], 'MA_CHUC_VU').toUpperCase() !== String(maChucVu || '').toUpperCase()) continue;
    const items = [];
    PERM.forEach(function (p) {
      if (_o(b, b.rows[i], p.ma)) items.push(p.ma);
    });
    return { ten: _o(b, b.rows[i], 'TEN_CHUC_VU'), items: items };
  }
  return null;
}

/** Tìm user (không phân biệt hoa/thường). Trả { dong, soDong } hoặc null. */
function _timUser(bang, userId) {
  const uid = String(userId || '').trim().toLowerCase();
  if (!uid) return null;
  for (let i = 0; i < bang.rows.length; i++) {
    if (_o(bang, bang.rows[i], 'USER_ID').toLowerCase() === uid) {
      return { dong: bang.rows[i], soDong: i + 4 };
    }
  }
  return null;
}

/** Xác thực 1 tài khoản. Trả object mô tả user, hoặc null nếu sai. */
function _xacThuc(userId, matKhau) {
  const b = _docBang(SH_USER);
  const u = _timUser(b, userId);
  if (!u) return null;
  if (!_o(b, u.dong, 'ACTIVE')) return { khoa: true };
  const salt = _o(b, u.dong, 'SALT');
  const hash = _o(b, u.dong, 'PW_HASH');
  if (!salt || !hash) return null;
  if (!_soBang(_pbkdf2(String(matKhau || ''), salt, PBKDF2_ITER), hash)) return null;
  const maCV = _o(b, u.dong, 'CHUC_VU');
  const cv = _quyenChucVu(maCV) || { ten: '', items: [] };
  const dv = _o(b, u.dong, 'DON_VI');
  return {
    bang: b, soDong: u.soDong,
    id: _o(b, u.dong, 'USER_ID'),
    ho_ten: _o(b, u.dong, 'HO_TEN'),
    chuc_vu: maCV,
    ten_chuc_vu: cv.ten,
    items: cv.items,
    don_vi: dv ? dv.split(',').map(s => s.trim()).filter(String) : null  // null = xem tất cả
  };
}

/** Xác thực và đòi quyền quản trị. Ném lỗi nếu không đạt. */
function _doiAdmin(p) {
  // Dò mật khẩu ADMIN là nguy nhất (vào được là đọc/sửa được cả bảng tài khoản)
  // nên chịu chung lưới với đăng nhập thường.
  const conKhoa = _conBiKhoa_(p.admin_user);
  if (conKhoa) throw new Error(_loiTamKhoa_(conKhoa));
  const a = _xacThuc(p.admin_user, p.admin_pass);
  if (!a || a.khoa || a.items.indexOf('perm_admin') < 0) {
    const vuaKhoa = _ghiLanSai_(p.admin_user);
    throw new Error(vuaKhoa ? _loiTamKhoa_(KHOA_PHAT_S) : 'Tài khoản quản trị không hợp lệ');
  }
  _xoaLanSai_(p.admin_user);
  return a;
}

/** Đếm số admin đang hoạt động — dùng cho lưới chống tự khóa mất admin cuối. */
function _demAdmin(truUser) {
  const b = _docBang(SH_USER);
  let n = 0;
  b.rows.forEach(function (r) {
    const uid = _o(b, r, 'USER_ID');
    if (!uid || !_o(b, r, 'ACTIVE')) return;
    if (truUser && uid.toLowerCase() === String(truUser).toLowerCase()) return;
    const cv = _quyenChucVu(_o(b, r, 'CHUC_VU'));
    if (cv && cv.items.indexOf('perm_admin') >= 0) n++;
  });
  return n;
}

// ============================== CỔNG HTTP ==============================

function doGet() {
  return ContentService.createTextOutput('TOOL_CHULONG — dich vu phan quyen. Dung POST.')
    .setMimeType(ContentService.MimeType.TEXT);
}

function doPost(e) {
  let p = {};
  try {
    p = JSON.parse((e && e.postData && e.postData.contents) || '{}');
  } catch (err) {
    return _traLoi({ ok: false, loi: 'Nội dung gửi lên không phải JSON' });
  }
  if (!_soBang(p.token, TOKEN)) {
    return _traLoi({ ok: false, loi: 'Sai token' });
  }

  const khoa = LockService.getScriptLock();
  try {
    khoa.waitLock(20000);
  } catch (err) {
    return _traLoi({ ok: false, loi: 'Máy khác đang ghi, thử lại sau vài giây' });
  }

  try {
    switch (p.hanh_dong) {
      case 'dang_nhap':    return _traLoi(_apiDangNhap(p));
      case 'nap':          return _traLoi(_apiNap(p));
      case 'luu_user':     return _traLoi(_apiLuuUser(p));
      case 'xoa_user':     return _traLoi(_apiXoaUser(p));
      case 'dat_mat_khau': return _traLoi(_apiDatMatKhau(p));
      case 'luu_chuc_vu':  return _traLoi(_apiLuuChucVu(p));
      case 'xoa_chuc_vu':  return _traLoi(_apiXoaChucVu(p));
      case 'ping':         return _traLoi({ ok: true, iter: PBKDF2_ITER, gio: _bayGio(),
                                            ban: BAN_CODE, co_ratelimit: true });
      default:             return _traLoi({ ok: false, loi: 'Không hiểu hành động: ' + p.hanh_dong });
    }
  } catch (err) {
    return _traLoi({ ok: false, loi: String(err && err.message || err) });
  } finally {
    khoa.releaseLock();
  }
}

function _traLoi(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

// ============================== CÁC HÀNH ĐỘNG ==============================

// ====================== CHỐNG DÒ MẬT KHẨU ======================
// Từ 21/09/2026 TOKEN được **ghim cứng trong mã nguồn của repo CÔNG KHAI**
// (để chỉ phải phát một file EXE). Nghĩa là ai cũng gọi được API này.
// Token chỉ còn là lớp chắn bot — **đây mới là chỗ thực sự chặn kẻ dò mật khẩu.**
//
// Đo thật 21/09/2026: không có giới hạn thì dò được ~1.800 lần/giờ (mỗi lần kẻ tấn
// công phải tự quay 200.000 vòng PBKDF2 ~95ms + chờ Apps Script ~2 giây).
// Với mốc dưới đây còn **32 lần/giờ cho mỗi tài khoản** — giảm 56 lần.
//
// ⚠️ CỐ Ý chỉ khoá **theo từng tài khoản**, KHÔNG khoá toàn cục. Khoá toàn cục thì
//    một kẻ rảnh rỗi gõ bậy vài chục lần là **khoá được cả công ty** — đổi một lỗ nhỏ
//    lấy một lỗ to hơn.
//
// Dùng CacheService (tự hết hạn, không đụng Sheet nên không làm chậm đăng nhập).
// Mất dữ liệu cache khi Google dọn ⇒ bộ đếm về 0. Chấp nhận được: đây là lưới
// làm chậm kẻ dò, không phải cổng khoá.
const KHOA_SO_LAN   = 8;     // sai bao nhiêu lần thì khoá
const KHOA_CUA_SO_S = 900;   // đếm trong bao lâu (giây) — 15 phút
const KHOA_PHAT_S   = 900;   // khoá bao lâu (giây) — 15 phút

function _khoaDem_(user) {
  return 'dnsai_' + String(user || '').trim().toLowerCase().slice(0, 120);
}

/** Số giây còn bị khoá; 0 = không bị khoá. */
function _conBiKhoa_(user) {
  try {
    const m = CacheService.getScriptCache().get(_khoaDem_(user) + '_k');
    if (!m) return 0;
    const con = Math.ceil((Number(m) - Date.now()) / 1000);
    return con > 0 ? con : 0;
  } catch (e) { return 0; }   // cache hỏng thì cho qua, đừng chặn người thật
}

/** Ghi một lần sai. Trả true nếu lần này làm tài khoản bị khoá. */
function _ghiLanSai_(user) {
  try {
    const c = CacheService.getScriptCache();
    const k = _khoaDem_(user);
    const n = Number(c.get(k) || 0) + 1;
    if (n >= KHOA_SO_LAN) {
      c.put(k + '_k', String(Date.now() + KHOA_PHAT_S * 1000), KHOA_PHAT_S);
      c.remove(k);
      return true;
    }
    c.put(k, String(n), KHOA_CUA_SO_S);
    return false;
  } catch (e) { return false; }
}

/** Đăng nhập đúng ⇒ xoá bộ đếm, khỏi cộng dồn từ mấy lần gõ nhầm cũ. */
function _xoaLanSai_(user) {
  try { CacheService.getScriptCache().remove(_khoaDem_(user)); } catch (e) {}
}

function _loiTamKhoa_(giay) {
  return 'Tài khoản tạm khoá do nhập sai quá ' + KHOA_SO_LAN + ' lần. '
       + 'Thử lại sau ' + Math.ceil(giay / 60) + ' phút.';
}

function _apiDangNhap(p) {
  const conKhoa = _conBiKhoa_(p.user);
  if (conKhoa) {
    // KHÔNG ghi log ở đây: đang bị dò thì mỗi lần gõ là một dòng, sheet Nhật ký
    // phình vô ích. Dòng báo khoá đã ghi đúng một lần lúc bắt đầu khoá.
    return { ok: false, loi: _loiTamKhoa_(conKhoa) };
  }
  const u = _xacThuc(p.user, p.mat_khau);
  if (!u) {
    const vuaKhoa = _ghiLanSai_(p.user);
    _ghiLog(p.user, 'ĐĂNG NHẬP HỎNG',
            vuaKhoa ? ('sai ' + KHOA_SO_LAN + ' lần → tạm khoá '
                       + Math.round(KHOA_PHAT_S / 60) + ' phút')
                    : 'sai tài khoản hoặc mật khẩu', p.may);
    return { ok: false,
             loi: vuaKhoa ? _loiTamKhoa_(KHOA_PHAT_S) : 'Sai tài khoản hoặc mật khẩu' };
  }
  if (u.khoa) {
    _ghiLog(p.user, 'ĐĂNG NHẬP HỎNG', 'tài khoản đã khóa', p.may);
    return { ok: false, loi: 'Tài khoản đã bị khóa' };
  }
  _xoaLanSai_(p.user);
  _xoaLanSai_(u.id);
  const c = u.bang.cot['DANG_NHAP_LUC'];
  if (c) u.bang.sh.getRange(u.soDong, c).setValue(_bayGio());
  _ghiLog(u.id, 'ĐĂNG NHẬP', u.chuc_vu + ' · ' + u.items.length + ' mục', p.may);
  return {
    ok: true,
    user: {
      id: u.id, ho_ten: u.ho_ten, chuc_vu: u.chuc_vu, ten_chuc_vu: u.ten_chuc_vu,
      items: u.items, don_vi: u.don_vi
    }
  };
}

/** Nạp toàn bộ danh sách user + chức vụ cho tab Phân quyền. KHÔNG trả hash/salt. */
function _apiNap(p) {
  _doiAdmin(p);
  const bu = _docBang(SH_USER);
  const users = [];
  bu.rows.forEach(function (r) {
    const uid = _o(bu, r, 'USER_ID');
    if (!uid) return;
    const dv = _o(bu, r, 'DON_VI');
    users.push({
      id: uid,
      ho_ten: _o(bu, r, 'HO_TEN'),
      chuc_vu: _o(bu, r, 'CHUC_VU'),
      active: !!_o(bu, r, 'ACTIVE'),
      don_vi: dv ? dv.split(',').map(s => s.trim()).filter(String) : null,
      co_mat_khau: !!_o(bu, r, 'PW_HASH'),
      dang_nhap_luc: _o(bu, r, 'DANG_NHAP_LUC'),
      ghi_chu: _o(bu, r, 'GHI_CHU')
    });
  });

  const br = _docBang(SH_ROLE);
  const chucVu = [];
  br.rows.forEach(function (r) {
    const ma = _o(br, r, 'MA_CHUC_VU');
    if (!ma) return;
    chucVu.push({
      ma: ma, ten: _o(br, r, 'TEN_CHUC_VU'),
      items: PERM.filter(q => _o(br, r, q.ma)).map(q => q.ma)
    });
  });
  return { ok: true, users: users, chuc_vu: chucVu, tat_ca_muc: PERM };
}

function _apiLuuUser(p) {
  const admin = _doiAdmin(p);
  const uid = String(p.user_id || '').trim();
  if (!uid) return { ok: false, loi: 'Thiếu tài khoản' };
  if (!/^[A-Za-z0-9_.]{3,30}$/.test(uid)) {
    return { ok: false, loi: 'Tài khoản chỉ gồm chữ, số, dấu chấm, gạch dưới (3–30 ký tự)' };
  }
  if (p.chuc_vu && !_quyenChucVu(p.chuc_vu)) {
    return { ok: false, loi: 'Chức vụ "' + p.chuc_vu + '" không có trong sheet Chức vụ' };
  }

  const b = _docBang(SH_USER);
  const cu = _timUser(b, uid);
  const moi = !cu;
  const soDong = cu ? cu.soDong : b.sh.getLastRow() + 1;

  // Lưới: không cho hạ quyền / khóa admin cuối cùng
  if (!moi) {
    const dangLaAdmin = (_quyenChucVu(_o(b, cu.dong, 'CHUC_VU')) || { items: [] }).items.indexOf('perm_admin') >= 0;
    const conLaAdmin = (_quyenChucVu(p.chuc_vu) || { items: [] }).items.indexOf('perm_admin') >= 0;
    const conBat = p.active !== false;
    if (dangLaAdmin && (!conLaAdmin || !conBat) && _demAdmin(uid) === 0) {
      return { ok: false, loi: 'Đây là tài khoản quản trị cuối cùng — không thể hạ quyền hoặc khóa' };
    }
  }

  // ⚠️ KIỂM TRƯỚC KHI GHI. Bản cũ ghi USER_ID / họ tên / chức vụ / đơn vị vào Sheet
  //    RỒI MỚI kiểm "tài khoản mới phải có mật khẩu" ⇒ tạo tài khoản mà quên gõ mật
  //    khẩu thì Sheet đã có sẵn một dòng KHÔNG CÓ PW_HASH (tài khoản ma). Tệ hơn: lần
  //    lưu sau `moi` thành false nên không còn bắt buộc mật khẩu nữa.
  //    Không đăng nhập được bằng dòng đó (_xacThuc đòi cả salt lẫn hash) nhưng là rác
  //    trên Sheet và làm người dùng tưởng đã tạo xong. Phát hiện 21/09/2026 khi test.
  if (moi && !p.mat_khau) return { ok: false, loi: 'Tài khoản mới phải có mật khẩu' };

  const ghi = function (ma, gt) {
    const c = b.cot[ma];
    if (c) b.sh.getRange(soDong, c).setValue(gt);
  };
  ghi('USER_ID', uid);
  if (p.ho_ten !== undefined) ghi('HO_TEN', p.ho_ten);
  if (p.chuc_vu !== undefined) ghi('CHUC_VU', p.chuc_vu);
  if (p.active !== undefined) ghi('ACTIVE', p.active ? 'x' : '');
  if (p.don_vi !== undefined) ghi('DON_VI', (p.don_vi || []).join(','));
  if (p.ghi_chu !== undefined) ghi('GHI_CHU', p.ghi_chu);

  // ⚠️ SỬA 21/09/2026 — BẢN CŨ CHỈ ĐẶT MẬT KHẨU KHI `moi === true`.
  //
  //    Hậu quả: ô "Mật khẩu mới" trong modal **Sửa** của app gửi lên đây rồi bị
  //    **vứt đi trong im lặng** — app báo "Lưu thành công", Sheet cập nhật tên/chức vụ/
  //    đơn vị, nhưng cột PW_HASH KHÔNG HỀ ĐỔI. Người dùng đổi mật khẩu xong thì
  //    không vào được bằng mật khẩu mới — mà vẫn vào được bằng mật khẩu CŨ.
  //    **Đã vấp thật 21/09/2026 với chính tài khoản admin.**
  //
  //    Nay: tài khoản mới thì **bắt buộc** có mật khẩu; tài khoản cũ thì đặt lại
  //    **khi nào có gửi lên** (để trống = giữ nguyên, đúng như nhãn trên modal).
  const doiMK = !!p.mat_khau;
  if (doiMK) {
    const kq = _doiMatKhauDong(b, soDong, p.mat_khau);
    if (!kq.ok) return kq;
  }
  _ghiLog(admin.id, moi ? 'TẠO USER' : 'SỬA USER',
    uid + ' · chức vụ ' + (p.chuc_vu || '') + ' · đơn vị ' + ((p.don_vi || []).join(',') || 'tất cả')
       + (doiMK && !moi ? ' · ĐỔI MẬT KHẨU' : ''), p.may);
  return { ok: true, user_id: uid, moi: moi, doi_mat_khau: doiMK };
}

function _apiXoaUser(p) {
  const admin = _doiAdmin(p);
  const uid = String(p.user_id || '').trim();
  const b = _docBang(SH_USER);
  const u = _timUser(b, uid);
  if (!u) return { ok: false, loi: 'Không có tài khoản "' + uid + '"' };
  if (_demAdmin(uid) === 0) {
    return { ok: false, loi: 'Đây là tài khoản quản trị cuối cùng — không thể xóa' };
  }
  b.sh.deleteRow(u.soDong);
  _ghiLog(admin.id, 'XÓA USER', uid, p.may);
  return { ok: true };
}

/** Đổi mật khẩu. Admin đổi cho người khác, hoặc chính chủ đổi (phải kèm mật khẩu cũ). */
function _apiDatMatKhau(p) {
  const uid = String(p.user_id || '').trim();
  let nguoiLam;
  if (p.mat_khau_cu) {
    // ⚠️ Đường này MIỄN kiểm quyền bên server.py (nằm trong PERM_PUBLIC) nên bất kỳ ai
    //    đăng nhập được cũng gọi được với `user_id` của NGƯỜI KHÁC. Không đếm lần sai ở
    //    đây thì nó thành đường dò mật khẩu **VÒNG QUA** rate limit của _apiDangNhap:
    //    gõ sai bao nhiêu lần cũng được. Phải chịu chung lưới.
    const conKhoa = _conBiKhoa_(uid);
    if (conKhoa) return { ok: false, loi: _loiTamKhoa_(conKhoa) };
    const tu = _xacThuc(uid, p.mat_khau_cu);
    if (!tu || tu.khoa) {
      const vuaKhoa = _ghiLanSai_(uid);
      return { ok: false,
               loi: vuaKhoa ? _loiTamKhoa_(KHOA_PHAT_S) : 'Mật khẩu hiện tại không đúng' };
    }
    _xoaLanSai_(uid);
    nguoiLam = tu.id;
  } else {
    nguoiLam = _doiAdmin(p).id;
  }
  const b = _docBang(SH_USER);
  const u = _timUser(b, uid);
  if (!u) return { ok: false, loi: 'Không có tài khoản "' + uid + '"' };
  const kq = _doiMatKhauDong(b, u.soDong, p.mat_khau_moi);
  if (!kq.ok) return kq;
  _ghiLog(nguoiLam, 'ĐỔI MẬT KHẨU', uid, p.may);
  return { ok: true };
}

function _doiMatKhauDong(b, soDong, matKhau) {
  matKhau = String(matKhau || '');
  if (matKhau.length < 6) return { ok: false, loi: 'Mật khẩu phải từ 6 ký tự trở lên' };
  const salt = _taoSalt();
  b.sh.getRange(soDong, b.cot['SALT']).setValue(salt);
  b.sh.getRange(soDong, b.cot['PW_HASH']).setValue(_pbkdf2(matKhau, salt, PBKDF2_ITER));
  if (b.cot['DOI_MK_LUC']) b.sh.getRange(soDong, b.cot['DOI_MK_LUC']).setValue(_bayGio());
  if (b.cot['MAT_KHAU_MOI']) b.sh.getRange(soDong, b.cot['MAT_KHAU_MOI']).clearContent();
  return { ok: true };
}

function _apiLuuChucVu(p) {
  const admin = _doiAdmin(p);
  const ma = String(p.ma || '').trim().toUpperCase();
  if (!/^[A-Z0-9_]{2,15}$/.test(ma)) {
    return { ok: false, loi: 'Mã chức vụ chỉ gồm chữ HOA, số, gạch dưới (2–15 ký tự)' };
  }
  const items = p.items || [];
  const b = _docBang(SH_ROLE);
  let soDong = 0;
  for (let i = 0; i < b.rows.length; i++) {
    if (_o(b, b.rows[i], 'MA_CHUC_VU').toUpperCase() === ma) { soDong = i + 4; break; }
  }
  // Sửa chức vụ đang có: không cho bỏ perm_admin nếu nó giữ admin cuối
  if (soDong && items.indexOf('perm_admin') < 0) {
    const cu = _quyenChucVu(ma);
    if (cu && cu.items.indexOf('perm_admin') >= 0) {
      const conAi = _demAdmin(null);
      const bu = _docBang(SH_USER);
      const thuocChucVuNay = bu.rows.filter(function (r) {
        return _o(bu, r, 'ACTIVE') && _o(bu, r, 'CHUC_VU').toUpperCase() === ma;
      }).length;
      if (conAi - thuocChucVuNay <= 0) {
        return { ok: false, loi: 'Bỏ quyền Phân quyền của chức vụ này sẽ không còn ai quản trị được' };
      }
    }
  }
  if (!soDong) soDong = b.sh.getLastRow() + 1;
  b.sh.getRange(soDong, b.cot['MA_CHUC_VU']).setValue(ma);
  if (p.ten !== undefined) b.sh.getRange(soDong, b.cot['TEN_CHUC_VU']).setValue(p.ten);
  PERM.forEach(function (q) {
    const c = b.cot[q.ma];
    if (c) b.sh.getRange(soDong, c).setValue(items.indexOf(q.ma) >= 0 ? 'x' : '');
  });
  _ghiLog(admin.id, 'LƯU CHỨC VỤ', ma + ' · ' + items.length + ' mục', p.may);
  return { ok: true, ma: ma };
}

function _apiXoaChucVu(p) {
  const admin = _doiAdmin(p);
  const ma = String(p.ma || '').trim().toUpperCase();
  const bu = _docBang(SH_USER);
  const dangDung = bu.rows.filter(r => _o(bu, r, 'CHUC_VU').toUpperCase() === ma).length;
  if (dangDung) {
    return { ok: false, loi: 'Còn ' + dangDung + ' tài khoản đang giữ chức vụ này' };
  }
  const b = _docBang(SH_ROLE);
  for (let i = 0; i < b.rows.length; i++) {
    if (_o(b, b.rows[i], 'MA_CHUC_VU').toUpperCase() === ma) {
      b.sh.deleteRow(i + 4);
      _ghiLog(admin.id, 'XÓA CHỨC VỤ', ma, p.may);
      return { ok: true };
    }
  }
  return { ok: false, loi: 'Không có chức vụ "' + ma + '"' };
}

// ============================== GÕ MẬT KHẨU TRÊN SHEET ==============================

/**
 * Chặn gõ mật khẩu thẳng trên Sheet.
 *
 * Vì sao bỏ đường này: mật khẩu giờ được app băm 200.000 vòng TRƯỚC KHI gửi lên,
 * mà Apps Script quay 200.000 vòng mất khoảng 3 PHÚT (đo thật 19/09/2026) nên
 * không thể tạo ra cùng một giá trị. Gõ tay ở đây sẽ sinh hash KHÔNG khớp và
 * người đó mất luôn đường đăng nhập.
 *
 * Tiện thể được thêm một cái lợi: mật khẩu không còn nằm lại trong Lịch sử phiên
 * bản của Google Sheet nữa.
 */
function onEdit(e) {
  try {
    const sh = e.range.getSheet();
    if (sh.getName() !== SH_USER) return;
    if (e.range.getRow() < 4) return;
    const cot = _docMaCot(sh);
    if (e.range.getColumn() !== cot['MAT_KHAU_MOI']) return;
    if (!String(e.value || '').trim()) return;

    e.range.clearContent();
    SpreadsheetApp.getActiveSpreadsheet().toast(
      'Không đặt mật khẩu ở đây được. Vào tab Phân quyền của phần mềm để đặt.', 'Đã bỏ qua', 8);
  } catch (err) {
    SpreadsheetApp.getActiveSpreadsheet().toast('Lỗi: ' + err.message);
  }
}
