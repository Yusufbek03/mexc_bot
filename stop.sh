#!/bin/bash

# Скрипт для остановки MEXC Bot

echo "🛑 Остановка MEXC Bot..."

# Проверка наличия PID файла
if [ ! -f "bot.pid" ]; then
    echo "❌ Файл bot.pid не найден. Бот не запущен."
    exit 1
fi

# Чтение PID
PID=$(cat bot.pid)

# Проверка, запущен ли процесс
if ! ps -p $PID > /dev/null; then
    echo "❌ Процесс с PID $PID не найден"
    rm -f bot.pid
    exit 1
fi

# Остановка процесса
echo "🔄 Остановка процесса $PID..."
kill $PID

# Ожидание завершения
sleep 2

# Принудительная остановка, если процесс не завершился
if ps -p $PID > /dev/null; then
    echo "⚠️ Принудительная остановка процесса..."
    kill -9 $PID
fi

# Удаление PID файла
rm -f bot.pid

echo "✅ MEXC Bot остановлен"
echo "📝 Логи сохранены в: logs/bot.log"
echo "🚀 Для запуска выполните: ./run.sh"
