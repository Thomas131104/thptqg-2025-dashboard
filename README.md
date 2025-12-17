# THPTQG 2025 Dashboard

Dashboard tương tác phân tích kết quả kỳ thi THPT Quốc gia 2025

## 1. Mục tiêu dự án

Phân tích tổng điểm xét tuyển đại học của hơn 1 triệu thí sinh.

Hiển thị phân bố điểm theo môn, tỉnh/thành, tổ hợp.

Dashboard trực quan, dễ tương tác, giúp quan sát dữ liệu nhanh chóng.

---

## 2. Workflow dữ liệu

- Repo preprocessing (thptqg-2025-preprocessing
)

    - Dọn sạch missing value, xử lý môn “trashy”.

    - Mapping mã tỉnh, sáp nhập tỉnh, tính tổng điểm.

    - Lưu kết quả Parquet để dùng cho dashboard.

- Repo dashboard (thptqg-2025-dashboard
)

    - Input Parquet từ preprocessing → hiển thị biểu đồ, bản đồ, bảng.

    - Tên file / cột được chuẩn hóa sang tiếng Anh để đồng bộ với code và giao diện.

--- 

## 3. Cấu trúc repo

```txt
- data/          # File Parquet đã tiền xử lý
- geojson/       # File GeoJSON cho bản đồ
- app.py         # File chính Dash app
- requirements.txt
- README.md      # File hướng dẫn
```

---

## 4. Hướng dẫn chạy

- Cách 1:
    - B1: Clone repo: `git clone https://github.com/Thomas131104/thptqg-2025-dashboard`
    - B2: Cài dependency: `pip install -r requirements.txt`
    - B3: Chạy chương trình: `pip install -r requirements.txt`
    - B4: Mở trang `127.0.0.1:65000` để xem kết quả

- Cách 2: Truy cập phiên bản public trên Dash Cloud `https://db5359fd-112f-4692-8773-628e752d7392.plotly.app/`

---

## 5. Thông tin dữ liệu

Nguồn dữ liệu gốc:

| **STT** | **Dữ liệu**                                    | **Nguồn**                                                                                                                                                                                          | **Mục đích sử dụng**                                         |
| ------- | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| 1       | Bảng điểm kỳ thi THPTQG 2025                   | [Chính phủ](https://xaydungchinhsach.chinhphu.vn/thoi-gian-cong-bo-diem-thi-tot-nghiep-nam-2025-119250326142147171.htm)                                                                            | Tính tổng điểm xét tuyển đại học, phân tích kết quả thí sinh |
| 2       | Bản đồ Việt Nam (GeoJSON)                      | [GIS Việt Nam](https://gis.vn)                                                                                                                                                                     | Vẽ bản đồ phân bố thí sinh theo tỉnh/thành phố               |
| 3       | Bảng quy đổi mã tỉnh (trước sáp nhập)          | [Lao Động](https://laodong.vn/giao-duc/danh-sach-65-hoi-dong-thi-tot-nghiep-thpt-thi-sinh-tranh-nham-de-truot-oan-896441.ldo)                                                                      | Chuẩn hóa mã tỉnh trong bảng điểm                            |
| 4       | Bảng quy đổi tỉnh trước và sau sáp nhập        | [Thư viện Pháp luật](https://thuvienphapluat.vn/phap-luat/ho-tro-phap-luat/danh-sach-sap-nhap-34-tinh-thanh-moi-nhat-2025-ten-goi-trung-tam-hanh-chinh-dien-tich-va-dan-so-ra--475580-214308.html) | Đối chiếu dữ liệu giữa các năm, cập nhật tên tỉnh/thành mới  |
| 5       | Bảng quy đổi tổ hợp môn xét tuyển đại học 2025 | [Tuyensinh247](https://thi.tuyensinh247.com/danh-sach-to-hop-xet-tuyen-nam-2025-theo-36-cach-chon-c24a80790.html)                                                                                  | Xác định tổ hợp môn xét tuyển của từng thí sinh              |

---

## 6. Bảng quy đổi file

| **File gốc (Preprocessing)** | **File chuẩn hóa (Dashboard)** | **Ghi chú**                        |
| ---------------------------- | ------------------------------ | ---------------------------------- |
| `diem_thi_2025.parquet`      | `diem_thi_2025.parquet`     | Bảng điểm thí sinh                 |
| `Việt Nam (tỉnh thành) - 34.geojson`    | `after-merging.geojson`          | GeoJSON bản đồ Việt Nam (Sau sáp nhập)         |
| `Việt Nam (tỉnh thành) - 63.geojson`    | `after-merging.geojson`          | GeoJSON bản đồ Việt Nam (Trước sáp nhập)         |
| `Quy đổi tỉnh thành.csv`          | `conversing-provinces.csv`           | Bao gồm bảng quy đổi tỉnh thành trước và sau sáp nhập, và mã tỉnh thành theo hội đồng coi thi |
| `Bảng tổ hợp môn.csv`             | `conversing_combinations.csv`        | Quy đổi tổ hợp môn xét tuyển       |


---

## 7. Công nghệ sử dụng

- Python: Polars, Pandas, GeoPandas, Plotly
- Dashboard: Dash + Dash Bootstrap Components
- Deployment: Dash Cloud public

---

By Mus