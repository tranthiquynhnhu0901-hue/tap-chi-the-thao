# TẠP CHÍ THỂ THAO — website tĩnh không cần build

Phiên bản: 14/10/2026 · 8 chuyên mục · 48 bài · HTML/CSS/JavaScript tĩnh.

## Triển khai GitHub Pages (không cần Node.js / npm)

1. Giải nén `tap-chi-the-thao.zip`.
2. Mở thư mục `tap-chi-the-thao` **bên trong ZIP** rồi upload toàn bộ tệp, thư mục, kể cả `.nojekyll`, lên gốc repository `tap-chi-the-thao` của GitHub. Đừng đưa thêm một cấp thư mục bên ngoài vào repository.
3. Vào **Settings → Pages → Build and deployment → Deploy from a branch**, chọn `main` và `/ (root)`, nhấn Save.
4. Chờ GitHub Pages hoàn tất triển khai, truy cập `https://<username>.github.io/tap-chi-the-thao/`.

**Cấu hình URL hiện tại:** `https://tranthiquynhnhu0901-hue.github.io/tap-chi-the-thao/`. Đây là URL canonical được chọn từ tên tài khoản trong URL SPORTHUB, **chưa xác minh có repository/triển khai thực tế**. Nếu tài khoản, repo hoặc domain khác, chạy `python scripts/change-base.py https://<username>.github.io/<repository>/` trước khi upload; hoặc sửa thủ công canonical, Open Graph URL, Schema, RSS, sitemap và robots. Script này chỉ dùng khi **đổi URL**, không dùng để build site. Với custom domain, nhập URL domain mới kết thúc `/`.

Toàn bộ liên kết CSS/JS/ảnh nội bộ dùng đường dẫn tương đối phù hợp dự án chạy trong subpath; việc thay đổi canonical không làm thay đổi liên kết SPORTHUB.

## Những gì có trong gói

- `index.html`: trang chủ có feature, bài mới, chuyên mục, phân tích, hướng dẫn.
- `bai-viet/<slug>/index.html`: **48 trang SEO được dựng sẵn**, nội dung chính hiển thị ngay khi không có JavaScript.
- `chuyen-muc/<slug>/index.html`: **8 chuyên mục**, mỗi mục 6 bài, phân trang 3 bài/lần (có JavaScript).
- `tim-kiem.html`: tìm kiếm tiếng Việt có hỗ trợ bỏ dấu bằng JavaScript, tải chỉ mục JSON nhỏ; yêu cầu chạy qua HTTP/GitHub Pages (không cần backend).
- `gioi-thieu/index.html`, `404.html`, `.nojekyll`, `robots.txt`, `sitemap.xml`, `feed.xml`.
- `assets/css/style.css`, `assets/js/site.js` — giao diện responsive và tương tác. 48 ảnh minh họa phong cách ảnh chụp tạo bằng AI được lưu cục bộ tại `assets/images/`.
- `data/articles.json`: dữ liệu bài, từ khóa, intent, nội dung, nguồn, ngày đăng, ảnh, liên kết nội bộ và SPORTHUB.
- `data/ecosystem-links.json`: **77 URL cho phép** (5 trang chính, 52 sản phẩm, 20 blog). Chỉ năm trang chính được đặt trong bài do chưa xác minh trang đích riêng lẻ.
- `reports/`: audit liên kết, bài viết, ảnh, trạng thái xác minh và thử nghiệm runtime.
- `scripts/audit-links.py`: quét tệp HTML đã dựng, đếm link thực nằm trong thân bài và kiểm tra local URL/ảnh.

## Bản xem trước độc lập

Tệp `tap-chi-the-thao-preview.html` được giao **riêng ngoài ZIP**. Có CSS, JS và toàn bộ 48 nội dung bài viết trong một tệp; 48 ảnh được nhúng dạng data URI nên hiển thị được khi không có Internet. Mở tệp bằng Chrome/Edge thông thường, điều hướng `#/`, `#/chuyen-muc/slug`, `#/bai-viet/slug` và tìm kiếm theo `#/tim-kiem?q=...`. Không cần chạy server, Node hay kết nối mạng cho nội dung. Các liên kết ra SPORTHUB cần Internet.

## Trạng thái SEO và SPORTHUB — đọc trước khi xuất bản chính thức

