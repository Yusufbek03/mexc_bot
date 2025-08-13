import logging
import asyncio
from datetime import datetime
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, MIN_SPREAD_PERCENT
from mexc_api import MEXCAPI

logger = logging.getLogger(__name__)

class SpreadBot:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        self.mexc_api = MEXCAPI()
        self.last_spreads = set()  # Для отслеживания уже отправленных спредов
        
        # Регистрируем команды
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("check", self.check_spreads_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("price", self.price_command))
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        welcome_message = """
🤖 **DETECT Manipulations Bot**

Бот для отслеживания расхождений цен между спотом и фьючерсами на бирже MEXC.

**Команды:**
/check - Проверить текущие спреды
/status - Статус бота
/start - Показать это сообщение

**Автоматические уведомления:**
Бот автоматически уведомляет о спредах от 5% и выше каждые 2 минуты.
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def check_spreads_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /check - показывает все пары с ценами из реального времени"""
        await update.message.reply_text("🔍 Проверяю спреды для всех пар...")
        
        try:
            async with self.mexc_api as api:
                # Получаем цены из стакана для всех пар
                spot_prices, futures_prices = await api.get_all_prices_from_orderbook()
                
                if spot_prices and futures_prices:
                    # Создаем список всех спредов
                    all_spreads = []
                    
                    for symbol in spot_prices.keys():
                        if symbol in futures_prices:
                            spot_price = spot_prices[symbol]
                            futures_price = futures_prices[symbol]
                            
                            if spot_price > 0 and futures_price > 0:
                                spread = abs(spot_price - futures_price) / spot_price * 100
                                
                                all_spreads.append({
                                    'symbol': symbol.replace('_USDT', ''),
                                    'spot_price': spot_price,
                                    'futures_price': futures_price,
                                    'spread': spread,
                                    'spot_symbol': symbol,
                                    'futures_symbol': symbol
                                })
                    
                    # Сортируем по спреду (от большего к меньшему)
                    all_spreads.sort(key=lambda x: x['spread'], reverse=True)
                    
                    if all_spreads:
                        message = f"📊 **Все пары с ценами из реального времени ({len(all_spreads)} пар):**\n\n"
                        
                        for spread in all_spreads:
                            symbol = spread['symbol']
                            spot_price = spread['spot_price']
                            futures_price = spread['futures_price']
                            spread_percent = spread['spread']
                            
                            # Определяем направление спреда
                            if spot_price > futures_price:
                                direction = "📈 LONG"
                                spread_type = "Спот > Фьючерс"
                            else:
                                direction = "📉 SHORT"
                                spread_type = "Фьючерс > Спот"
                            
                            # Форматируем каждую пару
                            message += f"**{symbol}** {direction}/USDT\n"
                            message += f"💰 Спред: **{spread_percent:.2f}%** ({spread_type})\n"
                            message += f"📊 Спот: {spot_price:.8f}\n"
                            message += f"📈 Фьючерс: {futures_price:.8f}\n\n"
                        
                        message += f"⏰ Обновлено: {datetime.now().strftime('%H:%M:%S')}"
                        
                        # Разбиваем на части, если сообщение слишком длинное
                        if len(message) > 4000:
                            parts = [message[i:i+4000] for i in range(0, len(message), 4000)]
                            for i, part in enumerate(parts):
                                if i == 0:
                                    await update.message.reply_text(part, parse_mode='Markdown')
                                else:
                                    await update.message.reply_text(f"Продолжение...\n\n{part}", parse_mode='Markdown')
                        else:
                            await update.message.reply_text(message, parse_mode='Markdown')
                    else:
                        await update.message.reply_text("❌ Не удалось получить данные о спредах")
                else:
                    await update.message.reply_text("❌ Не удалось получить цены из стакана")
                    
        except Exception as e:
            logger.error(f"Ошибка при проверке спредов: {e}")
            await update.message.reply_text(f"❌ Ошибка при проверке спредов: {e}")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /status"""
        status_message = f"""
📊 **Статус бота**

