from datetime import datetime, date
from zoneinfo import ZoneInfo
import requests
import os
import sys

# secret GitHub
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TARGET_DATE = date(2026, 7, 4)
MOSCOW_TZ = ZoneInfo("Europe/Moscow")

def days_left():
    today = datetime.now(MOSCOW_TZ).date()
    return (TARGET_DATE - today).days

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })
    response.raise_for_status()

def main():
    d = days_left()

    if d <= 0:
        send_message("МАКС ВЕРНУЛСЯ")
        # флаг завершения
        with open("DONE", "w") as f:
            f.write("finished")
        sys.exit(0)
    else:
        send_message(f"дней до возвращения макса: {d}")

if __name__ == "__main__":
    main()
