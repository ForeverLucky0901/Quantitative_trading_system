from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class OrderCreate(BaseModel):
    """订单创建模型"""
    strategy_id: int
    exchange: str
    symbol: str
    order_type: str = Field(..., pattern="^(market|limit)$")
    side: str = Field(..., pattern="^(buy|sell)$")
    price: Optional[float] = None
    amount: float = Field(..., gt=0)


class OrderResponse(BaseModel):
    """订单响应模型"""
    id: int
    strategy_id: int
    exchange: str
    symbol: str
    order_type: str
    side: str
    price: Optional[float] = None
    amount: float
    filled: float
    status: str
    order_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PositionResponse(BaseModel):
    """持仓响应模型"""
    id: int
    strategy_id: int
    exchange: str
    symbol: str
    side: str
    amount: float
    entry_price: float
    current_price: Optional[float] = None
    unrealized_pnl: float
    realized_pnl: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TradeResponse(BaseModel):
    """成交响应模型"""
    id: int
    order_id: int
    strategy_id: int
    exchange: str
    symbol: str
    side: str
    price: float
    amount: float
    fee: float
    pnl: Optional[float] = None
    trade_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
