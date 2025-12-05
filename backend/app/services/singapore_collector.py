"""
新加坡股市数据采集器
"""
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from loguru import logger


class SingaporeStockCollector:
    """
    新加坡股市数据采集器
    
    主要交易所：新加坡交易所 (SGX)
    数据源：Yahoo Finance
    """
    
    # 新加坡主要股票列表
    POPULAR_STOCKS = {
        'D05.SI': 'DBS Group Holdings',           # 星展银行
        'O39.SI': 'Oversea-Chinese Banking Corp',  # 华侨银行
        'U11.SI': 'United Overseas Bank',          # 大华银行
        'Z74.SI': 'Singapore Telecommunications',  # 新加坡电信
        'C6L.SI': 'Singapore Airlines',            # 新加坡航空
        'BN4.SI': 'Keppel Corporation',            # 吉宝集团
        'C52.SI': 'ComfortDelGro Corporation',     # 康福德高企业
        'S68.SI': 'Singapore Exchange',            # 新加坡交易所
        'C07.SI': 'Jardine Cycle & Carriage',      # 怡和合发
        'V03.SI': 'Venture Corporation',           # 伟创力
    }
    
    # STI成分股（海峡时报指数）
    STI_COMPONENTS = [
        'D05.SI', 'O39.SI', 'U11.SI', 'Z74.SI', 'C6L.SI',
        'BN4.SI', 'C52.SI', 'S68.SI', 'C07.SI', 'V03.SI',
        'Y92.SI', 'C38U.SI', 'BS6.SI', 'F34.SI', 'N2IU.SI',
        'ME8U.SI', 'A17U.SI', 'J36.SI', 'C09.SI', 'H78.SI',
    ]
    
    def __init__(self):
        """初始化新加坡股市采集器"""
        try:
            import yfinance as yf
            self.yf = yf
            logger.info("Singapore Stock Collector initialized")
        except ImportError:
            logger.warning("yfinance not installed")
            self.yf = None
    
    async def fetch_stock_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = '1d'
    ) -> pd.DataFrame:
        """
        获取新加坡股票数据
        
        Args:
            symbol: 股票代码（如 D05.SI）
            start_date: 开始日期
            end_date: 结束日期
            interval: 时间间隔
        
        Returns:
            DataFrame
        """
        if not self.yf:
            return pd.DataFrame()
        
        try:
            # 确保有 .SI 后缀
            if not symbol.endswith('.SI'):
                symbol = f"{symbol}.SI"
            
            ticker = self.yf.Ticker(symbol)
            df = ticker.history(
                start=start_date,
                end=end_date,
                interval=interval
            )
            
            logger.info(f"Fetched {len(df)} rows for {symbol} (Singapore)")
            return df
            
        except Exception as e:
            logger.error(f"Failed to fetch Singapore stock data: {e}")
            return pd.DataFrame()
    
    async def get_sti_index(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> pd.DataFrame:
        """
        获取海峡时报指数（STI）数据
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            DataFrame
        """
        return await self.fetch_stock_data('^STI', start_date, end_date)
    
    def get_popular_stocks(self) -> Dict[str, str]:
        """获取热门股票列表"""
        return self.POPULAR_STOCKS
    
    def get_sti_components(self) -> List[str]:
        """获取STI成分股列表"""
        return self.STI_COMPONENTS
