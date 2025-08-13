import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "8479495164:AAE_vi0hWlJFlNlX2wryVFGc3GwFlfR-Y10"
TELEGRAM_CHAT_ID = "8107614946"

# MEXC API Configuration
MEXC_BASE_URL = "https://www.mexc.com"
MEXC_FUTURES_BASE_URL = "https://futures.mexc.com"
MEXC_ACCESS_KEY = "mx0vglUJnhvxCq1Yi8"
MEXC_SECRET_KEY = "e62d558078964ab885e3fa7a6ad7de64"

# Bot Configuration
MIN_SPREAD_PERCENT = 5.0  # Минимальный спред для уведомления (5%)
UPDATE_INTERVAL = 600  # Интервал обновления в секундах (10 минут = 600 сек)
MAX_RETRIES = 3  # Максимальное количество попыток при ошибках API

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
