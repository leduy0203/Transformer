"""
Ứng dụng Trợ lý Phân loại Cảm xúc Tiếng Việt
Sử dụng Transformer (PhoBERT) để phân tích cảm xúc câu tiếng Việt
"""

import streamlit as st
from utils import (
    init_db,
    save_to_db,
    load_history,
    preprocess_text,
    load_model,
    analyze_sentiment,
)
from utils.config import MIN_TEXT_LENGTH

st.set_page_config(page_title="Trợ lý Phân loại Cảm xúc", layout="centered")


def main():
    init_db()

    st.title("Trợ lý Phân loại Cảm xúc Tiếng Việt")
    st.markdown("---")

    # Load model PhoBERT 
    with st.spinner("Đang tải mô hình AI..."):
        try:
            classifier = load_model()
        except Exception as e:
            st.error(f"Lỗi tải mô hình: {e}")
            return

    col1, col2 = st.columns([3, 1])
    with col1:
        user_input = st.text_input(
            "Nhập câu tiếng Việt của bạn:", placeholder="Ví dụ: Hôm nay tôi rất vui"
        )

    with col2:
        st.write("")
        st.write("")
        analyze_btn = st.button("Phân tích", type="primary")

    if analyze_btn:
        # Validation: Kiểm tra độ dài input
        if not user_input or len(user_input.strip()) < MIN_TEXT_LENGTH:
            st.warning(
                f"Câu quá ngắn hoặc rỗng! Vui lòng nhập ít nhất {MIN_TEXT_LENGTH} ký tự."
            )
        else:
            # Bước 1: Tiền xử lý (chuẩn hóa từ viết tắt, thiếu dấu)
            processed_text = preprocess_text(user_input)

            # Bước 2: Gọi model Transformer để phân loại cảm xúc
            result = analyze_sentiment(processed_text, classifier)

            raw_label = result["label"]
            score = result["score"]
            human_label = result["human_label"]

            st.success("Đã phân tích xong!")

            # Hiển thị kết quả phân loại
            m1, m2 = st.columns(2)
            m1.metric("Nhãn cảm xúc", human_label.split(" ")[0])
            m2.metric("Độ tin cậy", f"{score:.2%}")

            st.info(f"**Text đã chuẩn hóa:** {processed_text}")

            if "POS" in raw_label:
                st.balloons()
                st.success(f"**Kết luận:** {human_label}")
            elif "NEG" in raw_label:
                st.error(f"**Kết luận:** {human_label}")
            else:
                st.warning(f"**Kết luận:** {human_label}")

            # Lưu kết quả vào database 
            save_to_db(user_input, raw_label)

    st.markdown("---")

    # Hiển thị lịch sử phân loại từ database
    st.subheader("Lịch sử phân loại (50 tin mới nhất)")

    try:
        history_df = load_history()
        if not history_df.empty:
            st.dataframe(
                history_df,
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

    st.markdown("---")
    st.caption("Đồ án môn học: Xây dựng trợ lý phân loại cảm xúc sử dụng Transformer.")


if __name__ == "__main__":
    main()
