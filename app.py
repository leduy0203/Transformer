import streamlit as st
from transformers import pipeline
import sqlite3
import pandas as pd
from datetime import datetime
import os

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Trợ lý Phân loại Cảm xúc", page_icon="🤖", layout="centered"
)

# --- 1. DATABASE HANDLE (Lưu trữ & Hiển thị) ---
DB_NAME = "sentiment_history.db"


def init_db():
    """Khởi tạo database và bảng nếu chưa tồn tại"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS sentiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            sentiment TEXT,
            timestamp TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def save_to_db(text, sentiment):
    """Lưu kết quả vào DB (Chống SQL Injection bằng tham số hóa)"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Sử dụng ? để tránh SQL Injection như yêu cầu trong hình 4
    c.execute(
        "INSERT INTO sentiments (text, sentiment, timestamp) VALUES (?, ?, ?)",
        (text, sentiment, timestamp),
    )
    conn.commit()
    conn.close()


def load_history():
    """Lấy 50 dòng lịch sử mới nhất"""
    conn = sqlite3.connect(DB_NAME)
    # Giới hạn 50 dòng để không làm chậm giao diện (Yêu cầu hình 4)
    df = pd.read_sql_query(
        "SELECT text, sentiment, timestamp FROM sentiments ORDER BY timestamp DESC LIMIT 50",
        conn,
    )
    conn.close()
    return df


# --- 2. XỬ LÝ NLP (Preprocessing & Model) ---

# Dictionary chuẩn hóa từ viết tắt (Yêu cầu hình 1)
NORMALIZATION_DICT = {
    "rat": "rất",
    "ko": "không",
    "dc": "được",
    "ok": "tốt",
    "happy": "vui",
    "sad": "buồn",
    "do": "dở",
}


def preprocess_text(text):
    """
    Chuẩn hóa câu tiếng Việt:
    - Chuyển về chữ thường
    - Thay thế từ viết tắt
    """
    if not text:
        return ""

    text = text.lower().strip()

    # Thay thế từ điển
    words = text.split()
    corrected_words = [NORMALIZATION_DICT.get(word, word) for word in words]
    text = " ".join(corrected_words)

    return text


@st.cache_resource
def load_model():
    """
    Load model Transformer. Sử dụng @st.cache_resource để chỉ load 1 lần.
    Lựa chọn model: 'wonrax/phobert-base-vietnamese-sentiment'
    Lý do: Đây là phiên bản fine-tuned của PhoBERT cho tác vụ Sentiment,
    đảm bảo độ chính xác > 65% so với dùng bản base chưa train.
    """
    # Bạn có thể đổi thành 'uitnlp/visobert-sentiment' nếu muốn
    model_name = "wonrax/phobert-base-vietnamese-sentiment"

    # Pipeline phân loại văn bản
    classifier = pipeline("sentiment-analysis", model=model_name, tokenizer=model_name)
    return classifier


# --- 3. GIAO DIỆN NGƯỜI DÙNG (Streamlit) ---


def main():
    init_db()  # Khởi tạo DB khi chạy app

    st.title("Trợ lý Phân loại Cảm xúc Tiếng Việt")
    st.markdown("---")

    # Load model với spinner (Yêu cầu hình 4: hiển thị trạng thái khi load)
    with st.spinner("Đang tải mô hình AI... Vui lòng chờ giây lát..."):
        try:
            classifier = load_model()
        except Exception as e:
            st.error(f"Lỗi tải mô hình: {e}")
            return

    # Khu vực nhập liệu
    col1, col2 = st.columns([3, 1])
    with col1:
        user_input = st.text_input(
            "Nhập câu tiếng Việt của bạn:", placeholder="Ví dụ: Hôm nay tôi rất vui"
        )

    with col2:
        st.write("")  # Spacer
        st.write("")
        analyze_btn = st.button("Phân tích", type="primary", use_container_width=True)

    # Xử lý khi bấm nút
    if analyze_btn:
        # 1. Kiểm tra độ dài (Yêu cầu hình 1: Validation)
        if not user_input or len(user_input.strip()) < 5:
            st.warning("Câu quá ngắn hoặc rỗng! Vui lòng nhập ít nhất 5 ký tự.")
        else:
            # 2. Tiền xử lý
            processed_text = preprocess_text(user_input)

            # 3. Gọi Pipeline
            # Model này trả về: NEG, POS, NEU
            result = classifier(processed_text)[0]
            label_map = {
                "POS": "POSITIVE (Tích cực)",
                "NEG": "NEGATIVE (Tiêu cực)",
                "NEU": "NEUTRAL (Trung tính)",
            }

            raw_label = result["label"]
            score = result["score"]
            human_label = label_map.get(raw_label, "NEUTRAL")

            # 4. Hiển thị kết quả
            st.success("Đã phân tích xong!")

            # Tạo 3 cột để hiển thị metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Nhãn cảm xúc", human_label.split(" ")[0])
            m2.metric("Độ tin cậy", f"{score:.2%}")
            m3.metric("Text đã chuẩn hóa", processed_text)

            # Màu sắc visual dựa trên cảm xúc
            if "POS" in raw_label:
                st.balloons()
                st.info(f"Kết luận: {human_label}")
            elif "NEG" in raw_label:
                st.error(f"Kết luận: {human_label}")
            else:
                st.warning(f"Kết luận: {human_label}")

            # 5. Lưu vào Database
            save_to_db(user_input, raw_label)

    st.markdown("---")

    # --- 4. LỊCH SỬ PHÂN LOẠI (Yêu cầu hình 4) ---
    st.subheader("Lịch sử phân loại (50 tin mới nhất)")

    try:
        history_df = load_history()
        if not history_df.empty:
            # Format lại bảng cho đẹp
            st.dataframe(
                history_df,
                use_container_width=True,
                column_config={
                    "text": "Câu nhập vào",
                    "sentiment": "Cảm xúc",
                    "timestamp": "Thời gian",
                },
            )
        else:
            st.caption("Chưa có dữ liệu lịch sử.")
    except Exception as e:
        st.error("Không thể tải lịch sử.")

    # --- Footer ---
    st.markdown("---")
    st.caption("Đồ án môn học: Xây dựng trợ lý phân loại cảm xúc sử dụng Transformer.")


if __name__ == "__main__":
    main()
