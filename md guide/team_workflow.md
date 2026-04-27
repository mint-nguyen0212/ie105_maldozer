# 👥 Hướng Dẫn Làm Việc Nhóm - MalDozer Project

> **Nguyên tắc:** File APK (hàng chục GB) **KHÔNG** được commit vào Git.
> Chỉ commit **code, guide, model, và kết quả**.

---

## 📐 Cấu Trúc Repo Trên GitHub

```
IE105_maldozer/
├── .gitignore              ← Chặn APK & data trung gian
├── code/                   ← ✅ CÓ trên Git
│   ├── *.py                ← Source code
│   ├── method_dict.pickle  ← Dictionary ánh xạ (4.3 MB, có sẵn)
│   ├── word2vec.model      ← Model Word2Vec (sau Step 3)
│   └── deep_learning.model ← Model CNN (sau Step 4)
├── md guide/               ← ✅ CÓ trên Git
│   ├── training_guide.md
│   ├── team_workflow.md    ← File này
│   └── ...
└── data/                   ← ❌ KHÔNG trên Git (bị .gitignore)
    ├── apks/               ← File APK gốc
    ├── apis/               ← Output Step 1
    └── identifiers/        ← Output Step 2
```

---

## 🔄 Workflow Làm Việc Nhóm

### Người Train (tải APK + chạy pipeline)

```
1. git clone / git pull         ← Lấy code mới nhất
2. Tải APK từ nguồn ngoài      ← Google Drive / AndroZoo
3. Đặt APK vào data/apks/      ← Đúng cấu trúc goodware/ + malware/
4. Chạy pipeline training       ← Step 1 → 2 → 3 → 4
5. Chạy test.py                 ← Đo accuracy
6. git add & commit & push      ← CHỈ commit model + kết quả
```

### Người khác (review kết quả)

```
1. git pull                     ← Nhận model + kết quả (vài MB)
2. Xem kết quả accuracy         ← Từ file kết quả
3. (Tùy chọn) Tải APK riêng    ← Nếu muốn chạy lại / test thêm
```

---

## 📦 Chia Sẻ Dataset APK

### Cách 1: Google Drive (Đơn giản nhất)

1. Upload toàn bộ folder `data/apks/` lên Google Drive
2. Chia sẻ link cho nhóm
3. Người nhận tải về, giải nén vào `data/apks/`

### Cách 2: Link tải từ AndroZoo

Nếu dataset lấy từ AndroZoo, chỉ cần chia sẻ:
- File CSV chứa danh sách SHA256 hash của APK
- API key của AndroZoo
- Script tải tự động (xem bên dưới)

---

## 📝 Commit Gì Sau Khi Train?

### ✅ NÊN commit:

| File | Kích thước | Lý do |
|------|-----------|-------|
| `word2vec.model` | ~1-2 MB | Model embedding, cần cho Step 4 |
| `deep_learning.model` | ~5-20 MB | Model CNN đã train |
| Kết quả accuracy (screenshot/text) | < 1 MB | Báo cáo |
| Code đã sửa (*.py) | < 1 MB | Source code |

### ❌ KHÔNG commit:

| File | Kích thước | Lý do |
|------|-----------|-------|
| `data/apks/*.apk` | **20-50 GB** | Quá lớn, đã có .gitignore |
| `data/apis/*.feature` | ~500 MB | Output trung gian, tái tạo được |
| `data/identifiers/*` | ~200 MB | Output trung gian, tái tạo được |

---

## ⚡ Lệnh Git Thường Dùng

```bash
# Kiểm tra .gitignore hoạt động đúng (APK không xuất hiện)
git status

# Commit model + kết quả sau khi train
git add code/word2vec.model code/deep_learning.model
git add code/*.py
git commit -m "Add trained model - accuracy: XX%"
git push

# Thành viên khác pull về
git pull
```

---

## ⚠️ Lưu Ý Quan Trọng

1. **LUÔN kiểm tra `git status` trước khi commit** — đảm bảo không thấy file `.apk`
2. **Không dùng `git add .` hoặc `git add --all`** nếu chưa chắc .gitignore hoạt động
3. **Nếu lỡ commit file APK** → phải dùng `git filter-branch` hoặc `BFG Repo-Cleaner` để xóa khỏi history (rất phức tạp, nên tránh)
4. **File `deep_learning.model` có thể > 100 MB** → nếu vượt giới hạn GitHub, dùng Git LFS chỉ cho file model này
