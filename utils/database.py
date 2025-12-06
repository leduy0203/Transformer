"""
Component 1: Quản lý Database (Lưu trữ & Hiển thị lịch sử)
"""

import sqlite3
import pandas as pd
from datetime import datetime
from .config import DB_NAME


def init_db():
    """
    Khởi tạo database và bảng nếu chưa tồn tại.

    Bảng sentiments gồm:
    - id: Primary key tự tăng
    - text: Câu nhập vào
    - sentiment: Nhãn cảm xúc (POS/NEG/NEU)
    - timestamp: Thời gian phân loại
    """
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
    """
    Lưu kết quả phân loại vào database.

    Args:
        text (str): Câu nhập vào
        sentiment (str): Nhãn cảm xúc (POS/NEG/NEU)
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute(
        "INSERT INTO sentiments (text, sentiment, timestamp) VALUES (?, ?, ?)",
        (text, sentiment, timestamp),
    )
    conn.commit()
    conn.close()


def load_history(limit=50):
    """
    Lấy lịch sử phân loại từ database.

    Args:
        limit (int): Số dòng tối đa trả về

    Returns:
        pd.DataFrame: DataFrame chứa lịch sử
    """
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(
        "SELECT text, sentiment, timestamp FROM sentiments ORDER BY timestamp DESC LIMIT ?",
        conn,
        params=(limit,),
    )
    conn.close()
    return df
