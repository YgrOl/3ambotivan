from telethon import TelegramClient
import asyncio
from datetime import datetime, timedelta

# Введіть дані
API_ID = 26182309  # Замініть на ваш API ID
API_HASH = "3e3b91c160ec4110e028137568c62236"  # Замініть на ваш API Hash
GIF_PATH = r"1699393570818693.mp4"  # Шлях до GIF
FRIEND_USERNAME = "@genjimainbtw"  # Ім'я користувача друга
UTC_OFFSET = 3  # Часовий пояс MSK (UTC+3)

# Створення клієнта
client = TelegramClient("session_name", API_ID, API_HASH)

# Функція для відправки GIF
async def send_gif():
    try:
        if not client.is_connected():
            print("Клієнт не підключений. Перепідключаємося...")
            await client.connect()
        if not await client.is_user_authorized():
            print("Клієнт не авторизований. Перевірте сесію або авторизуйтеся.")
            return
        print(f"Відправляємо GIF другу {FRIEND_USERNAME}...")
        await client.send_file(FRIEND_USERNAME, GIF_PATH)
        print("GIF успішно надіслано!")
    except Exception as e:
        print(f"Помилка при відправці GIF: {e}")

# Розрахунок часу до наступного 03:00 за MSK
def seconds_until_target(hour, minute, utc_offset=0):
    now = datetime.utcnow()  # Поточний час у UTC
    target_hour = (hour - utc_offset) % 24  # Корекція для годин у межах 0–23
    target = now.replace(hour=target_hour, minute=minute, second=0, microsecond=0)

    if now > target:  # Якщо час вже пройшов, вибираємо наступний день
        target += timedelta(days=1)

    return (target - now).total_seconds()

# Основна функція
async def main():
    # Підключення до Telegram з використанням сесійного файлу
    await client.connect()
    if not await client.is_user_authorized():
        print("Клієнт не авторизований. Завантажте сесійний файл або авторизуйтеся вручну.")
        return
    print("Авторизація пройдена.")

    while True:
        # Час до 03:00 MSK
        sleep_time = seconds_until_target(3, 0, UTC_OFFSET)
        print(f"Чекаємо до 03:00 MSK... ({sleep_time:.2f} секунд)")
        await asyncio.sleep(sleep_time)
        await send_gif()  # Відправляємо GIF

# Запуск клієнта
if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
