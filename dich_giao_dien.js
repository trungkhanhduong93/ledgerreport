// dich_giao_dien.js — Việc 24 (29/09/2026): DỊCH SẴN giao diện lúc đóng gói.
//
// Trước đây mỗi lần mở app, trình duyệt phải tải Babel (~3 MB) rồi dịch ~9.400 dòng JSX trong <script type="text/babel">
// ⇒ màn trắng ~7–13 giây. Script này dịch MỘT LẦN lúc build, ghi ra web_dich_san/index.html; build_exe.py và
// release.yml nhúng file đó vào EXE THAY CHO index.html gốc. Chạy server.py từ mã nguồn thì vẫn dùng index.html gốc
// (Babel dịch trong trình duyệt như cũ) ⇒ sửa giao diện vẫn chỉ sửa index.html, KHÔNG sửa file trong web_dich_san/.
//
// ⛔ Tuỳ chọn Babel dưới đây là ĐÚNG tuỳ chọn @babel/standalone 7.29.7 tự dùng cho <script type="text/babel"> không có
//    data-presets / data-plugins (đọc từ chính file thu-vien/babel-standalone-7.29.7.min.js, hàm dựng tuỳ chọn cạnh chữ
//    sourceMaps:"inline"). Khác đúng một chỗ: không kèm sourcemap. ⇒ code chạy trong EXE = code trình duyệt tự dịch trước
//    đây, từng ký tự. Đổi preset (vd bỏ "env" cho gọn) là đổi cách code chạy — phải thử lại toàn bộ app, đừng tiện tay.
//
// Chạy: node dich_giao_dien.js   (không cần npm install — Babel lấy từ thu-vien/)
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const GOC = __dirname;
const TEP_BABEL = 'babel-standalone-7.29.7.min.js';
const THE_BABEL = `    <script src="/thu-vien/${TEP_BABEL}"></script>\n`;
const MO = '<script type="text/babel">';
const DONG = '</script>';
const RA = path.join(GOC, 'web_dich_san', 'index.html');

const TUY_CHON_BABEL = {
    presets: ['react', 'env'],
    plugins: ['transform-class-properties', 'transform-object-rest-spread', 'transform-flow-strip-types'],
    targets: { browsers: undefined },
    filename: 'giao-dien.jsx',
    sourceMaps: false,
    babelrc: false,
    configFile: false,
    browserslistConfigFile: false,   // chạy trong node đừng đi đọc .browserslistrc / package.json — trình duyệt không có
};

function viTriDuyNhat(s, chuoi, ten) {
    const i = s.indexOf(chuoi);
    if (i < 0) throw new Error(`Không thấy ${ten} trong index.html`);
    if (s.indexOf(chuoi, i + 1) >= 0) throw new Error(`${ten} xuất hiện hơn một lần trong index.html — script chỉ biết dịch đúng một khối`);
    return i;
}

function main() {
    const t0 = Date.now();
    const Babel = require(path.join(GOC, 'thu-vien', TEP_BABEL));
    const goc = fs.readFileSync(path.join(GOC, 'index.html'), 'utf8');
    // Trình duyệt chuẩn hoá xuống dòng về \n trước khi Babel đọc innerHTML — làm y vậy để code dịch ra trùng khít.
    const html = goc.replace(/\r\n?/g, '\n');

    const i = viTriDuyNhat(html, MO, 'thẻ <script type="text/babel">');
    const j = html.indexOf(DONG, i);
    if (j < 0) throw new Error('Thẻ <script type="text/babel"> không có thẻ đóng');
    const nguon = html.slice(i + MO.length, j);

    const code = Babel.transform(nguon, TUY_CHON_BABEL).code;
    // Code nằm thẳng trong <script> ⇒ chuỗi "</script" bên trong sẽ cắt ngang thẻ. Nguồn cũng nằm trong <script> nên
    // vốn không thể có — kiểm cho chắc, có là dừng chứ đừng sinh file hỏng.
    if (/<\/script/i.test(code)) throw new Error('Code dịch ra có chuỗi "</script" — không nhúng thẳng vào HTML được');

    // Băm bản ĐÃ chuẩn hoá xuống dòng: runner Windows của GitHub checkout ra CRLF, máy dev có thể LF — cùng nội dung
    // thì phải cùng dấu.
    const bamNguon = crypto.createHash('sha256').update(html, 'utf8').digest('hex');
    let ra = html.slice(0, i)
        + `<script>\n/* DỊCH SẴN lúc đóng gói bởi dich_giao_dien.js từ index.html (sha256 ${bamNguon.slice(0, 16)}…). `
        + `ĐỪNG sửa file này — sửa index.html rồi build lại. */\n`
        + code + '\n' + DONG
        + html.slice(j + DONG.length);

    viTriDuyNhat(ra, THE_BABEL, 'thẻ nạp Babel');
    ra = ra.replace(THE_BABEL, '');                  // đã dịch sẵn ⇒ khỏi tải + khởi động Babel ~3 MB
    const MOC = '<meta charset="UTF-8">';
    viTriDuyNhat(ra, MOC, 'thẻ <meta charset>');
    // Dấu để kiểm từ ngoài (M3): trang đang chạy là bản dịch sẵn, dịch từ index.html nào.
    ra = ra.replace(MOC, `${MOC}\n    <meta name="giao-dien-dich-san" content="${bamNguon}">`);

    fs.mkdirSync(path.dirname(RA), { recursive: true });
    fs.writeFileSync(RA, ra, 'utf8');
    console.log(`[OK] Dich san giao dien: ${nguon.length.toLocaleString('en')} ky tu JSX -> ${code.length.toLocaleString('en')} ky tu JS`
        + ` · ${path.relative(GOC, RA)} ${(Buffer.byteLength(ra) / 1024).toFixed(0)} KB · ${((Date.now() - t0) / 1000).toFixed(1)}s`
        + ` · nguon sha256 ${bamNguon.slice(0, 16)}`);
}

try { main(); } catch (e) { console.error('[LOI] Dich san giao dien:', e.message); process.exit(1); }
