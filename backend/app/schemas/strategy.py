from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class StrategyBase(BaseModel):
    """策略基础模型"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    code: str
    params: Optional[Dict[str, Any]] = None


class StrategyCreate(StrategyBase):
    """策略创建模型"""
    pass


class StrategyUpdate(BaseModel):
    """策略更新模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    code: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class StrategyResponse(StrategyBase):
    """策略响应模型"""
    id: int
    user_id: int
    status: str
    is_backtest: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class BacktestCreate(BaseModel):
    """回测创建模型"""
    strategy_id: int
    start_date: datetime
    end_date: datetime
    initial_capital: float = 100000.0


class BacktestResponse(BaseModel):
    """回测响应模型"""
    id: int
    strategy_id: int
    start_date: datetime
    end_date: datetime
    initial_capital: float
    final_capital: Optional[float] = None
    total_return: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    max_drawdown: Optional[float] = None
    win_rate: Optional[float] = None
    total_trades: Optional[int] = None
    result_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