- Kỹ thuật nội bộ được quét trên 48 HTML: mỗi bài có **5 liên kết SPORTHUB trong thân bài**, có mục “Tìm hiểu thêm”, 3 internal link ngữ cảnh, Article/Breadcrumb JSON-LD, meta, canonical, ảnh ALT. Tổng **240 lần xuất hiện** với **3 URL đích khác nhau**, không tính menu/footer.
- Tuy nhiên, **chưa thể xác minh trực tuyến** các URL đích của SPORTHUB qua công cụ hiện tại. Vì vậy 52 URL sản phẩm và 20 URL blog chỉ có trong danh mục, tuyệt đối không đặt tên hay gán chủ đề. Chỉ 3 trang đích cấp cao (home, shop, blog) được liên kết và cần rà soát trạng thái cùng **chất lượng ngữ cảnh biên tập** trước khi công khai.
- Các bài viết được soạn theo kiến thức phổ thông, có nguồn đối chiếu nhưng **chưa trải qua phản biện chuyên môn độc lập**. Không sử dụng tiêu đề, ngày đăng, tư cách tác giả được bịa ra để thay cho xác minh thực tế. Tên “Ban biên tập” là nhãn tập thể dự án, không phải một chuyên gia có chứng chỉ.
- Các bìa dùng 48 ảnh phong cách ảnh chụp tạo bằng AI, phân bổ 1 ảnh riêng cho mỗi bài. Ảnh không phải ảnh chụp sự kiện có thật; toàn bộ nằm trong ZIP.
- Bản xem trước đã được thử điều hướng client-side trong trình duyệt tự động bằng phương thức nạp HTML vào trang thử; môi trường hiện tại **chặn truy cập file:// và localhost bằng chính sách quản trị**, vì vậy không thể khẳng định đã trực tiếp mở file từ ổ đĩa hay chạy thử qua GitHub Pages. Kết quả ghi trong `reports/browser-tests.json`.

### Quy trình xuất bản có trách nhiệm

1. Xác minh online 77 URL, thông tin sản phẩm/blog, không tự suy đoán tên theo ID.
2. Duyệt thủ công vị trí từng liên kết SPORTHUB, bỏ các liên kết cấp cao gây quảng bá gượng ép; thay bằng đích cụ thể đã xác minh nếu liên quan. Chỉ công bố bài khi có ít nhất 5 liên kết thật sự hữu ích như trong đề bài.
3. Đề nghị người đủ chuyên môn rà lại kỹ thuật thể thao, luật thi đấu mới nhất, khuyến nghị dinh dưỡng và nhận diện tác giả/đơn vị xuất bản.
4. Thử thêm mobile, accessibility, tốc độ và link live trên domain triển khai thật.
5. Chạy `python scripts/audit-links.py` sau mỗi lần chỉnh HTML. Báo cáo SEO kỹ thuật **không phải điểm chính thức của Google**.

## Chỉnh sửa bài viết

Bạn có thể sửa HTML trong `bai-viet/<slug>/index.html`, cập nhật song song trường tương ứng trong `data/articles.json`, rồi cập nhật sitemap/RSS nếu tạo mới hoặc đổi slug. Website cuối cùng không cần một CMS hay công cụ build. Với nhiều bài, nên dùng quy trình biên tập có version control; không có backend và không có chức năng lưu bài online giả.

## Giấy phép minh họa

Bộ ảnh minh họa AI nằm cục bộ tại `assets/images/` và nguồn được ghi tại `reports/image-attribution.csv`. Các URL Unsplash trước đó chỉ được lưu cho mục đích lịch sử tại `reports/previous-remote-images.csv`.


## Cập nhật giao diện / hình ảnh / contextual links (v2)

- Giao diện tạp chí có **48 ảnh phong cách ảnh chụp tạo bằng AI**, không phải ảnh tư liệu; tất cả đều lưu thành WebP cục bộ và có thể hiển thị offline. Nếu website yêu cầu ảnh nhiếp ảnh gia thật, cần thay các ảnh này bằng tác phẩm có quyền sử dụng phù hợp.
- Mỗi bài có **4 link ngữ cảnh trên keyword trong thân bài + 1 liên kết ngữ cảnh trong “Tìm hiểu thêm”**. Anchor mô tả đúng nhóm chủ đề, không có các link giới thiệu/liên hệ chèn máy móc. Vì chưa xác minh được chi tiết trang đích SPORTHUB, các liên kết body chỉ dẫn về trang `shop.html` và `blog.html`, kết bài dẫn về trang chủ. 52 URL sản phẩm và 20 URL blog vẫn lưu đầy đủ, chưa sử dụng tùy tiện.
- Nếu cập nhật nội dung, sử dụng `data/articles.json` là nguồn biên tập rồi sửa trang HTML tương ứng, hoặc dùng script xây dựng của dự án nếu tích hợp lại công cụ build. Mã nguồn kết quả trong ZIP đã biên dịch sẵn.

## Cập nhật V3 — phân vai font và checklist SEO (14/10/2026)

### Hệ typography ba vai trò

