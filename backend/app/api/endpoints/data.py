"""
数据采集API接口
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime, timedelta

from app.core.database import get_db
from app.services.data_collector import data_collector

router = APIRouter()


@router.get("/exchanges")
async def list_exchanges():
    """获取支持的交易所列表"""
    return {
        "exchanges": list(data_collector.exchanges.keys()),
        "description": {
            "binance": "币安交易所",
            "binance_public": "币安公开数据（无需API密钥）",
            "okx": "OKX交易所"
        }
    }


@router.get("/symbols")
async def list_symbols(
    exchange: str = Query(..., description="交易所名称")
):
    """获取交易所支持的交易对"""
    symbols = await data_collector.fetch_all_symbols(exchange)
    return {
        "exchange": exchange,
        "symbols": symbols,
        "count": len(symbols)
    }


@router.get("/ticker")
async def get_ticker(
    exchange: str = Query(..., description="交易所名称"),
    symbol: str = Query(..., description="交易对，如 BTC/USDT")
):
    """获取实时行情"""
    ticker = await data_collector.fetch_ticker(exchange, symbol)
    return ticker


@router.get("/klines")
async def get_klines(
    exchange: str = Query(..., description="交易所名称"),
    symbol: str = Query(..., description="交易对，如 BTC/USDT"),
    interval: str = Query("1h", description="时间周期：1m, 5m, 15m, 1h, 4h, 1d"),
    limit: int = Query(100, le=1000, description="数量限制")
):
    """获取K线数据"""
    klines = await data_collector.fetch_ohlcv(
        exchange_name=exchange,
        symbol=symbol,
        timeframe=interval,
        limit=limit
    )
    return {
        "exchange": exchange,
        "symbol": symbol,
        "interval": interval,
        "data": klines
    }


@router.post("/collect")
async def collect_historical_data(
    exchange: str = Query(..., description="交易所名称"),
    symbol: str = Query(..., description="交易对，如 BTC/USDT"),
    interval: str = Query("1h", description="时间周期"),
    days: int = Query(30, le=365, description="采集天数"),
    db: AsyncSession = Depends(get_db)
):
    """
    采集历史数据并保存到数据库
    
    这是一个异步任务，会在后台执行数据采集
    """
    try:
        await data_collector.collect_historical_data(
            db=db,
            exchange_name=exchange,
            symbol=symbol,
            interval=interval,
            days=days
        )
        
        return {
            "status": "success",
            "message": f"Started collecting {days} days of {symbol} data from {exchange}",
            "exchange": exchange,
            "symbol": symbol,
            "interval": interval,
            "days": days
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@router.get("/popular-symbols")
async def get_popular_symbols():
    """获取热门交易对"""
    return {
        "crypto": [
            "BTC/USDT", "ETH/USDT", "BNB/USDT",
            "SOL/USDT", "XRP/USDT", "ADA/USDT",
            "DOGE/USDT", "AVAX/USDT", "DOT/USDT"
        ],
        "stocks": [
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
            "NVDA", "META", "NFLX", "AMD", "INTC"
        ],
        "a_stocks": [
            "000001.SZ", "600519.SH", "000858.SZ",
            "601318.SH", "600036.SH"
        ]
    }
