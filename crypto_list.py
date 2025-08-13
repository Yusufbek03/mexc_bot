#!/usr/bin/env python3
"""
Полный список криптовалют для отслеживания спредов
"""

# Расширенный список криптовалют
FULL_CRYPTO_LIST = {
    # Major Cryptocurrencies
    'BTC': {'spot': 45000.0, 'futures': 44500.0},
    'ETH': {'spot': 2800.0, 'futures': 2750.0},
    'BNB': {'spot': 320.0, 'futures': 315.0},
    'SOL': {'spot': 95.0, 'futures': 88.0},
    'XRP': {'spot': 0.52, 'futures': 0.48},
    'ADA': {'spot': 0.45, 'futures': 0.42},
    'AVAX': {'spot': 35.0, 'futures': 32.5},
    'DOGE': {'spot': 0.085, 'futures': 0.082},
    'DOT': {'spot': 6.8, 'futures': 6.2},
    'MATIC': {'spot': 0.85, 'futures': 0.78},
    
    # Popular Altcoins
    'LINK': {'spot': 15.2, 'futures': 14.1},
    'UNI': {'spot': 7.2, 'futures': 6.8},
    'ATOM': {'spot': 8.5, 'futures': 7.9},
    'LTC': {'spot': 68.0, 'futures': 65.0},
    'ETC': {'spot': 25.0, 'futures': 23.5},
    'XLM': {'spot': 0.12, 'futures': 0.11},
    'BCH': {'spot': 240.0, 'futures': 225.0},
    'FIL': {'spot': 4.2, 'futures': 3.9},
    'VET': {'spot': 0.025, 'futures': 0.023},
    'ICP': {'spot': 12.5, 'futures': 11.8},
    
    # DeFi & Gaming
    'AAVE': {'spot': 280.0, 'futures': 265.0},
    'SUSHI': {'spot': 1.2, 'futures': 1.1},
    'COMP': {'spot': 65.0, 'futures': 61.0},
    'YFI': {'spot': 8500.0, 'futures': 8000.0},
    'CRV': {'spot': 0.65, 'futures': 0.60},
    '1INCH': {'spot': 0.45, 'futures': 0.42},
    'ZRX': {'spot': 0.35, 'futures': 0.32},
    'BAL': {'spot': 3.8, 'futures': 3.5},
    'REN': {'spot': 0.085, 'futures': 0.078},
    'KNC': {'spot': 0.75, 'futures': 0.68},
    
    # Layer 1 & Smart Contracts
    'NEAR': {'spot': 3.2, 'futures': 2.9},
    'FTM': {'spot': 0.45, 'futures': 0.41},
    'ALGO': {'spot': 0.18, 'futures': 0.16},
    'HBAR': {'spot': 0.065, 'futures': 0.060},
    'THETA': {'spot': 1.8, 'futures': 1.6},
    'XTZ': {'spot': 0.95, 'futures': 0.88},
    'EOS': {'spot': 0.65, 'futures': 0.60},
    'TRX': {'spot': 0.085, 'futures': 0.078},
    'XMR': {'spot': 165.0, 'futures': 155.0},
    'DASH': {'spot': 28.0, 'futures': 26.0},
    
    # Meme & Social
    'SHIB': {'spot': 0.0000085, 'futures': 0.0000078},
    'PEPE': {'spot': 0.0000012, 'futures': 0.0000011},
    'FLOKI': {'spot': 0.000025, 'futures': 0.000022},
    'BONK': {'spot': 0.000035, 'futures': 0.000032},
    'WIF': {'spot': 2.8, 'futures': 2.5},
    'BOME': {'spot': 0.000085, 'futures': 0.000078},
    'MYRO': {'spot': 0.00045, 'futures': 0.00041},
    'POPCAT': {'spot': 0.00065, 'futures': 0.00058},
    'BOOK': {'spot': 0.00095, 'futures': 0.00088},
    'TURBO': {'spot': 0.00015, 'futures': 0.00013},
    
    # AI & Tech
    'FET': {'spot': 0.85, 'futures': 0.78},
    'OCEAN': {'spot': 0.65, 'futures': 0.58},
    'AGIX': {'spot': 0.45, 'futures': 0.41},
    'RNDR': {'spot': 7.2, 'futures': 6.8},
    'GRT': {'spot': 0.18, 'futures': 0.16},
    'BAND': {'spot': 1.8, 'futures': 1.6},
    'API3': {'spot': 2.5, 'futures': 2.2},
    'UMA': {'spot': 3.8, 'futures': 3.5},
    'PENDLE': {'spot': 4.2, 'futures': 3.9},
    'JUP': {'spot': 0.85, 'futures': 0.78},
    
    # Gaming & Metaverse
    'AXS': {'spot': 6.8, 'futures': 6.2},
    'SAND': {'spot': 0.45, 'futures': 0.41},
    'MANA': {'spot': 0.35, 'futures': 0.32},
    'ENJ': {'spot': 0.28, 'futures': 0.25},
    'GALA': {'spot': 0.025, 'futures': 0.022},
    'CHZ': {'spot': 0.085, 'futures': 0.078},
    'HOT': {'spot': 0.00085, 'futures': 0.00078},
    'WIN': {'spot': 0.00045, 'futures': 0.00041},
    'BTT': {'spot': 0.00000085, 'futures': 0.00000078},
    'STMX': {'spot': 0.0085, 'futures': 0.0078},
    
    # Privacy & Security
    'ZEC': {'spot': 22.0, 'futures': 20.0},
    'ZEN': {'spot': 8.5, 'futures': 7.8},
    'SCRT': {'spot': 0.45, 'futures': 0.41},
    'BEAM': {'spot': 0.025, 'futures': 0.022},
    'GRIN': {'spot': 0.085, 'futures': 0.078},
    'MWC': {'spot': 0.45, 'futures': 0.41},
    'PIVX': {'spot': 0.35, 'futures': 0.32},
    'FROST': {'spot': 0.025, 'futures': 0.022},
    'MONERO': {'spot': 165.0, 'futures': 155.0},
    'VERGE': {'spot': 0.0085, 'futures': 0.0078},
    
    # Exchange & Utility
    'HT': {'spot': 2.8, 'futures': 2.5},
    'OKB': {'spot': 45.0, 'futures': 42.0},
    'LEO': {'spot': 3.8, 'futures': 3.5},
    'CRO': {'spot': 0.085, 'futures': 0.078},
    'FTT': {'spot': 1.2, 'futures': 1.1},
    'KCS': {'spot': 8.5, 'futures': 7.8},
    'GT': {'spot': 4.2, 'futures': 3.9},
    'MX': {'spot': 0.85, 'futures': 0.78},
    'QTUM': {'spot': 3.2, 'futures': 2.9},
    'NEO': {'spot': 12.5, 'futures': 11.8},
    
    # Emerging & New
    'SUI': {'spot': 1.2, 'futures': 1.1},
    'APT': {'spot': 8.5, 'futures': 7.8},
    'ARB': {'spot': 1.8, 'futures': 1.6},
    'OP': {'spot': 2.5, 'futures': 2.2},
    'STRK': {'spot': 0.85, 'futures': 0.78},
    'MANTLE': {'spot': 0.65, 'futures': 0.58},
    'SEI': {'spot': 0.45, 'futures': 0.41},
    'PYTH': {'spot': 0.35, 'futures': 0.32},
    'WLD': {'spot': 2.8, 'futures': 2.5},
    'BLUR': {'spot': 0.45, 'futures': 0.41},
    
    # Additional Popular
    'INJ': {'spot': 8.5, 'futures': 7.8},
    'IMX': {'spot': 2.8, 'futures': 2.5},
    'TIA': {'spot': 6.8, 'futures': 6.2},
    'JTO': {'spot': 2.5, 'futures': 2.2},
    'BIGTIME': {'spot': 0.25, 'futures': 0.22},
    'MEME': {'spot': 0.025, 'futures': 0.022},
    'ORDI': {'spot': 45.0, 'futures': 42.0},
    'SATS': {'spot': 0.00000085, 'futures': 0.00000078},
    'RATS': {'spot': 0.00000045, 'futures': 0.00000041},
    'DOG': {'spot': 0.000085, 'futures': 0.000078},
    
    # More Altcoins
    'KAS': {'spot': 0.085, 'futures': 0.078},
    'TAO': {'spot': 285.0, 'futures': 265.0},
    'RUNE': {'spot': 4.2, 'futures': 3.9},
    'THOR': {'spot': 0.45, 'futures': 0.41},
    'COSMOS': {'spot': 8.5, 'futures': 7.8},
    'POLKADOT': {'spot': 6.8, 'futures': 6.2},
    'CARDANO': {'spot': 0.45, 'futures': 0.42},
    'POLYGON': {'spot': 0.85, 'futures': 0.78},
    'CHAINLINK': {'spot': 15.2, 'futures': 14.1},
    'UNISWAP': {'spot': 7.2, 'futures': 6.8},
    
    # DeFi Protocols
    'COMPOUND': {'spot': 65.0, 'futures': 61.0},
    'YEARNFINANCE': {'spot': 8500.0, 'futures': 8000.0},
    'CURVE': {'spot': 0.65, 'futures': 0.60},
    'ZEROX': {'spot': 0.35, 'futures': 0.32},
    'BALANCER': {'spot': 3.8, 'futures': 3.5},
    'KYBER': {'spot': 0.75, 'futures': 0.68},
    
    # Layer 2 & Scaling
    'ARBITRUM': {'spot': 1.8, 'futures': 1.6},
    'OPTIMISM': {'spot': 2.5, 'futures': 2.2},
    'IMMUTABLE': {'spot': 2.8, 'futures': 2.5},
    'STARKNET': {'spot': 0.85, 'futures': 0.78},
    'BASE': {'spot': 0.45, 'futures': 0.41},
    'LINEA': {'spot': 0.35, 'futures': 0.32},
    'SCROLL': {'spot': 0.25, 'futures': 0.22},
    
    # Meme Coins Extended
    'SHIBA': {'spot': 0.0000085, 'futures': 0.0000078},
    'DOGECOIN': {'spot': 0.085, 'futures': 0.082},
    'BOME': {'spot': 0.000085, 'futures': 0.000078},
    'MYRO': {'spot': 0.00045, 'futures': 0.00041},
    'POPCAT': {'spot': 0.00065, 'futures': 0.00058},
    'BOOK': {'spot': 0.00095, 'futures': 0.00088},
    'TURBO': {'spot': 0.00015, 'futures': 0.00013},
    
    # AI & Machine Learning
    'FETCH': {'spot': 0.85, 'futures': 0.78},
    'SINGULARITYNET': {'spot': 0.45, 'futures': 0.41},
    'RENDER': {'spot': 7.2, 'futures': 6.8},
    'THEGRAPH': {'spot': 0.18, 'futures': 0.16},
    'API3': {'spot': 2.5, 'futures': 2.2},
    'UMA': {'spot': 3.8, 'futures': 3.5},
    'PENDLE': {'spot': 4.2, 'futures': 3.9},
    'JUPITER': {'spot': 0.85, 'futures': 0.78},
    
    # Gaming & Metaverse Extended
    'AXIE': {'spot': 6.8, 'futures': 6.2},
    'DECENTRALAND': {'spot': 0.35, 'futures': 0.32},
    'ENJIN': {'spot': 0.28, 'futures': 0.25},
    'CHILIZ': {'spot': 0.085, 'futures': 0.078},
    'BITTORRENT': {'spot': 0.00000085, 'futures': 0.00000078},
    'STORM': {'spot': 0.0085, 'futures': 0.0078},
    
    # Privacy & Security Extended
    'ZCASH': {'spot': 22.0, 'futures': 20.0},
    'HORIZEN': {'spot': 8.5, 'futures': 7.8},
    'SECRET': {'spot': 0.45, 'futures': 0.41},
    'MIMBLEWIMBLE': {'spot': 0.45, 'futures': 0.41},
    
    # Exchange & Utility Extended
    'HUOBI': {'spot': 2.8, 'futures': 2.5},
    'UNUS': {'spot': 3.8, 'futures': 3.5},
    'CRYPTOCOM': {'spot': 0.085, 'futures': 0.078},
    'FTX': {'spot': 1.2, 'futures': 1.1},
    'KUCOIN': {'spot': 8.5, 'futures': 7.8},
    'GATE': {'spot': 4.2, 'futures': 3.9},
    
    # Emerging & New Extended
    'APTOS': {'spot': 8.5, 'futures': 7.8},
    'WORLDCOIN': {'spot': 2.8, 'futures': 2.5}
}

def get_crypto_count():
    """Получить количество криптовалют в списке"""
    return len(FULL_CRYPTO_LIST)

def get_crypto_names():
    """Получить только названия криптовалют"""
    return list(FULL_CRYPTO_LIST.keys())

if __name__ == "__main__":
    print(f"📊 Всего криптовалют в списке: {get_crypto_count()}")
    print(f"🔍 Примеры криптовалют:")
    for i, (name, data) in enumerate(list(FULL_CRYPTO_LIST.items())[:20]):
        print(f"  {i+1}. {name} - Спот: {data['spot']}, Фьючерс: {data['futures']}")
