# -*- coding: utf-8 -*-
"""Chuẩn bị nội dung Code.gs để DÁN lên Google Apps Script.

⛔ ĐỪNG dán thẳng phanquyen_gas/Code.gs lên Google.

Repo này CÔNG KHAI nên file Code.gs trong repo cố tình để hai hằng bí mật ở dạng
chuỗi giữ chỗ:

    const TOKEN = 'DAN_TOKEN_NGAU_NHIEN_VAO_DAY';
    const ADMIN_DK_BOOTSTRAP = 'DAN_CHUOI_BAM_ADMIN_VAO_DAY';

Dán thẳng file đó lên Google = **ghi đè TOKEN thật bằng chuỗi giữ chỗ**. Bản trong
editor hỏng ngay; và lần Triển khai kế tiếp là **toàn bộ EXE đã phát mất kết nối**,
vì token trong EXE không còn khớp token trên Google.
Đã vấp thật 21/09/2026 — cứu được chỉ vì lúc đó chưa bấm Triển khai.

Script này đọc Code.gs, thay TOKEN bằng giá trị thật lấy từ `ketnoi.json` (file đã
.gitignore, nằm ngoài repo công khai), rồi đưa kết quả vào CLIPBOARD để dán.

    python phanquyen_gas/chuan_bi_deploy.py

⚠️ KHÔNG ghi kết quả ra file trong repo — nó chứa token thật.

Sau khi dán lên Apps Script:
  1. Ctrl+S để lưu
  2. Triển khai → **Quản lý bản triển khai** → ✏️ → Phiên bản: **Mới** → Triển khai
     ⛔ ĐỪNG bấm "Triển khai mới" — sinh URL khác, mọi EXE đã phát sẽ chết.
  3. Kiểm lại bằng `ping`: kết quả phải có "ban" đúng bằng BAN_CODE trong file này.

ADMIN_DK_BOOTSTRAP không được khôi phục ở đây: nó chỉ dùng MỘT LẦN lúc khoiTao()
sinh tài khoản quản trị đầu tiên. Sheet đã có admin nên để nguyên chuỗi giữ chỗ là
vô hại. Cần dựng lại từ đầu thì tự điền tay trước khi chạy khoiTao().
"""
import io
import json
import os
import re
import subprocess
import sys

THU_MUC = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.dirname(THU_MUC)
CODE_GS = os.path.join(THU_MUC, 'Code.gs')
KETNOI = os.path.join(GOC, 'ketnoi.json')

GIU_CHO = 'DAN_TOKEN_NGAU_NHIEN_VAO_DAY'


def main():
    if not os.path.exists(KETNOI):
        print('[LOI] Khong thay ketnoi.json canh repo. File nay chua TOKEN that.')
        return 1

    ma = io.open(CODE_GS, encoding='utf-8').read()
    token = (json.load(io.open(KETNOI, encoding='utf-8')) or {}).get('token', '')
    if not token:
        print('[LOI] ketnoi.json khong co truong "token".')
        return 1

    cu = "const TOKEN = '%s';" % GIU_CHO
    if cu not in ma:
        hien = re.search(r"const TOKEN = '([^']*)'", ma)
        if hien and hien.group(1) == token:
            print('[OK ] Code.gs da mang token that san — khong can thay.')
        else:
            print('[LOI] Khong thay dong TOKEN giu cho, cung khong phai token that.')
            print('      Kiem lai dong `const TOKEN = ...` trong Code.gs.')
            return 1
    else:
        ma = ma.replace(cu, "const TOKEN = '%s';" % token)
        print('[OK ] Da thay chuoi giu cho bang TOKEN that.')

    ban = re.search(r"const BAN_CODE = '([^']*)'", ma)
    print('[OK ] BAN_CODE = %s  (sau khi Trien khai, ping phai tra dung chuoi nay)'
          % (ban.group(1) if ban else '(khong co)'))
    print('[OK ] Do dai noi dung: %d ky tu' % len(ma))

    if GIU_CHO in ma:
        print('[LOI] Van con chuoi giu cho trong noi dung — DUNG dan len Google.')
        return 1

    # Dua vao clipboard bang PowerShell (khong qua file trung gian — file do se chua TOKEN that).
    #
    # ⛔ BAT BUOC dat [Console]::InputEncoding = UTF8 TRUOC khi doc stdin.
    #    Thieu dong do thi PowerShell giai ma stdin theo bang ma ANSI cua console (cp1252 tren
    #    may nay), nen moi ky tu tieng Viet bien thanh rac kieu 'Cháº¡n gá»­i'. Da vap that
    #    21/09/2026: dan len Apps Script thi TOAN BO chu tieng Viet trong Code.gs hong —
    #    ke ca cac chuoi thong bao loi hien cho nguoi dung. Phat hien kip vi nhin man hinh
    #    truoc khi Ctrl+S; neu luu roi Trien khai la ca cong ty nhan thong bao loi rac.
    try:
        p = subprocess.Popen(
            ['powershell', '-NoProfile', '-Command',
             '[Console]::InputEncoding=[System.Text.Encoding]::UTF8; '
             '$i=[Console]::In.ReadToEnd(); Set-Clipboard -Value $i'],
            stdin=subprocess.PIPE)
        p.communicate(ma.encode('utf-8'))
        if p.returncode != 0:
            raise RuntimeError('PowerShell tra ma loi %s' % p.returncode)
    except Exception as e:
        print('[LOI] Khong dua duoc vao clipboard: %s' % e)
        return 1

    # Doc NGUOC clipboard ra va doi chieu — khong tin lenh copy (cung tinh than voi
    # Sync-And-Backup.ps1: doi chieu hash tung file, khong tin lenh copy).
    try:
        r = subprocess.run(
            ['powershell', '-NoProfile', '-Command',
             '[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; Get-Clipboard -Raw'],
            capture_output=True)
        lay = r.stdout.decode('utf-8', 'replace').replace('\r\n', '\n').strip()
        if lay != ma.replace('\r\n', '\n').strip():
            print('[LOI] Clipboard KHONG khop noi dung goc — DUNG dan len Google.')
            print('      Dai khai: %d ky tu goc vs %d ky tu trong clipboard.' % (len(ma), len(lay)))
            return 1
        print('[OK ] Da doc nguoc clipboard va doi chieu: KHOP tung ky tu (ke ca tieng Viet).')
    except Exception as e:
        print('[LOI] Khong doi chieu duoc clipboard: %s' % e)
        return 1

    print()
    print('=> Da nam trong CLIPBOARD. Gio sang Apps Script:')
    print('   Ctrl+A trong o code  ->  Ctrl+V  ->  Ctrl+S')
    print('   roi Trien khai -> Quan ly ban trien khai -> but chi -> Phien ban "Moi"')
    print('   (DUNG bam "Trien khai moi")')
    return 0


if __name__ == '__main__':
    sys.exit(main())
