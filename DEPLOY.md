# Инструкции по развертыванию Spread Monitor Bot

## Подготовка сервера

### 1. Системные требования

- **ОС**: Ubuntu 20.04+ / CentOS 7+ / Debian 10+
- **Python**: 3.8+
- **RAM**: минимум 512MB
- **Диск**: минимум 1GB свободного места
- **Сеть**: стабильное интернет-соединение

### 2. Установка зависимостей

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и pip
sudo apt install python3 python3-pip python3-venv -y

# Установка git
sudo apt install git -y

# Установка screen (для фонового запуска)
sudo apt install screen -y
```

## Развертывание

### 1. Клонирование репозитория

```bash
# Создание директории для проекта
mkdir -p /opt/spread-bot
cd /opt/spread-bot

# Клонирование репозитория
git clone <repository-url> .
```

### 2. Настройка виртуального окружения

```bash
# Создание виртуального окружения
python3 -m venv .venv

# Активация окружения
source .venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

### 3. Настройка конфигурации

```bash
# Редактирование конфигурации
nano config.py
```

Укажите ваши данные:
```python
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "ваш_токен_бота"
TELEGRAM_CHAT_ID = "ваш_chat_id"

# MEXC API Configuration
MEXC_ACCESS_KEY = "ваш_access_key"
MEXC_SECRET_KEY = "ваш_secret_key"
```

### 4. Настройка прав доступа

```bash
# Установка прав на выполнение скриптов
chmod +x *.sh

# Создание пользователя для бота (опционально)
sudo useradd -r -s /bin/false spreadbot
sudo chown -R spreadbot:spreadbot /opt/spread-bot
```

## Запуск

### 1. Тестовый запуск

```bash
# Активация окружения
source .venv/bin/activate

# Тестовый запуск
python main.py
```

### 2. Запуск в фоновом режиме

```bash
# Использование screen
screen -S spread-bot
source .venv/bin/activate
python main.py

# Отключение от screen: Ctrl+A, затем D
# Подключение к screen: screen -r spread-bot
```

### 3. Запуск через systemd (рекомендуется)

Создайте файл сервиса:

```bash
sudo nano /etc/systemd/system/spread-bot.service
```

Содержимое файла:
```ini
[Unit]
Description=Spread Monitor Bot
After=network.target

[Service]
Type=simple
User=spreadbot
WorkingDirectory=/opt/spread-bot
Environment=PATH=/opt/spread-bot/.venv/bin
ExecStart=/opt/spread-bot/.venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Активация сервиса:
```bash
# Перезагрузка systemd
sudo systemctl daemon-reload

# Включение автозапуска
sudo systemctl enable spread-bot

# Запуск сервиса
sudo systemctl start spread-bot

# Проверка статуса
sudo systemctl status spread-bot
```

## Мониторинг

### 1. Просмотр логов

```bash
# Логи systemd
sudo journalctl -u spread-bot -f

# Логи приложения
tail -f /opt/spread-bot/spread_bot.log

# Логи в реальном времени
tail -f /opt/spread-bot/logs/bot.log
```

### 2. Проверка статуса

```bash
# Статус сервиса
sudo systemctl status spread-bot

# Проверка процессов
ps aux | grep python

# Проверка портов
netstat -tlnp | grep python
```

### 3. Управление сервисом

```bash
# Остановка
sudo systemctl stop spread-bot

# Перезапуск
sudo systemctl restart spread-bot

# Перезагрузка конфигурации
sudo systemctl reload spread-bot
```

## Обновление

### 1. Обновление кода

```bash
cd /opt/spread-bot

# Остановка сервиса
sudo systemctl stop spread-bot

# Получение обновлений
git pull origin main

# Обновление зависимостей
source .venv/bin/activate
pip install -r requirements.txt

# Запуск сервиса
sudo systemctl start spread-bot
```

### 2. Откат к предыдущей версии

```bash
cd /opt/spread-bot

# Остановка сервиса
sudo systemctl stop spread-bot

# Откат к предыдущему коммиту
git reset --hard HEAD~1

# Запуск сервиса
sudo systemctl start spread-bot
```

## Безопасность

### 1. Настройка файрвола

```bash
# Установка UFW
sudo apt install ufw -y

# Настройка правил
sudo ufw allow ssh
sudo ufw allow 22
sudo ufw enable
```

### 2. Настройка SSL (опционально)

```bash
# Установка Certbot
sudo apt install certbot -y

# Получение SSL сертификата
sudo certbot certonly --standalone -d your-domain.com
```

### 3. Резервное копирование

```bash
# Создание скрипта резервного копирования
nano /opt/spread-bot/backup.sh
```

Содержимое скрипта:
```bash
#!/bin/bash
BACKUP_DIR="/opt/backups/spread-bot"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/spread-bot_$DATE.tar.gz /opt/spread-bot

# Удаление старых резервных копий (старше 7 дней)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

## Устранение неполадок

### 1. Частые проблемы

**Бот не запускается:**
```bash
# Проверка логов
sudo journalctl -u spread-bot -n 50

# Проверка прав доступа
ls -la /opt/spread-bot/

# Проверка виртуального окружения
/opt/spread-bot/.venv/bin/python --version
```

**Ошибки API:**
```bash
# Проверка подключения к интернету
ping -c 3 www.mexc.com

# Проверка DNS
nslookup www.mexc.com

# Проверка конфигурации
cat /opt/spread-bot/config.py
```

**Проблемы с Telegram:**
```bash
# Проверка токена бота
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe"

# Проверка chat_id
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates"
```

### 2. Мониторинг ресурсов

```bash
# Установка htop
sudo apt install htop -y

# Мониторинг в реальном времени
htop

# Проверка использования диска
df -h

# Проверка использования памяти
free -h
```

### 3. Автоматический перезапуск

Добавьте в systemd сервис:
```ini
[Service]
Restart=always
RestartSec=10
StartLimitInterval=60
StartLimitBurst=3
```

## Производительность

### 1. Оптимизация

```bash
# Увеличение лимитов файлов
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Оптимизация сети
echo "net.core.rmem_max = 16777216" | sudo tee -a /etc/sysctl.conf
echo "net.core.wmem_max = 16777216" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### 2. Мониторинг производительности

```bash
# Установка инструментов мониторинга
sudo apt install iotop iostat -y

# Мониторинг I/O
iotop

# Мониторинг CPU и диска
iostat -x 1
```

## Логирование

### 1. Настройка ротации логов

Создайте файл конфигурации logrotate:
```bash
sudo nano /etc/logrotate.d/spread-bot
```

Содержимое:
```
/opt/spread-bot/spread_bot.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 spreadbot spreadbot
    postrotate
        systemctl reload spread-bot
    endscript
}
```

### 2. Централизованное логирование

Для продакшена рекомендуется использовать:
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Graylog
- rsyslog

## Масштабирование

### 1. Горизонтальное масштабирование

Для обработки большего количества пар:
```bash
# Создание нескольких экземпляров
sudo cp /etc/systemd/system/spread-bot.service /etc/systemd/system/spread-bot-1.service
sudo cp /etc/systemd/system/spread-bot.service /etc/systemd/system/spread-bot-2.service

# Настройка разных конфигураций для каждого экземпляра
```

### 2. Балансировка нагрузки

Используйте nginx или haproxy для балансировки запросов к API.

## Заключение

После выполнения всех шагов у вас будет полностью настроенный и работающий Spread Monitor Bot на сервере с автоматическим перезапуском, мониторингом и резервным копированием.

Для получения дополнительной помощи обращайтесь к документации или создавайте issues в репозитории.
