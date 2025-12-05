from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.strategy import Strategy, Backtest
from app.schemas.strategy import (
    StrategyCreate, StrategyUpdate, StrategyResponse,
    BacktestCreate, BacktestResponse
)

router = APIRouter()


@router.post("/", response_model=StrategyResponse, status_code=status.HTTP_201_CREATED)
async def create_strategy(
    strategy_in: StrategyCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建策略"""
    # TODO: 获取当前用户ID
    user_id = 1  # 临时使用
    
    strategy = Strategy(
        user_id=user_id,
        name=strategy_in.name,
        description=strategy_in.description,
        code=strategy_in.code,
        params=strategy_in.params
    )
    db.add(strategy)
    await db.commit()
    await db.refresh(strategy)
    
    return strategy


@router.get("/", response_model=List[StrategyResponse])
async def list_strategies(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """获取策略列表"""
    result = await db.execute(select(Strategy).offset(skip).limit(limit))
    strategies = result.scalars().all()
    return strategies


@router.get("/{strategy_id}", response_model=StrategyResponse)
async def get_strategy(strategy_id: int, db: AsyncSession = Depends(get_db)):
    """获取策略详情"""
    result = await db.execute(select(Strategy).where(Strategy.id == strategy_id))
    strategy = result.scalar_one_or_none()
    
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    return strategy


@router.put("/{strategy_id}", response_model=StrategyResponse)
async def update_strategy(
    strategy_id: int,
    strategy_in: StrategyUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新策略"""
    result = await db.execute(select(Strategy).where(Strategy.id == strategy_id))
    strategy = result.scalar_one_or_none()
    
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    update_data = strategy_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(strategy, field, value)
    
    await db.commit()
    await db.refresh(strategy)
    
    return strategy


@router.delete("/{strategy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_strategy(strategy_id: int, db: AsyncSession = Depends(get_db)):
    """删除策略"""
    result = await db.execute(select(Strategy).where(Strategy.id == strategy_id))
    strategy = result.scalar_one_or_none()
    
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    await db.delete(strategy)
    await db.commit()


@router.post("/{strategy_id}/start")
async def start_strategy(strategy_id: int, db: AsyncSession = Depends(get_db)):
    """启动策略"""
    result = await db.execute(select(Strategy).where(Strategy.id == strategy_id))
    strategy = result.scalar_one_or_none()
    
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    strategy.status = "active"
    await db.commit()
    
    return {"message": "Strategy started successfully", "strategy_id": strategy_id}


@router.post("/{strategy_id}/stop")
async def stop_strategy(strategy_id: int, db: AsyncSession = Depends(get_db)):
    """停止策略"""
    result = await db.execute(select(Strategy).where(Strategy.id == strategy_id))
    strategy = result.scalar_one_or_none()
    
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    strategy.status = "inactive"
    await db.commit()
    
    return {"message": "Strategy stopped successfully", "strategy_id": strategy_id}


@router.post("/backtest", response_model=BacktestResponse)
async def create_backtest(
    backtest_in: BacktestCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建回测"""
    # 检查策略是否存在
    result = await db.execute(select(Strategy).where(Strategy.id == backtest_in.strategy_id))
    strategy = result.scalar_one_or_none()
    
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    backtest = Backtest(
        strategy_id=backtest_in.strategy_id,
        start_date=backtest_in.start_date,
        end_date=backtest_in.end_date,
        initial_capital=backtest_in.initial_capital
    )
    db.add(backtest)
    await db.commit()
    await db.refresh(backtest)
    
    # TODO: 异步执行回测任务
    
    return backtest


@router.get("/backtest/{backtest_id}", response_model=BacktestResponse)
async def get_backtest(backtest_id: int, db: AsyncSession = Depends(get_db)):
    """获取回测结果"""
    result = await db.execute(select(Backtest).where(Backtest.id == backtest_id))
    backtest = result.scalar_one_or_none()
    
    if not backtest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backtest not found"
        )
    
    return backtest
