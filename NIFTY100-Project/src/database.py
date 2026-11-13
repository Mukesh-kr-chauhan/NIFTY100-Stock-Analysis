
import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join("data", "nifty100.db")


def create_database():
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            date TEXT NOT NULL,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER
        )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully!")


def save_stock_data(data):
    if data.empty:
        print("No stock data available.")
        return

    conn = sqlite3.connect(DB_PATH)

    data = data.rename(columns={
        "Symbol": "symbol",
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })

    required_columns = [
        "symbol", "date", "open",
        "high", "low", "close", "volume"
    ]

    data = data[required_columns]

    data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")

    data.to_sql(
        "stock_prices",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()

    print(f"Saved {len(data)} stock records.")
