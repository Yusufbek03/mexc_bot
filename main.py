import asyncio
import logging
import signal
import sys
from datetime import datetime
from config import LOG_LEVEL, LOG_FORMAT, UPDATE_INTERVAL, MIN_SPREAD_PERCENT
from mexc_api import MEXCAPI
from telegram_bot import SpreadBot

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('spread_bot.log')
    ]
)
logger = logging.getLogger(__name__)

class SpreadMonitor:
    def __init__(self):
        self.bot = SpreadBot()
        self.mexc_api = MEXCAPI()
        self.running = True
        self.last_check = None
        self.realtime_task = None
        self.last_notification_time = {}  # Отслеживание времени последнего уведомления для каждого символа
        
        # Обработка сигналов для корректного завершения
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Обработчик сигналов для корректного завершения"""
        logger.info(f"Получен сигнал {signum}, завершение работы...")
        self.running = False
    
    async def price_update_handler(self, symbol: str, data, data_type: str):
        """Обработчик обновлений цен в реальном времени"""
        try:
            if data_type == 'price_update':
                # Обновление цены из стакана
                spot_price = data.get('spot', {}).get('price', 0)
                futures_price = data.get('futures', {}).get('price', 0)
                
                if spot_price > 0 and futures_price > 0:
                    # Обновляем цены в API
                    self.mexc_api.spot_prices[symbol] = spot_price
                    self.mexc_api.futures_prices[symbol] = futures_price
                    
                    # Рассчитываем спред
                    spread = abs(spot_price - futures_price) / spot_price * 100
                    
                    if spread >= MIN_SPREAD_PERCENT:
                        # Проверяем, прошло ли достаточно времени с последнего уведомления для этого символа
                        current_time = datetime.now()
                        last_notification = self.last_notification_time.get(symbol)
                        
                        if last_notification is None or (current_time - last_notification).total_seconds() >= UPDATE_INTERVAL:
                            logger.info(f"🚨 ВЫСОКИЙ СПРЕД в реальном времени!")
                            logger.info(f"   {symbol}: {spread:.2f}%")
                            logger.info(f"   Спот: ${spot_price:.8f}")
                            logger.info(f"   Фьючерс: ${futures_price:.8f}")
                            
                            # Отправляем уведомление
                            spread_info = [{
                                'symbol': symbol.replace('_USDT', ''),
                                'spot_price': spot_price,
                                'futures_price': futures_price,
                                'spread': spread,
                                'spot_symbol': symbol,
                                'futures_symbol': symbol
                            }]
                            
                            await self.bot.send_spread_alert(spread_info)
                            
                            # Обновляем время последнего уведомления для этого символа
                            self.last_notification_time[symbol] = current_time
                        else:
                            remaining_time = UPDATE_INTERVAL - (current_time - last_notification).total_seconds()
                            logger.debug(f"⏰ Пропускаем уведомление для {symbol}, следующее через {remaining_time:.0f} сек")
                    
                    logger.debug(f"💰 {symbol}: Спот ${spot_price:.8f}, Фьючерс ${futures_price:.8f}, Спред {spread:.2f}%")
                    
        except Exception as e:
            logger.error(f"Ошибка в обработчике цен: {e}")
    
    async def check_spreads(self):
        """Проверка спредов и отправка уведомлений"""
        try:
            logger.info("🔍 Проверка спредов из стакана...")
            
            async with self.mexc_api as api:
                # Получаем цены из стакана
                spot_prices, futures_prices = await api.get_all_prices_from_orderbook()
                
                if not spot_prices or not futures_prices:
                    logger.warning("Не удалось получить данные из стакана, используем тикеры")
                    spot_prices, futures_prices = await api.get_all_tickers()
                
                if not spot_prices or not futures_prices:
                    logger.error("Не удалось получить данные о ценах")
                    return
                
                # Поиск спредов
                spreads = api.find_spreads(spot_prices, futures_prices, MIN_SPREAD_PERCENT)
                
                if spreads:
                    logger.info(f"Найдено {len(spreads)} пар со спредом от {MIN_SPREAD_PERCENT}%")
                    
                    # Фильтруем спреды, для которых не прошло достаточно времени с последнего уведомления
                    current_time = datetime.now()
                    filtered_spreads = []
                    
                    for spread in spreads:
                        symbol = spread['spot_symbol']
                        last_notification = self.last_notification_time.get(symbol)
                        
                        if last_notification is None or (current_time - last_notification).total_seconds() >= UPDATE_INTERVAL:
                            filtered_spreads.append(spread)
                        else:
                            remaining_time = UPDATE_INTERVAL - (current_time - last_notification).total_seconds()
                            logger.debug(f"⏰ Пропускаем {symbol}, следующее уведомление через {remaining_time:.0f} сек")
                    
                    if filtered_spreads:
                        # Отправка уведомления в Telegram
                        await self.bot.send_spread_alert(filtered_spreads)
                        
                        # Обновляем время последнего уведомления для отправленных символов
                        for spread in filtered_spreads:
                            symbol = spread['spot_symbol']
                            self.last_notification_time[symbol] = current_time
                        
                        # Логирование найденных спредов
                        for spread in filtered_spreads[:5]:  # Логируем топ-5
                            logger.info(
                                f"Спред: {spread['symbol']} - {spread['spread']}% "
                                f"(Спот: {spread['spot_price']:.8f}, "
                                f"Фьючерс: {spread['futures_price']:.8f})"
                            )
                    else:
                        logger.info("Все найденные спреды были недавно уведомлены")
                else:
                    logger.info("Спреды от 5% не найдены")
                
                self.last_check = datetime.now()
                
        except Exception as e:
            logger.error(f"Ошибка при проверке спредов: {e}")
    
    async def start_realtime_monitoring(self):
        """Запуск мониторинга в реальном времени"""
        try:
            logger.info("🚀 Запуск мониторинга в реальном времени...")
            
            # Добавляем обработчик обновлений цен
            self.mexc_api.add_price_callback(self.price_update_handler)
            
            # Запускаем обновления в реальном времени
            self.realtime_task = asyncio.create_task(
                self.mexc_api.start_realtime_updates(
                    symbols=['BTC_USDT', 'ETH_USDT', 'BNB_USDT', 'ADA_USDT', 'SOL_USDT', 'UNI_USDT', 'DOT_USDT', 'LINK_USDT', 'MATIC_USDT', 'AVAX_USDT'],
                    update_interval=600  # Обновляем каждые 10 минут
                )
            )
            
            logger.info("✅ Мониторинг в реальном времени запущен")
            
        except Exception as e:
            logger.error(f"Ошибка запуска мониторинга в реальном времени: {e}")
    
    async def run_monitor(self):
        """Основной цикл мониторинга"""
        logger.info("🚀 Запуск мониторинга спредов...")
        logger.info(f"🎯 Минимальный спред: {MIN_SPREAD_PERCENT}%")
        logger.info(f"⏰ Интервал проверки: {UPDATE_INTERVAL} секунд ({UPDATE_INTERVAL/60:.1f} минут)")
        
        # Запуск Telegram бота в отдельной задаче
        bot_task = asyncio.create_task(self.bot.run())
        
        # Запуск мониторинга в реальном времени
        await self.start_realtime_monitoring()
        
        try:
            while self.running:
                # Периодическая проверка спредов (как fallback)
                await self.check_spreads()
                
                # Ожидание до следующей проверки
                for _ in range(UPDATE_INTERVAL):
                    if not self.running:
                        break
                    await asyncio.sleep(1)
                    
        except Exception as e:
            logger.error(f"Критическая ошибка в мониторинге: {e}")
        finally:
            # Остановка задач
            if self.realtime_task:
                self.realtime_task.cancel()
                try:
                    await self.realtime_task
                except asyncio.CancelledError:
                    pass
            
            bot_task.cancel()
            try:
                await bot_task
            except asyncio.CancelledError:
                pass
            
            logger.info("✅ Мониторинг завершен")
    
    async def run(self):
        """Запуск всех компонентов"""
        try:
            await self.run_monitor()
        except KeyboardInterrupt:
            logger.info("Получен сигнал прерывания")
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
        finally:
            self.running = False

async def main():
    """Главная функция"""
    monitor = SpreadMonitor()
    await monitor.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Программа завершена пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        sys.exit(1)
