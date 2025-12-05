from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.trade import Order, Position, Trade
from app.schemas.trade import OrderCreate, OrderResponse, PositionResponse, TradeResponse

router = APIRouter()


@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建订单"""
    order = Order(
        strategy_id=order_in.strategy_id,
        exchange=order_in.exchange,
        symbol=order_in.symbol,
        order_type=order_in.order_type,
        side=order_in.side,
        price=order_in.price,
        amount=order_in.amount
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    
    # TODO: 发送订单到交易所
    
    return order


@router.get("/orders", response_model=List[OrderResponse])
async def list_orders(
    strategy_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """获取订单列表"""
    query = select(Order)
    if strategy_id:
        query = query.where(Order.strategy_id == strategy_id)
    
    result = await db.execute(query.offset(skip).limit(limit))
    orders = result.scalars().all()
    return orders


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    """获取订单详情"""
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order


@router.post("/orders/{order_id}/cancel")
async def cancel_order(order_id: int, db: AsyncSession = Depends(get_db)):
    """取消订单"""
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    order.status = "cancelled"
    await db.commit()
    
    # TODO: 取消交易所订单
    
    return {"message": "Order cancelled successfully", "order_id": order_id}


@router.get("/positions", response_model=List[PositionResponse])
async def list_positions(
    strategy_id: int = None,
    db: AsyncSession = Depends(get_db)
):
    """获取持仓列表"""
    query = select(Position)
    if strategy_id:
        query = query.where(Position.strategy_id == strategy_id)
    
    result = await db.execute(query)
    positions = result.scalars().all()
    return positions


@router.get("/trades", response_model=List[TradeResponse])
async def list_trades(
    strategy_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """获取成交记录"""
    query = select(Trade)
    if strategy_id:
        query = query.where(Trade.strategy_id == strategy_id)
    
    result = await db.execute(query.offset(skip).limit(limit))
    trades = result.scalars().all()
    return trades
