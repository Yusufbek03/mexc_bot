# Spread Monitor Bot

Бот для мониторинга спредов между спотовыми и фьючерсными ценами криптовалют на бирже MEXC с уведомлениями в Telegram.

## 🚀 Быстрый старт

```bash
# Клонирование
git clone <repository-url>
cd bot

# Установка зависимостей
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Настройка config.py с вашими токенами
nano config.py

# Запуск
python main.py
```

## Возможности

- 🔍 Мониторинг спредов в реальном времени
- 📊 Отслеживание спотовых и фьючерсных цен
- 📱 Уведомления в Telegram при обнаружении высоких спредов
- ⚡ Автоматические обновления каждые 10 минут
- 🎯 Настраиваемый минимальный порог спреда (по умолчанию 5%)

## Установка

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd bot
```

2. **Создайте виртуальное окружение:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate  # Windows
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настройте конфигурацию:**
Отредактируйте файл `config.py`:
```python
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "ваш_токен_бота"
TELEGRAM_CHAT_ID = "ваш_chat_id"

# MEXC API Configuration
MEXC_ACCESS_KEY = "ваш_access_key"
MEXC_SECRET_KEY = "ваш_secret_key"

# Bot Configuration
MIN_SPREAD_PERCENT = 5.0  # Минимальный спред для уведомления
UPDATE_INTERVAL = 600     # Интервал обновления в секундах (10 минут)
```

## Запуск

### Простой запуск
```bash
python main.py
```

### Запуск с помощью скриптов

1. **Быстрый старт:**
```bash
chmod +x quick_start.sh
./quick_start.sh
```

2. **Запуск в фоне:**
```bash
chmod +x run.sh
./run.sh
```

3. **Проверка статуса:**
```bash
chmod +x status.sh
./status.sh
```

4. **Остановка:**
```bash
chmod +x stop.sh
./stop.sh
```

## Структура проекта

```
bot/
├── main.py              # Основной файл бота
├── config.py            # Конфигурация
├── mexc_api.py          # API для работы с MEXC
├── telegram_bot.py      # Telegram бот
├── crypto_list.py       # Список криптовалют
├── requirements.txt     # Зависимости
├── README.md           # Документация
├── quick_start.sh      # Скрипт быстрого запуска
├── run.sh              # Скрипт запуска в фоне
├── status.sh           # Скрипт проверки статуса
├── stop.sh             # Скрипт остановки
└── logs/               # Папка с логами
```

## Настройка Telegram бота

1. Создайте бота через @BotFather
2. Получите токен бота
3. Добавьте бота в нужный чат
4. Получите chat_id (можно использовать @userinfobot)
5. Укажите токен и chat_id в `config.py`

## Настройка MEXC API

1. Зарегистрируйтесь на MEXC
2. Создайте API ключи в личном кабинете
3. Укажите access_key и secret_key в `config.py`

## Логирование

Бот создает лог-файл `spread_bot.log` с подробной информацией о работе. Уровень логирования можно настроить в `config.py`.

## Мониторируемые пары

По умолчанию бот отслеживает следующие пары:
- BTC_USDT
- ETH_USDT
- BNB_USDT
- ADA_USDT
- SOL_USDT
- UNI_USDT
- DOT_USDT
- LINK_USDT
- MATIC_USDT
- AVAX_USDT

## Уведомления

Бот отправляет уведомления в Telegram при обнаружении спредов выше установленного порога. Уведомление содержит:
- Символ криптовалюты
- Процент спреда
- Спотовую цену
- Фьючерсную цену

## Безопасность

- Храните API ключи в безопасном месте
- Не публикуйте токены в публичных репозиториях
- Используйте виртуальное окружение
- Регулярно обновляйте зависимости

## Поддержка

При возникновении проблем:
1. Проверьте логи в файле `spread_bot.log`
2. Убедитесь в правильности настройки API ключей
3. Проверьте подключение к интернету
4. Убедитесь в корректности токена Telegram бота

## Лицензия

MIT License
