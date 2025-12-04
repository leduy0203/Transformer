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

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Trợ lý Phân loại Cảm xúc", page_icon="🤖", layout="centered"
)


# --- GIAO DIỆN NGƯỜI DÙNG (Streamlit) ---


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
        analyze_btn = st.button("Phân tích", type="primary")

    # Xử lý khi bấm nút
    if analyze_btn:
        # 1. Validation: Kiểm tra độ dài
        if not user_input or len(user_input.strip()) < MIN_TEXT_LENGTH:
            st.warning(
                f"Câu quá ngắn hoặc rỗng! Vui lòng nhập ít nhất {MIN_TEXT_LENGTH} ký tự."
            )
        else:
            # 2. Tiền xử lý (Component 1: Preprocessing)
            processed_text = preprocess_text(user_input)

            # 3. Phân loại cảm xúc (Component 2: Sentiment Analysis)
            result = analyze_sentiment(processed_text, classifier)

            raw_label = result["label"]
            score = result["score"]
            human_label = result["human_label"]

            # 4. Hiển thị kết quả (Component 3: Validation & Output)
            st.success("✅ Đã phân tích xong!")

            # Tạo 2 cột để hiển thị metrics chính
            m1, m2 = st.columns(2)
            m1.metric("Nhãn cảm xúc", human_label.split(" ")[0])
            m2.metric("Độ tin cậy", f"{score:.2%}")

            # Hiển thị text đã chuẩn hóa dạng info box
            st.info(f"📝 **Text đã chuẩn hóa:** {processed_text}")

            # Màu sắc visual dựa trên cảm xúc
            if "POS" in raw_label:
                st.balloons()
                st.success(f"🎉 **Kết luận:** {human_label}")
            elif "NEG" in raw_label:
                st.error(f"😔 **Kết luận:** {human_label}")
            else:
                st.warning(f"😐 **Kết luận:** {human_label}")

            # 5. Lưu vào Database (Component 4: Storage Engine)
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
