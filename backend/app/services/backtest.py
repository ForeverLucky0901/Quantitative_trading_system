import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime
from app.strategies.base import BaseStrategy


class BacktestEngine:
    """回测引擎"""
    
    def __init__(
        self,
        strategy: BaseStrategy,
        data: pd.DataFrame,
        initial_capital: float = 100000.0,
        commission: float = 0.001  # 手续费率
    ):
        self.strategy = strategy
        self.data = data
        self.initial_capital = initial_capital
        self.commission = commission
        
        self.capital = initial_capital
        self.positions = {}
        self.trades = []
        self.equity_curve = []
        
    def run(self) -> Dict[str, Any]:
        """运行回测"""
        for idx, row in self.data.iterrows():
            bar = {
                'timestamp': row.get('timestamp', idx),
                'open': row['open'],
                'high': row['high'],
                'low': row['low'],
                'close': row['close'],
                'volume': row['volume']
            }
            
            # 调用策略
            self.strategy.on_bar(bar)
            
            # 处理订单
            self._process_orders(bar)
            
            # 记录权益曲线
            equity = self._calculate_equity(bar['close'])
            self.equity_curve.append({
                'timestamp': bar['timestamp'],
                'equity': equity
            })
        
        # 计算回测结果
        return self._calculate_metrics()
    
    def _process_orders(self, bar: Dict[str, Any]):
        """处理订单"""
        for order in self.strategy.orders:
            if order['status'] == 'pending':
                # 简化处理：市价单立即成交
                if order['order_type'] == 'market':
                    price = bar['close']
                    amount = order['amount']
                    
                    if order['side'] == 'buy':
                        cost = price * amount * (1 + self.commission)
                        if self.capital >= cost:
                            self.capital -= cost
                            self.positions['amount'] = self.positions.get('amount', 0) + amount
                            self.positions['entry_price'] = price
                            
                            trade = {
                                'timestamp': bar['timestamp'],
                                'side': 'buy',
                                'price': price,
                                'amount': amount,
                                'commission': price * amount * self.commission
                            }
                            self.trades.append(trade)
                            order['status'] = 'filled'
                    
                    elif order['side'] == 'sell':
                        if self.positions.get('amount', 0) >= amount:
                            revenue = price * amount * (1 - self.commission)
                            self.capital += revenue
                            self.positions['amount'] -= amount
                            
                            trade = {
                                'timestamp': bar['timestamp'],
                                'side': 'sell',
                                'price': price,
                                'amount': amount,
                                'commission': price * amount * self.commission
                            }
                            self.trades.append(trade)
                            order['status'] = 'filled'
    
    def _calculate_equity(self, current_price: float) -> float:
        """计算当前权益"""
        position_value = self.positions.get('amount', 0) * current_price
        return self.capital + position_value
    
    def _calculate_metrics(self) -> Dict[str, Any]:
        """计算回测指标"""
        equity_df = pd.DataFrame(self.equity_curve)
        
        if len(equity_df) == 0:
            return {}
        
        # 总收益
        final_equity = equity_df['equity'].iloc[-1]
        total_return = (final_equity - self.initial_capital) / self.initial_capital
        
        # 收益率序列
        equity_df['returns'] = equity_df['equity'].pct_change()
        
        # 夏普比率 (假设无风险利率为0)
        sharpe_ratio = 0.0
        if equity_df['returns'].std() != 0:
            sharpe_ratio = equity_df['returns'].mean() / equity_df['returns'].std() * np.sqrt(252)
        
        # 最大回撤
        equity_df['cummax'] = equity_df['equity'].cummax()
        equity_df['drawdown'] = (equity_df['equity'] - equity_df['cummax']) / equity_df['cummax']
        max_drawdown = equity_df['drawdown'].min()
        
        # 胜率
        winning_trades = [t for t in self.trades if t['side'] == 'sell']
        win_rate = 0.0
        if len(winning_trades) > 0:
            # 简化计算
            win_rate = 0.5
        
        return {
            'initial_capital': self.initial_capital,
            'final_capital': final_equity,
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'total_trades': len(self.trades),
            'equity_curve': self.equity_curve,
            'trades': self.trades
        }
