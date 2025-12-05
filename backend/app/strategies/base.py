from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime
import pandas as pd


class BaseStrategy(ABC):
    """策略基类"""
    
    def __init__(self, params: Dict[str, Any] = None):
        self.params = params or {}
        self.positions = {}  # 持仓信息
        self.orders = []  # 订单列表
        self.trades = []  # 成交记录
        self.capital = self.params.get('initial_capital', 100000.0)
        self.current_bar = None
        
    @abstractmethod
    def on_bar(self, bar: Dict[str, Any]):
        """
        K线数据回调
        
        Args:
            bar: K线数据字典，包含 open, high, low, close, volume, timestamp
        """
        pass
    
    def on_order(self, order: Dict[str, Any]):
        """订单状态更新回调"""
        pass
    
    def on_trade(self, trade: Dict[str, Any]):
        """成交回调"""
        pass
    
    def buy(self, price: float, amount: float, order_type: str = "market") -> Dict[str, Any]:
        """
        买入
        
        Args:
            price: 价格
            amount: 数量
            order_type: 订单类型 (market/limit)
        
        Returns:
            订单信息
        """
        order = {
            "side": "buy",
            "price": price,
            "amount": amount,
            "order_type": order_type,
            "timestamp": datetime.now(),
            "status": "pending"
        }
        self.orders.append(order)
        return order
    
    def sell(self, price: float, amount: float, order_type: str = "market") -> Dict[str, Any]:
        """
        卖出
        
        Args:
            price: 价格
            amount: 数量
            order_type: 订单类型 (market/limit)
        
        Returns:
            订单信息
        """
        order = {
            "side": "sell",
            "price": price,
            "amount": amount,
            "order_type": order_type,
            "timestamp": datetime.now(),
            "status": "pending"
        }
        self.orders.append(order)
        return order
    
    def get_position(self, symbol: str = None) -> Dict[str, Any]:
        """获取持仓信息"""
        if symbol:
            return self.positions.get(symbol, {})
        return self.positions
    
    def get_capital(self) -> float:
        """获取当前资金"""
        return self.capital
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算技术指标
        
        Args:
            df: K线数据DataFrame
        
        Returns:
            添加了指标的DataFrame
        """
        return df


class MAStrategy(BaseStrategy):
    """移动平均线策略示例"""
    
    def __init__(self, params: Dict[str, Any] = None):
        super().__init__(params)
        self.short_period = self.params.get('short_period', 10)
        self.long_period = self.params.get('long_period', 30)
        self.prices = []
    
    def on_bar(self, bar: Dict[str, Any]):
        """K线回调"""
        self.current_bar = bar
        self.prices.append(bar['close'])
        
        # 保持价格列表长度
        if len(self.prices) > self.long_period:
            self.prices.pop(0)
        
        # 计算均线
        if len(self.prices) >= self.long_period:
            short_ma = sum(self.prices[-self.short_period:]) / self.short_period
            long_ma = sum(self.prices[-self.long_period:]) / self.long_period
            
            position = self.get_position()
            
            # 金叉买入
            if short_ma > long_ma and not position:
                amount = self.capital * 0.95 / bar['close']  # 使用95%资金
                self.buy(bar['close'], amount)
            
            # 死叉卖出
            elif short_ma < long_ma and position:
                self.sell(bar['close'], position.get('amount', 0))
