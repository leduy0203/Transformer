"""
Component 2: Xử lý NLP (Preprocessing & Sentiment Analysis)
"""

import streamlit as st
from transformers import pipeline
from .config import MODEL_NAME, NORMALIZATION_DICT


def preprocess_text(text):
    """
    Chuẩn hóa câu tiếng Việt trước khi phân loại.

    Các bước xử lý:
    1. Chuyển về chữ thường
    2. Loại bỏ khoảng trắng thừa
    3. Thay thế từ viết tắt bằng dictionary

    Args:
        text (str): Câu nhập vào

    Returns:
        str: Câu đã được chuẩn hóa

    Example:
        >>> preprocess_text("Hôm nay rat vui")
        "hôm nay rất vui"
    """
    if not text:
        return ""

    # Chuyển chữ thường và loại khoảng trắng
    text = text.lower().strip()

    # Thay thế từ viết tắt bằng dictionary
    words = text.split()
    corrected_words = [NORMALIZATION_DICT.get(word, word) for word in words]
    text = " ".join(corrected_words)

    return text


@st.cache_resource
def load_model():
    """
    Load model Transformer pre-trained cho sentiment analysis.

    Sử dụng @st.cache_resource để chỉ load 1 lần duy nhất,
    tránh reload mỗi khi user tương tác với UI.

    Model: wonrax/phobert-base-vietnamese-sentiment
    - Dựa trên PhoBERT (BERT cho tiếng Việt)
    - Fine-tuned cho tác vụ sentiment analysis
    - Độ chính xác > 65% trên test case tiếng Việt

    Returns:
        pipeline: Hugging Face pipeline cho sentiment-analysis
    """
    classifier = pipeline("sentiment-analysis", model=MODEL_NAME, tokenizer=MODEL_NAME)
    return classifier


def analyze_sentiment(text, classifier):
    """
    Phân loại cảm xúc cho câu đã được tiền xử lý.

    Args:
        text (str): Câu đã được chuẩn hóa
        classifier: Pipeline từ load_model()

    Returns:
        dict: {
            'label': str (POS/NEG/NEU),
            'score': float (độ tin cậy 0-1),
            'human_label': str (nhãn dễ đọc)
        }
    """
    # Gọi pipeline
    result = classifier(text)[0]

    # Map nhãn sang dạng dễ đọc
    label_map = {
        "POS": "POSITIVE (Tích cực)",
        "NEG": "NEGATIVE (Tiêu cực)",
        "NEU": "NEUTRAL (Trung tính)",
    }

    raw_label = result["label"]
    score = result["score"]
    human_label = label_map.get(raw_label, "NEUTRAL (Trung tính)")

    return {
        "label": raw_label,
        "score": score,
        "human_label": human_label,
    }
