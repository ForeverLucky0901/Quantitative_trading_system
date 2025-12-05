from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from app.core.database import Base


class Kline(Base):
    """K线数据模型"""
    __tablename__ = "klines"
    
    id = Column(Integer, primary_key=True, index=True)
    exchange = Column(String(50), nullable=False)
    symbol = Column(String(20), nullable=False)
    interval = Column(String(10), nullable=False)  # 1m, 5m, 15m, 1h, 4h, 1d
    timestamp = Column(DateTime(timezone=True), nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    
    __table_args__ = (
        Index('idx_kline_lookup', 'exchange', 'symbol', 'interval', 'timestamp'),
    )
    
    def __repr__(self):
        return f"<Kline {self.symbol} {self.interval} {self.timestamp}>"
