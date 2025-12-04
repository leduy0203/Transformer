# Trợ lý Phân loại Cảm xúc Tiếng Việt 🤖

Ứng dụng web sử dụng mô hình Transformer (PhoBERT) để phân loại cảm xúc (tích cực, tiêu cực, trung tính) cho câu tiếng Việt. Giao diện trực quan, dễ sử dụng, lưu lại lịch sử phân tích.

## Tính năng chính
- Nhập câu tiếng Việt, nhận kết quả phân loại cảm xúc (POSITIVE, NEGATIVE, NEUTRAL)
- Tiền xử lý, chuẩn hóa từ viết tắt
- Lưu và hiển thị lịch sử phân loại (50 dòng gần nhất)
- Giao diện web với Streamlit

## 📋 Yêu cầu hệ thống
- Python 3.8 trở lên
- Kết nối internet (để tải model lần đầu tiên)
- Khoảng 2GB dung lượng trống (cho model và dependencies)

## 🚀 Hướng dẫn cài đặt và chạy

### Bước 1: Cài đặt thư viện

Mở terminal/cmd tại thư mục dự án và chạy:

```bash
pip install -r requirements.txt
```

Quá trình cài đặt có thể mất 5-10 phút tùy theo tốc độ mạng.

### Bước 2: Chạy ứng dụng

```bash
streamlit run app.py
```

Hoặc nếu lệnh trên không hoạt động:

```bash
python -m streamlit run app.py
```

Sau khi chạy lệnh, terminal sẽ hiển thị:
```
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

Mở trình duyệt và truy cập địa chỉ `http://localhost:8501`.

### Bước 4: Sử dụng ứng dụng

1. Nhập câu tiếng Việt vào ô input (ví dụ: "Hôm nay tôi rất vui")
2. Nhấn nút **"Phân tích"**
3. Xem kết quả:
   - **Nhãn cảm xúc:** POSITIVE/NEGATIVE/NEUTRAL
   - **Độ tin cậy:** Xác suất dự đoán (%)
   - **Text đã chuẩn hóa:** Câu sau khi tiền xử lý
4. Kiểm tra **lịch sử phân loại** ở phía dưới

## ⚙️ Cấu trúc dự án

```
tranformer/
├── app.py                      # File chính - Giao diện Streamlit
├── utils/                      # Package chứa các module
│   ├── __init__.py            # Package exports
│   ├── config.py              # Cấu hình (model, dictionary, constants)
│   ├── database.py            # Quản lý SQLite (lưu trữ & hiển thị)
│   └── nlp_processor.py       # Tiền xử lý & phân loại cảm xúc
├── requirements.txt            # Danh sách thư viện cần thiết
├── README.md                  # Tài liệu này
├── .gitignore                 # Git ignore file
└── sentiment_history.db       # Database SQLite (tự động tạo khi chạy)
```

## 🔧 Xử lý lỗi thường gặp

### Lỗi: `streamlit: command not found`
**Nguyên nhân:** Chưa cài Streamlit hoặc chưa thêm vào PATH.

**Giải pháp:**
```bash
# Cài Streamlit
pip install streamlit

# Hoặc chạy bằng Python module
python -m streamlit run app.py
```

### Lỗi: `No module named 'transformers'`
**Giải pháp:**
```bash
pip install transformers torch
```

### Lỗi: Không tải được model từ Hugging Face
**Nguyên nhân:** Không có kết nối internet hoặc Hugging Face bị chặn.

**Giải pháp:**
- Kiểm tra kết nối internet
- Thử chạy lại ứng dụng (model sẽ tự động retry)
- Nếu vẫn lỗi, có thể thay model khác trong `utils/config.py`

### Lỗi: Port 8501 đã được sử dụng
**Giải pháp:** Chạy ứng dụng trên port khác
```bash
streamlit run app.py --server.port 8502
```

### Lỗi: Execution Policy (Windows)
**Giải pháp:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🛑 Tắt ứng dụng

Nhấn `Ctrl + C` trong terminal để dừng server Streamlit.

## 📝 Lưu ý khi chạy lần đầu

- **Model PhoBERT** sẽ được tải tự động từ Hugging Face (~500MB)
- Quá trình tải có thể mất **2-5 phút** tùy tốc độ mạng
- Model sẽ được **cache lại**, các lần chạy sau sẽ nhanh hơn
- Database `sentiment_history.db` sẽ tự động tạo khi bạn phân tích câu đầu tiên

## Ghi chú
- Mô hình sử dụng: `wonrax/phobert-base-vietnamese-sentiment` (có thể đổi sang model khác nếu muốn)
- Lịch sử lưu trong file SQLite `sentiment_history.db` (tự động tạo khi chạy lần đầu)

---
Đồ án môn học: Xây dựng trợ lý phân loại cảm xúc sử dụng Transformer.
