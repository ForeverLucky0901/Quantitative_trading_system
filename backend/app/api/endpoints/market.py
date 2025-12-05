from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.models.market import Kline

router = APIRouter()


@router.get("/klines")
async def get_klines(
    exchange: str = Query(..., description="交易所名称"),
    symbol: str = Query(..., description="交易对"),
    interval: str = Query(..., description="时间间隔"),
    start_time: datetime = Query(None, description="开始时间"),
    end_time: datetime = Query(None, description="结束时间"),
    limit: int = Query(500, le=1000, description="返回数量"),
    db: AsyncSession = Depends(get_db)
):
    """获取K线数据"""
    query = select(Kline).where(
        Kline.exchange == exchange,
        Kline.symbol == symbol,
        Kline.interval == interval
    )
    
    if start_time:
        query = query.where(Kline.timestamp >= start_time)
    if end_time:
        query = query.where(Kline.timestamp <= end_time)
    
    query = query.order_by(Kline.timestamp.desc()).limit(limit)
    
    result = await db.execute(query)
    klines = result.scalars().all()
    
    return {
        "exchange": exchange,
        "symbol": symbol,
        "interval": interval,
        "data": [
            {
                "timestamp": k.timestamp.isoformat(),
                "open": k.open,
                "high": k.high,
                "low": k.low,
                "close": k.close,
                "volume": k.volume
            }
            for k in reversed(klines)
        ]
    }


@router.get("/ticker")
async def get_ticker(
    exchange: str = Query(..., description="交易所名称"),
    symbol: str = Query(..., description="交易对")
):
    """获取实时行情"""
    # TODO: 从Redis或交易所API获取实时行情
    return {
        "exchange": exchange,
        "symbol": symbol,
        "last_price": 0.0,
        "bid": 0.0,
        "ask": 0.0,
        "volume_24h": 0.0,
        "change_24h": 0.0
    }


@router.get("/symbols")
async def get_symbols(exchange: str = Query(..., description="交易所名称")):
    """获取交易对列表"""
    # TODO: 从交易所API获取交易对列表
    return {
        "exchange": exchange,
        "symbols": ["BTC/USDT", "ETH/USDT", "BNB/USDT"]
    }
