# 📱 Hướng Dẫn Sử Dụng AndroZoo Downloader (`az`)

> Tool dòng lệnh để tải APK ngẫu nhiên từ kho [AndroZoo](https://androzoo.uni.lu/) theo các tiêu chí lọc tùy chỉnh.

---

## 📋 Mục Lục

- [Yêu cầu](#yêu-cầu)
- [Cài đặt](#cài-đặt)
- [Cấu hình](#cấu-hình)
- [Cách sử dụng](#cách-sử-dụng)
- [Các tham số](#các-tham-số)
- [Ví dụ thực tế](#ví-dụ-thực-tế)
- [Đóng góp](#đóng-góp)

---

## Yêu Cầu

- **Python 3.6** trở lên

---

## 🚀 Cài Đặt


### Bước 1 — Cài package

```bash
pip install azoo
```

### Bước 2 — Lấy API Key

Đăng ký tại [AndroZoo](https://androzoo.uni.lu/) để nhận API key miễn phí.

### Bước 3 — Tải file danh sách APK

Tải file `latest.csv.gz` tại: https://androzoo.uni.lu/static/lists/latest.csv.gz

Sau đó giải nén:

```bash
gunzip latest.csv.gz
```

---

## ⚙️ Cấu Hình

Có thể cấu hình API key và input file theo **3 cách**, ưu tiên theo thứ tự:

```
CLI option  >  File .az cục bộ  >  File .az toàn cục
```

### Cách 1 — File `.az` toàn cục (khuyến nghị)

Tạo file `.az` trong thư mục home:

- **Linux / macOS:** `~/.az`
- **Windows:** `C:\Users\%USERNAME%\.az`

Nội dung file:

```
key=YOUR_API_KEY_HERE
input_file=/đường/dẫn/tới/latest.csv
```

### Cách 2 — File `.az` cục bộ

Tạo file `.az` ngay trong thư mục bạn sẽ chạy lệnh `az`.

### Cách 3 — CLI option

```bash
az -k YOUR_API_KEY -i /path/to/latest.csv [các tham số khác]
```

---

## 📖 Cách Sử Dụng

```bash
az [OPTIONS]
```

### Cú pháp khoảng giá trị

Các tham số như `dexdate`, `apksize`, `vtdetection` nhận khoảng giá trị theo định dạng:

```
lower:upper   # cả hai đầu đều inclusive
:upper        # không giới hạn dưới
lower:        # không giới hạn trên
```

---

## 🔧 Các Tham Số

| Tham số | Mô tả |
|---|---|
| `-n, --number` | Số lượng APK cần tải |
| `-d, --dexdate` | Ngày của file dex, định dạng `%Y-%m-%d` (vd: `2015-10-03`) |
| `-s, --apksize` | Kích thước APK, tính bằng bytes |
| `-vt, --vtdetection` | Điểm VirusTotal (số nguyên) |
| `-pn, --pkgname` | Tên package (một hoặc nhiều, phân cách bằng dấu phẩy) |
| `-m, --markets` | Market nguồn (một hoặc nhiều, phân cách bằng dấu phẩy) |
| `--sha256` | Lọc theo SHA256 hash |
| `--sha1` | Lọc theo SHA1 hash |
| `--md5` | Lọc theo MD5 hash |
| `-md, --metadata` | Các cột metadata cần lưu vào `metadata.csv` |
| `-o, --out` | Thư mục đầu ra (mặc định: thư mục hiện tại) |
| `-sd, --seed` | Seed cho thuật toán random (giúp tái tạo kết quả) |
| `-k, --key` | AndroZoo API key |
| `-i, --input-file` | Đường dẫn đến file `latest.csv` |
| `-t, --threads` | Số luồng tải đồng thời (mặc định: 4) |
| `--version` | Hiển thị phiên bản |
| `--help` | Hiển thị trợ giúp |

### Các market hỗ trợ

```
1mobile, angeeks, anzhi, apk_bang, appchina, fdroid, freewarelovers,
genome, hiapk, markets, mi.com, play.google.com, proandroid, slideme, torrents
```

> ⚠️ Danh sách market có thể thay đổi do kho dữ liệu liên tục cập nhật.

### Metadata mặc định

Nếu không chỉ định `-md`, các cột mặc định được lưu là:

```
sha256, pkg_name, apk_size, dex_date, markets
```

---

## 💡 Ví Dụ Thực Tế

### 1. Ví dụ cơ bản từ tài liệu gốc

```bash
az -n 10 -d 2015-12-11: -s :3000000 -m play.google.com,appchina
```

Tải 10 APK từ `play.google.com` hoặc `appchina`, dexdate từ 2015-12-11 trở đi, kích thước tối đa 3MB.

---

### 2. Tải APK Goodware (sạch 100%) từ Google Play

```bash
az -n 100 \
   -m play.google.com \
   -vt 0:0 \
   -o ./goodware_apks
```

---

### 3. Tải APK quy mô lớn, nhiều luồng

```bash
az -n 500 \
   -m play.google.com \
   -vt 0:0 \
   -d 2020-01-01: \
   -s :10000000 \
   -t 8 \
   -o ./dataset
```

Tải 500 APK goodware từ Google Play, dexdate từ 2020, kích thước < 10MB, dùng 8 luồng.

---

### 4. Tải có thể tái tạo (reproducible)

```bash
az -n 100 -m play.google.com -vt 0:0 -sd 42 -o ./goodware_apks
```

Dùng `-sd 42` để mỗi lần chạy lại đều cho ra đúng bộ APK đó.

---

### 5. Tải APK theo hash cụ thể

```bash
az --sha256 abc123def456...,xyz789... -o ./specific_apks
```

---

### 6. Tùy chỉnh metadata lưu ra

```bash
az -n 50 -m play.google.com -vt 0:0 \
   -md sha256,pkg_name,apk_size,dex_date,markets,vt_detection \
   -o ./output
```

---

## Kết Quả Đầu Ra

Sau khi chạy, thư mục đầu ra sẽ chứa:

```
output/
├── *.apk           # Các file APK đã tải
└── metadata.csv    # Thông tin metadata của từng APK
```

---

## Đóng Góp

Dự án hiện đang mở để cộng đồng đóng góp. Nếu bạn thấy điều gì có thể cải thiện:

1. Tạo **Pull Request** trên GitHub
2. Xem **Trello board** để lấy ý tưởng: [az Trello Board](https://trello.com/b/45PDuGf6/az)


*Tài liệu này được tạo dựa trên README gốc của dự án AndroZoo Downloader (`azoo`).*