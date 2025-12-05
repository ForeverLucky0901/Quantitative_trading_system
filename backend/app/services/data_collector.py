"""
数据采集服务
支持多个数据源：CCXT（加密货币）、Yahoo Finance（股票）、Tushare（A股）
"""
import ccxt
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.market import Kline
from app.core.config import settings


class DataCollector:
    """数据采集器基类 - 支持多个加密货币交易所"""
    
    def __init__(self):
        self.exchanges = {}
        self._init_exchanges()
    
    def _init_exchanges(self):
        """初始化交易所连接"""
        try:
            # ========== 主流加密货币交易所 ==========
            
            # Binance（币安）- 全球最大
            if settings.BINANCE_API_KEY and settings.BINANCE_API_SECRET:
                self.exchanges['binance'] = ccxt.binance({
                    'apiKey': settings.BINANCE_API_KEY,
                    'secret': settings.BINANCE_API_SECRET,
                    'enableRateLimit': True,
                    'options': {'defaultType': 'spot'},
                })
                if settings.BINANCE_TESTNET:
                    self.exchanges['binance'].set_sandbox_mode(True)
                logger.info("Binance exchange initialized")
            
            # OKX（欧易）
            if settings.OKX_API_KEY and settings.OKX_API_SECRET:
                self.exchanges['okx'] = ccxt.okx({
                    'apiKey': settings.OKX_API_KEY,
                    'secret': settings.OKX_API_SECRET,
                    'password': settings.OKX_PASSPHRASE,
                    'enableRateLimit': True,
                })
                if settings.OKX_TESTNET:
                    self.exchanges['okx'].set_sandbox_mode(True)
                logger.info("OKX exchange initialized")
            
            # ========== 免费公开数据交易所（无需API密钥）==========
            
            # Binance 公开数据
            self.exchanges['binance_public'] = ccxt.binance({
                'enableRateLimit': True,
            })
            logger.info("Binance public API initialized")
            
            # Coinbase（美国最大合规交易所）
            self.exchanges['coinbase'] = ccxt.coinbase({
                'enableRateLimit': True,
            })
            logger.info("Coinbase public API initialized")
            
            # Kraken（欧洲老牌交易所）
            self.exchanges['kraken'] = ccxt.kraken({
                'enableRateLimit': True,
            })
            logger.info("Kraken public API initialized")
            
            # Bybit（衍生品交易所）
            self.exchanges['bybit'] = ccxt.bybit({
                'enableRateLimit': True,
            })
            logger.info("Bybit public API initialized")
            
            # Huobi（火币）
            self.exchanges['huobi'] = ccxt.huobi({
                'enableRateLimit': True,
            })
            logger.info("Huobi public API initialized")
            
            # Gate.io
            self.exchanges['gateio'] = ccxt.gateio({
                'enableRateLimit': True,
            })
            logger.info("Gate.io public API initialized")
            
            # KuCoin
            self.exchanges['kucoin'] = ccxt.kucoin({
                'enableRateLimit': True,
            })
            logger.info("KuCoin public API initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize exchanges: {e}")
    
    def get_exchange(self, exchange_name: str) -> Optional[ccxt.Exchange]:
        """获取交易所实例"""
        return self.exchanges.get(exchange_name) or self.exchanges.get(f'{exchange_name}_public')
    
    async def fetch_ohlcv(
        self,
        exchange_name: str,
        symbol: str,
        timeframe: str = '1h',
        since: Optional[datetime] = None,
        limit: int = 500
    ) -> List[Dict[str, Any]]:
        """
        获取K线数据
        
        Args:
            exchange_name: 交易所名称 (binance, okx等)
            symbol: 交易对 (BTC/USDT)
            timeframe: 时间周期 (1m, 5m, 15m, 1h, 4h, 1d)
            since: 开始时间
            limit: 数量限制
        
        Returns:
            K线数据列表
        """
        try:
            exchange = self.get_exchange(exchange_name)
            if not exchange:
                raise ValueError(f"Exchange {exchange_name} not found")
            
            # 转换时间戳
            since_ts = None
            if since:
                since_ts = int(since.timestamp() * 1000)
            
            # 获取OHLCV数据
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since_ts, limit)
            
            # 转换为字典格式
            result = []
            for candle in ohlcv:
                result.append({
                    'timestamp': datetime.fromtimestamp(candle[0] / 1000),
                    'open': float(candle[1]),
                    'high': float(candle[2]),
                    'low': float(candle[3]),
                    'close': float(candle[4]),
                    'volume': float(candle[5])
                })
            
            logger.info(f"Fetched {len(result)} candles for {symbol} from {exchange_name}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to fetch OHLCV: {e}")
            return []
    
    async def fetch_ticker(self, exchange_name: str, symbol: str) -> Dict[str, Any]:
        """
        获取实时行情
        
        Args:
            exchange_name: 交易所名称
            symbol: 交易对
        
        Returns:
            行情数据
        """
        try:
            exchange = self.get_exchange(exchange_name)
            if not exchange:
                raise ValueError(f"Exchange {exchange_name} not found")
            
            ticker = exchange.fetch_ticker(symbol)
            
            return {
                'symbol': symbol,
                'last': ticker.get('last'),
                'bid': ticker.get('bid'),
                'ask': ticker.get('ask'),
                'high': ticker.get('high'),
                'low': ticker.get('low'),
                'volume': ticker.get('baseVolume'),
                'timestamp': datetime.fromtimestamp(ticker['timestamp'] / 1000) if ticker.get('timestamp') else datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Failed to fetch ticker: {e}")
            return {}
    
    async def fetch_all_symbols(self, exchange_name: str) -> List[str]:
        """
        获取所有交易对
        
        Args:
            exchange_name: 交易所名称
        
        Returns:
            交易对列表
        """
        try:
            exchange = self.get_exchange(exchange_name)
            if not exchange:
                raise ValueError(f"Exchange {exchange_name} not found")
            
            markets = exchange.load_markets()
            symbols = [symbol for symbol in markets.keys() if '/USDT' in symbol]
            
            logger.info(f"Fetched {len(symbols)} symbols from {exchange_name}")
            return symbols
            
        except Exception as e:
            logger.error(f"Failed to fetch symbols: {e}")
            return []
    
    async def save_klines_to_db(
        self,
        db: AsyncSession,
        exchange_name: str,
        symbol: str,
        interval: str,
        klines: List[Dict[str, Any]]
    ):
        """
        保存K线数据到数据库
        
        Args:
            db: 数据库会话
            exchange_name: 交易所名称
            symbol: 交易对
            interval: 时间间隔
            klines: K线数据列表
        """
        try:
            for kline_data in klines:
                # 检查是否已存在
                result = await db.execute(
                    select(Kline).where(
                        Kline.exchange == exchange_name,
                        Kline.symbol == symbol,
                        Kline.interval == interval,
                        Kline.timestamp == kline_data['timestamp']
                    )
                )
                existing = result.scalar_one_or_none()
                
                if not existing:
                    kline = Kline(
                        exchange=exchange_name,
                        symbol=symbol,
                        interval=interval,
                        timestamp=kline_data['timestamp'],
                        open=kline_data['open'],
                        high=kline_data['high'],
                        low=kline_data['low'],
                        close=kline_data['close'],
                        volume=kline_data['volume']
                    )
                    db.add(kline)
            
            await db.commit()
            logger.info(f"Saved {len(klines)} klines to database")
            
        except Exception as e:
            logger.error(f"Failed to save klines to database: {e}")
            await db.rollback()
    
    async def collect_historical_data(
        self,
        db: AsyncSession,
        exchange_name: str,
        symbol: str,
        interval: str,
        days: int = 30
    ):
        """
        采集历史数据
        
        Args:
            db: 数据库会话
            exchange_name: 交易所名称
            symbol: 交易对
            interval: 时间间隔
            days: 采集天数
        """
        try:
            end_time = datetime.now()
            start_time = end_time - timedelta(days=days)
            
            logger.info(f"Collecting historical data for {symbol} from {start_time} to {end_time}")
            
            # 分批获取数据（每次最多500条）
            current_time = start_time
            all_klines = []
            
            while current_time < end_time:
                klines = await self.fetch_ohlcv(
                    exchange_name=exchange_name,
                    symbol=symbol,
                    timeframe=interval,
                    since=current_time,
                    limit=500
                )
                
                if not klines:
                    break
                
                all_klines.extend(klines)
                
                # 更新时间
                if klines:
                    current_time = klines[-1]['timestamp'] + timedelta(seconds=1)
                else:
                    break
            
            # 保存到数据库
            if all_klines:
                await self.save_klines_to_db(db, exchange_name, symbol, interval, all_klines)
                logger.info(f"Collected {len(all_klines)} historical klines for {symbol}")
            
        except Exception as e:
            logger.error(f"Failed to collect historical data: {e}")


class YahooFinanceCollector:
    """Yahoo Finance数据采集器 - 支持全球股票市场"""
    
    # 全球市场后缀映射
    MARKET_SUFFIXES = {
        # 亚洲市场
        'US': '',           # 美股：无后缀（如 AAPL）
        'HK': '.HK',        # 港股：.HK（如 0700.HK）
        'CN': '.SS',        # A股上海：.SS（如 600519.SS）
        'SZ': '.SZ',        # A股深圳：.SZ（如 000001.SZ）
        'JP': '.T',         # 日本：.T（如 7203.T 丰田）
        'KS': '.KS',        # 韩国KOSPI：.KS（如 005930.KS 三星）
        'KQ': '.KQ',        # 韩国KOSDAQ：.KQ
        'IN': '.NS',        # 印度NSE：.NS（如 TCS.NS）
        'BO': '.BO',        # 印度BSE：.BO
        'SG': '.SI',        # 新加坡：.SI（如 D05.SI）
        'TW': '.TW',        # 台湾：.TW（如 2330.TW 台积电）
        'TWO': '.TWO',      # 台湾柜买：.TWO
        'TH': '.BK',        # 泰国：.BK
        'MY': '.KL',        # 马来西亚：.KL
        'ID': '.JK',        # 印尼：.JK
        'PH': '.PS',        # 菲律宾：.PS
        'VN': '.VN',        # 越南：.VN
        
        # 欧洲市场
        'UK': '.L',         # 英国：.L（如 HSBA.L 汇丰）
        'DE': '.DE',        # 德国：.DE（如 VOW3.DE 大众）
        'FR': '.PA',        # 法国：.PA（如 MC.PA LVMH）
        'IT': '.MI',        # 意大利：.MI
        'ES': '.MC',        # 西班牙：.MC
        'NL': '.AS',        # 荷兰：.AS
        'CH': '.SW',        # 瑞士：.SW（如 NESN.SW 雀巢）
        'SE': '.ST',        # 瑞典：.ST
        'NO': '.OL',        # 挪威：.OL
        'DK': '.CO',        # 丹麦：.CO
        'FI': '.HE',        # 芬兰：.HE
        'BE': '.BR',        # 比利时：.BR
        'AT': '.VI',        # 奥地利：.VI
        'IE': '.IR',        # 爱尔兰：.IR
        'PT': '.LS',        # 葡萄牙：.LS
        'GR': '.AT',        # 希腊：.AT
        'RU': '.ME',        # 俄罗斯：.ME
        
        # 美洲市场
        'CA': '.TO',        # 加拿大：.TO（如 SHOP.TO Shopify）
        'BR': '.SA',        # 巴西：.SA
        'MX': '.MX',        # 墨西哥：.MX
        'AR': '.BA',        # 阿根廷：.BA
        'CL': '.SN',        # 智利：.SN
        
        # 大洋洲市场
        'AU': '.AX',        # 澳大利亚：.AX（如 BHP.AX 必和必拓）
        'NZ': '.NZ',        # 新西兰：.NZ
        
        # 中东市场
        'SA': '.SAU',       # 沙特：.SAU
        'AE': '.AD',        # 阿联酋：.AD
        'IL': '.TA',        # 以色列：.TA
        'TR': '.IS',        # 土耳其：.IS
        
        # 非洲市场
        'ZA': '.JO',        # 南非：.JO
        'EG': '.CA',        # 埃及：.CA
    }
    
    # 市场名称映射
    MARKET_NAMES = {
        # 亚洲
        'US': '美国',
        'HK': '香港',
        'CN': 'A股上海',
        'SZ': 'A股深圳',
        'JP': '日本',
        'KS': '韩国KOSPI',
        'KQ': '韩国KOSDAQ',
        'IN': '印度NSE',
        'BO': '印度BSE',
        'SG': '新加坡',
        'TW': '台湾',
        'TWO': '台湾柜买',
        'TH': '泰国',
        'MY': '马来西亚',
        'ID': '印尼',
        'PH': '菲律宾',
        'VN': '越南',
        
        # 欧洲
        'UK': '英国',
        'DE': '德国',
        'FR': '法国',
        'IT': '意大利',
        'ES': '西班牙',
        'NL': '荷兰',
        'CH': '瑞士',
        'SE': '瑞典',
        'NO': '挪威',
        'DK': '丹麦',
        'FI': '芬兰',
        'BE': '比利时',
        'AT': '奥地利',
        'IE': '爱尔兰',
        'PT': '葡萄牙',
        'GR': '希腊',
        'RU': '俄罗斯',
        
        # 美洲
        'CA': '加拿大',
        'BR': '巴西',
        'MX': '墨西哥',
        'AR': '阿根廷',
        'CL': '智利',
        
        # 大洋洲
        'AU': '澳大利亚',
        'NZ': '新西兰',
        
        # 中东
        'SA': '沙特',
        'AE': '阿联酋',
        'IL': '以色列',
        'TR': '土耳其',
        
        # 非洲
        'ZA': '南非',
        'EG': '埃及',
    }
    
    def __init__(self):
        try:
            import yfinance as yf
            self.yf = yf
            logger.info("Yahoo Finance initialized - supports global markets")
        except ImportError:
            logger.warning("yfinance not installed. Run: pip install yfinance")
            self.yf = None
    
    def format_symbol(self, symbol: str, market: str = 'US') -> str:
        """
        格式化股票代码
        
        Args:
            symbol: 原始股票代码
            market: 市场代码 (US, HK, CN, SZ, SG等)
        
        Returns:
            格式化后的代码
        """
        suffix = self.MARKET_SUFFIXES.get(market, '')
        if suffix and not symbol.endswith(suffix):
            return f"{symbol}{suffix}"
        return symbol
    
    async def fetch_stock_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = '1d',
        market: str = 'US'
    ) -> pd.DataFrame:
        """
        获取股票数据
        
        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            interval: 时间间隔 (1m, 5m, 1h, 1d, 1wk, 1mo)
            market: 市场代码 (US, HK, CN, SZ, SG等)
        
        Returns:
            DataFrame
        
        Examples:
            # 美股
            fetch_stock_data('AAPL', ..., market='US')
            
            # 港股
            fetch_stock_data('0700', ..., market='HK')  # 腾讯
            
            # A股
            fetch_stock_data('600519', ..., market='CN')  # 贵州茅台
            fetch_stock_data('000001', ..., market='SZ')  # 平安银行
            
            # 新加坡股
            fetch_stock_data('D05', ..., market='SG')  # DBS银行
        """
        if not self.yf:
            logger.error("yfinance not available")
            return pd.DataFrame()
        
        try:
            # 格式化股票代码
            formatted_symbol = self.format_symbol(symbol, market)
            
            ticker = self.yf.Ticker(formatted_symbol)
            df = ticker.history(
                start=start_date,
                end=end_date,
                interval=interval
            )
            
            logger.info(f"Fetched {len(df)} rows for {formatted_symbol} ({market}) from Yahoo Finance")
            return df
            
        except Exception as e:
            logger.error(f"Failed to fetch stock data for {symbol}: {e}")
            return pd.DataFrame()
    
    async def fetch_multiple_stocks(
        self,
        symbols: List[str],
        start_date: datetime,
        end_date: datetime,
        market: str = 'US'
    ) -> Dict[str, pd.DataFrame]:
        """
        批量获取多个股票数据
        
        Args:
            symbols: 股票代码列表
            start_date: 开始日期
            end_date: 结束日期
            market: 市场代码
        
        Returns:
            字典，key为股票代码，value为DataFrame
        """
        result = {}
        for symbol in symbols:
            df = await self.fetch_stock_data(symbol, start_date, end_date, market=market)
            if not df.empty:
                result[symbol] = df
        return result
    
    async def get_stock_info(self, symbol: str, market: str = 'US') -> Dict[str, Any]:
        """
        获取股票基本信息
        
        Args:
            symbol: 股票代码
            market: 市场代码
        
        Returns:
            股票信息字典
        """
        if not self.yf:
            return {}
        
        try:
            formatted_symbol = self.format_symbol(symbol, market)
            ticker = self.yf.Ticker(formatted_symbol)
            info = ticker.info
            
            return {
                'symbol': formatted_symbol,
                'name': info.get('longName', ''),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'market_cap': info.get('marketCap', 0),
                'currency': info.get('currency', ''),
                'exchange': info.get('exchange', ''),
            }
        except Exception as e:
            logger.error(f"Failed to get stock info: {e}")
            return {}


class TushareCollector:
    """Tushare数据采集器（A股）"""
    
    def __init__(self, token: str = None):
        try:
            import tushare as ts
            self.ts = ts
            if token:
                ts.set_token(token)
                self.pro = ts.pro_api()
            else:
                logger.warning("Tushare token not provided")
                self.pro = None
        except ImportError:
            logger.warning("tushare not installed. Run: pip install tushare")
            self.ts = None
            self.pro = None
    
    async def fetch_stock_daily(
        self,
        ts_code: str,
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """
        获取A股日线数据
        
        Args:
            ts_code: 股票代码 (如 000001.SZ)
            start_date: 开始日期 (YYYYMMDD)
            end_date: 结束日期 (YYYYMMDD)
        
        Returns:
            DataFrame
        """
        if not self.pro:
            logger.error("Tushare not available")
            return pd.DataFrame()
        
        try:
            df = self.pro.daily(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date
            )
            
            logger.info(f"Fetched {len(df)} rows for {ts_code} from Tushare")
            return df
            
        except Exception as e:
            logger.error(f"Failed to fetch stock data: {e}")
            return pd.DataFrame()


# 全局数据采集器实例
data_collector = DataCollector()
