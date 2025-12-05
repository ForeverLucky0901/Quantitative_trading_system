"""
多市场数据API接口
支持：加密货币、美股、港股、A股、新加坡股
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime, timedelta

from app.core.database import get_db
from app.services.data_collector import data_collector, YahooFinanceCollector, TushareCollector
from app.services.singapore_collector import SingaporeStockCollector
from app.services.global_markets import GLOBAL_POPULAR_STOCKS, MARKETS_BY_REGION, MAJOR_INDICES

router = APIRouter()

# 初始化采集器
yahoo_collector = YahooFinanceCollector()
singapore_collector = SingaporeStockCollector()


@router.get("/crypto/exchanges")
async def list_crypto_exchanges():
    """获取支持的加密货币交易所"""
    return {
        "exchanges": {
            "binance_public": {
                "name": "Binance（币安）",
                "description": "全球最大的加密货币交易所",
                "requires_api_key": False,
                "supported_markets": ["spot", "futures", "margin"]
            },
            "coinbase": {
                "name": "Coinbase",
                "description": "美国最大的合规交易所",
                "requires_api_key": False,
                "supported_markets": ["spot"]
            },
            "kraken": {
                "name": "Kraken",
                "description": "欧洲老牌交易所",
                "requires_api_key": False,
                "supported_markets": ["spot", "futures"]
            },
            "bybit": {
                "name": "Bybit",
                "description": "衍生品交易所",
                "requires_api_key": False,
                "supported_markets": ["spot", "futures"]
            },
            "okx": {
                "name": "OKX（欧易）",
                "description": "全球领先的数字资产交易所",
                "requires_api_key": False,
                "supported_markets": ["spot", "futures", "options"]
            },
            "huobi": {
                "name": "Huobi（火币）",
                "description": "老牌数字资产交易所",
                "requires_api_key": False,
                "supported_markets": ["spot", "futures"]
            },
            "gateio": {
                "name": "Gate.io",
                "description": "支持大量币种的交易所",
                "requires_api_key": False,
                "supported_markets": ["spot", "futures"]
            },
            "kucoin": {
                "name": "KuCoin",
                "description": "人民的交易所",
                "requires_api_key": False,
                "supported_markets": ["spot", "futures"]
            }
        },
        "total": 8
    }


@router.get("/crypto/symbols")
async def list_crypto_symbols(
    exchange: str = Query("binance_public", description="交易所名称")
):
    """获取加密货币交易对列表"""
    symbols = await data_collector.fetch_all_symbols(exchange)
    return {
        "exchange": exchange,
        "symbols": symbols[:100],  # 限制返回数量
        "total": len(symbols)
    }


@router.get("/crypto/ticker")
async def get_crypto_ticker(
    exchange: str = Query(..., description="交易所名称"),
    symbol: str = Query(..., description="交易对，如 BTC/USDT")
):
    """获取加密货币实时行情"""
    ticker = await data_collector.fetch_ticker(exchange, symbol)
    return ticker


@router.get("/stocks/us")
async def get_us_stocks():
    """获取美股热门股票列表"""
    return {
        "market": "US",
        "popular_stocks": {
            "tech": {
                "AAPL": "Apple Inc.",
                "MSFT": "Microsoft Corporation",
                "GOOGL": "Alphabet Inc.",
                "AMZN": "Amazon.com Inc.",
                "META": "Meta Platforms Inc.",
                "NVDA": "NVIDIA Corporation",
                "TSLA": "Tesla Inc.",
            },
            "finance": {
                "JPM": "JPMorgan Chase & Co.",
                "BAC": "Bank of America Corp",
                "WFC": "Wells Fargo & Company",
                "GS": "Goldman Sachs Group Inc.",
            },
            "indices": {
                "^GSPC": "S&P 500",
                "^DJI": "Dow Jones Industrial Average",
                "^IXIC": "NASDAQ Composite",
            }
        }
    }


@router.get("/stocks/hk")
async def get_hk_stocks():
    """获取港股热门股票列表"""
    return {
        "market": "HK",
        "popular_stocks": {
            "tech": {
                "0700.HK": "腾讯控股",
                "9988.HK": "阿里巴巴",
                "1810.HK": "小米集团",
                "9618.HK": "京东集团",
                "3690.HK": "美团",
            },
            "finance": {
                "0005.HK": "汇丰控股",
                "0939.HK": "建设银行",
                "1398.HK": "工商银行",
                "3988.HK": "中国银行",
            },
            "property": {
                "0001.HK": "长和",
                "0002.HK": "中电控股",
                "0003.HK": "香港中华煤气",
            },
            "indices": {
                "^HSI": "恒生指数",
                "^HSCE": "恒生中国企业指数",
            }
        }
    }


@router.get("/stocks/cn")
async def get_cn_stocks():
    """获取A股热门股票列表"""
    return {
        "market": "CN",
        "popular_stocks": {
            "shanghai": {
                "600519.SS": "贵州茅台",
                "600036.SS": "招商银行",
                "601318.SS": "中国平安",
                "600887.SS": "伊利股份",
                "601888.SS": "中国中免",
            },
            "shenzhen": {
                "000001.SZ": "平安银行",
                "000002.SZ": "万科A",
                "000858.SZ": "五粮液",
                "000333.SZ": "美的集团",
                "002594.SZ": "比亚迪",
            },
            "indices": {
                "000001.SS": "上证指数",
                "399001.SZ": "深证成指",
                "399006.SZ": "创业板指",
            }
        }
    }


@router.get("/stocks/sg")
async def get_sg_stocks():
    """获取新加坡股票列表"""
    popular = singapore_collector.get_popular_stocks()
    sti_components = singapore_collector.get_sti_components()
    
    return {
        "market": "SG",
        "popular_stocks": popular,
        "sti_components": sti_components,
        "indices": {
            "^STI": "海峡时报指数 (Straits Times Index)"
        }
    }


@router.get("/stocks/data")
async def get_stock_data(
    symbol: str = Query(..., description="股票代码"),
    market: str = Query("US", description="市场：US, HK, CN, SZ, SG"),
    start_date: str = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: str = Query(None, description="结束日期 YYYY-MM-DD"),
    interval: str = Query("1d", description="时间间隔：1d, 1wk, 1mo")
):
    """
    获取股票历史数据
    
    支持市场：
    - US: 美股（如 AAPL）
    - HK: 港股（如 0700）
    - CN: A股上海（如 600519）
    - SZ: A股深圳（如 000001）
    - SG: 新加坡（如 D05）
    """
    # 设置默认日期
    if not end_date:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    if not start_date:
        start_date = end_date - timedelta(days=30)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    
    # 根据市场选择采集器
    if market == 'SG':
        df = await singapore_collector.fetch_stock_data(symbol, start_date, end_date, interval)
    else:
        df = await yahoo_collector.fetch_stock_data(symbol, start_date, end_date, interval, market)
    
    if df.empty:
        return {
            "symbol": symbol,
            "market": market,
            "data": [],
            "message": "No data available"
        }
    
    # 转换为JSON格式
    data = []
    for index, row in df.iterrows():
        data.append({
            "date": index.strftime('%Y-%m-%d'),
            "open": float(row['Open']),
            "high": float(row['High']),
            "low": float(row['Low']),
            "close": float(row['Close']),
            "volume": int(row['Volume'])
        })
    
    return {
        "symbol": symbol,
        "market": market,
        "interval": interval,
        "data": data,
        "count": len(data)
    }


@router.get("/markets/summary")
async def get_markets_summary():
    """获取所有市场概览"""
    return {
        "crypto": {
            "name": "加密货币市场",
            "exchanges": 8,
            "description": "支持Binance、Coinbase、Kraken等主流交易所"
        },
        "stock_markets": {
            "total_markets": len(GLOBAL_POPULAR_STOCKS) + 5,  # 包含已有的市场
            "regions": MARKETS_BY_REGION,
            "description": "支持全球50+个股票市场"
        },
        "major_indices": {
            "total": len(MAJOR_INDICES),
            "description": "全球主要股票指数"
        }
    }


@router.get("/markets/all")
async def get_all_markets():
    """获取所有支持的市场列表"""
    markets = []
    
    # 添加已有市场的详细信息
    for market_code, market_data in GLOBAL_POPULAR_STOCKS.items():
        markets.append({
            "code": market_code,
            "name": market_data['name'],
            "exchange": market_data['exchange'],
            "index": market_data.get('index', ''),
            "stocks_count": len(market_data['stocks'])
        })
    
    # 按地区分组
    markets_by_region = {}
    for region, codes in MARKETS_BY_REGION.items():
        markets_by_region[region] = [
            {
                "code": code,
                "name": GLOBAL_POPULAR_STOCKS.get(code, {}).get('name', code),
                "stocks_count": len(GLOBAL_POPULAR_STOCKS.get(code, {}).get('stocks', {}))
            }
            for code in codes if code in GLOBAL_POPULAR_STOCKS or code in ['HK', 'CN', 'SZ', 'SG', 'US']
        ]
    
    return {
        "markets": markets,
        "by_region": markets_by_region,
        "total": len(markets)
    }


@router.get("/markets/indices")
async def get_major_indices():
    """获取全球主要指数"""
    return {
        "indices": MAJOR_INDICES,
        "total": len(MAJOR_INDICES)
    }


@router.get("/markets/{market_code}")
async def get_market_detail(market_code: str):
    """获取指定市场的详细信息"""
    market_code = market_code.upper()
    
    # 检查特殊市场
    if market_code == 'US':
        return await get_us_stocks()
    elif market_code == 'HK':
        return await get_hk_stocks()
    elif market_code in ['CN', 'SZ']:
        return await get_cn_stocks()
    elif market_code == 'SG':
        return await get_sg_stocks()
    
    # 检查全球市场
    if market_code in GLOBAL_POPULAR_STOCKS:
        market_data = GLOBAL_POPULAR_STOCKS[market_code]
        return {
            "market": market_code,
            "name": market_data['name'],
            "exchange": market_data['exchange'],
            "index": market_data.get('index', ''),
            "popular_stocks": market_data['stocks']
        }
    
    return {
        "error": "Market not found",
        "message": f"Market code '{market_code}' is not supported"
    }
