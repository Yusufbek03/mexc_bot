import aiohttp
import asyncio
import logging
import hmac
import hashlib
import time
import json
from typing import Dict, List, Optional, Tuple, Callable
from config import MEXC_BASE_URL, MEXC_FUTURES_BASE_URL, MEXC_ACCESS_KEY, MEXC_SECRET_KEY, MAX_RETRIES
import random

logger = logging.getLogger(__name__)

class MEXCAPI:
    def __init__(self):
        self.session = None
        self.spot_prices = {}
        self.futures_prices = {}
        self.callbacks = []
        
        # Импортируем полный список криптовалют
        from crypto_list import FULL_CRYPTO_LIST
        self.test_data = FULL_CRYPTO_LIST
        
        # API ключи
        self.access_key = MEXC_ACCESS_KEY
        self.secret_key = MEXC_SECRET_KEY
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def _generate_signature(self, params: str, timestamp: int) -> str:
        """Генерация подписи для API запросов"""
        message = f"{params}&timestamp={timestamp}"
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    async def get_spot_tickers(self) -> Dict[str, float]:
        """Получение всех тикеров спота через реальный API MEXC"""
        try:
            url = "https://api.mexc.com/api/v3/ticker/24hr"
            
            connector = aiohttp.TCPConnector(ssl=False, limit=100, force_close=True)
            timeout = aiohttp.ClientTimeout(total=30, connect=10)
            
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Accept': 'application/json'
                }
                
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        tickers = {}
                        
                        for item in data:
                            if isinstance(item, dict):
                                symbol = item.get('symbol', '')
                                price = item.get('lastPrice', 0)
                                
                                if symbol and price:
                                    try:
                                        price_float = float(price)
                                        if price_float > 0:
                                            # Конвертируем формат символа в BTC_USDT для единообразия
                                            symbol_upper = str(symbol).upper()
                                            if symbol_upper.endswith('USDT'):
                                                # "BTCUSDT" -> "BTC_USDT"
                                                base = symbol_upper[:-4]
                                                unified_symbol = f"{base}_USDT"
                                                tickers[unified_symbol] = price_float
                                            else:
                                                # Пропускаем не-USDT пары
                                                continue
                                    except (ValueError, TypeError):
                                        continue
                        
                        if tickers:
                            logger.info(f"✅ Получено {len(tickers)} спот тикеров с MEXC API")
                            self.spot_prices = tickers
                            return tickers
                        else:
                            logger.warning("Получен пустой ответ от MEXC API")
                    else:
                        logger.warning(f"Ошибка API MEXC: {response.status}")
                        
        except Exception as e:
            logger.error(f"Ошибка при получении спот тикеров: {e}")
        
        # Fallback к тестовым данным
        logger.warning("Используем тестовые данные для спота")
        spot_tickers, _ = self.generate_test_data()
        return spot_tickers
    
    async def get_futures_tickers(self) -> Dict[str, float]:
        """Получение всех тикеров фьючерсов через реальный API MEXC"""
        try:
            url = "https://contract.mexc.com/api/v1/contract/ticker"
            
            connector = aiohttp.TCPConnector(ssl=False, limit=100, force_close=True)
            timeout = aiohttp.ClientTimeout(total=30, connect=10)
            
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Accept': 'application/json'
                }
                
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        tickers = {}
                        
                        if data.get('success') and 'data' in data:
                            for item in data['data']:
                                if isinstance(item, dict):
                                    symbol = item.get('symbol', '')
                                    price = item.get('last', 0)
                                    
                                    if symbol and price:
                                        try:
                                            price_float = float(price)
                                            if price_float > 0:
                                                # Конвертируем формат символа в BTC_USDT для единообразия
                                                symbol_upper = str(symbol).upper()
                                                if symbol_upper.endswith('USDT'):
                                                    # "BTCUSDT" -> "BTC_USDT"
                                                    base = symbol_upper[:-4]
                                                    unified_symbol = f"{base}_USDT"
                                                    tickers[unified_symbol] = price_float
                                                else:
                                                    # Пропускаем не-USDT пары
                                                    continue
                                        except (ValueError, TypeError):
                                            continue
                        
                        if tickers:
                            logger.info(f"✅ Получено {len(tickers)} фьючерс тикеров с MEXC API")
                            self.futures_prices = tickers
                            return tickers
                        else:
                            logger.warning("Получен пустой ответ от MEXC Futures API")
                    else:
                        logger.warning(f"Ошибка MEXC Futures API: {response.status}")
                        
        except Exception as e:
            logger.error(f"Ошибка при получении фьючерс тикеров: {e}")
        
        # Fallback к тестовым данным
        logger.warning("Используем тестовые данные для фьючерсов")
        _, futures_tickers = self.generate_test_data()
        return futures_tickers
    
    async def get_order_book(self, symbol: str, limit: int = 20) -> Optional[Dict]:
        """Получение стакана заявок для конкретной пары"""
        for attempt in range(MAX_RETRIES):
            try:
                url = "https://api.mexc.com/api/v3/depth"
                # Для спотового API MEXC требуется формат символа без подчеркивания: BTCUSDT
                request_symbol = symbol.replace('_', '').upper()
                params = {
                    'symbol': request_symbol,
                    'limit': limit
                }
                
                connector = aiohttp.TCPConnector(ssl=False, limit=100, force_close=True)
                timeout = aiohttp.ClientTimeout(total=10, connect=5)
                
                async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                        'Accept': 'application/json'
                    }
                    
                    async with session.get(url, params=params, headers=headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            if 'bids' in data and 'asks' in data and data['bids'] and data['asks']:
                                logger.debug(f"✅ Получен стакан для {symbol}")
                                return data
                            else:
                                logger.warning(f"Пустой стакан для {symbol}")
                        else:
                            logger.warning(f"Ошибка получения стакана для {symbol}: {response.status}")
                        
                        if attempt < MAX_RETRIES - 1:
                            await asyncio.sleep(1)
                            
            except Exception as e:
                logger.error(f"Ошибка при получении стакана для {symbol} (попытка {attempt + 1}): {e}")
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(1)
        
        return None
    
    async def get_futures_order_book(self, symbol: str, limit: int = 20) -> Optional[Dict]:
        """Получение стакана заявок для фьючерсов"""
        for attempt in range(MAX_RETRIES):
            try:
                # Используем правильный URL для фьючерсного API MEXC
                url = "https://contract.mexc.com/api/v1/contract/depth"
                # Для фьючерсного API MEXC используется формат символа с подчеркиванием: BTC_USDT
                request_symbol = symbol.upper()
                params = {
                    'symbol': request_symbol,
                    'limit': limit
                }
                
                connector = aiohttp.TCPConnector(ssl=False, limit=100, force_close=True)
                timeout = aiohttp.ClientTimeout(total=10, connect=5)
                
                async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                        'Accept': 'application/json'
                    }
                    
                    async with session.get(url, params=params, headers=headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data.get('success') and 'data' in data:
                                orderbook_data = data['data']
                                if 'bids' in orderbook_data and 'asks' in orderbook_data and orderbook_data['bids'] and orderbook_data['asks']:
                                    logger.debug(f"✅ Получен фьючерсный стакан для {symbol}")
                                    return orderbook_data
                                else:
                                    logger.warning(f"Пустой фьючерсный стакан для {symbol}")
                            else:
                                logger.warning(f"Ошибка API для фьючерсного стакана {symbol}")
                        else:
                            logger.warning(f"Ошибка получения фьючерсного стакана для {symbol}: {response.status}")
                        
                        if attempt < MAX_RETRIES - 1:
                            await asyncio.sleep(1)
                            
            except Exception as e:
                logger.error(f"Ошибка при получении фьючерсного стакана для {symbol} (попытка {attempt + 1}): {e}")
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(1)
        
        return None
    
    def add_price_callback(self, callback: Callable):
        """Добавление колбэка для обновления цен"""
        self.callbacks.append(callback)
    
    async def start_realtime_updates(self, symbols: List[str] = None, update_interval: int = 10):
        """Запуск обновления цен в реальном времени из стакана"""
        if symbols is None:
            symbols = ['BTC_USDT', 'ETH_USDT', 'BNB_USDT', 'ADA_USDT', 'SOL_USDT', 'UNI_USDT', 'DOT_USDT', 'LINK_USDT', 'MATIC_USDT', 'AVAX_USDT']
        
        logger.info(f"Запуск обновления цен в реальном времени из стакана для {len(symbols)} символов")
        
        while True:
            try:
                # Получаем актуальные цены из стакана
                spot_prices, futures_prices = await self.get_all_prices_from_orderbook(symbols)
                
                # Обновляем внутренние словари
                self.spot_prices = spot_prices
                self.futures_prices = futures_prices
                
                # Вызываем колбэки для обновления цен
                for symbol in symbols:
                    if symbol in spot_prices and symbol in futures_prices:
                        spot_price = spot_prices[symbol]
                        futures_price = futures_prices[symbol]
                        
                        # Вызываем колбэки
                        for callback in self.callbacks:
                            try:
                                await callback(symbol, {
                                    'spot': {'price': spot_price},
                                    'futures': {'price': futures_price}
                                }, 'price_update')
                            except Exception as e:
                                logger.error(f"Ошибка в колбэке цены: {e}")
                
                await asyncio.sleep(update_interval)
                
            except Exception as e:
                logger.error(f"Ошибка в цикле обновления: {e}")
                await asyncio.sleep(update_interval)
    
    def generate_test_data(self) -> Tuple[Dict[str, float], Dict[str, float]]:
        """Генерация тестовых данных с реалистичными спредами"""
        spot_tickers = {}
        futures_tickers = {}
        
        for symbol, base_data in self.test_data.items():
            # Добавляем случайные колебания
            spot_variation = random.uniform(0.95, 1.05)
            futures_variation = random.uniform(0.90, 1.10)
            
            spot_price = base_data['spot'] * spot_variation
            futures_price = base_data['futures'] * futures_variation
            
            spot_tickers[f"{symbol}_USDT"] = round(spot_price, 8)
            futures_tickers[f"{symbol}_USDT"] = round(futures_price, 8)
        
        return spot_tickers, futures_tickers
    
    async def get_all_tickers(self) -> Tuple[Dict[str, float], Dict[str, float]]:
        """Получение всех цен из стакана одновременно (предпочтительно)"""
        try:
            # Пытаемся получить цены из стакана
            spot_prices, futures_prices = await self.get_all_prices_from_orderbook()
            
            if spot_prices and futures_prices:
                logger.info("✅ Получены цены из стакана")
                return spot_prices, futures_prices
            else:
                logger.warning("Не удалось получить цены из стакана, используем тикеры")
                # Fallback к тикерам
                spot_task = asyncio.create_task(self.get_spot_tickers())
                futures_task = asyncio.create_task(self.get_futures_tickers())
                return await asyncio.gather(spot_task, futures_task)
                
        except Exception as e:
            logger.error(f"Ошибка получения цен из стакана: {e}, используем тикеры")
            # Fallback к тикерам
            spot_task = asyncio.create_task(self.get_spot_tickers())
            futures_task = asyncio.create_task(self.get_futures_tickers())
            return await asyncio.gather(spot_task, futures_task)
    
    def normalize_symbol(self, symbol: str) -> str:
        """Нормализация символа для сравнения"""
        # Убираем _USDT/USDT и приводим к верхнему регистру
        return symbol.replace('_USDT', '').replace('USDT', '').upper()
    
    def calculate_spread(self, spot_price: float, futures_price: float) -> float:
        """Расчет спреда в процентах"""
        if spot_price <= 0 or futures_price <= 0:
            return 0.0
        
        spread = abs(spot_price - futures_price) / spot_price * 100
        return round(spread, 2)
    
    def find_spreads(self, spot_tickers: Dict[str, float], futures_tickers: Dict[str, float], min_spread: float = 5.0) -> List[Dict]:
        """Поиск пар с высоким спредом"""
        spreads = []
        
        # Создаем словарь нормализованных фьючерс тикеров
        normalized_futures = {}
        for symbol, price in futures_tickers.items():
            normalized_symbol = self.normalize_symbol(symbol)
            normalized_futures[normalized_symbol] = price
        
        # Проверяем споты
        for symbol, spot_price in spot_tickers.items():
            normalized_symbol = self.normalize_symbol(symbol)
            
            if normalized_symbol in normalized_futures:
                futures_price = normalized_futures[normalized_symbol]
                spread = self.calculate_spread(spot_price, futures_price)
                
                if spread >= min_spread:
                    spreads.append({
                        'symbol': normalized_symbol,
                        'spot_price': spot_price,
                        'futures_price': futures_price,
                        'spread': spread,
                        'spot_symbol': symbol,
                        'futures_symbol': symbol.replace('_USDT', '_USDT') if '_USDT' in symbol else symbol
                    })
        
        # Сортируем по убыванию спреда
        spreads.sort(key=lambda x: x['spread'], reverse=True)
        return spreads

    async def get_spot_prices_from_orderbook(self, symbols: List[str] = None) -> Dict[str, float]:
        """Получение спот цен из реального стакана заявок"""
        if symbols is None:
            symbols = ['BTC_USDT', 'ETH_USDT', 'BNB_USDT', 'ADA_USDT', 'SOL_USDT', 'UNI_USDT', 'DOT_USDT', 'LINK_USDT', 'MATIC_USDT', 'AVAX_USDT']
        
        prices = {}
        logger.info(f"Получение спот цен из стакана для {len(symbols)} символов...")
        
        # Создаем задачи для параллельного получения стаканов
        tasks = []
        for symbol in symbols:
            task = asyncio.create_task(self.get_order_book(symbol, limit=5))
            tasks.append((symbol, task))
        
        # Ждем выполнения всех задач
        for symbol, task in tasks:
            try:
                orderbook = await task
                if orderbook and 'bids' in orderbook and 'asks' in orderbook:
                    bids = orderbook['bids']
                    asks = orderbook['asks']
                    
                    if bids and asks:
                        # Берем среднюю цену между лучшим bid и ask
                        best_bid = float(bids[0][0])
                        best_ask = float(asks[0][0])
                        mid_price = (best_bid + best_ask) / 2
                        
                        prices[symbol] = mid_price
                        logger.debug(f"✅ {symbol}: ${mid_price:.8f} (bid: ${best_bid:.8f}, ask: ${best_ask:.8f})")
                    else:
                        logger.warning(f"Пустой стакан для {symbol}")
                else:
                    logger.warning(f"Не удалось получить стакан для {symbol}")
                    
            except Exception as e:
                logger.error(f"Ошибка получения стакана для {symbol}: {e}")
                continue
        
        if prices:
            logger.info(f"✅ Получено {len(prices)} спот цен из стакана")
            self.spot_prices = prices
        else:
            logger.warning("Не удалось получить ни одной цены из стакана")
        
        return prices
    
    async def get_futures_prices_from_orderbook(self, symbols: List[str] = None) -> Dict[str, float]:
        """Получение фьючерсных цен из реального стакана заявок"""
        if symbols is None:
            symbols = ['BTC_USDT', 'ETH_USDT', 'BNB_USDT', 'ADA_USDT', 'SOL_USDT', 'UNI_USDT', 'DOT_USDT', 'LINK_USDT', 'MATIC_USDT', 'AVAX_USDT']
        
        prices = {}
        logger.info(f"Получение фьючерсных цен из стакана для {len(symbols)} символов...")
        
        # Создаем задачи для параллельного получения стаканов
        tasks = []
        for symbol in symbols:
            task = asyncio.create_task(self.get_futures_order_book(symbol, limit=5))
            tasks.append((symbol, task))
        
        # Ждем выполнения всех задач
        for symbol, task in tasks:
            try:
                orderbook = await task
                if orderbook and 'bids' in orderbook and 'asks' in orderbook:
                    bids = orderbook['bids']
                    asks = orderbook['asks']
                    
                    if bids and asks:
                        # Берем среднюю цену между лучшим bid и ask
                        best_bid = float(bids[0][0])
                        best_ask = float(asks[0][0])
                        mid_price = (best_bid + best_ask) / 2
                        
                        prices[symbol] = mid_price
                        logger.debug(f"✅ {symbol}: ${mid_price:.8f} (bid: ${best_bid:.8f}, ask: ${best_ask:.8f})")
                    else:
                        logger.warning(f"Пустой фьючерсный стакан для {symbol}")
                else:
                    logger.warning(f"Не удалось получить фьючерсный стакан для {symbol}")
                    
            except Exception as e:
                logger.error(f"Ошибка получения фьючерсного стакана для {symbol}: {e}")
                continue
        
        if prices:
            logger.info(f"✅ Получено {len(prices)} фьючерсных цен из стакана")
            self.futures_prices = prices
        else:
            logger.warning("Не удалось получить ни одной фьючерсной цены из стакана")
        
        return prices
    
    async def get_all_prices_from_orderbook(self, symbols: List[str] = None) -> Tuple[Dict[str, float], Dict[str, float]]:
        """Получение всех цен из стакана одновременно"""
        if symbols is None:
            symbols = ['BTC_USDT', 'ETH_USDT', 'BNB_USDT', 'ADA_USDT', 'SOL_USDT', 'UNI_USDT', 'DOT_USDT', 'LINK_USDT', 'MATIC_USDT', 'AVAX_USDT']
        
        # Для спота используем стакан, для фьючерсов - тикеры (так как стакан фьючерсов недоступен)
        spot_task = asyncio.create_task(self.get_spot_prices_from_orderbook(symbols))
        futures_task = asyncio.create_task(self.get_futures_tickers())
        
        spot_prices, futures_tickers = await asyncio.gather(spot_task, futures_task)
        
        # Фильтруем фьючерсные цены только для нужных символов
        futures_prices = {}
        for symbol in symbols:
            if symbol in futures_tickers:
                futures_prices[symbol] = futures_tickers[symbol]
        
        # Если не удалось получить реальные фьючерсные цены, используем fallback
        if not futures_prices:
            logger.warning("Не удалось получить реальные фьючерсные цены, используем fallback")
            _, futures_tickers_fallback = self.generate_test_data()
            for symbol in symbols:
                if symbol in futures_tickers_fallback:
                    futures_prices[symbol] = futures_tickers_fallback[symbol]
        
        return spot_prices, futures_prices
    
    async def get_symbol_price_from_orderbook(self, symbol: str) -> Tuple[float, float]:
        """Получение цены конкретной пары из стакана (спот + фьючерс)"""
        try:
            spot_orderbook = await self.get_order_book(symbol, limit=5)
            futures_orderbook = await self.get_futures_order_book(symbol, limit=5)
            
            spot_price = 0
            futures_price = 0
            
            if spot_orderbook and 'bids' in spot_orderbook and 'asks' in spot_orderbook:
                bids = spot_orderbook['bids']
                asks = spot_orderbook['asks']
                if bids and asks:
                    best_bid = float(bids[0][0])
                    best_ask = float(asks[0][0])
                    spot_price = (best_bid + best_ask) / 2
            
            if futures_orderbook and 'bids' in futures_orderbook and 'asks' in futures_orderbook:
                bids = futures_orderbook['bids']
                asks = futures_orderbook['asks']
                if bids and asks:
                    best_bid = float(bids[0][0])
                    best_ask = float(asks[0][0])
                    futures_price = (best_bid + best_ask) / 2
            
            return spot_price, futures_price
            
        except Exception as e:
            logger.error(f"Ошибка получения цены для {symbol}: {e}")
            return 0, 0
