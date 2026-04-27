# 🚀 Hướng Dẫn Chi Tiết Huấn Luyện MalDozer với Dataset 11,000 APK

> **Dataset:** 11,000 mẫu APK (5,500 goodware + 5,500 malware)
> **Phân loại:** Binary Classification (2 class)

---

## 📋 Mục Lục

1. [Tổng quan Pipeline](#1-tổng-quan-pipeline)
2. [Yêu cầu hệ thống & Cài đặt thư viện](#2-yêu-cầu-hệ-thống--cài-đặt-thư-viện)
3. [Chuẩn bị Dataset](#3-chuẩn-bị-dataset)
4. [Cấu hình set_constant.py](#4-cấu-hình-set_constantpy)
5. [Step 1: Trích xuất API calls](#5-step-1-trích-xuất-api-calls)
6. [Step 2: Ánh xạ API → Identifier](#6-step-2-ánh-xạ-api--identifier)
7. [Step 3: Huấn luyện Word2Vec](#7-step-3-huấn-luyện-word2vec)
8. [Step 4: Huấn luyện CNN](#8-step-4-huấn-luyện-cnn)
9. [Đánh giá Model](#9-đánh-giá-model)
10. [Tham số tối ưu cho 11K dataset](#10-tham-số-tối-ưu-cho-11k-dataset)
11. [Xử lý lỗi thường gặp](#11-xử-lý-lỗi-thường-gặp)
12. [Chạy toàn bộ Pipeline tự động](#12-chạy-toàn-bộ-pipeline-tự-động)

---

## 1. Tổng Quan Pipeline

MalDozer xử lý qua **4 bước tuần tự**:

```
APK Files ──► API Sequences ──► Integer Identifiers ──► Word2Vec Embeddings ──► CNN Classification
  (Step 1)       (Step 2)            (Step 3)                (Step 4)
```

**Chi tiết luồng dữ liệu:**

| Bước | Script | Input | Output | Thời gian ước tính (11K) |
|------|--------|-------|--------|--------------------------|
| 1 | `one_get_api.py` | 11,000 APK files | 11,000 file `.feature` | **8-24 giờ** |
| 2 | `two_mapping_to_identifier.py` | `.feature` + `method_dict.pickle` | File identifier (train/test) | **10-30 phút** |
| 3 | `three_word2vec.py` | Tất cả file identifier | `word2vec.model` | **5-15 phút** |
| 4 | `four_deep_learning.py` | File identifier + `word2vec.model` | `deep_learning.model` | **1-4 giờ** |

> ⚠️ **Lưu ý:** Step 1 là bước tốn thời gian nhất vì phải decompile từng APK bằng Androguard.

---

## 2. Yêu Cầu Hệ Thống & Cài Đặt Thư Viện

### 2.1. Yêu cầu phần cứng

| Thành phần | Tối thiểu | Khuyến nghị |
|------------|-----------|-------------|
| RAM | 8 GB | 16 GB+ |
| Ổ cứng | 50 GB trống | 100 GB+ SSD |
| GPU | Không bắt buộc | NVIDIA GPU (CUDA) |
| CPU | 4 cores | 8+ cores |

### 2.2. Cài đặt thư viện

```bash
# Tạo virtual environment (khuyến nghị)
python -m venv .venv

# Kích hoạt (Windows)
.venv\Scripts\activate

# Cài đặt thư viện cần thiết
pip install androguard gensim tensorflow scikit-learn matplotlib numpy
```

**Phiên bản tương thích:**

| Thư viện | Phiên bản khuyến nghị | Ghi chú |
|----------|----------------------|---------|
| Python | 3.8 - 3.10 | TF2 hỗ trợ tốt nhất |
| TensorFlow | 2.10+ | Dùng `tensorflow-gpu` nếu có GPU |
| Gensim | 4.x | Tham số `size` → `vector_size` |
| Androguard | 3.3.5+ | Dùng để decompile APK |

### 2.3. Sửa code tương thích thư viện mới

Code gốc dùng Keras standalone và API cũ. Cần sửa **4 điểm chính**:

**a) Import Keras từ TensorFlow (tất cả file dùng keras):**
```python
# CŨ:
from keras.xxx import yyy

# MỚI:
from tensorflow.keras.xxx import yyy
```

**Các file cần sửa:** `four_deep_learning.py`, `my_generator.py`, `test.py`, `confuse.py`

**b) Word2Vec parameter (file `three_word2vec.py`):**
```python
# CŨ (gensim 3.x):
model = word2vec.Word2Vec(sentences, size=_size, ...)

# MỚI (gensim 4.x):
model = word2vec.Word2Vec(sentences, vector_size=_size, ...)
```

**c) fit_generator → fit (file `four_deep_learning.py`):**
```python
# CŨ:
model.fit_generator(generator, ...)

# MỚI:
model.fit(generator, ...)
```

**d) predict_classes → argmax (file `confuse.py`):**
```python
# CŨ:
y_pred = model.predict_classes(x_test)

# MỚI:
y_pred = np.argmax(model.predict(x_test), axis=1)
```

**e) RMSprop lr → learning_rate (file `four_deep_learning.py`):**
```python
# CŨ:
RMSprop(lr=1e-4)

# MỚI:
RMSprop(learning_rate=1e-4)
```

---

## 3. Chuẩn Bị Dataset

### 3.1. Cấu trúc thư mục cần tạo

Từ thư mục `Maldozer/` (nơi chứa code), tạo cấu trúc sau:

```
../data/
├── apk/                      ← THƯ MỤC GỐC CHỨA APK
│   ├── goodware/             ← 5,500 file APK lành tính
│   │   ├── app001.apk
│   │   ├── app002.apk
│   │   └── ... (5,500 files)
│   └── malware/              ← 5,500 file APK mã độc
│       ├── mal001.apk
│       ├── mal002.apk
│       └── ... (5,500 files)
│
├── apis/                     ← TỰ ĐỘNG TẠO bởi Step 1
│   ├── goodware/             ← Chứa .feature files
│   └── malware/
│
└── identifiers/              ← TỰ ĐỘNG TẠO bởi Step 2
    ├── train/
    │   ├── goodware/
    │   └── malware/
    └── test/
        ├── goodware/
        └── malware/
```

### 3.2. Đặt APK vào đúng vị trí

```bash
# Tạo thư mục (từ thư mục Maldozer/)
mkdir -p ../data/apk/goodware
mkdir -p ../data/apk/malware

# Copy APK vào (ví dụ)
cp /path/to/goodware/*.apk ../data/apk/goodware/
cp /path/to/malware/*.apk ../data/apk/malware/
```

### 3.3. Kiểm tra dataset

```bash
# Đếm số file
ls ../data/apk/goodware/ | wc -l   # Kỳ vọng: 5500
ls ../data/apk/malware/ | wc -l    # Kỳ vọng: 5500
```

Trên Windows PowerShell:
```powershell
(Get-ChildItem ..\data\apk\goodware\).Count   # Kỳ vọng: 5500
(Get-ChildItem ..\data\apk\malware\).Count     # Kỳ vọng: 5500
```

> ⚠️ **Quan trọng:** File APK có thể có hoặc không có đuôi `.apk` — cả hai đều được hỗ trợ (xem `extract_feature.py` line 34-35, nó lọc cả file không có extension và file `.apk`).

---

## 4. Cấu Hình `set_constant.py`

Đây là file **quan trọng nhất** — mọi tham số đều cấu hình ở đây.

### 4.1. Cấu hình đường dẫn và phân loại

Sửa phần đầu file `set_constant.py`:

```python
########## choose path ##########
apk_path = '../data/apk'      # ← Đường dẫn tương đối đến thư mục APK
TYPE = 2                       # ← 2 class: goodware + malware
TYPE_list = ["goodware", "malware"]  # ← Tên class, PHẢI KHỚP tên thư mục con

apis_path = '../data/apis'
identifiers_path = '../data/identifiers'
train_path = "../data/identifiers/train"
test_path = "../data/identifiers/test"
useful_api_class = "../../useful_api_class"
classes = "../../classes"
mapping_to_identifier_path = './method_dict.pickle'  # ← Đã có sẵn trong repo
word2vec_model_path = './word2vec.model'
save_model_path = './deep_learning.model'
type_map = {TYPE_list[i]: i for i in range(TYPE)}
########## choose path ##########
```

> ⚠️ **Lưu ý:** `mapping_to_identifier_path` trỏ đến file `method_dict.pickle` đã có sẵn trong repo (4.3 MB). File này chứa dictionary ánh xạ API name → integer ID. **KHÔNG cần chạy `find.py`** nếu đã có file này.

### 4.2. Cấu hình tham số cho dataset 11,000

```python
########## word2vec ##########
K = 64       # Chiều embedding Word2Vec — giữ nguyên (theo paper)
L = 2500     # Chiều dài chuỗi API tối đa — giữ nguyên hoặc giảm xuống 2000
########## word2vec ##########

########## CNN ##########
maxpooling_size = (14, 14)
batch_size = 32              # ← TĂNG lên 32 (dataset lớn, tăng tốc training)
filter_count = 512           # Giữ nguyên theo paper
kernel_size_ = 3             # Giữ nguyên theo paper
first_neuron_count = 256     # Giữ nguyên theo paper
dropout = 0.5                # Giữ nguyên theo paper
epochs_ = 15                 # Có thể tăng lên 20-30 nếu chưa hội tụ
val_split = 0.2              # 20% validation
test_split = 0.1             # 10% test
KFCV = True                  # Bật K-Fold Cross Validation
KFCV_K = 5                   # 5-fold
########## CNN ##########
```

### 4.3. Giải thích phân chia dữ liệu

Với 11,000 mẫu và cấu hình trên:

| Tập | Tỉ lệ | Số lượng | Mục đích |
|-----|--------|----------|----------|
| **Test** | 10% | ~1,100 | Đánh giá cuối cùng |
| **Train+Val** | 90% | ~9,900 | Huấn luyện + xác thực |

Khi `KFCV = True` (5-fold), trong 9,900 mẫu train:
- Mỗi fold: ~7,920 train + ~1,980 validation

---

## 5. Step 1: Trích Xuất API Calls

### 5.1. Script: `one_get_api.py` → gọi `extract_feature.py`

### 5.2. Cách hoạt động chi tiết

```
APK file
  └─► androguard.AnalyzeAPK() — Decompile APK, phân tích DEX bytecode
       └─► Duyệt tất cả class trong DEX
            └─► Duyệt tất cả method trong class
                 └─► Lấy cross-reference calls (xref_to)
                      └─► Ghi "ClassName:MethodName" vào file .feature
```

**Ví dụ nội dung file `.feature`:**
```
Landroid/app/Activity;:onCreate
Landroid/content/Intent;:<init>
Landroid/widget/Toast;:makeText
Ljava/net/URL;:openConnection
Landroid/telephony/SmsManager;:sendTextMessage
```

### 5.3. Chạy Step 1

```bash
cd Maldozer    # Đảm bảo đang ở thư mục chứa code
python one_get_api.py
```

### 5.4. Kiểm tra kết quả

```powershell
(Get-ChildItem ..\data\apis\goodware\).Count   # Kỳ vọng: ~5500
(Get-ChildItem ..\data\apis\malware\).Count     # Kỳ vọng: ~5500
```

> **Thời gian ước tính:** 8-24 giờ cho 11,000 APK (tùy kích thước APK và cấu hình máy).

> 💡 **Mẹo:** Script tự động skip file đã xử lý (kiểm tra `.feature` tồn tại). Nếu bị gián đoạn, chỉ cần chạy lại và nó sẽ tiếp tục từ chỗ dừng.

> ⚠️ **Lưu ý:** Một số APK có thể bị lỗi khi decompile (APK hỏng, bị obfuscate nặng). Chúng sẽ bị skip do khối `try/except` trong `extract_feature.py`. Số file `.feature` output có thể ít hơn 11,000.

---

## 6. Step 2: Ánh Xạ API → Identifier

### 6.1. Script: `two_mapping_to_identifier.py` (single-process) hoặc `two.py` (multi-process)

### 6.2. Cách hoạt động chi tiết

```
File .feature (text API names)
  └─► Đọc method_dict.pickle (API name → integer ID)
       └─► Với mỗi API call trong .feature:
            ├─► Nếu có trong dict → ghi integer ID
            └─► Nếu không có     → ghi "0" (unknown)
                 └─► Cắt/padding đến chiều dài L = 2500
                      └─► Chia ngẫu nhiên: 80% train, 20% test
```

**Ví dụ chuyển đổi:**
```
# Input (.feature):                    # Output (identifier):
Landroid/app/Activity;:onCreate    →   1523
Landroid/content/Intent;:<init>    →   892
Lcom/unknown/CustomLib;:doStuff   →   0       ← Không có trong dict
Landroid/widget/Toast;:makeText   →   2104
```

### 6.3. Chạy Step 2

**Cách 1 — Single-process (đơn giản, chậm hơn):**
```bash
python two_mapping_to_identifier.py
```

**Cách 2 — Multi-process (nhanh hơn, khuyến nghị cho 11K):**
```bash
python two.py
```

> `two.py` sử dụng 20 process song song, nhanh hơn đáng kể với dataset lớn.

### 6.4. Kiểm tra kết quả

```powershell
# Train set
(Get-ChildItem ..\data\identifiers\train\goodware\).Count
(Get-ChildItem ..\data\identifiers\train\malware\).Count

# Test set
(Get-ChildItem ..\data\identifiers\test\goodware\).Count
(Get-ChildItem ..\data\identifiers\test\malware\).Count
```

Kỳ vọng tổng train + test ≈ tổng số file `.feature` từ Step 1.

---

## 7. Step 3: Huấn Luyện Word2Vec

### 7.1. Script: `three_word2vec.py`

### 7.2. Cách hoạt động chi tiết

```
Tất cả file identifier (train + test)
  └─► Mỗi file = 1 "câu" (sentence), mỗi dòng = 1 "từ" (word)
       └─► Gom thành corpus (danh sách các câu)
            └─► Huấn luyện Word2Vec model
                 └─► Mỗi integer ID → vector 64 chiều
```

**Tham số Word2Vec:**

| Tham số | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `vector_size` | 64 (= K) | Chiều vector embedding |
| `window` | 4 | Context window size |
| `min_count` | 1 | Giữ tất cả từ (kể cả xuất hiện 1 lần) |
| `hs` | 1 | Dùng Hierarchical Softmax |
| `sg` | 0 (default) | Dùng CBOW algorithm |

### 7.3. Chạy Step 3

```bash
python three_word2vec.py
```

### 7.4. Kiểm tra kết quả

File `word2vec.model` được tạo trong thư mục code hiện tại. Kiểm tra:

```python
from gensim.models import Word2Vec
model = Word2Vec.load('./word2vec.model')
print(f"Vocabulary size: {len(model.wv)}")
print(f"Vector dimension: {model.wv.vector_size}")  # Kỳ vọng: 64
# Thử tra cứu 1 identifier
print(model.wv['1523'])  # Vector 64 chiều
```

---

## 8. Step 4: Huấn Luyện CNN

### 8.1. Script: `four_deep_learning.py`

### 8.2. Kiến trúc CNN

```
Input (2500 × 64 × 1)
  │
  ▼
Conv2D(filters=512, kernel=3×3, activation='relu')
  │
  ▼
MaxPooling2D(14 × 14)
  │
  ▼
Flatten
  │
  ▼
Dense(256, activation='relu')
  │
  ▼
Dropout(0.5)
  │
  ▼
Dense(2, activation='softmax')    ← 2 class output
  │
  ▼
Output: [P(goodware), P(malware)]
```

### 8.3. Luồng dữ liệu chi tiết trong Step 4

```
1. Load tất cả file identifier (train + test)
2. Mỗi file → tra Word2Vec → matrix (2500 × 64)
3. Reshape thành (2500, 64, 1) → chuẩn hóa /255
4. Label → one-hot encoding: goodware=[1,0], malware=[0,1]
5. Gộp train + test → shuffle cùng seed → chia lại:
   ├── 10% → Test set (~1,100 mẫu)
   └── 90% → Train set (~9,900 mẫu)
        └── 5-Fold CV:
             ├── Fold 1: 80% train + 20% val
             ├── Fold 2: 80% train + 20% val
             ├── ...
             └── Fold 5: 80% train + 20% val
6. Train CNN qua 15 epochs mỗi fold
7. Evaluate trên test set
8. Vẽ biểu đồ accuracy/loss
```

### 8.4. Chạy Step 4

```bash
python four_deep_learning.py
```

### 8.5. Output

- **Model:** `deep_learning.model` (hoặc `../deep_learning.model` tùy config)
- **Biểu đồ:** Matplotlib hiển thị Training/Validation accuracy & loss
- **Console:** In testing accuracy

---

## 9. Đánh Giá Model

### 9.1. Chạy đánh giá

```bash
python test.py
```

Script này load model đã train, chạy trên test set và in **confusion matrix**:

```
pred\real    real goodware    real malware
pred goodware   TP_good         FN
pred malware    FP              TP_mal
acc: 0.95xx
```

### 9.2. Metrics quan trọng

| Metric | Công thức | Ý nghĩa |
|--------|-----------|---------|
| Accuracy | (TP + TN) / Total | Tỉ lệ dự đoán đúng tổng thể |
| Precision | TP / (TP + FP) | Trong các mẫu dự đoán malware, bao nhiêu đúng |
| Recall | TP / (TP + FN) | Trong các malware thật, bao nhiêu được phát hiện |
| F1-Score | 2 × P × R / (P+R) | Trung bình điều hòa Precision & Recall |

---

## 10. Tham Số Tối Ưu Cho 11K Dataset

### 10.1. Cấu hình khuyến nghị

```python
# set_constant.py — Tối ưu cho 11,000 APK (50/50)
K = 64
L = 2500
batch_size = 32          # Lớn hơn default (10) → train nhanh hơn
filter_count = 512
kernel_size_ = 3
first_neuron_count = 256
dropout = 0.5
epochs_ = 15             # Có thể tăng 20-30 nếu cần
val_split = 0.2
test_split = 0.1
KFCV = True
KFCV_K = 5
```

### 10.2. Nếu gặp vấn đề

| Vấn đề | Triệu chứng | Giải pháp |
|--------|-------------|-----------|
| **Overfitting** | Train acc cao, val acc thấp | Tăng `dropout=0.7`, giảm `filter_count=256` |
| **Underfitting** | Cả train & val acc thấp | Tăng `epochs_=30`, giảm `dropout=0.3` |
| **Hết RAM** | MemoryError | Giảm `L=1500`, giảm `batch_size=16` |
| **Train quá chậm** | >1h/epoch | Dùng GPU, tăng `batch_size=64` |

---

## 11. Xử Lý Lỗi Thường Gặp

### 11.1. `ModuleNotFoundError: No module named 'keras'`
```bash
# Sửa import trong code:
# from keras.xxx → from tensorflow.keras.xxx
```

### 11.2. `TypeError: __init__() got an unexpected keyword argument 'size'`
```python
# Gensim 4.x đổi tham số:
# size → vector_size (trong three_word2vec.py)
```

### 11.3. `AttributeError: 'Sequential' object has no attribute 'predict_classes'`
```python
# Thay trong confuse.py:
# y_pred = model.predict_classes(x_test)
# → y_pred = np.argmax(model.predict(x_test), axis=1)
```

### 11.4. `MemoryError` khi load tất cả data
```python
# Giảm L trong set_constant.py:
L = 1500   # hoặc 1000

# Hoặc giảm K:
K = 32
```

### 11.5. `validation_split_` not defined (trong `two_mapping_to_identifier.py`)
```python
# File import `validation_split_` nhưng set_constant.py đặt tên `val_split`
# Sửa trong two_mapping_to_identifier.py line 6:
# from set_constant import L,apis_path,train_path,test_path,validation_split_
# → from set_constant import L,apis_path,train_path,test_path,val_split as validation_split_
```

---

## 12. Chạy Toàn Bộ Pipeline Tự Động

### 12.1. Dùng `main.py`

```bash
python main.py
```

Script này chạy tuần tự 4 bước và ghi thời gian mỗi bước vào file `21.txt`:
```
Step 1 time (seconds)
Dictionary load time
Step 2 time
Step 3 time
Step 4 time
```

### 12.2. Hoặc chạy từng bước thủ công

```bash
# Step 1: Trích xuất API (LÂU NHẤT — 8-24 giờ)
python one_get_api.py

# Step 2: Ánh xạ API → Identifier (10-30 phút)
python two.py
# hoặc: python two_mapping_to_identifier.py

# Step 3: Huấn luyện Word2Vec (5-15 phút)
python three_word2vec.py

# Step 4: Huấn luyện CNN (1-4 giờ)
python four_deep_learning.py

# Đánh giá
python test.py
```

> 💡 **Khuyến nghị chạy từng bước** thay vì `main.py` để có thể kiểm tra output mỗi bước và xử lý lỗi kịp thời.

---

## 📊 Tóm Tắt Nhanh

```
┌─────────────────────────────────────────────────────────┐
│  DATASET: 11,000 APK (5,500 goodware + 5,500 malware)  │
├─────────────────────────────────────────────────────────┤
│  1. Đặt APK vào ../data/apk/goodware/ và malware/      │
│  2. Sửa set_constant.py (apk_path, TYPE=2, batch=32)   │
│  3. Chạy: python one_get_api.py        [8-24h]         │
│  4. Chạy: python two.py               [10-30min]       │
│  5. Chạy: python three_word2vec.py     [5-15min]        │
│  6. Chạy: python four_deep_learning.py [1-4h]           │
│  7. Chạy: python test.py              [đánh giá]        │
│                                                         │
│  Output: deep_learning.model + accuracy/loss charts     │
│  Kỳ vọng accuracy: 95-98% (binary classification)      │
└─────────────────────────────────────────────────────────┘
```
