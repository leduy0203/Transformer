"""
Cấu hình chung cho ứng dụng
"""

DB_NAME = "sentiment_history.db"

MODEL_NAME = "wonrax/phobert-base-vietnamese-sentiment"

# Từ điển chuẩn hóa tiếng Việt
NORMALIZATION_DICT = {
    "rat": "rất",
    "ko": "không",
    "k": "không",
    "kg": "không",
    "kh": "không",
    "khg": "không",
    "dc": "được",
    "đc": "được",
    "ok": "tốt",
    "oke": "tốt",
    "happy": "vui",
    "sad": "buồn",
    "do": "dở",
    "j": "gì",
    "z": "vậy",
    "tks": "cảm ơn",
    "thank": "cảm ơn",
    "thanks": "cảm ơn",
    "hom": "hôm",
    "nay": "nay",
    "ngay": "ngày",
    "toi": "tôi",
    "ban": "bạn",
    "khong": "không",
    "duoc": "được",
    "tot": "tốt",
    "xau": "xấu",
    "dep": "đẹp",
    "qua": "quá",
    "dang": "đang",
    "den": "đến",
    "roi": "rồi",
    "nua": "nữa",
    "cho": "cho",
    "lam": "làm",
    "ma": "mà",
    "thi": "thì",
}

# Validation
MIN_TEXT_LENGTH = 5
MAX_TEXT_LENGTH = 500
