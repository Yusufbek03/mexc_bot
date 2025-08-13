#!/bin/bash

# Скрипт для запуска MEXC Bot

echo "🚀 Запуск MEXC Bot..."

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.8+"
    exit 1
fi

# Проверка виртуального окружения
if [ ! -d ".venv" ]; then
    echo "❌ Виртуальное окружение не найдено"
    echo "Создайте его командой: python3 -m venv .venv"
    exit 1
fi

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source .venv/bin/activate

# Проверка наличия зависимостей
if [ ! -f "requirements.txt" ]; then
    echo "❌ Файл requirements.txt не найден"
    exit 1
fi

# Установка зависимостей
echo "📦 Установка зависимостей..."
pip install -r requirements.txt

# Проверка конфигурации
if [ ! -f "config.py" ]; then
    echo "❌ Файл config.py не найден"
    exit 1
fi

# Создание директории для логов
mkdir -p logs

# Запуск бота в фоновом режиме
echo "🚀 Запуск бота в фоновом режиме..."
nohup python main.py > logs/bot.log 2>&1 &

# Сохранение PID
echo $! > bot.pid

echo "✅ Бот запущен с PID: $(cat bot.pid)"
echo "📝 Логи сохраняются в: logs/bot.log"
echo "🛑 Для остановки выполните: ./stop.sh"
echo "📊 Для просмотра логов: tail -f logs/bot.log"
echo "⏰ Обновление цен: каждые 10 секунд"
echo "🎯 Мониторинг: 10 криптопар"
echo "📱 Telegram: автоматические уведомления"
