from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Order(Base):
    """订单模型"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    exchange = Column(String(50), nullable=False)  # binance, okx, etc.
    symbol = Column(String(20), nullable=False)  # BTC/USDT
    order_type = Column(String(20), nullable=False)  # market, limit
    side = Column(String(10), nullable=False)  # buy, sell
    price = Column(Float)
    amount = Column(Float, nullable=False)
    filled = Column(Float, default=0.0)
    status = Column(String(20), default="pending")  # pending, filled, cancelled
    order_id = Column(String(100))  # 交易所订单ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联
    strategy = relationship("Strategy", backref="orders")
    
    def __repr__(self):
        return f"<Order {self.symbol} {self.side}>"


class Position(Base):
    """持仓模型"""
    __tablename__ = "positions"
    
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    exchange = Column(String(50), nullable=False)
    symbol = Column(String(20), nullable=False)
    side = Column(String(10), nullable=False)  # long, short
    amount = Column(Float, nullable=False)
    entry_price = Column(Float, nullable=False)
    current_price = Column(Float)
    unrealized_pnl = Column(Float, default=0.0)
    realized_pnl = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联
    strategy = relationship("Strategy", backref="positions")
    
    def __repr__(self):
        return f"<Position {self.symbol} {self.side}>"


class Trade(Base):
    """成交记录模型"""
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    exchange = Column(String(50), nullable=False)
    symbol = Column(String(20), nullable=False)
    side = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    fee = Column(Float, default=0.0)
    pnl = Column(Float)
    trade_id = Column(String(100))  # 交易所成交ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关联
    order = relationship("Order", backref="trades")
    strategy = relationship("Strategy", backref="trades")
    
    def __repr__(self):
        return f"<Trade {self.symbol} {self.side}>"