✅ Бот активен
⏰ Последнее обновление: {datetime.now().strftime('%H:%M:%S')}
🎯 Минимальный спред: {MIN_SPREAD_PERCENT}%
🔄 Автообновление: каждые 2 минуты
        """
        await update.message.reply_text(status_message, parse_mode='Markdown')
    
    def format_spreads_message(self, spreads: list) -> str:
        """Форматирование сообщения со спредами в нужном формате"""
        message = ""
        
        for spread in spreads:
            symbol = spread['symbol']
            spot_price = spread['spot_price']
            futures_price = spread['futures_price']
            spread_percent = spread['spread']
            
            # Определяем направление спреда
            if spot_price > futures_price:
                direction = "📈 LONG"
                spread_type = "Спот > Фьючерс"
            else:
                direction = "📉 SHORT"
                spread_type = "Фьючерс > Спот"
            
            # Форматируем сообщение в нужном стиле
            message += f"**{symbol}** {direction}/USDT\n"
            message += f"💰 Спред: **{spread_percent}%** ({spread_type})\n"
            message += f"📊 Спот: {spot_price:.8f}\n"
            message += f"📈 Фьючерс: {futures_price:.8f}\n"
            message += f"🔗 [Спот](https://www.mexc.com/exchange/{symbol}_USDT)\n"
            message += f"🔗 [Фьючерс](https://futures.mexc.com/exchange/{symbol}_USDT)\n\n"
        
        # Добавляем время обновления
        message += f"⏰ Обновлено: {datetime.now().strftime('%H:%M:%S')}"
        return message
    
    async def send_spread_alert(self, spreads: list):
        """Отправка уведомления о новых спредах"""
        if not spreads:
            return
        
        # Фильтруем только новые спреды
        new_spreads = []
        current_spreads = set()
        
        for spread in spreads:
            spread_key = f"{spread['symbol']}_{spread['spread']}"
            current_spreads.add(spread_key)
            
            if spread_key not in self.last_spreads:
                new_spreads.append(spread)
        
        if new_spreads:
            message = self.format_spreads_message(new_spreads)
            try:
                await self.bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=message,
                    parse_mode='Markdown',
                    disable_web_page_preview=True
                )
                logger.info(f"Отправлено уведомление о {len(new_spreads)} новых спредах")
            except Exception as e:
                logger.error(f"Ошибка отправки уведомления: {e}")
        
        # Обновляем список последних спредов
        self.last_spreads = current_spreads
    
    async def price_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /price - показывает цену конкретной пары"""
        if not context.args:
            await update.message.reply_text("❌ Укажите символ пары. Пример: /price BTC или /price UNI")
            return
        
        symbol = context.args[0].upper()
        if not symbol.endswith('_USDT'):
            symbol = f"{symbol}_USDT"
        
        await update.message.reply_text(f"🔍 Получаю цены для {symbol}...")
        
        try:
            async with self.mexc_api as api:
                spot_price, futures_price = await api.get_symbol_price_from_orderbook(symbol)
                
                if spot_price > 0 and futures_price > 0:
                    spread = abs(spot_price - futures_price) / spot_price * 100
                    
                    # Определяем направление спреда
                    if spot_price > futures_price:
                        direction = "📈 LONG"
                        spread_type = "Спот > Фьючерс"
                    else:
                        direction = "📉 SHORT"
                        spread_type = "Фьючерс > Спот"
                    
                    message = f"**{symbol.replace('_USDT', '')}** {direction}/USDT\n"
                    message += f"💰 Спред: **{spread:.2f}%** ({spread_type})\n"
                    message += f"📊 Спот: {spot_price:.8f}\n"
                    message += f"📈 Фьючерс: {futures_price:.8f}\n"
                    message += f"🔗 [Спот](https://www.mexc.com/exchange/{symbol})\n"
                    message += f"🔗 [Фьючерс](https://futures.mexc.com/exchange/{symbol})\n"
                    message += f"⏰ Обновлено: {datetime.now().strftime('%H:%M:%S')}"
                    
                    await update.message.reply_text(message, parse_mode='Markdown')
                else:
                    await update.message.reply_text(f"❌ Не удалось получить цены для {symbol}")
                    
        except Exception as e:
            logger.error(f"Ошибка при получении цены для {symbol}: {e}")
            await update.message.reply_text(f"❌ Ошибка при получении цены: {e}")
    
    async def run(self):
        """Запуск бота"""
        logger.info("Запуск Telegram бота...")
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        try:
            # Основной цикл бота
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Остановка бота...")
        finally:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
