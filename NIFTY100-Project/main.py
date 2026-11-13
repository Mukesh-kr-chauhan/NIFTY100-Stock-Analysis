
import yfinance as yf
import pandas as pd

from src.database import create_database, save_stock_data
from src.audit import initialize_audit, log_audit

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "ITC.NS",
    "LT.NS",
    "BHARTIARTL.NS",
    "AXISBANK.NS"
]


def collect_stock_data():

    all_data = []

    for symbol in stocks:

        print(f"Downloading {symbol}...")

        try:
            df = yf.download(
                symbol,
                period="1y",
                interval="1d",
                auto_adjust=True,
                progress=False
            )

            if df.empty:
                log_audit(
                    symbol,
                    0,
                    "FAILED",
                    "No data received"
                )
                continue

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            df = df.reset_index()
            df["Symbol"] = symbol

            all_data.append(df)

            log_audit(
                symbol,
                len(df),
                "SUCCESS"
            )

        except Exception as e:

            log_audit(
                symbol,
                0,
                "FAILED",
                str(e)
            )

            print(f"Error downloading {symbol}: {e}")

    if all_data:

        final_data = pd.concat(
            all_data,
            ignore_index=True
        )

        save_stock_data(final_data)

        print("\nStock data collection completed!")
        print("Total records:", len(final_data))

    else:
        print("No stock data collected.")


if __name__ == "__main__":

    initialize_audit()
    create_database()
    collect_stock_data()
