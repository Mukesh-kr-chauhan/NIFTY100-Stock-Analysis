
import os
import csv
from datetime import datetime

AUDIT_FILE = "output/load_audit.csv"


def initialize_audit():

    os.makedirs("output", exist_ok=True)

    if not os.path.exists(AUDIT_FILE):

        with open(AUDIT_FILE, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "timestamp",
                "symbol",
                "records_downloaded",
                "status",
                "error_message"
            ])


def log_audit(symbol, records, status, error=""):

    initialize_audit()

    with open(AUDIT_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            datetime.now().isoformat(),
            symbol,
            records,
            status,
            error
        ])

    print(f"Audit saved: {symbol} - {status}")
