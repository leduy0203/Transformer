# Trợ lý Phân loại Cảm xúc Tiếng Việt 🤖

Ứng dụng web sử dụng mô hình Transformer (PhoBERT) để phân loại cảm xúc (tích cực, tiêu cực, trung tính) cho câu tiếng Việt. Giao diện trực quan, dễ sử dụng, lưu lại lịch sử phân tích.

## Tính năng chính
- Nhập câu tiếng Việt, nhận kết quả phân loại cảm xúc (POSITIVE, NEGATIVE, NEUTRAL)
- Tiền xử lý, chuẩn hóa từ viết tắt
- Lưu và hiển thị lịch sử phân loại (50 dòng gần nhất)
- Giao diện web với Streamlit

## Cài đặt
1. Cài Python 3.8 trở lên
2. Cài các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```


## 🚀 Hướng dẫn chạy ứng dụng

**Bước 1:** Mở terminal/cmd và chuyển đến thư mục dự án.

**Bước 2:** Chạy lệnh sau để khởi động ứng dụng web:

```bash
streamlit run app.py
```

**Bước 3:**
- Sau khi chạy lệnh, terminal sẽ hiển thị một đường link (thường là http://localhost:8501).
- Nhấn vào link đó hoặc copy vào trình duyệt để sử dụng giao diện phân loại cảm xúc.

> **Lưu ý:** Nếu chưa cài thư viện, hãy chạy `pip install -r requirements.txt` trước khi chạy ứng dụng.

## Ghi chú
- Mô hình sử dụng: `wonrax/phobert-base-vietnamese-sentiment` (có thể đổi sang model khác nếu muốn)
- Lịch sử lưu trong file SQLite `sentiment_history.db` (tự động tạo khi chạy lần đầu)

---
Đồ án môn học: Xây dựng trợ lý phân loại cảm xúc sử dụng Transformer.
