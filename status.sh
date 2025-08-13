#!/bin/bash

# 🤖 DETECT Manipulations Bot - Статус
# Автор: Yusufbek
# Версия: 2.1

echo "📊 Статус DETECT Manipulations Bot"
echo "=================================="
echo ""

# Проверка PID файла
if [ ! -f "bot.pid" ]; then
    echo "❌ Бот не запущен (файл bot.pid не найден)"
    exit 1
fi

PID=$(cat bot.pid)

# Проверка процесса
if ! ps -p $PID > /dev/null; then
    echo "❌ Бот не запущен (процесс $PID не найден)"
    rm -f bot.pid
    exit 1
fi

echo "✅ Бот запущен (PID: $PID)"
echo ""

# Информация о процессе
echo "📈 Информация о процессе:"
ps -p $PID -o pid,ppid,pcpu,pmem,etime,command

echo ""

# Использование ресурсов
echo "💾 Использование ресурсов:"
ps -p $PID -o pid,pcpu,pmem,vsz,rss,etime

echo ""

# Проверка логов
if [ -f "logs/bot.log" ]; then
    echo "📝 Последние логи (10 строк):"
    echo "--------------------------------"
    tail -10 logs/bot.log
else
    echo "⚠️ Файл логов не найден"
fi

echo ""

# Проверка конфигурации
if [ -f "config.py" ]; then
    echo "⚙️ Конфигурация:"
    echo "--------------------------------"
    grep -E "MIN_SPREAD_PERCENT|UPDATE_INTERVAL|TELEGRAM_BOT_TOKEN" config.py | head -3
else
    echo "❌ Файл конфигурации не найден"
fi

echo ""
echo "🛑 Остановка: ./stop.sh"
echo "🔄 Перезапуск: ./quick_start.sh"
echo "📊 Логи: tail -f logs/bot.log"
