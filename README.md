# Kho Game F2P

Trang tĩnh (không cần build). Mỗi game là một thư mục trong `games/`, danh sách hiển thị lấy từ `games.json`.

## Thêm game mới
1. Tạo thư mục `games/<ten-game>/` chứa `index.html` (và `assets/` nếu có) cùng ảnh bìa `cover.png` (tỉ lệ 16:9, ví dụ 800x450).
2. Thêm một mục vào `games.json` (`url` trỏ tới `games/<ten-game>/`, hoặc một địa chỉ web đầy đủ nếu game nằm nơi khác).
3. Thêm địa chỉ game vào `sitemap.xml`.
4. Commit và push — Cloudflare Pages tự đăng lại sau ít phút.

Trong game, dùng đường dẫn tương đối (ví dụ `assets/hinh.png`), không dùng `/assets/...`.

## Triển khai
Cloudflare Pages: kết nối repo này, Build command để trống, Output directory là `/` (thư mục gốc).

## Bản quyền hình ảnh
- Ngọn Đèn Rừng Sương: Ninja Adventure Asset Pack — Pixel-boy & AAA, giấy phép CC0.
