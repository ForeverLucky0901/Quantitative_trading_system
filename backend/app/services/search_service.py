"""
实时搜索服务 - 获取最新市场信息
"""
import aiohttp
from typing import List, Dict, Any
from loguru import logger


class SearchService:
    """实时搜索服务"""
    
    def __init__(self):
        self.session = None
    
    async def search_news(self, query: str, limit: int = 5) -> List[str]:
        """
        搜索最新新闻
        
        Args:
            query: 搜索关键词
            limit: 返回数量
        
        Returns:
            新闻列表
        """
        try:
            # 使用免费的新闻API
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": query,
                "sortBy": "publishedAt",
                "pageSize": limit,
                "language": "zh",
                "apiKey": "your-newsapi-key"  # 需要申请
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = data.get("articles", [])
                        return [
                            f"{article['title']} - {article['publishedAt']}"
                            for article in articles
                        ]
            
            return []
            
        except Exception as e:
            logger.error(f"Search news failed: {e}")
            return []
    
    async def search_crypto_news(self, symbol: str) -> List[str]:
        """
        搜索加密货币新闻
        
        使用CoinGecko等免费API
        """
        try:
            # CoinGecko API（免费，无需密钥）
            coin_id = symbol.split("/")[0].lower()
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        news = []
                        
                        # 获取市场情绪
                        sentiment = data.get("sentiment_votes_up_percentage", 0)
                        news.append(f"市场情绪：{sentiment}%看涨")
                        
                        # 获取价格变化
                        price_change = data.get("market_data", {}).get("price_change_percentage_24h", 0)
                        news.append(f"24小时涨跌：{price_change:.2f}%")
                        
                        # 获取市值排名
                        rank = data.get("market_cap_rank", 0)
                        news.append(f"市值排名：第{rank}位")
                        
                        return news
            
            return []
            
        except Exception as e:
            logger.error(f"Search crypto news failed: {e}")
            return []
    
    async def get_market_sentiment(self, symbol: str) -> Dict[str, Any]:
        """
        获取市场情绪指标
        
        使用Fear & Greed Index等
        """
        try:
            # Alternative.me Fear & Greed Index（免费）
            url = "https://api.alternative.me/fng/"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        fng_data = data.get("data", [{}])[0]
                        
                        return {
                            "fear_greed_index": fng_data.get("value"),
                            "classification": fng_data.get("value_classification"),
                            "timestamp": fng_data.get("timestamp")
                        }
            
            return {}
            
        except Exception as e:
            logger.error(f"Get market sentiment failed: {e}")
            return {}


# 全局实例
search_service = SearchService()
