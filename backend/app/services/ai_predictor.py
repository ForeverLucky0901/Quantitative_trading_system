"""
AI预测服务 - 使用AI分析算法并提高准确率
"""
import json
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from loguru import logger
from openai import AsyncOpenAI
from app.core.config import settings


class AIPredictorService:
    """AI预测服务 - 分析算法并提高准确率"""
    
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY:
            self.client = AsyncOpenAI(
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_BASE_URL
            )
            logger.info("AI Predictor initialized")
    
    async def predict_price_movement(
        self,
        symbol: str,
        historical_data: pd.DataFrame,
        indicators: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        AI预测价格走势
        
        使用AI分析历史数据和技术指标，预测未来价格走势
        
        Args:
            symbol: 交易对
            historical_data: 历史K线数据
            indicators: 技术指标
        
        Returns:
            预测结果（方向、概率、目标价位）
        """
        if not self.client:
            return {"error": "AI service not configured"}
        
        try:
            # 1. 提取关键特征
            features = self._extract_features(historical_data, indicators)
            
            # 2. 构建预测提示词
            prompt = self._build_prediction_prompt(symbol, features, indicators)
            
            # 3. AI分析预测
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """你是一位顶级的量化交易AI分析师，专注于价格预测和算法优化。

你的核心能力：
1. 模式识别：识别历史数据中的重复模式
2. 多因子分析：综合考虑技术指标、量价关系、市场情绪
3. 概率评估：给出预测的置信度
4. 风险量化：评估预测的风险收益比

分析方法：
- 使用统计学方法分析历史规律
- 识别支撑阻力位和关键价位
- 评估趋势强度和持续性
- 计算预测的准确率和置信区间

输出要求：
- 明确的方向预测（上涨/下跌/震荡）
- 预测置信度（0-100%）
- 目标价位和时间周期
- 关键支撑阻力位
- 风险提示"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,  # 低温度，提高预测稳定性
                max_tokens=1500
            )
            
            prediction_text = response.choices[0].message.content
            
            # 4. 解析预测结果
            prediction = self._parse_prediction(prediction_text, historical_data)
            
            return {
                "symbol": symbol,
                "prediction": prediction,
                "analysis": prediction_text,
                "timestamp": datetime.now().isoformat(),
                "model": settings.OPENAI_MODEL
            }
            
        except Exception as e:
            logger.error(f"Price prediction failed: {e}")
            return {"error": str(e)}
    
    async def analyze_algorithm_performance(
        self,
        algorithm_name: str,
        backtest_results: List[Dict[str, Any]],
        market_conditions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        AI分析算法性能并提出优化建议
        
        Args:
            algorithm_name: 算法名称
            backtest_results: 回测结果列表
            market_conditions: 市场条件
        
        Returns:
            性能分析和优化建议
        """
        if not self.client:
            return {"error": "AI service not configured"}
        
        try:
            # 计算性能指标
            performance_metrics = self._calculate_performance_metrics(backtest_results)
            
            # 构建分析提示词
            prompt = f"""
请分析以下交易算法的性能，并提出优化建议：

算法名称：{algorithm_name}

性能指标：
{json.dumps(performance_metrics, ensure_ascii=False, indent=2)}

市场条件：
{json.dumps(market_conditions, ensure_ascii=False, indent=2)}

请提供：
1. 算法优缺点分析
2. 在不同市场条件下的表现
3. 参数优化建议（具体数值）
4. 风险控制改进方案
5. 预期准确率提升幅度
"""
            
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """你是一位算法优化专家，专注于提高交易算法的准确率和收益率。

分析维度：
1. 胜率分析：识别算法在何种情况下表现最好
2. 盈亏比分析：评估风险收益比是否合理
3. 回撤控制：分析最大回撤的原因
4. 参数敏感性：评估参数对结果的影响
5. 市场适应性：算法在不同市场环境的表现

优化策略：
- 基于数据驱动的参数调整
- 增加过滤条件提高信号质量
- 改进止损止盈逻辑
- 加入市场环境判断
- 优化仓位管理

输出要求：
- 具体的数值建议（不要模糊表述）
- 预期的性能提升
- 实施的优先级
- 风险评估"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "algorithm": algorithm_name,
                "analysis": analysis,
                "performance_metrics": performance_metrics,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Algorithm analysis failed: {e}")
            return {"error": str(e)}
    
    async def optimize_parameters(
        self,
        strategy_code: str,
        parameter_ranges: Dict[str, Tuple[float, float]],
        optimization_target: str = "sharpe_ratio"
    ) -> Dict[str, Any]:
        """
        AI辅助参数优化
        
        Args:
            strategy_code: 策略代码
            parameter_ranges: 参数范围 {"param_name": (min, max)}
            optimization_target: 优化目标（sharpe_ratio/total_return/max_drawdown）
        
        Returns:
            优化建议
        """
        if not self.client:
            return {"error": "AI service not configured"}
        
        try:
            prompt = f"""
请为以下策略提供参数优化建议：

策略代码：
```python
{strategy_code}
```

参数范围：
{json.dumps(parameter_ranges, ensure_ascii=False, indent=2)}

优化目标：{optimization_target}

请提供：
1. 推荐的参数组合（3-5组）
2. 每组参数的预期表现
3. 参数选择的理由
4. 参数之间的相互影响
5. 优化的置信度
"""
            
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """你是一位参数优化专家，精通网格搜索、贝叶斯优化等方法。

优化原则：
1. 避免过拟合：参数不要过于复杂
2. 稳健性优先：选择在多种情况下都表现良好的参数
3. 风险控制：确保参数不会导致过大风险
4. 可解释性：参数选择要有明确的逻辑

分析方法：
- 基于技术指标的典型周期
- 考虑市场的波动特征
- 参考历史最优参数
- 评估参数的敏感性"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            recommendations = response.choices[0].message.content
            
            return {
                "recommendations": recommendations,
                "parameter_ranges": parameter_ranges,
                "optimization_target": optimization_target,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Parameter optimization failed: {e}")
            return {"error": str(e)}
    
    async def detect_market_regime(
        self,
        historical_data: pd.DataFrame,
        indicators: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        AI识别市场状态（趋势/震荡/反转）
        
        不同市场状态需要不同的策略
        
        Args:
            historical_data: 历史数据
            indicators: 技术指标
        
        Returns:
            市场状态分析
        """
        if not self.client:
            return {"error": "AI service not configured"}
        
        try:
            # 计算市场特征
            market_features = self._calculate_market_features(historical_data)
            
            prompt = f"""
请分析当前市场状态：

市场特征：
{json.dumps(market_features, ensure_ascii=False, indent=2)}

技术指标：
{json.dumps(indicators, ensure_ascii=False, indent=2)}

请判断：
1. 当前市场状态（趋势市/震荡市/转折期）
2. 趋势强度（1-10分）
3. 波动率水平（低/中/高）
4. 适合的策略类型
5. 状态持续的可能性
"""
            
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """你是市场状态识别专家。

市场状态分类：
1. 趋势市：明确的上涨或下跌趋势
   - 适合趋势跟踪策略
   - 均线策略效果好
   
2. 震荡市：价格在区间内波动
   - 适合网格交易、均值回归
   - 突破策略容易失效
   
3. 转折期：趋势即将改变
   - 需要谨慎交易
   - 适合观望或轻仓

判断依据：
- ADX指标判断趋势强度
- 布林带宽度判断波动率
- 价格与均线的关系
- 成交量变化"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                max_tokens=1000
            )
            
            regime_analysis = response.choices[0].message.content
            
            return {
                "regime": regime_analysis,
                "market_features": market_features,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Market regime detection failed: {e}")
            return {"error": str(e)}
    
    def _extract_features(
        self,
        df: pd.DataFrame,
        indicators: Dict[str, Any]
    ) -> Dict[str, Any]:
        """提取关键特征用于预测"""
        features = {}
        
        try:
            # 价格特征
            features['current_price'] = float(df['close'].iloc[-1])
            features['price_change_1d'] = float(((df['close'].iloc[-1] - df['close'].iloc[-2]) / df['close'].iloc[-2]) * 100)
            features['price_change_5d'] = float(((df['close'].iloc[-1] - df['close'].iloc[-5]) / df['close'].iloc[-5]) * 100)
            
            # 波动率
            features['volatility'] = float(df['close'].pct_change().std() * 100)
            
            # 趋势特征
            if len(df) >= 20:
                sma_20 = df['close'].rolling(20).mean().iloc[-1]
                features['price_vs_sma20'] = float(((df['close'].iloc[-1] - sma_20) / sma_20) * 100)
            
            # 成交量特征
            if len(df) >= 20:
                vol_ma = df['volume'].rolling(20).mean().iloc[-1]
                features['volume_ratio'] = float(df['volume'].iloc[-1] / vol_ma)
            
            # 技术指标
            features['indicators'] = indicators
            
        except Exception as e:
            logger.error(f"Feature extraction failed: {e}")
        
        return features
    
    def _build_prediction_prompt(
        self,
        symbol: str,
        features: Dict[str, Any],
        indicators: Dict[str, Any]
    ) -> str:
        """构建预测提示词"""
        prompt = f"""
请预测 {symbol} 的价格走势：

当前特征：
{json.dumps(features, ensure_ascii=False, indent=2)}

请提供：
1. 方向预测（上涨/下跌/震荡）及置信度（0-100%）
2. 预测时间周期（1小时/4小时/1天）
3. 目标价位（具体数值）
4. 关键支撑位和阻力位
5. 预测依据（基于哪些指标和模式）
6. 风险提示

请以JSON格式返回：
{{
    "direction": "上涨/下跌/震荡",
    "confidence": 75,
    "timeframe": "4小时",
    "target_price": 45000,
    "support_levels": [42000, 41000],
    "resistance_levels": [46000, 47000],
    "reasoning": "详细理由",
    "risk_warning": "风险提示"
}}
"""
        return prompt
    
    def _parse_prediction(
        self,
        prediction_text: str,
        df: pd.DataFrame
    ) -> Dict[str, Any]:
        """解析AI预测结果"""
        try:
            # 尝试提取JSON
            import re
            json_match = re.search(r'\{.*\}', prediction_text, re.DOTALL)
            if json_match:
                prediction = json.loads(json_match.group())
                return prediction
        except:
            pass
        
        # 如果无法解析JSON，返回文本
        return {
            "raw_prediction": prediction_text,
            "current_price": float(df['close'].iloc[-1])
        }
    
    def _calculate_performance_metrics(
        self,
        backtest_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """计算性能指标"""
        if not backtest_results:
            return {}
        
        metrics = {}
        
        try:
            # 提取收益率
            returns = [r.get('total_return', 0) for r in backtest_results]
            metrics['avg_return'] = float(np.mean(returns))
            metrics['std_return'] = float(np.std(returns))
            metrics['max_return'] = float(np.max(returns))
            metrics['min_return'] = float(np.min(returns))
            
            # 胜率
            winning_trades = sum(1 for r in backtest_results if r.get('total_return', 0) > 0)
            metrics['win_rate'] = float(winning_trades / len(backtest_results)) if backtest_results else 0
            
            # 夏普比率
            sharpe_ratios = [r.get('sharpe_ratio', 0) for r in backtest_results]
            metrics['avg_sharpe'] = float(np.mean(sharpe_ratios))
            
            # 最大回撤
            drawdowns = [abs(r.get('max_drawdown', 0)) for r in backtest_results]
            metrics['avg_drawdown'] = float(np.mean(drawdowns))
            metrics['max_drawdown'] = float(np.max(drawdowns))
            
        except Exception as e:
            logger.error(f"Performance metrics calculation failed: {e}")
        
        return metrics
    
    def _calculate_market_features(
        self,
        df: pd.DataFrame
    ) -> Dict[str, Any]:
        """计算市场特征"""
        features = {}
        
        try:
            # ADX（趋势强度）
            if len(df) >= 14:
                # 简化版ADX计算
                high_low = df['high'] - df['low']
                high_close = abs(df['high'] - df['close'].shift())
                low_close = abs(df['low'] - df['close'].shift())
                tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
                atr = tr.rolling(14).mean()
                features['atr'] = float(atr.iloc[-1])
            
            # 波动率
            returns = df['close'].pct_change()
            features['volatility'] = float(returns.std() * 100)
            features['volatility_level'] = 'high' if features['volatility'] > 3 else 'medium' if features['volatility'] > 1.5 else 'low'
            
            # 趋势方向
            if len(df) >= 50:
                sma_20 = df['close'].rolling(20).mean().iloc[-1]
                sma_50 = df['close'].rolling(50).mean().iloc[-1]
                if sma_20 > sma_50:
                    features['trend_direction'] = 'uptrend'
                elif sma_20 < sma_50:
                    features['trend_direction'] = 'downtrend'
                else:
                    features['trend_direction'] = 'sideways'
            
        except Exception as e:
            logger.error(f"Market features calculation failed: {e}")
        
        return features


# 全局实例
ai_predictor = AIPredictorService()
