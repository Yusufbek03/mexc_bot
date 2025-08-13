#!/bin/bash

# 🤖 DETECT Manipulations Bot - Быстрый запуск
# Автор: Yusufbek
# Версия: 2.1

echo "🚀 DETECT Manipulations Bot v2.1"
echo "=================================="
echo ""

# Проверка Python
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Python 3.11 не найден. Установите Python 3.11+"
    exit 1
fi

# Проверка виртуального окружения
if [ ! -d ".venv" ]; then
    echo "🔧 Создание виртуального окружения..."
    python3.11 -m venv .venv
fi

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source .venv/bin/activate

# Установка зависимостей
echo "📦 Установка зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

# Проверка конфигурации
if [ ! -f "config.py" ]; then
    echo "❌ Файл config.py не найден"
    echo "Скопируйте config.prod.py в config.py и настройте"
    exit 1
fi

# Создание директорий
mkdir -p logs

# Остановка предыдущих экземпляров
if [ -f "bot.pid" ]; then
    echo "🛑 Остановка предыдущего экземпляра..."
    ./stop.sh
fi

# Тестирование API
echo "🧪 Тестирование API..."
python test_api.py

if [ $? -eq 0 ]; then
    echo "✅ API тест прошел успешно"
else
    echo "⚠️ API тест не прошел, но продолжаем..."
fi

# Запуск бота
echo "🚀 Запуск бота..."
echo "📝 Логи: logs/bot.log"
echo "🛑 Остановка: ./stop.sh"
echo "📊 Статус: ./status.sh"
echo ""

# Запуск в фоновом режиме
nohup python main.py > logs/bot.log 2>&1 &
echo $! > bot.pid

echo "✅ Бот запущен с PID: $(cat bot.pid)"
echo "⏰ Уведомления: каждые 2 минуты"
echo "🎯 Мониторинг: 10 криптопар"
echo "💰 Источник: реальные цены из стакана"
echo ""
echo "📱 Проверьте Telegram бота!"
echo "🔗 Логи: tail -f logs/bot.log"
