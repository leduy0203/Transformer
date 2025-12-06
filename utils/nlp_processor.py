"""
Component 2: Xử lý NLP (Preprocessing & Sentiment Analysis)
"""

import streamlit as st
from transformers import pipeline
from .config import MODEL_NAME, NORMALIZATION_DICT


def preprocess_text(text):
    """
    Chuẩn hóa câu tiếng Việt trước khi phân loại.

    Args:
        text (str): Câu nhập vào

    Returns:
        str: Câu đã được chuẩn hóa
    """
    if not text:
        return ""

    text = text.lower().strip()
    words = text.split()
    corrected_words = [NORMALIZATION_DICT.get(word, word) for word in words]
    text = " ".join(corrected_words)

    return text


@st.cache_resource
def load_model():
    """
    Load model Transformer pre-trained cho sentiment analysis.

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
        dict: Kết quả phân loại với label, score, human_label
    """
    result = classifier(text)[0]

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