- **Barlow Condensed**: logo, tiêu đề chuyên mục, nhãn nổi bật, số thứ tự và thành phần display.
- **Noto Serif**: tiêu đề bài trên thẻ, bài nổi bật, H1 chi tiết bài và tiêu đề H2 trong thân bài để tạo cảm giác tạp chí biên tập.
- **Be Vietnam Pro**: văn bản tiếng Việt dài, menu, nút, mô tả, breadcrumb, metadata, mục lục và biểu mẫu. Riêng câu mở đầu lớn của trang chủ dùng Be Vietnam Pro đậm để đảm bảo dấu tiếng Việt dễ đọc trên mobile.

Font tải tùy chọn qua Google Fonts; khi ngoại tuyến, browser tự dùng các font hệ thống dự phòng. **Không có file font nào cần tải/biên dịch**. Các giá trị được quản lý trong `assets/css/style.css` với biến `--display`, `--editorial` và `--ui`; bản HTML preview đã được đồng bộ hệ font này.

### SEO được cập nhật trên toàn bộ HTML

- **60 trang HTML** được rà soát: 48 bài, 8 chuyên mục, trang chủ, trang giới thiệu, trang tìm kiếm và trang 404.
- **Title Tag:** 50–60 ký tự; Meta Description: 105–125 ký tự, được viết từ mô tả đúng từng nội dung. Trường meta trong `data/articles.json` đồng bộ với HTML.
- **Canonical:** URL tuyệt đối theo `data/site-config.json`; tránh đổi slug bài viết cũ không cần thiết. Canonical không đồng nghĩa với việc URL GitHub Pages hiện tại đã tồn tại trên mạng.
- **Robots:** công khai `index, follow`; `/tim-kiem.html` và `/404.html` dùng `noindex, follow`. Sitemap chỉ có **58 canonical có thể index** và loại bỏ hai trang `noindex`.
- **Schema.org JSON-LD:** `Organization`/`WebSite` và `WebPage` cho trang chủ; `Article` + `BreadcrumbList` cho bài viết; `CollectionPage` + `BreadcrumbList` cho chuyên mục; `AboutPage` cho giới thiệu. Trang tìm kiếm `SearchResultsPage` và 404 `WebPage` nhưng `noindex`.
- **Heading:** đúng một H1 trong từng HTML; trang chủ có H1 giới thiệu toàn tạp chí, bài nổi bật và các bài phụ chuyển xuống H2. Footer không dùng các heading lạc cấp.
- **Alt/link:** alt ảnh, link nội bộ và canonical đều nằm trong bộ kiểm tra; ảnh dùng host bên ngoài nên tình trạng HTTP/hotlink vẫn cần xác minh trên domain thật.

### Cách tự chạy audit SEO, không cần thư viện Python bên thứ ba

```bash
python scripts/audit-seo.py
python scripts/audit-links.py
```

Báo cáo xuất ra `reports/seo-audit.csv`, `reports/seo-audit-summary.json` và các báo cáo liên kết. Script SEO kiểm tra title/description, H1, canonical, meta robots, kiểu schema và JSON hợp lệ, ảnh có alt, link nội bộ tồn tại, sitemap khớp trang `index`. Đây là **kiểm tra tại chỗ**, không phải kết quả Google Search Console/Rich Results Test hay xác minh ảnh, link SPORTHUB thực tế.

Nếu đổi tài khoản/repository/domain GitHub Pages, chạy `scripts/change-base.py` **trước khi xuất bản**, rồi chạy lại `audit-seo.py` để kiểm tra canonical, schema, sitemap và robots. Không cần đổi các đường dẫn bài viết đã hoạt động tốt.


## Ảnh minh họa cục bộ — bản bàn giao cuối

- Tất cả 48 bài hiện dùng 48 ảnh minh họa phong cách ảnh chụp tạo bằng AI, mỗi bài có ảnh riêng trong `assets/images/`. Đây **không phải ảnh chụp của nhiếp ảnh gia**, hình tư liệu sự kiện hay hình ảnh người thật.
- Ảnh đã tạo và được đóng gói trong ZIP nên GitHub Pages hiển thị được khi người dùng không kết nối trực tiếp tới Unsplash. CSS trang chủ dùng ảnh cục bộ; bản preview lưu ảnh dưới dạng data URI để hoạt động độc lập.
- 31 URL ảnh Unsplash từng sử dụng ở phiên bản trước được lưu lưu vết tại `reports/previous-remote-images.csv`, không được dùng để nhận công tác giả đối với những ảnh AI mới.
- Bảng nguồn mới: `reports/image-attribution.csv`. Kiểm tra tính toàn vẹn ảnh: `python scripts/audit-images.py`.
- Nếu cần sử dụng **ảnh chụp thật tuyệt đối**, phải thay ảnh minh họa AI bằng tệp ảnh được cấp phép thích hợp trước khi tuyên bố đó là ảnh tư liệu.
