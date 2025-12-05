from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON, ForeignKey, Float, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Strategy(Base):
    """策略模型"""
    __tablename__ = "strategies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    code = Column(Text, nullable=False)  # 策略代码
    params = Column(JSON)  # 策略参数
    status = Column(String(20), default="inactive")  # inactive, active, paused
    is_backtest = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关联
    user = relationship("User", backref="strategies")
    
    def __repr__(self):
        return f"<Strategy {self.name}>"


class Backtest(Base):
    """回测记录模型"""
    __tablename__ = "backtests"
    
    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    initial_capital = Column(Float, default=100000.0)
    final_capital = Column(Float)
    total_return = Column(Float)
    sharpe_ratio = Column(Float)
    max_drawdown = Column(Float)
    win_rate = Column(Float)
    total_trades = Column(Integer)
    result_data = Column(JSON)  # 详细回测结果
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关联
    strategy = relationship("Strategy", backref="backtests")
    
    def __repr__(self):
        return f"<Backtest {self.id}>"
