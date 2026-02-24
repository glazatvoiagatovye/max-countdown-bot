from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import calendar
import requests
import os
import sys

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

MOSCOW_TZ = ZoneInfo("Europe/Moscow")
TARGET_DATE = datetime(2026, 7, 4, 1, 0, 0, tzinfo=MOSCOW_TZ)

def pluralize(n, forms):
    """Возвращает слово с правильным окончанием для русского языка"""
    n = abs(n)
    if n % 10 == 1 and n % 100 != 11:
        form = forms[0]
    elif 2 <= n % 10 <= 4 and not (12 <= n % 100 <= 14):
        form = forms[1]
    else:
        form = forms[2]
    return f"{n} {form}"

def detailed_time_left():
    now = datetime.now(MOSCOW_TZ)
    if now >= TARGET_DATE:
        return None

    total_days = (TARGET_DATE - now).days  # общее количество дней

    # Считаем месяцы
    months = (TARGET_DATE.year - now.year) * 12 + (TARGET_DATE.month - now.month)
    temp_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    for _ in range(months):
        days_in_month = calendar.monthrange(temp_date.year, temp_date.month)[1]
        temp_date += timedelta(days=days_in_month)
    if temp_date > TARGET_DATE:
        months -= 1
        temp_date -= timedelta(days=calendar.monthrange(temp_date.year, temp_date.month)[1])

    remaining = TARGET_DATE - temp_date
    total_seconds = int(remaining.total_seconds())

    weeks = total_seconds // (7 * 24 * 3600)
    days = (total_seconds % (7 * 24 * 3600)) // (24 * 3600)
    hours = (total_seconds % (24 * 3600)) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    parts = []
    if months > 0:
        parts.append(pluralize(months, ["месяц", "месяца", "месяцев"]))
    if weeks > 0:
        parts.append(pluralize(weeks, ["неделя", "недели", "недель"]))
    if days > 0:
        parts.append(pluralize(days, ["день", "дня", "дней"]))
    # Часы, минуты, секунды всегда отображаем
    parts.append(pluralize(hours, ["час", "часа", "часов"]))
    parts.append(pluralize(minutes, ["минута", "минуты", "минут"]))
    parts.append(pluralize(seconds, ["секунда", "секунды", "секунд"]))

    return f"{total_days} {pluralize(total_days, ['день', 'дня', 'дней']).split()[1]}: [" + " / ".join(parts) + "]"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })
    response.raise_for_status()

def main():
    detailed = detailed_time_left()
    if detailed is None:
        send_message("МАКС ВЕРНУЛСЯ")
        with open("DONE", "w") as f:
            f.write("finished")
        sys.exit(0)
    else:
        send_message(f"До возвращения Макса {detailed}")

if __name__ == "__main__":
    main()
