import pyodbc
import logging
logger = logging.getLogger(__name__)
import threading
global_db_lock = threading.RLock()
from functools import wraps

def with_db_lock(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        with global_db_lock:
            # Thử lần 1
            resp = f(*args, **kwargs)
            
            status_code = 200
            msg = ""
            
            if isinstance(resp, tuple):
                if len(resp) > 1:
                    status_code = resp[1]
                if hasattr(resp[0], 'get_data'):
                    try: msg = resp[0].get_data(as_text=True).lower()
                    except: pass
                else:
                    msg = str(resp[0]).lower()
            elif hasattr(resp, 'status_code'):
                status_code = resp.status_code
                try: msg = resp.get_data(as_text=True).lower()
                except: pass
                
            if status_code == 500:
                is_conn_error = any(kw in msg for kw in (
                    "connection", "cursor", "closed", "hy000", "08s01", "communication link failure"
                ))
                if is_conn_error:
                    # Connection lỗi → Invalidate pool để xóa kết nối hỏng
                    try:
                        invalidate_pool()
                    except Exception:
                        pass
                    # Thử lần 2 với kết nối mới sạch sẽ
                    resp = f(*args, **kwargs)
                    
            return resp
    return decorated_function

from flask import Flask, jsonify, request, session, send_from_directory
from flask_cors import CORS
from datetime import datetime, date, timedelta
import os
import sys
import threading

import hashlib
import subprocess
import platform

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def _read_app_version():
    """Đọc version.txt (build_exe.py tự tăng mỗi lần build, và nhúng kèm vào EXE qua --add-data).
    Frontend lấy qua /api/version để hiển thị -> KHÔNG hardcode version ở index.html nữa."""
    try:
        with open(resource_path('version.txt'), 'r', encoding='utf-8') as f:
            v = f.read().strip()
            return v if v else 'dev'
    except Exception:
        return 'dev'

APP_VERSION = _read_app_version()

app = Flask(__name__)

# ⚠️ secret_key SINH NGẪU NHIÊN MỖI LẦN CHẠY — trước đây ghi cứng
# 'IACC_SECRET_SUPREME_2026'. Khoá ghi cứng trong mã nguồn của repo CÔNG KHAI nghĩa là
# ai cũng **tự ký được cookie giả**, và phiên cũ sống xuyên qua mọi lần build lại.
# Hệ quả phải chấp nhận: khởi động lại app (kể cả sau khi tự cập nhật) là phải
# đăng nhập lại — đúng với việc kho phiên bên dưới cũng nằm trong RAM.
app.secret_key = os.urandom(32)

# Cờ bảo vệ cookie — ghi rõ thay vì dựa vào mặc định của Flask.
# KHÔNG bật SECURE vì app chạy trên http://localhost:5050, bật lên là trình duyệt
# không gửi cookie nữa ⇒ đăng nhập xong vẫn bị coi là chưa đăng nhập.
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')
CORS(app, supports_credentials=True)

# ===================================================================
# KHO PHIÊN PHÍA MÁY CHỦ — THÔNG TIN KẾT NỐI SQL KHÔNG ĐƯỢC NẰM TRONG COOKIE
#
# ⚠️ BẪY ĐÃ ĐO THẬT (21/09/2026): cookie phiên của Flask được **KÝ, KHÔNG MÃ HOÁ**.
# Trước đây `session["db_config"] = data` đặt nguyên server/database/user/**password**
# của SQL vào cookie. Giải ra chỉ cần tách phần payload rồi base64 — **không cần
# secret_key**. Mở F12 → Application → Cookies là đọc được mật khẩu SQL.
#
# Nay cookie chỉ còn một **mã phiên ngẫu nhiên** (`sid`), bản thân nó không nói lên
# điều gì. Toàn bộ db_config nằm trong RAM của tiến trình này và chết theo tiến trình.
#
# ⛔ Đừng quay lại đặt db_config vào `session` — đó chính là cái vừa bị gỡ ra.
# ===================================================================
_phien_db = {}                      # sid -> {'cfg': db_config, 'luc': datetime}
_phien_lock = threading.Lock()
_PHIEN_HAN_GIO = 24                 # phiên không đụng tới quá số giờ này thì dọn

def _phien_don_dep_locked():
    """Dọn phiên quá hạn. Gọi khi ĐÃ giữ _phien_lock."""
    if len(_phien_db) < 50:
        return                      # app chạy local, thường chỉ vài phiên — khỏi quét
    nguong = datetime.now() - timedelta(hours=_PHIEN_HAN_GIO)
    for k in [k for k, v in _phien_db.items() if v.get('luc', nguong) < nguong]:
        _phien_db.pop(k, None)

def _db_cfg():
    """Thông tin kết nối SQL của phiên hiện tại, hoặc None khi chưa đăng nhập.
    Thay cho `session.get("db_config")` cũ — xem khối ghi chú ngay trên."""
    sid = session.get('sid')
    if not sid:
        return None
    with _phien_lock:
        m = _phien_db.get(sid)
        if not m:
            return None
        m['luc'] = datetime.now()
        return m['cfg']

def _dat_db_cfg(cfg):
    """Ghi thông tin kết nối cho phiên. **Luôn sinh sid MỚI** để một mã phiên bị lộ
    trước đó không dùng lại được sau khi đăng nhập (chống session fixation)."""
    cu = session.get('sid')
    sid = _secrets.token_urlsafe(32)
    with _phien_lock:
        if cu:
            _phien_db.pop(cu, None)
        _phien_db[sid] = {'cfg': cfg, 'luc': datetime.now()}
        _phien_don_dep_locked()
    session['sid'] = sid
    return sid

def _xoa_db_cfg():
    """Xoá phiên khỏi kho + bỏ sid khỏi cookie."""
    sid = session.pop('sid', None)
    if sid:
        with _phien_lock:
            _phien_db.pop(sid, None)

# ===================================================================
# PHÂN QUYỀN THEO MỤC — 23 mục (7 tab + BC001..BC016). Thêm 18/09/2026.
# NGUỒN chuẩn: PHANQUYEN_MA_TRAN_NHOM.csv (Đại Ca duyệt), NGOÀI repo.
#
# NGUYÊN TẮC (rút từ sự cố 15/08/2026):
#  - Cấm quyền phải trả 403, KHÔNG trả 401. Frontend gặp 401 là setIsLoggedIn(false)
#    → "bấm là văng ra khỏi phần mềm" (Bẫy 1). Guard này CHỈ lo QUYỀN MỤC; việc chưa
#    đăng nhập SQL vẫn để từng endpoint tự trả 401 như cũ.
#  - 3 endpoint phục vụ 2 báo cáo cùng lúc phải guard theo THAM SỐ, không theo tên route:
#    /api/report (BC001+BC003), /api/report_by_job (BC002+BC004), /api/cash_flow (BC009+BC010).
#    Chặn theo tên route thì người bị cấm BC003 vẫn xem được qua BC001 — lỗi không triệu chứng.
#  - /api/cash_flow trả CẢ direct+indirect trong một response ⇒ phải CẮT theo quyền, nếu không
#    ẩn menu BC010 mà vẫn lộ số qua network.
# ⚠️ GIAI ĐOẠN KHUNG: chưa có đăng nhập người dùng (PBKDF2 làm pha sau) → mặc định nhóm ADMIN
#    để app chạy y như cũ. Khi cắm đăng nhập, /api/login sẽ set session['app_group'] theo nhóm
#    thật; chỉ cần đổi giá trị mặc định ở _current_group() cho an toàn.
# ===================================================================
PERM_TABS    = ['ledger', 'sale', 'voucher', 'purchase', 'warehouse', 'warehouse_balance',
                'btp_reconcile', 'dcnb_reconcile', 'po_list']
PERM_REPORTS = ['BC%03d' % i for i in range(1, 17)]          # BC001..BC016
PERM_EXTRA   = ['perm_admin']                                # tab "Phân quyền" — CHỈ ADMIN
PERM_ALL_ITEMS = PERM_TABS + PERM_REPORTS + PERM_EXTRA

# Nhãn tiếng Việt của từng mã — gửi sang Apps Script để nó đặt tên cột cho mục MỚI trên
# sheet Chức vụ. Thiếu nhãn thì Google ghi thẳng mã, không hỏng gì, chỉ khó đọc.
PERM_ITEM_LABELS = {
    'ledger': 'Chứng từ tổng hợp', 'sale': 'Chứng từ bán hàng',
    'voucher': 'Chứng từ tiền', 'purchase': 'Chứng từ nhập kho',
    'warehouse': 'Chứng từ kho', 'warehouse_balance': 'Tồn kho thực tế',
    'btp_reconcile': 'Đối chiếu xuất SX BTP',
    'dcnb_reconcile': 'Đối chiếu điều chuyển nội bộ',
    'po_list': 'Danh sách PO (yêu cầu mua hàng)',
    'perm_admin': 'Tab Phân quyền (quản trị)',
}

def _nhan_muc_quyen():
    """{mã: nhãn} cho MỌI mã hiện có. Mã báo cáo chưa khai nhãn thì dùng chính mã."""
    return {ma: PERM_ITEM_LABELS.get(ma, ma) for ma in PERM_ALL_ITEMS}
_BC = lambda a, b: {'BC%03d' % i for i in range(a, b + 1)}   # tiện gom dải BC

# Nhóm → tập mã được xem. BC015/BC016 tạm CHỈ ADMIN (Đại Ca quyết sau).

# Tên nhóm hiển thị trong tab Phân quyền (dropdown chọn nhóm).

def _current_group():
    """Mã chức vụ của phiên. Rỗng = chưa đăng nhập.
    ⚠️ Trước 21/09/2026 hàm này mặc định trả 'ADMIN' — nghĩa là ai không có chức vụ
    thì thành toàn quyền. Giờ chức vụ do Google Sheet cấp, không có = không gì."""
    return session.get('app_group') or ''

def _current_perms():
    """Tập mã 24 mục phiên này được xem.

    Quyền đã chốt MỘT LẦN lúc đăng nhập và nằm sẵn trong session — **KHÔNG gọi
    mạng ở đây**, hàm này chạy ở MỌI request.

    Không có `app_items` ⇒ trả tập RỖNG. Trước 21/09/2026 nhánh này rơi về
    phanquyen.json rồi cuối cùng về 'ADMIN = full' — tức là phiên hỏng thì được
    toàn quyền, đúng chiều ngược với cái cần.

    ⚠️ PHÂN BIỆT với lỗi cũ đó: chức vụ **ADMIN** (giá trị Google Sheet cấp, không
    phải giá trị mặc định) được TÍNH RA đủ 100% mục — kể cả mục mới thêm vào app sau
    này. Lý do: `PERM` trong `phanquyen_gas/Code.gs` **ghi cứng danh sách mã** trên
    Google, nên mỗi lần app thêm tab/báo cáo mới là ADMIN **không thể** nhận được
    từ Sheet cho tới khi ai đó sửa Code.gs + thêm cột vào Sheet + Triển khai lại
    (Bẫy 19 — việc nguy hiểm). Đã vấp thật 21/09/2026: hai tab `dcnb_reconcile` và
    `po_list` không hiện với chính tài khoản admin.
    Chỗ này an toàn vì chỉ nhận đúng chuỗi 'ADMIN' **do Sheet trả về**; phiên hỏng
    hay chưa đăng nhập thì `_current_group()` trả '' ⇒ vẫn tập RỖNG như cũ.
    ⚠️ Nhóm KHÁC muốn được cấp mục mới thì vẫn phải bổ sung mã vào `PERM` trong
    Code.gs rồi Triển khai — app không tự làm thay được."""
    if _current_group() == 'ADMIN':
        return set(PERM_ALL_ITEMS)
    items = session.get('app_items')
    if isinstance(items, list):
        return set(x for x in items if x in PERM_ALL_ITEMS)
    return set()

# path tĩnh → mã quyền (1 route = 1 mục)
PERM_ROUTE_STATIC = {
    '/api/ledger': 'ledger', '/api/ledger/count': 'ledger',
    '/api/ledger/stream_csv': 'ledger', '/api/ledger/export': 'ledger',
    '/api/sale': 'sale', '/api/sale/count': 'sale', '/api/sale/stream_csv': 'sale',
    '/api/voucher': 'voucher', '/api/voucher/count': 'voucher', '/api/voucher/stream_csv': 'voucher',
    '/api/purchase': 'purchase', '/api/purchase/count': 'purchase',
    '/api/purchase/stream_csv': 'purchase', '/api/debug_purchase': 'purchase',
    '/api/warehouse': 'warehouse', '/api/warehouse/count': 'warehouse', '/api/warehouse/stream_csv': 'warehouse',
    '/api/warehouse_balance': 'warehouse_balance', '/api/warehouse_balance/count': 'warehouse_balance',
    '/api/warehouse_balance/stream_csv': 'warehouse_balance',
    '/api/btp_reconcile': 'btp_reconcile', '/api/btp_reconcile/count': 'btp_reconcile',
    '/api/btp_reconcile/stream_csv': 'btp_reconcile',
    '/api/dcnb_reconcile': 'dcnb_reconcile', '/api/dcnb_reconcile/count': 'dcnb_reconcile',
    '/api/dcnb_reconcile/stream_csv': 'dcnb_reconcile',
    '/api/po_list': 'po_list', '/api/po_list/count': 'po_list',
    '/api/po_list/stream_csv': 'po_list',
    '/api/balance_sheet': 'BC005', '/api/trial_balance': 'BC006', '/api/journal': 'BC007',
    '/api/account_details': 'BC008', '/api/cash_flow_cl': 'BC011',
    '/api/cash_book': 'BC012', '/api/cash_book/export_csv': 'BC012',
    '/api/debt_summary': 'BC013', '/api/vat_sales_report': 'BC014',
    '/api/sale_by_source': 'BC015', '/api/nxt': 'BC016',
    # Tab Phân quyền — CHỈ ADMIN (ADMIN bypass guard; nhóm khác thiếu 'perm_admin' → 403).
    '/api/perm/config': 'perm_admin', '/api/perm/user': 'perm_admin',
    '/api/perm/user/delete': 'perm_admin',
    '/api/perm/role': 'perm_admin', '/api/perm/role/delete': 'perm_admin',
}
# path không giới hạn theo mục (vẫn cần đăng nhập SQL — từng endpoint tự kiểm)
PERM_PUBLIC = {
    '/api/version', '/api/check_driver', '/api/install_driver', '/api/login', '/api/logout',
    '/api/metadata', '/api/metadata/refresh', '/api/export/status', '/api/export/cancel',
    '/api/save_export', '/api/open_file', '/api/open_folder',
    '/api/check_update', '/api/update_progress', '/api/apply_update', '/api/my_perms',
    # Tự đổi mật khẩu: ai cũng gọi được. Endpoint TỰ kiểm mật khẩu cũ hoặc tài khoản
    # quản trị rồi mới cho đổi — ĐỪNG đổi thành 'perm_admin', người thường sẽ kẹt.
    '/api/perm/password',
}

def _needed_perm(path):
    """Mã quyền cần cho path. '' = public (không kiểm mục). '__UNKNOWN__' = /api chưa khai báo."""
    if path in PERM_PUBLIC:
        return ''
    if path in PERM_ROUTE_STATIC:
        return PERM_ROUTE_STATIC[path]
    rep = (request.args.get('report') or '').strip().upper()
    if path == '/api/report':
        return rep if rep in ('BC001', 'BC003') else 'BC001'
    if path == '/api/report_by_job':
        return rep if rep in ('BC002', 'BC004') else 'BC002'
    if path == '/api/cash_flow':
        return rep if rep in ('BC009', 'BC010') else 'BC009'
    if path in ('/api/export_excel_backend', '/api/report_export_csv'):
        rt = (request.args.get('report_type') or '').strip().upper()
        return rt if rt in PERM_ALL_ITEMS else '__UNKNOWN__'
    return '__UNKNOWN__'

@app.before_request
def _perm_guard():
    path = request.path
    if not path.startswith('/api/'):
        return None                                  # file tĩnh — guard chỉ lo tầng dữ liệu
    if not _db_cfg():
        return None                                  # chưa đăng nhập SQL → endpoint tự trả 401
    needed = _needed_perm(path)
    if needed == '':
        return None                                  # public
    perms = _current_perms()
    if needed == '__UNKNOWN__':
        # route /api chưa khai báo → chỉ tài khoản có quyền quản trị (perm_admin) mới qua
        if 'perm_admin' in perms:
            return None
        logger.warning('PERM: route /api chua khai bao quyen: %s', path)
        return jsonify({"status": "error", "message": "Route chưa khai báo quyền"}), 403
    if needed in perms:
        return None
    return jsonify({"status": "error", "message": "Bạn không có quyền xem mục này"}), 403

# ===================================================================
# ĐĂNG NHẬP NGƯỜI DÙNG — mật khẩu RIÊNG của tool, băm PBKDF2 (một chiều, có salt).
# KHÔNG dùng mật khẩu iPOS (SEC_USER mã hoá 2 chiều AES, khoá chôn trong client — xem
# nhật ký 18/09/2026). Tool tự quản mật khẩu, Đại Ca cấp mật khẩu ban đầu cho từng người.
#
# Nguồn tài khoản: **Google Sheet TOOL_CHULONG, DUY NHẤT** (từ 21/09/2026). Chế độ file
# phanquyen.json đã BỎ HẲN — máy thiếu cấu hình là chặn đăng nhập, xem _loi_chua_cau_hinh.
# ⚠️ Mật khẩu tool KHÔNG lưu vào session/cookie (tách khỏi db_config lúc login).
# Hai hàm PBKDF2 dưới đây nay chỉ còn phục vụ BẢN CACHE OFFLINE (_cache_ghi/_cache_kiem);
# mật khẩu thật được kiểm tại Google, hash không bao giờ rời khỏi Sheet.
# ===================================================================
import json as _json, hmac as _hmac, base64 as _b64, secrets as _secrets

def _pbkdf2_hash(password, salt=None, iterations=200_000):
    if salt is None:
        salt = _secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac('sha256', (password or '').encode('utf-8'), salt, iterations)
    return "pbkdf2_sha256$%d$%s$%s" % (iterations, _b64.b64encode(salt).decode(), _b64.b64encode(dk).decode())

def _pbkdf2_verify(password, stored):
    try:
        algo, iter_s, salt_b64, hash_b64 = (stored or '').split('$')
        if algo != 'pbkdf2_sha256':
            return False
        salt = _b64.b64decode(salt_b64)
        expected = _b64.b64decode(hash_b64)
        dk = hashlib.pbkdf2_hmac('sha256', (password or '').encode('utf-8'), salt, int(iter_s))
        return _hmac.compare_digest(dk, expected)
    except Exception:
        return False

_phanquyen_cache = None







def _current_allowed_orgs():
    """Đơn vị phiên này được xem. Chốt lúc đăng nhập, không gọi mạng.

    None = KHÔNG giới hạn (thấy tất cả, kể cả đơn vị thêm sau này).
    set(...) = chỉ được xem đúng các đơn vị đó (áp cho MỌI danh sách + báo cáo).
    ⚠️ Trên Sheet, cột DON_VI để trống = xem TẤT CẢ, không phải "không xem gì"."""
    orgs = session.get('app_orgs')
    return set(str(o) for o in orgs) if isinstance(orgs, list) else None

# ===================================================================
# NGUỒN TÀI KHOẢN DÙNG CHUNG NHIỀU MÁY — GOOGLE SHEET qua Apps Script
# (chốt 19/09/2026; chi tiết: phanquyen_gas/HUONG_DAN.md)
#
# LUẬT: mật khẩu được KIỂM TẠI GOOGLE, bảng hash KHÔNG BAO GIỜ tải về máy khách.
#       App gửi lên user+mật khẩu, nhận về đúng danh sách quyền.
#
# ⚠️ Quyền lấy MỘT LẦN lúc đăng nhập rồi giữ trong session. _current_perms() và
#    _current_allowed_orgs() chạy ở MỌI request — gọi mạng trong đó là mỗi cú bấm
#    phải chờ Google 1–3 giây. Hệ quả phải chấp nhận: thu hồi quyền của ai đó chỉ có
#    hiệu lực khi người đó đăng nhập lại.
#
# ⛔ Chưa cấu hình ketnoi.json → **CHẶN đăng nhập** (_loi_chua_cau_hinh). Trước 21/09/2026
#    nhánh đó rơi về phanquyen.json rồi về 'ADMIN = full' — mở toang mà không cảnh báo gì.
# ===================================================================
import urllib.request as _url_req
import urllib.error as _url_err
import time as _time

# ⚠️ Apps Script CHẬP CHỜN THẬT — đo 20/09/2026 trên máy có mạng tốt (0,2s ra google.com):
#    cùng một lệnh `ping` lúc trả sau 5s, lúc 10,4s, lúc mất 19,7s rồi trả HTTP 404.
#    404 ở đây KHÔNG phải sai URL — là lỗi nhất thời phía Google, gọi lại là được.
#    Để timeout 15s + không thử lại thì nhân viên sẽ ngẫu nhiên đăng nhập hỏng mà
#    không hiểu vì sao, lại còn bị báo nhầm thành "mất mạng".
_GS_TIMEOUT = 45.0          # rộng tay: máy thật sự mất mạng vẫn hỏng nhanh ở bước nối
_GS_SO_LAN_THU = 3          # thử lại khi Google trả 404 / 5xx / hết giờ
_CACHE_HAN_NGAY = 7         # số ngày bản cache offline còn dùng được

class _GSOffline(Exception):
    """Không nối được tới Google (mất mạng / Google chặn). KHÁC với sai mật khẩu."""

_DK_ITER = 200_000
def _dan_xuat_dk(uid, mat_khau):
    """Băm mật khẩu NGAY TẠI MÁY NÀY rồi mới gửi lên Google — mật khẩu gốc không
    bao giờ rời khỏi máy người dùng.

    Vì sao phải làm ở đây: Apps Script chậm hơn Python ~2.500 lần (đo thật
    19/09/2026 — Python 200.000 vòng hết 74 mili-giây, Apps Script 10.000 vòng
    hết 9 GIÂY). Đẩy phần nặng về máy khách thì đăng nhập nhanh mà vẫn giữ đủ
    200.000 vòng bảo vệ cho bảng lưu bên Google.

    Salt suy thẳng từ tên tài khoản (không ngẫu nhiên) để khỏi tốn thêm một lượt
    hỏi Google xin salt — mỗi lượt như thế mất gần 2 giây. Google vẫn băm tiếp
    1.000 vòng với salt ngẫu nhiên riêng nên bảng lưu bên đó không bị trùng nhau.

    ⚠️ uid phải chuẩn hoá y hệt ở MỌI nơi gọi (strip + lower), lệch một chữ hoa
    là ra chuỗi khác và người dùng không đăng nhập được."""
    u = (uid or '').strip().lower()
    salt = ('TOOL_CHULONG|' + u).encode('utf-8')
    dk = hashlib.pbkdf2_hmac('sha256', (mat_khau or '').encode('utf-8'), salt, _DK_ITER)
    return _b64.b64encode(dk).decode()

def _thu_muc_canh_exe():
    return os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.abspath('.')

_gs_cfg_cache = None
# -------------------------------------------------------------------
# ĐỊ CHỈ KẾT NỐI — GHIM CỨNG (chốt 21/09/2026)
#
# Để chỉ phải phát **MỘT file EXE**, không kèm file cấu hình nào. Đổi về sau thì
# sửa đúng hai dòng dưới đây rồi build lại.
#
# ⚠️ REPO NÀY CÔNG KHAI ⇒ hai chuỗi này ai cũng đọc được trên GitHub. Đã cân nhắc
#    và chấp nhận: TOKEN chỉ là **lớp chắn bot**, không phải thứ quyết định quyền.
#    7/8 lệnh của Apps Script đều đòi thêm mật khẩu (xem `_doiAdmin` trong Code.gs):
#    kẻ cầm token KHÔNG đọc được danh sách tài khoản, KHÔNG sửa được ai, KHÔNG lấy
#    được bảng hash, và không chạm được số liệu kế toán (nằm ở SQL Server sau VPN).
#
# ⛔ CÁI NÀY CHỈ ĐÚNG CHO **TOKEN APPS SCRIPT**. Tuyệt đối không ghim theo kiểu này
#    bất cứ thông tin SQL Server nào — cái đó mở thật vào dữ liệu kế toán.
#
# Đổi token thì phải đổi CẢ HAI đầu: `const TOKEN` trong Code.gs + dòng dưới đây.
# Triển khai lại Apps Script bằng **Phiên bản mới**, đừNG bấm "Triển khai mới"
# — nó sinh URL khác và mọi EXE đã phát cho nhân viên sẽ mất kết nối.
# -------------------------------------------------------------------
_GS_URL_GHIM = 'https://script.google.com/macros/s/AKfycbx8ZrKnVNbb3RcSORdYgaFmhqoBC-CvzRUnEJW1l_2CKad0S43IMZxHL-G5b7PEiFIk/exec'
_GS_TOKEN_GHIM = 'kpP8e2h7CVHKJQjxApSbsWRbirJ4U9Z2K1hqnGwcqFy8jjuv'

def _gs_config(force=False):
    """Cấu hình kết nối tới Apps Script.

    Thứ tự ưu tiên — file ĐÈ LÊN bản ghim cứng:
      1. `ketnoi.json` cạnh EXE  → để đổi gấp mà khỏi build lại (gửi 1 file là xong)
      2. `ketnoi.json` nhúng trong EXE (nếu build có kèm)
      3. **Bản ghim cứng ở trên** — đường mặc định, dùng cho mọi máy bình thường

    Trả None **chỉ khi** cả ba đều trống — lúc đó `_loi_chua_cau_hinh()` chặn đăng nhập."""
    global _gs_cfg_cache
    if _gs_cfg_cache is not None and not force:
        return _gs_cfg_cache or None
    cfg = {}
    for p in (os.path.join(_thu_muc_canh_exe(), 'ketnoi.json'), resource_path('ketnoi.json')):
        try:
            with open(p, encoding='utf-8') as f:
                cfg = _json.load(f) or {}
            logger.info('Nap cau hinh Google Sheet tu file: %s', p)
            break
        except FileNotFoundError:
            continue
        except Exception as e:
            logger.warning('Loi doc ketnoi.json %s: %s', p, e)
    if not (cfg.get('url') and cfg.get('token')):
        if _GS_URL_GHIM and _GS_TOKEN_GHIM:
            cfg = {'url': _GS_URL_GHIM, 'token': _GS_TOKEN_GHIM}
            logger.info('Dung cau hinh Google Sheet ghim san trong ma nguon')
        else:
            cfg = {}
    _gs_cfg_cache = cfg
    return cfg or None

def _gs_goi(hanh_dong, **thamso):
    """Gọi Apps Script. Trả dict kết quả.
    Ném _GSOffline nếu KHÔNG NỐI ĐƯỢC — phải phân biệt với 'nối được nhưng sai mật khẩu',
    vì chỉ trường hợp mất mạng mới được phép rơi về bản cache offline."""
    cfg = _gs_config()
    if not cfg:
        raise _GSOffline('Chưa cấu hình ketnoi.json')
    body = dict(thamso)
    body['token'] = cfg['token']
    body['hanh_dong'] = hanh_dong
    body.setdefault('may', platform.node())
    data = _json.dumps(body, ensure_ascii=False).encode('utf-8')

    # Thử lại được vì mọi hành động hiện có đều lặp lại vô hại: 'luu_user' tìm theo
    # user_id rồi ghi đè, 'dat_mat_khau' đặt lại cùng giá trị, 'dang_nhap'/'nap' chỉ đọc.
    # Thêm hành động MỚI mà không chịu được gọi hai lần thì phải bỏ qua vòng lặp này.
    loi_cuoi = None
    for lan in range(1, _GS_SO_LAN_THU + 1):
        req = _url_req.Request(cfg['url'], data=data,
                               headers={'Content-Type': 'application/json'})
        try:
            # Apps Script trả kết quả qua 1 lần redirect sang script.googleusercontent.com;
            # urlopen tự đi theo redirect nên không cần xử lý thêm.
            with _url_req.urlopen(req, timeout=_GS_TIMEOUT) as resp:
                return _json.loads(resp.read().decode('utf-8'))
        except _url_err.HTTPError as e:
            loi_cuoi = 'Google trả lỗi HTTP %s' % e.code
            # 404 và 5xx của Apps Script là lỗi nhất thời — gọi lại thường là được.
            # Mã khác (403 chẳng hạn) là hỏng thật, dừng ngay khỏi mất công chờ.
            if e.code != 404 and e.code < 500:
                raise Exception('%s — kiểm tra lại bản triển khai' % loi_cuoi)
        except Exception as e:
            loi_cuoi = str(e)
        if lan < _GS_SO_LAN_THU:
            logger.warning('Goi Google that bai (lan %d/%d): %s — thu lai',
                           lan, _GS_SO_LAN_THU, loi_cuoi)
            _time.sleep(1.5 * lan)
    raise _GSOffline(loi_cuoi or 'không rõ nguyên nhân')

# ---------- Bản cache offline ----------
# Chứa hash PBKDF2 200.000 vòng của mật khẩu (KHÔNG chứa mật khẩu), kèm quyền đã cấp.
# Đây là mô hình "credential cached" quen thuộc: chỉ những ai ĐÃ đăng nhập thành công
# trên CHÍNH máy này mới có mục trong file, và mục đó hết hạn sau _CACHE_HAN_NGAY ngày.
def _cache_path():
    return os.path.join(_thu_muc_canh_exe(), 'phanquyen_cache.json')

def _cache_doc_file():
    try:
        with open(_cache_path(), encoding='utf-8') as f:
            return _json.load(f) or {}
    except Exception:
        return {}

def _cache_ghi(uid, mat_khau, thongtin):
    """Lưu lại để lần sau mất mạng vẫn đăng nhập được."""
    try:
        d = _cache_doc_file()
        d[uid.lower()] = {
            'pw': _pbkdf2_hash(mat_khau),
            'ttin': thongtin,
            'luc': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        with open(_cache_path(), 'w', encoding='utf-8') as f:
            _json.dump(d, f, ensure_ascii=False, indent=1)
    except Exception as e:
        logger.warning('Khong ghi duoc cache quyen: %s', e)

def _xoa_cache_uid(uid):
    """Xoá một mục khỏi bản cache offline trên MÁY NÀY.
    Gọi sau khi đổi mật khẩu — không thì mất mạng vẫn vào được bằng mật khẩu cũ."""
    try:
        c = _cache_doc_file()
        if c.pop((uid or '').lower(), None) is not None:
            with open(_cache_path(), 'w', encoding='utf-8') as f:
                _json.dump(c, f, ensure_ascii=False, indent=1)
            logger.info('Da xoa cache offline cua tai khoan sau khi doi mat khau')
    except Exception as e:
        logger.warning('Khong xoa duoc cache sau khi doi mat khau: %s', e)

def _cache_kiem(uid, mat_khau):
    """Đăng nhập bằng bản cache khi mất mạng.
    Trả (thongtin, mốc_đồng_bộ, False) nếu vào được, hoặc (None, lý_do, có_phải_sai_mật_khẩu).

    Cần cờ thứ 3 vì hai chuyện phải nói khác nhau: gõ sai mật khẩu là lỗi của người
    dùng, còn mấy lý do kia đều là hệ quả của việc KHÔNG gọi được Google — phải nói
    rõ điều đó ra, không thì người ta đọc "máy này chưa từng đăng nhập" mà chẳng hiểu
    tại sao hôm qua vẫn vào được."""
    m = _cache_doc_file().get((uid or '').lower())
    if not m:
        return None, 'máy này chưa từng đăng nhập thành công nên không có bản lưu để dùng tạm.', False
    try:
        luc = datetime.strptime(m['luc'], '%Y-%m-%d %H:%M:%S')
    except Exception:
        return None, 'bản quyền lưu trên máy bị hỏng.', False
    so_ngay = (datetime.now() - luc).days
    if so_ngay > _CACHE_HAN_NGAY:
        return None, ('bản quyền lưu trên máy đã quá %d ngày (đồng bộ lần cuối %s) nên không '
                      'dùng tạm được nữa.' % (_CACHE_HAN_NGAY, luc.strftime('%d/%m/%Y'))), False
    if not _pbkdf2_verify(mat_khau, m.get('pw', '')):
        return None, 'Sai tài khoản hoặc mật khẩu ứng dụng.', True
    return m.get('ttin') or {}, luc.strftime('%d/%m/%Y %H:%M'), False

# ===== GZIP COMPRESSION =====
# JSON nén rất tốt (5–10× nhỏ hơn) → giảm bandwidth + parse time cho payload 500k dòng
import gzip
import io as _io
@app.after_request
def _gzip_response(response):
    try:
        accept_enc = request.headers.get('Accept-Encoding', '')
        if 'gzip' not in accept_enc.lower():
            return response
        if response.status_code < 200 or response.status_code >= 300:
            return response
        if response.headers.get('Content-Encoding'):
            return response
        # File tĩnh (send_from_directory) đi đường direct_passthrough VÀ cũng bị tính là
        # is_streamed, nhưng nó có Content-Length rõ ràng nên nén an toàn → phải xét TRƯỚC
        # nhánh is_streamed. Trước đây get_data() ném RuntimeError trên direct_passthrough,
        # bị nuốt ở except cuối hàm ⇒ index.html (~575KB) CHƯA TỪNG được nén, mỗi lần mở app
        # là tải nguyên 575KB.
        if response.direct_passthrough:
            clen = response.content_length
            if clen is None or clen > 8 * 1024 * 1024:   # chặn ngưỡng, không ôm file lớn vào RAM
                return response
            response.direct_passthrough = False
        # ⚠️ Response dạng STREAM (các endpoint xuất CSV dùng stream_with_context):
        # get_data() sẽ NUỐT TRỌN generator vào RAM rồi mới gửi → mất sạch tác dụng streaming
        # mà chính các endpoint đó được viết ra để có. Hệ quả: file lớn thì trình duyệt đứng
        # im không nhận được byte nào cho tới khi chạy xong, RAM phình theo kích thước file.
        elif response.is_streamed:
            return response
        ctype = (response.content_type or '').lower()
        # Chỉ nén text/JSON, không nén binary đã nén sẵn
        if not (ctype.startswith('application/json') or ctype.startswith('text/')
                or ctype.startswith('application/javascript')):
            return response
        data = response.get_data()
        if len(data) < 1024:  # payload nhỏ thì bỏ qua, overhead không đáng
            return response
        buf = _io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode='wb', compresslevel=5) as gz:
            gz.write(data)
        compressed = buf.getvalue()
        response.set_data(compressed)
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = str(len(compressed))
        response.headers['Vary'] = 'Accept-Encoding'
    except Exception:
        pass
    return response

def kill_process_on_port(port):
    """Giải phóng port nếu có process khác đang chiếm đóng (Tránh lỗi cache bản cũ)."""
    try:
        if platform.system() == "Windows":
            # Tìm PID đang dùng port
            cmd = f'netstat -ano | findstr :{port}'
            output = subprocess.check_output(cmd, shell=True).decode()
            for line in output.splitlines():
                if "LISTENING" in line:
                    pid = line.strip().split()[-1]
                    if int(pid) != os.getpid(): # Đừng tự sát
                        subprocess.run(f'taskkill /F /PID {pid}', shell=True, capture_output=True)
    except:
        pass

# Thực hiện dọn dẹp port ngay khi khởi chạy
kill_process_on_port(5050)

def check_odbc_driver(driver_name="ODBC Driver 17 for SQL Server"):
    """Kiểm tra driver ODBC có tồn tại không."""
    return True

def install_odbc_driver():
    """Chạy script cài driver ODBC."""
    try:
        script_path = resource_path("install_driver.ps1")
        if not os.path.exists(script_path):
            return False, "Script cài driver không tìm thấy"

        # Chạy PowerShell script với admin rights
        cmd = f'powershell -ExecutionPolicy Bypass -File "{script_path}"'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

        if result.returncode == 0:
            return True, "Cài đặt driver thành công"
        else:
            return False, f"Lỗi cài đặt: {result.stderr}"
    except Exception as e:
        return False, str(e)

# In-memory metadata cache: key = database name
_meta_cache = {}

# Cache đơn vị "ngoài cây 00" theo database (dùng cho LCTT BC009/BC010)
_external_orgs_cache = {}

# Connection pool: key = hash(db_config) → pyodbc connection
# Tránh mở-đóng connection mỗi request (tiết kiệm 200-500ms / request)
_conn_pool = {}
_pool_lock = threading.Lock()
# Lần cuối mỗi connection được dùng — để khỏi bắn "SELECT 1" dò sống trước mọi request.
import time
_conn_last_used = {}
_POOL_PROBE_AFTER_SEC = 30

def _pool_key(db_config):
    """Tạo key ổn định từ db_config (không chứa password plaintext trong key)."""
    raw = f"{db_config.get('server')}|{db_config.get('database')}|{db_config.get('user')}"
    return hashlib.md5(raw.encode()).hexdigest()

def _make_conn(db_config):
    conn_str = (
        f"DRIVER={{{db_config['driver']}}};"
        f"SERVER={db_config['server']};"
        f"DATABASE={db_config['database']};"
        f"UID={db_config['user']};"
        f"PWD={db_config['password']};"
        "Trusted_Connection=no;"
    )
    conn = pyodbc.connect(conn_str, timeout=5)
    conn.autocommit = True  # Tránh treo transaction và khóa bảng
    # SET NOCOUNT ON: bỏ thông báo "X rows affected" → giảm round-trip & overhead network
    try:
        conn.execute("SET NOCOUNT ON")
    except Exception:
        pass
    return conn

@app.route("/api/version")
def get_version():
    """Public (không cần đăng nhập) — màn hình login cũng hiển thị version."""
    return jsonify({"status": "ok", "version": APP_VERSION})


@app.route("/")
def index():
    resp = send_from_directory(resource_path("."), "index.html")
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp

@app.route("/<path:filename>")
def serve_static(filename):
    resp = send_from_directory(resource_path("."), filename)
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return resp

def get_connection():
    """Trả connection từ pool, tạo mới nếu chưa có hoặc đã chết."""
    db_config = _db_cfg()
    if not db_config:
        raise Exception("Vui lòng đăng nhập SQL Server trước!")

    key = _pool_key(db_config)

    with _pool_lock:
        conn = _conn_pool.get(key)
        if conn is not None:
            # Test connection còn sống không — nhưng CHỈ khi đã nhàn rỗi một lúc.
            # "SELECT 1" là một vòng đi-về tới SQL Server; bắn nó trước MỌI request khiến
            # mỗi thao tác gánh thêm nguyên một round-trip mạng (thấy rõ khi server ở xa).
            # Connection vừa dùng cách đây vài giây thì gần như chắc chắn còn sống, mà nếu
            # có chết thật thì @with_db_lock đã bắt lỗi kết nối, invalidate_pool rồi chạy
            # lại lần 2 với connection sạch → vẫn an toàn, chỉ mất 1 lần thử.
            if (time.time() - _conn_last_used.get(key, 0)) < _POOL_PROBE_AFTER_SEC:
                _conn_last_used[key] = time.time()
                return conn
            try:
                conn.cursor().execute("SELECT 1").fetchone()
                _conn_last_used[key] = time.time()
                return conn
            except Exception:
                try: conn.close()
                except: pass
                _conn_pool.pop(key, None)
                _conn_last_used.pop(key, None)

        # Tạo connection mới
        conn = _make_conn(db_config)
        _conn_pool[key] = conn
        _conn_last_used[key] = time.time()
        return conn

def close_pool_for(db_config):
    """Đóng connection trong pool khi logout."""
    if not db_config:
        return
    key = _pool_key(db_config)
    with _pool_lock:
        conn = _conn_pool.pop(key, None)
        _conn_last_used.pop(key, None)   # bỏ luôn mốc thời gian, giữ 2 dict luôn khớp nhau
    if conn:
        try: conn.close()
        except: pass

def invalidate_pool():
    """Drop connection hiện tại khỏi pool (gọi khi query lỗi — có thể do conn chết giữa chừng)."""
    db_config = _db_cfg()
    close_pool_for(db_config)

@app.route("/api/check_driver")
def check_driver():
    """Kiểm tra driver ODBC có tồn tại."""
    has_driver = check_odbc_driver()
    return jsonify({"has_driver": has_driver, "drivers": pyodbc.drivers()})

@app.route("/api/install_driver", methods=["POST"])
def install_driver():
    """Cài đặt ODBC driver."""
    success, message = install_odbc_driver()
    return jsonify({"success": success, "message": message})

def _loi_ket_noi_de_hieu(e, cau_hinh=None):
    """Đổi lỗi ODBC thô thành câu người dùng đọc được.

    Lỗi gốc trông như thế này — không ai ngoài dân kỹ thuật hiểu nổi:
      ('08001', '[08001] [Microsoft][ODBC SQL Server Driver][DBNETLIB]SQL Server
       does not exist or access denied. (17) (SQLDriverConnect)...')

    Trả (thông_điệp_dễ_hiểu, nguyên_văn_lỗi). Nguyên văn vẫn gửi kèm để còn chẩn
    đoán, nhưng để sau nút "Chi tiết" chứ không đập thẳng vào mặt người dùng.
    """
    goc = str(e)
    t = goc.lower()
    c = cau_hinh or {}
    may_chu = c.get('server') or 'máy chủ'
    csdl = c.get('database') or 'database'
    nguoi_dung = c.get('user') or 'tài khoản'

    # ⚠️ THỨ TỰ XÉT RẤT QUAN TRỌNG, và phải xét "không tới được máy chủ" TRƯỚC "hết giờ chờ".
    #    ODBC Driver 17 khi không tới được máy chủ sẽ trả VỀ CẢ HAI:
    #      "Login timeout expired" + "Server is not found or not accessible"
    #    Xét chữ "timeout" trước thì báo thành "máy chủ quá tải, thử lại sau" — dẫn người
    #    dùng đi sai hướng, ngồi chờ thay vì đi bật VPN. Đã trả giá 20/09/2026.
    khong_toi_duoc = ('server is not found or not accessible' in t
                      or 'network-related' in t
                      or 'does not exist or access denied' in t
                      or 'connectionopen' in t
                      or 'tcp provider' in t
                      or 'named pipes provider' in t)
    if khong_toi_duoc:
        return ('Không kết nối được tới máy chủ %s.\n'
                'Kiểm tra lần lượt: đã bật VPN / vào đúng mạng nội bộ chưa · địa chỉ và cổng '
                'có gõ đúng không · máy chủ SQL có đang bật không.' % may_chu, goc)
    # Tới đây mới là "gọi được máy chủ nhưng nó trả lời chậm quá".
    if 'timeout expired' in t or 'hyt00' in t:
        return ('Máy chủ có trả lời nhưng quá chậm nên phải bỏ cuộc. Mạng đang chậm, hoặc '
                'máy chủ SQL đang quá tải. Thử lại sau ít phút.', goc)
    if 'login failed for user' in t or '28000' in t:
        return ('Sai User ID hoặc Password của SQL Server (không phải mật khẩu ứng dụng).', goc)
    if 'cannot open database' in t:
        return ('Không mở được database "%s". Kiểm tra tên database, hoặc tài khoản "%s" '
                'chưa được cấp quyền vào database này.' % (csdl, nguoi_dung), goc)
    if 'data source name not found' in t or 'im002' in t:
        return ('Máy này chưa cài driver ODBC cho SQL Server. Bấm nút cài driver ở màn hình '
                'đăng nhập rồi thử lại.', goc)
    if '08001' in t or '08s01' in t:
        return ('Không kết nối được tới máy chủ %s.\n'
                'Kiểm tra lần lượt: đã bật VPN / vào đúng mạng nội bộ chưa · địa chỉ và cổng '
                'có gõ đúng không · máy chủ SQL có đang bật không.' % may_chu, goc)
    return ('Không kết nối được tới máy chủ %s.' % may_chu, goc)

@app.route("/api/login", methods=["POST"])
def login():
    data = None          # phải khai trước: khối except ở cuối có đọc biến này
    try:
        data = request.json or {}
        # Tách credential ỨNG DỤNG khỏi db_config — mật khẩu tool KHÔNG được lưu vào session/cookie.
        app_user = (data.pop('app_user', '') or '').strip()
        app_password = data.pop('app_password', '') or ''

        # (1) Xác thực tài khoản ứng dụng — **Google Sheet là nguồn DUY NHẤT**.
        #     Thiếu cấu hình là chặn ngay. Trước 21/09/2026 nhánh này rơi về
        #     phanquyen.json, và không có cả file đó thì app_group='ADMIN' ⇒ mở toang
        #     24 mục cho bất kỳ ai đăng nhập được SQL (xem _loi_chua_cau_hinh).
        if not _gs_config():
            return _loi_chua_cau_hinh()

        app_group = ''
        real_uid = None
        app_items = None
        app_orgs = None
        app_nguon = 'gsheet'
        ho_ten = None
        canh_bao = None

        try:
            # Gửi CHUỖI ĐÃ BĂM, không gửi mật khẩu gốc (xem _dan_xuat_dk).
            kq = _gs_goi('dang_nhap', user=app_user,
                         mat_khau=_dan_xuat_dk(app_user, app_password))
        except _GSOffline as _e_gs:
            # CHỈ khi mất mạng mới được rơi về bản lưu trên máy.
            ttin, ly_do, sai_mat_khau = _cache_kiem(app_user, app_password)
            if not ttin:
                thong_diep = ly_do if sai_mat_khau else (
                    'Không kết nối được tới Google (nơi lưu danh sách tài khoản), và %s\n'
                    'Kiểm tra mạng rồi thử lại.' % ly_do)
                return jsonify({"status": "error", "message": thong_diep,
                                "chi_tiet": str(_e_gs)}), 401
            kq = {"ok": True, "user": ttin}
            canh_bao = ('Không nối được Google — đang dùng bản quyền lưu trên máy '
                        '(đồng bộ lần cuối %s). Quyền mới cấp/thu hồi chưa có hiệu lực.' % ly_do)
        if not kq.get('ok'):
            return jsonify({"status": "error",
                            "message": kq.get('loi') or 'Sai tài khoản hoặc mật khẩu'}), 401
        u = kq.get('user') or {}
        real_uid = u.get('id') or app_user
        ho_ten = u.get('ho_ten')
        app_group = u.get('chuc_vu') or ''
        app_items = [x for x in (u.get('items') or []) if x in PERM_ALL_ITEMS]
        app_orgs = u.get('don_vi') if isinstance(u.get('don_vi'), list) else None
        if not canh_bao:
            _cache_ghi(real_uid, app_password, u)   # để lần sau mất mạng vẫn vào được

        # (2) Kết nối SQL (như cũ). data giờ chỉ còn field SQL.
        old = _db_cfg()
        if old:
            close_pool_for(old)
        conn = _make_conn(data)
        key = _pool_key(data)
        with _pool_lock:
            _conn_pool[key] = conn

        _dat_db_cfg(data)
        session['app_user'] = real_uid
        session['app_group'] = app_group
        session['app_nguon'] = app_nguon
        session['app_ten'] = ho_ten
        # Chỉ ghi khi nguồn là Google Sheet — để _current_perms() biết đường nào mà lần.
        session['app_items'] = app_items or []
        session['app_orgs'] = app_orgs
        _meta_cache.pop(data.get('database'), None)
        _tran_usage_cache.pop(data.get('database'), None)
        return jsonify({"status": "ok", "message": "Đăng nhập thành công!",
                        "app_user": real_uid, "group": app_group,
                        "name": ho_ten, "canh_bao": canh_bao})
    except Exception as e:
        # Không quăng nguyên văn lỗi ODBC ra màn hình — dịch sang tiếng người,
        # nguyên văn để sau nút "Chi tiết" cho lúc cần chẩn đoán.
        thong_diep, nguyen_van = _loi_ket_noi_de_hieu(e, data if isinstance(data, dict) else None)
        logger.warning('Login that bai: %s', nguyen_van)
        return jsonify({"status": "error", "message": thong_diep, "chi_tiet": nguyen_van}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    db_config = _db_cfg()
    db_name = (db_config or {}).get('database')
    close_pool_for(db_config)
    _xoa_db_cfg()
    session.pop('app_group', None)
    session.pop('app_user', None)
    for _k in ('app_items', 'app_orgs', 'app_nguon', 'app_ten'):
        session.pop(_k, None)
    if db_name:
        _meta_cache.pop(db_name, None)
        _tran_usage_cache.pop(db_name, None)
    return jsonify({"status": "ok"})

@app.route("/api/my_perms")
def my_perms():
    """Frontend gọi sau khi đăng nhập để lọc menu (7 tab + 16 báo cáo) theo quyền.
    'items' là danh sách mã ĐƯỢC xem; FE ẩn mọi mục không nằm trong đây."""
    if not _db_cfg():
        return jsonify({"status": "error", "message": "Chưa đăng nhập SQL Server"}), 401
    _ao = _current_allowed_orgs()
    return jsonify({"status": "ok", "group": _current_group(), "items": sorted(_current_perms()),
                    "app_user": session.get('app_user'), "name": session.get('app_ten'),
                    "nguon": session.get('app_nguon') or 'gsheet',
                    "allowed_orgs": (sorted(_ao) if _ao is not None else None)})

# --------- TAB PHÂN QUYỀN (chỉ ADMIN — guard đã chặn nhóm khác bằng mã 'perm_admin') ---------
# --- Cầu nối lên Google Sheet cho các lệnh QUẢN TRỊ ---
# Mật khẩu tool KHÔNG lưu session (luật từ đầu). Mọi lệnh ghi lên Sheet đều đòi tài khoản
# admin + mật khẩu, nên frontend phải hỏi lại mật khẩu quản trị và gửi kèm theo từng lệnh.
def _gs_admin(d):
    mk = (d.get('admin_pass') or '').strip()
    if not mk:
        raise ValueError('Nhập lại mật khẩu quản trị để ghi lên Google Sheet')
    adm = session.get('app_user') or ''
    # Băm bằng chính tài khoản ADMIN đang đăng nhập — không phải tài khoản bị sửa.
    return {'admin_user': adm, 'admin_pass': _dan_xuat_dk(adm, mk)}

def _loi_chua_cau_hinh():
    """Máy chưa có cấu hình tới nơi lưu tài khoản ⇒ **KHÔNG cho vào**.

    ⚠️ Trước 21/09/2026 nhánh này rơi về phanquyen.json, và không có cả file đó
    thì `app_group='ADMIN'` ⇒ **bất kỳ ai đăng nhập được SQL là thấy đủ 24 mục, mọi
    đơn vị** — im lặng, không một dòng cảnh báo. Quên chép cấu hình sang máy nào là
    máy đó coi như không có phân quyền, mà nhìn bằng mắt thì y hệt bản đúng.
    Nay thiếu cấu hình là chặn thẳng, và nói rõ phải làm gì."""
    return jsonify({
        "status": "error",
        "message": ("Bản cài đặt này chưa được cấu hình để kiểm tra tài khoản và phân quyền.\n"
                    "Liên hệ người quản trị để nhận lại bản cài đúng."),
        "chi_tiet": "Thiếu cấu hình kết nối tới nơi lưu tài khoản (ketnoi.json cạnh EXE).",
    }), 503

def _gs_tra_loi(hanh_dong, **thamso):
    """Gọi Sheet và quy đổi thẳng thành response Flask."""
    try:
        kq = _gs_goi(hanh_dong, **thamso)
    except _GSOffline as e:
        return jsonify({"status": "error",
                        "message": "Không nối được Google Sheet (%s). Quản trị tài khoản "
                                   "bắt buộc phải có mạng." % e}), 503
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 502
    if not kq.get('ok'):
        return jsonify({"status": "error", "message": kq.get('loi') or 'Google Sheet từ chối'}), 400
    return jsonify(dict(kq, status="ok"))

@app.route("/api/perm/config", methods=["GET", "POST"])
def perm_config():
    if not _db_cfg():
        return jsonify({"status": "error", "message": "Chưa đăng nhập"}), 401
    if not _gs_config():
        return _loi_chua_cau_hinh()
    # Cần mật khẩu quản trị (gửi qua POST body, KHÔNG qua URL).
    try:
        adm = _gs_admin(request.json or {})
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e), "can_mat_khau": True}), 401
    try:
        kq = _gs_goi('nap', **adm)
    except _GSOffline as e:
        return jsonify({"status": "error",
                        "message": "Không nối được Google Sheet (%s)." % e}), 503
    if not kq.get('ok'):
        return jsonify({"status": "error", "message": kq.get('loi') or 'Sai mật khẩu quản trị'}), 401
    vai = {c['ma'].upper(): c for c in kq.get('chuc_vu', [])}
    ulist = [{"uid": u['id'], "name": u.get('ho_ten', ''),
              "group": u.get('chuc_vu', ''),
              "group_name": vai.get((u.get('chuc_vu') or '').upper(), {}).get('ten', u.get('chuc_vu', '')),
              "items": sorted(vai.get((u.get('chuc_vu') or '').upper(), {}).get('items', [])),
              "orgs": u.get('don_vi'),
              "active": bool(u.get('active')),
              "co_mat_khau": bool(u.get('co_mat_khau')),
              "dang_nhap_luc": u.get('dang_nhap_luc', ''),
              "ghi_chu": u.get('ghi_chu', '')}
             for u in kq.get('users', [])]
    groups = [{"id": c['ma'], "name": c.get('ten', c['ma']), "items": c.get('items', [])}
              for c in kq.get('chuc_vu', [])]
    return jsonify({"status": "ok", "nguon": "gsheet", "users": ulist, "groups": groups,
                    "all_items": PERM_ALL_ITEMS})

@app.route("/api/perm/user", methods=["POST"])
def perm_save_user():
    if not _db_cfg():
        return jsonify({"status": "error", "message": "Chưa đăng nhập"}), 401
    if not _gs_config():
        return _loi_chua_cau_hinh()
    d = request.json or {}
    uid = (d.get('uid') or '').strip()
    if not uid:
        return jsonify({"status": "error", "message": "Thiếu mã tài khoản"}), 400
    # Chức vụ quyết định quyền → KHÔNG gửi 'items' của riêng user lên Sheet.
    # ⚠️ Độ dài mật khẩu PHẢI kiểm ở đây: Google chỉ nhận được chuỗi băm 44 ký tự
    #    nên phép kiểm "≥ 6 ký tự" bên đó không còn ý nghĩa.
    if d.get('password') and len(d['password']) < 6:
        return jsonify({"status": "error", "message": "Mật khẩu phải từ 6 ký tự trở lên"}), 400
    try:
        adm = _gs_admin(d)
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e), "can_mat_khau": True}), 401
    kq = _gs_tra_loi('luu_user', user_id=uid,
                       ho_ten=(d.get('name') or '').strip(),
                       chuc_vu=(d.get('group') or '').strip(),
                       active=bool(d.get('active', True)),
                       don_vi=(d.get('orgs') if isinstance(d.get('orgs'), list) else []),
                       ghi_chu=d.get('ghi_chu', ''),
                       # Băm bằng tài khoản MỚI (uid), không phải tài khoản admin.
                       mat_khau=(_dan_xuat_dk(uid, d['password']) if d.get('password') else ''),
                       **adm)
    if d.get('password') and not isinstance(kq, tuple):
        # Đổi mật khẩu rồi ⇒ bản cache offline cũ không còn khớp. Phải xoá, không thì
        # máy này **mất mạng vẫn đăng nhập được bằng MẬT KHẨU CŨ** suốt 7 ngày.
        # ⚠️ Chỉ xoá được cache TRÊN MÁY NÀY. Máy khác đã từng đăng nhập bằng mật khẩu
        #    cũ thì vẫn giữ cache đó tới khi hết hạn — hạn chế của mô hình "credential
        #    cached", giống hệt Windows domain. Ghi ra đây để khỏi tưởng đã kín.
        _xoa_cache_uid(uid)
    return kq

@app.route("/api/perm/user/delete", methods=["POST"])
def perm_delete_user():
    if not _db_cfg():
        return jsonify({"status": "error", "message": "Chưa đăng nhập"}), 401
    if not _gs_config():
        return _loi_chua_cau_hinh()
    d = request.json or {}
    uid = (d.get('uid') or '').strip()
    try:
        adm = _gs_admin(d)
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e), "can_mat_khau": True}), 401
    return _gs_tra_loi('xoa_user', user_id=uid, **adm)

# --- CHỨC VỤ (chỉ có khi nguồn là Google Sheet) ---
# Chốt 19/09/2026: CHỨC VỤ QUYẾT ĐỊNH QUYỀN, user không tick riêng nữa.
# Sửa 1 dòng chức vụ là cả nhóm đổi theo — nhưng chỉ có hiệu lực khi người ta đăng nhập lại.
@app.route("/api/perm/role", methods=["POST"])
def perm_save_role():
    if not _db_cfg():
        return jsonify({"status": "error", "message": "Chưa đăng nhập"}), 401
    if not _gs_config():
        return jsonify({"status": "error",
                        "message": "Chức vụ chỉ sửa được khi dùng nguồn Google Sheet"}), 400
    d = request.json or {}
    items = d.get('items')
    if not isinstance(items, list):
        return jsonify({"status": "error", "message": "Thiếu danh sách quyền (items)"}), 400
    try:
        adm = _gs_admin(d)
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e), "can_mat_khau": True}), 401
    # Gửi kèm TOÀN BỘ mã app đang có + nhãn tiếng Việt. Google dùng nó để tự tạo cột cho
    # mục mới và để biết mục nào cần bỏ tick. Trước 21/09/2026 Google lặp hằng PERM ghi cứng
    # trong Code.gs ⇒ mã app mới thêm bị **bỏ qua trong im lặng**, app vẫn báo lưu thành công.
    return _gs_tra_loi('luu_chuc_vu', ma=(d.get('ma') or '').strip(),
                       ten=(d.get('ten') or '').strip(),
                       items=[x for x in items if x in PERM_ALL_ITEMS],
                       tat_ca_muc=list(PERM_ALL_ITEMS),
                       nhan_muc=_nhan_muc_quyen(), **adm)

@app.route("/api/perm/role/delete", methods=["POST"])
def perm_delete_role():
    if not _db_cfg():
        return jsonify({"status": "error", "message": "Chưa đăng nhập"}), 401
    if not _gs_config():
        return jsonify({"status": "error",
                        "message": "Chức vụ chỉ sửa được khi dùng nguồn Google Sheet"}), 400
    d = request.json or {}
    try:
        adm = _gs_admin(d)
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e), "can_mat_khau": True}), 401
    return _gs_tra_loi('xoa_chuc_vu', ma=(d.get('ma') or '').strip(), **adm)

@app.route("/api/perm/password", methods=["POST"])
def perm_set_password():
    """Đổi mật khẩu. Admin đổi hộ người khác, hoặc chính chủ tự đổi (phải kèm mật khẩu cũ).
    Mật khẩu đi theo đường này KHÔNG bao giờ nằm lại trong Sheet — khác với gõ tay lên ô."""
    if not _db_cfg():
        return jsonify({"status": "error", "message": "Chưa đăng nhập"}), 401
    if not _gs_config():
        return _loi_chua_cau_hinh()
    d = request.json or {}
    uid = (d.get('uid') or '').strip()
    mk_moi = d.get('password') or ''
    if not uid:
        return jsonify({"status": "error", "message": "Thiếu mã tài khoản"}), 400
    if len(mk_moi) < 6:
        return jsonify({"status": "error", "message": "Mật khẩu phải từ 6 ký tự trở lên"}), 400
    # Cả mật khẩu cũ lẫn mới đều băm bằng uid CỦA NGƯỜI BỊ ĐỔI.
    tham = {'user_id': uid, 'mat_khau_moi': _dan_xuat_dk(uid, mk_moi)}
    if d.get('old_password'):                 # chính chủ tự đổi
        tham['mat_khau_cu'] = _dan_xuat_dk(uid, d['old_password'])
    else:                                     # admin đổi hộ
        try:
            tham.update(_gs_admin(d))
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e), "can_mat_khau": True}), 401
    kq = _gs_tra_loi('dat_mat_khau', **tham)
    # _gs_tra_loi trả Response khi thành công, trả tuple (Response, mã lỗi) khi hỏng.
    if not isinstance(kq, tuple):
        # Mật khẩu đã đổi ⇒ bản cache offline cũ không còn khớp, phải xoá mục đó.
        try:
            c = _cache_doc_file()
            if c.pop(uid.lower(), None) is not None:
                with open(_cache_path(), 'w', encoding='utf-8') as f:
                    _json.dump(c, f, ensure_ascii=False, indent=1)
        except Exception as e:
            logger.warning('Khong xoa duoc cache sau khi doi mat khau: %s', e)
    return kq

# ---------------------------------------------------------------------------
# DANH MỤC LOẠI CHỨNG TỪ ("Loại CT") — nguồn là dbo.SYS_TRAN, KHÔNG phải
# DISTINCT trên dữ liệu phát sinh.
#
# Bản cũ dựng danh sách bằng `SELECT DISTINCT TRAN_ID FROM dbo.LEDGER` → chỉ ra
# 39 mã (đo 14,9 giây trên IACC_CHULONG) trong khi SYS_TRAN có 90 mã (0,04 giây).
# Hậu quả đã đo 15/09/2026: 35 mã ACTIVE=1 chưa từng có bút toán (SO, SOXU, TX,
# TX1, TX2, HBTL, NKHAU, NMSC, XCK, XKHOK, ADJUST, TS, VAT_BR…) KHÔNG hiện trong
# bộ lọc. Mã chứng từ mới lập luôn rơi vào nhóm này, và nhóm đơn đặt hàng
# (SO/TX/PO) về bản chất không sinh bút toán nên sẽ thiếu vĩnh viễn.
#
# Phạm vi từng tab lấy theo SYS_TRAN.OUTPUT_FORM (form nhập liệu của iPOS) + cột
# IS_SALE — đã đối chiếu dữ liệu thật 15/09/2026: mọi mã trong SALE_VIEW là
# FRMSALE, trong PURCHASE_VIEW là FRMPURCHASE, trong VOUCHER là FRMVOUCHER.
#
# ⚠️ Phải đối chiếu với VIEW mà tab thực sự đọc, KHÔNG phải bảng gốc:
# `SALE_VIEW` và `PURCHASE_VIEW` đều có `WHERE SYS_TRAN.IS_SALE = 1` trong định
# nghĩa view, nên tab Bán hàng chỉ xem được 8/18 mã có trong bảng SALE, tab Mua
# hàng chỉ 5/10 mã của bảng PURCHASE (NKHO, NSP, NSC, NDC, NDCNB có IS_SALE=0).
# Đưa mã IS_SALE=0 vào bộ lọc 2 tab đó là chắc chắn 0 dòng.
#
# Vẫn HỢP thêm mã thực sự có trong từng view làm lưới an toàn — DB khác có thể
# đặt OUTPUT_FORM kiểu khác, và luật ở đây là "thà thừa còn hơn thiếu".
# ---------------------------------------------------------------------------
_tran_usage_cache = {}   # db_name -> {tab: set(TRAN_ID)} — phần phải scan bảng, cache riêng

# Form nhập liệu của iPOS → tab nào trong phần "Danh sách" đọc được chứng từ đó.
# Tab kho nhận cả phiếu xuất (FRMSALE) lẫn phiếu nhập (FRMPURCHASE).
_TRAN_FORM_TABS = {
    'FRMSALE':     ('sale', 'warehouse'),
    'FRMPURCHASE': ('purchase', 'warehouse'),
    'FRMVOUCHER':  ('voucher',),
}
_TRAN_TABS = ('ledger', 'sale', 'purchase', 'warehouse', 'voucher')


def _load_tran_usage(cursor, db_name):
    """Mã chứng từ THỰC SỰ đang có trong từng bảng nghiệp vụ.

    Quét ĐÚNG đối tượng mà từng tab thực sự đọc — SALE_VIEW / PURCHASE_VIEW /
    WAREHOUSE_VIEW / VOUCHER — chứ KHÔNG phải bảng gốc SALE / PURCHASE / WAREHOUSE.
    Quét nhầm bảng gốc là cho ra mã mà tab không bao giờ hiện được: SALE_VIEW và
    PURCHASE_VIEW đều có `WHERE SYS_TRAN.IS_SALE = 1`, nên bảng SALE có 18 mã mà
    view chỉ ra 8; bảng PURCHASE có 10 mã mà view chỉ ra 5 (NKHO/NSP/NSC/NDC/NDCNB
    có IS_SALE=0 nên tab Mua hàng không xem được — hạn chế sẵn có của view).

    Phải scan (không có index trên TRAN_ID) nên cache theo database: đo 15/09/2026 —
    SALE_VIEW 2,93s · PURCHASE_VIEW 0,16s · WAREHOUSE_VIEW 2,97s · VOUCHER 0,23s.
    Vẫn rẻ hơn hẳn DISTINCT trên LEDGER (14,9s) mà bản cũ chạy mỗi lần nạp.
    """
    cached = _tran_usage_cache.get(db_name)
    if cached is not None:
        return cached
    usage = {t: set() for t in _TRAN_TABS}
    try:
        cursor.execute("""
            SELECT 'sale'      AS tab, DISTINCT_ID FROM (SELECT DISTINCT LTRIM(RTRIM(TRAN_ID)) AS DISTINCT_ID FROM dbo.SALE_VIEW      WITH (NOLOCK) WHERE TRAN_ID IS NOT NULL) S
            UNION ALL
            SELECT 'purchase',        DISTINCT_ID FROM (SELECT DISTINCT LTRIM(RTRIM(TRAN_ID)) AS DISTINCT_ID FROM dbo.PURCHASE_VIEW  WITH (NOLOCK) WHERE TRAN_ID IS NOT NULL) P
            UNION ALL
            SELECT 'warehouse',       DISTINCT_ID FROM (SELECT DISTINCT LTRIM(RTRIM(TRAN_ID)) AS DISTINCT_ID FROM dbo.WAREHOUSE_VIEW WITH (NOLOCK) WHERE TRAN_ID IS NOT NULL) W
            UNION ALL
            SELECT 'voucher',         DISTINCT_ID FROM (SELECT DISTINCT LTRIM(RTRIM(TRAN_ID)) AS DISTINCT_ID FROM dbo.VOUCHER        WITH (NOLOCK) WHERE TRAN_ID IS NOT NULL) V
        """)
        for tab, tid in cursor.fetchall():
            if tid:
                usage[tab].add(tid.strip())
    except Exception:
        # Bảng thiếu / lỗi quyền → coi như không có lưới an toàn, vẫn chạy bằng SYS_TRAN.
        usage = {t: set() for t in _TRAN_TABS}
    _tran_usage_cache[db_name] = usage
    return usage


def _build_tran_catalog(cursor, db_name):
    """→ (tran_ids, tran_ids_by_tab, ten_map). Đọc SYS_TRAN mỗi lần gọi (0,04s)
    nên mã chứng từ mới khai báo là thấy ngay, không cần bấm "Danh mục" hay khởi
    động lại EXE. Phần phải scan bảng thì lấy từ _load_tran_usage (có cache).

    CHỈ đưa vào bộ lọc mã đang hoạt động (`ACTIVE = 1`) cho gọn — trên
    `IACC_CHULONG` bỏ được 16 mã đã ngưng dùng (PO, SBO, SD, XKHO2, TSKH,
    VAT_DCT…). NGOẠI LỆ: mã `ACTIVE = 0` mà **vẫn còn chứng từ lịch sử** thì
    phải giữ lại, không thì có dữ liệu mà không lọc ra được.

    Vẫn ĐỌC hết bảng (không `WHERE ACTIVE=1`) để lấy TÊN cho mọi mã: bản cũ lọc
    `ACTIVE=1` ngay lúc lấy tên nên mã ngưng dùng hiện trơ mã, không có tên.
    """
    cursor.execute("""
        SELECT CAST(TRAN_ID AS NVARCHAR(100)), TRAN_NAME, OUTPUT_FORM,
               ISNULL(IS_SALE, 0), ISNULL(ACTIVE, 0)
        FROM dbo.SYS_TRAN WITH (NOLOCK) ORDER BY TRAN_ID
    """)
    rows = [(r[0].strip(), (r[1] or '').strip(), (r[2] or '').strip().upper(),
             int(r[3] or 0), int(r[4] or 0))
            for r in cursor.fetchall() if r[0]]

    usage   = _load_tran_usage(cursor, db_name)
    by_tab  = {t: [] for t in _TRAN_TABS}
    name_of = {tid: (nm or tid) for tid, nm, _f, _s, _a in rows}
    seen    = set()

    for tid, nm, form, is_sale, active in rows:
        seen.add(tid)
        item = {"id": tid, "name": nm or tid}
        used_in = [t for t in _TRAN_TABS if tid in usage.get(t, ())]

        if active:
            by_tab['ledger'].append(item)      # sổ tổng hợp nhận mọi loại chứng từ
            for tab in _TRAN_FORM_TABS.get(form, ()):
                # SALE_VIEW và PURCHASE_VIEW lọc IS_SALE=1 ngay trong định nghĩa view ⇒
                # mã IS_SALE=0 có đưa vào bộ lọc cũng không bao giờ ra dòng nào.
                # WAREHOUSE_VIEW lọc theo hàng hoá (IS_WAREHOUSE_BALANCE) chứ không theo
                # loại chứng từ, nên tab kho không áp điều kiện này.
                if tab in ('sale', 'purchase') and not is_sale:
                    continue
                by_tab[tab].append(item)
        elif used_in:
            # Đã ngưng dùng NHƯNG còn chứng từ lịch sử → vẫn phải lọc ra được.
            by_tab['ledger'].append(item)

        for tab in used_in:                    # lưới an toàn: có thật thì phải hiện
            if tab != 'ledger' and item not in by_tab[tab]:
                by_tab[tab].append(item)

    # Mã đang dùng thật nhưng KHÔNG khai trong SYS_TRAN (DB khác có thể gặp) —
    # vẫn phải lọc được, tên hiển thị bằng chính mã.
    for tab in _TRAN_TABS:
        for tid in sorted(usage.get(tab, ())):
            if tid not in seen:
                item = {"id": tid, "name": tid}
                by_tab[tab].append(item)
                if item not in by_tab['ledger']:
                    by_tab['ledger'].append(item)
                name_of.setdefault(tid, tid)

    for tab in _TRAN_TABS:
        by_tab[tab].sort(key=lambda it: it['id'])
    return by_tab['ledger'], by_tab, name_of


@app.route("/api/metadata")
@with_db_lock
def get_metadata():
    try:
        db_name = (_db_cfg() or {}).get('database', 'N/A')

        if db_name in _meta_cache:
            # Danh mục nặng (TK, hàng hoá, đối tượng…) giữ nguyên cache, nhưng danh
            # sách LOẠI CHỨNG TỪ thì đọc lại SYS_TRAN mỗi lần (0,04s): mã mới khai
            # báo phải thấy ngay, không bắt người dùng đi tìm nút "Danh mục".
            cached = _meta_cache[db_name]
            try:
                t_all, t_by_tab, _ = _build_tran_catalog(get_connection().cursor(), db_name)
                cached["tran_ids"]        = t_all
                cached["tran_ids_by_tab"] = t_by_tab
            except Exception:
                pass          # đọc lại hỏng thì trả bản cache cũ, đừng làm chết màn hình
            return jsonify(cached)

        conn = get_connection()
        cursor = conn.cursor()

        # Gộp toàn bộ dimension tables thành 1 batch query
        batch_sql = """
            SELECT 'account'   AS kind, CAST(ACCOUNT_ID      AS NVARCHAR(100)), ACCOUNT_NAME, NULL    FROM dbo.DM_ACCOUNT WITH (NOLOCK)     WHERE ACTIVE=1
            UNION ALL
            SELECT 'org',              CAST(ORGANIZATION_ID AS NVARCHAR(100)), ORGANIZATION_NAME, ADDRESS FROM dbo.DM_ORGANIZATION WITH (NOLOCK) WHERE ACTIVE=1
            UNION ALL
            SELECT 'pr_detail',        CAST(PR_DETAIL_ID    AS NVARCHAR(100)), PR_DETAIL_NAME, NULL FROM dbo.DM_PR_DETAIL WITH (NOLOCK)   WHERE ACTIVE=1
            UNION ALL
            SELECT 'job',              CAST(JOB_ID          AS NVARCHAR(100)), JOB_NAME,        NULL FROM dbo.DM_JOB WITH (NOLOCK)         WHERE ACTIVE=1
            UNION ALL
            SELECT 'item',             CAST(ITEM_ID         AS NVARCHAR(100)), ITEM_NAME,       NULL FROM dbo.DM_ITEM WITH (NOLOCK)        WHERE ACTIVE=1
            UNION ALL
            SELECT 'expense',          CAST(EXPENSE_ID      AS NVARCHAR(100)), EXPENSE_NAME,    NULL FROM dbo.DM_EXPENSE WITH (NOLOCK)     WHERE ACTIVE=1
            UNION ALL
            SELECT 'product',          CAST(PRODUCT_ID      AS NVARCHAR(100)), PRODUCT_NAME,    NULL FROM dbo.DM_PRODUCT WITH (NOLOCK)     WHERE ACTIVE=1
            UNION ALL
            SELECT 'warehouse',        CAST(WAREHOUSE_ID    AS NVARCHAR(100)), WAREHOUSE_NAME,  NULL FROM dbo.DM_WAREHOUSE WITH (NOLOCK)   WHERE ACTIVE=1
            UNION ALL
            SELECT 'unit',             CAST(UNIT_ID         AS NVARCHAR(100)), UNIT_NAME,       NULL FROM dbo.DM_UNIT WITH (NOLOCK)        WHERE ACTIVE=1
            UNION ALL
            SELECT 'banks',            CAST(BANK_ID         AS NVARCHAR(100)), BANK_NAME,       NULL FROM dbo.DM_BANK WITH (NOLOCK)        WHERE ACTIVE=1
        """
        cursor.execute(batch_sql)
        accounts, orgs, pr_details, jobs, items, expenses, products, warehouses, units, banks = [], [], [], [], [], [], [], [], [], []
        bucket = {
            'account': accounts, 'org': orgs, 'pr_detail': pr_details,
            'job': jobs, 'item': items, 'expense': expenses, 'product': products,
            'warehouse': warehouses, 'unit': units, 'banks': banks
        }
        for kind, id_val, name_val, extra_val in cursor.fetchall():
            item = {"id": (id_val or '').strip(), "name": name_val or ''}
            if extra_val: item["address"] = extra_val
            bucket[kind].append(item)


        # Thông tin công ty cho tiêu đề báo cáo — lấy từ dbo.SYS_SYSTEMVAR (key-value)
        company = {"name": "", "address": "", "tax_code": ""}
        try:
            cursor.execute("""SELECT VAR_NAME, VAR_VALUE FROM dbo.SYS_SYSTEMVAR WITH (NOLOCK)
                              WHERE VAR_NAME IN ('COMPANY_NAME','PARENT_COMPANY','ADDRESS','TAX_FILE_NUMBER')""")
            sv = {r[0]: (r[1] or '').strip() for r in cursor.fetchall()}
            company = {
                "name":     sv.get('COMPANY_NAME') or sv.get('PARENT_COMPANY') or '',
                "address":  sv.get('ADDRESS', ''),
                "tax_code": sv.get('TAX_FILE_NUMBER', ''),
            }
        except Exception:
            pass

        tran_ids, tran_ids_by_tab, _ = _build_tran_catalog(cursor, db_name)

        # Lấy row count từ metadata SQL Server (tức thì, không scan bảng)
        # index_id 0=heap, 1=clustered → IN (0,1) đảm bảo lấy đúng 1 cái
        cursor.execute("""
            SELECT ISNULL(SUM(row_count), 0)
            FROM sys.dm_db_partition_stats
            WHERE object_id = OBJECT_ID('dbo.LEDGER') AND index_id IN (0, 1)
        """)
        global_total = int(cursor.fetchone()[0] or 0)

        result = {
            "status": "ok",
            "db_info": {"database": db_name},
            "company": company,
            "global_total": global_total,
            "accounts": accounts, "orgs": orgs, "pr_details": pr_details,
            "tran_ids": tran_ids, "tran_ids_by_tab": tran_ids_by_tab,
            "jobs": jobs, "items": items,
            "products": products, "expenses": expenses, "warehouses": warehouses,
            "units": units, "banks": banks
        }
        _meta_cache[db_name] = result
        return jsonify(result)
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()  # Conn có thể đã chết → drop khỏi pool
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500

@app.route("/api/metadata/refresh", methods=["POST"])
def refresh_metadata():
    db_name = (_db_cfg() or {}).get('database')
    if db_name:
        _meta_cache.pop(db_name, None)
        _tran_usage_cache.pop(db_name, None)   # bấm "Danh mục" thì quét lại cả mã đang dùng thật
    return jsonify({"status": "ok"})

# Whitelist cột được phép sort cho từng endpoint — tránh SQL injection
LEDGER_SORT_WHITELIST = {
    "TRAN_DATE":         "L.TRAN_DATE",
    "TRAN_NO":           "L.TRAN_NO",
    "TRAN_ID":           "L.TRAN_ID",
    "ACCOUNT_ID":        "L.ACCOUNT_ID",
    "ACCOUNT_ID_CONTRA": "L.ACCOUNT_ID_CONTRA",
    "DESCRIPTION":       "L.DESCRIPTION",
    "AMOUNT":            "L.AMOUNT",
    "ORGANIZATION_ID":   "L.ORGANIZATION_ID",
    "PR_DETAIL_ID":      "L.PR_DETAIL_ID",
    "JOB_ID":            "L.JOB_ID",
    "ITEM_ID":           "L.ITEM_ID",
    "PRODUCT_ID":        "L.PRODUCT_ID",
    "EXPENSE_ID":        "L.EXPENSE_ID",
}

PURCHASE_SORT_WHITELIST = {col: f"P.{col}" for col in [
    "ORGANIZATION_ID","TRAN_ID","TRAN_NO","TRAN_DATE","VAT_TRAN_NO","VAT_TRAN_DATE",
    "PO_TRAN_NO","WAREHOUSE_ID","WAREHOUSE_NAME","ITEM_ID","DESCRIPTION","UNIT_ID",
    "QUANTITY","UNIT_ID_WH","QUANTITY_WH","UNIT_PRICE","DISCOUNT_AMOUNT","PURCHASE_COST",
    "VAT_TAX_RATE","VAT_TAX_AMOUNT","TOTAL_AMOUNT","ACCOUNT_ID_COST","PR_DETAIL_ID",
    "PR_DETAIL_NAME","EXPENSE_ID","JOB_ID","JOB_NAME"
]}
PURCHASE_SORT_WHITELIST["ORGANIZATION_NAME"] = "O.ORGANIZATION_NAME"
PURCHASE_SORT_WHITELIST["EXPENSE_NAME"]      = "E.EXPENSE_NAME"

WAREHOUSE_SORT_WHITELIST = {col: f"W.{col}" for col in [
    "ISSUE_RECEIVE","ORGANIZATION_ID","TRAN_ID","TRAN_NO","TRAN_DATE",
    "WAREHOUSE_ID","WAREHOUSE_NAME","WAREHOUSE_ID_ISSUE","ITEM_ID","ITEM_NAME",
    "UNIT_ID_WH","QUANTITY","UNIT_ID_EXTRA","QUANTITY_EXTRA","UNIT_PRICE","AMOUNT",
    "ACCOUNT_ID","ACCOUNT_ID_CONTRA","PR_DETAIL_ID","PR_DETAIL_NAME",
    "EXPENSE_ID","EXPENSE_NAME","JOB_ID","JOB_NAME"
]}
WAREHOUSE_SORT_WHITELIST["ORGANIZATION_NAME"]    = "O.ORGANIZATION_NAME"
WAREHOUSE_SORT_WHITELIST["WAREHOUSE_NAME_ISSUE"] = "WI.WAREHOUSE_NAME"


def _resolve_order_by(request_args, whitelist, default_sql):
    """Trả về ORDER BY clause an toàn từ request args."""
    col = request_args.get("order_by", "").strip()
    direction = request_args.get("order_dir", "desc").strip().lower()
    direction = "ASC" if direction == "asc" else "DESC"
    sql_col = whitelist.get(col)
    if not sql_col:
        return default_sql
    return f"{sql_col} {direction}"


def _apply_date_search(s_date, clauses, params):
    """Parse input ngày (cột 'Ngày CT') thành WHERE filter SARGable nhất có thể.

    Các dạng hỗ trợ:
      - "dd/mm/yyyy"   → exact date (SARGable)
      - "mm/yyyy"      → range toàn bộ tháng (SARGable)
      - "yyyy"         → range toàn bộ năm (SARGable)
      - "dd/mm"        → DAY(..)=dd AND MONTH(..)=mm (non-SARGable nhưng cơ hội dùng data lọc nhỏ hơn CONVERT+LIKE)
      - "dd"           → DAY(..)=dd (non-SARGable)
      - khác           → fallback CONVERT+LIKE (tương thích cũ)
    """
    s = s_date.strip()
    parts = [p for p in s.split('/') if p != '']
    try:
        if len(parts) == 3:
            d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
            if y < 100: y += 2000
            dt = date(y, m, d)
            clauses.append("L.TRAN_DATE = ?")
            params.append(dt.strftime("%Y%m%d"))
            return
        if len(parts) == 2:
            a, b = int(parts[0]), int(parts[1])
            # Phân biệt "mm/yyyy" vs "dd/mm"
            if b >= 1900:  # "mm/yyyy"
                month, year = a, b
                if 1 <= month <= 12:
                    start = date(year, month, 1)
                    end   = date(year+1, 1, 1) if month == 12 else date(year, month+1, 1)
                    clauses.append("L.TRAN_DATE >= ? AND L.TRAN_DATE < ?")
                    params.extend([start.strftime("%Y%m%d"), end.strftime("%Y%m%d")])
                    return
            # "dd/mm"
            if 1 <= a <= 31 and 1 <= b <= 12:
                clauses.append("DAY(L.TRAN_DATE) = ? AND MONTH(L.TRAN_DATE) = ?")
                params.extend([a, b])
                return
        if len(parts) == 1:
            n = int(parts[0])
            if n >= 1900:  # cả năm
                start = date(n, 1, 1)
                end   = date(n+1, 1, 1)
                clauses.append("L.TRAN_DATE >= ? AND L.TRAN_DATE < ?")
                params.extend([start.strftime("%Y%m%d"), end.strftime("%Y%m%d")])
                return
            if 1 <= n <= 31:  # ngày trong tháng
                clauses.append("DAY(L.TRAN_DATE) = ?")
                params.append(n)
                return
    except (ValueError, TypeError):
        pass
    # Fallback: giữ behavior cũ cho input không theo pattern
    clauses.append("CONVERT(VARCHAR(10), L.TRAN_DATE, 103) LIKE ?")
    params.append(f"%{s}%")

def _build_where(request_args):
    """Xây dựng WHERE clause + params từ request args. Trả về (where_sql, params, has_join_search)."""
    f_date = request_args.get("from_date", "01/01/2026")
    t_date = request_args.get("to_date",  "31/12/2026")
    from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
    to_dt   = datetime.strptime(t_date, "%d/%m/%Y").date()

    clauses = ["L.TRAN_DATE >= ?", "L.TRAN_DATE <= ?"]
    params  = [from_dt.strftime("%Y%m%d"), to_dt.strftime("%Y%m%d")]

    # IN filters
    for field, arg in [
        ("L.TRAN_ID",          "tran_ids"),
        ("L.ORGANIZATION_ID",  "org_ids"),
        ("L.JOB_ID",           "job_ids"),
        ("L.PR_DETAIL_ID",     "pr_detail_ids"),
        ("L.ITEM_ID",          "item_ids"),
        ("L.PRODUCT_ID",       "product_ids"),
        ("L.EXPENSE_ID",       "expense_ids"),
    ]:
        raw = request_args.get(arg, "")
        vals = [v for v in raw.split(",") if v]
        if arg == "org_ids":
            # Lọc đơn vị LUÔN đi qua _org_filter_sql — nơi DUY NHẤT ép quyền đơn vị theo tài
            # khoản (chọn gì cũng bị giao với danh sách được phép). Không chọn ⇒ mặc định loại
            # đơn vị ngoài cây '00', hoặc = đúng đơn vị được phép nếu tài khoản bị giới hạn.
            _oc, _op = _org_filter_sql(vals, field)
            if _oc:
                clauses.append(_oc)
                params.extend(_op)
        elif vals:
            clauses.append(f"{field} IN ({','.join(['?']*len(vals))})")
            params.extend(vals)

    # Tài khoản / TK đối ứng: nếu chọn TK mẹ (vd 641) → match cả TK con (6411..6419)
    # Dùng LIKE 'xxx%' (SARGable) thay cho IN exact match
    for field, arg in [
        ("L.ACCOUNT_ID",       "acc_ids"),
        ("L.ACCOUNT_ID_CONTRA", "contra_acc_ids"),
    ]:
        raw = request_args.get(arg, "")
        vals = [v for v in raw.split(",") if v]
        if vals:
            like_clauses = [f"{field} LIKE ?" for _ in vals]
            clauses.append("(" + " OR ".join(like_clauses) + ")")
            params.extend([f"{v}%" for v in vals])

    # LIKE search trên cột LEDGER
    # ID fields: trailing wildcard → dùng được index (100x nhanh hơn)
    # TEXT fields: contains → chấp nhận chậm do người dùng cần tìm keyword giữa câu
    ID_PREFIX_FIELDS = [
        ("L.TRAN_NO",          "tran_no"),
        ("L.TRAN_ID",          "s_tran_id"),
        ("L.ACCOUNT_ID",       "s_acc_id"),
        ("L.ACCOUNT_ID_CONTRA", "s_contra_id"),
        ("L.ORGANIZATION_ID",  "s_org_id"),
    ]
    TEXT_CONTAINS_FIELDS = [
        ("L.DESCRIPTION",      "s_desc"),
    ]

    for field, arg in ID_PREFIX_FIELDS:
        val = request_args.get(arg, "").strip()
        if val:
            clauses.append(f"{field} LIKE ?")
            params.append(f"{val}%")  # trailing wildcard — SARGable

    for field, arg in TEXT_CONTAINS_FIELDS:
        val = request_args.get(arg, "").strip()
        if val:
            clauses.append(f"{field} LIKE ?")
            params.append(f"%{val}%")

    # Tìm theo ngày — parse thành filter SARGable thay vì CONVERT+LIKE
    s_date = request_args.get("s_date", "").strip()
    if s_date:
        _apply_date_search(s_date, clauses, params)

    # LIKE trên cột JOIN — NAME: dùng contains vì tên VN thường có tiền tố
    # (VD: "Phí điện", "Phí nước" → gõ "điện" tìm keyword giữa câu)
    join_clauses = []
    join_params  = []
    for field, arg in [
        ("PD.PR_DETAIL_NAME", "s_pr_name"),
        ("E.EXPENSE_NAME",    "s_exp_name"),
        ("O.ORGANIZATION_NAME","s_org_name"),
        ("I.ITEM_NAME",       "s_item_name"),
        ("P.ITEM_NAME",       "s_prod_name"),
    ]:
        val = request_args.get(arg, "").strip()
        if val:
            join_clauses.append(f"{field} LIKE ?")
            join_params.append(f"%{val}%")

    return " AND ".join(clauses), params, join_clauses, join_params

@app.route("/api/ledger")
@with_db_lock
def get_ledger():
    try:
        page      = int(request.args.get("page",     1))
        page_size = int(request.args.get("page_size", 100))
        export_all = request.args.get("export_all") == "1"
        # Nếu frontend biết total từ lần query trước (đổi trang) → skip COUNT+SUM
        known_total  = request.args.get("known_total")
        known_deb    = request.args.get("known_deb")
        known_crd    = request.args.get("known_crd")
        skip_count   = page > 1 and known_total is not None and not export_all

        where_sql, params, join_clauses, join_params = _build_where(request.args)

        order_by_sql = _resolve_order_by(request.args, LEDGER_SORT_WHITELIST, "L.TRAN_DATE DESC, L.TRAN_NO")

        offset = (page - 1) * page_size

        # ---- CÁC CỘT LEDGER CƠ BẢN (không JOIN) ----
        BASE_COLS = """
            L.TRAN_DATE, L.TRAN_NO, L.TRAN_ID, L.DEBIT_CREDIT,
            L.ACCOUNT_ID, L.ACCOUNT_ID_CONTRA,
            L.PR_DETAIL_ID, L.DESCRIPTION, L.COMMENTS,
            L.AMOUNT, L.JOB_ID,
            L.ITEM_ID, L.PRODUCT_ID,
            L.EXPENSE_ID, L.ORGANIZATION_ID, L.BANK_ID, L.BANK_ID_CONTRA,
            L.EXPENSE_ID_CONTRA, L.PR_DETAIL_ID_CONTRA, L.JOB_ID_CONTRA, L.ITEM_ID_CONTRA
        """

        if join_clauses:
            # Có search trên cột tên → buộc phải JOIN các bảng dimension liên quan
            join_filter = " AND ".join(join_clauses)

            # Chỉ JOIN đúng bảng cần thiết cho search
            needed = set()
            for c in join_clauses:
                if 'PD.' in c: needed.add('pd')
                if 'E.'  in c: needed.add('e')
                if 'O.'  in c: needed.add('o')
                if 'I.'  in c: needed.add('i')
                if 'P.'  in c: needed.add('p')

            joins = ["FROM dbo.LEDGER L WITH (NOLOCK)"]
            if 'pd' in needed: joins.append("LEFT JOIN dbo.DM_PR_DETAIL   PD WITH (NOLOCK) ON L.PR_DETAIL_ID    = PD.PR_DETAIL_ID")
            if 'i'  in needed: joins.append("LEFT JOIN dbo.DM_ITEM         I  WITH (NOLOCK) ON L.ITEM_ID         = I.ITEM_ID")
            if 'p'  in needed: joins.append("LEFT JOIN dbo.DM_ITEM         P  WITH (NOLOCK) ON L.PRODUCT_ID      = P.ITEM_ID")
            if 'e'  in needed: joins.append("LEFT JOIN dbo.DM_EXPENSE      E  WITH (NOLOCK) ON L.EXPENSE_ID      = E.EXPENSE_ID")
            if 'o'  in needed: joins.append("LEFT JOIN dbo.DM_ORGANIZATION O  WITH (NOLOCK) ON L.ORGANIZATION_ID = O.ORGANIZATION_ID")
            JOIN_TABLES = " ".join(joins)

            count_sql = f"""
                SELECT
                    COUNT(*) AS total_rows,
                    SUM(CASE WHEN L.DEBIT_CREDIT='DEB' THEN L.AMOUNT ELSE 0 END) AS sum_deb,
                    SUM(CASE WHEN L.DEBIT_CREDIT='CRD' THEN L.AMOUNT ELSE 0 END) AS sum_crd
                {JOIN_TABLES}
                WHERE {where_sql}
                AND {join_filter}
            """

            # Phân trang ROW_NUMBER(): tương thích SQL Server 2005+ (bao gồm cả SQL Server 2008)
            paged_sql = f"""
                SELECT * FROM (
                    SELECT {BASE_COLS},
                           ROW_NUMBER() OVER (ORDER BY {order_by_sql}) AS RowNum
                    {JOIN_TABLES}
                    WHERE {where_sql}
                    AND {join_filter}
                ) AS RowConstrainedResult
                WHERE RowNum > ? AND RowNum <= ?
            """
            count_params = params + join_params
            data_params  = params + join_params
        else:
            # KHÔNG có join search → không JOIN gì cả (nhanh nhất có thể)
            # Tên dimension sẽ được map ở Python từ _meta_cache
            count_sql = f"""
                SELECT
                    COUNT(*) AS total_rows,
                    SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT ELSE 0 END) AS sum_deb,
                    SUM(CASE WHEN DEBIT_CREDIT='CRD' THEN AMOUNT ELSE 0 END) AS sum_crd
                FROM dbo.LEDGER L WITH (NOLOCK)
                WHERE {where_sql}
            """

            paged_sql = f"""
                SELECT * FROM (
                    SELECT {BASE_COLS},
                           ROW_NUMBER() OVER (ORDER BY {order_by_sql}) AS RowNum
                    FROM dbo.LEDGER L WITH (NOLOCK)
                    WHERE {where_sql}
                ) AS RowConstrainedResult
                WHERE RowNum > ? AND RowNum <= ?
            """
            count_params = params
            data_params  = params

        conn   = get_connection()
        cursor = conn.cursor()

        if export_all:
            if join_clauses:
                sql = f"""
                    SELECT {BASE_COLS}
                    {JOIN_TABLES}
                    WHERE {where_sql}
                    AND {join_filter}
                    ORDER BY {order_by_sql}
                """
                cursor.execute(sql, data_params)
            else:
                sql = f"""
                    SELECT {BASE_COLS}
                    FROM dbo.LEDGER L WITH (NOLOCK)
                    WHERE {where_sql}
                    ORDER BY {order_by_sql}
                """
                cursor.execute(sql, data_params)
            columns  = [col[0] for c_idx, col in enumerate(cursor.description)]
            raw_rows = cursor.fetchall()
            total_rows = len(raw_rows)
            total_debit = 0
            total_credit = 0
            # Note: with export_all we don't calculate sum in python for large sets, or we can calculate it
            for r in raw_rows:
                dc = r[columns.index('DEBIT_CREDIT')] if 'DEBIT_CREDIT' in columns else None
                amt = float(r[columns.index('AMOUNT')] or 0) if 'AMOUNT' in columns else 0
                if dc == 'DEB': total_debit += amt
                elif dc == 'CRD': total_credit += amt
        else:
            # Query 1: COUNT + SUM — chỉ chạy khi page=1 hoặc frontend không biết total
            if skip_count:
                total_rows   = int(known_total)
                total_debit  = float(known_deb or 0)
                total_credit = float(known_crd or 0)
            else:
                cursor.execute(count_sql, count_params)
                count_row    = cursor.fetchone()
                total_rows   = count_row[0] or 0
                total_debit  = float(count_row[1] or 0)
                total_credit = float(count_row[2] or 0)
            
            # Query 2: Data trang hiện tại (ROW_NUMBER)
            cursor.execute(paged_sql, data_params + [offset, offset + page_size])
            columns  = [col[0] for col in cursor.description]
            raw_rows = cursor.fetchall()

        # Chuẩn bị dimension maps từ cache (để post-enrich khi không JOIN)
        db_name = (_db_cfg() or {}).get('database', 'N/A')
        meta = _meta_cache.get(db_name)
        if meta is None:
            # Cache chưa có → populate bằng cách truy vấn dimension nhẹ
            # (xảy ra 1 lần sau khi login trực tiếp vào ledger mà chưa mở filter)
            try:
                cur2 = conn.cursor()
                cur2.execute("""
                    SELECT 'pr_details' k, CAST(PR_DETAIL_ID AS NVARCHAR(100)), PR_DETAIL_NAME FROM dbo.DM_PR_DETAIL WITH (NOLOCK) WHERE ACTIVE=1
                    UNION ALL SELECT 'items',    CAST(ITEM_ID AS NVARCHAR(100)),   ITEM_NAME    FROM dbo.DM_ITEM WITH (NOLOCK)     WHERE ACTIVE=1
                    UNION ALL SELECT 'products', CAST(PRODUCT_ID AS NVARCHAR(100)), PRODUCT_NAME FROM dbo.DM_PRODUCT WITH (NOLOCK)  WHERE ACTIVE=1
                    UNION ALL SELECT 'expenses', CAST(EXPENSE_ID AS NVARCHAR(100)), EXPENSE_NAME FROM dbo.DM_EXPENSE WITH (NOLOCK)  WHERE ACTIVE=1
                    UNION ALL SELECT 'orgs',     CAST(ORGANIZATION_ID AS NVARCHAR(100)), ORGANIZATION_NAME FROM dbo.DM_ORGANIZATION WITH (NOLOCK) WHERE ACTIVE=1
                    UNION ALL SELECT 'tran_ids', CAST(TRAN_ID AS NVARCHAR(100)), TRAN_NAME FROM dbo.SYS_TRAN WITH (NOLOCK)
                    UNION ALL SELECT 'banks',    CAST(BANK_ID AS NVARCHAR(100)), BANK_NAME FROM dbo.DM_BANK WITH (NOLOCK) WHERE ACTIVE=1
                    UNION ALL SELECT 'jobs',     CAST(JOB_ID AS NVARCHAR(100)), JOB_NAME  FROM dbo.DM_JOB WITH (NOLOCK)  WHERE ACTIVE=1
                """)
                partial = {'pr_details': [], 'items': [], 'products': [], 'expenses': [], 'orgs': [], 'tran_ids': [], 'banks': [], 'jobs': []}
                for k, i, n in cur2.fetchall():
                    partial[k].append({'id': (i or '').strip(), 'name': n or ''})
                meta = partial
            except Exception:
                meta = {}
        meta = meta or {}
        def _build_map(key):
            return {(it.get('id') or '').strip(): it.get('name') or '' for it in meta.get(key, [])}
        pr_map   = _build_map('pr_details')
        item_map = _build_map('items')
        prod_map = _build_map('products')
        exp_map  = _build_map('expenses')
        org_map  = _build_map('orgs')
        tran_map = _build_map('tran_ids')
        bank_map = _build_map('banks')
        job_map  = _build_map('jobs')

        # Tối ưu cho payload lớn (500k+ dòng): pre-compute column indices, tránh
        # dict(zip()) + .get() trong vòng lặp nóng. Build dict trực tiếp bằng index.
        col_idx = {c: i for i, c in enumerate(columns)}
        idx_pr     = col_idx.get('PR_DETAIL_ID', -1)
        idx_pr_contra = col_idx.get('PR_DETAIL_ID_CONTRA', -1)
        idx_item   = col_idx.get('ITEM_ID', -1)
        idx_item_contra = col_idx.get('ITEM_ID_CONTRA', -1)
        idx_prod   = col_idx.get('PRODUCT_ID', -1)
        idx_exp    = col_idx.get('EXPENSE_ID', -1)
        idx_exp_contra = col_idx.get('EXPENSE_ID_CONTRA', -1)
        idx_org    = col_idx.get('ORGANIZATION_ID', -1)
        idx_tran   = col_idx.get('TRAN_ID', -1)
        idx_bank   = col_idx.get('BANK_ID', -1)
        idx_bank_contra = col_idx.get('BANK_ID_CONTRA', -1)
        idx_date   = col_idx.get('TRAN_DATE', -1)
        idx_job    = col_idx.get('JOB_ID', -1)
        idx_job_contra = col_idx.get('JOB_ID_CONTRA', -1)
        has_pr_name   = 'PR_DETAIL_NAME' in col_idx
        has_pr_name_contra = 'PR_DETAIL_NAME_CONTRA' in col_idx
        has_item_name = 'ITEM_NAME' in col_idx
        has_item_name_contra = 'ITEM_NAME_CONTRA' in col_idx
        has_prod_name = 'PRODUCT_NAME' in col_idx
        has_exp_name  = 'EXPENSE_NAME' in col_idx
        has_exp_name_contra = 'EXPENSE_NAME_CONTRA' in col_idx
        has_org_name  = 'ORGANIZATION_NAME' in col_idx
        has_tran_name = 'TRAN_NAME' in col_idx
        has_bank_name = 'BANK_NAME' in col_idx
        has_bank_name_contra = 'BANK_NAME_CONTRA' in col_idx
        has_job_name = 'JOB_NAME' in col_idx
        has_job_name_contra = 'JOB_NAME_CONTRA' in col_idx

        def _strip(v):
            return v.strip() if isinstance(v, str) else (v or '')

        rows = []
        rows_append = rows.append
        for raw in raw_rows:
            r = {columns[i]: raw[i] for i in range(len(columns))}
            if idx_date != -1:
                dv = raw[idx_date]
                if isinstance(dv, (date, datetime)):
                    r['TRAN_DATE'] = dv.strftime("%d/%m/%Y")
            if not has_pr_name and idx_pr != -1:
                r['PR_DETAIL_NAME']    = pr_map.get(_strip(raw[idx_pr]), '')
            if not has_pr_name_contra and idx_pr_contra != -1:
                r['PR_DETAIL_NAME_CONTRA'] = pr_map.get(_strip(raw[idx_pr_contra]), '')
            if not has_item_name and idx_item != -1:
                r['ITEM_NAME']         = item_map.get(_strip(raw[idx_item]), '')
            if not has_item_name_contra and idx_item_contra != -1:
                r['ITEM_NAME_CONTRA']  = item_map.get(_strip(raw[idx_item_contra]), '')
            if not has_prod_name and idx_prod != -1:
                r['PRODUCT_NAME']      = item_map.get(_strip(raw[idx_prod]), '')
            if not has_exp_name and idx_exp != -1:
                r['EXPENSE_NAME']      = exp_map.get(_strip(raw[idx_exp]), '')
            if not has_exp_name_contra and idx_exp_contra != -1:
                r['EXPENSE_NAME_CONTRA'] = exp_map.get(_strip(raw[idx_exp_contra]), '')
            if not has_job_name and idx_job != -1:
                r['JOB_NAME']          = job_map.get(_strip(raw[idx_job]), '')
            if not has_job_name_contra and idx_job_contra != -1:
                r['JOB_NAME_CONTRA']   = job_map.get(_strip(raw[idx_job_contra]), '')
            if not has_org_name and idx_org != -1:
                r['ORGANIZATION_NAME'] = org_map.get(_strip(raw[idx_org]), '')
            if not has_tran_name and idx_tran != -1:
                r['TRAN_NAME']         = tran_map.get(_strip(raw[idx_tran]), '')
            if not has_bank_name and idx_bank != -1:
                r['BANK_NAME']         = bank_map.get(_strip(raw[idx_bank]), '')
            if not has_bank_name_contra and idx_bank_contra != -1:
                r['BANK_NAME_CONTRA']  = bank_map.get(_strip(raw[idx_bank_contra]), '')
            rows_append(r)

        return jsonify({
            "status": "ok",
            "data": rows,
            "pagination": {
                "total_rows":  total_rows,
                "total_pages": max(1, (total_rows + page_size - 1) // page_size) if not export_all else 1,
                "page": page if not export_all else 1
            },
            "summary": {
                "total_debit":  total_debit,
                "total_credit": total_credit
            }
        })
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


# Cột lấy trực tiếp từ PURCHASE_VIEW (P). View đã có WAREHOUSE_NAME và JOB_NAME.
# Chỉ ORGANIZATION_NAME và EXPENSE_NAME phải JOIN bảng dimension.
PURCHASE_BASE_COLUMNS = [
    "ORGANIZATION_ID",
    "TRAN_ID", "TRAN_NO", "TRAN_DATE",
    "VAT_TRAN_NO", "VAT_TRAN_DATE", "PO_TRAN_NO",
    "WAREHOUSE_ID", "WAREHOUSE_NAME",
    "ITEM_ID", "DESCRIPTION", "UNIT_ID",
    "QUANTITY", "UNIT_ID_WH", "QUANTITY_WH",
    "UNIT_PRICE", "DISCOUNT_AMOUNT", "PURCHASE_COST",
    "VAT_TAX_RATE", "VAT_TAX_AMOUNT", "TOTAL_AMOUNT",
    "ACCOUNT_ID_COST",
    "EXPENSE_ID",
    "JOB_ID", "JOB_NAME",
    "PR_DETAIL_ID", "PR_DETAIL_NAME",
]

def _build_purchase_where(request_args):
    """WHERE + params cho dbo.PURCHASE_VIEW. Dùng alias P. Trả (where_sql, params)."""
    f_date = request_args.get("from_date", "01/01/2026")
    t_date = request_args.get("to_date",  "31/12/2026")
    from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
    to_dt   = datetime.strptime(t_date, "%d/%m/%Y").date()

    clauses = ["P.TRAN_DATE >= ?", "P.TRAN_DATE <= ?"]
    params  = [from_dt.strftime("%Y%m%d"), to_dt.strftime("%Y%m%d")]

    for field, arg in [
        ("P.TRAN_ID",        "tran_ids"),
        ("P.ORGANIZATION_ID", "org_ids"),
        ("P.JOB_ID",         "job_ids"),
        ("P.ITEM_ID",        "item_ids"),
        ("P.EXPENSE_ID",     "expense_ids"),
        ("P.PR_DETAIL_ID",   "pr_detail_ids"),
        ("P.WAREHOUSE_ID",   "wh_ids"),
    ]:
        raw = request_args.get(arg, "")
        vals = [v for v in raw.split(",") if v]
        if arg == "org_ids":
            # Lọc đơn vị LUÔN đi qua _org_filter_sql — nơi DUY NHẤT ép quyền đơn vị theo tài
            # khoản (chọn gì cũng bị giao với danh sách được phép). Không chọn ⇒ mặc định loại
            # đơn vị ngoài cây '00', hoặc = đúng đơn vị được phép nếu tài khoản bị giới hạn.
            _oc, _op = _org_filter_sql(vals, field)
            if _oc:
                clauses.append(_oc)
                params.extend(_op)
        elif vals:
            clauses.append(f"{field} IN ({','.join(['?']*len(vals))})")
            params.extend(vals)

    # ID prefix LIKE
    for field, arg in [
        ("P.TRAN_NO",        "tran_no"),
        ("P.TRAN_ID",        "s_tran_id"),
        ("P.ORGANIZATION_ID", "s_org_id"),
        ("P.WAREHOUSE_ID",   "s_wh_id"),
        ("P.ITEM_ID",        "s_item_id"),
        ("P.VAT_TRAN_NO",    "s_inv_no"),
        ("P.PO_TRAN_NO",     "s_po_no"),
        ("P.EXPENSE_ID",     "s_exp_id"),
        ("P.JOB_ID",         "s_job_id"),
        ("P.ACCOUNT_ID_COST", "s_acc_cost"),
        ("P.PR_DETAIL_ID",   "s_pr_id"),
        ("P.UNIT_ID",        "s_unit_id"),
        ("P.UNIT_ID_WH",     "s_unit_id_wh"),
    ]:
        val = request_args.get(arg, "").strip()
        if val:
            clauses.append(f"{field} LIKE ?")
            params.append(f"{val}%")

    # text contains LIKE (cột đến từ JOIN dimension)
    for field, arg in [
        ("P.DESCRIPTION",      "s_desc"),
        ("O.ORGANIZATION_NAME", "s_org_name"),
        ("P.WAREHOUSE_NAME",   "s_wh_name"),
        ("E.EXPENSE_NAME",     "s_exp_name"),
        ("P.JOB_NAME",         "s_job_name"),
        ("P.PR_DETAIL_NAME",   "s_pr_name"),
    ]:
        val = request_args.get(arg, "").strip()
        if val:
            clauses.append(f"{field} LIKE ?")
            params.append(f"%{val}%")

    # Search ngày VAT_TRAN_DATE — chỉ hỗ trợ dd/mm/yyyy
    vd = request_args.get("s_vat_date", "").strip()
    if vd:
        try:
            parts = [p for p in vd.split('/') if p]
            if len(parts) == 3:
                d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
                if y < 100: y += 2000
                clauses.append("P.VAT_TRAN_DATE = ?")
                params.append(f"{y:04d}{m:02d}{d:02d}")
            else:
                clauses.append("CONVERT(VARCHAR(10), P.VAT_TRAN_DATE, 103) LIKE ?")
                params.append(f"%{vd}%")
        except Exception:
            clauses.append("CONVERT(VARCHAR(10), P.VAT_TRAN_DATE, 103) LIKE ?")
            params.append(f"%{vd}%")

    return " AND ".join(clauses), params


@app.route("/api/debug_purchase")
def debug_purchase():
    """Liệt kê cột thực tế của dbo.PURCHASE_VIEW + sample 3 dòng."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'PURCHASE_VIEW'
            ORDER BY ORDINAL_POSITION
        """)
        cols = [{"name": r[0], "type": r[1]} for r in cursor.fetchall()]
        cursor.execute("SELECT COUNT(*) FROM dbo.PURCHASE_VIEW WITH (NOLOCK)")
        total = cursor.fetchone()[0]
        sample = []
        try:
            cursor.execute("SELECT TOP 3 * FROM dbo.PURCHASE_VIEW WITH (NOLOCK)")
            sample_cols = [c[0] for c in cursor.description]
            for r in cursor.fetchall():
                sample.append({c: (v.strftime("%d/%m/%Y") if hasattr(v,'strftime') else (float(v) if hasattr(v,'real') and not isinstance(v,bool) else (str(v) if v is not None else None))) for c, v in zip(sample_cols, r)})
        except Exception as se:
            sample = [{"err": str(se)}]
        return jsonify({"total_rows": total, "columns": cols, "sample": sample})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/purchase")
@with_db_lock
def get_purchase():
    """Danh sách chứng từ nhập kho lấy từ dbo.PURCHASE_VIEW."""
    try:
        page      = int(request.args.get("page",     1))
        page_size = int(request.args.get("page_size", 100))
        export_all = request.args.get("export_all") == "1"
        known_total = request.args.get("known_total")
        known_sums  = request.args.get("known_sums")  # JSON string
        skip_count  = page > 1 and known_total is not None and known_sums is not None and not export_all

        where_sql, params = _build_purchase_where(request.args)
        order_by_sql = _resolve_order_by(request.args, PURCHASE_SORT_WHITELIST, "P.TRAN_DATE DESC, P.TRAN_NO")
        col_list = ", ".join(f"P.{c}" for c in PURCHASE_BASE_COLUMNS)
        # JOIN bảng dimension để lấy ORGANIZATION_NAME, EXPENSE_NAME
        # (WAREHOUSE_NAME, JOB_NAME đã có sẵn trong PURCHASE_VIEW)
        JOIN_SQL = """
            FROM dbo.PURCHASE_VIEW P WITH (NOLOCK)
            LEFT JOIN dbo.DM_ORGANIZATION O WITH (NOLOCK) ON P.ORGANIZATION_ID = O.ORGANIZATION_ID
            LEFT JOIN dbo.DM_EXPENSE      E WITH (NOLOCK) ON P.EXPENSE_ID      = E.EXPENSE_ID
        """
        SELECT_LIST = f"{col_list}, O.ORGANIZATION_NAME AS ORGANIZATION_NAME, E.EXPENSE_NAME AS EXPENSE_NAME"

        conn   = get_connection()
        cursor = conn.cursor()

        SUM_SQL = """
            SUM(ISNULL(P.QUANTITY,0))        AS S_QUANTITY,
            SUM(ISNULL(P.QUANTITY_WH,0))     AS S_QUANTITY_WH,
            SUM(ISNULL(P.DISCOUNT_AMOUNT,0)) AS S_DISCOUNT,
            SUM(ISNULL(P.VAT_TAX_AMOUNT,0))  AS S_VAT_TAX,
            SUM(ISNULL(P.TOTAL_AMOUNT,0))    AS S_TOTAL
        """

        if export_all:
            sql = f"""
                SELECT {SELECT_LIST}
                {JOIN_SQL}
                WHERE {where_sql}
                ORDER BY {order_by_sql}
            """
            cursor.execute(sql, params)
            columns  = [c[0] for c in cursor.description]
            raw_rows = cursor.fetchall()
            total_rows = len(raw_rows)
            summary = {"quantity": 0, "quantity_wh": 0, "discount": 0, "vat_tax": 0, "total": 0}
            qi = {c: i for i, c in enumerate(columns)}
            for r in raw_rows:
                summary["quantity"]    += float(r[qi.get("QUANTITY")]        or 0) if "QUANTITY"        in qi else 0
                summary["quantity_wh"] += float(r[qi.get("QUANTITY_WH")]     or 0) if "QUANTITY_WH"     in qi else 0
                summary["discount"]    += float(r[qi.get("DISCOUNT_AMOUNT")] or 0) if "DISCOUNT_AMOUNT" in qi else 0
                summary["vat_tax"]     += float(r[qi.get("VAT_TAX_AMOUNT")]  or 0) if "VAT_TAX_AMOUNT"  in qi else 0
                summary["total"]       += float(r[qi.get("TOTAL_AMOUNT")]    or 0) if "TOTAL_AMOUNT"    in qi else 0
        else:
            if skip_count:
                import json as _json
                total_rows = int(known_total)
                try:    summary = _json.loads(known_sums)
                except: summary = {"quantity":0,"quantity_wh":0,"discount":0,"vat_tax":0,"total":0}
            else:
                cursor.execute(f"SELECT COUNT(*), {SUM_SQL} {JOIN_SQL} WHERE {where_sql}", params)
                row = cursor.fetchone()
                total_rows = row[0] or 0
                summary = {
                    "quantity":    float(row[1] or 0),
                    "quantity_wh": float(row[2] or 0),
                    "discount":    float(row[3] or 0),
                    "vat_tax":     float(row[4] or 0),
                    "total":       float(row[5] or 0),
                }

            offset = (page - 1) * page_size
            sql = f"""
                SELECT * FROM (
                    SELECT {SELECT_LIST},
                           ROW_NUMBER() OVER (ORDER BY {order_by_sql}) AS RowNum
                    {JOIN_SQL}
                    WHERE {where_sql}
                ) AS RowConstrainedResult
                WHERE RowNum > ? AND RowNum <= ?
            """
            cursor.execute(sql, params + [offset, offset + page_size])
            columns  = [c[0] for c in cursor.description]
            raw_rows = cursor.fetchall()

        db_name = (_db_cfg() or {}).get('database', 'N/A')
        meta = _meta_cache.get(db_name) or {}
        tran_map = { (it.get('id') or '').strip(): it.get('name') or '' for it in meta.get('tran_ids', []) }

        rows = []
        for raw in raw_rows:
            r = dict(zip(columns, raw))
            if 'TRAN_NAME' not in r:
                r['TRAN_NAME'] = tran_map.get((str(r.get('TRAN_ID') or '')).strip(), '')
            for dk in ("TRAN_DATE", "VAT_TRAN_DATE"):
                v = r.get(dk)
                if isinstance(v, (date, datetime)):
                    r[dk] = v.strftime("%d/%m/%Y")
            for nk in ("QUANTITY","QUANTITY_WH","UNIT_PRICE","DISCOUNT_AMOUNT","PURCHASE_COST","VAT_TAX_RATE","VAT_TAX_AMOUNT","TOTAL_AMOUNT"):
                v = r.get(nk)
                if v is not None:
                    try: r[nk] = float(v)
                    except: pass
            rows.append(r)

        return jsonify({
            "status": "ok",
            "data": rows,
            "pagination": {
                "total_rows":  total_rows,
                "total_pages": max(1, (total_rows + page_size - 1) // page_size),
                "page": page if not export_all else 1
            },
            "summary": summary
        })
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


# =============== WAREHOUSE_VIEW (Phiếu nhập/xuất kho) ===============
WAREHOUSE_BASE_COLUMNS = [
    "ISSUE_RECEIVE",
    "ORGANIZATION_ID",
    "TRAN_ID", "TRAN_NO", "TRAN_DATE",
    "WAREHOUSE_ID", "WAREHOUSE_NAME",
    "WAREHOUSE_ID_ISSUE",
    "ITEM_ID", "ITEM_NAME",
    "UNIT_ID_WH", "QUANTITY",
    "UNIT_ID_EXTRA", "QUANTITY_EXTRA",
    "UNIT_PRICE", "AMOUNT",
    "ACCOUNT_ID", "ACCOUNT_ID_CONTRA",
    "PR_DETAIL_ID", "PR_DETAIL_NAME",
    "EXPENSE_ID", "EXPENSE_NAME",
    "JOB_ID", "JOB_NAME",
]

def _build_warehouse_where(request_args):
    f_date = request_args.get("from_date", "01/01/2026")
    t_date = request_args.get("to_date",  "31/12/2026")
    from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
    to_dt   = datetime.strptime(t_date, "%d/%m/%Y").date()

    clauses = ["W.TRAN_DATE >= ?", "W.TRAN_DATE <= ?"]
    params  = [from_dt.strftime("%Y%m%d"), to_dt.strftime("%Y%m%d")]

    for field, arg in [
        ("W.TRAN_ID",        "tran_ids"),
        ("W.ORGANIZATION_ID", "org_ids"),
        ("W.JOB_ID",         "job_ids"),
        ("W.ITEM_ID",        "item_ids"),
        ("W.EXPENSE_ID",     "expense_ids"),
        ("W.PR_DETAIL_ID",   "pr_detail_ids"),
        ("W.WAREHOUSE_ID",   "wh_ids"),
        ("W.PRODUCT_ID",     "product_ids"),
    ]:
        raw = request_args.get(arg, "")
        vals = [v for v in raw.split(",") if v]
        if arg == "org_ids":
            # Lọc đơn vị LUÔN đi qua _org_filter_sql — nơi DUY NHẤT ép quyền đơn vị theo tài
            # khoản (chọn gì cũng bị giao với danh sách được phép). Không chọn ⇒ mặc định loại
            # đơn vị ngoài cây '00', hoặc = đúng đơn vị được phép nếu tài khoản bị giới hạn.
            _oc, _op = _org_filter_sql(vals, field)
            if _oc:
                clauses.append(_oc)
                params.extend(_op)
        elif vals:
            clauses.append(f"{field} IN ({','.join(['?']*len(vals))})")
            params.extend(vals)

    ir = request_args.get("issue_receive", "").strip()
    if ir in ("N", "X"):
        clauses.append("W.ISSUE_RECEIVE = ?")
        params.append(ir)

    for field, arg in [
        ("W.TRAN_NO",           "tran_no"),
        ("W.TRAN_ID",           "s_tran_id"),
        ("W.ORGANIZATION_ID",   "s_org_id"),
        ("W.WAREHOUSE_ID",      "s_wh_id"),
        ("W.WAREHOUSE_ID_ISSUE", "s_wh_id_issue"),
        ("W.ITEM_ID",           "s_item_id"),
        ("W.PR_DETAIL_ID",      "s_pr_id"),
        ("W.EXPENSE_ID",        "s_exp_id"),
        ("W.JOB_ID",            "s_job_id"),
        ("W.ACCOUNT_ID",        "s_acc_id"),
        ("W.ACCOUNT_ID_CONTRA", "s_acc_contra"),
        ("W.UNIT_ID_WH",        "s_unit_id_wh"),
        ("W.UNIT_ID_EXTRA",     "s_unit_id_extra"),
    ]:
        val = request_args.get(arg, "").strip()
        if val:
            clauses.append(f"{field} LIKE ?")
            params.append(f"{val}%")

    for field, arg in [
        ("W.DESCRIPTION",      "s_desc"),
        ("O.ORGANIZATION_NAME", "s_org_name"),
        ("W.WAREHOUSE_NAME",   "s_wh_name"),
        ("WI.WAREHOUSE_NAME",  "s_wh_name_issue"),
        ("W.ITEM_NAME",        "s_item_name"),
        ("W.EXPENSE_NAME",     "s_exp_name"),
        ("W.JOB_NAME",         "s_job_name"),
        ("W.PR_DETAIL_NAME",   "s_pr_name"),
    ]:
        val = request_args.get(arg, "").strip()
        if val:
            clauses.append(f"{field} LIKE ?")
            params.append(f"%{val}%")

    return " AND ".join(clauses), params


@app.route("/api/warehouse")
@with_db_lock
def get_warehouse():
    try:
        page      = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 100))
        export_all = request.args.get("export_all") == "1"
        known_total = request.args.get("known_total")
        known_sums  = request.args.get("known_sums")
        skip_count  = page > 1 and known_total is not None and known_sums is not None and not export_all

        where_sql, params = _build_warehouse_where(request.args)
        order_by_sql = _resolve_order_by(request.args, WAREHOUSE_SORT_WHITELIST, "W.TRAN_DATE DESC, W.TRAN_NO")

        select_parts = [f"W.{c}" for c in WAREHOUSE_BASE_COLUMNS]
        select_parts.append("O.ORGANIZATION_NAME AS ORGANIZATION_NAME")
        select_parts.append("WI.WAREHOUSE_NAME AS WAREHOUSE_NAME_ISSUE")
        SELECT_LIST = ", ".join(select_parts)

        JOIN_SQL = """
            FROM dbo.WAREHOUSE_VIEW W WITH (NOLOCK)
            LEFT JOIN dbo.DM_ORGANIZATION O  WITH (NOLOCK) ON W.ORGANIZATION_ID    = O.ORGANIZATION_ID
            LEFT JOIN dbo.DM_WAREHOUSE    WI WITH (NOLOCK) ON W.WAREHOUSE_ID_ISSUE = WI.WAREHOUSE_ID
        """

        SUM_SQL = """
            SUM(ISNULL(W.QUANTITY,0))       AS S_QUANTITY,
            SUM(ISNULL(W.QUANTITY_EXTRA,0)) AS S_QUANTITY_EXTRA,
            SUM(ISNULL(W.AMOUNT,0))         AS S_AMOUNT
        """

        conn = get_connection()
        cursor = conn.cursor()

        if export_all:
            sql = f"SELECT {SELECT_LIST} {JOIN_SQL} WHERE {where_sql} ORDER BY {order_by_sql}"
            cursor.execute(sql, params)
            columns  = [c[0] for c in cursor.description]
            raw_rows = cursor.fetchall()
            total_rows = len(raw_rows)
            summary = {"quantity": 0, "quantity_extra": 0, "amount": 0}
            qi = {c: i for i, c in enumerate(columns)}
            for r in raw_rows:
                summary["quantity"]       += float(r[qi.get("QUANTITY")]       or 0) if "QUANTITY"       in qi else 0
                summary["quantity_extra"] += float(r[qi.get("QUANTITY_EXTRA")] or 0) if "QUANTITY_EXTRA" in qi else 0
                summary["amount"]         += float(r[qi.get("AMOUNT")]         or 0) if "AMOUNT"         in qi else 0
        else:
            if skip_count:
                import json as _json
                total_rows = int(known_total)
                try:    summary = _json.loads(known_sums)
                except: summary = {"quantity":0,"quantity_extra":0,"amount":0}
            else:
                cursor.execute(f"SELECT COUNT(*), {SUM_SQL} {JOIN_SQL} WHERE {where_sql}", params)
                row = cursor.fetchone()
                total_rows = row[0] or 0
                summary = {
                    "quantity":       float(row[1] or 0),
                    "quantity_extra": float(row[2] or 0),
                    "amount":         float(row[3] or 0),
                }

            offset = (page - 1) * page_size
            sql = f"""
                SELECT * FROM (
                    SELECT {SELECT_LIST},
                           ROW_NUMBER() OVER (ORDER BY {order_by_sql}) AS RowNum
                    {JOIN_SQL}
                    WHERE {where_sql}
                ) AS RowConstrainedResult
                WHERE RowNum > ? AND RowNum <= ?
            """
            cursor.execute(sql, params + [offset, offset + page_size])
            columns  = [c[0] for c in cursor.description]
            raw_rows = cursor.fetchall()

        db_name = (_db_cfg() or {}).get('database', 'N/A')
        meta = _meta_cache.get(db_name) or {}
        tran_map = { (it.get('id') or '').strip(): it.get('name') or '' for it in meta.get('tran_ids', []) }

        rows = []
        for raw in raw_rows:
            r = dict(zip(columns, raw))
            if 'TRAN_NAME' not in r:
                r['TRAN_NAME'] = tran_map.get((str(r.get('TRAN_ID') or '')).strip(), '')
            v = r.get("TRAN_DATE")
            if isinstance(v, (date, datetime)):
                r["TRAN_DATE"] = v.strftime("%d/%m/%Y")
            for nk in ("QUANTITY","QUANTITY_EXTRA","UNIT_PRICE","AMOUNT"):
                v = r.get(nk)
                if v is not None:
                    try: r[nk] = float(v)
                    except: pass
            rows.append(r)

        return jsonify({
            "status": "ok",
            "data": rows,
            "pagination": {
                "total_rows": total_rows,
                "total_pages": max(1, (total_rows + page_size - 1) // page_size),
                "page": page if not export_all else 1
            },
            "summary": summary
        })
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


# ============== EXPORT CSV TO DISK (cho dataset lớn) ==============
import uuid

# Folder lưu file export — Downloads\iPOS_Ledger_Studio
def _export_dir():
    home = os.path.expanduser("~")
    # Windows: Downloads. Khác OS: home directory.
    if platform.system() == "Windows":
        base = os.path.join(home, "Downloads", "iPOS_Ledger_Studio")
    else:
        base = os.path.join(home, "iPOS_Ledger_Studio")
    try:
        os.makedirs(base, exist_ok=True)
    except Exception:
        base = home
    return base


# In-memory map theo dõi tiến trình job export
# { job_id: { status, current, total, file_path, filename, error } }
_export_jobs = {}
_export_jobs_lock = threading.Lock()


def _csv_escape(v):
    """Escape 1 cell cho CSV chuẩn RFC 4180."""
    if v is None:
        return ""
    if isinstance(v, (datetime, date)):
        return v.strftime("%d/%m/%Y")
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if any(c in s for c in (',', '"', '\n', '\r')):
        return '"' + s.replace('"', '""') + '"'
    return s


def _csv_text_cell(v):
    """Ép Excel giữ NGUYÊN chuỗi mã (không mất số 0 đầu, vd '03' → không thành 3).
    Trả về công thức Excel ="..."; ô rỗng giữ rỗng. Kết quả vẫn phải đi qua _csv_escape."""
    s = "" if v is None else str(v).strip()
    return f'="{s}"' if s else ""


def _write_csv_to_disk(job_id, headers, row_iter, filename, total_estimate):
    """Ghi CSV vào disk theo job_id, update progress vào _export_jobs."""
    out_path = os.path.join(_export_dir(), filename)
    try:
        with open(out_path, 'w', encoding='utf-8-sig', newline='') as f:
            f.write(','.join(_csv_escape(h) for h in headers) + '\r\n')
            BATCH = 2000
            count = 0
            buf = []
            for row in row_iter:
                buf.append(','.join(_csv_escape(v) for v in row))
                if len(buf) >= BATCH:
                    f.write('\r\n'.join(buf) + '\r\n')
                    count += len(buf)
                    buf.clear()
                    with _export_jobs_lock:
                        job = _export_jobs.get(job_id)
                        if job is not None:
                            job['current'] = count
                            if job.get('cancelled'):
                                raise RuntimeError("Cancelled by user")
            if buf:
                f.write('\r\n'.join(buf) + '\r\n')
                count += len(buf)

        with _export_jobs_lock:
            job = _export_jobs.get(job_id)
            if job is not None:
                job['status']    = 'done'
                job['current']   = count
                job['total']     = count
                job['file_path'] = out_path
                job['filename']  = filename
    except Exception as e:
        # Xoá file dở dang
        try: os.remove(out_path)
        except: pass
        with _export_jobs_lock:
            job = _export_jobs.get(job_id)
            if job is not None:
                job['status'] = 'error'
                job['error']  = str(e)


def _write_xlsx_to_disk(job_id, headers, row_iter, filename, total_estimate, sheet_limit=1000000):
    """Ghi dữ liệu lớn ra XLSX, tự sang sheet mới khi chạm `sheet_limit` dòng.

    Trần cứng của Excel là 1.048.576 dòng/sheet (kể cả dòng tiêu đề) nên sheet_limit
    KHÔNG được vượt 1.048.575 — có kẹp cứng bên dưới, truyền sai cỡ nào cũng không
    sinh ra được file Excel mở không nổi. Mặc định 1 triệu dòng/sheet cho mọi nơi:
    bám sát trần Excel nên số sheet ít nhất có thể (mốc 500k cũ cắt dày gấp đôi mức
    cần thiết, file nhiều sheet hơn mà chẳng được lợi gì)."""
    import xlsxwriter
    out_path = os.path.join(_export_dir(), filename)
    try:
        workbook = xlsxwriter.Workbook(out_path, {'constant_memory': True})
        header_format = workbook.add_format({'bg_color': '#f8fafc', 'align': 'center'})
        num_format = workbook.add_format({'num_format': '#,##0'})
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
        text_format = workbook.add_format({'num_format': '@'})
        cell_format = workbook.add_format({})
        text_format = workbook.add_format({'num_format': '@'})

        sheet_limit = min(int(sheet_limit or 1000000), 1048575)   # không bao giờ vượt trần Excel
        sheet_idx = 1
        worksheet = workbook.add_worksheet(f"Sheet {sheet_idx}")
        
        for col_num, header in enumerate(headers):
            worksheet.write_string(0, col_num, str(header), header_format)

        row_num = 1
        count = 0
        for row in row_iter:
            if row_num > sheet_limit:
                sheet_idx += 1
                worksheet = workbook.add_worksheet(f"Sheet {sheet_idx}")
                for col_num, header in enumerate(headers):
                    worksheet.write_string(0, col_num, str(header), header_format)
                row_num = 1

            for col_num, val in enumerate(row):
                if val is None or val == '':
                    worksheet.write_blank(row_num, col_num, "", text_format)
                elif isinstance(val, (datetime, date)):
                    worksheet.write_datetime(row_num, col_num, val, date_format)
                elif isinstance(val, (int, float)):
                    worksheet.write_number(row_num, col_num, val, num_format)
                else:
                    worksheet.write_string(row_num, col_num, str(val), text_format)
                    
            row_num += 1
            count += 1
            if count % 2000 == 0:
                with _export_jobs_lock:
                    job = _export_jobs.get(job_id)
                    if job is not None:
                        job['current'] = count
                        if job.get('cancelled'):
                            workbook.close()
                            raise RuntimeError("Cancelled by user")

        workbook.close()
        with _export_jobs_lock:
            job = _export_jobs.get(job_id)
            if job is not None:
                job['status'] = 'done'
                job['current'] = count
                job['total'] = count
                job['file_path'] = out_path
                job['filename'] = filename
    except Exception as e:
        try: os.remove(out_path)
        except: pass
        with _export_jobs_lock:
            job = _export_jobs.get(job_id)
            if job is not None:
                job['status'] = 'error'
                job['error']  = str(e)


@app.route("/api/export/status")
def get_export_status():
    """Frontend poll để hiển thị progress."""
    job_id = request.args.get("job_id", "")
    with _export_jobs_lock:
        job = _export_jobs.get(job_id)
        if not job:
            return jsonify({"status": "not_found"}), 404
        return jsonify({k: v for k, v in job.items() if k != 'cancelled'})


@app.route("/api/export/cancel", methods=["POST"])
def cancel_export():
    job_id = request.json.get("job_id") if request.is_json else request.args.get("job_id", "")
    with _export_jobs_lock:
        job = _export_jobs.get(job_id)
        if job and job.get('status') == 'running':
            job['cancelled'] = True
    return jsonify({"status": "ok"})


@app.route("/api/save_export", methods=["POST"])
def save_export_route():
    """Lưu file xuất (XLS/CSV) vào _export_dir và trả về đường dẫn để mở file/folder."""
    try:
        data = request.get_json(force=True, silent=True) or {}
        filename = data.get("filename", "export.xls")
        content = data.get("content", "")
        filename = os.path.basename(filename)
        out_path = os.path.join(_export_dir(), filename)
        
        with open(out_path, "w", encoding="utf-8-sig", errors="ignore", newline="") as f:
            f.write(content)
            
        return jsonify({
            "status": "ok",
            "path": out_path,
            "filename": filename
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/open_file", methods=["POST"])
def open_file_route():
    """Mở file (CSV/Excel) bằng app mặc định của OS."""
    try:
        data = request.get_json(force=True, silent=True) or {}
        path = data.get("path", "")
        # Validate: chỉ cho mở file trong _export_dir để tránh bị abuse
        norm = os.path.realpath(path)
        if not norm.startswith(os.path.realpath(_export_dir())):
            return jsonify({"status": "error", "message": "Đường dẫn không hợp lệ"}), 400
        if not os.path.exists(norm):
            return jsonify({"status": "error", "message": "File không tồn tại"}), 404
        if platform.system() == "Windows":
            os.startfile(norm)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", norm])
        else:
            subprocess.Popen(["xdg-open", norm])
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/open_folder", methods=["POST"])
def open_folder_route():
    """Mở Explorer/Finder vào folder chứa file (highlight file)."""
    try:
        data = request.get_json(force=True, silent=True) or {}
        path = data.get("path", "")
        norm = os.path.realpath(path)
        exp_root = os.path.realpath(_export_dir())
        if not norm.startswith(exp_root):
            return jsonify({"status": "error", "message": "Đường dẫn không hợp lệ"}), 400
        if platform.system() == "Windows":
            win_path = os.path.normpath(norm)
            if os.path.exists(win_path):
                subprocess.Popen(f'explorer.exe /select,"{win_path}"')
            else:
                subprocess.Popen(f'explorer.exe "{os.path.normpath(exp_root)}"')
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-R", norm if os.path.exists(norm) else exp_root])
        else:
            target = os.path.dirname(norm) if os.path.exists(norm) else exp_root
            subprocess.Popen(["xdg-open", target])
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def _start_export_job(filename, headers, sql, params, transform_row, total_estimate=0, sheet_limit=1000000):
    """Mở connection mới (cùng db_config session) → chạy query → ghi disk ở thread riêng.

    transform_row(raw_row, sql_cols) → list giá trị theo thứ tự headers.
    Trả về job_id ngay.
    """
    job_id = uuid.uuid4().hex
    with _export_jobs_lock:
        _export_jobs[job_id] = {
            'status': 'running', 'current': 0, 'total': total_estimate,
            'file_path': None, 'filename': filename, 'error': None,
            'cancelled': False,
        }
    db_cfg = _db_cfg()

    def _runner():
        own_conn = None
        try:
            if not db_cfg:
                raise Exception("Chưa đăng nhập SQL Server")
            # Connection riêng cho thread — không dùng pool chung
            own_conn = _make_conn(db_cfg)
            cursor = own_conn.cursor()
            cursor.execute(sql, params)
            sql_cols = [c[0] for c in cursor.description]

            def row_iter():
                while True:
                    batch = cursor.fetchmany(1000)
                    if not batch: break
                    for raw in batch:
                        yield transform_row(raw, sql_cols)

            if filename.lower().endswith('.xlsx'):
                _write_xlsx_to_disk(job_id, headers, row_iter(), filename, total_estimate, sheet_limit)
            else:
                _write_csv_to_disk(job_id, headers, row_iter(), filename, total_estimate)
        except Exception as e:
            with _export_jobs_lock:
                job = _export_jobs.get(job_id)
                if job is not None:
                    job['status'] = 'error'
                    job['error']  = str(e)
        finally:
            if own_conn:
                try: own_conn.close()
                except: pass

    threading.Thread(target=_runner, daemon=True).start()
    return job_id


# --- LEDGER count + stream csv ---
LEDGER_CSV_COLS = [
    ("TRAN_DATE","Ngày CT"), ("TRAN_NO","Số chứng từ"), ("TRAN_ID","Mã CT"), ("TRAN_NAME","Tên chứng từ"),
    ("ACCOUNT_ID","Tài khoản"), ("ACCOUNT_ID_CONTRA","Đối ứng"),
    ("DESCRIPTION","Diễn giải"),
    ("DEBIT","Nợ"), ("CREDIT","Có"),
    ("PR_DETAIL_ID","Mã ĐT"), ("PR_DETAIL_NAME","Đối tượng"),
    ("PR_DETAIL_ID_CONTRA","Mã ĐT ĐƯ"), ("PR_DETAIL_NAME_CONTRA","Đối tượng ĐƯ"),
    ("EXPENSE_ID","Mã MCP"), ("EXPENSE_NAME","Mục chi phí"),
    ("EXPENSE_ID_CONTRA","Mã MCP ĐƯ"), ("EXPENSE_NAME_CONTRA","Mục chi phí ĐƯ"),
    ("ORGANIZATION_ID","Mã ĐV"), ("ORGANIZATION_NAME","Tên đơn vị"),
    ("ITEM_ID","Mã HH"), ("ITEM_NAME","Hàng hóa"),
    ("ITEM_ID_CONTRA","Mã HH ĐƯ"), ("ITEM_NAME_CONTRA","Hàng hóa ĐƯ"),
    ("JOB_ID","Mã CV"), ("JOB_NAME","Công việc"),
    ("JOB_ID_CONTRA","Mã CV ĐƯ"), ("JOB_NAME_CONTRA","Công việc ĐƯ"),
    ("PRODUCT_ID","Mã SP"), ("PRODUCT_NAME","Sản phẩm"),
    ("BANK_ID","Mã NH"), ("BANK_NAME","Ngân hàng"),
    ("BANK_ID_CONTRA","Mã NH ĐƯ"), ("BANK_NAME_CONTRA","NH đối ứng"),
]


@app.route("/api/ledger/count")
@with_db_lock
def get_ledger_count():
    """Chỉ trả số dòng (cho frontend quyết định xuất xlsx hay stream CSV)."""
    try:
        where_sql, params, join_clauses, join_params = _build_where(request.args)
        conn = get_connection()
        cursor = conn.cursor()
        if join_clauses:
            needed = set()
            for c in join_clauses:
                if 'PD.' in c: needed.add('pd')
                if 'E.'  in c: needed.add('e')
                if 'O.'  in c: needed.add('o')
                if 'I.'  in c: needed.add('i')
                if 'P.'  in c: needed.add('p')
                if 'B.'  in c: needed.add('b')
            joins = ["FROM dbo.LEDGER L WITH (NOLOCK)"]
            if 'pd' in needed: joins.append("LEFT JOIN dbo.DM_PR_DETAIL   PD WITH (NOLOCK) ON L.PR_DETAIL_ID    = PD.PR_DETAIL_ID")
            if 'i'  in needed: joins.append("LEFT JOIN dbo.DM_ITEM         I  WITH (NOLOCK) ON L.ITEM_ID         = I.ITEM_ID")
            if 'p'  in needed: joins.append("LEFT JOIN dbo.DM_ITEM         P  WITH (NOLOCK) ON L.PRODUCT_ID      = P.ITEM_ID")
            if 'e'  in needed: joins.append("LEFT JOIN dbo.DM_EXPENSE      E  WITH (NOLOCK) ON L.EXPENSE_ID      = E.EXPENSE_ID")
            if 'o'  in needed: joins.append("LEFT JOIN dbo.DM_ORGANIZATION O  WITH (NOLOCK) ON L.ORGANIZATION_ID = O.ORGANIZATION_ID")
            if 'b'  in needed: joins.append("LEFT JOIN dbo.DM_BANK         B  WITH (NOLOCK) ON L.BANK_ID         = B.BANK_ID")
            jt = " ".join(joins)
            join_filter = " AND ".join(join_clauses)
            cursor.execute(f"SELECT COUNT(*) {jt} WHERE {where_sql} AND {join_filter}", params + join_params)
        else:
            cursor.execute(f"SELECT COUNT(*) FROM dbo.LEDGER L WITH (NOLOCK) WHERE {where_sql}", params)
        total = cursor.fetchone()[0] or 0
        return jsonify({"status": "ok", "total": int(total)})
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


@app.route("/api/ledger/stream_csv", methods=["POST", "GET"])
def get_ledger_stream_csv():
    """Tạo job ghi CSV vào disk + trả job_id để poll progress."""
    try:
        args = request.args
        total_estimate = int(args.get("total", 0) or 0)
        where_sql, params, join_clauses, join_params = _build_where(args)
        order_by_sql = _resolve_order_by(args, LEDGER_SORT_WHITELIST, "L.TRAN_DATE DESC, L.TRAN_NO")

        BASE_COLS = """
            L.TRAN_DATE, L.TRAN_NO, L.TRAN_ID, T.TRAN_NAME,
            L.ACCOUNT_ID, L.ACCOUNT_ID_CONTRA,
            L.DESCRIPTION, L.COMMENTS, L.DEBIT_CREDIT, L.AMOUNT,
            L.PR_DETAIL_ID, PD.PR_DETAIL_NAME,
            L.PR_DETAIL_ID_CONTRA, PD2.PR_DETAIL_NAME AS PR_DETAIL_NAME_CONTRA,
            L.EXPENSE_ID, E.EXPENSE_NAME,
            L.EXPENSE_ID_CONTRA, E2.EXPENSE_NAME AS EXPENSE_NAME_CONTRA,
            L.ORGANIZATION_ID, O.ORGANIZATION_NAME,
            L.ITEM_ID, I.ITEM_NAME,
            L.ITEM_ID_CONTRA, I2.ITEM_NAME AS ITEM_NAME_CONTRA,
            L.JOB_ID, J.JOB_NAME,
            L.JOB_ID_CONTRA, J2.JOB_NAME AS JOB_NAME_CONTRA,
            L.PRODUCT_ID, P.ITEM_NAME AS PRODUCT_NAME,
            L.BANK_ID, B.BANK_NAME,
            L.BANK_ID_CONTRA, B2.BANK_NAME AS BANK_NAME_CONTRA
        """
        joins = [
            "FROM dbo.LEDGER L WITH (NOLOCK)",
            "LEFT JOIN dbo.SYS_TRAN       T   WITH (NOLOCK) ON L.TRAN_ID             = T.TRAN_ID",
            "LEFT JOIN dbo.DM_PR_DETAIL   PD  WITH (NOLOCK) ON L.PR_DETAIL_ID       = PD.PR_DETAIL_ID",
            "LEFT JOIN dbo.DM_PR_DETAIL   PD2 WITH (NOLOCK) ON L.PR_DETAIL_ID_CONTRA= PD2.PR_DETAIL_ID",
            "LEFT JOIN dbo.DM_EXPENSE     E   WITH (NOLOCK) ON L.EXPENSE_ID         = E.EXPENSE_ID",
            "LEFT JOIN dbo.DM_EXPENSE     E2  WITH (NOLOCK) ON L.EXPENSE_ID_CONTRA  = E2.EXPENSE_ID",
            "LEFT JOIN dbo.DM_ORGANIZATION O  WITH (NOLOCK) ON L.ORGANIZATION_ID    = O.ORGANIZATION_ID",
            "LEFT JOIN dbo.DM_ITEM        I   WITH (NOLOCK) ON L.ITEM_ID            = I.ITEM_ID",
            "LEFT JOIN dbo.DM_ITEM        I2  WITH (NOLOCK) ON L.ITEM_ID_CONTRA     = I2.ITEM_ID",
            "LEFT JOIN dbo.DM_JOB         J   WITH (NOLOCK) ON L.JOB_ID             = J.JOB_ID",
            "LEFT JOIN dbo.DM_JOB         J2  WITH (NOLOCK) ON L.JOB_ID_CONTRA      = J2.JOB_ID",
            "LEFT JOIN dbo.DM_ITEM        P   WITH (NOLOCK) ON L.PRODUCT_ID         = P.ITEM_ID",
            "LEFT JOIN dbo.DM_BANK        B   WITH (NOLOCK) ON L.BANK_ID            = B.BANK_ID",
            "LEFT JOIN dbo.DM_BANK        B2  WITH (NOLOCK) ON L.BANK_ID_CONTRA     = B2.BANK_ID",
        ]
        jt = " ".join(joins)
        join_filter = " AND ".join(join_clauses) if join_clauses else "1=1"
        sql = f"SELECT {BASE_COLS} {jt} WHERE {where_sql} AND {join_filter} ORDER BY {order_by_sql}"

        def transform(raw, _cols):
            (tran_date, tran_no, tran_id, tran_name,
             acc, acc_contra, desc, comments, dc, amount,
             pr_id, pr_name, pr_id_contra, pr_name_contra,
             exp_id, exp_name, exp_id_contra, exp_name_contra,
             org_id, org_name,
             item_id, item_name, item_id_contra, item_name_contra,
             job_id, job_name, job_id_contra, job_name_contra,
             prod_id, prod_name,
             bank_id, bank_name, bank_id_contra, bank_name_contra) = raw
            debit  = float(amount) if dc == 'DEB' and amount is not None else ''
            credit = float(amount) if dc == 'CRD' and amount is not None else ''
            return [
                tran_date, tran_no, tran_id, tran_name or '',
                acc, acc_contra,
                desc or comments or '',
                debit, credit,
                pr_id or '', pr_name or '',
                pr_id_contra or '', pr_name_contra or '',
                exp_id or '', exp_name or '',
                exp_id_contra or '', exp_name_contra or '',
                org_id or '', org_name or '',
                item_id or '', item_name or '',
                item_id_contra or '', item_name_contra or '',
                job_id or '', job_name or '',
                job_id_contra or '', job_name_contra or '',
                prod_id or '', prod_name or '',
                bank_id or '', bank_name or '',
                bank_id_contra or '', bank_name_contra or '',
            ]

        headers = [label for _, label in LEDGER_CSV_COLS]
        fname   = f"ChungTuTongHop_{args.get('from_date','').replace('/','')}-{args.get('to_date','').replace('/','')}.{args.get('format', 'csv')}"
        job_id  = _start_export_job(fname, headers, sql, params + join_params, transform, total_estimate)
        return jsonify({"status": "ok", "job_id": job_id, "filename": fname})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# --- PURCHASE count + stream csv ---
PURCHASE_CSV_COLS = [
    ("ORGANIZATION_ID","Mã đơn vị"), ("ORGANIZATION_NAME","Tên đơn vị"),
    ("TRAN_ID","Mã chứng từ"), ("TRAN_NO","Số chứng từ"), ("TRAN_DATE","Ngày chứng từ"),
    ("VAT_TRAN_NO","Số hóa đơn"), ("VAT_TRAN_DATE","Ngày hóa đơn"), ("PO_TRAN_NO","Số PO"),
    ("WAREHOUSE_ID","Mã kho"), ("WAREHOUSE_NAME","Tên kho"),
    ("ITEM_ID","Mã hàng hóa"), ("DESCRIPTION","Diễn giải"),
    ("UNIT_ID","Đơn vị tính"), ("QUANTITY","Số lượng"),
    ("UNIT_ID_WH","ĐVT kho"), ("QUANTITY_WH","SL kho"),
    ("UNIT_PRICE","Đơn giá"), ("DISCOUNT_AMOUNT","Giảm giá"), ("PURCHASE_COST","Chi phí"),
    ("VAT_TAX_RATE","Thuế suất"), ("VAT_TAX_AMOUNT","Tiền thuế VAT"), ("TOTAL_AMOUNT","Tổng tiền"),
    ("ACCOUNT_ID_COST","TK kho"),
    ("PR_DETAIL_ID","Mã đối tượng"), ("PR_DETAIL_NAME","Tên đối tượng"),
    ("EXPENSE_ID","Mã MCP"), ("EXPENSE_NAME","Tên MCP"),
    ("JOB_ID","Mã công việc"), ("JOB_NAME","Tên công việc"),
]


@app.route("/api/purchase/count")
@with_db_lock
def get_purchase_count():
    try:
        where_sql, params = _build_purchase_where(request.args)
        JOIN_SQL = """
            FROM dbo.PURCHASE_VIEW P WITH (NOLOCK)
            LEFT JOIN dbo.DM_ORGANIZATION O WITH (NOLOCK) ON P.ORGANIZATION_ID = O.ORGANIZATION_ID
            LEFT JOIN dbo.DM_EXPENSE      E WITH (NOLOCK) ON P.EXPENSE_ID      = E.EXPENSE_ID
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) {JOIN_SQL} WHERE {where_sql}", params)
        total = cursor.fetchone()[0] or 0
        return jsonify({"status": "ok", "total": int(total)})
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


@app.route("/api/purchase/stream_csv", methods=["POST", "GET"])
def get_purchase_stream_csv():
    try:
        args = request.args
        total_estimate = int(args.get("total", 0) or 0)
        where_sql, params = _build_purchase_where(args)
        order_by_sql = _resolve_order_by(args, PURCHASE_SORT_WHITELIST, "P.TRAN_DATE DESC, P.TRAN_NO")

        col_list = ", ".join(f"P.{c}" for c in PURCHASE_BASE_COLUMNS)
        JOIN_SQL = """
            FROM dbo.PURCHASE_VIEW P WITH (NOLOCK)
            LEFT JOIN dbo.DM_ORGANIZATION O WITH (NOLOCK) ON P.ORGANIZATION_ID = O.ORGANIZATION_ID
            LEFT JOIN dbo.DM_EXPENSE      E WITH (NOLOCK) ON P.EXPENSE_ID      = E.EXPENSE_ID
        """
        SELECT_LIST = f"{col_list}, O.ORGANIZATION_NAME AS ORGANIZATION_NAME, E.EXPENSE_NAME AS EXPENSE_NAME"
        sql = f"SELECT {SELECT_LIST} {JOIN_SQL} WHERE {where_sql} ORDER BY {order_by_sql}"

        def transform(raw, sql_cols):
            d = dict(zip(sql_cols, raw))
            return [d.get(key) for key, _ in PURCHASE_CSV_COLS]

        headers = [label for _, label in PURCHASE_CSV_COLS]
        fname   = f"PhieuNhapKho_{args.get('from_date','').replace('/','')}-{args.get('to_date','').replace('/','')}.{args.get('format', 'csv')}"
        job_id  = _start_export_job(fname, headers, sql, params, transform, total_estimate)
        return jsonify({"status": "ok", "job_id": job_id, "filename": fname})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# --- WAREHOUSE count + stream csv ---
WAREHOUSE_CSV_COLS = [
    ("ISSUE_RECEIVE","N/X"),
    ("ORGANIZATION_ID","Mã đơn vị"), ("ORGANIZATION_NAME","Tên đơn vị"),
    ("TRAN_ID","Mã chứng từ"), ("TRAN_NO","Số chứng từ"), ("TRAN_DATE","Ngày chứng từ"),
    ("WAREHOUSE_ID","Mã kho"), ("WAREHOUSE_NAME","Tên kho"),
    ("WAREHOUSE_ID_ISSUE","Mã kho xuất"), ("WAREHOUSE_NAME_ISSUE","Tên kho xuất"),
    ("ITEM_ID","Mã hàng hóa"), ("ITEM_NAME","Tên hàng hóa"),
    ("UNIT_ID_WH","ĐVT"), ("QUANTITY","Số lượng"),
    ("UNIT_ID_EXTRA","ĐVT quy đổi"), ("QUANTITY_EXTRA","SL quy đổi"),
    ("UNIT_PRICE","Đơn giá"), ("AMOUNT","Thành tiền"),
    ("ACCOUNT_ID","Tài khoản"), ("ACCOUNT_ID_CONTRA","TK đối ứng"),
    ("PR_DETAIL_ID","Mã đối tượng"), ("PR_DETAIL_NAME","Tên đối tượng"),
    ("EXPENSE_ID","Mã MCP"), ("EXPENSE_NAME","Tên MCP"),
    ("JOB_ID","Mã công việc"), ("JOB_NAME","Tên công việc"),
]


@app.route("/api/warehouse/count")
@with_db_lock
def get_warehouse_count():
    try:
        where_sql, params = _build_warehouse_where(request.args)
        JOIN_SQL = """
            FROM dbo.WAREHOUSE_VIEW W WITH (NOLOCK)
            LEFT JOIN dbo.DM_ORGANIZATION O  WITH (NOLOCK) ON W.ORGANIZATION_ID    = O.ORGANIZATION_ID
            LEFT JOIN dbo.DM_WAREHOUSE    WI WITH (NOLOCK) ON W.WAREHOUSE_ID_ISSUE = WI.WAREHOUSE_ID
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) {JOIN_SQL} WHERE {where_sql}", params)
        total = cursor.fetchone()[0] or 0
        return jsonify({"status": "ok", "total": int(total)})
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


@app.route("/api/warehouse/stream_csv", methods=["POST", "GET"])
def get_warehouse_stream_csv():
    try:
        args = request.args
        total_estimate = int(args.get("total", 0) or 0)
        where_sql, params = _build_warehouse_where(args)
        order_by_sql = _resolve_order_by(args, WAREHOUSE_SORT_WHITELIST, "W.TRAN_DATE DESC, W.TRAN_NO")

        select_parts = [f"W.{c}" for c in WAREHOUSE_BASE_COLUMNS]
        select_parts.append("O.ORGANIZATION_NAME AS ORGANIZATION_NAME")
        select_parts.append("WI.WAREHOUSE_NAME AS WAREHOUSE_NAME_ISSUE")
        SELECT_LIST = ", ".join(select_parts)
        JOIN_SQL = """
            FROM dbo.WAREHOUSE_VIEW W WITH (NOLOCK)
            LEFT JOIN dbo.DM_ORGANIZATION O  WITH (NOLOCK) ON W.ORGANIZATION_ID    = O.ORGANIZATION_ID
            LEFT JOIN dbo.DM_WAREHOUSE    WI WITH (NOLOCK) ON W.WAREHOUSE_ID_ISSUE = WI.WAREHOUSE_ID
        """
        sql = f"SELECT {SELECT_LIST} {JOIN_SQL} WHERE {where_sql} ORDER BY {order_by_sql}"

        def transform(raw, sql_cols):
            d = dict(zip(sql_cols, raw))
            return [d.get(key) for key, _ in WAREHOUSE_CSV_COLS]

        headers = [label for _, label in WAREHOUSE_CSV_COLS]
        fname   = f"ChungTuKho_{args.get('from_date','').replace('/','')}-{args.get('to_date','').replace('/','')}.{args.get('format', 'csv')}"
        job_id  = _start_export_job(fname, headers, sql, params, transform, total_estimate)
        return jsonify({"status": "ok", "job_id": job_id, "filename": fname})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# =============== WAREHOUSE_BALANCE_ACTUAL (Danh sách tồn kho thực tế) ===============
# Bảng số dư tồn kho theo (Đơn vị x Kho x Mặt hàng) TẠI TỪNG NGÀY (TRAN_DATE = ngày snapshot,
# KHÔNG phải ngày phát sinh giao dịch — không có TRAN_NO/TRAN_ID vì đây không phải chứng từ).
# AMOUNT/UNIT_PRICE/QUANTITY_EXTRA/JOB_ID/PACKAGE/BARCODE/ACCOUNT_ID_ADJUST luôn rỗng/=0 ở DB
# CHULONG nên KHÔNG đưa vào SELECT. QUANTITY_ADJ/UNIT_ID_ADJ = số lượng/đơn vị đóng gói GỐC
# trước quy đổi ra đơn vị theo dõi tồn kho (VD 68 BICH quy đổi = 34000 G) — hiển thị "SL nguyên"/
# "ĐVT nguyên". Không lọc IS_APPROVED — hiển thị nguyên trạng cả 0 và 1.
WAREHOUSE_BALANCE_BASE_COLUMNS = [
    "TRAN_DATE", "ORGANIZATION_ID", "WAREHOUSE_ID", "ITEM_ID",
    "QUANTITY", "QUANTITY_ADJ", "UNIT_ID_ADJ", "USER_ID", "ACCOUNT_ID", "IS_APPROVED",
]

WAREHOUSE_BALANCE_SORT_WHITELIST = {col: f"WBA.{col}" for col in WAREHOUSE_BALANCE_BASE_COLUMNS}
WAREHOUSE_BALANCE_SORT_WHITELIST["ORGANIZATION_NAME"] = "O.ORGANIZATION_NAME"
WAREHOUSE_BALANCE_SORT_WHITELIST["WAREHOUSE_NAME"]    = "WH.WAREHOUSE_NAME"
WAREHOUSE_BALANCE_SORT_WHITELIST["ITEM_NAME"]         = "I.ITEM_NAME"
WAREHOUSE_BALANCE_SORT_WHITELIST["UNIT_ID"]           = "I.UNIT_ID"

WAREHOUSE_BALANCE_CSV_COLS = [
    ("TRAN_DATE", "Ngày"),
    ("ORGANIZATION_ID", "Mã ĐV"), ("ORGANIZATION_NAME", "Tên đơn vị"),
    ("WAREHOUSE_ID", "Mã kho"), ("WAREHOUSE_NAME", "Tên kho"),
    ("ITEM_ID", "Mã hàng"), ("ITEM_NAME", "Tên hàng"), ("UNIT_ID", "ĐVT"),
    ("QUANTITY", "Số lượng"),
    ("QUANTITY_ADJ", "SL nguyên"), ("UNIT_ID_ADJ", "ĐVT nguyên"),
    ("USER_ID", "Người thực hiện"), ("ACCOUNT_ID", "Tài khoản"),
    ("IS_APPROVED", "Đã duyệt"),
]

_WBA_JOIN_SQL = """
    FROM dbo.WAREHOUSE_BALANCE_ACTUAL WBA WITH (NOLOCK)
    LEFT JOIN dbo.DM_ORGANIZATION O  WITH (NOLOCK) ON WBA.ORGANIZATION_ID = O.ORGANIZATION_ID
    LEFT JOIN dbo.DM_WAREHOUSE    WH WITH (NOLOCK) ON WBA.WAREHOUSE_ID    = WH.WAREHOUSE_ID
    LEFT JOIN dbo.DM_ITEM         I  WITH (NOLOCK) ON WBA.ITEM_ID         = I.ITEM_ID
"""


def _warehouse_balance_select_list():
    parts = [f"WBA.{c}" for c in WAREHOUSE_BALANCE_BASE_COLUMNS]
    parts.append("O.ORGANIZATION_NAME AS ORGANIZATION_NAME")
    parts.append("WH.WAREHOUSE_NAME AS WAREHOUSE_NAME")
    parts.append("I.ITEM_NAME AS ITEM_NAME")
    parts.append("I.UNIT_ID AS UNIT_ID")
    return ", ".join(parts)


def _build_warehouse_balance_where(request_args):
    f_date = request_args.get("from_date", "01/01/2026")
    t_date = request_args.get("to_date",  "31/12/2026")
    from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
    to_dt   = datetime.strptime(t_date, "%d/%m/%Y").date()

    clauses = ["WBA.TRAN_DATE >= ?", "WBA.TRAN_DATE <= ?"]
    params  = [from_dt.strftime("%Y%m%d"), to_dt.strftime("%Y%m%d")]

    for field, arg in [
        ("WBA.ORGANIZATION_ID", "org_ids"),
        ("WBA.WAREHOUSE_ID",    "wh_ids"),
        ("WBA.ITEM_ID",         "item_ids"),
        ("WBA.ACCOUNT_ID",      "acc_ids"),
    ]:
        raw = request_args.get(arg, "")
        vals = [v for v in raw.split(",") if v]
        if arg == "org_ids":
            # Lọc đơn vị LUÔN đi qua _org_filter_sql — nơi DUY NHẤT ép quyền đơn vị theo tài
            # khoản (chọn gì cũng bị giao với danh sách được phép). Không chọn ⇒ mặc định loại
            # đơn vị ngoài cây '00', hoặc = đúng đơn vị được phép nếu tài khoản bị giới hạn.
            _oc, _op = _org_filter_sql(vals, field)
            if _oc:
                clauses.append(_oc)
                params.extend(_op)
        elif vals:
            clauses.append(f"{field} IN ({','.join(['?']*len(vals))})")
            params.extend(vals)

    for field, arg in [
        ("WBA.ORGANIZATION_ID", "s_org_id"),
        ("WBA.WAREHOUSE_ID",    "s_wh_id"),
        ("WBA.ITEM_ID",         "s_item_id"),
        ("WBA.USER_ID",         "s_user_id"),
        ("WBA.ACCOUNT_ID",      "s_acc_id"),
    ]:
        val = request_args.get(arg, "").strip()
        if val:
            clauses.append(f"{field} LIKE ?")
            params.append(f"{val}%")

    for field, arg in [
        ("O.ORGANIZATION_NAME", "s_org_name"),
        ("WH.WAREHOUSE_NAME",   "s_wh_name"),
        ("I.ITEM_NAME",         "s_item_name"),
    ]:
        val = request_args.get(arg, "").strip()
        if val:
            clauses.append(f"{field} LIKE ?")
            params.append(f"%{val}%")

    return " AND ".join(clauses), params


@app.route("/api/warehouse_balance")
@with_db_lock
def get_warehouse_balance():
    try:
        page      = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 100))
        export_all  = request.args.get("export_all") == "1"
        known_total = request.args.get("known_total")
        skip_count  = page > 1 and known_total is not None and not export_all

        where_sql, params = _build_warehouse_balance_where(request.args)
        order_by_sql = _resolve_order_by(
            request.args, WAREHOUSE_BALANCE_SORT_WHITELIST,
            "WBA.TRAN_DATE DESC, WBA.WAREHOUSE_ID, WBA.ITEM_ID"
        )
        SELECT_LIST = _warehouse_balance_select_list()

        conn = get_connection()
        cursor = conn.cursor()

        if export_all:
            sql = f"SELECT {SELECT_LIST} {_WBA_JOIN_SQL} WHERE {where_sql} ORDER BY {order_by_sql}"
            cursor.execute(sql, params)
            columns  = [c[0] for c in cursor.description]
            raw_rows = cursor.fetchall()
            total_rows = len(raw_rows)
        else:
            if skip_count:
                total_rows = int(known_total)
            else:
                cursor.execute(f"SELECT COUNT(*) {_WBA_JOIN_SQL} WHERE {where_sql}", params)
                total_rows = cursor.fetchone()[0] or 0

            offset = (page - 1) * page_size
            sql = f"""
                SELECT * FROM (
                    SELECT {SELECT_LIST},
                           ROW_NUMBER() OVER (ORDER BY {order_by_sql}) AS RowNum
                    {_WBA_JOIN_SQL}
                    WHERE {where_sql}
                ) AS RowConstrainedResult
                WHERE RowNum > ? AND RowNum <= ?
            """
            cursor.execute(sql, params + [offset, offset + page_size])
            columns  = [c[0] for c in cursor.description]
            raw_rows = cursor.fetchall()

        rows = []
        for raw in raw_rows:
            r = dict(zip(columns, raw))
            v = r.get("TRAN_DATE")
            if isinstance(v, (date, datetime)):
                r["TRAN_DATE"] = v.strftime("%d/%m/%Y")
            for nk in ("QUANTITY", "QUANTITY_ADJ"):
                v = r.get(nk)
                if v is not None:
                    try: r[nk] = float(v)
                    except: pass
            rows.append(r)

        return jsonify({
            "status": "ok",
            "data": rows,
            "pagination": {
                "total_rows": total_rows,
                "total_pages": max(1, (total_rows + page_size - 1) // page_size),
                "page": page if not export_all else 1
            }
        })
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


@app.route("/api/warehouse_balance/count")
@with_db_lock
def get_warehouse_balance_count():
    try:
        where_sql, params = _build_warehouse_balance_where(request.args)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) {_WBA_JOIN_SQL} WHERE {where_sql}", params)
        total = cursor.fetchone()[0] or 0
        return jsonify({"status": "ok", "total": int(total)})
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


@app.route("/api/warehouse_balance/stream_csv", methods=["POST", "GET"])
def get_warehouse_balance_stream_csv():
    try:
        args = request.args
        total_estimate = int(args.get("total", 0) or 0)
        where_sql, params = _build_warehouse_balance_where(args)
        order_by_sql = _resolve_order_by(
            args, WAREHOUSE_BALANCE_SORT_WHITELIST,
            "WBA.TRAN_DATE DESC, WBA.WAREHOUSE_ID, WBA.ITEM_ID"
        )
        SELECT_LIST = _warehouse_balance_select_list()
        sql = f"SELECT {SELECT_LIST} {_WBA_JOIN_SQL} WHERE {where_sql} ORDER BY {order_by_sql}"

        def transform(raw, sql_cols):
            d = dict(zip(sql_cols, raw))
            return [d.get(key) for key, _ in WAREHOUSE_BALANCE_CSV_COLS]

        headers = [label for _, label in WAREHOUSE_BALANCE_CSV_COLS]
        fname   = f"TonKhoThucTe_{args.get('from_date','').replace('/','')}-{args.get('to_date','').replace('/','')}.{args.get('format', 'csv')}"
        job_id  = _start_export_job(fname, headers, sql, params, transform, total_estimate)
        return jsonify({"status": "ok", "job_id": job_id, "filename": fname})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# =============== ĐỐI CHIẾU XUẤT KHO SX BTP → NHẬP KHO THÀNH PHẨM ===============
# Danh sách RIÊNG BIỆT. Mỗi dòng = 1 nguyên liệu trên phiếu xuất XKHOSXBTP, kèm phiếu nhập
# NSP tương ứng của đúng bán thành phẩm đó.
#
# LUẬT NGHIỆP VỤ (Chú Long xác nhận): nhập kho thành phẩm BẮT BUỘC bấm ngay trên phiếu xuất
# kho SX BTP. Chỉ khi bấm từ đó, phiếu NSP mới được ghi PURCHASE.SALE_PR_KEY trỏ ngược về
# phiếu xuất. Tạo 2 phiếu độc lập ⇒ KHÔNG có cách nào đối chiếu.
#   ⇒ Nối phiếu CHỈ bằng PURCHASE.SALE_PR_KEY = SALE.PR_KEY.
#   ⇒ CẤM nối theo số phiếu: số phiếu trùng nhau giữa các đơn vị, và cặp (đơn vị + số phiếu)
#      cũng không duy nhất (35 ca trùng trong 2026).
#
# SỐ LƯỢNG — 3 trường khác nhau, đừng lẫn:
#   JOB_QTY        = SL bán thành phẩm SẢN XUẤT (duy nhất theo cặp phiếu × BTP)
#   QUANTITY (X)   = SL NGUYÊN LIỆU xuất dùng, từng dòng
#   QUANTITY (N)   = SL thành phẩm nhập kho, theo ĐVT cơ bản
#   QUANTITY_EXTRA = cùng số đó nhưng theo ĐVT nhập liệu (202 BỊCH = 202.000 G)
# JOB_QTY có thể ghi theo MỘT TRONG HAI đơn vị tuỳ người nhập ⇒ lấy mốc gần hơn để so.
# So thẳng JOB_QTY với QUANTITY sẽ đẻ ra 1.091 ca "sai" hoàn toàn giả (đã đo trên DB thật).
BTP_TT_DU   = "Đã nhập đủ"
BTP_TT_CHUA = "Chưa nhập kho BTP"
BTP_TT_LECH = "Lệch số lượng"
# Chiều ngược: phiếu NHẬP không truy được về phiếu xuất. Hai gốc rễ, cùng một hậu quả —
#   (1) làm tay: tạo phiếu nhập độc lập, không bấm từ phiếu xuất  ⇒ SALE_PR_KEY = 0
#   (2) phiếu xuất bị xoá (hoặc xoá rồi lập lại ⇒ cấp khoá mới)   ⇒ khoá trỏ về chỗ trống
BTP_TT_KHONGGOC = "Không tìm thấy phiếu xuất liên quan"

# ⚠️ HAI TRẠNG THÁI "CHƯA GHI SỔ" — cùng khuôn với tab điều chuyển nội bộ (Bẫy 24).
# Phiếu DRAFT không sinh dòng nào trong WAREHOUSE nên vô hình với nhánh X/N ⇒ phải đọc
# thêm SALE_DETAIL / PURCHASE_DETAIL, nối bằng FR_KEY (KHÔNG phải PR_KEY), SL lấy QUANTITY_WH.
# ⚠️ ĐO 21/09/2026: XKHOSXBTP và NSP **chưa từng có một phiếu DRAFT nào** trong cả lịch sử DB
#    (21.588 và 21.298 phiếu, 100% POSTED, dữ liệu từ 01/01/2026) ⇒ hai nhóm này hiện LUÔN
#    bằng 0. Giữ lại để mai kia iPOS/quy trình đổi thì tab bắt được ngay, không phải sửa gấp.
#    Công thức vẫn được kiểm thật bằng cách chạy lên phiếu ĐÃ ghi sổ: SALE_DETAIL khớp
#    WAREHOUSE 10.094/10.094 (cả SL lẫn JOB_QTY), PURCHASE_DETAIL khớp 4.149/4.149, 0 lệch.
BTP_TT_XUAT_NHAP = "Phiếu xuất chưa ghi sổ"
BTP_TT_NHAP_NHAP = "Phiếu nhập chưa ghi sổ"

BTP_STATUS_MAP = {"du": BTP_TT_DU, "chua": BTP_TT_CHUA,
                  "lech": BTP_TT_LECH, "khonggoc": BTP_TT_KHONGGOC,
                  "xuat_chua_gs": BTP_TT_XUAT_NHAP, "nhap_chua_gs": BTP_TT_NHAP_NHAP}

BTPDC_SORT_WHITELIST = {c: c for c in [
    "DON_VI", "TEN_DON_VI", "NGAY_XUAT", "SO_PHIEU_XUAT", "KHO_XUAT", "TEN_KHO_XUAT",
    "BTP", "TEN_BTP", "SL_SX", "DVT_BTP", "NVL", "TEN_NVL", "DVT_NVL",
    "SL_NVL_XUAT", "TIEN_NVL", "SO_PHIEU_NHAP", "NGAY_NHAP", "KHO_NHAP",
    "SL_NHAP", "CHENH_SL", "TIEN_NHAP", "TRANG_THAI", "GHI_CHU",
]}

BTPDC_CSV_COLS = [
    ("DON_VI", "Mã ĐV"), ("TEN_DON_VI", "Tên đơn vị"),
    ("NGAY_XUAT", "Ngày xuất"), ("SO_PHIEU_XUAT", "Phiếu xuất"),
    ("KHO_XUAT", "Mã kho xuất"), ("TEN_KHO_XUAT", "Tên kho xuất"),
    ("BTP", "Mã BTP"), ("TEN_BTP", "Tên BTP"),
    ("SL_SX", "SL sản xuất"), ("DVT_BTP", "ĐVT BTP"),
    ("NVL", "Mã NVL"), ("TEN_NVL", "Tên nguyên liệu"), ("DVT_NVL", "ĐVT NVL"),
    ("SL_NVL_XUAT", "SL NVL xuất"), ("TIEN_NVL", "Tiền NVL"),
    ("SO_PHIEU_NHAP", "Phiếu nhập"), ("NGAY_NHAP", "Ngày nhập"), ("KHO_NHAP", "Kho nhập"),
    ("SL_NHAP", "SL nhập"), ("CHENH_SL", "Chênh SL"), ("TIEN_NHAP", "Tiền nhập"),
    ("TRANG_THAI", "Trạng thái"), ("GHI_CHU", "Ghi chú"),
]

# CTE dựng sẵn bảng đối chiếu DC. {inner} = điều kiện lọc sớm trên dòng xuất (ngày/đơn vị/kho/NVL)
_BTPDC_CTE = """
WITH X AS (
    SELECT W.PR_KEY, W.TRAN_NO, W.TRAN_DATE, W.ORGANIZATION_ID, W.WAREHOUSE_ID,
           W.ITEM_ID, W.PRODUCT_ID, W.QUANTITY, W.AMOUNT, W.JOB_QTY
    FROM dbo.WAREHOUSE W WITH (NOLOCK)
    WHERE W.TRAN_ID = 'XKHOSXBTP' AND W.ISSUE_RECEIVE = 'X' AND {inner}
),
XB AS (
    -- Phiếu xuất SX BTP chưa ghi sổ (xem khối ghi chú ở BTP_TT_XUAT_NHAP).
    SELECT S.PR_KEY, S.TRAN_NO, S.TRAN_DATE, S.ORGANIZATION_ID, S.WAREHOUSE_ID,
           SD.ITEM_ID, SD.PRODUCT_ID,
           QUANTITY = SUM(SD.QUANTITY_WH), JOB_QTY = SUM(ISNULL(SD.JOB_QTY, 0))
    FROM dbo.SALE S WITH (NOLOCK)
    JOIN dbo.SALE_DETAIL SD WITH (NOLOCK) ON SD.FR_KEY = S.PR_KEY
    WHERE S.TRAN_ID = 'XKHOSXBTP' AND S.STATUS <> 'POSTED'
      AND ISNULL(SD.QUANTITY_WH, 0) <> 0 AND {inner_draft}
    GROUP BY S.PR_KEY, S.TRAN_NO, S.TRAN_DATE, S.ORGANIZATION_ID, S.WAREHOUSE_ID,
             SD.ITEM_ID, SD.PRODUCT_ID
),
P AS (
    SELECT PR_KEY, TRAN_NO, TRAN_DATE, SALE_PR_KEY
    FROM dbo.PURCHASE WITH (NOLOCK)
    WHERE TRAN_ID = 'NSP' AND SALE_PR_KEY IS NOT NULL AND SALE_PR_KEY <> 0
),
N0 AS (
    SELECT P.SALE_PR_KEY, WN.ITEM_ID AS BTP_ID, P.TRAN_NO, P.TRAN_DATE, WN.WAREHOUSE_ID,
           SL = SUM(WN.QUANTITY), SL_NG = SUM(ISNULL(WN.QUANTITY_EXTRA, 0)), TIEN = SUM(WN.AMOUNT)
    FROM P
    JOIN dbo.WAREHOUSE WN WITH (NOLOCK) ON WN.PR_KEY = P.PR_KEY AND WN.ISSUE_RECEIVE = 'N'
    GROUP BY P.SALE_PR_KEY, WN.ITEM_ID, P.TRAN_NO, P.TRAN_DATE, WN.WAREHOUSE_ID
),
N AS (
    SELECT SALE_PR_KEY, BTP_ID,
           SO_PHIEU_NHAP = STRING_AGG(TRAN_NO, ' + '),
           NGAY_NHAP     = MIN(TRAN_DATE),
           KHO_NHAP      = STRING_AGG(WAREHOUSE_ID, ' + '),
           SL_NHAP       = SUM(SL),
           SL_NHAP_NG    = SUM(SL_NG),
           TIEN_NHAP     = SUM(TIEN)
    FROM N0 GROUP BY SALE_PR_KEY, BTP_ID
),
NB AS (
    -- Phiếu nhập kho thành phẩm chưa ghi sổ. Giữ nguyên mẹo "mốc gần hơn" của tab này:
    -- vẫn trả cả SL theo ĐVT cơ bản lẫn ĐVT nhập liệu để DC chọn mốc gần JOB_QTY hơn.
    SELECT P4.SALE_PR_KEY, BTP_ID = PD.ITEM_ID,
           SO_PHIEU_NHAP = MAX(P4.TRAN_NO),
           NGAY_NHAP     = MIN(P4.TRAN_DATE),
           KHO_NHAP      = MAX(PD.WAREHOUSE_ID),
           SL_NHAP       = SUM(PD.QUANTITY_WH),
           SL_NHAP_NG    = SUM(ISNULL(PD.QUANTITY_EXTRA, 0)),
           TIEN_NHAP     = CAST(NULL AS decimal(18, 6))
    FROM dbo.PURCHASE P4 WITH (NOLOCK)
    JOIN dbo.PURCHASE_DETAIL PD WITH (NOLOCK) ON PD.FR_KEY = P4.PR_KEY
    WHERE P4.TRAN_ID = 'NSP' AND P4.STATUS <> 'POSTED'
      AND P4.SALE_PR_KEY IS NOT NULL AND P4.SALE_PR_KEY <> 0
      AND ISNULL(PD.QUANTITY_WH, 0) <> 0
    GROUP BY P4.SALE_PR_KEY, PD.ITEM_ID
),
ORPH_H AS (
    -- Đầu phiếu NHẬP không truy được về phiếu xuất (lọc mức phiếu: ngày nhập + đơn vị)
    SELECT P2.PR_KEY, P2.ORGANIZATION_ID, P2.ORIG_TRAN_NO, P2.TRAN_NO, P2.TRAN_DATE
    FROM dbo.PURCHASE P2 WITH (NOLOCK)
    LEFT JOIN dbo.SALE S2 WITH (NOLOCK) ON S2.PR_KEY = P2.SALE_PR_KEY
    WHERE P2.TRAN_ID = 'NSP'
      AND (P2.SALE_PR_KEY IS NULL OR P2.SALE_PR_KEY = 0 OR S2.PR_KEY IS NULL)
      AND {inner_orph}
),
ORPH_X AS (
    -- Số chứng từ xuất ghi trên phiếu nhập giờ còn dẫn tới phiếu nào không?
    -- JOIN một lượt thay vì OUTER APPLY từng dòng (SALE không có index trên TRAN_NO).
    SELECT H.PR_KEY, PK_MOI = MAX(S3.PR_KEY)
    FROM ORPH_H H
    JOIN dbo.SALE S3 WITH (NOLOCK)
      ON S3.TRAN_NO = H.ORIG_TRAN_NO
     AND S3.ORGANIZATION_ID = H.ORGANIZATION_ID
     AND S3.TRAN_ID = 'XKHOSXBTP'
    GROUP BY H.PR_KEY
),
ORPH_N AS (
    -- Phiếu xuất đó đã có phiếu nhập KHÁC nối vào chưa ⇒ nghi nhập trùng
    SELECT X.PR_KEY, NSP_KHAC = MAX(P3.TRAN_NO)
    FROM ORPH_X X
    JOIN dbo.PURCHASE P3 WITH (NOLOCK)
      ON P3.TRAN_ID = 'NSP' AND P3.SALE_PR_KEY = X.PK_MOI AND P3.PR_KEY <> X.PR_KEY
    GROUP BY X.PR_KEY
),
ORPH AS (
    -- Mỗi dòng = 1 mã BTP đã nhập. Phần xuất để trống vì không có phiếu xuất để lấy.
    SELECT
        PR_KEY_XUAT   = 'N' + CAST(CAST(H.PR_KEY AS bigint) AS varchar(30)),
        DON_VI        = H.ORGANIZATION_ID,
        TEN_DON_VI    = MAX(O2.ORGANIZATION_NAME),
        NGAY_XUAT     = CAST(NULL AS smalldatetime),
        SO_PHIEU_XUAT = NULLIF(LTRIM(RTRIM(H.ORIG_TRAN_NO)), ''),
        KHO_XUAT      = CAST(NULL AS nvarchar(20)),
        TEN_KHO_XUAT  = CAST(NULL AS nvarchar(150)),
        BTP           = WN2.ITEM_ID,
        TEN_BTP       = MAX(BI2.ITEM_NAME),
        SL_SX         = CAST(NULL AS decimal(18, 6)),
        DVT_BTP       = MAX(BI2.UNIT_ID),
        NVL           = CAST(NULL AS nvarchar(20)),
        TEN_NVL       = CAST(NULL AS nvarchar(150)),
        DVT_NVL       = CAST(NULL AS nvarchar(20)),
        SL_NVL_XUAT   = CAST(NULL AS decimal(18, 6)),
        TIEN_NVL      = CAST(NULL AS decimal(18, 6)),
        SO_PHIEU_NHAP = H.TRAN_NO,
        NGAY_NHAP     = H.TRAN_DATE,
        KHO_NHAP      = WN2.WAREHOUSE_ID,
        SL_NHAP       = SUM(WN2.QUANTITY),
        TIEN_NHAP     = SUM(WN2.AMOUNT),
        CHENH_SL      = CAST(NULL AS decimal(18, 6)),
        TRANG_THAI    = N'{tt_khonggoc}',
        GHI_CHU       = CASE
            WHEN NULLIF(LTRIM(RTRIM(H.ORIG_TRAN_NO)), '') IS NULL
                 THEN N'Làm tay — không bấm từ phiếu xuất nào, không dựng lại được'
            WHEN MAX(XM.PK_MOI) IS NULL
                 THEN N'Phiếu xuất đã bị xoá — không còn phiếu nào cùng số, phải lập lại phiếu xuất'
            WHEN MAX(NK.NSP_KHAC) IS NOT NULL
                 THEN N'NGHI NHẬP TRÙNG — phiếu xuất đã có phiếu nhập khác: ' + MAX(NK.NSP_KHAC)
            ELSE N'Liên kết đứt — phiếu xuất đã lập lại (khoá mới), chưa có phiếu nhập nào nối vào'
        END
    FROM ORPH_H H
    JOIN dbo.WAREHOUSE WN2 WITH (NOLOCK) ON WN2.PR_KEY = H.PR_KEY AND WN2.ISSUE_RECEIVE = 'N'
    LEFT JOIN ORPH_X XM ON XM.PR_KEY = H.PR_KEY
    LEFT JOIN ORPH_N NK ON NK.PR_KEY = H.PR_KEY
    LEFT JOIN dbo.DM_ITEM         BI2 WITH (NOLOCK) ON BI2.ITEM_ID = WN2.ITEM_ID
    LEFT JOIN dbo.DM_ORGANIZATION O2  WITH (NOLOCK) ON O2.ORGANIZATION_ID = H.ORGANIZATION_ID
    WHERE {inner_orph_wh}
    GROUP BY H.PR_KEY, H.ORGANIZATION_ID, H.ORIG_TRAN_NO, H.TRAN_NO, H.TRAN_DATE,
             WN2.WAREHOUSE_ID, WN2.ITEM_ID
),
DC AS (
    SELECT
        PR_KEY_XUAT   = CAST(CAST(X.PR_KEY AS bigint) AS varchar(30)),
        DON_VI        = X.ORGANIZATION_ID,
        TEN_DON_VI    = O.ORGANIZATION_NAME,
        NGAY_XUAT     = X.TRAN_DATE,
        SO_PHIEU_XUAT = X.TRAN_NO,
        KHO_XUAT      = X.WAREHOUSE_ID,
        TEN_KHO_XUAT  = WH.WAREHOUSE_NAME,
        BTP           = X.PRODUCT_ID,
        TEN_BTP       = BI.ITEM_NAME,
        SL_SX         = X.JOB_QTY,
        DVT_BTP       = BI.UNIT_ID,
        NVL           = X.ITEM_ID,
        TEN_NVL       = DI.ITEM_NAME,
        DVT_NVL       = DI.UNIT_ID,
        SL_NVL_XUAT   = X.QUANTITY,
        TIEN_NVL      = X.AMOUNT,
        SO_PHIEU_NHAP = COALESCE(N.SO_PHIEU_NHAP, NB.SO_PHIEU_NHAP),
        NGAY_NHAP     = COALESCE(N.NGAY_NHAP, NB.NGAY_NHAP),
        KHO_NHAP      = COALESCE(N.KHO_NHAP, NB.KHO_NHAP),
        SL_NHAP       = MOC.SL_MOC,
        TIEN_NHAP     = N.TIEN_NHAP,
        CHENH_SL      = CASE WHEN MOC.SL_MOC IS NULL THEN X.JOB_QTY
                             ELSE X.JOB_QTY - MOC.SL_MOC END,
        -- Đã ghi sổ xét trước, rồi mới tới bản nháp — giống hệt tab điều chuyển nội bộ.
        TRANG_THAI    = CASE WHEN N.SL_NHAP IS NOT NULL AND X.JOB_QTY = MOC.SL_MOC
                                                              THEN N'{tt_du}'
                             WHEN N.SL_NHAP IS NOT NULL       THEN N'{tt_lech}'
                             WHEN NB.SL_NHAP IS NOT NULL      THEN N'{tt_nhap_nhap}'
                             ELSE                                  N'{tt_chua}' END,
        GHI_CHU       = CASE WHEN N.SL_NHAP IS NULL AND NB.SL_NHAP IS NOT NULL
                             THEN N'ĐÃ lập phiếu nhập kho thành phẩm ' + NB.SO_PHIEU_NHAP
                                  + N' nhưng chưa bấm ghi sổ — thành phẩm chưa vào kho'
                             ELSE CAST(NULL AS nvarchar(200)) END
    FROM X
    LEFT JOIN N  ON N.SALE_PR_KEY  = X.PR_KEY AND N.BTP_ID  = X.PRODUCT_ID
    LEFT JOIN NB ON NB.SALE_PR_KEY = X.PR_KEY AND NB.BTP_ID = X.PRODUCT_ID
    -- Mốc gần hơn: JOB_QTY có thể ghi theo ĐVT cơ bản HOẶC ĐVT nhập liệu tuỳ người gõ.
    -- Áp cho cả phiếu đã ghi sổ (N) lẫn bản nháp (NB) — cùng một bệnh.
    OUTER APPLY (SELECT SL_MOC = CASE
            WHEN N.SL_NHAP IS NOT NULL THEN
                 CASE WHEN ABS(X.JOB_QTY - N.SL_NHAP) <= ABS(X.JOB_QTY - N.SL_NHAP_NG)
                      THEN N.SL_NHAP ELSE N.SL_NHAP_NG END
            WHEN NB.SL_NHAP IS NOT NULL THEN
                 CASE WHEN ABS(X.JOB_QTY - NB.SL_NHAP) <= ABS(X.JOB_QTY - NB.SL_NHAP_NG)
                      THEN NB.SL_NHAP ELSE NB.SL_NHAP_NG END
            ELSE NULL END) MOC
    LEFT JOIN dbo.DM_ITEM         DI WITH (NOLOCK) ON DI.ITEM_ID = X.ITEM_ID
    LEFT JOIN dbo.DM_ITEM         BI WITH (NOLOCK) ON BI.ITEM_ID = X.PRODUCT_ID
    LEFT JOIN dbo.DM_WAREHOUSE    WH WITH (NOLOCK) ON WH.WAREHOUSE_ID = X.WAREHOUSE_ID
    LEFT JOIN dbo.DM_ORGANIZATION O  WITH (NOLOCK) ON O.ORGANIZATION_ID = X.ORGANIZATION_ID

    UNION ALL
    -- Phiếu xuất SX BTP chưa ghi sổ: nguyên liệu chưa trừ kho, chưa có gì để nhập.
    SELECT
        PR_KEY_XUAT   = CAST(CAST(XB.PR_KEY AS bigint) AS varchar(30)),
        DON_VI        = XB.ORGANIZATION_ID,
        TEN_DON_VI    = O5.ORGANIZATION_NAME,
        NGAY_XUAT     = XB.TRAN_DATE,
        SO_PHIEU_XUAT = XB.TRAN_NO,
        KHO_XUAT      = XB.WAREHOUSE_ID,
        TEN_KHO_XUAT  = WH5.WAREHOUSE_NAME,
        BTP           = XB.PRODUCT_ID,
        TEN_BTP       = BI5.ITEM_NAME,
        SL_SX         = XB.JOB_QTY,
        DVT_BTP       = BI5.UNIT_ID,
        NVL           = XB.ITEM_ID,
        TEN_NVL       = DI5.ITEM_NAME,
        DVT_NVL       = DI5.UNIT_ID,
        SL_NVL_XUAT   = XB.QUANTITY,
        TIEN_NVL      = CAST(NULL AS decimal(18, 6)),
        SO_PHIEU_NHAP = CAST(NULL AS nvarchar(200)),
        NGAY_NHAP     = CAST(NULL AS smalldatetime),
        KHO_NHAP      = CAST(NULL AS nvarchar(20)),
        SL_NHAP       = CAST(NULL AS decimal(18, 6)),
        TIEN_NHAP     = CAST(NULL AS decimal(18, 6)),
        CHENH_SL      = CAST(NULL AS decimal(18, 6)),
        TRANG_THAI    = N'{tt_xuat_nhap}',
        GHI_CHU       = N'Phiếu xuất chưa ghi sổ — nguyên liệu chưa trừ khỏi kho. '
                        + N'Kế toán cần ghi sổ phiếu này trước khi nhập kho thành phẩm.'
    FROM XB
    LEFT JOIN dbo.DM_ITEM         DI5 WITH (NOLOCK) ON DI5.ITEM_ID = XB.ITEM_ID
    LEFT JOIN dbo.DM_ITEM         BI5 WITH (NOLOCK) ON BI5.ITEM_ID = XB.PRODUCT_ID
    LEFT JOIN dbo.DM_WAREHOUSE    WH5 WITH (NOLOCK) ON WH5.WAREHOUSE_ID = XB.WAREHOUSE_ID
    LEFT JOIN dbo.DM_ORGANIZATION O5  WITH (NOLOCK) ON O5.ORGANIZATION_ID = XB.ORGANIZATION_ID

    UNION ALL SELECT * FROM ORPH
)
"""

_BTPDC_SELECT = ", ".join([
    "PR_KEY_XUAT", "DON_VI", "TEN_DON_VI", "NGAY_XUAT", "SO_PHIEU_XUAT",
    "KHO_XUAT", "TEN_KHO_XUAT", "BTP", "TEN_BTP", "SL_SX", "DVT_BTP",
    "NVL", "TEN_NVL", "DVT_NVL", "SL_NVL_XUAT", "TIEN_NVL",
    "SO_PHIEU_NHAP", "NGAY_NHAP", "KHO_NHAP", "SL_NHAP", "CHENH_SL", "TIEN_NHAP",
    "TRANG_THAI", "GHI_CHU",
])


def _btp_cte(inner_sql, inner_draft_sql, inner_orph_sql, inner_orph_wh_sql):
    # Thứ tự replace có ý: {inner_orph_wh} phải đi trước {inner_orph}, nếu không
    # "{inner_orph}" nuốt mất phần đầu của "{inner_orph_wh}" và để lại chuỗi rác "_wh}".
    return _BTPDC_CTE.replace("{inner_orph_wh}", inner_orph_wh_sql) \
                     .replace("{inner_orph}", inner_orph_sql) \
                     .replace("{inner_draft}", inner_draft_sql) \
                     .replace("{inner}", inner_sql) \
                     .replace("{tt_chua}", BTP_TT_CHUA) \
                     .replace("{tt_du}", BTP_TT_DU) \
                     .replace("{tt_lech}", BTP_TT_LECH) \
                     .replace("{tt_khonggoc}", BTP_TT_KHONGGOC) \
                     .replace("{tt_xuat_nhap}", BTP_TT_XUAT_NHAP) \
                     .replace("{tt_nhap_nhap}", BTP_TT_NHAP_NHAP)


def _build_btp_where(request_args, bo_trang_thai=False):
    """Trả (cte_sql, outer_where, params) — params đúng thứ tự dấu ? (Bẫy 5: inner trước outer).

    ⚠️ `bo_trang_thai=True` ⇒ bỏ riêng bộ lọc trạng thái — xem `_build_dcnb_where`,
    cùng một con bug, sửa cùng một cách.
    """
    f_date = request_args.get("from_date", "01/01/2026")
    t_date = request_args.get("to_date",  "31/12/2026")
    from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
    to_dt   = datetime.strptime(t_date, "%d/%m/%Y").date()

    d1, d2 = from_dt.strftime("%Y%m%d"), to_dt.strftime("%Y%m%d")

    # Nhánh phiếu xuất: lọc theo ngày phiếu XUẤT
    inner   = ["W.TRAN_DATE >= ?", "W.TRAN_DATE <= ?"]
    iparams = [d1, d2]
    # Nhánh phiếu xuất CHƯA GHI SỔ: cùng điều kiện nhưng đọc SALE/SALE_DETAIL
    draft   = ["S.TRAN_DATE >= ?", "S.TRAN_DATE <= ?"]
    dparams = [d1, d2]
    # Nhánh phiếu nhập mồ côi: không có phiếu xuất nên lọc theo ngày phiếu NHẬP
    orph    = ["P2.TRAN_DATE >= ?", "P2.TRAN_DATE <= ?"]   # mức phiếu
    oiparams = [d1, d2]
    orph_wh, owparams = [], []                                # mức dòng (kho nhập)

    for field, ofield, dfield, arg in [
            ("W.ORGANIZATION_ID", "P2.ORGANIZATION_ID", "S.ORGANIZATION_ID", "org_ids"),
            ("W.WAREHOUSE_ID",    "WN2.WAREHOUSE_ID",   "S.WAREHOUSE_ID",    "wh_ids"),
            ("W.ITEM_ID",         None,                 "SD.ITEM_ID",        "item_ids"),
            ("W.PRODUCT_ID",      "WN2.ITEM_ID",        "SD.PRODUCT_ID",     "btp_ids")]:
        vals = [v for v in request_args.get(arg, "").split(",") if v]
        if arg == "org_ids":
            # Lọc đơn vị đi qua _org_filter_sql (ép quyền đơn vị theo tài khoản) cho CẢ 3 nhánh:
            # dòng khớp (W.), phiếu xuất chưa ghi sổ (S.) và phiếu nhập mồ côi (P2.).
            # Thiếu nhánh nào là nhánh đó lộ dữ liệu ngoài quyền.
            _oc, _op = _org_filter_sql(vals, field)
            if _oc:
                inner.append(_oc)
                iparams.extend(_op)
            _oc3, _op3 = _org_filter_sql(vals, dfield)
            if _oc3:
                draft.append(_oc3)
                dparams.extend(_op3)
            _oc2, _op2 = _org_filter_sql(vals, ofield)
            if _oc2:
                orph.append(_oc2)
                oiparams.extend(_op2)
            continue
        if vals:
            ph = ','.join(['?'] * len(vals))
            inner.append(f"{field} IN ({ph})")
            iparams.extend(vals)
            draft.append(f"{dfield} IN ({ph})")
            dparams.extend(vals)
            if ofield and ofield.startswith("WN2."):      # lọc ở mức dòng
                orph_wh.append(f"{ofield} IN ({ph})")
                owparams.extend(vals)
            elif ofield:                                   # lọc ở mức phiếu
                orph.append(f"{ofield} IN ({ph})")
                oiparams.extend(vals)
            else:
                # Lọc theo nguyên liệu ⇒ dòng phiếu nhập mồ côi không có NVL nên bị loại hẳn
                orph.append("1 = 0")

    outer, oparams = [], []
    st = BTP_STATUS_MAP.get(request_args.get("status", "").strip())
    if st and not bo_trang_thai:
        outer.append("TRANG_THAI = ?")
        oparams.append(st)

    for field, arg, like in [("DON_VI", "s_org_id", "{}%"), ("TEN_DON_VI", "s_org_name", "%{}%"),
                             ("SO_PHIEU_XUAT", "s_tran_no", "{}%"), ("KHO_XUAT", "s_wh_id", "{}%"),
                             ("BTP", "s_btp", "{}%"), ("TEN_BTP", "s_btp_name", "%{}%"),
                             ("NVL", "s_nvl", "{}%"), ("TEN_NVL", "s_nvl_name", "%{}%"),
                             ("SO_PHIEU_NHAP", "s_nsp_no", "{}%")]:
        val = request_args.get(arg, "").strip()
        if val:
            outer.append(f"{field} LIKE ?")
            oparams.append(like.format(val))

    # Thứ tự params PHẢI đúng thứ tự dấu ? trong SQL (Bẫy 5):
    # CTE X (iparams) → CTE XB (dparams) → CTE ORPH_H (oiparams)
    #   → WHERE của ORPH (owparams) → WHERE ngoài (oparams)
    return (_btp_cte(" AND ".join(inner), " AND ".join(draft), " AND ".join(orph),
                     " AND ".join(orph_wh) if orph_wh else "1 = 1"),
            (" AND ".join(outer) if outer else "1=1"),
            iparams + dparams + oiparams + owparams + oparams)


def _btp_fmt_rows(columns, raw_rows):
    rows = []
    for raw in raw_rows:
        r = dict(zip(columns, raw))
        for dk in ("NGAY_XUAT", "NGAY_NHAP"):
            v = r.get(dk)
            if isinstance(v, (date, datetime)):
                r[dk] = v.strftime("%d/%m/%Y")
        for nk in ("SL_SX", "SL_NVL_XUAT", "TIEN_NVL", "SL_NHAP", "CHENH_SL", "TIEN_NHAP"):
            v = r.get(nk)
            if v is not None:
                try: r[nk] = float(v)
                except: pass
        pk = r.pop("PR_KEY_XUAT", None)
        r["PR_KEY_XUAT"] = str(pk) if pk is not None else ""
        rows.append(r)
    return rows


def _btp_summary(cursor, cte, where_sql, params):
    """Thống kê theo trạng thái — dùng luôn làm COUNT, khỏi quét bảng thêm lần nữa."""
    cursor.execute(f"""
        {cte}
        SELECT TRANG_THAI, SO_DONG = COUNT(*),
               SO_PHIEU = COUNT(DISTINCT CAST(PR_KEY_XUAT AS varchar(30))),
               SO_CAP   = COUNT(DISTINCT CONCAT(CAST(PR_KEY_XUAT AS varchar(30)), '|', BTP)),
               TIEN_NVL = SUM(TIEN_NVL)
        FROM DC WHERE {where_sql}
        GROUP BY TRANG_THAI
    """, params)
    out = {"tong_dong": 0, "so_dong": {}, "so_cap": {}, "so_phieu": {}, "tien": {}}
    for tt, so_dong, so_phieu, so_cap, tien in cursor.fetchall():
        tt = (tt or "").strip()
        out["tong_dong"] += int(so_dong or 0)
        out["so_dong"][tt] = int(so_dong or 0)
        out["so_cap"][tt] = int(so_cap or 0)
        out["so_phieu"][tt] = int(so_phieu or 0)
        out["tien"][tt] = float(tien or 0)
    return out


@app.route("/api/btp_reconcile")
@with_db_lock
def get_btp_reconcile():
    try:
        page      = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 100))
        export_all  = request.args.get("export_all") == "1"
        known_total = request.args.get("known_total")
        skip_count  = page > 1 and known_total is not None and not export_all

        cte, where_sql, params = _build_btp_where(request.args)
        order_by_sql = _resolve_order_by(
            request.args, BTPDC_SORT_WHITELIST,
            "DON_VI, NGAY_XUAT, SO_PHIEU_XUAT, BTP, NVL"
        )

        conn = get_connection()
        cursor = conn.cursor()

        summary = None
        if export_all:
            cursor.execute(f"{cte} SELECT {_BTPDC_SELECT} FROM DC WHERE {where_sql} ORDER BY {order_by_sql}", params)
            columns  = [c[0] for c in cursor.description]
            raw_rows = cursor.fetchall()
            total_rows = len(raw_rows)
        else:
            if skip_count:
                total_rows = int(known_total)
            else:
                _, w_tt, p_tt = _build_btp_where(request.args, bo_trang_thai=True)
                summary = _btp_summary(cursor, cte, w_tt, p_tt)
                _st = BTP_STATUS_MAP.get(request.args.get("status", "").strip())
                total_rows = summary["so_dong"].get(_st, 0) if _st else summary["tong_dong"]

            offset = (page - 1) * page_size
            cursor.execute(f"""
                {cte}
                SELECT * FROM (
                    SELECT {_BTPDC_SELECT},
                           ROW_NUMBER() OVER (ORDER BY {order_by_sql}) AS RowNum
                    FROM DC WHERE {where_sql}
                ) AS T WHERE RowNum > ? AND RowNum <= ?
            """, params + [offset, offset + page_size])
            columns  = [c[0] for c in cursor.description]
            raw_rows = cursor.fetchall()

        return jsonify({
            "status": "ok",
            "data": _btp_fmt_rows(columns, raw_rows),
            "summary": summary,
            "pagination": {
                "total_rows": total_rows,
                "total_pages": max(1, (total_rows + page_size - 1) // page_size),
                "page": page if not export_all else 1
            }
        })
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


@app.route("/api/btp_reconcile/count")
@with_db_lock
def get_btp_reconcile_count():
    try:
        cte, where_sql, params = _build_btp_where(request.args)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"{cte} SELECT COUNT(*) FROM DC WHERE {where_sql}", params)
        total = cursor.fetchone()[0] or 0
        return jsonify({"status": "ok", "total": int(total)})
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


@app.route("/api/btp_reconcile/stream_csv", methods=["POST", "GET"])
def get_btp_reconcile_stream_csv():
    try:
        args = request.args
        total_estimate = int(args.get("total", 0) or 0)
        cte, where_sql, params = _build_btp_where(args)
        order_by_sql = _resolve_order_by(
            args, BTPDC_SORT_WHITELIST, "DON_VI, NGAY_XUAT, SO_PHIEU_XUAT, BTP, NVL"
        )
        sql = f"{cte} SELECT {_BTPDC_SELECT} FROM DC WHERE {where_sql} ORDER BY {order_by_sql}"

        def transform(raw, sql_cols):
            d = dict(zip(sql_cols, raw))
            out = []
            for key, _ in BTPDC_CSV_COLS:
                v = d.get(key)
                if isinstance(v, (date, datetime)):
                    v = v.strftime("%d/%m/%Y")
                out.append(v)
            return out

        headers = [label for _, label in BTPDC_CSV_COLS]
        fname   = f"DoiChieuXuatSX_NhapTP_{args.get('from_date','').replace('/','')}-{args.get('to_date','').replace('/','')}.{args.get('format', 'csv')}"
        job_id  = _start_export_job(fname, headers, sql, params, transform, total_estimate)
        return jsonify({"status": "ok", "job_id": job_id, "filename": fname})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# =============== ĐỐI CHIẾU ĐIỀU CHUYỂN NỘI BỘ (XDCNB → NDCNB) ===============
# Danh sách RIÊNG BIỆT. Mỗi dòng = 1 mã hàng trên phiếu xuất XDCNB, kèm phiếu nhập
# NDCNB tương ứng của đúng mã hàng đó.
#
# KHOÁ NỐI — đo trên IACC_CHULONG ngày 21/09/2026:
#   PURCHASE.SALE_PR_KEY = SALE.PR_KEY, y hệt khuôn BTP.
#   19.838 phiếu NDCNB năm 2026 → 19.828 nối được (99,95%), 10 mồ côi.
#   ⛔ CẤM nối theo số phiếu — số phiếu trùng nhau giữa các đơn vị.
#
# ⚠️ KHÁC BTP Ở HAI ĐIỂM, ĐỪNG BÊ NGUYÊN:
#   1) Xuất và nhập ở HAI ĐƠN VỊ KHÁC NHAU (kho tổng 01 xuất → cửa hàng 35/71/32… nhận).
#      Vì vậy có CẢ HAI cột đơn vị. Bộ lọc Đơn vị áp cho phía XUẤT (chủ phiếu), phía nhận
#      lọc bằng ô tìm kiếm riêng — xem ghi chú ở _build_dcnb_where.
#   2) NDCNB có IS_SALE = 0 ⇒ **KHÔNG nằm trong PURCHASE_VIEW** (Bẫy 15). Phải đọc thẳng
#      bảng dbo.PURCHASE; đọc qua view là ra 0 dòng mà không báo lỗi.
#
# SỐ LƯỢNG: hai phía cùng ĐVT cơ bản nên so THẲNG QUANTITY là đúng — đã đo 2026:
#   khớp 133.348 · chưa nhận 4.603 · lệch 28. KHÔNG cần mẹo "mốc gần hơn" như BTP
#   (mẹo đó sinh ra vì JOB_QTY của BTP ghi bằng 1 trong 2 đơn vị tuỳ người gõ).
DCNB_TT_DU   = "Đã nhận đủ"
DCNB_TT_CHUA = "Không tìm thấy phiếu nhập"
DCNB_TT_LECH = "Lệch số lượng"
DCNB_TT_KHONGGOC = "Không tìm thấy phiếu xuất liên quan"

# ⚠️ HAI TRẠNG THÁI "CHƯA GHI SỔ" — thêm 21/09/2026, xem Bẫy 24 trong CLAUDE.md.
# STATUS trên SALE/PURCHASE chỉ có ĐÚNG 2 giá trị: 'POSTED' (đã ghi sổ) / 'DRAFT'.
# (REVIEW_STATUS là thứ khác, gần như không dùng: 29/19.887 phiếu ⇒ ĐỪNG lấy nhầm.)
# Phiếu DRAFT **KHÔNG sinh một dòng nào trong dbo.WAREHOUSE** — đo T09/2026: 13 phiếu
# XDCNB DRAFT → 0 dòng; 211 phiếu NDCNB DRAFT → 0 dòng. Vì vậy chúng VÔ HÌNH với nhánh
# X/N vốn đọc WAREHOUSE, phải đọc thêm SALE_DETAIL / PURCHASE_DETAIL (nối bằng FR_KEY).
DCNB_TT_XUAT_NHAP = "Phiếu xuất chưa ghi sổ"
DCNB_TT_NHAP_NHAP = "Phiếu nhập chưa ghi sổ"

DCNB_STATUS_MAP = {"du": DCNB_TT_DU, "chua": DCNB_TT_CHUA,
                   "lech": DCNB_TT_LECH, "khonggoc": DCNB_TT_KHONGGOC,
                   "xuat_chua_gs": DCNB_TT_XUAT_NHAP, "nhap_chua_gs": DCNB_TT_NHAP_NHAP}

DCNB_SORT_WHITELIST = {c: c for c in [
    "DON_VI_XUAT", "TEN_DV_XUAT", "NGAY_XUAT", "SO_PHIEU_XUAT", "KHO_XUAT", "TEN_KHO_XUAT",
    "MA_HANG", "TEN_HANG", "DVT", "SL_XUAT", "TIEN_XUAT",
    "DON_VI_NHAP", "TEN_DV_NHAP", "SO_PHIEU_NHAP", "NGAY_NHAP", "KHO_NHAP", "TEN_KHO_NHAP",
    "SL_NHAN", "CHENH_SL", "TRANG_THAI", "GHI_CHU",
]}

DCNB_CSV_COLS = [
    ("DON_VI_XUAT", "Mã ĐV xuất"), ("TEN_DV_XUAT", "Tên đơn vị xuất"),
    ("NGAY_XUAT", "Ngày xuất"), ("SO_PHIEU_XUAT", "Phiếu xuất"),
    ("KHO_XUAT", "Mã kho xuất"), ("TEN_KHO_XUAT", "Tên kho xuất"),
    ("MA_HANG", "Mã hàng"), ("TEN_HANG", "Tên hàng"), ("DVT", "ĐVT"),
    ("SL_XUAT", "SL xuất"), ("TIEN_XUAT", "Tiền xuất"),
    ("DON_VI_NHAP", "Mã ĐV nhận"), ("TEN_DV_NHAP", "Tên đơn vị nhận"),
    ("SO_PHIEU_NHAP", "Phiếu nhập"), ("NGAY_NHAP", "Ngày nhập"),
    ("KHO_NHAP", "Mã kho nhập"), ("TEN_KHO_NHAP", "Tên kho nhập"),
    ("SL_NHAN", "SL nhận"), ("CHENH_SL", "Chênh SL"),
    ("TRANG_THAI", "Trạng thái"), ("GHI_CHU", "Ghi chú"),
]

# {inner} = lọc sớm trên dòng xuất (ngày/đơn vị xuất/kho/mã hàng)
_DCNB_CTE = """
WITH X AS (
    SELECT W.PR_KEY, W.TRAN_NO, W.TRAN_DATE, W.ORGANIZATION_ID, W.WAREHOUSE_ID, W.ITEM_ID,
           QUANTITY = SUM(W.QUANTITY), AMOUNT = SUM(W.AMOUNT)
    FROM dbo.WAREHOUSE W WITH (NOLOCK)
    WHERE W.TRAN_ID = 'XDCNB' AND W.ISSUE_RECEIVE = 'X' AND {inner}
    GROUP BY W.PR_KEY, W.TRAN_NO, W.TRAN_DATE, W.ORGANIZATION_ID, W.WAREHOUSE_ID, W.ITEM_ID
),
XD AS (
    -- Phiếu XUẤT chưa ghi sổ. Không có dòng nào trong WAREHOUSE nên phải lấy từ SALE_DETAIL.
    -- ⛔ Nối bằng FR_KEY, KHÔNG phải PR_KEY: trên *_DETAIL của iPOS thì PR_KEY là khoá của
    --    chính dòng đó, FR_KEY mới trỏ về phiếu cha (giống PO_DETAIL.FR_KEY ở Bẫy 20).
    --    Nối nhầm PR_KEY ra 0 dòng cho CẢ phiếu đã ghi sổ — đã vấp thật khi khảo sát.
    -- ⛔ SL phải lấy QUANTITY_WH. Đo T09/2026 so với WAREHOUSE.QUANTITY:
    --    QUANTITY_WH khớp 12.706/12.706 (100%) · QUANTITY chỉ 3.569 (28%) · QUANTITY_EXTRA 3.273.
    --    QUANTITY ghi theo ĐVT nhập liệu (10 BỊCH) còn kho theo ĐVT cơ bản (7.000 G).
    -- QUANTITY_WH <> 0: bỏ dòng trống trên phiếu — đo được 39/39 ca lệch giữa SALE_DETAIL và
    --    WAREHOUSE đều là dòng SL = 0, lọc đi thì hai nguồn trùng khít.
    SELECT S.PR_KEY, S.TRAN_NO, S.TRAN_DATE, S.ORGANIZATION_ID,
           S.WAREHOUSE_ID, S.WAREHOUSE_ID_RECEIVE, SD.ITEM_ID,
           QUANTITY = SUM(SD.QUANTITY_WH)
    FROM dbo.SALE S WITH (NOLOCK)
    JOIN dbo.SALE_DETAIL SD WITH (NOLOCK) ON SD.FR_KEY = S.PR_KEY
    WHERE S.TRAN_ID = 'XDCNB' AND S.STATUS <> 'POSTED'
      AND ISNULL(SD.QUANTITY_WH, 0) <> 0 AND {inner_draft}
    GROUP BY S.PR_KEY, S.TRAN_NO, S.TRAN_DATE, S.ORGANIZATION_ID,
             S.WAREHOUSE_ID, S.WAREHOUSE_ID_RECEIVE, SD.ITEM_ID
),
P AS (
    SELECT PR_KEY, TRAN_NO, TRAN_DATE, SALE_PR_KEY, ORGANIZATION_ID
    FROM dbo.PURCHASE WITH (NOLOCK)
    WHERE TRAN_ID = 'NDCNB' AND SALE_PR_KEY IS NOT NULL AND SALE_PR_KEY <> 0
),
N0 AS (
    SELECT P.SALE_PR_KEY, WN.ITEM_ID, P.TRAN_NO, P.TRAN_DATE,
           P.ORGANIZATION_ID, WN.WAREHOUSE_ID, SL = SUM(WN.QUANTITY)
    FROM P
    JOIN dbo.WAREHOUSE WN WITH (NOLOCK) ON WN.PR_KEY = P.PR_KEY AND WN.ISSUE_RECEIVE = 'N'
    GROUP BY P.SALE_PR_KEY, WN.ITEM_ID, P.TRAN_NO, P.TRAN_DATE, P.ORGANIZATION_ID, WN.WAREHOUSE_ID
),
N AS (
    SELECT SALE_PR_KEY, ITEM_ID,
           SO_PHIEU_NHAP = STRING_AGG(TRAN_NO, ' + '),
           NGAY_NHAP     = MIN(TRAN_DATE),
           DON_VI_NHAP   = STRING_AGG(ORGANIZATION_ID, ' + '),
           KHO_NHAP      = STRING_AGG(WAREHOUSE_ID, ' + '),
           SL_NHAN       = SUM(SL)
    FROM N0 GROUP BY SALE_PR_KEY, ITEM_ID
),
NP AS (
    -- Phiếu nhập có tồn tại ở MỨC PHIẾU không (bất kể mã hàng) — dùng để tách hai loại
    -- trong nhóm "Không tìm thấy phiếu nhập": mất hẳn phiếu, hay có phiếu mà thiếu mã.
    -- Đo T09/2026: 8 phiếu mất hẳn, 3 phiếu có phiếu nhập nhưng thiếu đúng một mã hàng
    -- (vd XNB00373/T09 xuất 13 mã, NNB0009/T09 đã ghi sổ chỉ có 12 — thiếu COC 2.000 G).
    -- Lấy lại từ CTE P nên KHÔNG quét thêm bảng PURCHASE lần nữa.
    SELECT SALE_PR_KEY, SO_PHIEU = MAX(TRAN_NO) FROM P GROUP BY SALE_PR_KEY
),
ND AS (
    -- Phiếu NHẬP chưa duyệt ghi sổ. ⚠️ iPOS TỰ SINH phiếu nhập khi phiếu xuất ghi sổ —
    -- bên nhận KHÔNG tự lập, họ chỉ kiểm rồi bấm duyệt. Đo T09/2026: 1.906/1.915 phiếu xuất
    -- đã ghi sổ có phiếu nhập trỏ về (99,53%). Đừng ghi chữ "bên nhận đã lập phiếu" — sai người.
    -- Tách khỏi nhóm "Không tìm thấy phiếu nhập" vì hai việc khác hẳn nhau: ở đây phiếu đã
    -- có sẵn, bấm duyệt là xong, không mất hàng. Đo T09/2026: 187 phiếu nằm ở nhóm này.
    -- Cùng luật với XD: nối FR_KEY, lấy QUANTITY_WH (khớp WAREHOUSE 11.013/11.013).
    -- Không lọc theo ngày, giống CTE P ở trên — phiếu nhập có thể sang tháng khác.
    SELECT P2.SALE_PR_KEY, PD.ITEM_ID,
           SO_PHIEU_NHAP = MAX(P2.TRAN_NO),
           NGAY_NHAP     = MIN(P2.TRAN_DATE),
           DON_VI_NHAP   = MAX(P2.ORGANIZATION_ID),
           KHO_NHAP      = MAX(PD.WAREHOUSE_ID),
           SL_NHAN       = SUM(PD.QUANTITY_WH)
    FROM dbo.PURCHASE P2 WITH (NOLOCK)
    JOIN dbo.PURCHASE_DETAIL PD WITH (NOLOCK) ON PD.FR_KEY = P2.PR_KEY
    WHERE P2.TRAN_ID = 'NDCNB' AND P2.STATUS <> 'POSTED'
      AND P2.SALE_PR_KEY IS NOT NULL AND P2.SALE_PR_KEY <> 0
      AND ISNULL(PD.QUANTITY_WH, 0) <> 0
    GROUP BY P2.SALE_PR_KEY, PD.ITEM_ID
),
ORPH_H AS (
    -- Phiếu NHẬP không truy được về phiếu xuất (lọc mức phiếu: ngày nhập + đơn vị nhận)
    SELECT P2.PR_KEY, P2.ORGANIZATION_ID, P2.ORIG_TRAN_NO, P2.TRAN_NO, P2.TRAN_DATE
    FROM dbo.PURCHASE P2 WITH (NOLOCK)
    LEFT JOIN dbo.SALE S2 WITH (NOLOCK) ON S2.PR_KEY = P2.SALE_PR_KEY
    WHERE P2.TRAN_ID = 'NDCNB'
      AND (P2.SALE_PR_KEY IS NULL OR P2.SALE_PR_KEY = 0 OR S2.PR_KEY IS NULL)
      AND {inner_orph}
),
ORPH_X AS (
    -- Số chứng từ xuất ghi trên phiếu nhập giờ còn dẫn tới phiếu nào không?
    -- JOIN một lượt, KHÔNG dùng OUTER APPLY tương quan: SALE 1 triệu dòng không có
    -- index trên TRAN_NO, viết kiểu tương quan làm tab tụt xuống hàng chục giây.
    SELECT H.PR_KEY, PK_MOI = MAX(S3.PR_KEY)
    FROM ORPH_H H
    JOIN dbo.SALE S3 WITH (NOLOCK)
      ON S3.TRAN_NO = H.ORIG_TRAN_NO AND S3.TRAN_ID = 'XDCNB'
    GROUP BY H.PR_KEY
),
ORPH_N AS (
    -- Phiếu xuất đó đã có phiếu nhập KHÁC nối vào chưa ⇒ nghi nhận trùng
    SELECT X.PR_KEY, NDC_KHAC = MAX(P3.TRAN_NO)
    FROM ORPH_X X
    JOIN dbo.PURCHASE P3 WITH (NOLOCK)
      ON P3.TRAN_ID = 'NDCNB' AND P3.SALE_PR_KEY = X.PK_MOI AND P3.PR_KEY <> X.PR_KEY
    GROUP BY X.PR_KEY
),
ORPH AS (
    -- Mỗi dòng = 1 mã hàng đã nhận. Phần xuất để trống vì không có phiếu xuất để lấy.
    SELECT
        PR_KEY_XUAT   = 'N' + CAST(CAST(H.PR_KEY AS bigint) AS varchar(30)),
        DON_VI_XUAT   = CAST(NULL AS nvarchar(20)),
        TEN_DV_XUAT   = CAST(NULL AS nvarchar(150)),
        NGAY_XUAT     = CAST(NULL AS smalldatetime),
        SO_PHIEU_XUAT = NULLIF(LTRIM(RTRIM(H.ORIG_TRAN_NO)), ''),
        KHO_XUAT      = CAST(NULL AS nvarchar(20)),
        TEN_KHO_XUAT  = CAST(NULL AS nvarchar(150)),
        MA_HANG       = WN2.ITEM_ID,
        TEN_HANG      = MAX(DI2.ITEM_NAME),
        DVT           = MAX(DI2.UNIT_ID),
        SL_XUAT       = CAST(NULL AS decimal(18, 6)),
        TIEN_XUAT     = CAST(NULL AS decimal(18, 6)),
        DON_VI_NHAP   = H.ORGANIZATION_ID,
        TEN_DV_NHAP   = MAX(O2.ORGANIZATION_NAME),
        SO_PHIEU_NHAP = H.TRAN_NO,
        NGAY_NHAP     = H.TRAN_DATE,
        KHO_NHAP      = WN2.WAREHOUSE_ID,
        TEN_KHO_NHAP  = MAX(DW2.WAREHOUSE_NAME),
        SL_NHAN       = SUM(WN2.QUANTITY),
        CHENH_SL      = CAST(NULL AS decimal(18, 6)),
        TRANG_THAI    = N'{tt_khonggoc}',
        GHI_CHU       = CASE
            WHEN NULLIF(LTRIM(RTRIM(H.ORIG_TRAN_NO)), '') IS NULL
                 THEN N'Làm tay — không bấm từ phiếu xuất nào, không dựng lại được'
            WHEN MAX(XM.PK_MOI) IS NULL
                 THEN N'Phiếu xuất đã bị xoá — không còn phiếu nào cùng số, phải lập lại phiếu xuất'
            WHEN MAX(NK.NDC_KHAC) IS NOT NULL
                 THEN N'NGHI NHẬN TRÙNG — phiếu xuất đã có phiếu nhập khác: ' + MAX(NK.NDC_KHAC)
            ELSE N'Liên kết đứt — phiếu xuất đã lập lại (khoá mới), chưa có phiếu nhập nào nối vào'
        END
    FROM ORPH_H H
    JOIN dbo.WAREHOUSE WN2 WITH (NOLOCK) ON WN2.PR_KEY = H.PR_KEY AND WN2.ISSUE_RECEIVE = 'N'
    LEFT JOIN ORPH_X XM ON XM.PR_KEY = H.PR_KEY
    LEFT JOIN ORPH_N NK ON NK.PR_KEY = H.PR_KEY
    LEFT JOIN dbo.DM_ITEM         DI2 WITH (NOLOCK) ON DI2.ITEM_ID = WN2.ITEM_ID
    LEFT JOIN dbo.DM_ORGANIZATION O2  WITH (NOLOCK) ON O2.ORGANIZATION_ID = H.ORGANIZATION_ID
    LEFT JOIN dbo.DM_WAREHOUSE    DW2 WITH (NOLOCK) ON DW2.WAREHOUSE_ID = WN2.WAREHOUSE_ID
    WHERE {inner_orph_wh}
    GROUP BY H.PR_KEY, H.ORGANIZATION_ID, H.ORIG_TRAN_NO, H.TRAN_NO, H.TRAN_DATE,
             WN2.WAREHOUSE_ID, WN2.ITEM_ID
),
DC AS (
    SELECT
        PR_KEY_XUAT   = CAST(CAST(X.PR_KEY AS bigint) AS varchar(30)),
        DON_VI_XUAT   = X.ORGANIZATION_ID,
        TEN_DV_XUAT   = O.ORGANIZATION_NAME,
        NGAY_XUAT     = X.TRAN_DATE,
        SO_PHIEU_XUAT = X.TRAN_NO,
        KHO_XUAT      = X.WAREHOUSE_ID,
        TEN_KHO_XUAT  = WH.WAREHOUSE_NAME,
        MA_HANG       = X.ITEM_ID,
        TEN_HANG      = DI.ITEM_NAME,
        DVT           = DI.UNIT_ID,
        SL_XUAT       = X.QUANTITY,
        TIEN_XUAT     = X.AMOUNT,
        -- Kho/đơn vị NHẬN lấy theo 3 mức ưu tiên: đã ghi sổ → bản nháp → kho đến ghi sẵn
        -- trên đầu phiếu xuất (SALE.WAREHOUSE_ID_RECEIVE). Nhờ mức 3 mà dòng chưa nhận
        -- không còn để trống "—" như trước. Mức 3 đáng tin: đo cả năm 2026 được
        -- 19.225/19.226 cặp khớp kho nhận thật (1 lệch), và 0 phiếu đi tới nhiều kho.
        DON_VI_NHAP   = COALESCE(N.DON_VI_NHAP, ND.DON_VI_NHAP, DWR.ORGANIZATION_ID),
        TEN_DV_NHAP   = COALESCE(ON2.ORGANIZATION_NAME, ON3.ORGANIZATION_NAME),
        SO_PHIEU_NHAP = COALESCE(N.SO_PHIEU_NHAP, ND.SO_PHIEU_NHAP),
        NGAY_NHAP     = COALESCE(N.NGAY_NHAP, ND.NGAY_NHAP),
        KHO_NHAP      = COALESCE(N.KHO_NHAP, ND.KHO_NHAP, XS.WAREHOUSE_ID_RECEIVE),
        TEN_KHO_NHAP  = COALESCE(WHN.WAREHOUSE_NAME, WHD.WAREHOUSE_NAME, DWR.WAREHOUSE_NAME),
        SL_NHAN       = COALESCE(N.SL_NHAN, ND.SL_NHAN),
        CHENH_SL      = CASE WHEN N.SL_NHAN  IS NOT NULL THEN X.QUANTITY - N.SL_NHAN
                             WHEN ND.SL_NHAN IS NOT NULL THEN X.QUANTITY - ND.SL_NHAN
                             ELSE X.QUANTITY END,
        -- Thứ tự xét: đã ghi sổ thắng trước, rồi mới tới bản nháp. Đo được 0 phiếu xuất
        -- vừa có phiếu nhập đã ghi sổ vừa có bản nháp ⇒ hai nhánh không chồng nhau.
        TRANG_THAI    = CASE WHEN N.SL_NHAN IS NOT NULL AND X.QUANTITY = N.SL_NHAN
                                                             THEN N'{tt_du}'
                             WHEN N.SL_NHAN IS NOT NULL      THEN N'{tt_lech}'
                             WHEN ND.SL_NHAN IS NOT NULL     THEN N'{tt_nhap_nhap}'
                             ELSE                                 N'{tt_chua}' END,
        GHI_CHU       = CASE
                             WHEN N.SL_NHAN IS NULL AND ND.SL_NHAN IS NOT NULL
                                  THEN N'Phiếu nhập ' + ND.SO_PHIEU_NHAP + N' chưa duyệt ghi sổ'
                             -- Không khớp mã hàng nào, NHƯNG phiếu nhập vẫn tồn tại ⇒ hàng ra
                             -- khỏi kho mà bị bỏ sót đúng mã này. Không nói rõ thì người đọc đi
                             -- tìm phiếu nhập, thấy có, rồi tưởng báo cáo sai.
                             WHEN N.SL_NHAN IS NULL AND ND.SL_NHAN IS NULL
                                  AND NP.SO_PHIEU IS NOT NULL
                                  THEN N'Phiếu nhập ' + NP.SO_PHIEU + N' CÓ nhưng thiếu mã hàng này'
                             ELSE CAST(NULL AS nvarchar(200)) END
    FROM X
    LEFT JOIN N  ON N.SALE_PR_KEY  = X.PR_KEY AND N.ITEM_ID  = X.ITEM_ID
    LEFT JOIN ND ON ND.SALE_PR_KEY = X.PR_KEY AND ND.ITEM_ID = X.ITEM_ID
    LEFT JOIN NP ON NP.SALE_PR_KEY = X.PR_KEY
    -- Đầu phiếu xuất: chỉ lấy WAREHOUSE_ID_RECEIVE (kho đến). PR_KEY là khoá chính của SALE.
    LEFT JOIN dbo.SALE            XS  WITH (NOLOCK) ON XS.PR_KEY = X.PR_KEY
    LEFT JOIN dbo.DM_ITEM         DI  WITH (NOLOCK) ON DI.ITEM_ID = X.ITEM_ID
    LEFT JOIN dbo.DM_WAREHOUSE    WH  WITH (NOLOCK) ON WH.WAREHOUSE_ID = X.WAREHOUSE_ID
    LEFT JOIN dbo.DM_ORGANIZATION O   WITH (NOLOCK) ON O.ORGANIZATION_ID = X.ORGANIZATION_ID
    LEFT JOIN dbo.DM_WAREHOUSE    WHN WITH (NOLOCK) ON WHN.WAREHOUSE_ID = N.KHO_NHAP
    LEFT JOIN dbo.DM_WAREHOUSE    WHD WITH (NOLOCK) ON WHD.WAREHOUSE_ID = ND.KHO_NHAP
    LEFT JOIN dbo.DM_WAREHOUSE    DWR WITH (NOLOCK) ON DWR.WAREHOUSE_ID = XS.WAREHOUSE_ID_RECEIVE
    -- Tên đơn vị nhận chỉ tra được khi phiếu xuất đi tới ĐÚNG MỘT đơn vị. Đi nhiều nơi thì
    -- DON_VI_NHAP là chuỗi "35 + 71" nên JOIN không khớp ⇒ để trống tên, mã vẫn hiện đủ.
    LEFT JOIN dbo.DM_ORGANIZATION ON2 WITH (NOLOCK) ON ON2.ORGANIZATION_ID = N.DON_VI_NHAP
    -- Suy đơn vị nhận từ kho đến. Đo T09/2026: khớp 1.511/1.511, 0 kho thiếu đơn vị.
    LEFT JOIN dbo.DM_ORGANIZATION ON3 WITH (NOLOCK) ON ON3.ORGANIZATION_ID = DWR.ORGANIZATION_ID

    UNION ALL
    -- Phiếu XUẤT chưa ghi sổ: hàng chưa hề trừ kho, nên KHÔNG có phía nhận để đối chiếu.
    SELECT
        PR_KEY_XUAT   = CAST(CAST(XD.PR_KEY AS bigint) AS varchar(30)),
        DON_VI_XUAT   = XD.ORGANIZATION_ID,
        TEN_DV_XUAT   = O4.ORGANIZATION_NAME,
        NGAY_XUAT     = XD.TRAN_DATE,
        SO_PHIEU_XUAT = XD.TRAN_NO,
        KHO_XUAT      = XD.WAREHOUSE_ID,
        TEN_KHO_XUAT  = WH4.WAREHOUSE_NAME,
        MA_HANG       = XD.ITEM_ID,
        TEN_HANG      = DI4.ITEM_NAME,
        DVT           = DI4.UNIT_ID,
        SL_XUAT       = XD.QUANTITY,
        TIEN_XUAT     = CAST(NULL AS decimal(18, 6)),
        DON_VI_NHAP   = DW4.ORGANIZATION_ID,
        TEN_DV_NHAP   = ON4.ORGANIZATION_NAME,
        SO_PHIEU_NHAP = CAST(NULL AS nvarchar(200)),
        NGAY_NHAP     = CAST(NULL AS smalldatetime),
        KHO_NHAP      = XD.WAREHOUSE_ID_RECEIVE,
        TEN_KHO_NHAP  = DW4.WAREHOUSE_NAME,
        SL_NHAN       = CAST(NULL AS decimal(18, 6)),
        CHENH_SL      = CAST(NULL AS decimal(18, 6)),
        TRANG_THAI    = N'{tt_xuat_nhap}',
        GHI_CHU       = N'Phiếu xuất chưa ghi sổ — hàng chưa trừ khỏi kho, bên nhận chưa '
                        + N'nhận được. Kế toán đơn vị xuất cần ghi sổ phiếu này.'
    FROM XD
    LEFT JOIN dbo.DM_ITEM         DI4 WITH (NOLOCK) ON DI4.ITEM_ID = XD.ITEM_ID
    LEFT JOIN dbo.DM_WAREHOUSE    WH4 WITH (NOLOCK) ON WH4.WAREHOUSE_ID = XD.WAREHOUSE_ID
    LEFT JOIN dbo.DM_ORGANIZATION O4  WITH (NOLOCK) ON O4.ORGANIZATION_ID = XD.ORGANIZATION_ID
    LEFT JOIN dbo.DM_WAREHOUSE    DW4 WITH (NOLOCK) ON DW4.WAREHOUSE_ID = XD.WAREHOUSE_ID_RECEIVE
    LEFT JOIN dbo.DM_ORGANIZATION ON4 WITH (NOLOCK) ON ON4.ORGANIZATION_ID = DW4.ORGANIZATION_ID

    UNION ALL SELECT * FROM ORPH
)
"""

_DCNB_SELECT = ", ".join([
    "PR_KEY_XUAT", "DON_VI_XUAT", "TEN_DV_XUAT", "NGAY_XUAT", "SO_PHIEU_XUAT",
    "KHO_XUAT", "TEN_KHO_XUAT", "MA_HANG", "TEN_HANG", "DVT", "SL_XUAT", "TIEN_XUAT",
    "DON_VI_NHAP", "TEN_DV_NHAP", "SO_PHIEU_NHAP", "NGAY_NHAP", "KHO_NHAP", "TEN_KHO_NHAP",
    "SL_NHAN", "CHENH_SL", "TRANG_THAI", "GHI_CHU",
])


def _dcnb_cte(inner, inner_draft, inner_orph, inner_orph_wh):
    return _DCNB_CTE.format(
        inner=inner, inner_draft=inner_draft,
        inner_orph=inner_orph, inner_orph_wh=inner_orph_wh,
        tt_du=DCNB_TT_DU, tt_chua=DCNB_TT_CHUA, tt_lech=DCNB_TT_LECH,
        tt_khonggoc=DCNB_TT_KHONGGOC,
        tt_xuat_nhap=DCNB_TT_XUAT_NHAP, tt_nhap_nhap=DCNB_TT_NHAP_NHAP,
    )


def _build_dcnb_where(request_args, bo_trang_thai=False):
    """Trả (cte_sql, outer_where, params) — params đúng thứ tự dấu ? (Bẫy 5: inner trước outer).

    ⚠️ Bộ lọc Đơn vị áp cho phía XUẤT (W.ORGANIZATION_ID), giống mọi tab khác lấy đơn vị của
    chính chứng từ. Nhánh phiếu nhập mồ côi không có phía xuất nên áp cho đơn vị NHẬN.
    Muốn lọc theo đơn vị nhận ở nhánh thường thì dùng ô tìm "s_dv_nhap" ở WHERE ngoài.
    """
    f_date = request_args.get("from_date", "01/01/2026")
    t_date = request_args.get("to_date",  "31/12/2026")
    from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
    to_dt   = datetime.strptime(t_date, "%d/%m/%Y").date()
    d1, d2 = from_dt.strftime("%Y%m%d"), to_dt.strftime("%Y%m%d")

    inner   = ["W.TRAN_DATE >= ?", "W.TRAN_DATE <= ?"]
    iparams = [d1, d2]
    draft   = ["S.TRAN_DATE >= ?", "S.TRAN_DATE <= ?"]         # nhánh phiếu xuất chưa ghi sổ
    dparams = [d1, d2]
    orph    = ["P2.TRAN_DATE >= ?", "P2.TRAN_DATE <= ?"]      # mức phiếu nhập
    oiparams = [d1, d2]
    orph_wh, owparams = [], []                                 # mức dòng (mã hàng)

    for field, ofield, dfield, arg in [
            ("W.ORGANIZATION_ID", "P2.ORGANIZATION_ID", "S.ORGANIZATION_ID", "org_ids"),
            ("W.WAREHOUSE_ID",    None,                 "S.WAREHOUSE_ID",    "wh_ids"),
            ("W.ITEM_ID",         "WN2.ITEM_ID",        "SD.ITEM_ID",        "item_ids")]:
        vals = [v for v in request_args.get(arg, "").split(",") if v]
        if arg == "org_ids":
            # Đi qua _org_filter_sql cho CẢ 3 nhánh ⇒ ép quyền đơn vị theo tài khoản.
            # Thiếu nhánh nào là nhánh đó lộ dữ liệu ngoài quyền.
            _oc, _op = _org_filter_sql(vals, field)
            if _oc:
                inner.append(_oc)
                iparams.extend(_op)
            _oc3, _op3 = _org_filter_sql(vals, dfield)
            if _oc3:
                draft.append(_oc3)
                dparams.extend(_op3)
            _oc2, _op2 = _org_filter_sql(vals, ofield)
            if _oc2:
                orph.append(_oc2)
                oiparams.extend(_op2)
            continue
        if vals:
            ph = ','.join(['?'] * len(vals))
            inner.append(f"{field} IN ({ph})")
            iparams.extend(vals)
            draft.append(f"{dfield} IN ({ph})")
            dparams.extend(vals)
            if ofield:
                orph_wh.append(f"{ofield} IN ({ph})")
                owparams.extend(vals)
            else:
                # Lọc theo kho XUẤT ⇒ dòng phiếu nhập mồ côi không có kho xuất nên loại hẳn
                orph.append("1 = 0")

    outer, oparams = [], []
    st = DCNB_STATUS_MAP.get(request_args.get("status", "").strip())
    if st and not bo_trang_thai:
        # ⚠️ Bỏ riêng bộ lọc trạng thái khi dựng phần tóm tắt (hàng chip), giữ nguyên mọi bộ
        # lọc khác. Kẹp TRANG_THAI vào đây là bấm một chip thì mọi chip còn lại về 0 — nhìn
        # như cả kỳ không có dòng nào. Đã vấp thật 24/09/2026.
        outer.append("TRANG_THAI = ?")
        oparams.append(st)

    # Lọc theo kho NHẬN. Phải đặt ở WHERE ngoài vì KHO_NHAP là cột dựng trong CTE (gộp từ
    # 3 nguồn). Dùng IN được vì đo 2026: 0/133.607 nhóm đi tới nhiều kho ⇒ KHO_NHAP luôn
    # là một mã đơn, không bao giờ là chuỗi gộp "A + B".
    wh_nhap = [v for v in request_args.get("wh_nhap_ids", "").split(",") if v]
    if wh_nhap:
        outer.append(f"KHO_NHAP IN ({','.join(['?'] * len(wh_nhap))})")
        oparams.extend(wh_nhap)

    for field, arg, like in [("DON_VI_XUAT", "s_org_id", "{}%"),
                             ("TEN_DV_XUAT", "s_org_name", "%{}%"),
                             ("SO_PHIEU_XUAT", "s_tran_no", "{}%"),
                             ("KHO_XUAT", "s_wh_id", "{}%"),
                             ("MA_HANG", "s_item", "{}%"),
                             ("TEN_HANG", "s_item_name", "%{}%"),
                             ("DVT", "s_dvt", "{}%"),
                             ("DON_VI_NHAP", "s_dv_nhap", "{}%"),
                             ("TEN_DV_NHAP", "s_dv_nhap_name", "%{}%"),
                             ("SO_PHIEU_NHAP", "s_nhap_no", "{}%"),
                             ("KHO_NHAP", "s_kho_nhap", "{}%")]:
        val = request_args.get(arg, "").strip()
        if val:
            outer.append(f"{field} LIKE ?")
            oparams.append(like.format(val))

    # SL xuất là số nên phải ép về chuỗi mới LIKE được. Gõ "1000" ra mọi dòng bắt đầu bằng
    # 1000 — thô nhưng đồng nhất với các cột khác. Cần lọc khoảng thì phải làm min/max riêng.
    val = request_args.get("s_sl_xuat", "").strip()
    if val:
        outer.append("CAST(CAST(SL_XUAT AS decimal(18, 2)) AS varchar(30)) LIKE ?")
        oparams.append(f"{val}%")

    # Thứ tự params PHẢI đúng thứ tự dấu ? trong SQL (Bẫy 5):
    # CTE X (iparams) → CTE XD (dparams) → CTE ORPH_H (oiparams)
    #   → WHERE của ORPH (owparams) → WHERE ngoài (oparams)
    return (_dcnb_cte(" AND ".join(inner), " AND ".join(draft), " AND ".join(orph),
                      " AND ".join(orph_wh) if orph_wh else "1 = 1"),
            (" AND ".join(outer) if outer else "1=1"),
            iparams + dparams + oiparams + owparams + oparams)


def _dcnb_fmt_rows(columns, raw_rows):
    rows = []
    for raw in raw_rows:
        r = dict(zip(columns, raw))
        for dk in ("NGAY_XUAT", "NGAY_NHAP"):
            v = r.get(dk)
            if isinstance(v, (date, datetime)):
                r[dk] = v.strftime("%d/%m/%Y")
        for nk in ("SL_XUAT", "TIEN_XUAT", "SL_NHAN", "CHENH_SL"):
            v = r.get(nk)
            if v is not None:
                try: r[nk] = float(v)
                except: pass
        pk = r.pop("PR_KEY_XUAT", None)
        r["PR_KEY_XUAT"] = str(pk) if pk is not None else ""
        rows.append(r)
    return rows


def _dcnb_summary(cursor, cte, where_sql, params):
    """Thống kê theo trạng thái — dùng luôn làm COUNT, khỏi quét bảng thêm lần nữa."""
    cursor.execute(f"""
        {cte}
        SELECT TRANG_THAI, SO_DONG = COUNT(*),
               SO_PHIEU = COUNT(DISTINCT CAST(PR_KEY_XUAT AS varchar(30))),
               TIEN_XUAT = SUM(TIEN_XUAT)
        FROM DC WHERE {where_sql}
        GROUP BY TRANG_THAI
    """, params)
    # so_dong tách theo từng trạng thái: nhờ nó mà biết số dòng của nhóm đang chọn ngay trong
    # lượt quét này, khỏi phải chạy thêm một câu COUNT nữa.
    out = {"tong_dong": 0, "so_dong": {}, "so_phieu": {}, "tien": {}}
    for tt, so_dong, so_phieu, tien in cursor.fetchall():
        tt = (tt or "").strip()
        out["tong_dong"] += int(so_dong or 0)
        out["so_dong"][tt] = int(so_dong or 0)
        out["so_phieu"][tt] = int(so_phieu or 0)
        out["tien"][tt] = float(tien or 0)
    return out


@app.route("/api/dcnb_reconcile")
@with_db_lock
def get_dcnb_reconcile():
    try:
        page      = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 100))
        export_all  = request.args.get("export_all") == "1"
        known_total = request.args.get("known_total")
        skip_count  = page > 1 and known_total is not None and not export_all

        cte, where_sql, params = _build_dcnb_where(request.args)
        order_by_sql = _resolve_order_by(
            request.args, DCNB_SORT_WHITELIST,
            "DON_VI_XUAT, NGAY_XUAT, SO_PHIEU_XUAT, MA_HANG"
        )

        conn = get_connection()
        cursor = conn.cursor()

        summary = None
        if export_all:
            cursor.execute(f"{cte} SELECT {_DCNB_SELECT} FROM DC WHERE {where_sql} ORDER BY {order_by_sql}", params)
            columns  = [c[0] for c in cursor.description]
            raw_rows = cursor.fetchall()
            total_rows = len(raw_rows)
        else:
            if skip_count:
                total_rows = int(known_total)
            else:
                _, w_tt, p_tt = _build_dcnb_where(request.args, bo_trang_thai=True)
                summary = _dcnb_summary(cursor, cte, w_tt, p_tt)
                _st = DCNB_STATUS_MAP.get(request.args.get("status", "").strip())
                total_rows = summary["so_dong"].get(_st, 0) if _st else summary["tong_dong"]

            offset = (page - 1) * page_size
            cursor.execute(f"""
                {cte}
                SELECT * FROM (
                    SELECT {_DCNB_SELECT},
                           ROW_NUMBER() OVER (ORDER BY {order_by_sql}) AS RowNum
                    FROM DC WHERE {where_sql}
                ) AS T WHERE RowNum > ? AND RowNum <= ?
            """, params + [offset, offset + page_size])
            columns  = [c[0] for c in cursor.description]
            raw_rows = cursor.fetchall()

        return jsonify({
            "status": "ok",
            "data": _dcnb_fmt_rows(columns, raw_rows),
            "summary": summary,
            "pagination": {
                "total_rows": total_rows,
                "total_pages": max(1, (total_rows + page_size - 1) // page_size),
                "page": page if not export_all else 1
            }
        })
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


@app.route("/api/dcnb_reconcile/count")
@with_db_lock
def get_dcnb_reconcile_count():
    try:
        cte, where_sql, params = _build_dcnb_where(request.args)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"{cte} SELECT COUNT(*) FROM DC WHERE {where_sql}", params)
        total = cursor.fetchone()[0] or 0
        return jsonify({"status": "ok", "total": int(total)})
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


@app.route("/api/dcnb_reconcile/stream_csv", methods=["POST", "GET"])
def get_dcnb_reconcile_stream_csv():
    try:
        args = request.args
        total_estimate = int(args.get("total", 0) or 0)
        cte, where_sql, params = _build_dcnb_where(args)
        order_by_sql = _resolve_order_by(
            args, DCNB_SORT_WHITELIST, "DON_VI_XUAT, NGAY_XUAT, SO_PHIEU_XUAT, MA_HANG"
        )
        sql = f"{cte} SELECT {_DCNB_SELECT} FROM DC WHERE {where_sql} ORDER BY {order_by_sql}"

        def transform(raw, sql_cols):
            d = dict(zip(sql_cols, raw))
            out = []
            for key, _ in DCNB_CSV_COLS:
                v = d.get(key)
                if isinstance(v, (date, datetime)):
                    v = v.strftime("%d/%m/%Y")
                out.append(v)
            return out

        headers = [label for _, label in DCNB_CSV_COLS]
        fname   = f"DoiChieuDieuChuyenNoiBo_{args.get('from_date','').replace('/','')}-{args.get('to_date','').replace('/','')}.{args.get('format', 'csv')}"
        job_id  = _start_export_job(fname, headers, sql, params, transform, total_estimate)
        return jsonify({"status": "ok", "job_id": job_id, "filename": fname})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# =============== DANH SÁCH PO — YÊU CẦU MUA HÀNG (TX / TX1 / TX2) ===============
# Mỗi dòng = 1 mã hàng trên một phiếu PO. Nguồn dbo.PO + dbo.PO_DETAIL (KHÔNG có view).
#
# ⛔ CỐ Ý KHÔNG CÓ CỘT "ĐÃ CÓ PHIẾU MUA HÀNG CHƯA" — Đại Ca chốt bỏ ngày 21/09/2026.
#    iPOS trên IACC_CHULONG KHÔNG ghi liên kết PO → phiếu nhập mua. Đã đo 7 khoá:
#      • PURCHASE.SALE_PR_KEY (khoá mà BTP/ĐCNB dùng) ........ 0/4.950 phiếu NM có
#      • PURCHASE.ORIG_TRAN_NO ............................... 0 (chỉ 147 phiếu ghi 'EXCEL')
#      • WAREHOUSE ........................................... không có cột nào trỏ về PO
#      • PURCHASE_DETAIL.PO_TRAN_NO + đơn vị ................. duy nhất nhưng mã hàng chỉ khớp 3,3%
#      • PURCHASE_DETAIL.PO_TRAN_NO không kèm đơn vị ......... mã hàng khớp 41,6% NHƯNG
#        1 dòng nhập ghép với tới 50 phiếu PO (số phiếu PO trùng: POCH2026/0001/T08 có 50 bản
#        ở 50 đơn vị, cùng ngày) ⇒ nổ dòng, số sai hoàn toàn
#      • PO_DETAIL.FR_KEY → PURCHASE.PR_KEY .................. 766 dòng có, mã hàng khớp 2,2%;
#        5 PO khác đơn vị cùng trỏ về MỘT phiếu nhập ⇒ giá trị rác
#      • PO_DETAIL.QUANTITY_RECEIVE .......................... = 0 trên cả 3.383 dòng
#    Ca soi tận nơi: PO POCH2026/0001/T01 của đơn vị 44 đặt LY-NH600 22.000 CÁI, nhưng 12 dòng
#    nhập ghi tham chiếu đúng số PO đó lại toàn mã KEA-* — không dính dáng gì.
#    ➡️ Thêm cột đó vào là bịa liên kết. Muốn làm thì phải hỏi Chú Long / iPOS trước.
#
# ⚠️ ĐỪNG lọc theo dbo.PURCHASE_ORDER — bảng đó TRỐNG 0 dòng (di sản). PO thật ở dbo.PO.
# ⚠️ Danh mục TX/TX1/TX2 lấy TÊN từ SYS_TRAN (Bẫy 14: danh mục lấy ở bảng danh mục).
PO_TRAN_IDS = ("TX", "TX1", "TX2")

# STATUS trên dbo.PO — đo 2026: APPROVED 4.198 · PENDING_APPROVAL 15 · CANCEL 3 · RECEIVED 1.
# Dịch sang tiếng người: người dùng là kế toán, không đọc mã tiếng Anh.
PO_TT_MAP_SQL = """CASE UPPER(LTRIM(RTRIM(ISNULL(PO.STATUS, ''))))
        WHEN 'APPROVED'         THEN N'Đã duyệt'
        WHEN 'PENDING_APPROVAL' THEN N'Chờ duyệt'
        WHEN 'CANCEL'           THEN N'Đã huỷ'
        WHEN 'CANCELLED'        THEN N'Đã huỷ'
        WHEN 'RECEIVED'         THEN N'Đã nhận hàng'
        WHEN ''                 THEN N'(chưa ghi)'
        ELSE PO.STATUS END"""

PO_STATUS_MAP = {"duyet": "Đã duyệt", "cho": "Chờ duyệt",
                 "huy": "Đã huỷ", "nhan": "Đã nhận hàng"}

POLIST_SORT_WHITELIST = {c: c for c in [
    "DON_VI", "TEN_DON_VI", "LOAI_PO", "TEN_LOAI", "SO_PHIEU", "NGAY", "NGAY_GIAO",
    "KHO", "TEN_KHO", "NGUOI_LAP", "TEN_NGUOI_LAP",
    "MA_HANG", "TEN_HANG", "DVT", "SL_DAT", "DON_GIA", "THANH_TIEN", "TONG_TIEN",
    "TRANG_THAI", "GHI_CHU",
]}

POLIST_CSV_COLS = [
    ("DON_VI", "Mã ĐV"), ("TEN_DON_VI", "Tên đơn vị"),
    ("LOAI_PO", "Loại PO"), ("TEN_LOAI", "Tên loại PO"),
    ("SO_PHIEU", "Số phiếu PO"), ("NGAY", "Ngày lập"), ("NGAY_GIAO", "Ngày giao"),
    ("KHO", "Mã kho"), ("TEN_KHO", "Tên kho"),
    ("NGUOI_LAP", "Mã người lập"), ("TEN_NGUOI_LAP", "Người lập"),
    ("MA_HANG", "Mã hàng"), ("TEN_HANG", "Tên hàng"), ("DVT", "ĐVT"),
    ("SL_DAT", "SL đặt"), ("DON_GIA", "Đơn giá"),
    ("THANH_TIEN", "Thành tiền"), ("TONG_TIEN", "Tổng tiền"),
    ("TRANG_THAI", "Trạng thái"), ("GHI_CHU", "Ghi chú"),
]

# Bọc trong CTE `POL` — KHÔNG phải để cho đẹp: ORDER BY của phân trang dùng tên cột đầu ra
# (DON_VI, NGAY, SO_PHIEU…). SQL Server KHÔNG cho dùng bí danh của chính câu SELECT bên trong
# ROW_NUMBER() OVER (ORDER BY …) ⇒ lỗi "Invalid column name 'DON_VI'". Đã vấp thật 21/09/2026.
# Vật chất hoá qua CTE rồi mới ORDER BY thì hết — đúng cách BTP/ĐCNB đang làm.
_POLIST_CTE = """
WITH POL AS (
SELECT
    PR_KEY_PO     = CAST(CAST(PO.PR_KEY AS bigint) AS varchar(30)),
    DON_VI        = PO.ORGANIZATION_ID,
    TEN_DON_VI    = O.ORGANIZATION_NAME,
    LOAI_PO       = PO.TRAN_ID,
    TEN_LOAI      = ST.TRAN_NAME,
    SO_PHIEU      = PO.TRAN_NO,
    NGAY          = PO.TRAN_DATE,
    NGAY_GIAO     = PO.RELEASE_DATE,
    KHO           = D.WAREHOUSE_ID,
    TEN_KHO       = WH.WAREHOUSE_NAME,
    NGUOI_LAP     = PO.EMPLOYEE_ID,
    TEN_NGUOI_LAP = EM.EMPLOYEE_NAME,
    MA_HANG       = D.ITEM_ID,
    TEN_HANG      = ISNULL(NULLIF(LTRIM(RTRIM(D.DESCRIPTION)), ''), DI.ITEM_NAME),
    DVT           = ISNULL(NULLIF(LTRIM(RTRIM(D.UNIT_ID)), ''), DI.UNIT_ID),
    SL_DAT        = D.QUANTITY,
    DON_GIA       = D.UNIT_PRICE,
    THANH_TIEN    = D.AMOUNT,
    TONG_TIEN     = D.TOTAL_AMOUNT,
    TRANG_THAI    = {tt},
    GHI_CHU       = PO.COMMENTS
FROM dbo.PO PO WITH (NOLOCK)
JOIN dbo.PO_DETAIL D WITH (NOLOCK) ON D.PR_KEY = PO.PR_KEY
LEFT JOIN dbo.SYS_TRAN        ST WITH (NOLOCK) ON ST.TRAN_ID = PO.TRAN_ID
LEFT JOIN dbo.DM_ORGANIZATION O  WITH (NOLOCK) ON O.ORGANIZATION_ID = PO.ORGANIZATION_ID
LEFT JOIN dbo.DM_WAREHOUSE    WH WITH (NOLOCK) ON WH.WAREHOUSE_ID = D.WAREHOUSE_ID
LEFT JOIN dbo.DM_ITEM         DI WITH (NOLOCK) ON DI.ITEM_ID = D.ITEM_ID
LEFT JOIN dbo.DM_EMPLOYEE     EM WITH (NOLOCK) ON EM.EMPLOYEE_ID = PO.EMPLOYEE_ID
WHERE {where}
)
"""

# Không danh mục nào trong 5 bảng JOIN ở trên có khoá trùng (đã đo 21/09/2026: SYS_TRAN,
# DM_ORGANIZATION, DM_WAREHOUSE, DM_ITEM, DM_EMPLOYEE đều 0 khoá trùng) ⇒ JOIN không nhân dòng.
_POLIST_SELECT = ", ".join([
    "PR_KEY_PO", "DON_VI", "TEN_DON_VI", "LOAI_PO", "TEN_LOAI", "SO_PHIEU", "NGAY",
    "NGAY_GIAO", "KHO", "TEN_KHO", "NGUOI_LAP", "TEN_NGUOI_LAP", "MA_HANG", "TEN_HANG",
    "DVT", "SL_DAT", "DON_GIA", "THANH_TIEN", "TONG_TIEN", "TRANG_THAI", "GHI_CHU",
])


def _build_polist_where(request_args, bo_trang_thai=False):
    """Trả (cte_sql, params). Mọi điều kiện nằm cùng một mệnh đề WHERE nên thứ tự params
    chính là thứ tự thêm vào đây (Bẫy 5)."""
    f_date = request_args.get("from_date", "01/01/2026")
    t_date = request_args.get("to_date",  "31/12/2026")
    from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
    to_dt   = datetime.strptime(t_date, "%d/%m/%Y").date()
    d1, d2 = from_dt.strftime("%Y%m%d"), to_dt.strftime("%Y%m%d")

    where  = ["PO.TRAN_DATE >= ?", "PO.TRAN_DATE <= ?"]
    params = [d1, d2]

    # Loại PO: mặc định cả 3 mã TX/TX1/TX2; người dùng chọn thì giao với danh sách hợp lệ
    # (đừng nhận thẳng giá trị người dùng gửi lên — nhận bậy là quét cả bảng PO).
    loai = [v for v in request_args.get("loai_po", "").split(",") if v in PO_TRAN_IDS]
    loai = loai or list(PO_TRAN_IDS)
    where.append(f"PO.TRAN_ID IN ({','.join(['?'] * len(loai))})")
    params.extend(loai)

    # Đơn vị đi qua _org_filter_sql ⇒ ép quyền đơn vị theo tài khoản (điểm DUY NHẤT).
    orgs = [v for v in request_args.get("org_ids", "").split(",") if v]
    oc, op = _org_filter_sql(orgs, "PO.ORGANIZATION_ID")
    if oc:
        where.append(oc)
        params.extend(op)

    for field, arg in [("D.WAREHOUSE_ID", "wh_ids"), ("D.ITEM_ID", "item_ids")]:
        vals = [v for v in request_args.get(arg, "").split(",") if v]
        if vals:
            where.append(f"{field} IN ({','.join(['?'] * len(vals))})")
            params.extend(vals)

    st = PO_STATUS_MAP.get(request_args.get("status", "").strip())
    if st and not bo_trang_thai:
    # ⚠️ Bỏ riêng bộ lọc trạng thái khi dựng phần tóm tắt (hàng chip), giữ nguyên mọi bộ
    # lọc khác. Kẹp TRANG_THAI vào đây là bấm một chip thì mọi chip còn lại về 0 — nhìn
    # như cả kỳ không có dòng nào. Đã vấp thật 24/09/2026.
        where.append(f"{PO_TT_MAP_SQL} = ?")
        params.append(st)

    for field, arg, like in [("PO.ORGANIZATION_ID", "s_org_id", "{}%"),
                             ("O.ORGANIZATION_NAME", "s_org_name", "%{}%"),
                             ("PO.TRAN_NO", "s_tran_no", "{}%"),
                             ("D.WAREHOUSE_ID", "s_wh_id", "{}%"),
                             ("D.ITEM_ID", "s_item", "{}%"),
                             ("DI.ITEM_NAME", "s_item_name", "%{}%"),
                             ("PO.EMPLOYEE_ID", "s_emp", "{}%")]:
        val = request_args.get(arg, "").strip()
        if val:
            where.append(f"{field} LIKE ?")
            params.append(like.format(val))

    return _POLIST_CTE.format(where=" AND ".join(where), tt=PO_TT_MAP_SQL), params


def _polist_fmt_rows(columns, raw_rows):
    rows = []
    for raw in raw_rows:
        r = dict(zip(columns, raw))
        for dk in ("NGAY", "NGAY_GIAO"):
            v = r.get(dk)
            if isinstance(v, (date, datetime)):
                r[dk] = v.strftime("%d/%m/%Y")
        for nk in ("SL_DAT", "DON_GIA", "THANH_TIEN", "TONG_TIEN"):
            v = r.get(nk)
            if v is not None:
                try: r[nk] = float(v)
                except: pass
        pk = r.pop("PR_KEY_PO", None)
        r["PR_KEY_PO"] = str(pk) if pk is not None else ""
        rows.append(r)
    return rows


def _polist_summary(cursor, cte, params):
    """Thống kê theo trạng thái — dùng luôn làm COUNT, khỏi quét bảng thêm lần nữa."""
    cursor.execute(f"""
        {cte}
        SELECT TRANG_THAI,
               SO_DONG  = COUNT(*),
               SO_PHIEU = COUNT(DISTINCT PR_KEY_PO),
               TIEN     = SUM(TONG_TIEN)
        FROM POL GROUP BY TRANG_THAI
    """, params)
    out = {"tong_dong": 0, "so_dong": {}, "so_phieu": {}, "tien": {}}
    for tt, so_dong, so_phieu, tien in cursor.fetchall():
        tt = (tt or "").strip()
        out["tong_dong"] += int(so_dong or 0)
        out["so_dong"][tt] = int(so_dong or 0)
        out["so_phieu"][tt] = int(so_phieu or 0)
        out["tien"][tt] = float(tien or 0)
    return out


@app.route("/api/po_list")
@with_db_lock
def get_po_list():
    try:
        page      = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 100))
        export_all  = request.args.get("export_all") == "1"
        known_total = request.args.get("known_total")
        skip_count  = page > 1 and known_total is not None and not export_all

        cte, params = _build_polist_where(request.args)
        order_by_sql = _resolve_order_by(
            request.args, POLIST_SORT_WHITELIST, "DON_VI, NGAY, SO_PHIEU, MA_HANG"
        )

        conn = get_connection()
        cursor = conn.cursor()

        summary = None
        if export_all:
            cursor.execute(f"{cte} SELECT {_POLIST_SELECT} FROM POL ORDER BY {order_by_sql}", params)
            columns  = [c[0] for c in cursor.description]
            raw_rows = cursor.fetchall()
            total_rows = len(raw_rows)
        else:
            if skip_count:
                total_rows = int(known_total)
            else:
                cte_tt, p_tt = _build_polist_where(request.args, bo_trang_thai=True)
                summary = _polist_summary(cursor, cte_tt, p_tt)
                _st = PO_STATUS_MAP.get(request.args.get("status", "").strip())
                total_rows = summary["so_dong"].get(_st, 0) if _st else summary["tong_dong"]

            offset = (page - 1) * page_size
            cursor.execute(f"""
                {cte}
                SELECT * FROM (
                    SELECT {_POLIST_SELECT},
                           RowNum = ROW_NUMBER() OVER (ORDER BY {order_by_sql})
                    FROM POL
                ) AS T WHERE RowNum > ? AND RowNum <= ?
            """, params + [offset, offset + page_size])
            columns  = [c[0] for c in cursor.description]
            raw_rows = cursor.fetchall()

        return jsonify({
            "status": "ok",
            "data": _polist_fmt_rows(columns, raw_rows),
            "summary": summary,
            "pagination": {
                "total_rows": total_rows,
                "total_pages": max(1, (total_rows + page_size - 1) // page_size),
                "page": page if not export_all else 1
            }
        })
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


@app.route("/api/po_list/count")
@with_db_lock
def get_po_list_count():
    try:
        cte, params = _build_polist_where(request.args)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"{cte} SELECT COUNT(*) FROM POL", params)
        total = cursor.fetchone()[0] or 0
        return jsonify({"status": "ok", "total": int(total)})
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


@app.route("/api/po_list/stream_csv", methods=["POST", "GET"])
def get_po_list_stream_csv():
    try:
        args = request.args
        total_estimate = int(args.get("total", 0) or 0)
        cte, params = _build_polist_where(args)
        order_by_sql = _resolve_order_by(
            args, POLIST_SORT_WHITELIST, "DON_VI, NGAY, SO_PHIEU, MA_HANG"
        )
        sql = f"{cte} SELECT {_POLIST_SELECT} FROM POL ORDER BY {order_by_sql}"

        def transform(raw, sql_cols):
            d = dict(zip(sql_cols, raw))
            out = []
            for key, _ in POLIST_CSV_COLS:
                v = d.get(key)
                if isinstance(v, (date, datetime)):
                    v = v.strftime("%d/%m/%Y")
                out.append(v)
            return out

        headers = [label for _, label in POLIST_CSV_COLS]
        fname   = f"DanhSachPO_{args.get('from_date','').replace('/','')}-{args.get('to_date','').replace('/','')}.{args.get('format', 'csv')}"
        job_id  = _start_export_job(fname, headers, sql, params, transform, total_estimate)
        return jsonify({"status": "ok", "job_id": job_id, "filename": fname})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# =============== SALE_VIEW (Danh sách chứng từ bán hàng) ===============
# Nguồn dbo.SALE_VIEW (152 cột, mức dòng hàng). ITEM_NAME/JOB_NAME/PR_DETAIL_NAME
# đã có sẵn trong view; ORGANIZATION_NAME/EXPENSE_NAME lấy qua JOIN như Purchase.
SALE_BASE_COLUMNS = [
    "ORGANIZATION_ID",
    "TRAN_ID", "TRAN_NO", "TRAN_DATE",
    "VAT_TRAN_NO", "VAT_TRAN_DATE", "VAT_TRAN_SERIE",
    "PR_DETAIL_ID", "PR_DETAIL_NAME",
    "CONTACT_PERSON", "ADDRESS", "TAX_FILE_NUMBER", "PHONE",
    "WAREHOUSE_ID", "EMPLOYEE_ID",
    "ITEM_ID", "ITEM_NAME", "DESCRIPTION", "UNIT_ID",
    "QUANTITY", "UNIT_PRICE", "AMOUNT",
    "DISCOUNT_AMOUNT", "VAT_TAX_RATE", "VAT_TAX_AMOUNT",
    "TOTAL_AMOUNT", "COG_AMOUNT",
    "ACCOUNT_ID", "ACCOUNT_ID_PR", "ACCOUNT_ID_INCOME", "ACCOUNT_ID_VAT", "ACCOUNT_ID_COST",
    "EXPENSE_ID", "JOB_ID", "JOB_NAME", "IS_RETURN", "STATUS",
]

# Cột phụ trên SALE_VIEW — chỉ đưa vào SELECT nếu THỰC SỰ tồn tại (guard qua INFORMATION_SCHEMA,
# tránh bẫy "SELECT cột không có → crash + ngắt pool"). PAYMENT_METHOD_NAME/EXTRA_NAME_2 KHÔNG nằm
# trong SALE_VIEW → map tên ở Python từ DM_PAYMENT_METHOD / DM_EXTRA_2.
SALE_EXTRA_COLUMNS = ["PAYMENT_METHOD_ID", "EXTRA_ID_2", "INCOME_AMOUNT", "VAT_INCOME_AMOUNT", "COMMENTS"]

SALE_SORT_WHITELIST = {col: f"S.{col}" for col in SALE_BASE_COLUMNS}
SALE_SORT_WHITELIST["ORGANIZATION_NAME"] = "O.ORGANIZATION_NAME"
SALE_SORT_WHITELIST["EXPENSE_NAME"]      = "E.EXPENSE_NAME"


def _build_sale_where(request_args):
    """WHERE + params cho dbo.SALE_VIEW. Dùng alias S. Trả (where_sql, params)."""
    f_date = request_args.get("from_date", "01/01/2026")
    t_date = request_args.get("to_date",  "31/12/2026")
    from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
    to_dt   = datetime.strptime(t_date, "%d/%m/%Y").date()

    clauses = ["S.TRAN_DATE >= ?", "S.TRAN_DATE <= ?"]
    params  = [from_dt.strftime("%Y%m%d"), to_dt.strftime("%Y%m%d")]

    for field, arg in [
        ("S.TRAN_ID",        "tran_ids"),
        ("S.ORGANIZATION_ID", "org_ids"),
        ("S.JOB_ID",         "job_ids"),
        ("S.ITEM_ID",        "item_ids"),
        ("S.EXPENSE_ID",     "expense_ids"),
        ("S.PR_DETAIL_ID",   "pr_detail_ids"),
        ("S.WAREHOUSE_ID",   "wh_ids"),
    ]:
        raw = request_args.get(arg, "")
        vals = [v for v in raw.split(",") if v]
        if arg == "org_ids":
            # Lọc đơn vị LUÔN đi qua _org_filter_sql — nơi DUY NHẤT ép quyền đơn vị theo tài
            # khoản (chọn gì cũng bị giao với danh sách được phép). Không chọn ⇒ mặc định loại
            # đơn vị ngoài cây '00', hoặc = đúng đơn vị được phép nếu tài khoản bị giới hạn.
            _oc, _op = _org_filter_sql(vals, field)
            if _oc:
                clauses.append(_oc)
                params.extend(_op)
        elif vals:
            clauses.append(f"{field} IN ({','.join(['?']*len(vals))})")
            params.extend(vals)

    # Lọc hàng bán trả lại (IS_RETURN): '1' chỉ hàng trả, '0' chỉ bán thường
    ret = request_args.get("is_return", "").strip()
    if ret in ("0", "1"):
        clauses.append("ISNULL(S.IS_RETURN,0) = ?")
        params.append(int(ret))

    # ID prefix LIKE (SARGable)
    for field, arg in [
        ("S.TRAN_NO",        "tran_no"),
        ("S.TRAN_ID",        "s_tran_id"),
        ("S.ORGANIZATION_ID", "s_org_id"),
        ("S.WAREHOUSE_ID",   "s_wh_id"),
        ("S.ITEM_ID",        "s_item_id"),
        ("S.VAT_TRAN_NO",    "s_inv_no"),
        ("S.EXPENSE_ID",     "s_exp_id"),
        ("S.JOB_ID",         "s_job_id"),
        ("S.ACCOUNT_ID",     "s_acc_id"),
        ("S.PR_DETAIL_ID",   "s_pr_id"),
        ("S.UNIT_ID",        "s_unit_id"),
        ("S.EMPLOYEE_ID",    "s_emp_id"),
    ]:
        val = request_args.get(arg, "").strip()
        if val:
            clauses.append(f"{field} LIKE ?")
            params.append(f"{val}%")

    # text contains LIKE
    for field, arg in [
        ("S.DESCRIPTION",      "s_desc"),
        ("S.ITEM_NAME",        "s_item_name"),
        ("O.ORGANIZATION_NAME", "s_org_name"),
        ("E.EXPENSE_NAME",     "s_exp_name"),
        ("S.JOB_NAME",         "s_job_name"),
        ("S.PR_DETAIL_NAME",   "s_pr_name"),
        ("S.CONTACT_PERSON",   "s_contact"),
    ]:
        val = request_args.get(arg, "").strip()
        if val:
            clauses.append(f"{field} LIKE ?")
            params.append(f"%{val}%")

    # Search ngày VAT_TRAN_DATE — dd/mm/yyyy
    vd = request_args.get("s_vat_date", "").strip()
    if vd:
        try:
            parts = [p for p in vd.split('/') if p]
            if len(parts) == 3:
                dd, mm, yy = int(parts[0]), int(parts[1]), int(parts[2])
                if yy < 100: yy += 2000
                clauses.append("S.VAT_TRAN_DATE = ?")
                params.append(f"{yy:04d}{mm:02d}{dd:02d}")
            else:
                clauses.append("CONVERT(VARCHAR(10), S.VAT_TRAN_DATE, 103) LIKE ?")
                params.append(f"%{vd}%")
        except Exception:
            clauses.append("CONVERT(VARCHAR(10), S.VAT_TRAN_DATE, 103) LIKE ?")
            params.append(f"%{vd}%")

    return " AND ".join(clauses), params


SALE_JOIN_SQL = """
    FROM dbo.SALE_VIEW S WITH (NOLOCK)
    LEFT JOIN dbo.DM_ORGANIZATION O WITH (NOLOCK) ON S.ORGANIZATION_ID = O.ORGANIZATION_ID
    LEFT JOIN dbo.DM_EXPENSE      E WITH (NOLOCK) ON S.EXPENSE_ID      = E.EXPENSE_ID
"""
SALE_SELECT_LIST = (", ".join(f"S.{c}" for c in SALE_BASE_COLUMNS)
                    + ", O.ORGANIZATION_NAME AS ORGANIZATION_NAME, E.EXPENSE_NAME AS EXPENSE_NAME")
# Fast path: chỉ đọc SALE_VIEW, KHÔNG join DM_ORGANIZATION/DM_EXPENSE (join nặng trên view lớn).
# Tên đơn vị/MCP được map từ _meta_cache ở Python. Chỉ join khi người dùng thực sự
# search/sort theo TÊN đơn vị hoặc TÊN MCP.
SALE_FROM_ONLY   = "FROM dbo.SALE_VIEW S WITH (NOLOCK)"
SALE_BASE_SELECT = ", ".join(f"S.{c}" for c in SALE_BASE_COLUMNS)
SALE_NUM_COLS  = ("QUANTITY", "UNIT_PRICE", "AMOUNT", "DISCOUNT_AMOUNT",
                  "VAT_TAX_RATE", "VAT_TAX_AMOUNT", "TOTAL_AMOUNT", "COG_AMOUNT",
                  "INCOME_AMOUNT", "VAT_INCOME_AMOUNT")
SALE_DATE_COLS = ("TRAN_DATE", "VAT_TRAN_DATE")


def _sale_needs_join(args):
    """Chỉ cần JOIN DM khi WHERE/ORDER tham chiếu cột TÊN đơn vị/MCP."""
    ob = (args.get("order_by", "") or "").strip()
    return bool((args.get("s_org_name", "") or "").strip()
                or (args.get("s_exp_name", "") or "").strip()) or ob in ("ORGANIZATION_NAME", "EXPENSE_NAME")


def _sale_name_maps():
    """Map ID → tên cho đơn vị / MCP / kho / ĐVT, lấy từ _meta_cache (tránh JOIN)."""
    db_name = (_db_cfg() or {}).get('database', 'N/A')
    meta = _meta_cache.get(db_name) or {}
    org_map  = {(it.get('id') or '').strip(): it.get('name') or '' for it in meta.get('orgs', [])}
    exp_map  = {(it.get('id') or '').strip(): it.get('name') or '' for it in meta.get('expenses', [])}
    wh_map   = {(it.get('id') or '').strip(): it.get('name') or '' for it in meta.get('warehouses', [])}
    unit_map = {(it.get('id') or '').strip(): it.get('name') or '' for it in meta.get('units', [])}
    return org_map, exp_map, wh_map, unit_map


# Cache theo DB: cột thực có của SALE_VIEW + map tên HTTT / nguồn đơn (extra_2).
_sale_dim_cache = {}


def _sale_dim_info():
    """Trả {'cols': set(tên cột SALE_VIEW in HOA), 'pay': {id:tên HTTT}, 'extra2': {id:tên nguồn}}.
    Introspect 1 lần rồi cache theo DB. Nếu KHÔNG đọc được schema → 'cols' rỗng → KHÔNG thêm cột phụ
    (an toàn: thà thiếu cột còn hơn crash pool). DM_PAYMENT_METHOD/DM_EXTRA_2 bọc try riêng."""
    db = (_db_cfg() or {}).get('database', 'N/A')
    info = _sale_dim_cache.get(db)
    if info is not None:
        return info
    cols, pay_map, extra2_map = set(), {}, {}
    try:
        cur = get_connection().cursor()
        try:
            cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='SALE_VIEW'")
            cols = {(r[0] or '').upper() for r in cur.fetchall()}
        except Exception:
            cols = set()
        try:
            cur.execute("SELECT CAST(PAYMENT_METHOD_ID AS NVARCHAR(100)), PAYMENT_METHOD_NAME FROM dbo.DM_PAYMENT_METHOD WITH (NOLOCK)")
            pay_map = {(r[0] or '').strip(): (r[1] or '').strip() for r in cur.fetchall()}
        except Exception:
            pay_map = {}
        try:
            cur.execute("SELECT CAST(EXTRA_ID_2 AS NVARCHAR(100)), EXTRA_NAME_2 FROM dbo.DM_EXTRA_2 WITH (NOLOCK)")
            extra2_map = {(r[0] or '').strip(): (r[1] or '').strip() for r in cur.fetchall()}
        except Exception:
            extra2_map = {}
    except Exception:
        pass
    info = {"cols": cols, "pay": pay_map, "extra2": extra2_map}
    _sale_dim_cache[db] = info
    return info


def _sale_extra_cols(dim):
    """Danh sách cột phụ THỰC SỰ có trong SALE_VIEW (theo introspect)."""
    return [c for c in SALE_EXTRA_COLUMNS if c.upper() in dim["cols"]]


def _sale_select_list(need_join, extra_cols):
    base = ", ".join(f"S.{c}" for c in (SALE_BASE_COLUMNS + extra_cols))
    if need_join:
        return base + ", O.ORGANIZATION_NAME AS ORGANIZATION_NAME, E.EXPENSE_NAME AS EXPENSE_NAME"
    return base


@app.route("/api/sale")
@with_db_lock
def get_sale():
    """Danh sách chứng từ bán hàng lấy từ dbo.SALE_VIEW (mức dòng hàng)."""
    try:
        page      = int(request.args.get("page",     1))
        page_size = int(request.args.get("page_size", 100))
        export_all = request.args.get("export_all") == "1"
        known_total = request.args.get("known_total")
        known_sums  = request.args.get("known_sums")
        skip_count  = page > 1 and known_total is not None and known_sums is not None and not export_all

        where_sql, params = _build_sale_where(request.args)
        order_by_sql = _resolve_order_by(request.args, SALE_SORT_WHITELIST, "S.TRAN_DATE DESC, S.TRAN_NO")

        # Fast path: bỏ JOIN DM nếu không search/sort theo tên (map tên ở Python).
        need_join   = _sale_needs_join(request.args)
        join_sql    = SALE_JOIN_SQL if need_join else SALE_FROM_ONLY
        dim         = _sale_dim_info()
        extra_cols  = _sale_extra_cols(dim)
        select_list = _sale_select_list(need_join, extra_cols)

        conn   = get_connection()
        cursor = conn.cursor()

        SUM_SQL = """
            SUM(ISNULL(S.QUANTITY,0))        AS S_QUANTITY,
            SUM(ISNULL(S.AMOUNT,0))          AS S_AMOUNT,
            SUM(ISNULL(S.DISCOUNT_AMOUNT,0)) AS S_DISCOUNT,
            SUM(ISNULL(S.VAT_TAX_AMOUNT,0))  AS S_VAT_TAX,
            SUM(ISNULL(S.TOTAL_AMOUNT,0))    AS S_TOTAL,
            SUM(ISNULL(S.COG_AMOUNT,0))      AS S_COG
        """

        if export_all:
            sql = f"SELECT {select_list} {join_sql} WHERE {where_sql} ORDER BY {order_by_sql} OPTION (RECOMPILE)"
            cursor.execute(sql, params)
            columns  = [c[0] for c in cursor.description]
            raw_rows = cursor.fetchall()
            total_rows = len(raw_rows)
            qi = {c: idx for idx, c in enumerate(columns)}
            summary = {"quantity": 0, "amount": 0, "discount": 0, "vat_tax": 0, "total": 0, "cog": 0}
            for r in raw_rows:
                summary["quantity"] += float(r[qi.get("QUANTITY")]        or 0) if "QUANTITY"        in qi else 0
                summary["amount"]   += float(r[qi.get("AMOUNT")]          or 0) if "AMOUNT"          in qi else 0
                summary["discount"] += float(r[qi.get("DISCOUNT_AMOUNT")] or 0) if "DISCOUNT_AMOUNT" in qi else 0
                summary["vat_tax"]  += float(r[qi.get("VAT_TAX_AMOUNT")]  or 0) if "VAT_TAX_AMOUNT"  in qi else 0
                summary["total"]    += float(r[qi.get("TOTAL_AMOUNT")]    or 0) if "TOTAL_AMOUNT"    in qi else 0
                summary["cog"]      += float(r[qi.get("COG_AMOUNT")]      or 0) if "COG_AMOUNT"      in qi else 0
        else:
            if skip_count:
                import json as _json
                total_rows = int(known_total)
                try:    summary = _json.loads(known_sums)
                except: summary = {"quantity":0,"amount":0,"discount":0,"vat_tax":0,"total":0,"cog":0}
            else:
                cursor.execute(f"SELECT COUNT(*), {SUM_SQL} {join_sql} WHERE {where_sql} OPTION (RECOMPILE)", params)
                row = cursor.fetchone()
                total_rows = row[0] or 0
                summary = {
                    "quantity": float(row[1] or 0),
                    "amount":   float(row[2] or 0),
                    "discount": float(row[3] or 0),
                    "vat_tax":  float(row[4] or 0),
                    "total":    float(row[5] or 0),
                    "cog":      float(row[6] or 0),
                }

            offset = (page - 1) * page_size
            sql = f"""
                SELECT * FROM (
                    SELECT {select_list},
                           ROW_NUMBER() OVER (ORDER BY {order_by_sql}) AS RowNum
                    {join_sql}
                    WHERE {where_sql}
                ) AS RowConstrainedResult
                WHERE RowNum > ? AND RowNum <= ?
                OPTION (RECOMPILE)
            """
            cursor.execute(sql, params + [offset, offset + page_size])
            columns  = [c[0] for c in cursor.description]
            raw_rows = cursor.fetchall()

        db_name = (_db_cfg() or {}).get('database', 'N/A')
        meta = _meta_cache.get(db_name) or {}
        tran_map = { (it.get('id') or '').strip(): it.get('name') or '' for it in meta.get('tran_ids', []) }
        org_map, exp_map, wh_map, unit_map = _sale_name_maps()

        rows = []
        for raw in raw_rows:
            r = dict(zip(columns, raw))
            if 'TRAN_NAME' not in r:
                r['TRAN_NAME'] = tran_map.get((str(r.get('TRAN_ID') or '')).strip(), '')
            if not need_join:   # tên đơn vị/MCP map từ meta thay cho JOIN
                r['ORGANIZATION_NAME'] = org_map.get((str(r.get('ORGANIZATION_ID') or '')).strip(), '')
                r['EXPENSE_NAME']      = exp_map.get((str(r.get('EXPENSE_ID') or '')).strip(), '')
            # Tên kho + tên ĐVT luôn map từ meta (không có trong SALE_VIEW)
            r['WAREHOUSE_NAME'] = wh_map.get((str(r.get('WAREHOUSE_ID') or '')).strip(), '')
            r['UNIT_NAME']      = unit_map.get((str(r.get('UNIT_ID') or '')).strip(), '')
            # Tên HTTT + tên nguồn đơn (extra_2) map từ DM_PAYMENT_METHOD / DM_EXTRA_2
            r['PAYMENT_METHOD_NAME'] = dim["pay"].get((str(r.get('PAYMENT_METHOD_ID') or '')).strip(), '')
            r['EXTRA_NAME_2']        = dim["extra2"].get((str(r.get('EXTRA_ID_2') or '')).strip(), '')
            for dk in SALE_DATE_COLS:
                v = r.get(dk)
                if isinstance(v, (date, datetime)):
                    r[dk] = v.strftime("%d/%m/%Y")
            for nk in SALE_NUM_COLS:
                v = r.get(nk)
                if v is not None:
                    try: r[nk] = float(v)
                    except: pass
            rows.append(r)

        return jsonify({
            "status": "ok",
            "data": rows,
            "pagination": {
                "total_rows":  total_rows,
                "total_pages": max(1, (total_rows + page_size - 1) // page_size),
                "page": page if not export_all else 1
            },
            "summary": summary
        })
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


SALE_CSV_COLS = [
    ("ORGANIZATION_ID","Mã đơn vị"), ("ORGANIZATION_NAME","Tên đơn vị"),
    ("TRAN_ID","Mã chứng từ"), ("TRAN_NO","Số chứng từ"), ("TRAN_DATE","Ngày chứng từ"),
    ("VAT_TRAN_NO","Số hóa đơn"), ("VAT_TRAN_DATE","Ngày hóa đơn"), ("VAT_TRAN_SERIE","Ký hiệu HĐ"),
    ("PR_DETAIL_ID","Mã đối tượng"), ("PR_DETAIL_NAME","Tên đối tượng"),
    ("CONTACT_PERSON","Người liên hệ"), ("ADDRESS","Địa chỉ"),
    ("TAX_FILE_NUMBER","Mã số thuế"), ("PHONE","Điện thoại"),
    ("WAREHOUSE_ID","Mã kho"), ("WAREHOUSE_NAME","Tên kho"), ("EMPLOYEE_ID","Mã NV"),
    ("ITEM_ID","Mã hàng hóa"), ("ITEM_NAME","Tên hàng hóa"),
    ("DESCRIPTION","Diễn giải"), ("UNIT_ID","ĐVT"), ("UNIT_NAME","Tên đơn vị tính"),
    ("QUANTITY","Số lượng"), ("UNIT_PRICE","Đơn giá"), ("AMOUNT","Thành tiền"),
    ("DISCOUNT_AMOUNT","Giảm giá"), ("VAT_TAX_RATE","Thuế suất"), ("VAT_TAX_AMOUNT","Tiền thuế VAT"),
    ("TOTAL_AMOUNT","Tổng thanh toán"), ("COG_AMOUNT","Giá vốn"),
    ("ACCOUNT_ID","Tài khoản"), ("ACCOUNT_ID_PR","Tài khoản công nợ"), ("ACCOUNT_ID_COST","TK kho"), ("ACCOUNT_ID_INCOME","TK doanh thu"), ("ACCOUNT_ID_VAT","TK thuế"),
    ("EXPENSE_ID","Mã MCP"), ("EXPENSE_NAME","Tên MCP"),
    ("JOB_ID","Mã công việc"), ("JOB_NAME","Tên công việc"),
    ("IS_RETURN","Hàng trả"), ("STATUS","Trạng thái"),
    ("PAYMENT_METHOD_ID","Mã HTTT"), ("PAYMENT_METHOD_NAME","Hình thức thanh toán"),
    ("EXTRA_ID_2","Mã nguồn đơn"), ("EXTRA_NAME_2","Nguồn đơn"),
    ("INCOME_AMOUNT","Doanh thu"), ("VAT_INCOME_AMOUNT","Thuế doanh thu"),
    ("COMMENTS","Ghi chú"),
]


@app.route("/api/sale/count")
@with_db_lock
def get_sale_count():
    try:
        where_sql, params = _build_sale_where(request.args)
        join_sql = SALE_JOIN_SQL if _sale_needs_join(request.args) else SALE_FROM_ONLY
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) {join_sql} WHERE {where_sql} OPTION (RECOMPILE)", params)
        total = cursor.fetchone()[0] or 0
        return jsonify({"status": "ok", "total": int(total)})
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


@app.route("/api/sale/stream_csv", methods=["POST", "GET"])
def get_sale_stream_csv():
    try:
        args = request.args
        total_estimate = int(args.get("total", 0) or 0)
        where_sql, params = _build_sale_where(args)
        order_by_sql = _resolve_order_by(args, SALE_SORT_WHITELIST, "S.TRAN_DATE DESC, S.TRAN_NO")
        need_join = _sale_needs_join(args)
        org_map, exp_map, wh_map, unit_map = _sale_name_maps()
        dim = _sale_dim_info()
        extra_cols = _sale_extra_cols(dim)
        join_from = SALE_JOIN_SQL if need_join else SALE_FROM_ONLY
        sql = f"SELECT {_sale_select_list(need_join, extra_cols)} {join_from} WHERE {where_sql} ORDER BY {order_by_sql} OPTION (RECOMPILE)"

        def transform(raw, sql_cols):
            d = dict(zip(sql_cols, raw))
            if not need_join:
                d['ORGANIZATION_NAME'] = org_map.get((str(d.get('ORGANIZATION_ID') or '')).strip(), '')
                d['EXPENSE_NAME']      = exp_map.get((str(d.get('EXPENSE_ID') or '')).strip(), '')
            d['WAREHOUSE_NAME'] = wh_map.get((str(d.get('WAREHOUSE_ID') or '')).strip(), '')
            d['UNIT_NAME']      = unit_map.get((str(d.get('UNIT_ID') or '')).strip(), '')
            d['PAYMENT_METHOD_NAME'] = dim["pay"].get((str(d.get('PAYMENT_METHOD_ID') or '')).strip(), '')
            d['EXTRA_NAME_2']        = dim["extra2"].get((str(d.get('EXTRA_ID_2') or '')).strip(), '')
            return [d.get(key) for key, _ in SALE_CSV_COLS]

        headers = [label for _, label in SALE_CSV_COLS]
        fname   = f"ChungTuBanHang_{args.get('from_date','').replace('/','')}-{args.get('to_date','').replace('/','')}.{args.get('format', 'csv')}"
        job_id  = _start_export_job(fname, headers, sql, params, transform, total_estimate)
        return jsonify({"status": "ok", "job_id": job_id, "filename": fname})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
# DANH SÁCH CHỨNG TỪ TIỀN — query BẢNG GỐC VOUCHER ⋈ VOUCHER_DETAIL (alias H/D),
# map tên đối tượng + ngân hàng từ DM_PR_DETAIL ở Python.
# (KHÔNG dùng VOUCHER_VIEW: sort qua 2 join DM_PR_DETAIL trên view = ~390s cho 10k dòng;
#  query base + OFFSET/FETCH = ~1.7s.)
# ============================================================
VOUCHER_H_COLS = ["ORGANIZATION_ID", "TRAN_ID", "TRAN_NO", "TRAN_DATE", "CONTACT_PERSON", "ADDRESS", "STATUS"]
VOUCHER_D_COLS = ["ACCOUNT_ID_DEBIT", "ACCOUNT_ID_CREDIT", "DESCRIPTION", "AMOUNT",
                  "PR_DETAIL_ID_DEBIT", "PR_DETAIL_ID_CREDIT", "EXPENSE_ID_DEBIT", "EXPENSE_ID_CREDIT",
                  "JOB_ID_DEBIT", "JOB_ID_CREDIT", "REFERENCE_NO", "EMPLOYEE_ID", "CURRENCY_ID"]
VOUCHER_SELECT = (", ".join(f"H.{c}" for c in VOUCHER_H_COLS) + ", " + ", ".join(f"D.{c}" for c in VOUCHER_D_COLS))
VOUCHER_FROM   = ("FROM dbo.VOUCHER H WITH (NOLOCK) "
                  "INNER JOIN dbo.VOUCHER_DETAIL D WITH (NOLOCK) ON H.PR_KEY = D.FR_KEY")
VOUCHER_SORT_WHITELIST = {
    "ORGANIZATION_ID": "H.ORGANIZATION_ID", "TRAN_ID": "H.TRAN_ID", "TRAN_NO": "H.TRAN_NO",
    "TRAN_DATE": "H.TRAN_DATE", "STATUS": "H.STATUS", "CONTACT_PERSON": "H.CONTACT_PERSON",
    "ACCOUNT_ID_DEBIT": "D.ACCOUNT_ID_DEBIT", "ACCOUNT_ID_CREDIT": "D.ACCOUNT_ID_CREDIT",
    "AMOUNT": "D.AMOUNT", "DESCRIPTION": "D.DESCRIPTION", "EMPLOYEE_ID": "D.EMPLOYEE_ID",
    "REFERENCE_NO": "D.REFERENCE_NO",
}
VOUCHER_NUM_COLS  = ("AMOUNT",)
VOUCHER_DATE_COLS = ("TRAN_DATE",)


def _build_voucher_where(request_args):
    """WHERE + params cho VOUCHER (alias H) ⋈ VOUCHER_DETAIL (alias D)."""
    f_date = request_args.get("from_date", "01/01/2026")
    t_date = request_args.get("to_date",  "31/12/2026")
    from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
    to_dt   = datetime.strptime(t_date, "%d/%m/%Y").date()
    clauses = ["H.TRAN_DATE >= ?", "H.TRAN_DATE <= ?"]
    params  = [from_dt.strftime("%Y%m%d"), to_dt.strftime("%Y%m%d")]

    for field, arg in [("H.TRAN_ID", "tran_ids"), ("H.ORGANIZATION_ID", "org_ids")]:
        raw = request_args.get(arg, "")
        vals = [v for v in raw.split(",") if v]
        if arg == "org_ids":
            # Lọc đơn vị LUÔN đi qua _org_filter_sql — nơi DUY NHẤT ép quyền đơn vị theo tài
            # khoản (chọn gì cũng bị giao với danh sách được phép). Không chọn ⇒ mặc định loại
            # đơn vị ngoài cây '00', hoặc = đúng đơn vị được phép nếu tài khoản bị giới hạn.
            _oc, _op = _org_filter_sql(vals, field)
            if _oc:
                clauses.append(_oc)
                params.extend(_op)
        elif vals:
            clauses.append(f"{field} IN ({','.join(['?']*len(vals))})")
            params.extend(vals)

    for arg, field_debit, field_credit in [
        ("acc_ids", "D.ACCOUNT_ID_DEBIT", "D.ACCOUNT_ID_CREDIT"),
        ("pr_detail_ids", "D.PR_DETAIL_ID_DEBIT", "D.PR_DETAIL_ID_CREDIT"),
        ("expense_ids", "D.EXPENSE_ID_DEBIT", "D.EXPENSE_ID_CREDIT"),
        ("job_ids", "D.JOB_ID_DEBIT", "D.JOB_ID_CREDIT"),
    ]:
        raw = request_args.get(arg, "")
        vals = [v for v in raw.split(",") if v]
        if vals:
            if arg == "acc_ids":
                # For acc_ids, we do a LIKE search for each value on both DEBIT and CREDIT
                clauses.append("(" + " OR ".join(f"{field_debit} LIKE ? OR {field_credit} LIKE ?" for _ in vals) + ")")
                for v in vals:
                    params.extend([f"{v}%", f"{v}%"])
            else:
                # For others, we do an IN search on both DEBIT and CREDIT
                qs = ','.join(['?']*len(vals))
                clauses.append(f"({field_debit} IN ({qs}) OR {field_credit} IN ({qs}))")
                params.extend(vals)
                params.extend(vals)

    for field, arg in [
        ("H.TRAN_NO", "tran_no"), ("H.TRAN_ID", "s_tran_id"), ("H.ORGANIZATION_ID", "s_org_id"),
        ("D.ACCOUNT_ID_DEBIT", "s_acc_debit"), ("D.ACCOUNT_ID_CREDIT", "s_acc_credit"),
        ("D.EMPLOYEE_ID", "s_emp_id"), ("D.REFERENCE_NO", "s_ref"),
        ("D.PR_DETAIL_ID_DEBIT", "s_pr_id_debit"), ("D.PR_DETAIL_ID_CREDIT", "s_pr_id_credit"),
        ("D.EXPENSE_ID_DEBIT", "s_exp_debit"), ("D.EXPENSE_ID_CREDIT", "s_exp_credit"),
        ("D.JOB_ID_DEBIT", "s_job_debit"), ("D.JOB_ID_CREDIT", "s_job_credit"),
        ("D.CURRENCY_ID", "s_currency"),
    ]:
        val = request_args.get(arg, "").strip()
        if val:
            clauses.append(f"{field} LIKE ?"); params.append(f"{val}%")

    for field, arg in [("D.DESCRIPTION", "s_desc"), ("H.CONTACT_PERSON", "s_contact"), ("H.ADDRESS", "s_address")]:
        val = request_args.get(arg, "").strip()
        if val:
            clauses.append(f"{field} LIKE ?"); params.append(f"%{val}%")

    return " AND ".join(clauses), params


def _voucher_prdetail_map(cursor):
    """PR_DETAIL_ID -> (TÊN, BANK_NAME, BANK_ACCOUNT) từ DM_PR_DETAIL (~945 dòng, tức thì)."""
    try:
        cursor.execute("SELECT PR_DETAIL_ID, PR_DETAIL_NAME, BANK_NAME, BANK_ACCOUNT FROM dbo.DM_PR_DETAIL WITH (NOLOCK)")
        return {(r[0] or "").strip(): ((r[1] or ""), (r[2] or ""), (r[3] or "")) for r in cursor.fetchall()}
    except Exception:
        return {}


def _voucher_enrich(rows_dicts, cursor):
    """Bổ sung tên đơn vị / tên chứng từ / tên+bank đối tượng Nợ/Có."""
    db_name = (_db_cfg() or {}).get('database', 'N/A')
    meta = _meta_cache.get(db_name) or {}
    org_map  = {(it.get('id') or '').strip(): it.get('name') or '' for it in meta.get('orgs', [])}
    tran_map = {(it.get('id') or '').strip(): it.get('name') or '' for it in meta.get('tran_ids', [])}
    pr_map   = _voucher_prdetail_map(cursor)
    for r in rows_dicts:
        r['ORGANIZATION_NAME'] = org_map.get((str(r.get('ORGANIZATION_ID') or '')).strip(), '')
        r['TRAN_NAME']         = tran_map.get((str(r.get('TRAN_ID') or '')).strip(), '')
        pd = pr_map.get((str(r.get('PR_DETAIL_ID_DEBIT') or '')).strip())
        r['PR_DETAIL_NAME_DEBIT'], r['BANK_NAME_DEBIT'], r['BANK_ACCOUNT_DEBIT'] = pd if pd else ('', '', '')
        pc = pr_map.get((str(r.get('PR_DETAIL_ID_CREDIT') or '')).strip())
        r['PR_DETAIL_NAME_CREDIT'], r['BANK_NAME_CREDIT'], r['BANK_ACCOUNT_CREDIT'] = pc if pc else ('', '', '')
        for dk in VOUCHER_DATE_COLS:
            v = r.get(dk)
            if isinstance(v, (date, datetime)): r[dk] = v.strftime("%d/%m/%Y")
        for nk in VOUCHER_NUM_COLS:
            v = r.get(nk)
            if v is not None:
                try: r[nk] = float(v)
                except: pass
    return rows_dicts



@app.route("/api/voucher")
@with_db_lock
def get_voucher():
    """Danh sách chứng từ tiền/kế toán (phiếu thu/chi, báo nợ/có...) từ VOUCHER ⋈ VOUCHER_DETAIL."""
    try:
        page      = int(request.args.get("page",     1))
        page_size = int(request.args.get("page_size", 100))
        export_all = request.args.get("export_all") == "1"
        known_total = request.args.get("known_total")
        known_sums  = request.args.get("known_sums")
        skip_count  = page > 1 and known_total is not None and known_sums is not None and not export_all

        where_sql, params = _build_voucher_where(request.args)
        order_by_sql = _resolve_order_by(request.args, VOUCHER_SORT_WHITELIST, "H.TRAN_DATE DESC, H.TRAN_NO")

        cursor = get_connection().cursor()

        if export_all:
            cursor.execute(f"SELECT {VOUCHER_SELECT} {VOUCHER_FROM} WHERE {where_sql} ORDER BY {order_by_sql}", params)
            columns  = [c[0] for c in cursor.description]
            raw_rows = cursor.fetchall()
            total_rows = len(raw_rows)
            qi = {c: idx for idx, c in enumerate(columns)}
            summary = {"amount": sum(float(r[qi["AMOUNT"]] or 0) for r in raw_rows) if "AMOUNT" in qi else 0}
        else:
            if skip_count:
                import json as _json
                total_rows = int(known_total)
                try:    summary = _json.loads(known_sums)
                except: summary = {"amount": 0}
            else:
                cursor.execute(f"SELECT COUNT(*), SUM(ISNULL(D.AMOUNT,0)) {VOUCHER_FROM} WHERE {where_sql}", params)
                row = cursor.fetchone()
                total_rows = row[0] or 0
                summary = {"amount": float(row[1] or 0)}

            offset = (page - 1) * page_size
            # Lọc/sắp chỉ đụng cột của VOUCHER (H) ⇒ chọn ĐÚNG các chứng từ của trang TRƯỚC,
            # rồi mới join VOUCHER_DETAIL. Bản cũ join trọn 148k dòng của tháng rồi mới sort
            # (VOUCHER_DETAIL không có index trên FR_KEY, VOUCHER không có index trên TRAN_DATE)
            # → đo tháng 7/2026: 22,4 giây cho 100 dòng. Lọc header trước còn 0,36 giây.
            columns = raw_rows = None
            if "D." not in where_sql and order_by_sql.startswith("H."):
                cursor.execute(f"""
                    WITH HP AS (
                        SELECT TOP (?) H.PR_KEY, ROW_NUMBER() OVER (ORDER BY {order_by_sql}) AS HRN
                        FROM dbo.VOUCHER H WITH (NOLOCK)
                        WHERE {where_sql}
                        ORDER BY {order_by_sql}
                    )
                    SELECT * FROM (
                        SELECT {VOUCHER_SELECT}, ROW_NUMBER() OVER (ORDER BY HP.HRN, D.PR_KEY) AS RN
                        FROM HP
                        JOIN dbo.VOUCHER        H WITH (NOLOCK) ON H.PR_KEY = HP.PR_KEY
                        JOIN dbo.VOUCHER_DETAIL D WITH (NOLOCK) ON D.FR_KEY = HP.PR_KEY
                    ) X WHERE RN > ? AND RN <= ?
                """, [offset + page_size] + params + [offset, offset + page_size])
                cand_cols = [c[0] for c in cursor.description][:-1]   # bỏ cột RN kỹ thuật
                cand_rows = cursor.fetchall()
                # Mỗi chứng từ có ít nhất 1 dòng chi tiết ⇒ N chứng từ đầu nuôi đủ N dòng đầu.
                # DB có chứng từ rỗng (INNER JOIN loại đi) thì lấy hụt → quay về query đầy đủ.
                if len(cand_rows) >= max(0, min(total_rows, offset + page_size) - offset):
                    columns, raw_rows = cand_cols, cand_rows
            if raw_rows is None:
                cursor.execute(
                    f"SELECT {VOUCHER_SELECT} {VOUCHER_FROM} WHERE {where_sql} ORDER BY {order_by_sql} "
                    f"OFFSET ? ROWS FETCH NEXT ? ROWS ONLY", params + [offset, page_size])
                columns  = [c[0] for c in cursor.description]
                raw_rows = cursor.fetchall()

        rows = _voucher_enrich([dict(zip(columns, raw)) for raw in raw_rows], cursor)

        return jsonify({
            "status": "ok",
            "data": rows,
            "pagination": {
                "total_rows":  total_rows,
                "total_pages": max(1, (total_rows + page_size - 1) // page_size),
                "page": page if not export_all else 1
            },
            "summary": summary
        })
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


VOUCHER_CSV_COLS = [
    ("ORGANIZATION_ID","Mã đơn vị"), ("ORGANIZATION_NAME","Tên đơn vị"),
    ("TRAN_ID","Mã chứng từ"), ("TRAN_NAME","Tên chứng từ"), ("TRAN_NO","Số chứng từ"), ("TRAN_DATE","Ngày chứng từ"),
    ("ACCOUNT_ID_DEBIT","Tài khoản"), ("ACCOUNT_ID_CREDIT","Tài khoản đối ứng"),
    ("DESCRIPTION","Diễn giải"), ("AMOUNT","Số tiền"),
    ("PR_DETAIL_ID_DEBIT","Mã Đối tượng"), ("PR_DETAIL_NAME_DEBIT","Đối tượng"),
    ("PR_DETAIL_ID_CREDIT","Mã ĐT đối ứng"), ("PR_DETAIL_NAME_CREDIT","Đối tượng đối ứng"),
    ("EXPENSE_ID_DEBIT","Mục chi phí"), ("EXPENSE_ID_CREDIT","MCP đối ứng"),
    ("JOB_ID_DEBIT","Công việc"), ("JOB_ID_CREDIT","CV đối ứng"),
    ("BANK_NAME_DEBIT","Ngân hàng"), ("BANK_ACCOUNT_DEBIT","TK Ngân hàng"),
    ("BANK_NAME_CREDIT","Ngân hàng đối ứng"), ("BANK_ACCOUNT_CREDIT","TKNH đối ứng"),
    ("CONTACT_PERSON","Người nộp/nhận"), ("ADDRESS","Địa chỉ"), ("REFERENCE_NO","Số tham chiếu"),
    ("EMPLOYEE_ID","Mã NV"), ("CURRENCY_ID","Tiền tệ"), ("STATUS","Trạng thái"),
]


@app.route("/api/voucher/count")
@with_db_lock
def get_voucher_count():
    try:
        where_sql, params = _build_voucher_where(request.args)
        cursor = get_connection().cursor()
        cursor.execute(f"SELECT COUNT(*) {VOUCHER_FROM} WHERE {where_sql}", params)
        total = cursor.fetchone()[0] or 0
        return jsonify({"status": "ok", "total": int(total)})
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


@app.route("/api/voucher/stream_csv", methods=["POST", "GET"])
def get_voucher_stream_csv():
    try:
        args = request.args
        total_estimate = int(args.get("total", 0) or 0)
        where_sql, params = _build_voucher_where(args)
        order_by_sql = _resolve_order_by(args, VOUCHER_SORT_WHITELIST, "H.TRAN_DATE DESC, H.TRAN_NO")
        sql = f"SELECT {VOUCHER_SELECT} {VOUCHER_FROM} WHERE {where_sql} ORDER BY {order_by_sql}"

        # Map tên/bank chuẩn bị sẵn (chạy 1 lần) để transform per-row khỏi query DB
        db_name = (_db_cfg() or {}).get('database', 'N/A')
        meta = _meta_cache.get(db_name) or {}
        org_map  = {(it.get('id') or '').strip(): it.get('name') or '' for it in meta.get('orgs', [])}
        tran_map = {(it.get('id') or '').strip(): it.get('name') or '' for it in meta.get('tran_ids', [])}
        pr_map   = _voucher_prdetail_map(get_connection().cursor())

        def transform(raw, sql_cols):
            d = dict(zip(sql_cols, raw))
            d['ORGANIZATION_NAME'] = org_map.get((str(d.get('ORGANIZATION_ID') or '')).strip(), '')
            d['TRAN_NAME']         = tran_map.get((str(d.get('TRAN_ID') or '')).strip(), '')
            pd = pr_map.get((str(d.get('PR_DETAIL_ID_DEBIT') or '')).strip()) or ('', '', '')
            d['PR_DETAIL_NAME_DEBIT'], d['BANK_NAME_DEBIT'], d['BANK_ACCOUNT_DEBIT'] = pd
            pc = pr_map.get((str(d.get('PR_DETAIL_ID_CREDIT') or '')).strip()) or ('', '', '')
            d['PR_DETAIL_NAME_CREDIT'], d['BANK_NAME_CREDIT'], d['BANK_ACCOUNT_CREDIT'] = pc
            return [d.get(key) for key, _ in VOUCHER_CSV_COLS]

        headers = [label for _, label in VOUCHER_CSV_COLS]
        fname   = f"ChungTuTien_{args.get('from_date','').replace('/','')}-{args.get('to_date','').replace('/','')}.{args.get('format', 'csv')}"
        job_id  = _start_export_job(fname, headers, sql, params, transform, total_estimate)
        return jsonify({"status": "ok", "job_id": job_id, "filename": fname})
    except Exception as e:
        # Route này KHÔNG có @with_db_lock nên không được tự thử lại → phải tự vứt connection
        # hỏng khỏi pool, nếu không lần bấm sau vẫn vớ đúng connection chết đó và lỗi tiếp.
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 500


@app.route("/api/ledger/export")
@with_db_lock
def get_ledger_export():
    """Trả toàn bộ ledger (không phân trang) cho xuất Excel — phải JOIN dimension."""
    try:
        where_sql, params, join_clauses, join_params = _build_where(request.args)

        BASE_COLS = """
            L.TRAN_DATE, L.TRAN_NO, L.TRAN_ID, L.DEBIT_CREDIT,
            L.ACCOUNT_ID, L.ACCOUNT_ID_CONTRA,
            L.PR_DETAIL_ID, L.DESCRIPTION, L.COMMENTS,
            L.AMOUNT, L.JOB_ID,
            L.ITEM_ID, L.PRODUCT_ID,
            L.EXPENSE_ID, L.ORGANIZATION_ID, L.BANK_ID, L.BANK_ID_CONTRA,
            L.EXPENSE_ID_CONTRA, L.PR_DETAIL_ID_CONTRA, L.JOB_ID_CONTRA, L.ITEM_ID_CONTRA,
            PD.PR_DETAIL_NAME, PD2.PR_DETAIL_NAME AS PR_DETAIL_NAME_CONTRA,
            E.EXPENSE_NAME, E2.EXPENSE_NAME AS EXPENSE_NAME_CONTRA,
            J.JOB_NAME, J2.JOB_NAME AS JOB_NAME_CONTRA,
            O.ORGANIZATION_NAME,
            I.ITEM_NAME, I2.ITEM_NAME AS ITEM_NAME_CONTRA,
            P.ITEM_NAME AS PRODUCT_NAME, B.BANK_NAME, B2.BANK_NAME AS BANK_NAME_CONTRA
        """
        joins = [
            "FROM dbo.LEDGER L WITH (NOLOCK)",
            "LEFT JOIN dbo.DM_PR_DETAIL   PD  WITH (NOLOCK) ON L.PR_DETAIL_ID       = PD.PR_DETAIL_ID",
            "LEFT JOIN dbo.DM_PR_DETAIL   PD2 WITH (NOLOCK) ON L.PR_DETAIL_ID_CONTRA= PD2.PR_DETAIL_ID",
            "LEFT JOIN dbo.DM_ITEM        I WITH (NOLOCK)   ON L.ITEM_ID            = I.ITEM_ID",
            "LEFT JOIN dbo.DM_ITEM        I2 WITH (NOLOCK)  ON L.ITEM_ID_CONTRA     = I2.ITEM_ID",
            "LEFT JOIN dbo.DM_ITEM        P WITH (NOLOCK)   ON L.PRODUCT_ID         = P.ITEM_ID",
            "LEFT JOIN dbo.DM_EXPENSE     E WITH (NOLOCK)   ON L.EXPENSE_ID         = E.EXPENSE_ID",
            "LEFT JOIN dbo.DM_EXPENSE     E2 WITH (NOLOCK)  ON L.EXPENSE_ID_CONTRA  = E2.EXPENSE_ID",
            "LEFT JOIN dbo.DM_JOB         J WITH (NOLOCK)   ON L.JOB_ID             = J.JOB_ID",
            "LEFT JOIN dbo.DM_JOB         J2 WITH (NOLOCK)  ON L.JOB_ID_CONTRA      = J2.JOB_ID",
            "LEFT JOIN dbo.DM_ORGANIZATION O WITH (NOLOCK)  ON L.ORGANIZATION_ID    = O.ORGANIZATION_ID",
            "LEFT JOIN dbo.DM_BANK        B WITH (NOLOCK)   ON L.BANK_ID            = B.BANK_ID",
            "LEFT JOIN dbo.DM_BANK        B2 WITH (NOLOCK)  ON L.BANK_ID_CONTRA     = B2.BANK_ID",
        ]
        JOIN_TABLES = " ".join(joins)
        join_filter = " AND ".join(join_clauses) if join_clauses else "1=1"

        sql = f"""
            SELECT {BASE_COLS}
            {JOIN_TABLES}
            WHERE {where_sql} AND {join_filter}
            ORDER BY L.TRAN_DATE DESC, L.TRAN_NO
        """

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params + join_params)
        columns = [c[0] for c in cursor.description]
        rows = []
        for raw in cursor.fetchall():
            r = dict(zip(columns, raw))
            if isinstance(r.get('TRAN_DATE'), (date, datetime)):
                r['TRAN_DATE'] = r['TRAN_DATE'].strftime("%d/%m/%Y")
            if r.get('AMOUNT') is not None:
                try: r['AMOUNT'] = float(r['AMOUNT'])
                except: pass
            rows.append(r)

        return jsonify({"status": "ok", "data": rows, "total_rows": len(rows)})
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


# ===== BC005 — BẢNG CÂN ĐỐI KẾ TOÁN (TT200, mẫu B01-DN) =====
def _map_account_to_cdkt(acc, bal):
    """Trả về list (code, value) — mã chỉ tiêu CDKT và giá trị đóng góp.
    bal = SUM(DEB) - SUM(CRD) của ACCOUNT_ID.
    Các tài khoản có thể đảo dấu (131, 331, 138, 334, 338...) sẽ vào chỉ tiêu Tài sản
    nếu dư Nợ, vào chỉ tiêu Nguồn vốn nếu dư Có.
    """
    a = (acc or "").strip()
    if not a or bal == 0:
        return []
    a4 = a[:4]
    a3 = a[:3]
    out = []
    # Tiền — TK mẹ 111, 112, 113 (gồm tất cả TK con: 1111, 1121, 1131...)
    if a.startswith('11'):
        out.append(('111', bal))
    elif a4 == '1281':
        out.append(('112', bal))
    elif a4 in ('1282', '1288'):
        out.append(('123', bal))
    elif a3 == '121':
        out.append(('121', bal))
    elif a4 == '2291':
        out.append(('122', bal))  # âm (dư Có → bal âm)
    elif a.startswith('1311'):
        if bal >= 0: out.append(('131', bal))
        else:        out.append(('312', -bal))
    elif a.startswith('1312'):
        if bal >= 0: out.append(('211', bal))
        else:        out.append(('312', -bal))
    elif a3 == '331':
        if bal >= 0: out.append(('132', bal))
        else:        out.append(('311', -bal))
    elif a3 == '136':
        out.append(('133', bal))
    elif a4 == '1283':
        if bal >= 0: out.append(('135', bal))
        else:        out.append(('338', -bal))
    elif a.startswith('1385') or a.startswith('1388') or a.startswith('3388'):
        if bal >= 0: out.append(('136', bal))
        else:        out.append(('319', -bal))
    elif a.startswith('141') or a.startswith('2441'):
        out.append(('136', bal))
    elif a3 == '138':
        if bal >= 0: out.append(('139', bal)) # Thường 1381 vào 139
        else:        out.append(('319', -bal))
    elif a3 == '334':
        out.append(('314', -bal))
    elif a3 == '338':
        # Các khoản 338 khác ngoài 3388 (ví dụ BHXH)
        if bal >= 0: out.append(('136', bal)) 
        else:        out.append(('319', -bal))
    elif a4 == '2293':
        out.append(('137', bal))
    elif a3 in ('151', '152', '153', '154', '155', '156', '157', '158'):
        out.append(('141', bal))
    elif a4 == '2294':
        out.append(('149', bal))
    elif a3 == '242':
        out.append(('151', bal))
    elif a3 == '133':
        out.append(('152', bal))
    elif a3 == '333':
        if bal >= 0: out.append(('153', bal))
        else:        out.append(('313', -bal))
    elif a3 == '171':
        if bal >= 0: out.append(('154', bal))
        else:        out.append(('324', -bal))
    # TSCĐ
    elif a3 == '211':
        out.append(('222', bal))
    elif a4 == '2141':
        out.append(('223', bal))  # bal âm
    elif a3 == '213':
        out.append(('228', bal))   # Nguyên giá TSCĐ vô hình (228), KHÔNG phải 227 (227 là nhóm = 228+229)
    elif a4 == '2143':
        out.append(('229', bal))   # Hao mòn TSCĐ vô hình (229)
    elif a3 == '244':
        out.append(('216', bal))   # Cầm cố, ký quỹ ký cược dài hạn → Phải thu dài hạn khác
    elif a3 == '217':
        out.append(('230', bal))
    elif a4 == '2147':
        out.append(('232', bal))
    elif a3 == '241':
        out.append(('242', bal))
    elif a3 == '221':
        out.append(('251', bal))
    elif a3 == '222':
        out.append(('252', bal))
    elif a4 == '2292':
        out.append(('254', bal))
    elif a3 == '228':
        out.append(('255', bal))
    # Nợ phải trả
    elif a.startswith('3362') or a.startswith('3363') or a.startswith('3368'):
        out.append(('316', -bal))
    elif a3 == '335':
        out.append(('315', -bal))
    elif a3 == '352':
        out.append(('321', -bal))
    elif a3 in ('353',):
        out.append(('322', -bal))
    elif a3 == '344':
        out.append(('323', -bal))
    elif a3 == '343':
        out.append(('336', -bal))
    elif a3 == '341':
        # Vay & nợ thuê tài chính — gộp dài hạn
        out.append(('338', -bal))
    elif a3 == '347':
        out.append(('341', -bal))
    elif a3 == '356':
        out.append(('343', -bal))
    # Vốn chủ sở hữu
    elif a4 == '4111':
        out.append(('411A', -bal))
        out.append(('411', -bal))
    elif a4 == '4112':
        out.append(('412', -bal))
    elif a4 == '4113':
        out.append(('411B', -bal))
        out.append(('411', -bal))
    elif a3 == '412':
        out.append(('416', -bal))
    elif a3 == '413':
        out.append(('417', -bal))
    elif a3 == '414':
        out.append(('418', -bal))
    elif a3 == '417':
        out.append(('419', -bal))
    elif a3 == '418':
        out.append(('420', -bal))
    elif a3 == '419':
        out.append(('415', bal))   # cổ phiếu quỹ ghi Nợ
    elif a.startswith('421'):
        out.append(('421', -bal))
        out.append(('421A', -bal))
    elif a3 == '441':
        out.append(('422', -bal))
    elif a3 == '461':
        out.append(('431', -bal))
    elif a3 == '466':
        out.append(('432', -bal))
    return out


def _calc_cdkt_balances(rows):
    """rows: list (account_id, balance). Trả dict {code: value}."""
    result = {}
    for acc, bal in rows:
        for code, val in _map_account_to_cdkt(acc, bal):
            result[code] = result.get(code, 0.0) + float(val)

    # Tổng hợp các chỉ tiêu nhóm
    def s(*codes):
        return sum(result.get(c, 0.0) for c in codes)

    # Tài sản ngắn hạn
    result['110'] = s('111', '112')
    result['120'] = s('121', '122', '123')
    result['130'] = s('131', '132', '133', '134', '135', '136', '137', '139')
    result['140'] = s('141', '149')
    result['150'] = s('151', '152', '153', '154', '155')
    result['100'] = s('110', '120', '130', '140', '150')
    # Tài sản dài hạn
    result['210'] = s('211', '212', '213', '214', '215', '216', '217')
    result['221'] = s('222', '223')
    result['224'] = s('225', '226')
    result['227'] = s('228', '229')
    result['220'] = s('221', '224', '227')
    result['230'] = s('231', '232')  # 231 thường rỗng, dùng raw 230 thay thế
    if not result.get('230'):
        result['230'] = result.get('230', 0.0)
    result['240'] = s('241', '242')
    result['250'] = s('251', '252', '253', '254', '255')
    result['260'] = s('261', '262', '263', '268')
    result['200'] = s('210', '220', '230', '240', '250', '260')
    # Tổng tài sản
    result['270'] = s('100', '200')
    # Nợ ngắn hạn
    result['310'] = s('311', '312', '313', '314', '315', '316', '317', '318', '319', '320', '321', '322', '323', '324')
    # Nợ dài hạn
    result['330'] = s('331', '332', '333', '334', '335', '336', '337', '338', '339', '340', '341', '342', '343')
    result['300'] = s('310', '330')
    # Vốn CSH
    if not result.get('411'):
        result['411'] = s('411A', '411B')
    result['410'] = s('411', '412', '413', '414', '415', '416', '417', '418', '419', '420', '421', '422')
    result['430'] = s('431', '432')
    result['400'] = s('410', '430')
    result['440'] = s('300', '400')
    return result


# Mốc luỹ kế = (toán tử, ngày 'YYYYMMDD'). Toán tử giữ NGUYÊN như bản cũ ('<=' / '<') —
# TRAN_DATE là smalldatetime nên đổi '<= 31/07' thành '< 01/08' là ĐỔI SỐ LIỆU, không được làm.
_CUT_INVERSE = {'<': '>=', '<=': '>'}

# BC005 và BC011 hỏi CÙNG bộ mốc cho cùng kỳ, mà mỗi lượt quét tốn ~45 giây — xem lần lượt
# hai báo cáo là ngồi chờ hai lần y hệt nhau. Giữ lại kết quả mới nhất, TTL ngắn để kế toán
# vừa sửa bút toán xong, mở lại báo cáo trong vài phút vẫn thấy số mới.
_ledger_cum_cache = {}          # {key: (thời điểm, kết quả)} — chỉ giữ 1 entry
_LEDGER_CUM_TTL_SEC = 180


def _ledger_cum_by_cutoffs(cur, first_day_of_year, cutoffs, org_ids):
    """Số dư luỹ kế {(acc, pr, org): BAL} tại NHIỀU mốc thời gian, chỉ quét LEDGER MỘT lượt.

    Bản cũ gọi một run_ledger() riêng cho từng mốc, mỗi lần GROUP BY toàn bộ LEDGER từ 01/01
    tới mốc đó ⇒ 4 mốc là quét ~4 lần số dòng của kỳ. Đo trên IACC_CHULONG tháng 7/2026
    (17,3 triệu dòng trong kỳ): BC005 mất 206 giây, BC011 mất 208 giây — và nút thắt là CPU
    của GROUP BY chứ không phải đọc đĩa, nên thêm index KHÔNG cứu được, phải bớt lượt quét.

    Các mốc đều là "từ đầu năm tới X" nên lồng nhau ⇒ chỉ cần quét mỗi LÁT CẮT RỜI đúng một
    lần rồi cộng dồn (prefix sum). Tổng số dòng quét bằng đúng một lượt kỳ; số từng mốc
    giống hệt bản cũ.
    """
    _lc, _lp = _org_filter_sql(org_ids, "L.ORGANIZATION_ID")
    # '< d' chặt hơn '<= d' nên phải đứng trước khi trùng ngày, để các lát luôn lồng nhau
    uniq = sorted(set(cutoffs), key=lambda c: (c[1], 0 if c[0] == '<' else 1))

    ck = ((_db_cfg() or {}).get('database', ''),
          first_day_of_year, tuple(uniq), tuple(org_ids or ()))
    hit = _ledger_cum_cache.get(ck)
    if hit is not None and (time.time() - hit[0]) < _LEDGER_CUM_TTL_SEC:
        return hit[1]

    result, running, prev = {}, {}, None
    for cut in uniq:
        where  = ["L.TRAN_DATE >= ?", f"L.TRAN_DATE {cut[0]} ?"]
        params = [first_day_of_year, cut[1]]
        if prev is not None:
            # Lát cắt RỜI: cắt bỏ phần đã cộng ở mốc trước
            where.append(f"L.TRAN_DATE {_CUT_INVERSE[prev[0]]} ?")
            params.append(prev[1])
        if _lc:
            where.append(_lc)
            params.extend(_lp)
        cur.execute(f"""
            SELECT L.ACCOUNT_ID, ISNULL(L.PR_DETAIL_ID, ''), ISNULL(L.ORGANIZATION_ID, ''),
                   SUM(CASE WHEN L.DEBIT_CREDIT='DEB' THEN L.AMOUNT WHEN L.DEBIT_CREDIT='CRD' THEN -L.AMOUNT ELSE 0 END) AS BAL
            FROM dbo.LEDGER L WITH (NOLOCK)
            WHERE {' AND '.join(where)}
            GROUP BY L.ACCOUNT_ID, ISNULL(L.PR_DETAIL_ID, ''), ISNULL(L.ORGANIZATION_ID, '')
        """, params)
        for r in cur.fetchall():
            k = ((r[0] or '').strip(), (r[1] or '').strip(), (r[2] or '').strip())
            running[k] = running.get(k, 0.0) + float(r[3] or 0)
        result[cut] = dict(running)   # snapshot luỹ kế tới mốc này
        prev = cut

    _ledger_cum_cache.clear()         # chỉ giữ kết quả mới nhất, tránh phình RAM
    _ledger_cum_cache[ck] = (time.time(), result)
    return result


def _cdkt_cutoffs(from_dt, to_dt):
    """4 mốc mà BC005/BC011 cần: cuối kỳ, trước đầu kỳ, cuối tháng trước, trước đầu tháng trước."""
    prev_m_end   = from_dt.replace(day=1) - timedelta(days=1)
    prev_m_start = prev_m_end.replace(day=1)
    return (('<=', to_dt.strftime("%Y%m%d")),
            ('<',  from_dt.strftime("%Y%m%d")),
            ('<=', prev_m_end.strftime("%Y%m%d")),
            ('<',  prev_m_start.strftime("%Y%m%d")))


def _compute_cdkt(from_dt, to_dt, org_ids):
    """Tính số dư các chỉ tiêu CĐKT (mã CDKT) cho kỳ — dùng chung cho BC005 & BC011.
    Trả (opening, closing): dict mã CDKT -> số dư. opening = đầu kỳ (trước from_dt),
    closing = cuối kỳ (đến to_dt). Có sẵn '421B' = biến động LN sau thuế trong kỳ."""
    if True:
        cur = get_connection().cursor()

        _bs_clause, org_params = _org_filter_sql(org_ids, "ORGANIZATION_ID")
        org_where = (" AND " + _bs_clause) if _bs_clause else ""

        # Thêm biến ngày đầu năm để tránh bị cộng dồn cả phát sinh các năm cũ
        first_day_of_year = date(from_dt.year, 1, 1).strftime("%Y%m%d")

        # 1) Số dư đầu năm từ BALANCE_VIEW (toàn bộ dòng đều là số dư đầu kỳ)
        # 1) Số dư đầu năm từ BALANCE_VIEW (toàn bộ dòng đều là số dư đầu kỳ)
        try:
            cur.execute("SELECT TOP 1 ORGANIZATION_ID FROM dbo.BALANCE_VIEW WITH (NOLOCK)")
            has_org_in_balance = True
        except Exception:
            has_org_in_balance = False

        if has_org_in_balance:
            q_open = f"""
                SELECT ACCOUNT_ID, ISNULL(PR_DETAIL_ID, ''), ISNULL(ORGANIZATION_ID, ''),
                       SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT WHEN DEBIT_CREDIT='CRD' THEN -AMOUNT ELSE 0 END) AS BAL
                FROM dbo.BALANCE_VIEW WITH (NOLOCK)
                WHERE TRAN_DATE = ? {org_where}
                GROUP BY ACCOUNT_ID, ISNULL(PR_DETAIL_ID, ''), ISNULL(ORGANIZATION_ID, '')
            """
            org_params_open = [first_day_of_year] + list(org_params)
        else:
            q_open = f"""
                SELECT ACCOUNT_ID, ISNULL(PR_DETAIL_ID, ''), '' AS ORGANIZATION_ID,
                       SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT WHEN DEBIT_CREDIT='CRD' THEN -AMOUNT ELSE 0 END) AS BAL
                FROM dbo.BALANCE_VIEW WITH (NOLOCK)
                WHERE TRAN_DATE = ?
                GROUP BY ACCOUNT_ID, ISNULL(PR_DETAIL_ID, '')
            """
            org_params_open = [first_day_of_year]

        cur.execute(q_open, org_params_open)
        opening_year = { ((r[0] or '').strip(), (r[1] or '').strip(), (r[2] or '').strip()): float(r[3] or 0) for r in cur.fetchall() }

        # 2) Phát sinh lũy kế đến từng mốc — MỘT lượt quét cho cả 4 mốc (xem _ledger_cum_by_cutoffs)
        cut_end, cut_start, cut_pm_end, cut_pm_start = _cdkt_cutoffs(from_dt, to_dt)
        _cum = _ledger_cum_by_cutoffs(cur, first_day_of_year,
                                      (cut_end, cut_start, cut_pm_end, cut_pm_start), org_ids)
        ledger_to_end   = _cum[cut_end]
        ledger_to_start = _cum[cut_start]

        # 3) Cộng dồn: số dư = đầu năm + phát sinh lũy kế
        all_keys = set(opening_year) | set(ledger_to_end) | set(ledger_to_start)
        this_rows_full = [(k[0], k[1], k[2], opening_year.get(k, 0.0) + ledger_to_end.get(k, 0.0)) for k in all_keys]
        prev_rows_full = [(k[0], k[1], k[2], opening_year.get(k, 0.0) + ledger_to_start.get(k, 0.0)) for k in all_keys]

        # Roll up to (ACCOUNT_ID, PR_DETAIL_ID) for standard CDKT
        this_acc_pr = {}
        for acc, pr, org, bal in this_rows_full:
            this_acc_pr[(acc, pr)] = this_acc_pr.get((acc, pr), 0.0) + bal
        prev_acc_pr = {}
        for acc, pr, org, bal in prev_rows_full:
            prev_acc_pr[(acc, pr)] = prev_acc_pr.get((acc, pr), 0.0) + bal

        this_rows = [(acc, bal) for (acc, pr), bal in this_acc_pr.items()]
        prev_rows = [(acc, bal) for (acc, pr), bal in prev_acc_pr.items()]

        closing = _calc_cdkt_balances(this_rows)   # Kỳ này
        opening = _calc_cdkt_balances(prev_rows)   # Kỳ trước

        # Tính toán 1311 và 1312
        target_orgs = {'42', '51', '36', '65', '18', '31'}
        def calc_sub_131(rows_full, acc_pr_bals):
            # Precompute (acc,pr) -> tổng bal của các đơn vị target → O(N) thay vì O(N^2)
            # (vòng lặp cũ quét toàn bộ rows_full cho MỖI nhóm 1311 → 200s+ trên DB lớn)
            org_bal_idx = {}
            for a, p, o, bal in rows_full:
                if o in target_orgs:
                    k = (a, p)
                    org_bal_idx[k] = org_bal_idx.get(k, 0.0) + bal
            val_1311 = 0.0
            for (acc, pr), total_bal in acc_pr_bals.items():
                if acc.startswith('1311') and total_bal >= 0:
                    val_1311 += org_bal_idx.get((acc, pr), 0.0)
            return val_1311

        closing['1311'] = calc_sub_131(this_rows_full, this_acc_pr)
        closing['1312'] = closing.get('131', 0.0) - closing['1311']

        opening['1311'] = calc_sub_131(prev_rows_full, prev_acc_pr)
        opening['1312'] = opening.get('131', 0.0) - opening['1311']

        # --- XỬ LÝ ĐẶC BIỆT DÒNG 421A, 421B ---
        closing['421A'] = opening.get('421A', 0.0)

        def get_movement_421(d_end, d_start):
            end_val = sum(v for (a, pr, org), v in d_end.items() if a.startswith('421'))
            start_val = sum(v for (a, pr, org), v in d_start.items() if a.startswith('421'))
            return -(end_val - start_val)

        closing['421B'] = get_movement_421(ledger_to_end, ledger_to_start)

        try:
            opening['421B'] = get_movement_421(_cum[cut_pm_end], _cum[cut_pm_start])
        except Exception:
            opening['421B'] = 0.0

        return opening, closing


@app.route("/api/balance_sheet")
@with_db_lock
def get_balance_sheet():
    """BC005 - Bảng Cân đối Kế toán (TT200, mẫu B01-DN).

    Số dư mỗi TK (BAL = SUM(DEB) - SUM(CRD)) tính theo công thức:
      Kỳ này  = (số dư đầu năm từ BALANCE_VIEW)
                + (phát sinh từ LEDGER_VIEW với TRAN_DATE <= to_date)
      Kỳ trước = (số dư đầu năm từ BALANCE_VIEW)
                + (phát sinh từ LEDGER_VIEW với TRAN_DATE < from_date)
    """
    try:
        f_date  = request.args.get("from_date")
        t_date  = request.args.get("to_date")
        org_ids = [v for v in request.args.get("org_ids", "").split(",") if v]

        from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
        to_dt   = datetime.strptime(t_date, "%d/%m/%Y").date()

        # Không chọn đơn vị ⇒ LOẠI đơn vị ngoài cây '00' (vd '66'), giống BC001/BC009/BC010/BC011.
        # Trước 15/08/2026 chỗ này để rỗng ⇒ báo cáo GỘP CẢ đơn vị ngoài cây → không tie được
        # với các báo cáo khác, và làm Bảng cân đối kế toán không cân.
        _oc, org_params = _org_filter_sql(org_ids, "ORGANIZATION_ID")
        org_where = (" AND " + _oc) if _oc else ""

        cur = get_connection().cursor()

        # Thêm biến ngày đầu năm để tránh bị cộng dồn cả phát sinh các năm cũ
        first_day_of_year = date(from_dt.year, 1, 1).strftime("%Y%m%d")

        # 1) Số dư đầu năm từ BALANCE_VIEW (toàn bộ dòng đều là số dư đầu kỳ)
        # 1) Số dư đầu năm từ BALANCE_VIEW (toàn bộ dòng đều là số dư đầu kỳ)
        try:
            cur.execute("SELECT TOP 1 ORGANIZATION_ID FROM dbo.BALANCE_VIEW WITH (NOLOCK)")
            has_org_in_balance = True
        except Exception:
            has_org_in_balance = False

        if has_org_in_balance:
            q_open = f"""
                SELECT ACCOUNT_ID, ISNULL(PR_DETAIL_ID, ''), ISNULL(ORGANIZATION_ID, ''),
                       SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT WHEN DEBIT_CREDIT='CRD' THEN -AMOUNT ELSE 0 END) AS BAL
                FROM dbo.BALANCE_VIEW WITH (NOLOCK)
                WHERE TRAN_DATE = ? {org_where}
                GROUP BY ACCOUNT_ID, ISNULL(PR_DETAIL_ID, ''), ISNULL(ORGANIZATION_ID, '')
            """
            # PHẢI là org_params (khớp số dấu ? trong org_where), KHÔNG phải org_ids —
            # khi không chọn đơn vị thì org_ids rỗng nhưng org_where vẫn có NOT IN (?).
            org_params_open = [first_day_of_year] + list(org_params)
        else:
            q_open = f"""
                SELECT ACCOUNT_ID, ISNULL(PR_DETAIL_ID, ''), '' AS ORGANIZATION_ID,
                       SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT WHEN DEBIT_CREDIT='CRD' THEN -AMOUNT ELSE 0 END) AS BAL
                FROM dbo.BALANCE_VIEW WITH (NOLOCK)
                WHERE TRAN_DATE = ?
                GROUP BY ACCOUNT_ID, ISNULL(PR_DETAIL_ID, '')
            """
            org_params_open = [first_day_of_year]

        cur.execute(q_open, org_params_open)
        opening_year = { ((r[0] or '').strip(), (r[1] or '').strip(), (r[2] or '').strip()): float(r[3] or 0) for r in cur.fetchall() }

        # 2) Phát sinh lũy kế đến từng mốc — MỘT lượt quét cho cả 4 mốc (xem _ledger_cum_by_cutoffs).
        # Truy vấn này sinh ra số dư thật của BC005 — _ledger_cum_by_cutoffs LOẠI đơn vị ngoài cây
        # '00' y như org_where ở trên, nếu không thì bảng cân đối KHÔNG CÂN (đơn vị 66 mang theo
        # số dư TK 6xx chưa kết chuyển, không có chỗ trên CĐKT).
        cut_end, cut_start, cut_pm_end, cut_pm_start = _cdkt_cutoffs(from_dt, to_dt)
        _cum = _ledger_cum_by_cutoffs(cur, first_day_of_year,
                                      (cut_end, cut_start, cut_pm_end, cut_pm_start), org_ids)
        ledger_to_end   = _cum[cut_end]
        ledger_to_start = _cum[cut_start]

        # 3) Cộng dồn: số dư = đầu năm + phát sinh lũy kế
        all_keys = set(opening_year) | set(ledger_to_end) | set(ledger_to_start)
        this_rows_full = [(k[0], k[1], k[2], opening_year.get(k, 0.0) + ledger_to_end.get(k, 0.0)) for k in all_keys]
        prev_rows_full = [(k[0], k[1], k[2], opening_year.get(k, 0.0) + ledger_to_start.get(k, 0.0)) for k in all_keys]

        # Roll up to (ACCOUNT_ID, PR_DETAIL_ID) for standard CDKT
        this_acc_pr = {}
        for acc, pr, org, bal in this_rows_full:
            this_acc_pr[(acc, pr)] = this_acc_pr.get((acc, pr), 0.0) + bal
        prev_acc_pr = {}
        for acc, pr, org, bal in prev_rows_full:
            prev_acc_pr[(acc, pr)] = prev_acc_pr.get((acc, pr), 0.0) + bal

        this_rows = [(acc, bal) for (acc, pr), bal in this_acc_pr.items()]
        prev_rows = [(acc, bal) for (acc, pr), bal in prev_acc_pr.items()]

        closing = _calc_cdkt_balances(this_rows)   # Kỳ này
        opening = _calc_cdkt_balances(prev_rows)   # Kỳ trước

        # Tính toán 1311 và 1312
        target_orgs = {'42', '51', '36', '65', '18', '31'}
        def calc_sub_131(rows_full, acc_pr_bals):
            # Precompute (acc,pr) -> tổng bal của các đơn vị target → O(N) thay vì O(N^2)
            # (vòng lặp cũ quét toàn bộ rows_full cho MỖI nhóm 1311 → 200s+ trên DB lớn)
            org_bal_idx = {}
            for a, p, o, bal in rows_full:
                if o in target_orgs:
                    k = (a, p)
                    org_bal_idx[k] = org_bal_idx.get(k, 0.0) + bal
            val_1311 = 0.0
            for (acc, pr), total_bal in acc_pr_bals.items():
                if acc.startswith('1311') and total_bal >= 0:
                    val_1311 += org_bal_idx.get((acc, pr), 0.0)
            return val_1311

        closing['1311'] = calc_sub_131(this_rows_full, this_acc_pr)
        closing['1312'] = closing.get('131', 0.0) - closing['1311']
        
        opening['1311'] = calc_sub_131(prev_rows_full, prev_acc_pr)
        opening['1312'] = opening.get('131', 0.0) - opening['1311']

        # --- XỬ LÝ ĐẶC BIỆT DÒNG 421A, 421B ---
        closing['421A'] = opening.get('421A', 0.0)

        def get_movement_421(d_end, d_start):
            end_val = sum(v for (a, pr, org), v in d_end.items() if a.startswith('421'))
            start_val = sum(v for (a, pr, org), v in d_start.items() if a.startswith('421'))
            return -(end_val - start_val)

        closing['421B'] = get_movement_421(ledger_to_end, ledger_to_start)

        try:
            opening['421B'] = get_movement_421(_cum[cut_pm_end], _cum[cut_pm_start])
        except Exception:
            opening['421B'] = 0.0

        return jsonify({
            "status": "ok",
            "data": {"opening": opening, "closing": closing}
        })
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


# ===== BC006 — BẢNG CÂN ĐỐI PHÁT SINH =====
@app.route("/api/trial_balance")
@with_db_lock
def get_trial_balance():
    try:
        f_date  = request.args.get("from_date")
        t_date  = request.args.get("to_date")
        org_ids = [v for v in request.args.get("org_ids", "").split(",") if v]

        from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
        to_dt   = datetime.strptime(t_date, "%d/%m/%Y").date()

        # Không chọn đơn vị ⇒ LOẠI đơn vị ngoài cây '00' (vd '66'), giống BC001/BC009/BC010/BC011.
        # Trước 15/08/2026 chỗ này để org_where rỗng ⇒ BC006 GỘP CẢ đơn vị ngoài cây → không tie
        # được với các báo cáo khác.
        _oc, org_params = _org_filter_sql(org_ids, "ORGANIZATION_ID")
        org_where = (" AND " + _oc) if _oc else ""

        cur = get_connection().cursor()
        first_day_of_year = date(from_dt.year, 1, 1).strftime("%Y%m%d")

        # 1. Lấy danh mục DM_ACCOUNT
        cur.execute("SELECT ACCOUNT_ID, ACCOUNT_NAME, IS_PARENT, ACCOUNT_TYPE_ID, PARENT_ACCOUNT_ID FROM dbo.DM_ACCOUNT WITH (NOLOCK)")
        accounts = {}
        for r in cur.fetchall():
            acc_id = (r[0] or "").strip()
            db_type = (r[3] or "").strip().lower()
            
            # Ép chuẩn loại tài khoản theo Kế toán Việt Nam (nếu DB rác/thiếu)
            if acc_id.startswith(('3', '4', '5', '7', '214', '229')):
                db_type = 'crd'
            elif acc_id.startswith(('1', '2', '6', '8', '9')):
                db_type = 'deb'
            else:
                db_type = 'deb'
                
            accounts[acc_id] = {
                "name": (r[1] or "").strip(),
                "is_parent": bool(r[2]),
                "type": db_type,
                "parent_id": (r[4] or "").strip()
            }
            
        # 1.1 Kế thừa thuộc tính lưỡng tính (debcrd) từ tài khoản cha hoặc tiền tố chuẩn
        sorted_accs = sorted(accounts.keys(), key=lambda x: len(x))
        for acc_id in sorted_accs:
            # Ép kiểu cho các tài khoản lưỡng tính kinh điển nếu DB config sai
            if acc_id.startswith('131') or acc_id.startswith('331') or acc_id.startswith('1388') or acc_id.startswith('3388'):
                accounts[acc_id]["type"] = 'debcrd'
            
            parent_id = accounts[acc_id]["parent_id"]
            if not parent_id:
                for i in range(len(acc_id)-1, 0, -1):
                    prefix = acc_id[:i]
                    if prefix in accounts and accounts[prefix]["is_parent"]:
                        parent_id = prefix
                        break
            if parent_id and parent_id in accounts:
                if accounts[parent_id]["type"] == 'debcrd':
                    accounts[acc_id]["type"] = 'debcrd'

        # 2. Lấy Dư đầu kỳ (từ BALANCE_VIEW đầu năm)
        q_open = f"""
            SELECT ACCOUNT_ID, ISNULL(PR_DETAIL_ID, ''),
                   SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT WHEN DEBIT_CREDIT='CRD' THEN -AMOUNT ELSE 0 END) AS BAL
            FROM dbo.BALANCE_VIEW WITH (NOLOCK)
            WHERE TRAN_DATE = ? {org_where}
            GROUP BY ACCOUNT_ID, ISNULL(PR_DETAIL_ID, '')
        """
        org_params_open = [first_day_of_year] + list(org_params)   # org_params, KHÔNG phải org_ids
        cur.execute(q_open, org_params_open)
        opening_year = { ((r[0] or '').strip(), (r[1] or '').strip()): float(r[2] or 0) for r in cur.fetchall() }

        # Lũy kế từ đầu năm tới trước from_dt (nếu có)
        ledger_to_start = {}
        if from_dt > date(from_dt.year, 1, 1):
            where_start = ["L.TRAN_DATE >= ?", "L.TRAN_DATE < ?"]
            params_start = [first_day_of_year, from_dt.strftime("%Y%m%d")]
            _lc, _lp = _org_filter_sql(org_ids, "L.ORGANIZATION_ID")
            if _lc:
                where_start.append(_lc)
                params_start.extend(_lp)
            q_ledger_start = f"""
                SELECT L.ACCOUNT_ID, ISNULL(L.PR_DETAIL_ID, ''),
                       SUM(CASE WHEN L.DEBIT_CREDIT='DEB' THEN L.AMOUNT WHEN L.DEBIT_CREDIT='CRD' THEN -L.AMOUNT ELSE 0 END) AS BAL
                FROM dbo.LEDGER L WITH (NOLOCK)
                WHERE {' AND '.join(where_start)}
                GROUP BY L.ACCOUNT_ID, ISNULL(L.PR_DETAIL_ID, '')
            """
            cur.execute(q_ledger_start, params_start)
            ledger_to_start = { ((r[0] or '').strip(), (r[1] or '').strip()): float(r[2] or 0) for r in cur.fetchall() }

        # 3. Lấy Phát sinh trong kỳ
        where_period = ["L.TRAN_DATE >= ?", "L.TRAN_DATE <= ?"]
        params_period = [from_dt.strftime("%Y%m%d"), to_dt.strftime("%Y%m%d")]
        _lc2, _lp2 = _org_filter_sql(org_ids, "L.ORGANIZATION_ID")
        if _lc2:
            where_period.append(_lc2)
            params_period.extend(_lp2)
        q_period = f"""
            SELECT L.ACCOUNT_ID, ISNULL(L.PR_DETAIL_ID, ''),
                   SUM(CASE WHEN L.DEBIT_CREDIT='DEB' THEN L.AMOUNT ELSE 0 END) AS DEB,
                   SUM(CASE WHEN L.DEBIT_CREDIT='CRD' THEN L.AMOUNT ELSE 0 END) AS CRD
            FROM dbo.LEDGER L WITH (NOLOCK)
            WHERE {' AND '.join(where_period)}
            GROUP BY L.ACCOUNT_ID, ISNULL(L.PR_DETAIL_ID, '')
        """
        cur.execute(q_period, params_period)
        period_data = { ((r[0] or '').strip(), (r[1] or '').strip()): {"deb": float(r[2] or 0), "crd": float(r[3] or 0)} for r in cur.fetchall() }

        # 4. Tính toán Dư Nợ/Có theo Object
        all_keys = set(opening_year.keys()) | set(ledger_to_start.keys()) | set(period_data.keys())
        raw_result = {}
        for acc_id, pr_id in all_keys:
            if acc_id not in raw_result:
                raw_result[acc_id] = {"open_deb": 0, "open_crd": 0, "period_deb": 0, "period_crd": 0, "close_deb": 0, "close_crd": 0}
            
            open_bal = opening_year.get((acc_id, pr_id), 0.0) + ledger_to_start.get((acc_id, pr_id), 0.0)
            p_data = period_data.get((acc_id, pr_id), {"deb": 0, "crd": 0})
            p_deb = p_data["deb"]
            p_crd = p_data["crd"]
            close_bal = open_bal + p_deb - p_crd
            
            acc_type = accounts.get(acc_id, {"type": "deb"})["type"]
            node = raw_result[acc_id]
            node["period_deb"] += p_deb
            node["period_crd"] += p_crd
            
            if acc_type == 'debcrd':
                if open_bal > 0: node["open_deb"] += open_bal
                elif open_bal < 0: node["open_crd"] += -open_bal
                
                if close_bal > 0: node["close_deb"] += close_bal
                elif close_bal < 0: node["close_crd"] += -close_bal
            else:
                node["open_deb"] += open_bal
                node["close_deb"] += close_bal
                
        # 5. Bù trừ tài khoản thường ở cấp Account
        for acc_id, node in raw_result.items():
            acc_type = accounts.get(acc_id, {"type": "deb"})["type"]
            if acc_type == 'deb':
                net_open = node["open_deb"] - node["open_crd"]
                node["open_deb"] = net_open
                node["open_crd"] = 0
                
                net_close = node["close_deb"] - node["close_crd"]
                node["close_deb"] = net_close
                node["close_crd"] = 0
            elif acc_type == 'crd':
                net_open = node["open_crd"] - node["open_deb"]
                node["open_crd"] = net_open
                node["open_deb"] = 0
                
                net_close = node["close_crd"] - node["close_deb"]
                node["close_crd"] = net_close
                node["close_deb"] = 0

        # 6. Chuẩn bị Final Result
        final_result = {acc: {"open_deb": 0, "open_crd": 0, "period_deb": 0, "period_crd": 0, "close_deb": 0, "close_crd": 0} for acc in accounts}
        for acc in raw_result:
            if acc not in final_result:
                final_result[acc] = {"open_deb": 0, "open_crd": 0, "period_deb": 0, "period_crd": 0, "close_deb": 0, "close_crd": 0}
        
        for acc_id, node in raw_result.items():
            for k in final_result[acc_id]:
                final_result[acc_id][k] += node[k]

        # 7. Cuộn dữ liệu lên Tài khoản Cha (từ mã dài tới mã ngắn)
        sorted_accs = sorted(final_result.keys(), key=lambda x: len(x), reverse=True)
        for acc_id in sorted_accs:
            parent_id = accounts.get(acc_id, {}).get("parent_id")
            if not parent_id:
                for i in range(len(acc_id)-1, 0, -1):
                    prefix = acc_id[:i]
                    if prefix in final_result and accounts.get(prefix, {}).get("is_parent"):
                        parent_id = prefix
                        break
                        
            if parent_id and parent_id in final_result:
                for k in final_result[acc_id]:
                    final_result[parent_id][k] += final_result[acc_id][k]
                    
        # 8. Filter những tài khoản có số liệu (chỉ trả về những tài khoản != 0)
        output = []
        for acc_id, node in final_result.items():
            if any(round(v, 2) != 0 for v in node.values()):
                output.append({
                    "id": acc_id,
                    "name": accounts.get(acc_id, {}).get("name", ""),
                    "is_parent": accounts.get(acc_id, {}).get("is_parent", False),
                    **node
                })
                
        output.sort(key=lambda x: x["id"])
        
        # 9. Tính Tổng cộng (Grand Total)
        # Bằng cách lấy tổng của tất cả các LEAF nodes (tài khoản không phải parent)
        total = {"open_deb": 0, "open_crd": 0, "period_deb": 0, "period_crd": 0, "close_deb": 0, "close_crd": 0}
        for acc_id, node in raw_result.items():
            for k in total:
                total[k] += node[k]

        return jsonify({
            "status": "ok",
            "data": output,
            "total": total
        })
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


@app.route("/api/debt_summary")
@with_db_lock
def get_debt_summary():
    """BC011 — Bảng tổng hợp phát sinh công nợ: gộp theo ĐỐI TƯỢNG cho (các) tài khoản đã chọn.
    Dư đầu/cuối tính net theo TỪNG đối tượng (lưỡng tính: >0 ghi Nợ, <0 ghi Có).
    Nguồn: BALANCE_VIEW (dư đầu năm) + LEDGER (lũy kế & phát sinh) — giống trial_balance."""
    try:
        f_date  = request.args.get("from_date")
        t_date  = request.args.get("to_date")
        acc_ids = [v.strip() for v in request.args.get("acc_ids", "").split(",") if v.strip()]
        pr_ids  = [v for v in request.args.get("pr_detail_ids", "").split(",") if v]
        org_ids = [v for v in request.args.get("org_ids", "").split(",") if v]

        if not acc_ids:
            return jsonify({"status": "error", "message": "Vui lòng chọn Tài khoản để xem báo cáo công nợ."}), 400

        from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
        to_dt   = datetime.strptime(t_date, "%d/%m/%Y").date()
        first_day_of_year = date(from_dt.year, 1, 1).strftime("%Y%m%d")

        # Tài khoản: khớp cả tài khoản con (LIKE 'acc%')
        acc_clause = "(" + " OR ".join(["ACCOUNT_ID LIKE ?"] * len(acc_ids)) + ")"
        acc_params = [a + "%" for a in acc_ids]

        # Không chọn đơn vị ⇒ LOẠI đơn vị ngoài cây '00' (vd '66'), giống các báo cáo khác.
        _oc, org_params = _org_filter_sql(org_ids, "ORGANIZATION_ID")
        org_clause = (" AND " + _oc) if _oc else ""

        pr_clause, pr_params = "", []
        if pr_ids:
            pr_clause = f" AND ISNULL(PR_DETAIL_ID,'') IN ({','.join(['?']*len(pr_ids))})"
            pr_params = list(pr_ids)

        cur = get_connection().cursor()

        # Gộp theo (ĐỐI TƯỢNG, TÀI KHOẢN công nợ) — thêm cột TK vào báo cáo.
        # 1. Dư đầu năm (BALANCE_VIEW) theo đối tượng + tài khoản
        q_open = f"""
            SELECT ISNULL(PR_DETAIL_ID,''), ISNULL(ACCOUNT_ID,''),
                   SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT WHEN DEBIT_CREDIT='CRD' THEN -AMOUNT ELSE 0 END)
            FROM dbo.BALANCE_VIEW WITH (NOLOCK)
            WHERE {acc_clause} AND TRAN_DATE = ? {org_clause} {pr_clause}
            GROUP BY ISNULL(PR_DETAIL_ID,''), ISNULL(ACCOUNT_ID,'')
        """
        cur.execute(q_open, acc_params + [first_day_of_year] + org_params + pr_params)
        opening = {((r[0] or '').strip(), (r[1] or '').strip()): float(r[2] or 0) for r in cur.fetchall()}

        # 2. Lũy kế từ đầu năm → trước from_dt (LEDGER)
        ledger_start = {}
        if from_dt > date(from_dt.year, 1, 1):
            q_start = f"""
                SELECT ISNULL(PR_DETAIL_ID,''), ISNULL(ACCOUNT_ID,''),
                       SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT WHEN DEBIT_CREDIT='CRD' THEN -AMOUNT ELSE 0 END)
                FROM dbo.LEDGER WITH (NOLOCK)
                WHERE {acc_clause} AND TRAN_DATE >= ? AND TRAN_DATE < ? {org_clause} {pr_clause}
                GROUP BY ISNULL(PR_DETAIL_ID,''), ISNULL(ACCOUNT_ID,'')
            """
            cur.execute(q_start, acc_params + [first_day_of_year, from_dt.strftime("%Y%m%d")] + org_params + pr_params)
            ledger_start = {((r[0] or '').strip(), (r[1] or '').strip()): float(r[2] or 0) for r in cur.fetchall()}

        # 3. Phát sinh trong kỳ (LEDGER)
        q_period = f"""
            SELECT ISNULL(PR_DETAIL_ID,''), ISNULL(ACCOUNT_ID,''),
                   SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT ELSE 0 END),
                   SUM(CASE WHEN DEBIT_CREDIT='CRD' THEN AMOUNT ELSE 0 END)
            FROM dbo.LEDGER WITH (NOLOCK)
            WHERE {acc_clause} AND TRAN_DATE >= ? AND TRAN_DATE <= ? {org_clause} {pr_clause}
            GROUP BY ISNULL(PR_DETAIL_ID,''), ISNULL(ACCOUNT_ID,'')
        """
        cur.execute(q_period, acc_params + [from_dt.strftime("%Y%m%d"), to_dt.strftime("%Y%m%d")] + org_params + pr_params)
        period = {((r[0] or '').strip(), (r[1] or '').strip()): {"deb": float(r[2] or 0), "crd": float(r[3] or 0)} for r in cur.fetchall()}

        # 4. Tên đối tượng
        pr_name = {}
        try:
            cur.execute("SELECT PR_DETAIL_ID, PR_DETAIL_NAME FROM dbo.DM_PR_DETAIL WITH (NOLOCK)")
            pr_name = {(r[0] or '').strip(): (r[1] or '').strip() for r in cur.fetchall()}
        except Exception:
            pass

        # 5. Tổng hợp theo (đối tượng, tài khoản) — net lưỡng tính từng dòng
        keys = set(opening) | set(ledger_start) | set(period)
        rows = []
        total = {"open_deb": 0, "open_crd": 0, "period_deb": 0, "period_crd": 0, "close_deb": 0, "close_crd": 0}
        for key in keys:
            pid, acc = key
            open_bal = opening.get(key, 0.0) + ledger_start.get(key, 0.0)
            pd = period.get(key, {"deb": 0, "crd": 0})
            p_deb, p_crd = pd["deb"], pd["crd"]
            close_bal = open_bal + p_deb - p_crd
            node = {
                "open_deb":  open_bal if open_bal > 0 else 0,
                "open_crd": -open_bal if open_bal < 0 else 0,
                "period_deb": p_deb,
                "period_crd": p_crd,
                "close_deb":  close_bal if close_bal > 0 else 0,
                "close_crd": -close_bal if close_bal < 0 else 0,
            }
            if all(round(v, 2) == 0 for v in node.values()):
                continue
            for k in total:
                total[k] += node[k]
            rows.append({"id": pid, "name": pr_name.get(pid, ''), "acc": acc, "is_parent": False, **node})

        # Sắp xếp theo Tài khoản công nợ rồi tới đối tượng (giống mẫu Excel)
        rows.sort(key=lambda x: (x["acc"], x["name"], x["id"]))

        return jsonify({"status": "ok", "data": rows, "total": total})
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


# ===== BC007 — SỔ NHẬT KÝ CHUNG =====

# ===== API XUẤT EXCEL CHUYÊN DỤNG (XỬ LÝ DỮ LIỆU LỚN) =====
from io import BytesIO
from flask import send_file
import xlsxwriter

@app.route("/api/export_excel_backend")
@with_db_lock
def export_excel_backend():
    try:
        report_type = request.args.get("report_type")
        f_date = request.args.get("from_date")
        t_date = request.args.get("to_date")
        org_ids = [v for v in request.args.get("org_ids", "").split(",") if v]
        account_id = request.args.get("account_id", "")
        
        from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
        to_dt = datetime.strptime(t_date, "%d/%m/%Y").date()
        
        # Không chọn đơn vị ⇒ LOẠI đơn vị ngoài cây '00' (vd '66'), giống BC001/BC009/BC010/BC011.
        # Trước 15/08/2026 chỗ này để rỗng ⇒ báo cáo GỘP CẢ đơn vị ngoài cây → không tie được
        # với các báo cáo khác, và làm Bảng cân đối kế toán không cân.
        _oc, org_params = _org_filter_sql(org_ids, "ORGANIZATION_ID")
        org_where = (" AND " + _oc) if _oc else ""

        cur = get_connection().cursor()
        
        if report_type == "BC007":
            title = "SỔ NHẬT KÝ CHUNG"
            sql = f"""
                SELECT TRAN_DATE, TRAN_NO, DESCRIPTION, ACCOUNT_ID, ACCOUNT_ID_CONTRA, DEBIT_CREDIT, AMOUNT
                FROM dbo.LEDGER_VIEW WITH (NOLOCK)
                WHERE TRAN_DATE >= ? AND TRAN_DATE <= ? {org_where}
                ORDER BY TRAN_DATE, TRAN_NO
            """
            params = [from_dt.strftime("%Y%m%d"), to_dt.strftime("%Y%m%d")] + org_params
            headers = ["Ngày HT", "Số CT", "Diễn giải", "TK Nợ", "TK Có", "Phát sinh Nợ", "Phát sinh Có"]
        elif report_type == "BC008":
            title = "SỔ CHI TIẾT TÀI KHOẢN"
            sql = f"""
                SELECT TRAN_DATE, TRAN_NO, DESCRIPTION, ACCOUNT_ID_CONTRA, DEBIT_CREDIT, AMOUNT
                FROM dbo.LEDGER_VIEW WITH (NOLOCK)
                WHERE ACCOUNT_ID LIKE ? + '%' AND TRAN_DATE >= ? AND TRAN_DATE <= ? {org_where}
                ORDER BY TRAN_DATE, TRAN_NO
            """
            params = [account_id, from_dt.strftime("%Y%m%d"), to_dt.strftime("%Y%m%d")] + org_params
            headers = ["Ngày HT", "Số CT", "Diễn giải", "TK Đối ứng", "Phát sinh Nợ", "Phát sinh Có", "Dư Nợ", "Dư Có"]
            
            open_bal_deb = 0
            open_bal_crd = 0
            first_day_of_year = date(from_dt.year, 1, 1).strftime("%Y%m%d")
            sql_open = f"""
                SELECT SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT ELSE 0 END),
                       SUM(CASE WHEN DEBIT_CREDIT='CRD' THEN AMOUNT ELSE 0 END)
                FROM dbo.BALANCE_VIEW WITH (NOLOCK)
                WHERE ACCOUNT_ID LIKE ? + '%' AND TRAN_DATE = ? {org_where}
            """
            cur.execute(sql_open, [account_id, first_day_of_year] + org_params)
            r_open = cur.fetchone()
            if r_open:
                open_bal_deb += float(r_open[0] or 0)
                open_bal_crd += float(r_open[1] or 0)
                
            if from_dt > date(from_dt.year, 1, 1):
                sql_lk = f"""
                    SELECT SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT ELSE 0 END),
                           SUM(CASE WHEN DEBIT_CREDIT='CRD' THEN AMOUNT ELSE 0 END)
                    FROM dbo.LEDGER_VIEW WITH (NOLOCK)
                    WHERE ACCOUNT_ID LIKE ? + '%' AND TRAN_DATE >= ? AND TRAN_DATE < ? {org_where}
                """
                cur.execute(sql_lk, [account_id, first_day_of_year, from_dt.strftime("%Y%m%d")] + org_params)
                r_lk = cur.fetchone()
                if r_lk:
                    open_bal_deb += float(r_lk[0] or 0)
                    open_bal_crd += float(r_lk[1] or 0)
        else:
            return jsonify({"status": "error", "message": "Report type không hỗ trợ xuất Excel trực tiếp từ backend."}), 400

        cur.execute(sql, params)
        rows = cur.fetchall()
        total_rows = len(rows)

        SPLIT_LIMIT = 500000
        sheets_data = {}
        
        if total_rows > SPLIT_LIMIT:
            for r in rows:
                dt = r[0]
                year_key = f"Năm {dt.year}"
                if year_key not in sheets_data: sheets_data[year_key] = []
                sheets_data[year_key].append(r)
                
            new_sheets = {}
            for k, s_rows in sheets_data.items():
                if len(s_rows) > SPLIT_LIMIT:
                    for r in s_rows:
                        dt = r[0]
                        quarter = (dt.month - 1) // 3 + 1
                        q_key = f"{k} - Q{quarter}"
                        if q_key not in new_sheets: new_sheets[q_key] = []
                        new_sheets[q_key].append(r)
                else:
                    new_sheets[k] = s_rows
            sheets_data = new_sheets
            
            final_sheets = {}
            for k, s_rows in sheets_data.items():
                if len(s_rows) > SPLIT_LIMIT:
                    for r in s_rows:
                        dt = r[0]
                        m_key = f"{k} - Th{dt.month}"
                        if m_key not in final_sheets: final_sheets[m_key] = []
                        final_sheets[m_key].append(r)
                else:
                    final_sheets[k] = s_rows
            sheets_data = final_sheets
        else:
            sheets_data["Data"] = rows
            
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        header_format = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#D3D3D3'})
        num_format = workbook.add_format({'num_format': '#,##0'})
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
        
        for sheet_name, s_rows in sheets_data.items():
            ws = workbook.add_worksheet(sheet_name[:31])
            # Auto-fit column widths
            if report_type == 'BC007':
                ws.set_column(0, 0, 12)
                ws.set_column(1, 1, 15)
                ws.set_column(2, 2, 45)
                ws.set_column(3, 3, 12)
                ws.set_column(4, 4, 12)
                ws.set_column(5, 6, 18)
            else:
                ws.set_column(0, 0, 12)
                ws.set_column(1, 1, 15)
                ws.set_column(2, 2, 45)
                ws.set_column(3, 3, 12)
                ws.set_column(4, 5, 18)
                ws.set_column(6, 7, 18)
# Lấy tên đơn vị
            org_name = "Tất cả đơn vị"
            if org_ids:
                try:
                    org_cur = get_connection().cursor()
                    org_cur.execute("SELECT ORGANIZATION_NAME FROM dbo.DM_ORGANIZATION WHERE ORGANIZATION_ID = ?", [org_ids[0]])
                    r_org = org_cur.fetchone()
                    if r_org:
                        org_name = f"{org_ids[0]} - {r_org[0]}"
                except Exception as e:
                    org_name = f"Đơn vị: {','.join(org_ids)}"

            mso_pattern = "Mẫu S03a - DN" if report_type == "BC007" else "Mẫu S38 - DN"
            last_col = 6 if report_type == "BC007" else 7

            company_format = workbook.add_format({'bold': True, 'font_size': 11})
            pattern_format = workbook.add_format({'bold': True, 'italic': True, 'font_size': 10, 'align': 'right'})
            org_format = workbook.add_format({'bold': True, 'font_size': 9, 'font_color': '#475569'})
            title_format = workbook.add_format({'bold': True, 'font_size': 15, 'align': 'center'})
            period_format = workbook.add_format({'bold': True, 'font_size': 11, 'font_color': '#4f46e5', 'align': 'center'})

            # Lấy thông tin công ty phục vụ in ấn/báo cáo
            company_name = "CÔNG TY TNHH DUONG THANH LONG"
            try:
                company_cur = get_connection().cursor()
                company_cur.execute("""
                    SELECT VAR_NAME, VAR_VALUE FROM dbo.SYS_SYSTEMVAR WITH (NOLOCK) 
                    WHERE VAR_NAME IN ('COMPANY_NAME','PARENT_COMPANY')
                """)
                sv_comp = {r[0]: (r[1] or '').strip() for r in company_cur.fetchall()}
                val = sv_comp.get('COMPANY_NAME') or sv_comp.get('PARENT_COMPANY')
                if val:
                    company_name = val
                else:
                    # Fallback sang organization '00'
                    company_cur.execute("SELECT ORGANIZATION_NAME FROM dbo.DM_ORGANIZATION WHERE ORGANIZATION_ID = '00'")
                    r_org = company_cur.fetchone()
                    if r_org and r_org[0]:
                        company_name = r_org[0].strip()
            except Exception:
                pass

            ws.write(0, 0, company_name, company_format)
            ws.write(0, last_col, mso_pattern, pattern_format)
            ws.write(1, 0, f"Đơn vị: {org_name}", org_format)
            
            ws.merge_range(3, 0, 3, last_col, title, title_format)
            ws.merge_range(4, 0, 4, last_col, f"Từ ngày {f_date} đến {t_date}", period_format)

            start_row = 6
            if report_type == "BC008":
                ws.write(5, 0, f"Tài khoản: {account_id}", workbook.add_format({'bold': True, 'font_size': 10}))
                start_row = 7

            for col_num, col_name in enumerate(headers):
                ws.write(start_row, col_num, col_name, header_format)

            current_row = start_row + 1

            if report_type == "BC008":
                if sheet_name == list(sheets_data.keys())[0]:
                    ws.write(current_row, 2, "Số dư đầu kỳ", cell_format)
                    ws.write(current_row, 6, open_bal_deb if open_bal_deb > open_bal_crd else 0, num_format)
                    ws.write(current_row, 7, open_bal_crd if open_bal_crd > open_bal_deb else 0, num_format)
                    current_row += 1
                running_deb = open_bal_deb
                running_crd = open_bal_crd

            for r in s_rows:
                ws.write(current_row, 0, r[0], date_format)
                ws.write(current_row, 1, r[1] or "", text_format)
                ws.write(current_row, 2, r[2] or "", cell_format)
                
                if report_type == "BC007":
                    ws.write(current_row, 3, r[3] or "", text_format)
                    ws.write(current_row, 4, r[4] or "", text_format)
                    amt = float(r[6] or 0)
                    is_deb = (r[5] == 'DEB')
                    ws.write(current_row, 5, amt if is_deb else 0, num_format)
                    ws.write(current_row, 6, amt if not is_deb else 0, num_format)
                else:
                    ws.write(current_row, 3, r[3] or "", text_format)
                    amt = float(r[5] or 0)
                    is_deb = (r[4] == 'DEB')
                    ws.write(current_row, 4, amt if is_deb else 0, num_format)
                    ws.write(current_row, 5, amt if not is_deb else 0, num_format)
                    
                    if is_deb: running_deb += amt
                    else: running_crd += amt
                    
                    bal_d = running_deb - running_crd
                    if bal_d > 0:
                        ws.write(current_row, 6, bal_d, num_format)
                        ws.write(current_row, 7, 0, num_format)
                    else:
                        ws.write(current_row, 6, 0, num_format)
                        ws.write(current_row, 7, -bal_d, num_format)
                current_row += 1

            # Ghi Footer chữ ký ở cuối sheet
            current_row += 1
            from datetime import datetime as dt_class
            today = dt_class.now()
            date_str = f"TP. HCM, Ngày {today.day} Tháng {today.month} Năm {today.year}"
            
            sig_date_format = workbook.add_format({'italic': True, 'font_size': 10, 'align': 'center'})
            sig_title_format = workbook.add_format({'bold': True, 'font_size': 11, 'align': 'center'})
            sig_help_format = workbook.add_format({'italic': True, 'font_size': 9, 'font_color': '#94a3b8', 'align': 'center'})

            ws.merge_range(current_row, last_col - 2, current_row, last_col, date_str, sig_date_format)
            current_row += 1
            
            ws.merge_range(current_row, 0, current_row, 1, "NGƯỜI LẬP BIỂU", sig_title_format)
            ws.merge_range(current_row, 2, current_row, last_col - 3, "KẾ TOÁN TRƯỞNG", sig_title_format)
            ws.merge_range(current_row, last_col - 2, current_row, last_col, "GIÁM ĐỐC", sig_title_format)
            current_row += 1
            
            ws.merge_range(current_row, 0, current_row, 1, "(Ký, họ tên)", sig_help_format)
            ws.merge_range(current_row, 2, current_row, last_col - 3, "(Ký, họ tên)", sig_help_format)
            ws.merge_range(current_row, last_col - 2, current_row, last_col, "(Ký, họ tên)", sig_help_format)
            current_row += 4 # Khoảng trống ký tên
            
            ws.freeze_panes(start_row + 1, 0)
            
        workbook.close()
        output.seek(0)
        
        return send_file(output, as_attachment=True, download_name=f"{report_type}_Export.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        msg = str(e)
        logger.error(f"Error in export_excel_backend: {msg}")
        return jsonify({"status": "error", "message": msg}), 500


@app.route("/api/report_export_csv")
def report_export_csv():
    """Xuất CSV STREAMING (không giới hạn dòng) cho báo cáo nhiều dòng: BC007 (Nhật ký chung), BC008 (Sổ chi tiết).
    Dùng connection riêng + stream trực tiếp tới trình duyệt → KHÔNG giữ pool, KHÔNG nạp RAM,
    KHÔNG dính giới hạn 1.048.576 dòng của Excel (xls/xlsx). Excel/Sheets mở CSV này bình thường."""
    from flask import Response, stream_with_context
    try:
        report_type = request.args.get("report_type", "")
        mode = request.args.get("mode", "summary")   # BC007: 'summary' (như web) | 'detail' (nhật ký chung chi tiết)
        f_date = request.args.get("from_date")
        t_date = request.args.get("to_date")
        org_ids = [v for v in request.args.get("org_ids", "").split(",") if v]
        # BC008: giữ NGUYÊN chuỗi đa chọn ('111,112') — tách/lọc bằng _acc_like_sql, KHÔNG cắt lấy mã đầu
        account_id = request.args.get("account_id", "").strip()
        from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
        to_dt   = datetime.strptime(t_date, "%d/%m/%Y").date()
        db_cfg = _db_cfg()
        if not db_cfg:
            return jsonify({"status": "error", "message": "Chưa đăng nhập SQL Server"}), 401

        # Xuất CSV phải lọc đơn vị Y HỆT bản trên màn hình, nếu không file xuất ra sẽ nhiều
        # dòng hơn báo cáo đang xem (gồm cả đơn vị ngoài cây '00').
        _oc, org_params = _org_filter_sql(org_ids, "ORGANIZATION_ID")
        org_where = (" AND " + _oc) if _oc else ""

        d_from = from_dt.strftime("%Y%m%d")
        d_to   = to_dt.strftime("%Y%m%d")
        first_day = date(from_dt.year, 1, 1).strftime("%Y%m%d")

        # org filter với alias L. (LEDGER) và LV. (LEDGER_VIEW) — tránh nhập nhằng khi JOIN DM_ORGANIZATION.
        # PHẢI đi qua _org_filter_sql y như org_where ở trên: ba biến này dùng CHUNG một mảng
        # org_params, nên nếu chỗ này còn dựng theo org_ids (rỗng khi không chọn đơn vị) thì số dấu ?
        # không khớp số params → "SQL contains 2 parameter markers, but 3 parameters were supplied".
        _lc, _lp   = _org_filter_sql(org_ids, "L.ORGANIZATION_ID")
        _lvc, _lvp = _org_filter_sql(org_ids, "LV.ORGANIZATION_ID")
        org_where_l  = (" AND " + _lc)  if _lc  else ""
        org_where_lv = (" AND " + _lvc) if _lvc else ""

        if report_type == "BC007" and mode == "detail":
            # NHẬT KÝ CHUNG CHI TIẾT — theo mẫu SQL người dùng cung cấp (bổ sung Tên đơn vị)
            headers = ["Bảng", "Mã đơn vị", "Tên đơn vị", "Công việc", "Mã chứng từ", "Ngày chứng từ",
                       "Số chứng từ", "Diễn giải", "Tài khoản", "Tài khoản đối ứng", "Mã đối tượng",
                       "Tên đối tượng", "Số tiền nợ", "Số tiền có", "Ghi chú"]
            sql = f"""SELECT 'NKC', LV.ORGANIZATION_ID, O.ORGANIZATION_NAME, LV.JOB_NAME, LV.TRAN_ID,
                             LV.TRAN_DATE, LV.TRAN_NO, LV.DESCRIPTION, LV.ACCOUNT_ID, LV.ACCOUNT_ID_CONTRA,
                             LV.PR_DETAIL_ID, LV.PR_DETAIL_NAME, LV.DEBIT_CREDIT, LV.AMOUNT, LV.COMMENTS
                      FROM dbo.LEDGER_VIEW LV WITH (NOLOCK)
                      LEFT JOIN dbo.DM_ORGANIZATION O WITH (NOLOCK) ON LV.ORGANIZATION_ID = O.ORGANIZATION_ID
                      WHERE LV.TRAN_DATE >= ? AND LV.TRAN_DATE <= ? {org_where_lv}
                      ORDER BY LV.TRAN_DATE, LV.TRAN_NO"""
            params = [d_from, d_to] + org_params
            fname = f"BC007_Nhat_Ky_Chung_ChiTiet_{from_dt.strftime('%d%m%Y')}-{to_dt.strftime('%d%m%Y')}.csv"
        elif report_type == "BC007":
            # TỔNG HỢP (như web đang xem) — thêm Đơn vị / Tên đơn vị / Mã chứng từ
            journal_view_mode = request.args.get("journal_view_mode", "detail")
            if journal_view_mode == "summary":
                headers = ["Mã chứng từ", "Số CT", "Diễn giải",
                           "TK Nợ", "TK Có", "Phát sinh Nợ", "Phát sinh Có"]
            else:
                headers = ["Đơn vị", "Tên đơn vị", "Ngày HT", "Mã chứng từ", "Số CT", "Diễn giải",
                           "TK Nợ", "TK Có", "Phát sinh Nợ", "Phát sinh Có"]
            sql = f"""SELECT L.ORGANIZATION_ID, O.ORGANIZATION_NAME, L.TRAN_DATE, L.TRAN_ID, L.TRAN_NO,
                             L.DESCRIPTION, L.ACCOUNT_ID, L.ACCOUNT_ID_CONTRA, L.DEBIT_CREDIT, L.AMOUNT
                      FROM dbo.LEDGER L WITH (NOLOCK)
                      LEFT JOIN dbo.DM_ORGANIZATION O WITH (NOLOCK) ON L.ORGANIZATION_ID = O.ORGANIZATION_ID
                      WHERE L.TRAN_DATE >= ? AND L.TRAN_DATE <= ? {org_where_l}
                      ORDER BY L.TRAN_DATE, L.TRAN_NO"""
            params = [d_from, d_to] + org_params
            fname = f"BC007_So_Nhat_Ky_Chung_{from_dt.strftime('%d%m%Y')}-{to_dt.strftime('%d%m%Y')}.csv"
        elif report_type == "BC008":
            if not account_id:
                return jsonify({"status": "error", "message": "Vui lòng chọn Tài khoản."}), 400
            headers = ["Ngày HT", "Số CT", "Diễn giải", "TK Đối ứng", "Phát sinh Nợ", "Phát sinh Có", "Dư Nợ", "Dư Có"]
            # Tài khoản là bộ lọc ĐA CHỌN — dùng chung helper với bản trên màn hình, nếu không 2 bên lệch nhau
            acc_clause, acc_params = _acc_like_sql(account_id)
            sql = f"""SELECT TRAN_DATE, TRAN_NO, DESCRIPTION, ACCOUNT_ID_CONTRA, DEBIT_CREDIT, AMOUNT
                      FROM dbo.LEDGER WITH (NOLOCK) WHERE {acc_clause} AND TRAN_DATE >= ? AND TRAN_DATE <= ? {org_where}
                      ORDER BY TRAN_DATE, TRAN_NO"""
            params = acc_params + [d_from, d_to] + org_params
            fname = (f"BC008_So_Chi_Tiet_{account_id.replace(',', '-')}"
                     f"_{from_dt.strftime('%d%m%Y')}-{to_dt.strftime('%d%m%Y')}.csv")
        elif report_type in ("BC014", "BC013"):
            # BẢNG KÊ HÓA ĐƠN BÁN RA (6.2) — cột y hệt bảng trên web, xuất TOÀN BỘ (không phân trang).
            # Nhận cả "BC013" (mã cũ trước 15/08/2026) lẫn "BC014" (mã hiện tại) để index.html
            # còn nằm trong cache trình duyệt vẫn xuất được, không báo "Report type không hỗ trợ".
            # Bộ lọc phải khớp /api/vat_sales_report: đơn vị dùng _org_filter_sql (không chọn ⇒ loại đơn vị
            # ngoài cây '00'), tài khoản LIKE prefix đa chọn — nếu dùng org_where thường sẽ lệch số so màn hình.
            acc_ids_13 = [v.strip() for v in request.args.get("acc_ids", "").split(",") if v.strip()]
            _oc, _op = _org_filter_sql(org_ids, "ORGANIZATION_ID")
            vat_org_where = (" AND " + _oc) if _oc else ""
            vat_acc_where, vat_acc_params = "", []
            if acc_ids_13:
                vat_acc_where = " AND (" + " OR ".join(["ACCOUNT_ID LIKE ?"] * len(acc_ids_13)) + ")"
                vat_acc_params = [a + "%" for a in acc_ids_13]
            headers = ["TT", "Ký hiệu hóa đơn", "Số hóa đơn", "Ngày phát hành", "Tên người bán",
                       "Mã số thuế người mua", "Mặt hàng", "Doanh số bán chưa có thuế",
                       "Thuế suất (%)", "Thuế GTGT", "Ghi chú"]
            if mode == "summary":
                # Gộp mỗi số hóa đơn 1 dòng — GROUP BY y hệt nhánh summary của /api/vat_sales_report
                sql = f"""SELECT ISNULL(VAT_TRAN_SERIE,''), ISNULL(VAT_TRAN_NO,''), VAT_TRAN_DATE,
                                 ISNULL(PR_DETAIL_NAME,''), ISNULL(TAX_FILE_NUMBER,''),
                                 N'Bán hàng hóa, dịch vụ', ISNULL(SUM(AMOUNT_ITEM),0),
                                 ISNULL(MAX(VAT_TAX_RATE),0), ISNULL(SUM(AMOUNT),0), N''
                          FROM dbo.VAT_TRANSACTION_VIEW WITH (NOLOCK)
                          WHERE DEBIT_CREDIT = 'CRD'
                            AND VAT_TRAN_DATE >= ? AND VAT_TRAN_DATE <= ?{vat_org_where}{vat_acc_where}
                          GROUP BY VAT_TRAN_SERIE, VAT_TRAN_NO, VAT_TRAN_DATE, PR_DETAIL_NAME, TAX_FILE_NUMBER, ACCOUNT_ID
                          ORDER BY VAT_TRAN_DATE, VAT_TRAN_NO"""
            else:
                sql = f"""SELECT ISNULL(VAT_TRAN_SERIE,''), ISNULL(VAT_TRAN_NO,''), VAT_TRAN_DATE,
                                 ISNULL(PR_DETAIL_NAME,''), ISNULL(TAX_FILE_NUMBER,''), ISNULL(ITEM_NAME,''),
                                 ISNULL(AMOUNT_ITEM,0), ISNULL(VAT_TAX_RATE,0), ISNULL(AMOUNT,0), ISNULL(COMMENTS,'')
                          FROM dbo.VAT_TRANSACTION_VIEW WITH (NOLOCK)
                          WHERE DEBIT_CREDIT = 'CRD'
                            AND VAT_TRAN_DATE >= ? AND VAT_TRAN_DATE <= ?{vat_org_where}{vat_acc_where}
                          ORDER BY VAT_TAX_RATE, VAT_TRAN_DATE, VAT_TRAN_NO"""
            params = [d_from, d_to] + list(_op) + vat_acc_params
            fname = (f"BC014_Bang_Ke_Ban_Ra_{'TongHop' if mode == 'summary' else 'ChiTiet'}"
                     f"_{from_dt.strftime('%d%m%Y')}-{to_dt.strftime('%d%m%Y')}.csv")
        else:
            return jsonify({"status": "error", "message": "Report type không hỗ trợ xuất CSV."}), 400

        # ── XUẤT XLSX MỘT FILE NHIỀU SHEET — CHỈ BC007 ────────────────────────────
        # Nhật ký chung một tháng đã đo được 2.851.224 dòng (T08/2026), vượt xa trần
        # 1.048.576 dòng/sheet của Excel ⇒ mở file CSV bằng Excel bị cắt mất phần đuôi
        # (đo thật: mất 63% dữ liệu, dừng ở 12/08) mà người dùng không hề nhận ra.
        # Xuất .xlsx tự sang sheet mới mỗi 1.000.000 dòng: vẫn MỘT file mở thẳng bằng
        # Excel, và còn NHẸ HƠN CSV ~2,7 lần (115 MB so với 317 MB) vì .xlsx vốn là gói
        # ZIP nén sẵn. Dùng CHUNG sql/params/headers với nhánh CSV ở trên nên hai định
        # dạng không thể lệch số. Ghi mất vài phút ⇒ đi qua _start_export_job (thread
        # riêng + progress + huỷ), trả job_id để frontend poll /api/export/status.
        if report_type == "BC007" and request.args.get("format", "").lower() == "xlsx":
            _is_detail = (mode == "detail")
            _jvm = request.args.get("journal_view_mode", "detail")

            def _tf_xlsx(r, _cols):
                # Trả kiểu Python thật (datetime/float) để xlsxwriter ghi đúng ô ngày và
                # ô số — Excel cộng/lọc/sắp xếp được ngay, khác CSV vốn chỉ toàn chuỗi.
                # Mã đơn vị ghi thẳng '05', KHÔNG bọc ="05" như CSV: mẹo đó chỉ để Excel
                # khỏi ăn mất số 0 đầu lúc parse text, ô xlsx đã ép sẵn định dạng text.
                if _is_detail:
                    amt = float(r[13] or 0); is_deb = (r[12] == 'DEB')
                    return [r[0] or '', r[1] or '', r[2] or '', r[3] or '', r[4] or '', r[5],
                            r[6] or '', r[7] or '', r[8] or '', r[9] or '', r[10] or '', r[11] or '',
                            amt if is_deb else 0, amt if not is_deb else 0, r[14] or '']
                amt = float(r[9] or 0); is_deb = (r[8] == 'DEB')
                if _jvm == "summary":
                    return [r[3] or '', r[4] or '', r[5] or '', r[6] or '', r[7] or '',
                            amt if is_deb else 0, amt if not is_deb else 0]
                return [r[0] or '', r[1] or '', r[2], r[3] or '', r[4] or '', r[5] or '',
                        r[6] or '', r[7] or '', amt if is_deb else 0, amt if not is_deb else 0]

            job_id = _start_export_job(fname[:-4] + ".xlsx", headers, sql, params,
                                       _tf_xlsx, sheet_limit=1000000)
            return jsonify({"status": "ok", "job_id": job_id})

        def _amt(a):
            a = float(a or 0)
            return int(a) if a.is_integer() else a

        def generate():
            own = _make_conn(db_cfg)
            try:
                cur = own.cursor()
                yield '﻿' + ','.join(_csv_escape(h) for h in headers) + '\r\n'   # BOM để Excel nhận UTF-8

                if report_type == "BC008":
                    odeb = ocrd = 0.0
                    c2 = own.cursor()
                    c2.execute(f"""SELECT SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT ELSE 0 END),
                                          SUM(CASE WHEN DEBIT_CREDIT='CRD' THEN AMOUNT ELSE 0 END)
                                   FROM dbo.BALANCE_VIEW WITH (NOLOCK) WHERE {acc_clause} AND TRAN_DATE = ? {org_where}""",
                               acc_params + [first_day] + org_params)
                    ro = c2.fetchone()
                    if ro: odeb += float(ro[0] or 0); ocrd += float(ro[1] or 0)
                    if from_dt > date(from_dt.year, 1, 1):
                        c2.execute(f"""SELECT SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT ELSE 0 END),
                                              SUM(CASE WHEN DEBIT_CREDIT='CRD' THEN AMOUNT ELSE 0 END)
                                       FROM dbo.LEDGER WITH (NOLOCK) WHERE {acc_clause} AND TRAN_DATE >= ? AND TRAN_DATE < ? {org_where}""",
                                   acc_params + [first_day, d_from] + org_params)
                        rl = c2.fetchone()
                        if rl: odeb += float(rl[0] or 0); ocrd += float(rl[1] or 0)
                    run = odeb - ocrd
                    yield ','.join(_csv_escape(x) for x in ['', '', 'Số dư đầu kỳ', '', '', '',
                                                            _amt(run if run > 0 else 0), _amt(-run if run < 0 else 0)]) + '\r\n'
                    cur.execute(sql, params)
                    while True:
                        batch = cur.fetchmany(2000)
                        if not batch: break
                        lines = []
                        for r in batch:
                            amt = float(r[5] or 0); is_deb = (r[4] == 'DEB')
                            run += amt if is_deb else -amt
                            lines.append(','.join(_csv_escape(x) for x in [
                                r[0], r[1] or '', r[2] or '', r[3] or '',
                                _amt(amt if is_deb else 0), _amt(amt if not is_deb else 0),
                                _amt(run if run > 0 else 0), _amt(-run if run < 0 else 0)]))
                        yield '\r\n'.join(lines) + '\r\n'
                elif report_type in ("BC014", "BC013"):  # BẢNG KÊ BÁN RA — TT tự đánh, mã giữ dạng text, chốt Tổng cộng
                    cur.execute(sql, params)
                    stt = 0
                    sum_amt = sum_vat = 0.0
                    while True:
                        batch = cur.fetchmany(2000)
                        if not batch: break
                        lines = []
                        for r in batch:
                            stt += 1
                            amt = float(r[6] or 0); vat = float(r[8] or 0)
                            sum_amt += amt; sum_vat += vat
                            lines.append(','.join(_csv_escape(x) for x in [
                                stt, _csv_text_cell(r[0]), _csv_text_cell(r[1]), r[2],
                                r[3] or '', _csv_text_cell(r[4]), r[5] or '',
                                _amt(amt), _amt(float(r[7] or 0)), _amt(vat), r[9] or '']))
                        yield '\r\n'.join(lines) + '\r\n'
                    yield ','.join(_csv_escape(x) for x in [
                        '', '', '', '', '', '', 'Tổng cộng', _amt(sum_amt), '', _amt(sum_vat), '']) + '\r\n'
                elif report_type == "BC007" and mode == "detail":  # NHẬT KÝ CHUNG CHI TIẾT
                    cur.execute(sql, params)
                    while True:
                        batch = cur.fetchmany(2000)
                        if not batch: break
                        lines = []
                        for r in batch:
                            amt = float(r[13] or 0); is_deb = (r[12] == 'DEB')
                            lines.append(','.join(_csv_escape(x) for x in [
                                r[0] or '', _csv_text_cell(r[1]), r[2] or '', r[3] or '', r[4] or '', r[5],
                                r[6] or '', r[7] or '', r[8] or '', r[9] or '', _csv_text_cell(r[10]), r[11] or '',
                                _amt(amt if is_deb else 0), _amt(amt if not is_deb else 0), r[14] or '']))
                        yield '\r\n'.join(lines) + '\r\n'
                else:  # BC007 TỔNG HỢP (như web)
                    cur.execute(sql, params)
                    journal_view_mode = request.args.get("journal_view_mode", "detail")
                    while True:
                        batch = cur.fetchmany(2000)
                        if not batch: break
                        lines = []
                        for r in batch:
                            amt = float(r[9] or 0); is_deb = (r[8] == 'DEB')
                            if journal_view_mode == "summary":
                                row_data = [
                                    r[3] or '', r[4] or '', r[5] or '',
                                    r[6] or '', r[7] or '',
                                    _amt(amt if is_deb else 0), _amt(amt if not is_deb else 0)
                                ]
                            else:
                                row_data = [
                                    _csv_text_cell(r[0]), r[1] or '', r[2], r[3] or '', r[4] or '', r[5] or '',
                                    r[6] or '', r[7] or '',
                                    _amt(amt if is_deb else 0), _amt(amt if not is_deb else 0)
                                ]
                            lines.append(','.join(_csv_escape(x) for x in row_data))
                        yield '\r\n'.join(lines) + '\r\n'
            finally:
                try: own.close()
                except: pass

        resp = Response(stream_with_context(generate()), mimetype='text/csv; charset=utf-8')
        resp.headers['Content-Disposition'] = f'attachment; filename="{fname}"'
        resp.headers['Cache-Control'] = 'no-cache'
        return resp
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================================
# BC009 / BC010 — LƯU CHUYỂN TIỀN TỆ (trực tiếp + gián tiếp), chuẩn TT200/B03-DN
# Logic port nguyên từ LedgerReport (đã validated DB IACC_CHULONG T1-6/2026).
# ============================================================================

def _get_external_org_ids():
    """Danh sách ORGANIZATION_ID KHÔNG thuộc cây đơn vị '00' (vd: đơn vị ngoài như '66').
    Mặc định các báo cáo loại trừ những đơn vị này; người dùng muốn xem thì tự chọn ở bộ lọc."""
    db_config = (_db_cfg() or {})
    db_name = db_config.get('database', '')
    if db_name in _external_orgs_cache:
        return _external_orgs_cache[db_name]
    ext = []
    try:
        cur = get_connection().cursor()
        cur.execute("SELECT ORGANIZATION_ID, ISNULL(PARENT_ORGANIZATION_ID,'') FROM dbo.DM_ORGANIZATION WITH (NOLOCK)")
        par = {(r[0] or '').strip(): (r[1] or '').strip() for r in cur.fetchall()}
        def reaches_root(o):
            seen = set(); c = o
            while c and c not in seen:
                if c == '00':
                    return True
                seen.add(c); c = par.get(c, '')
            return False
        if '00' not in par:
            # ⛔ CHỐT AN TOÀN: DB không hề có đơn vị gốc '00' (DB của khách khác có thể đánh mã
            # khác hẳn). Khi đó reaches_root() trả False cho MỌI đơn vị ⇒ ext = toàn bộ danh sách
            # ⇒ mệnh đề NOT IN (tất cả) ⇒ mọi báo cáo trả 0 dòng mà KHÔNG báo lỗi gì.
            # Không có gốc '00' thì coi như không có khái niệm "ngoài cây" → không lọc.
            logger.warning("DM_ORGANIZATION khong co don vi goc '00' — bo qua loc don vi ngoai cay.")
            ext = []
        else:
            ext = [o for o in par if o != '00' and not reaches_root(o)]
    except Exception:
        ext = []
    _external_orgs_cache[db_name] = ext
    return ext


def _acc_like_sql(account_id, col="ACCOUNT_ID"):
    """Bộ lọc tài khoản cha→con cho BC008. `account_id` có thể chứa NHIỀU mã ngăn bởi dấu phẩy ('111,112').
    Trả (clause, params) = "(col LIKE ? OR col LIKE ?)", ['111%','112%'].

    ⚠️ Code cũ ghép thẳng chuỗi vào `col LIKE ? + '%'` → thành `LIKE '111,112%'` → KHÔNG khớp dòng nào →
    chọn 2 tài khoản là báo cáo/file xuất RỖNG mà không báo lỗi (bộ lọc Tài khoản là đa chọn nên rất dễ dính).
    Dùng chung 1 helper cho cả bản trên màn hình lẫn nút xuất để 2 bên không lệch nhau.
    (Port từ LedgerReport — xem mục 9.6; Studio dính lỗi này tới 27/07/2026.)
    """
    accs = [a.strip() for a in (account_id or "").split(",") if a.strip()]
    if not accs:
        return "", []
    clause = "(" + " OR ".join([f"{col} LIKE ?"] * len(accs)) + ")"
    return clause, [a + "%" for a in accs]


def _org_filter_sql(org_ids, col="ORGANIZATION_ID"):
    """Trả (clause, params) cho bộ lọc đơn vị.
    - Có chọn đơn vị  -> col IN (...)  (tôn trọng đúng lựa chọn, kể cả đơn vị ngoài)
    - Không chọn      -> mặc định loại đơn vị ngoài cây 00 (col NOT IN externals)
    """
    # ÉP QUYỀN ĐƠN VỊ theo tài khoản (row-level). Điểm DUY NHẤT — mọi danh sách/báo cáo đi qua đây.
    allowed = _current_allowed_orgs()
    if allowed is not None:
        base = [str(o) for o in org_ids] if org_ids else None
        eff = [o for o in base if o in allowed] if base else sorted(allowed)
        if not eff:
            return "1=0", []                 # chọn toàn đơn vị ngoài quyền → không trả dòng nào
        return f"{col} IN ({','.join(['?'] * len(eff))})", list(eff)
    if org_ids:
        return f"{col} IN ({','.join(['?'] * len(org_ids))})", list(org_ids)
    ext = _get_external_org_ids()
    if ext:
        return f"{col} NOT IN ({','.join(['?'] * len(ext))})", list(ext)
    return "", []


def _cf_is_cash(acc):
    a = (acc or "").strip()
    return a[:3] in ("111", "112", "113") or a[:4] == "1281"


def _cf_classify_direct(contra, dc):
    """Trả mã chỉ tiêu B03-DN (trực tiếp) cho 1 nghiệp vụ tiền.
    dc='DEB' → tiền THU (+) ; dc='CRD' → tiền CHI (−)."""
    c = (contra or "").strip()
    p3, p4 = c[:3], c[:4]
    if dc == "DEB":   # ----- TIỀN THU -----
        if p3 in ("511", "512", "131") or p4 == "3331": return "01"   # bán hàng, thu nợ KH, VAT đầu ra
        if p3 == "411":                                  return "31"   # nhận vốn góp CSH
        if p4 == "3411" or p3 in ("341", "343", "171"):  return "33"   # thu từ đi vay
        if p3 == "515" or p4 in ("1281", "1288", "1283", "121"): return "27"  # thu lãi, cổ tức
        if p3 == "128":                                  return "24"   # thu hồi cho vay
        if p3 in ("221", "222") or p4 == "2281":         return "26"   # thu hồi góp vốn
        if p3 == "711":                                  return "22"   # thanh lý TSCĐ
        return "06"                                                    # thu khác HĐKD
    else:             # ----- TIỀN CHI -----
        if p3 == "131":                                  return "01"   # đảo/hoàn thu bán hàng → net Mã 01
        if p3 == "334":                                  return "03"   # trả người lao động
        if p4 == "3334":                                 return "05"   # thuế TNDN đã nộp
        if p3 == "635":                                  return "04"   # lãi vay đã trả
        if p3 in ("151", "152", "153", "154", "155", "156", "157", "158", "159",
                  "331", "611", "621", "627", "641", "642", "133", "242", "142"): return "02"  # chi NCC/HHDV
        if p3 in ("211", "213", "217", "241"):           return "21"   # chi mua TSCĐ
        if p3 == "128":                                  return "23"   # chi cho vay
        if p3 in ("221", "222") or p4 == "2281":         return "25"   # chi góp vốn
        if p4 == "3412":                                 return "35"   # trả nợ gốc thuê tài chính
        if p4 == "3411" or p3 in ("341", "343", "171"):  return "34"   # trả nợ gốc vay
        if p3 == "419":                                  return "32"   # mua lại cổ phiếu
        if p3 == "421":                                  return "36"   # cổ tức, LN đã trả CSH
        return "07"                                                    # chi khác HĐKD


@app.route("/api/cash_flow")
@with_db_lock
def get_cash_flow():
    """BC009 (trực tiếp) + BC010 (gián tiếp). Trả {'direct':{...}, 'indirect':{...}}.
    Cả 2 dùng chung dữ liệu kỳ; Mã 20 gián tiếp được chốt khớp Mã 20 trực tiếp."""
    try:
        f_date  = request.args.get("from_date")
        t_date  = request.args.get("to_date")
        org_ids = [v for v in request.args.get("org_ids", "").split(",") if v]

        from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
        to_dt   = datetime.strptime(t_date, "%d/%m/%Y").date()
        first_day_of_year = date(from_dt.year, 1, 1).strftime("%Y%m%d")
        f_str = from_dt.strftime("%Y%m%d")
        t_str = to_dt.strftime("%Y%m%d")

        cur = get_connection().cursor()
        _rc, _rp = _org_filter_sql(org_ids, "L.ORGANIZATION_ID")
        org_and = (" AND " + _rc) if _rc else ""

        cash_like = ("(L.ACCOUNT_ID LIKE '111%' OR L.ACCOUNT_ID LIKE '112%' "
                     "OR L.ACCOUNT_ID LIKE '113%' OR L.ACCOUNT_ID LIKE '1281%')")

        # ---------- 1) PHƯƠNG PHÁP TRỰC TIẾP ----------
        q_cash = f"""
            SELECT L.ACCOUNT_ID_CONTRA, L.DEBIT_CREDIT, SUM(L.AMOUNT)
            FROM dbo.LEDGER L WITH (NOLOCK)
            WHERE {cash_like} AND L.TRAN_DATE >= ? AND L.TRAN_DATE <= ?{org_and}
            GROUP BY L.ACCOUNT_ID_CONTRA, L.DEBIT_CREDIT
        """
        cur.execute(q_cash, [f_str, t_str] + list(_rp))
        d = {}
        for contra, dc, total in cur.fetchall():
            if _cf_is_cash(contra):           # loại chuyển tiền nội bộ
                continue
            code = _cf_classify_direct(contra, dc)
            sign = 1.0 if (dc or "").strip() == "DEB" else -1.0
            d[code] = d.get(code, 0.0) + sign * float(total or 0)

        def g(*cs): return sum(d.get(c, 0.0) for c in cs)
        d["20"] = g("01", "02", "03", "04", "05", "06", "07")
        d["30"] = g("21", "22", "23", "24", "25", "26", "27")
        d["40"] = g("31", "32", "33", "34", "35", "36")
        d["50"] = g("20", "30", "40")

        # ---------- 2) TIỀN & TƯƠNG ĐƯƠNG TIỀN ĐẦU/CUỐI KỲ (Mã 60/70) ----------
        try:
            cur.execute("SELECT TOP 1 ORGANIZATION_ID FROM dbo.BALANCE_VIEW WITH (NOLOCK)")
            _bs_clause, _bs_p = _org_filter_sql(org_ids, "ORGANIZATION_ID")
            _bs_and = (" AND " + _bs_clause) if _bs_clause else ""
            has_org_bal = True
        except Exception:
            _bs_and, _bs_p, has_org_bal = "", [], False
        cash_like_bv = ("(ACCOUNT_ID LIKE '111%' OR ACCOUNT_ID LIKE '112%' "
                        "OR ACCOUNT_ID LIKE '113%' OR ACCOUNT_ID LIKE '1281%')")
        q_open = f"""
            SELECT SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT WHEN DEBIT_CREDIT='CRD' THEN -AMOUNT ELSE 0 END)
            FROM dbo.BALANCE_VIEW WITH (NOLOCK)
            WHERE TRAN_DATE = ? AND {cash_like_bv}{_bs_and if has_org_bal else ''}
        """
        cur.execute(q_open, [first_day_of_year] + (list(_bs_p) if has_org_bal else []))
        cash_open_year = float((cur.fetchone() or [0])[0] or 0)

        def cash_mov(end_inclusive=None, end_exclusive=None):
            where = [cash_like, "L.TRAN_DATE >= ?"]
            params = [first_day_of_year]
            if end_inclusive:
                where.append("L.TRAN_DATE <= ?"); params.append(end_inclusive)
            if end_exclusive:
                where.append("L.TRAN_DATE < ?");  params.append(end_exclusive)
            if _rc:
                where.append(_rc); params.extend(_rp)
            cur.execute(f"""SELECT SUM(CASE WHEN L.DEBIT_CREDIT='DEB' THEN L.AMOUNT ELSE -L.AMOUNT END)
                            FROM dbo.LEDGER L WITH (NOLOCK) WHERE {' AND '.join(where)}""", params)
            return float((cur.fetchone() or [0])[0] or 0)

        d["60"] = cash_open_year + cash_mov(end_exclusive=f_str)   # tiền đầu kỳ
        d["61"] = 0.0                                              # ảnh hưởng tỷ giá (chưa tách)
        d["70"] = cash_open_year + cash_mov(end_inclusive=t_str)   # tiền cuối kỳ

        # ---------- 3) PHƯƠNG PHÁP GIÁN TIẾP ----------
        cur.execute(f"""
            SELECT L.ACCOUNT_ID, L.ACCOUNT_ID_CONTRA, L.DEBIT_CREDIT, SUM(L.AMOUNT)
            FROM dbo.LEDGER L WITH (NOLOCK)
            WHERE L.TRAN_DATE >= ? AND L.TRAN_DATE <= ?{org_and}
            GROUP BY L.ACCOUNT_ID, L.ACCOUNT_ID_CONTRA, L.DEBIT_CREDIT
        """, [f_str, t_str] + list(_rp))
        pl = cur.fetchall()

        def s(pfx, dc, excl=()):
            return sum(float(r[3] or 0) for r in pl
                       if (r[0] or "").strip().startswith(pfx) and r[2] == dc
                       and not any((r[1] or "").strip().startswith(e) for e in excl))
        def net(pfx):  # biến động số dư trong kỳ (DEB-CRD), loại bút toán kết chuyển 911
            return s(pfx, "DEB", ["911"]) - s(pfx, "CRD", ["911"])

        # LN trước thuế & chi phí lãi vay: dùng CHÍNH engine KQKD (_calc_results) để khớp
        # tuyệt đối với báo cáo BC001 (r['13'] = LN trước thuế, r['07'] = chi phí tài chính).
        # r['13'] chỉ phụ thuộc tổng số TK 5/6/7/8 (không cần item_class) nên truyền field rỗng
        # — nhưng PHẢI có đủ key expense_class/expense_id, _calc_results đọc trực tiếp d['...'].
        cf_data = [{"acc": (r[0] or "").strip(), "contra": (r[1] or "").strip(),
                    "dc": r[2], "val": float(r[3] or 0),
                    "item_class": "", "expense_class": "", "expense_id": "",
                    "month": from_dt.month, "year": from_dt.year} for r in pl]
        kq = _calc_results(cf_data, {}, {})

        i = {}
        i["01"] = kq.get("13", 0.0)                                             # LN trước thuế (= BC001)
        i["02"] = s("214", "CRD", ["911"]) - s("214", "DEB", ["911"])           # khấu hao
        i["03"] = sum((s(p_, "CRD", ["911"]) - s(p_, "DEB", ["911"])) for p_ in ("229", "352", "159"))  # dự phòng
        i["04"] = 0.0
        i["05"] = 0.0
        i["06"] = kq.get("07", 0.0)                                             # chi phí lãi vay (= BC001 r07)
        i["09"] = -sum(net(p_) for p_ in ["131", "133", "136", "138", "141", "244"])  # phải thu
        i["10"] = -sum(net(p_) for p_ in ["151", "152", "153", "154", "155", "156", "157", "158"])  # tồn kho
        i["11"] = -sum(net(p_) for p_ in ["331", "333", "334", "335", "336", "337", "338"])  # phải trả
        i["12"] = -net("242")                                                   # chi phí trả trước
        i["13"] = -net("121")                                                   # chứng khoán KD
        i["14"] = d.get("04", 0.0)                                              # lãi vay đã trả (từ trực tiếp)
        i["15"] = d.get("05", 0.0)                                              # thuế TNDN đã nộp (từ trực tiếp)
        i["16"] = 0.0
        i["17"] = 0.0
        sum_wc  = sum(i[k] for k in ("09", "10", "11", "12", "13", "14", "15", "16", "17"))
        base    = i["01"] + i["02"] + i["03"] + i["04"] + i["05"] + i["06"]
        i["07"] = d["20"] - (base + sum_wc)   # điều chỉnh khác (chốt khớp Mã 20 trực tiếp)
        i["08"] = base + i["07"]
        i["20"] = i["08"] + sum_wc
        for k in ("21", "22", "23", "24", "25", "26", "27", "30",
                  "31", "32", "33", "34", "35", "36", "40", "50", "60", "61", "70"):
            i[k] = d.get(k, 0.0)

        # Cắt theo quyền: user chỉ có BC009 thì KHÔNG trả 'indirect' (và ngược lại) —
        # tránh ẩn menu BC010 mà vẫn lộ số qua network. ADMIN có cả hai nên trả đủ như cũ.
        _p = _current_perms()
        _cf = {}
        if 'BC009' in _p: _cf['direct'] = d
        if 'BC010' in _p: _cf['indirect'] = i
        return jsonify({"status": "ok", "data": _cf})
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


@app.route("/api/journal")
@with_db_lock
def get_journal():
    try:
        f_date = request.args.get("from_date")
        t_date = request.args.get("to_date")
        org_ids = [v for v in request.args.get("org_ids", "").split(",") if v]
        
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 10000))

        from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
        to_dt = datetime.strptime(t_date, "%d/%m/%Y").date()

        # Không chọn đơn vị ⇒ LOẠI đơn vị ngoài cây '00' (vd '66'), giống BC001/BC009/BC010/BC011.
        # Trước 15/08/2026 chỗ này để rỗng ⇒ báo cáo GỘP CẢ đơn vị ngoài cây → không tie được
        # với các báo cáo khác, và làm Bảng cân đối kế toán không cân.
        _oc, org_params = _org_filter_sql(org_ids, "ORGANIZATION_ID")
        org_where = (" AND " + _oc) if _oc else ""

        cur = get_connection().cursor()
        
        count_sql = f"""
            SELECT COUNT(*),
                   SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT ELSE 0 END),
                   SUM(CASE WHEN DEBIT_CREDIT='CRD' THEN AMOUNT ELSE 0 END)
            FROM dbo.LEDGER_VIEW WITH (NOLOCK)
            WHERE TRAN_DATE >= ? AND TRAN_DATE <= ? {org_where}
        """
        base_params = [from_dt.strftime("%Y%m%d"), to_dt.strftime("%Y%m%d")] + org_params
        cur.execute(count_sql, base_params)
        c_row = cur.fetchone()
        total_rows = c_row[0] or 0
        total_deb = float(c_row[1] or 0)
        total_crd = float(c_row[2] or 0)
        
        # Map ORGANIZATION_ID -> ORGANIZATION_NAME (LEDGER_VIEW không có sẵn tên đơn vị)
        org_map = {}
        try:
            cur.execute("SELECT CAST(ORGANIZATION_ID AS NVARCHAR(100)), ORGANIZATION_NAME FROM dbo.DM_ORGANIZATION WITH (NOLOCK)")
            org_map = {(r[0] or '').strip(): (r[1] or '').strip() for r in cur.fetchall()}
        except Exception:
            pass

        offset = (page - 1) * page_size
        paged_sql = f"""
            WITH CTE AS (
                SELECT
                    TRAN_DATE, TRAN_NO, DESCRIPTION, ACCOUNT_ID, ACCOUNT_ID_CONTRA, DEBIT_CREDIT, AMOUNT,
                    ORGANIZATION_ID, TRAN_ID,
                    ROW_NUMBER() OVER (ORDER BY TRAN_DATE, TRAN_NO) as RowNum
                FROM dbo.LEDGER_VIEW WITH (NOLOCK)
                WHERE TRAN_DATE >= ? AND TRAN_DATE <= ? {org_where}
            )
            SELECT * FROM CTE WHERE RowNum > ? AND RowNum <= ?
        """
        cur.execute(paged_sql, base_params + [offset, offset + page_size])

        rows = []
        for r in cur.fetchall():
            org_id = (str(r[7]) if r[7] is not None else "").strip()
            rows.append({
                "tran_date": r[0].strftime("%d/%m/%Y") if r[0] else "",
                "tran_no": r[1] or "",
                "description": r[2] or "",
                "account_id": r[3] or "",
                "contra_account_id": r[4] or "",
                "debit_credit": r[5] or "",
                "amount": float(r[6] or 0),
                "org_id": org_id,
                "org_name": org_map.get(org_id, ""),
                "tran_id": (str(r[8]) if r[8] is not None else "").strip()
            })

        return jsonify({
            "status": "ok",
            "data": rows,
            "period_sums": {"deb": total_deb, "crd": total_crd},
            "pagination": {
                "total_rows": total_rows,
                "total_pages": max(1, (total_rows + page_size - 1) // page_size),
                "page": page
            }
        })
    except Exception as e:
        msg = str(e)
        logger.error(f"Error in BC007 get_journal: {msg}")
        return jsonify({"status": "error", "message": msg}), 500

@app.route("/api/account_details")
@with_db_lock
def get_account_details():
    try:
        f_date = request.args.get("from_date")
        t_date = request.args.get("to_date")
        account_id = request.args.get("account_id", "")
        org_ids = [v for v in request.args.get("org_ids", "").split(",") if v]
        
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 10000))
        # page_size = 0 ⇒ LẤY TOÀN BỘ (phục vụ xuất .xls giữ form: DOM phải có đủ mọi trang)
        export_all = page_size <= 0
        if export_all:
            page = 1

        if not account_id:
            return jsonify({"status": "error", "message": "Vui lòng chọn tài khoản!"}), 400

        from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
        to_dt = datetime.strptime(t_date, "%d/%m/%Y").date()
        first_day_of_year = date(from_dt.year, 1, 1).strftime("%Y%m%d")

        # Không chọn đơn vị ⇒ LOẠI đơn vị ngoài cây '00' (vd '66'), giống BC001/BC009/BC010/BC011.
        # Trước 15/08/2026 chỗ này để rỗng ⇒ báo cáo GỘP CẢ đơn vị ngoài cây → không tie được
        # với các báo cáo khác, và làm Bảng cân đối kế toán không cân.
        _oc, org_params = _org_filter_sql(org_ids, "ORGANIZATION_ID")
        org_where = (" AND " + _oc) if _oc else ""

        cur = get_connection().cursor()

        # Bộ lọc Tài khoản là ĐA CHỌN → phải dùng _acc_like_sql, không ghép chuỗi vào LIKE ? + '%'
        acc_clause, acc_params = _acc_like_sql(account_id)

        open_bal_deb = 0
        open_bal_crd = 0
        sql_open = f"""
            SELECT SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT ELSE 0 END),
                   SUM(CASE WHEN DEBIT_CREDIT='CRD' THEN AMOUNT ELSE 0 END)
            FROM dbo.BALANCE_VIEW WITH (NOLOCK)
            WHERE {acc_clause} AND TRAN_DATE = ? {org_where}
        """
        cur.execute(sql_open, acc_params + [first_day_of_year] + org_params)
        r_open = cur.fetchone()
        if r_open:
            open_bal_deb += float(r_open[0] or 0)
            open_bal_crd += float(r_open[1] or 0)

        if from_dt > date(from_dt.year, 1, 1):
            sql_lk = f"""
                SELECT SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT ELSE 0 END),
                       SUM(CASE WHEN DEBIT_CREDIT='CRD' THEN AMOUNT ELSE 0 END)
                FROM dbo.LEDGER_VIEW WITH (NOLOCK)
                WHERE {acc_clause} AND TRAN_DATE >= ? AND TRAN_DATE < ? {org_where}
            """
            cur.execute(sql_lk, acc_params + [first_day_of_year, from_dt.strftime("%Y%m%d")] + org_params)
            r_lk = cur.fetchone()
            if r_lk:
                open_bal_deb += float(r_lk[0] or 0)
                open_bal_crd += float(r_lk[1] or 0)

        base_params = acc_params + [from_dt.strftime("%Y%m%d"), to_dt.strftime("%Y%m%d")] + org_params
        
        offset = (page - 1) * page_size
        
        stats_sql = f"""
            WITH CTE AS (
                SELECT DEBIT_CREDIT, AMOUNT,
                       ROW_NUMBER() OVER (ORDER BY TRAN_DATE, TRAN_NO) as RowNum
                FROM dbo.LEDGER_VIEW WITH (NOLOCK)
                WHERE {acc_clause} AND TRAN_DATE >= ? AND TRAN_DATE <= ? {org_where}
            )
            SELECT 
                COUNT(*),
                SUM(CASE WHEN DEBIT_CREDIT='DEB' THEN AMOUNT ELSE 0 END),
                SUM(CASE WHEN DEBIT_CREDIT='CRD' THEN AMOUNT ELSE 0 END),
                SUM(CASE WHEN RowNum <= ? AND DEBIT_CREDIT='DEB' THEN AMOUNT ELSE 0 END),
                SUM(CASE WHEN RowNum <= ? AND DEBIT_CREDIT='CRD' THEN AMOUNT ELSE 0 END)
            FROM CTE
        """
        cur.execute(stats_sql, base_params + [offset, offset])
        s_row = cur.fetchone()
        
        total_rows = s_row[0] or 0
        total_deb = float(s_row[1] or 0)
        total_crd = float(s_row[2] or 0)
        offset_deb = float(s_row[3] or 0)
        offset_crd = float(s_row[4] or 0)

        paged_sql = f"""
            WITH CTE AS (
                SELECT 
                    TRAN_DATE, TRAN_NO, DESCRIPTION, ACCOUNT_ID_CONTRA, DEBIT_CREDIT, AMOUNT,
                    ROW_NUMBER() OVER (ORDER BY TRAN_DATE, TRAN_NO) as RowNum
                FROM dbo.LEDGER_VIEW WITH (NOLOCK)
                WHERE {acc_clause} AND TRAN_DATE >= ? AND TRAN_DATE <= ? {org_where}
            )
            SELECT * FROM CTE WHERE RowNum > ? AND RowNum <= ?
        """
        # export_all: cận trên = total_rows (đã đếm ở stats_sql) → lấy hết, không phân trang
        cur.execute(paged_sql, base_params + [offset, total_rows if export_all else offset + page_size])

        rows = []
        for r in cur.fetchall():
            rows.append({
                "tran_date": r[0].strftime("%d/%m/%Y") if r[0] else "",
                "tran_no": r[1] or "",
                "description": r[2] or "",
                "contra_account_id": r[3] or "",
                "debit_credit": r[4] or "",
                "amount": float(r[5] or 0)
            })

        return jsonify({
            "status": "ok",
            "opening_balance": {"deb": open_bal_deb, "crd": open_bal_crd},
            "offset_balance": {"deb": offset_deb, "crd": offset_crd},
            "period_sums": {"deb": total_deb, "crd": total_crd},
            "data": rows,
            "pagination": {
                "total_rows": total_rows,
                "total_pages": 1 if export_all else max(1, (total_rows + page_size - 1) // page_size),
                "page": page
            }
        })
    except Exception as e:
        msg = str(e)
        logger.error(f"Error in BC008 get_account_details: {msg}")
        return jsonify({"status": "error", "message": msg}), 500


# ============================================================
# BC012 — SỔ TIỀN MẶT VÀ TIỀN NGÂN HÀNG (nguồn: VOUCHER_VIEW)
#   - Mỗi tài khoản tiền (mặc định 111,112,113) là 1 "sổ" riêng:
#     Dư đầu kỳ (net phát sinh trước from_date) -> phát sinh Nợ/Có -> Dư cuối kỳ.
#   - VOUCHER_VIEW là view định khoản kép: mỗi dòng có ACCOUNT_ID_DEBIT + ACCOUNT_ID_CREDIT + AMOUNT,
#     nên TK đối ứng có sẵn. Phía Nợ thuộc TK tiền -> ghi Nợ (thu); phía Có -> ghi Có (chi);
#     dòng chuyển nội bộ giữa 2 TK tiền sinh 2 bút toán.
# ============================================================
# Cache 1 kết quả flat mới nhất để PHÂN TRANG (10000 dòng/trang) không phải dựng lại mỗi lần đổi trang.
_cashbook_cache = {}  # {cache_key: flat_list}


def _cashbook_key(f_date, t_date, acc_ids, contra_ids, tran_no, org_ids):
    db_name = (_db_cfg() or {}).get('database', 'N/A')
    return hashlib.md5("|".join([
        db_name, f_date, t_date, ",".join(acc_ids), ",".join(contra_ids), tran_no, ",".join(org_ids)
    ]).encode()).hexdigest()


def _build_cashbook_flat(from_dt, to_dt, acc_ids, contra_ids, tran_no, org_ids):
    """Dựng danh sách dòng hiển thị PHẲNG (head/row/cong/du/grand) + số dư luỹ kế cho sổ quỹ BC012."""
    _oc, org_params = _org_filter_sql(org_ids, "ORGANIZATION_ID")
    org_where = (" AND " + _oc) if _oc else ""
    cur = get_connection().cursor()

    acc_name = {}
    try:
        cur.execute("SELECT ACCOUNT_ID, ACCOUNT_NAME FROM dbo.DM_ACCOUNT WITH (NOLOCK)")
        acc_name = {(r[0] or '').strip(): (r[1] or '').strip() for r in cur.fetchall()}
    except Exception:
        pass

    opening = {a: 0.0 for a in acc_ids}
    open_sel = ", ".join(
        "SUM(CASE WHEN ACCOUNT_ID_DEBIT LIKE ? THEN AMOUNT ELSE 0 END) - SUM(CASE WHEN ACCOUNT_ID_CREDIT LIKE ? THEN AMOUNT ELSE 0 END)"
        for _ in acc_ids)
    open_acc_clause = " OR ".join(["ACCOUNT_ID_DEBIT LIKE ?"] * len(acc_ids) + ["ACCOUNT_ID_CREDIT LIKE ?"] * len(acc_ids))
    open_params = []
    for a in acc_ids:
        open_params += [a + "%", a + "%"]
    open_params += [from_dt.strftime("%Y%m%d")]
    open_params += [a + "%" for a in acc_ids] * 2
    open_params += org_params
    cur.execute(f"""
        SELECT {open_sel}
        FROM dbo.VOUCHER_VIEW WITH (NOLOCK)
        WHERE TRAN_DATE < ? AND ({open_acc_clause}){org_where}
    """, open_params)
    orow = cur.fetchone()
    if orow:
        for i, a in enumerate(acc_ids):
            opening[a] = float(orow[i] or 0)

    acc_like_clause = " OR ".join(["ACCOUNT_ID_DEBIT LIKE ?"] * len(acc_ids) +
                                  ["ACCOUNT_ID_CREDIT LIKE ?"] * len(acc_ids))
    params = [from_dt.strftime("%Y%m%d"), to_dt.strftime("%Y%m%d")] + [a + "%" for a in acc_ids] * 2 + org_params
    contra_where = ""
    if contra_ids:
        contra_where = " AND (" + " OR ".join(["ACCOUNT_ID_DEBIT LIKE ?", "ACCOUNT_ID_CREDIT LIKE ?"] * len(contra_ids)) + ")"
        for c in contra_ids:
            params += [c + "%", c + "%"]
    tran_where = ""
    if tran_no:
        tran_where = " AND TRAN_NO LIKE ?"
        params.append("%" + tran_no + "%")

    cur.execute(f"""
        SELECT TRAN_DATE, TRAN_NO, DESCRIPTION, ACCOUNT_ID_DEBIT, ACCOUNT_ID_CREDIT, AMOUNT
        FROM dbo.VOUCHER_VIEW WITH (NOLOCK)
        WHERE TRAN_DATE >= ? AND TRAN_DATE <= ? AND ({acc_like_clause}){org_where}{contra_where}{tran_where}
        ORDER BY TRAN_DATE, TRAN_NO, PR_KEY_CTU
    """, params)

    buckets = {acc: [] for acc in acc_ids}
    for row in cur.fetchall():
        tdate = row[0].strftime("%d/%m/%Y") if row[0] else ""
        tno   = row[1] or ""
        desc  = row[2] or ""
        deb_acc = (row[3] or "").strip()
        crd_acc = (row[4] or "").strip()
        amt   = float(row[5] or 0)
        for acc in acc_ids:
            if deb_acc.startswith(acc):
                contra = crd_acc
                if (not contra_ids) or any(contra.startswith(c) for c in contra_ids):
                    buckets[acc].append((tdate, tno, desc, contra, amt, 0.0))
            if crd_acc.startswith(acc):
                contra = deb_acc
                if (not contra_ids) or any(contra.startswith(c) for c in contra_ids):
                    buckets[acc].append((tdate, tno, desc, contra, 0.0, amt))

    flat = []
    ngroups = len(acc_ids)
    g_pd = g_pc = g_close = 0.0
    for acc in acc_ids:
        rows = buckets[acc]
        open_net = opening.get(acc, 0.0)
        flat.append({"t": "head", "account_id": acc, "account_name": acc_name.get(acc, ""), "opening": open_net})
        running = open_net
        sum_deb = sum_crd = 0.0
        for i, (tdate, tno, desc, contra, deb, crd) in enumerate(rows):
            running += deb - crd
            sum_deb += deb; sum_crd += crd
            flat.append({"t": "row", "account_id": acc, "stt": i + 1, "tran_date": tdate, "tran_no": tno,
                         "description": desc, "contra_account_id": contra, "debit": deb, "credit": crd, "balance": running})
        close_net = open_net + sum_deb - sum_crd
        flat.append({"t": "cong", "account_id": acc, "sum_deb": sum_deb, "sum_crd": sum_crd})
        flat.append({"t": "du", "account_id": acc, "close": close_net})
        g_pd += sum_deb; g_pc += sum_crd; g_close += close_net
    if ngroups > 1:
        flat.append({"t": "grand", "period_deb": g_pd, "period_crd": g_pc, "close": g_close})
    return flat


def _cashbook_flat_cached(f_date, t_date, acc_ids, contra_ids, tran_no, org_ids):
    from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
    to_dt   = datetime.strptime(t_date, "%d/%m/%Y").date()
    # Cache key PHẢI kèm đơn vị-được-phép của tài khoản: 2 user khác quyền, cùng tham số lọc,
    # nếu dùng chung key sẽ trả nhầm dữ liệu của nhau (lỗ bảo mật do cache).
    _allowed = _current_allowed_orgs()
    _akey = tuple(sorted(_allowed)) if _allowed is not None else None
    key = (_cashbook_key(f_date, t_date, acc_ids, contra_ids, tran_no, org_ids), _akey)
    flat = _cashbook_cache.get(key)
    if flat is None:
        flat = _build_cashbook_flat(from_dt, to_dt, acc_ids, contra_ids, tran_no, org_ids)
        _cashbook_cache.clear()
        _cashbook_cache[key] = flat
    return flat


@app.route("/api/cash_book")
@with_db_lock
def get_cash_book():
    try:
        f_date = request.args.get("from_date")
        t_date = request.args.get("to_date")
        acc_ids = [v.strip() for v in request.args.get("acc_ids", "").split(",") if v.strip()] or ["111", "112", "113"]
        contra_ids = [v.strip() for v in request.args.get("contra_acc_ids", "").split(",") if v.strip()]
        tran_no = request.args.get("tran_no", "").strip()
        org_ids = [v for v in request.args.get("org_ids", "").split(",") if v]
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 10000))

        flat = _cashbook_flat_cached(f_date, t_date, acc_ids, contra_ids, tran_no, org_ids)
        total = len(flat)
        # page_size = 0 ⇒ LẤY TOÀN BỘ (phục vụ xuất .xls giữ form: DOM phải có đủ mọi trang)
        if page_size <= 0:
            return jsonify({"status": "ok", "rows": flat,
                            "pagination": {"total_rows": total, "total_pages": 1, "page": 1}})
        total_pages = max(1, (total + page_size - 1) // page_size)
        page = max(1, min(page, total_pages))
        offset = (page - 1) * page_size
        return jsonify({"status": "ok", "rows": flat[offset:offset + page_size],
                        "pagination": {"total_rows": total, "total_pages": total_pages, "page": page}})
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        logger.error(f"Error in BC012 get_cash_book: {msg}")
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


@app.route("/api/cash_book/export_csv")
@with_db_lock
def get_cash_book_export_csv():
    """Xuất TOÀN BỘ sổ quỹ BC012 ra CSV (UTF-8 BOM) — chịu được số dòng rất lớn, không phụ thuộc DOM/phân trang."""
    try:
        f_date = request.args.get("from_date")
        t_date = request.args.get("to_date")
        acc_ids = [v.strip() for v in request.args.get("acc_ids", "").split(",") if v.strip()] or ["111", "112", "113"]
        contra_ids = [v.strip() for v in request.args.get("contra_acc_ids", "").split(",") if v.strip()]
        tran_no = request.args.get("tran_no", "").strip()
        org_ids = [v for v in request.args.get("org_ids", "").split(",") if v]
        flat = _cashbook_flat_cached(f_date, t_date, acc_ids, contra_ids, tran_no, org_ids)
        body = _cashbook_csv_stream(flat)
        fname = f"BC012_So_Tien_Mat_Va_Tien_Ngan_Hang_{f_date.replace('/','')}-{t_date.replace('/','')}.csv"
        from flask import Response
        return Response(body, mimetype="text/csv; charset=utf-8",
                        headers={"Content-Disposition": f"attachment; filename={fname}"})
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


@app.route("/api/vat_sales_report")
@with_db_lock
def get_vat_sales_report():
    """Báo cáo 6.2 - BẢNG KÊ HÓA ĐƠN, CHỨNG TỪ HÀNG HÓA, DỊCH VỤ BÁN RA (Tổng hợp & Chi tiết)."""
    try:
        f_date = request.args.get("from_date")
        t_date = request.args.get("to_date")
        mode = request.args.get("mode", "detail")  # 'detail' | 'summary'
        org_ids = [v for v in request.args.get("org_ids", "").split(",") if v]
        acc_ids = [v.strip() for v in request.args.get("acc_ids", "").split(",") if v.strip()]
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 1000))
        # page_size = 0 ⇒ LẤY TOÀN BỘ (phục vụ xuất .xls giữ form: DOM phải có đủ mọi trang)
        export_all = page_size <= 0
        if not export_all and page_size > 1000: page_size = 1000

        if not f_date or not t_date:
            return jsonify({"status": "error", "message": "Thiếu từ ngày / đến ngày"}), 400

        f_dt = datetime.strptime(f_date, "%d/%m/%Y").strftime("%Y%m%d")
        t_dt = datetime.strptime(t_date, "%d/%m/%Y").strftime("%Y%m%d")

        _oc, _op = _org_filter_sql(org_ids, "ORGANIZATION_ID")
        org_where = (" AND " + _oc) if _oc else ""

        acc_where = ""
        acc_params = []
        if acc_ids:
            acc_where = " AND (" + " OR ".join(["ACCOUNT_ID LIKE ?"] * len(acc_ids)) + ")"
            acc_params = [a + "%" for a in acc_ids]

        params = [f_dt, t_dt] + list(_op) + list(acc_params)
        cur = get_connection().cursor()

        # 1. Tính tổng số tiền (luôn giống nhau cho cả Tổng hợp & Chi tiết)
        totals_sql = f"""
            SELECT 
                ISNULL(SUM(AMOUNT_ITEM), 0),
                ISNULL(SUM(CASE WHEN VAT_TAX_RATE > 0 THEN AMOUNT_ITEM ELSE 0 END), 0),
                ISNULL(SUM(AMOUNT), 0)
            FROM dbo.VAT_TRANSACTION_VIEW WITH (NOLOCK)
            WHERE DEBIT_CREDIT = 'CRD'
              AND VAT_TRAN_DATE >= ? AND VAT_TRAN_DATE <= ?{org_where}{acc_where}
        """
        cur.execute(totals_sql, params)
        tot_row = cur.fetchone()
        total_amount_item = float(tot_row[0] or 0) if tot_row else 0.0
        taxable_amount_item = float(tot_row[1] or 0) if tot_row else 0.0
        total_vat_amount = float(tot_row[2] or 0) if tot_row else 0.0

        # 2. Đếm số dòng (Tổng hợp đếm theo Số HĐ, Chi tiết đếm từng mặt hàng)
        if mode == "summary":
            count_sql = f"""
                SELECT COUNT(*) FROM (
                    SELECT VAT_TRAN_SERIE, VAT_TRAN_NO
                    FROM dbo.VAT_TRANSACTION_VIEW WITH (NOLOCK)
                    WHERE DEBIT_CREDIT = 'CRD'
                      AND VAT_TRAN_DATE >= ? AND VAT_TRAN_DATE <= ?{org_where}{acc_where}
                    GROUP BY VAT_TRAN_SERIE, VAT_TRAN_NO, VAT_TRAN_DATE, PR_DETAIL_NAME, TAX_FILE_NUMBER, ACCOUNT_ID
                ) AS Grp
            """
        else:
            count_sql = f"""
                SELECT COUNT(*)
                FROM dbo.VAT_TRANSACTION_VIEW WITH (NOLOCK)
                WHERE DEBIT_CREDIT = 'CRD'
                  AND VAT_TRAN_DATE >= ? AND VAT_TRAN_DATE <= ?{org_where}{acc_where}
            """
        cur.execute(count_sql, params)
        c_row = cur.fetchone()
        total_rows = c_row[0] if c_row else 0

        if export_all:
            total_pages, page = 1, 1
            start_row, end_row = 0, total_rows
        else:
            total_pages = max(1, (total_rows + page_size - 1) // page_size)
            page = max(1, min(page, total_pages))
            start_row = (page - 1) * page_size
            end_row = page * page_size

        # 3. Phân trang SQL Server
        if mode == "summary":
            page_sql = f"""
                SELECT * FROM (
                    SELECT 
                        ISNULL(VAT_TRAN_SERIE, '') AS serie,
                        ISNULL(VAT_TRAN_NO, '') AS no,
                        VAT_TRAN_DATE AS date_raw,
                        ISNULL(PR_DETAIL_NAME, '') AS seller,
                        ISNULL(TAX_FILE_NUMBER, '') AS tax_code,
                        N'Bán hàng hóa, dịch vụ' AS item,
                        ISNULL(SUM(AMOUNT_ITEM), 0) AS amount_item,
                        ISNULL(MAX(VAT_TAX_RATE), 0) AS tax_rate,
                        ISNULL(SUM(AMOUNT), 0) AS vat_amount,
                        N'' AS comments,
                        ISNULL(ACCOUNT_ID, '') AS account_id,
                        ROW_NUMBER() OVER (ORDER BY VAT_TRAN_DATE, VAT_TRAN_NO) AS RowNum
                    FROM dbo.VAT_TRANSACTION_VIEW WITH (NOLOCK)
                    WHERE DEBIT_CREDIT = 'CRD'
                      AND VAT_TRAN_DATE >= ? AND VAT_TRAN_DATE <= ?{org_where}{acc_where}
                    GROUP BY VAT_TRAN_SERIE, VAT_TRAN_NO, VAT_TRAN_DATE, PR_DETAIL_NAME, TAX_FILE_NUMBER, ACCOUNT_ID
                ) AS Paged
                WHERE RowNum > ? AND RowNum <= ?
                ORDER BY RowNum
            """
        else:
            page_sql = f"""
                SELECT * FROM (
                    SELECT 
                        ISNULL(VAT_TRAN_SERIE, '') AS serie,
                        ISNULL(VAT_TRAN_NO, '') AS no,
                        VAT_TRAN_DATE AS date_raw,
                        ISNULL(PR_DETAIL_NAME, '') AS seller,
                        ISNULL(TAX_FILE_NUMBER, '') AS tax_code,
                        ISNULL(ITEM_NAME, '') AS item,
                        ISNULL(AMOUNT_ITEM, 0) AS amount_item,
                        ISNULL(VAT_TAX_RATE, 0) AS tax_rate,
                        ISNULL(AMOUNT, 0) AS vat_amount,
                        ISNULL(COMMENTS, '') AS comments,
                        ISNULL(ACCOUNT_ID, '') AS account_id,
                        ROW_NUMBER() OVER (ORDER BY VAT_TAX_RATE, VAT_TRAN_DATE, VAT_TRAN_NO) AS RowNum
                    FROM dbo.VAT_TRANSACTION_VIEW WITH (NOLOCK)
                    WHERE DEBIT_CREDIT = 'CRD'
                      AND VAT_TRAN_DATE >= ? AND VAT_TRAN_DATE <= ?{org_where}{acc_where}
                ) AS Paged
                WHERE RowNum > ? AND RowNum <= ?
                ORDER BY RowNum
            """

        cur.execute(page_sql, params + [start_row, end_row])
        rows = []
        for r in cur.fetchall():
            rows.append({
                "serie": (r[0] or '').strip(),
                "no": (r[1] or '').strip(),
                "date": r[2].strftime("%d/%m/%Y") if r[2] else "",
                "seller": (r[3] or '').strip(),
                "tax_code": (r[4] or '').strip(),
                "item": (r[5] or '').strip(),
                "amount_item": float(r[6] or 0),
                "tax_rate": float(r[7] or 0),
                "tax_amount": float(r[8] or 0),
                "comments": (r[9] or '').strip(),
                "account_id": (r[10] or '').strip()
            })

        totals = {
            "total_amount_item": total_amount_item,
            "taxable_amount_item": taxable_amount_item,
            "total_vat_amount": total_vat_amount
        }
        pagination = {
            "total_rows": total_rows,
            "total_pages": total_pages,
            "page": page,
            "page_size": page_size
        }

        return jsonify({"status": "ok", "data": rows, "totals": totals, "pagination": pagination})
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        logger.error(f"Error in BC013 get_vat_sales_report: {msg}")
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


# ---------------------------------------------------------------------
# BC015 — BÁO CÁO BÁN HÀNG THEO NGUỒN ĐƠN
# ---------------------------------------------------------------------
# Ánh xạ cột: đã SUM đối chiếu form gốc T1/2026 (dòng ShopeeFood + 4 đơn vị, khớp 8/8).
# ⚠️ ĐỪNG tin tên cột "nghe hợp lý": chiết khấu KHÔNG phải DISCOUNT2_AMOUNT và giảm giá
#    KHÔNG phải DISCOUNT_AMOUNT — hai cột đó lệch so với form gốc. Cột đúng là bản REAL_*.
SALE_SOURCE_MONEY_COLS = [
    ("amount",     "AMOUNT"),                    # Tiền hàng
    ("discount2",  "REAL_DISCOUNT2_AMOUNT"),     # Chiết khấu
    ("discount",   "REAL_DISCOUNT_AMOUNT"),      # Giảm giá
    ("tax",        "VAT_TAX_AMOUNT"),            # Tiền thuế
    ("voucher",    "LUX_TAX_AMOUNT"),            # Voucher
    ("commission", "EXPORT_TAX_AMOUNT"),         # Hoa hồng
    ("income",     "INCOME_AMOUNT"),             # Doanh thu
    ("total",      "TOTAL_AMOUNT"),              # Tổng tiền
]


@app.route("/api/sale_by_source")
@with_db_lock
def get_sale_by_source():
    """BC015 — Bán hàng theo nguồn đơn. Group cấp 1 = nguồn đơn (EXTRA_ID_2), cấp 2 = đơn vị,
    mode='detail' thêm dòng chi tiết theo ngày. Chỉ lấy chứng từ STATUS='POSTED'."""
    try:
        f_date = request.args.get("from_date")
        t_date = request.args.get("to_date")
        mode = request.args.get("mode", "summary")   # 'summary' | 'detail'
        org_ids = [v for v in request.args.get("org_ids", "").split(",") if v]
        source_ids = [v for v in request.args.get("source_ids", "").split(",") if v]
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 500))
        export_all = page_size <= 0        # page_size=0 ⇒ toàn bộ, phục vụ xuất .xls giữ form

        if not f_date or not t_date:
            return jsonify({"status": "error", "message": "Thiếu từ ngày / đến ngày"}), 400

        f_dt = datetime.strptime(f_date, "%d/%m/%Y").strftime("%Y%m%d")
        # TRAN_DATE là smalldatetime: dùng "< ngày kế tiếp", KHÔNG dùng <= mốc 00:00:00
        # (bẫy cũ: lọc bằng BETWEEN làm mất trọn ngày cuối kỳ).
        t_dt = (datetime.strptime(t_date, "%d/%m/%Y") + timedelta(days=1)).strftime("%Y%m%d")

        _oc, _op = _org_filter_sql(org_ids, "S.ORGANIZATION_ID")
        org_where = (" AND " + _oc) if _oc else ""

        src_where, src_params = "", []
        if source_ids:
            src_where = " AND S.EXTRA_ID_2 IN (" + ",".join(["?"] * len(source_ids)) + ")"
            src_params = list(source_ids)

        # Thứ tự params phải ĐÚNG thứ tự dấu ? trong chuỗi SQL: status, from, to, org, source.
        params = ["POSTED", f_dt, t_dt] + list(_op) + src_params

        sums = ", ".join(f"ISNULL(SUM(S.{col}), 0)" for _, col in SALE_SOURCE_MONEY_COLS)
        day_expr = "CONVERT(VARCHAR(8), S.TRAN_DATE, 112)"
        day_col = f", {day_expr}" if mode == "detail" else ""

        sql = f"""
            SELECT S.EXTRA_ID_2, E.EXTRA_NAME_2, S.ORGANIZATION_ID, O.ORGANIZATION_NAME{day_col},
                   {sums}
            FROM dbo.SALE_VIEW S WITH (NOLOCK)
            LEFT JOIN dbo.DM_EXTRA_2 E WITH (NOLOCK)
                   ON CAST(E.EXTRA_ID_2 AS NVARCHAR(100)) = S.EXTRA_ID_2
            LEFT JOIN dbo.DM_ORGANIZATION O WITH (NOLOCK)
                   ON O.ORGANIZATION_ID = S.ORGANIZATION_ID
            WHERE S.STATUS = ? AND S.TRAN_DATE >= ? AND S.TRAN_DATE < ?{org_where}{src_where}
            GROUP BY S.EXTRA_ID_2, E.EXTRA_NAME_2, S.ORGANIZATION_ID, O.ORGANIZATION_NAME{day_col}
            ORDER BY CASE WHEN ISNULL(S.EXTRA_ID_2, '') = '' THEN 1 ELSE 0 END,
                     S.EXTRA_ID_2, S.ORGANIZATION_ID{day_col}
        """
        cur = get_connection().cursor()
        cur.execute(sql, params)
        db_rows = cur.fetchall()

        keys = [k for k, _ in SALE_SOURCE_MONEY_COLS]
        nfix = 4 + (1 if mode == "detail" else 0)   # số cột khoá đứng trước khối tiền

        def zeros():
            return {k: 0.0 for k in keys}

        def add(dst, src):
            for k in keys:
                dst[k] += src[k]

        # Dựng cây nguồn đơn → đơn vị → (ngày), giữ nguyên thứ tự SQL đã ORDER BY.
        tree, order = {}, []
        for r in db_rows:
            sid = (r[0] or "").strip()
            sname = (r[1] or "").strip() or ("(không có nguồn đơn)" if not sid else sid)
            oid = (r[2] or "").strip()
            oname = (r[3] or "").strip() or oid
            money = {k: float(r[nfix + i] or 0) for i, k in enumerate(keys)}

            if sid not in tree:
                tree[sid] = {"name": sname, "sum": zeros(), "orgs": {}, "org_order": []}
                order.append(sid)
            node = tree[sid]
            add(node["sum"], money)
            if oid not in node["orgs"]:
                node["orgs"][oid] = {"name": oname, "sum": zeros(), "days": []}
                node["org_order"].append(oid)
            onode = node["orgs"][oid]
            add(onode["sum"], money)
            if mode == "detail":
                d = (r[4] or "").strip()          # 'YYYYMMDD' — đã CONVERT ở SQL, không phải đối tượng ngày
                ngay = f"{d[6:8]}/{d[4:6]}/{d[0:4]}" if len(d) == 8 else d
                onode["days"].append({"date": ngay, **money})

        # Ẩn dòng có TOÀN BỘ khối tiền = 0 (đơn vị có chứng từ POSTED nhưng không phát sinh
        # số nào). Tổng cộng không đổi vì các dòng bị bỏ đều bằng 0.
        def all_zero(d):
            return all(round(d[k], 2) == 0 for k in keys)

        flat, grand = [], zeros()
        for sid in order:
            node = tree[sid]
            add(grand, node["sum"])
            if all_zero(node["sum"]):
                continue
            flat.append({"t": "source", "source_id": sid, "source_name": node["name"], **node["sum"]})
            for oid in node["org_order"]:
                onode = node["orgs"][oid]
                if all_zero(onode["sum"]):
                    continue
                flat.append({"t": "org", "org_id": oid, "org_name": onode["name"], **onode["sum"]})
                for d in onode["days"]:
                    if all_zero(d):
                        continue
                    flat.append({"t": "day", **d})

        total_rows = len(flat)
        if export_all:
            total_pages, page, rows = 1, 1, flat
        else:
            total_pages = max(1, (total_rows + page_size - 1) // page_size)
            page = max(1, min(page, total_pages))
            rows = flat[(page - 1) * page_size: page * page_size]

        return jsonify({
            "status": "ok",
            "rows": rows,
            "totals": grand,
            "pagination": {"total_rows": total_rows, "total_pages": total_pages,
                           "page": page, "page_size": page_size}
        })
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        logger.error(f"Error in BC015 get_sale_by_source: {msg}")
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


# =====================================================================
# BC016 — NHẬP XUẤT TỒN NHÀ HÀNG
# =====================================================================
# Nguồn: WAREHOUSE_VIEW (KHÔNG dùng bảng WAREHOUSE) — VIEW lọc sẵn
# DM_ITEM.IS_WAREHOUSE_BALANCE = 1, tức chỉ hàng có quản lý tồn kho.
# Đo 05/09/2026 trên IACC_CHULONG: base table 691.469 dòng / VIEW 494.819 dòng,
# tồn lệch 1,98 triệu đơn vị. Lấy nhầm base table là sai toàn bộ báo cáo.

# Thứ tự cột bám theo form gốc "5.7 - BÁO CÁO NHẬP XUẤT TỒN NHÀ HÀNG" của iPOS
# để đối chiếu được từng khối. TRAN_ID lạ (DB khác, hoặc iPOS thêm mới) xếp sau, theo alphabet.
NXT_TRAN_ORDER_IN = ["NM", "MNB", "NMND", "NMTU", "NKHO", "NSP", "NDCNB", "NDC"]
NXT_TRAN_ORDER_OUT = ["BH", "BHVAT", "BHK", "XDCNB", "BNB", "XKHOSXBTP", "XKHO",
                      "XKHODLK", "XKHOHN", "XHUY", "XSC", "XKHOKK", "XDC"]


def _nxt_open_cutoff(from_dt):
    """Mốc dồn tồn đầu kỳ = 01/01 của NĂM TÀI CHÍNH chứa from_date — KHÔNG dồn từ đầu dữ liệu.

    Luật này không có trong tài liệu nào, đo ngày 05/09/2026 mới ra: IACC_CHULONG còn 53 dòng
    phát sinh tháng 12/2025 (798.274,60 SL / 30.333.901 đ). Gộp chúng vào tồn đầu kỳ 2026 thì
    lệch form gốc đúng bằng chừng đó; cắt từ 01/01 thì khớp form gốc 0 tuyệt đối trên cả 9 chỉ tiêu.
    """
    return date(from_dt.year, 1, 1)


@app.route("/api/nxt")
@with_db_lock
def get_nxt():
    """BC016 — Nhập xuất tồn nhà hàng.

    Đầu kỳ / cuối kỳ là số tổng; nhập và xuất trong kỳ tách thành CỘT ĐỘNG theo từng
    TRAN_ID, mỗi cột 2 ô (số lượng + giá trị). Cột nào cả kỳ không có số thì không trả về.
    Dòng = mặt hàng; gom nhóm theo `group_by`:
      'class'     -> nhóm hàng hoá (dòng = mặt hàng gộp toàn công ty)
      'warehouse' -> kho           (dòng = mặt hàng trong từng kho, giống form gốc)
    """
    try:
        f_date = request.args.get("from_date")
        t_date = request.args.get("to_date")
        if not f_date or not t_date:
            return jsonify({"status": "error", "message": "Thiếu từ ngày / đến ngày"}), 400

        group_by = request.args.get("group_by", "class")
        if group_by not in ("class", "warehouse"):
            group_by = "class"
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 0))   # đếm theo DÒNG CHI TIẾT, 0 = lấy hết
        export_all = page_size <= 0

        try:
            from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
            to_dt = datetime.strptime(t_date, "%d/%m/%Y").date()
        except ValueError:
            return jsonify({"status": "error",
                            "message": "Ngày phải theo định dạng dd/mm/yyyy"}), 400
        # Kỳ ngược thì CHẶN, đừng trả số: mọi phát sinh sẽ rơi hết vào nhánh '_OPEN'
        # ⇒ báo cáo ra một bảng chỉ có tồn đầu, trông vẫn "chạy được" mà vô nghĩa.
        if to_dt < from_dt:
            return jsonify({"status": "error",
                            "message": "Đến ngày phải lớn hơn hoặc bằng Từ ngày"}), 400
        y_start = _nxt_open_cutoff(from_dt).strftime("%Y%m%d")
        f_dt = from_dt.strftime("%Y%m%d")
        # TRAN_DATE là smalldatetime => chặn trên bằng "< ngày kế tiếp", KHÔNG dùng <= mốc 00:00:00
        # (Bẫy 4: dùng <= sẽ mất trọn ngày cuối kỳ).
        t_next = (to_dt + timedelta(days=1)).strftime("%Y%m%d")

        # -- Bộ lọc ------------------------------------------------------------
        # Thứ tự params phải ĐÚNG thứ tự dấu ? trong chuỗi SQL (Bẫy 5): CASE trong SELECT
        # của subquery đứng TRƯỚC mệnh đề WHERE, nên f_dt đi đầu, rồi mới tới wparams.
        where = ["W.TRAN_DATE >= ?", "W.TRAN_DATE < ?"]
        wparams = [y_start, t_next]

        org_ids = [v for v in request.args.get("org_ids", "").split(",") if v]
        _oc, _op = _org_filter_sql(org_ids, "W.ORGANIZATION_ID")
        if _oc:
            where.append(_oc)
            wparams.extend(_op)

        for field, arg in [("W.WAREHOUSE_ID", "wh_ids"),
                           ("W.ITEM_ID", "item_ids"),
                           ("W.ITEM_CLASS_ID", "class_ids")]:
            vals = [v for v in request.args.get(arg, "").split(",") if v]
            if vals:
                where.append(f"{field} IN ({','.join(['?'] * len(vals))})")
                wparams.extend(vals)

        gkey_sql = "W.WAREHOUSE_ID" if group_by == "warehouse" else "W.ITEM_CLASS_ID"

        # ⚡ GROUP BY chỉ gồm 4 khoá NGẮN. Bản đầu còn kéo theo GNAME (tên kho/tên nhóm,
        # nvarchar dài) + MAX(ITEM_NAME) + MAX(UNIT_ID) và join DM_ITEM_CLASS: kỳ cả năm
        # mất 66–74 giây. Tên lấy riêng từ danh mục (đã đối chiếu: 0 lệch trên cả ba cột
        # ITEM_NAME / UNIT_ID_WH / WAREHOUSE_NAME giữa VIEW và DM_*), nên bỏ ra khỏi
        # phép gộp là đúng số mà nhanh hơn hẳn.
        sql = f"""
            SELECT GKEY, ITEM_ID, COLKEY, IR, SUM(QTY) AS QTY, SUM(AMT) AS AMT
            FROM (
                SELECT ISNULL({gkey_sql}, '') AS GKEY, W.ITEM_ID,
                       CASE WHEN W.TRAN_DATE < ? THEN '_OPEN' ELSE W.TRAN_ID END AS COLKEY,
                       W.ISSUE_RECEIVE AS IR,
                       ISNULL(W.QUANTITY, 0) AS QTY, ISNULL(W.AMOUNT, 0) AS AMT
                FROM dbo.WAREHOUSE_VIEW W WITH (NOLOCK)
                WHERE {' AND '.join(where)}
            ) T
            GROUP BY GKEY, ITEM_ID, COLKEY, IR
        """
        cur = get_connection().cursor()
        cur.execute(sql, [f_dt] + wparams)
        db_rows = cur.fetchall()

        # Danh mục tra tên — đều là bảng nhỏ (861 mặt hàng / 87 kho / 7 nhóm / vài chục loại CT).
        cur.execute("SELECT ITEM_ID, ITEM_NAME, UNIT_ID FROM dbo.DM_ITEM WITH (NOLOCK)")
        item_info = {(r[0] or '').strip(): ((r[1] or '').strip(), (r[2] or '').strip())
                     for r in cur.fetchall()}
        if group_by == "warehouse":
            cur.execute("SELECT WAREHOUSE_ID, WAREHOUSE_NAME FROM dbo.DM_WAREHOUSE WITH (NOLOCK)")
        else:
            cur.execute("SELECT ITEM_CLASS_ID, ITEM_CLASS_NAME FROM dbo.DM_ITEM_CLASS WITH (NOLOCK)")
        group_names = {(r[0] or '').strip(): (r[1] or '').strip() for r in cur.fetchall()}

        cur.execute("SELECT CAST(TRAN_ID AS NVARCHAR(100)), TRAN_NAME FROM dbo.SYS_TRAN WITH (NOLOCK)")
        tran_names = {(r[0] or '').strip(): (r[1] or '').strip() for r in cur.fetchall()}

        # -- Gom cây: nhóm -> mặt hàng -----------------------------------------
        groups, gorder = {}, []
        used_in, used_out = {}, {}     # TRAN_ID -> True nếu có phát sinh khác 0

        for r in db_rows:
            gkey = (r[0] or '').strip()
            item_id = (r[1] or '').strip()
            colkey = (r[2] or '').strip()
            ir = (r[3] or '').strip()
            qty, amt = float(r[4] or 0), float(r[5] or 0)

            if gkey not in groups:
                groups[gkey] = {"key": gkey, "name": group_names.get(gkey) or gkey,
                                "items": {}, "iorder": []}
                gorder.append(gkey)
            g = groups[gkey]
            if item_id not in g["items"]:
                iname, iunit = item_info.get(item_id, ('', ''))
                g["items"][item_id] = {"item_name": iname or item_id, "unit": iunit,
                                       "open_qty": 0.0, "open_amt": 0.0, "in": {}, "out": {}}
                g["iorder"].append(item_id)
            it = g["items"][item_id]

            if colkey == "_OPEN":
                # Tồn đầu kỳ: nhập cộng, xuất trừ.
                sign = 1.0 if ir == "N" else -1.0
                it["open_qty"] += sign * qty
                it["open_amt"] += sign * amt
            else:
                bucket, used = ("in", used_in) if ir == "N" else ("out", used_out)
                cell = it[bucket].setdefault(colkey, [0.0, 0.0])
                cell[0] += qty
                cell[1] += amt
                if round(qty, 4) != 0 or round(amt, 2) != 0:
                    used[colkey] = True

        # -- Cột động: chỉ giữ TRAN_ID thực sự có số ---------------------------
        def order_cols(used, preferred):
            known = [t for t in preferred if t in used]
            rest = sorted(t for t in used if t not in preferred)
            return [{"tran_id": t, "name": tran_names.get(t, t)} for t in known + rest]

        cols_in = order_cols(used_in, NXT_TRAN_ORDER_IN)
        cols_out = order_cols(used_out, NXT_TRAN_ORDER_OUT)
        keys_in = [c["tran_id"] for c in cols_in]
        keys_out = [c["tran_id"] for c in cols_out]

        # -- Dựng dòng + cộng tổng ---------------------------------------------
        TOT_FIELDS = ("open_qty", "open_amt", "in_qty", "in_amt",
                      "out_qty", "out_amt", "close_qty", "close_amt")

        def blank_tot():
            d = {f: 0.0 for f in TOT_FIELDS}
            d["in"] = {k: [0.0, 0.0] for k in keys_in}
            d["out"] = {k: [0.0, 0.0] for k in keys_out}
            return d

        def add_tot(dst, src):
            for f in TOT_FIELDS:
                dst[f] += src[f]
            for b, ks in (("in", keys_in), ("out", keys_out)):
                for k in ks:
                    c = src[b].get(k)
                    if c:
                        dst[b][k][0] += c[0]
                        dst[b][k][1] += c[1]

        out_groups, grand = [], blank_tot()
        for gk in gorder:
            g = groups[gk]
            gtot = blank_tot()
            rows = []
            for iid in g["iorder"]:
                it = g["items"][iid]
                in_qty = sum(it["in"].get(k, (0.0, 0.0))[0] for k in keys_in)
                in_amt = sum(it["in"].get(k, (0.0, 0.0))[1] for k in keys_in)
                out_qty = sum(it["out"].get(k, (0.0, 0.0))[0] for k in keys_out)
                out_amt = sum(it["out"].get(k, (0.0, 0.0))[1] for k in keys_out)
                row = {
                    "item_id": iid, "item_name": it["item_name"], "unit": it["unit"],
                    "open_qty": it["open_qty"], "open_amt": it["open_amt"],
                    "in_qty": in_qty, "in_amt": in_amt,
                    "out_qty": out_qty, "out_amt": out_amt,
                    "close_qty": it["open_qty"] + in_qty - out_qty,
                    "close_amt": it["open_amt"] + in_amt - out_amt,
                    "in": {k: it["in"].get(k, [0.0, 0.0]) for k in keys_in},
                    "out": {k: it["out"].get(k, [0.0, 0.0]) for k in keys_out},
                }
                add_tot(gtot, row)
                # Ẩn dòng câm tuyệt đối (không tồn đầu, không phát sinh, không tồn cuối).
                # Dòng chỉ có tồn đầu = tồn cuối VẪN hiện, bỏ đi là tổng tồn cuối hụt.
                if all(round(row[f], 4) == 0 for f in TOT_FIELDS):
                    continue
                rows.append(row)
            add_tot(grand, gtot)
            if not rows:
                continue
            rows.sort(key=lambda x: x["item_id"])
            out_groups.append({"key": g["key"], "name": g["name"],
                               "rows": rows, "totals": gtot})

        out_groups.sort(key=lambda x: x["key"])

        # Phân trang theo DÒNG CHI TIẾT. Nhóm bị cắt ngang giữa hai trang vẫn an toàn:
        # `totals` của mỗi nhóm là tổng ĐẦY ĐỦ (cộng xong trước khi cắt), nên trang sau
        # lặp lại đầu nhóm với đúng con số đó — không phải tổng của riêng phần đang hiện.
        # `grand` cũng cộng xong trước khi cắt ⇒ dòng tổng cuối bảng không đổi theo trang.
        total_groups = len(out_groups)
        total_rows = sum(len(g["rows"]) for g in out_groups)
        if export_all:
            total_pages, page = 1, 1
        else:
            total_pages = max(1, (total_rows + page_size - 1) // page_size)
            page = max(1, min(page, total_pages))
            lo, hi = (page - 1) * page_size, page * page_size
            paged, seen = [], 0
            for g in out_groups:
                n = len(g["rows"])
                if seen + n > lo and seen < hi:          # nhóm có phần nằm trong trang
                    paged.append({**g, "rows": g["rows"][max(0, lo - seen): hi - seen]})
                seen += n
            out_groups = paged

        return jsonify({
            "status": "ok",
            "group_by": group_by,
            "columns": {"in": cols_in, "out": cols_out},
            "groups": out_groups,
            "grand": grand,
            "pagination": {"total_rows": total_rows, "total_groups": total_groups,
                           "total_pages": total_pages, "page": page, "page_size": page_size},
        })
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        logger.error(f"Error in BC016 get_nxt: {msg}")
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


def _cashbook_csv_stream(flat):
    """Generator sinh từng dòng CSV từ danh sách flat (tiết kiệm RAM khi nhiều dòng)."""
    def esc(s):
        s = "" if s is None else str(s)
        if any(ch in s for ch in [',', '"', '\n', '\r']):
            return '"' + s.replace('"', '""') + '"'
        return s
    def n(v):
        v = float(v or 0)
        return "" if v == 0 else str(int(round(v)))
    yield "﻿" + ",".join(["STT", "Ngày ghi sổ", "Số CT Nợ", "Số CT Có", "Diễn giải", "Tk đối ứng", "Nợ", "Có", "Dư"]) + "\r\n"
    for r in flat:
        t = r["t"]
        if t == "head":
            label = f"Tài khoản {r['account_id']}" + (f" - {r['account_name']}" if r.get("account_name") else "")
            yield ",".join(["", "", "", "", esc(label), "", "", "", "Số dư đầu kỳ: " + n(r["opening"])]) + "\r\n"
        elif t == "cong":
            yield ",".join(["", "", "", "", esc(f"Cộng phát sinh — TK {r['account_id']}"), "", n(r["sum_deb"]), n(r["sum_crd"]), ""]) + "\r\n"
        elif t == "du":
            yield ",".join(["", "", "", "", esc(f"Số dư cuối kỳ — TK {r['account_id']}"), "", "", "", n(r["close"])]) + "\r\n"
        elif t == "grand":
            yield ",".join(["", "", "", "", "Tổng cộng tất cả tài khoản", "", n(r["period_deb"]), n(r["period_crd"]), n(r["close"])]) + "\r\n"
        else:
            deb = r["debit"]; crd = r["credit"]
            yield ",".join([str(r["stt"]), esc(r["tran_date"]),
                            esc(r["tran_no"]) if deb > 0 else "", esc(r["tran_no"]) if crd > 0 else "",
                            esc(r["description"]), esc(r["contra_account_id"]),
                            n(deb), n(crd), n(r["balance"])]) + "\r\n"


# =====================================================================
# BÁO CÁO KQKD (BC001-BC004) & LCTT CHÚ LONG (BC011)
# =====================================================================

@app.route("/api/cash_flow_cl")
@with_db_lock
def get_cash_flow_cl():
    """BC011 — LCTT gián tiếp kiểu 'Chú Long': suất phát từ LN trước thuế (KQKD)
    + biến động chi tiết các khoản mục trên Bảng cân đối kế toán (CĐKT) + biến động
    TK 411 cho hoạt động tài chính. Liệt kê 12 dòng vốn lưu động, KHÔNG dùng dòng plug.
    Chênh lệch nhỏ (nếu có, do bút toán P&L chưa kết chuyển hết) gom vào Mã 16/17."""
    # Phiên đăng nhập: cookie chỉ giữ 'sid', thông tin SQL nằm ở kho _phien_db
    # phía máy chủ (xem _db_cfg) — và KHÔNG có khóa "logged_in" (Bẫy 1).
    # Kiểm nhầm khóa đó thì endpoint LUÔN trả 401, mà frontend gặp 401 là setIsLoggedIn(false)
    # → người dùng bị đá văng về màn hình đăng nhập ngay khi bấm Xem báo cáo.
    if not _db_cfg():
        return jsonify({"status": "error", "message": "Chưa đăng nhập SQL Server"}), 401
    try:
        f_date  = request.args.get("from_date")
        t_date  = request.args.get("to_date")
        org_ids = [v for v in request.args.get("org_ids", "").split(",") if v]
        if not f_date or not t_date:
            return jsonify({"status": "error", "message": "Thiếu tham số từ ngày/đến ngày"}), 400
        from_dt = datetime.strptime(f_date, "%d/%m/%Y").date()
        to_dt   = datetime.strptime(t_date, "%d/%m/%Y").date()
        f_str, t_str = from_dt.strftime("%Y%m%d"), to_dt.strftime("%Y%m%d")
        first_day_of_year = date(from_dt.year, 1, 1).strftime("%Y%m%d")

        # 1) Số dư CĐKT đầu/cuối kỳ (dùng chung engine BC005)
        opening, closing = _compute_cdkt(from_dt, to_dt, org_ids)
        def dlt(code): return closing.get(code, 0.0) - opening.get(code, 0.0)  # biến động trong kỳ

        cur = get_connection().cursor()
        _rc, _rp = _org_filter_sql(org_ids, "L.ORGANIZATION_ID")
        org_and = (" AND " + _rc) if _rc else ""

        # 2) LN trước thuế (Mã 01) + khấu hao/dự phòng/lãi vay: dùng engine KQKD (_calc_results)
        cur.execute(f"""
            SELECT L.ACCOUNT_ID, L.ACCOUNT_ID_CONTRA, L.DEBIT_CREDIT, SUM(L.AMOUNT)
            FROM dbo.LEDGER L WITH (NOLOCK)
            WHERE L.TRAN_DATE >= ? AND L.TRAN_DATE <= ?{org_and}
            GROUP BY L.ACCOUNT_ID, L.ACCOUNT_ID_CONTRA, L.DEBIT_CREDIT
        """, [f_str, t_str] + list(_rp))
        pl = cur.fetchall()
        def s(pfx, dc, excl=()):
            return sum(float(r[3] or 0) for r in pl
                       if (r[0] or "").strip().startswith(pfx) and r[2] == dc
                       and not any((r[1] or "").strip().startswith(e) for e in excl))
        cf_data = [{"acc": (r[0] or "").strip(), "contra": (r[1] or "").strip(),
                    "dc": r[2], "val": float(r[3] or 0),
                    "item_class": "", "expense_class": "", "expense_id": "",
                    "month": from_dt.month, "year": from_dt.year} for r in pl]
        kq = _calc_results(cf_data, {}, {})

        # 3) Hoạt động đầu tư & tài chính (lấy theo dòng tiền thực tế + biến động TK 411)
        # Thu lãi/cổ tức (Mã 27): tiền THU đối ứng 515/121/128/1281
        def cash_in(contra_prefixes):
            tot = 0.0
            where = ["(L.ACCOUNT_ID LIKE '111%' OR L.ACCOUNT_ID LIKE '112%' OR L.ACCOUNT_ID LIKE '113%' OR L.ACCOUNT_ID LIKE '1281%')",
                     "L.DEBIT_CREDIT='DEB'", "L.TRAN_DATE>=?", "L.TRAN_DATE<=?"]
            params = [f_str, t_str]
            ors = " OR ".join("L.ACCOUNT_ID_CONTRA LIKE ?" for _ in contra_prefixes)
            where.append("(" + ors + ")")
            params += [p_ + "%" for p_ in contra_prefixes]
            if _rc: where.append(_rc); params += list(_rp)
            cur.execute(f"SELECT ISNULL(SUM(L.AMOUNT),0) FROM dbo.LEDGER L WITH (NOLOCK) WHERE {' AND '.join(where)}", params)
            return float((cur.fetchone() or [0])[0] or 0)

        m27 = cash_in(["515", "121", "128", "1281"])      # thu lãi cho vay, cổ tức, LN được chia
        # Mã 21 chi mua TSCĐ = tăng nguyên giá TSCĐ (CĐKT 222 + 240 XDCB)
        m21 = -(dlt('222') + dlt('227') + dlt('240'))     # 222 hữu hình, 227 vô hình, 240 XDCB dở dang
        if abs(m21) < 1: m21 = 0.0

        # Tài chính: biến động TK 411 trong kỳ (Có = nhận vốn → Mã 31 ; Nợ = trả vốn → Mã 32)
        m31 = s("411", "CRD")
        m32 = -s("411", "DEB")

        # 4) Mã 60 / 70 — tiền & tương đương tiền đầu/cuối kỳ (theo từng nhóm TK)
        def cash_bal(acc_like, end_inclusive=None, end_exclusive=None):
            where = [acc_like, "L.TRAN_DATE >= ?"]; params = [first_day_of_year]
            if end_inclusive: where.append("L.TRAN_DATE <= ?"); params.append(end_inclusive)
            if end_exclusive: where.append("L.TRAN_DATE < ?");  params.append(end_exclusive)
            if _rc: where.append(_rc); params += list(_rp)
            cur.execute(f"""SELECT ISNULL(SUM(CASE WHEN L.DEBIT_CREDIT='DEB' THEN L.AMOUNT ELSE -L.AMOUNT END),0)
                            FROM dbo.LEDGER L WITH (NOLOCK) WHERE {' AND '.join(where)}""", params)
            return float((cur.fetchone() or [0])[0] or 0)
        likes = {'111': "L.ACCOUNT_ID LIKE '111%'", '112': "L.ACCOUNT_ID LIKE '112%'",
                 '113': "(L.ACCOUNT_ID LIKE '113%' OR L.ACCOUNT_ID LIKE '1281%')"}
        o = {}  # tiền đầu kỳ theo nhóm
        cl_ = {} # tiền cuối kỳ theo nhóm
        for k, lk in likes.items():
            o[k]  = cash_bal(lk, end_exclusive=f_str)
            cl_[k] = cash_bal(lk, end_inclusive=t_str)
        m60 = o['111'] + o['112'] + o['113']
        m70 = cl_['111'] + cl_['112'] + cl_['113']
        net_cash = m70 - m60   # biến động tiền thực tế trong kỳ

        # 5) Lắp báo cáo
        r = {}
        r['01'] = kq.get('13', 0.0)                       # LN trước thuế
        r['02'] = s("214", "CRD", ["911"]) - s("214", "DEB", ["911"])   # khấu hao
        r['03'] = sum((s(p_, "CRD", ["911"]) - s(p_, "DEB", ["911"])) for p_ in ("229", "352", "159"))
        r['04'] = 0.0
        r['05'] = -m27                                    # loại lãi/lỗ từ HĐĐT khỏi HĐKD
        r['06'] = kq.get('07', 0.0)                       # chi phí lãi vay
        r['08'] = r['01'] + r['02'] + r['03'] + r['04'] + r['05'] + r['06']
        # 12 dòng thay đổi vốn lưu động (tài sản: -Δ ; nợ phải trả: +Δ) — map theo dòng CĐKT
        r['w01'] = -dlt('131')                            # phải thu KH
        r['w02'] = -dlt('132')                            # trả trước người bán
        r['w03'] = -dlt('133')                            # phải thu nội bộ
        r['w04'] = -dlt('136')                            # phải thu khác
        r['w05'] = -dlt('141')                            # hàng tồn kho
        r['w06'] = -(dlt('151') + dlt('152') + dlt('153') + dlt('155'))  # chi phí trả trước & TS NH khác
        r['w07'] = dlt('311')                             # phải trả người bán
        r['w08'] = dlt('312')                             # người mua trả tiền trước
        r['w09'] = dlt('313')                             # thuế & phải nộp NN
        r['w10'] = dlt('314')                             # phải trả người lao động
        r['w11'] = dlt('316')                             # phải trả nội bộ
        r['w12'] = dlt('315') + dlt('317') + dlt('318') + dlt('319') + dlt('320') + dlt('321') + dlt('322') + dlt('323')  # phải trả, phải nộp khác
        sum_wc = sum(r[f'w{n:02d}'] for n in range(1, 13))
        # Mã 30 / 40
        r['21'], r['22'], r['23'], r['24'], r['25'], r['26'], r['27'] = m21, 0.0, 0.0, 0.0, 0.0, 0.0, m27
        r['30'] = m21 + m27
        r['31'], r['32'], r['33'], r['34'], r['35'], r['36'] = m31, m32, 0.0, 0.0, 0.0, 0.0
        r['40'] = m31 + m32
        # Mã 20 từ các thành phần; chênh lệch còn lại (nếu có) gom vào tiền thu/chi khác HĐKD (16/17)
        m20_components = r['08'] + sum_wc
        residual = net_cash - (m20_components + r['30'] + r['40'])
        r['16'] = residual if residual >= 0 else 0.0      # tiền thu khác HĐKD
        r['17'] = residual if residual < 0 else 0.0       # tiền chi khác HĐKD
        r['20'] = m20_components + r['16'] + r['17']
        r['50'] = r['20'] + r['30'] + r['40']
        r['60'] = m60; r['61'] = 0.0; r['70'] = m70
        r['60_111'], r['60_112'], r['60_113'] = o['111'], o['112'], o['113']
        r['70_111'], r['70_112'], r['70_113'] = cl_['111'], cl_['112'], cl_['113']

        return jsonify({"status": "ok", "data": r})
    except Exception as e:
        msg = str(e)
        if "đăng nhập" not in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), 401 if "đăng nhập" in msg else 500


def _calc_results(data, thtt_expense_list, expense_classes):
    sum_map = {}
    excl_map = {}
    exp_cls_map = {}
    exp_id_map = {}
    for d in data:
        acc = d['acc']; contra = d['contra']; dc = d['dc']
        ic = d['item_class']; ec = d['expense_class']; eid = d['expense_id']; val = d['val']
        k1 = (acc, dc, ic);             sum_map[k1]     = sum_map.get(k1, 0) + val
        k2 = (acc, contra[:3], dc, ic); excl_map[k2]    = excl_map.get(k2, 0) + val
        k3 = (acc, dc, ec);             exp_cls_map[k3] = exp_cls_map.get(k3, 0) + val
        k4 = (acc, dc, eid);            exp_id_map[k4]  = exp_id_map.get(k4, 0) + val

    def s(acc_prefix, dc, item_classes=None):
        if isinstance(item_classes, str): item_classes = [item_classes]
        total = 0
        for (acc, d_c, ic), val in sum_map.items():
            if d_c == dc and acc.startswith(acc_prefix):
                if item_classes is None or ic in item_classes:
                    total += val
        return total

    def s_excl(acc_prefix, dc, excl_contras, item_classes=None):
        if isinstance(item_classes, str): item_classes = [item_classes]
        total = 0
        for (acc, contra, d_c, ic), val in excl_map.items():
            if d_c == dc and acc.startswith(acc_prefix):
                if item_classes is None or ic in item_classes:
                    if not any(contra.startswith(c) for c in excl_contras):
                        total += val
        return total

    def s_multi(acc_prefixes, dc, item_classes=None):
        if isinstance(item_classes, str): item_classes = [item_classes]
        if isinstance(acc_prefixes, str): acc_prefixes = [acc_prefixes]
        total = 0
        for (acc, d_c, ic), val in sum_map.items():
            if d_c == dc and any(acc.startswith(p) for p in acc_prefixes):
                if item_classes is None or ic in item_classes:
                    total += val
        return total

    def s_multi_excl(acc_prefixes, dc, excl_contras, item_classes=None):
        if isinstance(item_classes, str): item_classes = [item_classes]
        if isinstance(acc_prefixes, str): acc_prefixes = [acc_prefixes]
        total = 0
        for (acc, contra, d_c, ic), val in excl_map.items():
            if d_c == dc and any(acc.startswith(p) for p in acc_prefixes):
                if item_classes is None or ic in item_classes:
                    if not any(contra.startswith(c) for c in excl_contras):
                        total += val
        return total

    r = {}
    r['01']  = s('511', 'CRD') - s_excl('511', 'DEB', ['911', '521'])
    r['011'] = s('511', 'CRD', 'CF') - s_excl('511', 'DEB', ['911', '521'], 'CF')
    _oth = ['ITEM_TYPE_OTHER', 'KHAC', 'SC', 'TEA', 'TRA', 'T', 'TUI']
    r['012'] = s('511', 'CRD', list(_oth)) - s_excl('511', 'DEB', ['911', '521'], list(_oth))
    r['013'] = s('511', 'CRD', 'THUCAN') - s_excl('511', 'DEB', ['911', '521'], 'THUCAN')
    r['014'] = s('511', 'CRD', ['ITEM_TYPE-CA65', 'ITEM_TYPE-ZJWK']) - s_excl('511', 'DEB', ['911', '521'], ['ITEM_TYPE-CA65', 'ITEM_TYPE-ZJWK'])
    r['015'] = s('511', 'CRD', 'MC') - s_excl('511', 'DEB', ['911', '521'], 'MC')
    r['016'] = s('511', 'CRD', 'TA') - s_excl('511', 'DEB', ['911', '521'], 'TA')
    r['017'] = s('511', 'CRD', 'ITEM_TYPE-6CAX') - s_excl('511', 'DEB', ['911', '521'], 'ITEM_TYPE-6CAX')
    r['018'] = s('511', 'CRD', 'CB') - s_excl('511', 'DEB', ['911', '521'], 'CB')
    r['019'] = r['01'] - (r['011'] + r['012'] + r['013'] + r['014'] + r['015'] + r['016'] + r['017'] + r['018'])
    r['02']  = s('521', 'DEB') - s_excl('521', 'CRD', ['511'])
    r['020'] = r['02']
    r['03']  = r['01'] - r['02']
    r['04']  = s('632', 'DEB') - s_excl('632', 'CRD', ['911'])
    r['05']  = r['03'] - r['04']
    r['06']  = s('515', 'CRD') - s_excl('515', 'DEB', ['911'])
    r['061'] = r['06']
    r['07']  = s('635', 'DEB') - s_excl('635', 'CRD', ['911'])
    r['071'] = sum(d['val'] for d in data if d['acc'].startswith('635') and d['dc'] == 'DEB' and not any(d['contra'].startswith(c) for c in ('911',)))
    r['08']  = s_multi(['641', '642'], 'DEB') - s_multi_excl(['641', '642'], 'CRD', ['911'])

    thtt_deb = sum(d['val'] for d in data if any(d['acc'].startswith(p) for p in ('641', '642')) and d['dc'] == 'DEB' and d['expense_id'].strip().upper().startswith('THTT.'))
    thtt_crd = sum(d['val'] for d in data if any(d['acc'].startswith(p) for p in ('641', '642')) and d['dc'] == 'CRD' and d['expense_id'].strip().upper().startswith('THTT.') and not any(d['contra'].startswith(c) for c in ('911',)))
    r['081'] = thtt_deb - thtt_crd

    thtt_map = {}
    for eid, ename in thtt_expense_list.items():
        thtt_map[eid] = {'deb': 0, 'crd': 0, 'name': ename}
    for d in data:
        if not any(d['acc'].startswith(p) for p in ('641', '642')): continue
        eid = d['expense_id'].upper()
        if eid not in thtt_map: continue
        if d['dc'] == 'DEB':
            thtt_map[eid]['deb'] += d['val']
        elif d['dc'] == 'CRD' and not any(d['contra'].startswith(c) for c in ('911',)):
            thtt_map[eid]['crd'] += d['val']
    r['_081_details'] = [{'id': eid, 'name': info['name'], 'val': info['deb'] - info['crd']} for eid, info in sorted(thtt_map.items())]

    expense_class_mapping = {'082': 'TTTM', '083': 'TTTT', '084': 'CPVH', '085': 'TL', '086': 'BH', '087': 'TAX', '088': 'CPKH', '089': 'CPC'}
    for line_id, exp_class in expense_class_mapping.items():
        cls_deb = sum(d['val'] for d in data if any(d['acc'].startswith(p) for p in ('641', '642')) and d['dc'] == 'DEB' and d['expense_class'] == exp_class)
        cls_crd = sum(d['val'] for d in data if any(d['acc'].startswith(p) for p in ('641', '642')) and d['dc'] == 'CRD' and d['expense_class'] == exp_class and not any(d['contra'].startswith(c) for c in ('911',)))
        r[line_id] = cls_deb - cls_crd
        cls_expenses = expense_classes.get(exp_class, {})
        cls_map = {}
        for eid, ename in cls_expenses.items():
            cls_map[eid] = {'deb': 0, 'crd': 0, 'name': ename}
        for d in data:
            if not any(d['acc'].startswith(p) for p in ('641', '642')): continue
            if d['expense_class'] != exp_class: continue
            eid = d['expense_id'].upper()
            if eid not in cls_map: continue
            if d['dc'] == 'DEB':
                cls_map[eid]['deb'] += d['val']
            elif d['dc'] == 'CRD' and not any(d['contra'].startswith(c) for c in ('911',)):
                cls_map[eid]['crd'] += d['val']
        r["_" + line_id + "_details"] = [{'id': eid, 'name': info['name'], 'val': info['deb'] - info['crd']} for eid, info in sorted(cls_map.items())]

    _subs = ('08201', '08202', '08203', '08204', '08205', '08301', '08302', '08303', '08304', '08305', '08306', '08401', '08402', '08403', '08404', '08405', '08406', '08407', '08408', '084081', '08409', '08410', '08411', '08412', '084121', '08413', '08501', '08502', '08503', '08504', '08601', '08602', '08603', '08604', '08605', '08701', '08702', '08703', '08704', '08705', '08801', '08901', '08902', '08903', '08904', '08905', '08906', '08907', '08908', '08909', '08910', '08911', '08912', '08913', '08914', '08915', '08916', '08917', '08918', '08919', '08920', '08921', '08922')
    for sub in _subs:
        r[sub] = 0

    # --- Bổ sung chi phí 641/642 nằm ngoài các nhóm chuẩn để 08 = Σ(081..089) ---
    extra_084 = 0
    for d in data:
        if not any(d['acc'].startswith(p) for p in ('641', '642')): continue
        if d['expense_class'] not in ('04', '01'): continue
        if d['dc'] == 'DEB':
            extra_084 += d['val']
        elif d['dc'] == 'CRD' and not any(d['contra'].startswith(c) for c in ('911',)):
            extra_084 -= d['val']
    if abs(extra_084) >= 1:
        r['084'] = r.get('084', 0) + extra_084
        r.setdefault('_084_details', []).append({'id': '', 'name': 'Chi phí Nguyên vật liệu khác', 'val': extra_084})

    residual_089 = r['08'] - (r.get('081', 0) + r.get('082', 0) + r.get('083', 0) + r.get('084', 0)
                              + r.get('085', 0) + r.get('086', 0) + r.get('087', 0) + r.get('088', 0) + r.get('089', 0))
    if abs(residual_089) >= 1:
        r['089'] = r.get('089', 0) + residual_089
        r.setdefault('_089_details', []).append({'id': '', 'name': 'Chi phí chung khác', 'val': residual_089})

    r['09'] = r['05'] + r['06'] - r['07'] - r['08']
    r['10'] = s('711', 'CRD') - s_excl('711', 'DEB', ['911'])
    r['11'] = s('811', 'DEB') - s_excl('811', 'CRD', ['911'])
    r['12'] = r['10'] - r['11']
    r['13'] = r['09'] + r['12']
    r['14'] = s('8211', 'DEB') - s_excl('8211', 'CRD', ['911'])
    r['15'] = s('8212', 'DEB') - s_excl('8212', 'CRD', ['911'])
    r['16'] = r['13'] - r['14'] - r['15']
    # 16.1/16.2 — mẫu riêng Chú Long. 16.1 là SỐ DƯ CÓ CUỐI KỲ của TK 33311 (khớp Bảng cân đối
    # số phát sinh), KHÔNG phải phát sinh trong kỳ ⇒ cần dữ liệu NGOÀI khoảng đang xem, mà hàm này
    # chỉ thấy đúng khoảng đó. Route gọi _vat_payable_closing() rồi GHI ĐÈ hai khoá này;
    # ở đây chỉ đặt mặc định để báo cáo không vỡ nếu có nơi gọi thẳng _calc_results.
    r['161'] = 0.0
    r['162'] = r['16']
    r['17'] = 0
    r['18'] = 0
    return r


# Bộ tài khoản DUY NHẤT mà _calc_results() đọc tới (511/515/521/632/635/641/642/711/811/821).
# LEDGER có 18,9 triệu dòng; query KQKD trước đây GROUP BY TOÀN BỘ tài khoản rồi vứt đi ~56% số
# nhóm. Lọc ngay tại SQL: 16,2s → 7,7s cho kỳ 1 tháng (đo 19/08/2026, kết quả _calc_results
# giống hệt từng nhóm), và đọc ít trang hơn nên đỡ tranh buffer pool 1410 MB với việc lưu phiếu.
# ⚠️ Thêm/bớt tiền tố tài khoản trong _calc_results thì PHẢI cập nhật danh sách này — thiếu một
# tiền tố là chỉ tiêu tương ứng lặng lẽ về 0, không báo lỗi.
_KQKD_ACCOUNTS = ('511', '515', '521', '632', '635', '641', '642', '711', '811', '821')


def _kqkd_acc_filter_sql(col="L.ACCOUNT_ID"):
    """(clause, params) lọc đúng bộ tài khoản KQKD — xem _KQKD_ACCOUNTS."""
    clause = "(" + " OR ".join(f"{col} LIKE ?" for _ in _KQKD_ACCOUNTS) + ")"
    return clause, [a + '%' for a in _KQKD_ACCOUNTS]


def _vat_payable_closing(from_dt, to_dt, org_ids, job_ids=None):
    """Chỉ tiêu 16.1 (BC001–BC004) — Thuế GTGT phải nộp = **SỐ DƯ CÓ CUỐI KỲ của TK 33311**,
    đúng như cột "Dư cuối kỳ" trên Bảng cân đối số phát sinh, KHÔNG phải phát sinh trong kỳ:

        dư cuối kỳ = dư đầu kỳ + PS Có − PS Nợ

    Dư đầu kỳ dồn thẳng từ LEDGER kể từ 01/01 của năm — `BALANCE_VIEW` của IACC_CHULONG trống
    0 dòng (xem CLAUDE.md), và TK 33311 không có phát sinh nào trước 01/01/2026 (đã kiểm).
    Chỉ lấy đúng TK `33311`, không lấy `3331` nói chung.

    Trả về (dư cuối tại to_dt, {'<tháng>_<năm>': dư cuối tháng đó}, {job_id: dư cuối tại to_dt}).
    """
    first_day = date(from_dt.year, 1, 1)
    # Thứ tự append vào where PHẢI khớp thứ tự append vào params (Bẫy 5).
    where = ["L.ACCOUNT_ID = '33311'", "L.TRAN_DATE >= ?", "L.TRAN_DATE <= ?"]
    params = [first_day.strftime('%Y%m%d'), to_dt.strftime('%Y%m%d')]
    _oc, _op = _org_filter_sql(org_ids, "L.ORGANIZATION_ID")
    if _oc:
        where.append(_oc)
        params.extend(_op)
    if job_ids:
        where.append(f"L.JOB_ID IN ({','.join(['?'] * len(job_ids))})")
        params.extend(job_ids)

    cursor = get_connection().cursor()
    cursor.execute(f"""
        SELECT YEAR(L.TRAN_DATE) AS Y, MONTH(L.TRAN_DATE) AS M, ISNULL(L.JOB_ID, '') AS JOB_ID,
               SUM(CASE WHEN L.DEBIT_CREDIT = 'CRD' THEN L.AMOUNT ELSE -L.AMOUNT END) AS NET
        FROM dbo.LEDGER L WITH (NOLOCK)
        WHERE {' AND '.join(where)}
        GROUP BY YEAR(L.TRAN_DATE), MONTH(L.TRAN_DATE), ISNULL(L.JOB_ID, '')
    """, params)

    net_by_month = {}
    net_by_job = {}
    for r_ in cursor.fetchall():
        y_, m_, jid_, net_ = r_[0], r_[1], (r_[2] or '').strip(), float(r_[3] or 0)
        net_by_month[(y_, m_)] = net_by_month.get((y_, m_), 0.0) + net_
        net_by_job[jid_] = net_by_job.get(jid_, 0.0) + net_

    # Cộng dồn từ đầu năm: dư cuối THÁNG NÀO cũng là luỹ kế tới hết tháng đó.
    running = 0.0
    monthly_closing = {}
    y, m = first_day.year, first_day.month
    while (y, m) <= (to_dt.year, to_dt.month):
        running += net_by_month.get((y, m), 0.0)
        monthly_closing[f"{m}_{y}"] = running
        m += 1
        if m > 12:
            m = 1
            y += 1
    return running, monthly_closing, net_by_job


@app.route('/api/report')
@with_db_lock
def get_report():
    # Phiên đăng nhập: cookie chỉ giữ 'sid', thông tin SQL nằm ở kho _phien_db
    # phía máy chủ (xem _db_cfg) — và KHÔNG có khóa "logged_in" (Bẫy 1).
    # Kiểm nhầm khóa đó thì endpoint LUÔN trả 401, mà frontend gặp 401 là setIsLoggedIn(false)
    # → người dùng bị đá văng về màn hình đăng nhập ngay khi bấm Xem báo cáo.
    if not _db_cfg():
        return jsonify({"status": "error", "message": "Chưa đăng nhập SQL Server"}), 401
    try:
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        org_ids = [v for v in request.args.get('org_ids', '').split(',') if v]
        job_ids = [v for v in request.args.get('job_ids', '').split(',') if v]
        if not from_date or not to_date:
            return jsonify({"status": "error", "message": "Thiếu tham số từ ngày/đến ngày"}), 400

        from_dt = datetime.strptime(from_date, '%d/%m/%Y').date()
        to_dt = datetime.strptime(to_date, '%d/%m/%Y').date()

        month_list = []
        cur_y, cur_m = from_dt.year, from_dt.month
        end_y, end_m = to_dt.year, to_dt.month
        while (cur_y, cur_m) <= (end_y, end_m):
            month_list.append({"month": cur_m, "year": cur_y})
            cur_m += 1
            if cur_m > 12:
                cur_m = 1
                cur_y += 1

        where_clauses = ["L.TRAN_DATE >= ?", "L.TRAN_DATE <= ?"]
        params = [from_dt.strftime('%Y%m%d'), to_dt.strftime('%Y%m%d')]
        _ac, _ap = _kqkd_acc_filter_sql("L.ACCOUNT_ID")
        where_clauses.append(_ac)
        params.extend(_ap)
        _oc, _op = _org_filter_sql(org_ids, "L.ORGANIZATION_ID")
        if _oc:
            where_clauses.append(_oc)
            params.extend(_op)
        if job_ids:
            where_clauses.append(f"L.JOB_ID IN ({','.join(['?'] * len(job_ids))})")
            params.extend(job_ids)
        where_sql = " AND ".join(where_clauses)

        query = f"""
            SELECT L.ACCOUNT_ID, L.ACCOUNT_ID_CONTRA, L.DEBIT_CREDIT,
                   I.ITEM_CLASS1_ID, E.EXPENSE_CLASS_ID, L.EXPENSE_ID,
                   MONTH(L.TRAN_DATE) AS M, YEAR(L.TRAN_DATE) AS Y,
                   SUM(L.AMOUNT) as TOTAL
            FROM dbo.LEDGER L WITH (NOLOCK)
            LEFT JOIN dbo.DM_ITEM I WITH (NOLOCK) ON L.ITEM_ID = I.ITEM_ID
            LEFT JOIN dbo.DM_EXPENSE E WITH (NOLOCK) ON L.EXPENSE_ID = E.EXPENSE_ID
            WHERE {where_sql}
            GROUP BY L.ACCOUNT_ID, L.ACCOUNT_ID_CONTRA, L.DEBIT_CREDIT,
                     I.ITEM_CLASS1_ID, E.EXPENSE_CLASS_ID, L.EXPENSE_ID,
                     MONTH(L.TRAN_DATE), YEAR(L.TRAN_DATE)
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        raw = cursor.fetchall()

        cursor.execute("""
            SELECT EXPENSE_CLASS_ID, EXPENSE_ID, EXPENSE_NAME
            FROM dbo.DM_EXPENSE WITH (NOLOCK)
            WHERE EXPENSE_CLASS_ID IN ('THTT','TTTM','TTTT','CPVH','TL','BH','TAX','CPKH','CPC')
            ORDER BY EXPENSE_CLASS_ID, EXPENSE_ID
        """)
        expense_classes = {}
        for r in cursor.fetchall():
            cls = (r[0] or '').strip()
            eid = (r[1] or '').strip().upper()
            ename = (r[2] or '').strip()
            if cls not in expense_classes:
                expense_classes[cls] = {}
            expense_classes[cls][eid] = ename
        thtt_expense_list = expense_classes.get('THTT', {})

        all_data = [{
            'acc': (r[0] or '').strip(),
            'contra': (r[1] or '').strip(),
            'dc': r[2],
            'item_class': (r[3] or '').strip().upper(),
            'expense_class': (r[4] or '').strip().upper(),
            'expense_id': (r[5] or '').strip().upper(),
            'month': r[6],
            'year': r[7],
            'val': float(r[8] or 0)
        } for r in raw]

        total_results = _calc_results(all_data, thtt_expense_list, expense_classes)

        monthly = {}
        for mp in month_list:
            m_data = [d for d in all_data if d['month'] == mp['month'] and d['year'] == mp['year']]
            m_key = f"{mp['month']}_{mp['year']}"
            monthly[m_key] = _calc_results(m_data, thtt_expense_list, expense_classes)

        # 16.1 = số dư Có CUỐI KỲ của TK 33311 → phải dồn từ đầu năm, không suy ra được từ all_data.
        vat_close, vat_monthly, _ = _vat_payable_closing(from_dt, to_dt, org_ids, job_ids)
        total_results['161'] = vat_close
        total_results['162'] = total_results['16'] - vat_close
        for _mk, _mres in monthly.items():
            _mres['161'] = vat_monthly.get(_mk, 0.0)
            _mres['162'] = _mres['16'] - _mres['161']

        return jsonify({
            "status": "ok",
            "data": total_results,
            "monthly": monthly,
            "month_list": month_list
        })
    except Exception as e:
        msg = str(e)
        if 'đăng nhập' in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), (401 if 'đăng nhập' in msg else 500)


@app.route('/api/report_by_job')
@with_db_lock
def get_report_by_job():
    # Phiên đăng nhập: cookie chỉ giữ 'sid', thông tin SQL nằm ở kho _phien_db
    # phía máy chủ (xem _db_cfg) — và KHÔNG có khóa "logged_in" (Bẫy 1).
    # Kiểm nhầm khóa đó thì endpoint LUÔN trả 401, mà frontend gặp 401 là setIsLoggedIn(false)
    # → người dùng bị đá văng về màn hình đăng nhập ngay khi bấm Xem báo cáo.
    if not _db_cfg():
        return jsonify({"status": "error", "message": "Chưa đăng nhập SQL Server"}), 401
    try:
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        org_ids = [v for v in request.args.get('org_ids', '').split(',') if v]
        job_ids = [v for v in request.args.get('job_ids', '').split(',') if v]
        if not from_date or not to_date:
            return jsonify({"status": "error", "message": "Thiếu tham số từ ngày/đến ngày"}), 400

        from_dt = datetime.strptime(from_date, '%d/%m/%Y').date()
        to_dt = datetime.strptime(to_date, '%d/%m/%Y').date()

        where_clauses = ["L.TRAN_DATE >= ?", "L.TRAN_DATE <= ?"]
        params = [from_dt.strftime('%Y%m%d'), to_dt.strftime('%Y%m%d')]
        _ac, _ap = _kqkd_acc_filter_sql("L.ACCOUNT_ID")
        where_clauses.append(_ac)
        params.extend(_ap)
        _oc, _op = _org_filter_sql(org_ids, "L.ORGANIZATION_ID")
        if _oc:
            where_clauses.append(_oc)
            params.extend(_op)
        if job_ids:
            where_clauses.append(f"L.JOB_ID IN ({','.join(['?'] * len(job_ids))})")
            params.extend(job_ids)
        where_sql = " AND ".join(where_clauses)

        query = f"""
            SELECT L.ACCOUNT_ID, L.ACCOUNT_ID_CONTRA, L.DEBIT_CREDIT,
                   I.ITEM_CLASS1_ID, E.EXPENSE_CLASS_ID, L.EXPENSE_ID,
                   ISNULL(L.JOB_ID, '') AS JOB_ID,
                   SUM(L.AMOUNT) as TOTAL
            FROM dbo.LEDGER L WITH (NOLOCK)
            LEFT JOIN dbo.DM_ITEM I WITH (NOLOCK) ON L.ITEM_ID = I.ITEM_ID
            LEFT JOIN dbo.DM_EXPENSE E WITH (NOLOCK) ON L.EXPENSE_ID = E.EXPENSE_ID
            WHERE {where_sql}
            GROUP BY L.ACCOUNT_ID, L.ACCOUNT_ID_CONTRA, L.DEBIT_CREDIT,
                     I.ITEM_CLASS1_ID, E.EXPENSE_CLASS_ID, L.EXPENSE_ID,
                     ISNULL(L.JOB_ID, '')
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        raw = cursor.fetchall()

        cursor.execute("""
            SELECT EXPENSE_CLASS_ID, EXPENSE_ID, EXPENSE_NAME
            FROM dbo.DM_EXPENSE WITH (NOLOCK)
            WHERE EXPENSE_CLASS_ID IN ('THTT','TTTM','TTTT','CPVH','TL','BH','TAX','CPKH','CPC')
            ORDER BY EXPENSE_CLASS_ID, EXPENSE_ID
        """)
        expense_classes = {}
        for r in cursor.fetchall():
            cls = (r[0] or '').strip()
            eid = (r[1] or '').strip().upper()
            ename = (r[2] or '').strip()
            if cls not in expense_classes:
                expense_classes[cls] = {}
            expense_classes[cls][eid] = ename
        thtt_expense_list = expense_classes.get('THTT', {})

        all_data = [{
            'acc': (r[0] or '').strip(),
            'contra': (r[1] or '').strip(),
            'dc': r[2],
            'item_class': (r[3] or '').strip().upper(),
            'expense_class': (r[4] or '').strip().upper(),
            'expense_id': (r[5] or '').strip().upper(),
            'job_id': (r[6] or '').strip(),
            'val': float(r[7] or 0),
        } for r in raw]

        if job_ids:
            seen_jobs = set(d['job_id'] for d in all_data)
            job_list_ids = [j for j in job_ids if j in seen_jobs]
        else:
            seen = set()
            job_list_ids = []
            for d in all_data:
                jid = d['job_id']
                if jid and jid not in seen:
                    seen.add(jid)
                    job_list_ids.append(jid)
            job_list_ids.sort()

        db_name = (_db_cfg() or {}).get('database', 'N/A')
        meta = _meta_cache.get(db_name) or {}
        job_name_map = {(j.get('id') or '').strip(): (j.get('name') or '') for j in meta.get('jobs', [])}
        job_list = [{"id": jid, "name": job_name_map.get(jid, '')} for jid in job_list_ids]

        total_results = _calc_results(all_data, thtt_expense_list, expense_classes)

        jobs_result = {}
        for jid in job_list_ids:
            j_data = [d for d in all_data if d['job_id'] == jid]
            jobs_result[jid] = _calc_results(j_data, thtt_expense_list, expense_classes)

        # 16.1 = số dư Có CUỐI KỲ của TK 33311 (dồn từ đầu năm). Bút toán thuế thường KHÔNG gắn
        # JOB_ID nên phần lớn số này rơi vào cột công việc rỗng — cột tổng mới là con số cần đọc.
        vat_close, _, vat_by_job = _vat_payable_closing(from_dt, to_dt, org_ids, job_ids)
        total_results['161'] = vat_close
        total_results['162'] = total_results['16'] - vat_close
        for _jid, _jres in jobs_result.items():
            _jres['161'] = vat_by_job.get(_jid, 0.0)
            _jres['162'] = _jres['16'] - _jres['161']

        return jsonify({
            "status": "ok",
            "data": total_results,
            "jobs": jobs_result,
            "job_list": job_list
        })
    except Exception as e:
        msg = str(e)
        if 'đăng nhập' in msg:
            invalidate_pool()
        return jsonify({"status": "error", "message": msg}), (401 if 'đăng nhập' in msg else 500)


# ==============================================================================
# MODULE TỰ ĐỘNG CẬP NHẬT (AUTO-UPDATE VIA GITHUB RELEASES & NTFS RENAME)
# ==============================================================================
import urllib.request
import json
import re

_update_lock = threading.Lock()
_update_state = {
    "status": "idle",       # "idle", "downloading", "applying", "ready", "error"
    "progress": 0,          # 0 - 100
    "downloaded_bytes": 0,
    "total_bytes": 0,
    "error_message": "",
    "target_version": ""
}

# Handle tiến trình Chrome --app đang mở (launch_app_window đặt). Updater phải ĐÓNG cửa sổ này
# trước khi chạy bản mới — xem chú thích trong _async_download_and_swap.
_app_window_proc = None
# Bật trong lúc thay EXE: chặn launch_app_window tự tắt server khi cửa sổ bị đóng CÓ CHỦ ĐÍCH.
_update_in_progress = False

def _cleanup_old_executables(retry_seconds=0):
    """Dọn các tệp tạm .old / .new / .tmp_dl do lần cập nhật trước để lại.

    ⚠️ Bản VỪA được cập nhật phải gọi với `retry_seconds > 0`: file `.old` chính là image của
    tiến trình cũ vừa khởi chạy mình, Windows còn KHOÁ nó cho tới khi tiến trình đó thoát hẳn.
    Thử xoá đúng một lần rồi thôi (cách cũ) luôn thất bại im lặng ⇒ file `.old` nằm lại tới tận
    lần chạy sau — đúng triệu chứng "cập nhật xong vẫn còn file exe cũ đổi tên".
    """
    if not getattr(sys, 'frozen', False):
        return
    try:
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    except Exception:
        return
    deadline = time.time() + max(0, retry_seconds)
    while True:
        con_lai = []
        try:
            dang_tai = _update_state.get("status") in ("downloading", "applying")
            for fname in os.listdir(exe_dir):
                if not (fname.endswith(".old") or fname.endswith(".new") or fname.endswith(".tmp_dl")):
                    continue
                # Vòng retry chạy tới 60s; nếu user bấm cập nhật trong lúc đó thì file .new
                # đang được ghi dở — xoá là giết luôn bản đang tải.
                if dang_tai and not fname.endswith(".old"):
                    continue
                try:
                    os.remove(os.path.join(exe_dir, fname))
                except Exception:
                    con_lai.append(fname)
        except Exception:
            return
        if not con_lai or time.time() >= deadline:
            return
        time.sleep(1.0)

def _child_env_without_pyi():
    """Env sạch để spawn EXE mới — PHẢI gỡ các biến bootloader PyInstaller onefile.

    ⚠️ BẪY ĐÃ LÀM CHẾT TÍNH NĂNG TỰ CẬP NHẬT (28/08/2026): `subprocess.Popen([exe_path])`
    kế thừa nguyên env của tiến trình đang chạy, trong đó bootloader onefile đã đặt
    `_PYI_APPLICATION_HOME_DIR` / `_PYI_ARCHIVE_FILE` / `_PYI_PARENT_PROCESS_LEVEL`
    (bản PyInstaller <=5 tên là `_MEIPASS2`). Bootloader của EXE MỚI thấy các biến này thì
    hiểu nhầm mình là tiến trình con giai đoạn 2 của cha, nên đối chiếu executable của tiến
    trình cha với chính mình — cha là `...exe.old` (vừa bị đổi tên), con là `...exe` ⇒ KHÁC ⇒
    dừng ngay ở tầng bootloader với hộp thoại:
        Security validation failure: parent process has different executable!
    Python chưa chạy được dòng nào, nên `.old` cũng không ai dọn.
    Triệu chứng người dùng: *"tải về xong chỉ thấy đổi EXE cũ thành .old, mở bản mới thì báo lỗi"*.

    Đo thế nào cho đúng: tiến trình bản mới VẪN nằm trong `tasklist` nhưng chỉ ~10 MB RAM
    (bootloader đang giữ hộp thoại) và KHÔNG LISTENING cổng 5050. Đã tái hiện + verify fix
    ngày 28/08/2026 bằng chính EXE tải từ GitHub Release.
    """
    env = os.environ.copy()
    for k in ("_PYI_APPLICATION_HOME_DIR", "_PYI_ARCHIVE_FILE", "_PYI_PARENT_PROCESS_LEVEL",
              "_PYI_SPLASH_IPC", "_MEIPASS2"):
        env.pop(k, None)
    return env

def _parse_semver(v_str):
    """Trích xuất tuple (major, minor, patch) từ chuỗi version ví dụ v1.8.6 -> (1, 8, 6)"""
    if not v_str:
        return (0, 0, 0)
    nums = re.findall(r'\d+', str(v_str))
    if not nums:
        return (0, 0, 0)
    return tuple(int(n) for n in nums[:3])

@app.route('/api/check_update', methods=['GET'])
def check_github_update():
    """Kiểm tra bản release mới nhất từ GitHub Releases API (timeout 3.0s)."""
    try:
        url = "https://api.github.com/repos/trungkhanhduong93/ledgerreport/releases/latest"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": f"iPOS-Accounting-Report/{APP_VERSION}",
                "Accept": "application/vnd.github.v3+json"
            }
        )
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            if resp.status != 200:
                return jsonify({"status": "error", "message": f"GitHub trả mã {resp.status}"}), 502
            data = json.loads(resp.read().decode('utf-8'))

        latest_tag = data.get('tag_name', '')
        release_name = data.get('name', '')
        release_body = data.get('body', '')
        published_at = data.get('published_at', '')
        assets = data.get('assets', [])

        # Tìm tệp thực thi .exe
        exe_asset = None
        for a in assets:
            if a.get('name', '').lower().endswith('.exe'):
                exe_asset = a
                break

        curr_ver_tuple = _parse_semver(APP_VERSION)
        latest_ver_tuple = _parse_semver(latest_tag)
        has_update = latest_ver_tuple > curr_ver_tuple

        download_url = exe_asset.get('browser_download_url', '') if exe_asset else ''
        file_size = exe_asset.get('size', 0) if exe_asset else 0

        sha256 = ''
        if exe_asset and exe_asset.get('digest', '').startswith('sha256:'):
            sha256 = exe_asset['digest'].replace('sha256:', '')

        return jsonify({
            "status": "ok",
            "has_update": has_update,
            "current_version": APP_VERSION,
            "latest_version": latest_tag,
            "release_name": release_name,
            "release_notes": release_body,
            "published_at": published_at,
            "download_url": download_url,
            "file_size": file_size,
            "sha256": sha256,
            "is_frozen": getattr(sys, 'frozen', False)
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "has_update": False,
            "message": str(e),
            "current_version": APP_VERSION,
            "is_frozen": getattr(sys, 'frozen', False)
        })

@app.route('/api/update_progress', methods=['GET'])
def get_update_progress_api():
    """Truy vấn tiến trình tải tệp cập nhật."""
    with _update_lock:
        return jsonify(_update_state)

@app.route('/api/apply_update', methods=['POST'])
def apply_update_api():
    """Tải tệp mới và thực hiện cơ chế NTFS Rename-then-Replace in-place."""
    if not getattr(sys, 'frozen', False):
        return jsonify({
            "status": "error",
            "message": "Tính năng tự động cập nhật chỉ khả dụng khi chạy từ file EXE đóng gói."
        }), 400

    with _update_lock:
        if _update_state["status"] in ("downloading", "applying"):
            return jsonify({"status": "busy", "message": "Đang có tiến trình cập nhật đang chạy."})
        _update_state["status"] = "downloading"
        _update_state["progress"] = 0
        _update_state["downloaded_bytes"] = 0
        _update_state["total_bytes"] = 0
        _update_state["error_message"] = ""

    def _async_download_and_swap():
        global _update_state, _update_in_progress
        exe_path = os.path.abspath(sys.executable)
        exe_dir = os.path.dirname(exe_path)
        temp_new_path = os.path.join(exe_dir, f"{os.path.basename(exe_path)}.new")
        old_backup_path = os.path.join(exe_dir, f"{os.path.basename(exe_path)}.old")

        try:
            # 1. Truy vấn release info lấy download url
            url = "https://api.github.com/repos/trungkhanhduong93/ledgerreport/releases/latest"
            req = urllib.request.Request(
                url,
                headers={"User-Agent": f"iPOS-Accounting-Report/{APP_VERSION}"}
            )
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                data = json.loads(resp.read().decode('utf-8'))

            download_url = None
            target_ver = data.get('tag_name', '')
            for a in data.get('assets', []):
                if a.get('name', '').lower().endswith('.exe'):
                    download_url = a.get('browser_download_url')
                    break

            if not download_url:
                raise ValueError("Không tìm thấy tệp EXE phát hành trong bản mới nhất trên GitHub.")

            with _update_lock:
                _update_state["target_version"] = target_ver

            # 2. Tải tệp chunked vào file .new
            req_dl = urllib.request.Request(
                download_url,
                headers={"User-Agent": f"iPOS-Accounting-Report/{APP_VERSION}"}
            )
            with urllib.request.urlopen(req_dl, timeout=30.0) as dl_resp:
                total_size = int(dl_resp.headers.get('Content-Length', 0))
                downloaded = 0
                chunk_size = 64 * 1024  # 64 KB

                with open(temp_new_path, 'wb') as out_f:
                    while True:
                        chunk = dl_resp.read(chunk_size)
                        if not chunk:
                            break
                        out_f.write(chunk)
                        downloaded += len(chunk)
                        pct = int((downloaded / total_size) * 100) if total_size > 0 else 50
                        with _update_lock:
                            _update_state["progress"] = pct
                            _update_state["downloaded_bytes"] = downloaded
                            _update_state["total_bytes"] = total_size

            # Kiểm tra an toàn tính toàn vẹn
            actual_size = os.path.getsize(temp_new_path)
            if actual_size < 5 * 1024 * 1024:  # Ít nhất 5MB
                if os.path.exists(temp_new_path):
                    os.remove(temp_new_path)
                raise ValueError(f"Dung lượng tệp tải về không hợp lệ ({actual_size} bytes).")

            with _update_lock:
                _update_state["status"] = "applying"
                _update_state["progress"] = 100

            # 3. Thực hiện chuỗi lệnh NTFS Rename-then-Replace
            if os.path.exists(old_backup_path):
                try:
                    os.remove(old_backup_path)
                except Exception:
                    pass

            os.rename(exe_path, old_backup_path)
            os.rename(temp_new_path, exe_path)

            with _update_lock:
                _update_state["status"] = "ready"

            # 4. ĐÓNG CỬA SỔ APP CŨ trước khi chạy bản mới.
            # Chrome dùng chung --user-data-dir: nếu instance cũ còn sống thì cửa sổ mà bản mới
            # spawn sẽ bị "bàn giao" cho instance cũ rồi tự thoát <5s → bản mới chạy ngầm KHÔNG
            # có cửa sổ nào, user tưởng cập nhật xong là mất app (xem bẫy 12/08/2026 ở
            # launch_app_window). Bật cờ trước để launch_app_window không hiểu nhầm là user đóng
            # cửa sổ rồi taskkill chính tiến trình này — làm vậy thì bản mới không kịp khởi chạy.
            _update_in_progress = True
            try:
                if _app_window_proc is not None and _app_window_proc.poll() is None:
                    _app_window_proc.terminate()
                    try:
                        _app_window_proc.wait(timeout=5)
                    except Exception:
                        pass
            except Exception:
                pass

            # 5. Khởi chạy bản mới độc lập (tách khỏi process tree để không bị kill chéo)
            time.sleep(0.8)
            child_env = _child_env_without_pyi()   # xem _child_env_without_pyi: thiếu là bản mới chết
            if platform.system() == "Windows":
                DETACHED_PROCESS = 0x00000008
                CREATE_NEW_PROCESS_GROUP = 0x00000200
                subprocess.Popen(
                    [exe_path],
                    creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
                    close_fds=True,
                    cwd=exe_dir,
                    env=child_env
                )
            else:
                subprocess.Popen([exe_path], close_fds=True, cwd=exe_dir, env=child_env)

            # Đóng pool SQL và thoát tiến trình cũ trực tiếp
            try:
                with _pool_lock:
                    for c in list(_conn_pool.values()):
                        try: c.close()
                        except: pass
                    _conn_pool.clear()
            except Exception:
                pass
            time.sleep(0.5)
            os._exit(0)

        except Exception as err:
            _update_in_progress = False
            with _update_lock:
                _update_state["status"] = "error"
                _update_state["error_message"] = str(err)
            if os.path.exists(temp_new_path):
                try:
                    os.remove(temp_new_path)
                except Exception:
                    pass

    t = threading.Thread(target=_async_download_and_swap, daemon=True)
    t.start()

    return jsonify({
        "status": "ok",
        "message": "Đang bắt đầu tải bản cập nhật trong nền."
    })


if __name__ == "__main__":
    # Dọn nền có retry: file .old là image của bản cũ vừa khởi chạy mình, phải đợi nó thoát hẳn.
    threading.Thread(target=_cleanup_old_executables, kwargs={"retry_seconds": 60},
                     daemon=True).start()
    import threading

    import webbrowser
    import time
    import socket

    APP_URL  = 'http://localhost:5050'
    APP_PORT = 5050

    def _find_chromium_browser():
        """Tìm path Chrome/Edge/Brave để mở app ở chế độ standalone (--app)."""
        candidates = []
        if platform.system() == "Windows":
            envs = [os.environ.get("ProgramFiles", r"C:\Program Files"),
                    os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                    os.environ.get("LocalAppData", os.path.expanduser(r"~\AppData\Local"))]
            rel_paths = [
                r"Google\Chrome\Application\chrome.exe",
                r"Microsoft\Edge\Application\msedge.exe",
                r"BraveSoftware\Brave-Browser\Application\brave.exe",
            ]
            for base in envs:
                if not base: continue
                for rel in rel_paths:
                    p = os.path.join(base, rel)
                    if os.path.exists(p):
                        candidates.append(p)
        else:
            # macOS / Linux: trông vào PATH
            for name in ("google-chrome", "chrome", "chromium", "msedge", "brave-browser"):
                from shutil import which
                p = which(name)
                if p: candidates.append(p)
        return candidates[0] if candidates else None

    def _wait_port_ready(host, port, timeout=15):
        """Đợi Flask đã bind port xong rồi mới mở browser."""
        end = time.time() + timeout
        while time.time() < end:
            try:
                with socket.create_connection((host, port), timeout=0.5):
                    return True
            except OSError:
                time.sleep(0.2)
        return False

    def _shutdown_everything(reason=""):
        """Đóng connection pool, kill chính tiến trình mình + mọi process con."""
        try:
            print(f"[shutdown] {reason}")
        except Exception:
            pass
        # Đóng connection pool SQL
        try:
            with _pool_lock:
                for c in list(_conn_pool.values()):
                    try: c.close()
                    except: pass
                _conn_pool.clear()
        except Exception:
            pass
        # Kill toàn bộ process tree của EXE → Flask + bất kỳ child nào
        try:
            if platform.system() == "Windows":
                subprocess.run(
                    f'taskkill /F /T /PID {os.getpid()}',
                    shell=True, capture_output=True
                )
            else:
                os.kill(os.getpid(), 9)
        except Exception:
            os._exit(0)

    def launch_app_window():
        """Mở app dưới dạng cửa sổ standalone. Khi user đóng cửa sổ → tắt server."""
        global _app_window_proc
        if not _wait_port_ready("127.0.0.1", APP_PORT):
            webbrowser.open(APP_URL)
            return  # Không track được → server chạy ngầm như cũ

        chromium = _find_chromium_browser()
        if not chromium:
            # Không có Chrome/Edge → fallback browser mặc định (không track được khi đóng)
            webbrowser.open(APP_URL)
            return

        # Profile dir riêng cho app
        if platform.system() == "Windows":
            profile_dir = os.path.join(os.environ.get("LocalAppData", os.path.expanduser(r"~\AppData\Local")),
                                       "iPOS_Ledger_Studio", "AppProfile")
        else:
            profile_dir = os.path.expanduser("~/.ipos_ledger_studio/AppProfile")

        try:
            os.makedirs(profile_dir, exist_ok=True)
        except Exception:
            profile_dir = None

        args = [
            chromium,
            f"--app={APP_URL}",
            "--new-window",
            "--disable-features=Translate",
            "--no-first-run",
            "--no-default-browser-check",
        ]
        if profile_dir:
            args.append(f"--user-data-dir={profile_dir}")

        try:
            # close_fds + KHÔNG dùng shell → có handle process thật để wait()
            _t_spawn = time.time()
            proc = subprocess.Popen(args, close_fds=True)
            _app_window_proc = proc   # updater cần handle này để đóng cửa sổ khi thay EXE
        except Exception:
            webbrowser.open(APP_URL)
            return

        # Block thread này cho tới khi user đóng cửa sổ Chrome --app
        try:
            proc.wait()
        except Exception:
            pass

        # Đang thay EXE: cửa sổ do CHÍNH updater đóng, không phải user. Shutdown ở đây sẽ giết
        # tiến trình trước khi nó kịp Popen bản mới → cập nhật xong không có gì chạy lên.
        if _update_in_progress:
            print("[launcher] Cua so dong do dang cap nhat -> khong shutdown, de updater lo")
            return

        # ⚠️ BẪY ĐÃ TỪNG LÀM SERVER "CHẾT NGAY KHI VỪA LÊN" (phát hiện 12/08/2026):
        # Nếu ĐÃ có sẵn 1 Chrome đang dùng chung --user-data-dir này (cửa sổ app cũ chưa đóng
        # hẳn, hoặc process mồ côi còn sót), thì chrome.exe vừa spawn sẽ BÀN GIAO việc mở cửa sổ
        # cho instance cũ rồi TỰ THOÁT NGAY (<1s). proc.wait() trả về tức thì → hiểu nhầm là
        # "user đã đóng cửa sổ" → server taskkill chính nó → EXE thoát mã 1, mọi request sau đó
        # báo "Failed to fetch" dù code hoàn toàn đúng. Triệu chứng điển hình: vừa build xong,
        # chạy EXE là chết ngay, phải đóng hết Chrome mới chạy được.
        # => Thoát quá nhanh = bàn giao, KHÔNG phải user đóng cửa sổ. Giữ server chạy ngầm,
        #    đúng như nhánh dự phòng "không track được" ở trên.
        if time.time() - _t_spawn < 5:
            print("[launcher] Chrome ban giao cho instance cu (thoat <5s) -> giu server chay ngam")
            return

        # User đã đóng cửa sổ → shutdown toàn bộ
        _shutdown_everything("Cua so app da bi dong")

    def _wait_port_free(port, timeout=6):
        """Đợi cổng được nhả. Sau khi tự cập nhật, bản mới khởi chạy trong lúc bản cũ còn
        vài trăm ms nữa mới thoát — bind ngay là OSError 10048 rồi rơi vào `finally` tự tắt,
        người dùng thấy "cập nhật xong mở lên là tắt ngay".

        Timeout để ngắn có chủ đích: Werkzeug bind kèm SO_REUSEADDR nên trên Windows nó CƯỚP
        được cổng kể cả khi một tiến trình ma còn đang LISTEN (đã đo), còn phép thử ở đây thì
        không — gặp ghost server là đợi cho hết timeout rồi mới chạy tiếp. Hết giờ vẫn chạy,
        chỉ chậm, không chặn."""
        end = time.time() + timeout
        while time.time() < end:
            s_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s_test.bind(("0.0.0.0", port))
                return True
            except OSError:
                time.sleep(0.3)
            finally:
                try: s_test.close()
                except Exception: pass
        return False

    _wait_port_free(APP_PORT)

    # Chạy launcher ở thread riêng (không daemon vì cần block để kill khi đóng)
    launcher = threading.Thread(target=launch_app_window, daemon=True)
    launcher.start()

    # Bắt Ctrl+C / signal tắt sạch
    import signal
    def _signal_handler(signum, frame):
        _shutdown_everything(f"Nhan signal {signum}")
    try:
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)
    except Exception:
        pass

    # use_reloader=False để khi đóng gói EXE không spawn process con
    try:
        app.run(host="0.0.0.0", port=APP_PORT, debug=False, use_reloader=False)
    finally:
        _shutdown_everything("Flask exited")
