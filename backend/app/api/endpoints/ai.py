"""
AI功能API接口
支持市场分析、策略生成、交易信号、智能问答等
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.services.ai_service import ai_service
from app.services.ai_predictor import ai_predictor
from app.services.data_collector import data_collector
import pandas as pd

router = APIRouter()


class MarketAnalysisRequest(BaseModel):
    """市场分析请求"""
    symbol: str = Field(..., description="交易对/股票代码")
    exchange: str = Field("binance_public", description="交易所")
    include_news: bool = Field(False, description="是否包含新闻分析")
    news_items: Optional[List[str]] = Field(None, description="新闻列表")


class StrategyGenerationRequest(BaseModel):
    """策略生成请求"""
    description: str = Field(..., description="策略描述")
    strategy_type: str = Field("technical", description="策略类型")
    params: Optional[Dict[str, Any]] = Field(None, description="额外参数")


class TradingSignalRequest(BaseModel):
    """交易信号请求"""
    symbol: str = Field(..., description="交易对")
    exchange: str = Field("binance_public", description="交易所")
    timeframe: str = Field("1h", description="时间周期")
    limit: int = Field(100, description="K线数量")


class QuestionRequest(BaseModel):
    """问答请求"""
    question: str = Field(..., description="用户问题")
    context: Optional[Dict[str, Any]] = Field(None, description="上下文信息")


class StrategyOptimizationRequest(BaseModel):
    """策略优化请求"""
    strategy_code: str = Field(..., description="策略代码")
    backtest_results: List[Dict[str, Any]] = Field(..., description="回测结果")


@router.post("/analyze-market")
async def analyze_market(
    request: MarketAnalysisRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    AI市场分析
    
    分析指定交易对的市场趋势、技术面、支撑阻力位等
    """
    try:
        # 获取市场数据
        ticker = await data_collector.fetch_ticker(request.exchange, request.symbol)
        
        # 获取K线数据用于技术分析
        klines = await data_collector.fetch_ohlcv(
            exchange_name=request.exchange,
            symbol=request.symbol,
            timeframe="1h",
            limit=100
        )
        
        # 构建市场数据
        market_data = {
            "price": ticker.get("last"),
            "volume": ticker.get("volume"),
            "change_percent": ticker.get("percentage"),
            "high_24h": ticker.get("high"),
            "low_24h": ticker.get("low"),
            "technical_indicators": _calculate_simple_indicators(klines) if klines else {}
        }
        
        # 调用AI分析
        analysis = await ai_service.analyze_market(
            symbol=request.symbol,
            market_data=market_data,
            news=request.news_items if request.include_news else None
        )
        
        return {
            "status": "success",
            "data": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-strategy")
async def generate_strategy(request: StrategyGenerationRequest):
    """
    AI策略生成
    
    根据用户描述自动生成量化交易策略代码
    """
    try:
        result = await ai_service.generate_strategy(
            description=request.description,
            strategy_type=request.strategy_type,
            params=request.params
        )
        
        return {
            "status": "success",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/trading-signal")
async def generate_trading_signal(request: TradingSignalRequest):
    """
    AI交易信号生成
    
    基于市场数据和技术指标生成交易信号和建议
    """
    try:
        # 获取K线数据
        klines = await data_collector.fetch_ohlcv(
            exchange_name=request.exchange,
            symbol=request.symbol,
            timeframe=request.timeframe,
            limit=request.limit
        )
        
        if not klines:
            raise HTTPException(status_code=404, detail="No market data available")
        
        # 转换为DataFrame
        df = pd.DataFrame(klines)
        
        # 计算技术指标
        indicators = _calculate_technical_indicators(df)
        
        # 生成交易信号
        signal = await ai_service.generate_trading_signal(
            symbol=request.symbol,
            market_data=df,
            indicators=indicators
        )
        
        return {
            "status": "success",
            "data": signal
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask")
async def ask_question(request: QuestionRequest):
    """
    AI智能问答
    
    回答量化交易相关问题
    """
    try:
        answer = await ai_service.answer_question(
            question=request.question,
            context=request.context
        )
        
        return {
            "status": "success",
            "data": answer
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize-strategy")
async def optimize_strategy(request: StrategyOptimizationRequest):
    """
    AI策略优化建议
    
    基于回测结果提供参数优化建议
    """
    try:
        suggestions = await ai_service.optimize_strategy_params(
            strategy_code=request.strategy_code,
            backtest_results=request.backtest_results
        )
        
        return {
            "status": "success",
            "data": suggestions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict-price")
async def predict_price_movement(request: TradingSignalRequest):
    """
    AI价格预测
    
    使用AI分析历史数据，预测未来价格走势
    """
    try:
        # 获取历史数据
        klines = await data_collector.fetch_ohlcv(
            exchange_name=request.exchange,
            symbol=request.symbol,
            timeframe=request.timeframe,
            limit=request.limit
        )
        
        if not klines:
            raise HTTPException(status_code=404, detail="No market data available")
        
        df = pd.DataFrame(klines)
        indicators = _calculate_technical_indicators(df)
        
        # AI预测
        prediction = await ai_predictor.predict_price_movement(
            symbol=request.symbol,
            historical_data=df,
            indicators=indicators
        )
        
        return {
            "status": "success",
            "data": prediction
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-algorithm")
async def analyze_algorithm_performance(
    algorithm_name: str = Body(...),
    backtest_results: List[Dict[str, Any]] = Body(...),
    market_conditions: Dict[str, Any] = Body(default={})
):
    """
    AI算法性能分析
    
    分析算法表现，提出优化建议以提高准确率
    """
    try:
        analysis = await ai_predictor.analyze_algorithm_performance(
            algorithm_name=algorithm_name,
            backtest_results=backtest_results,
            market_conditions=market_conditions
        )
        
        return {
            "status": "success",
            "data": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize-parameters")
async def optimize_algorithm_parameters(
    strategy_code: str = Body(...),
    parameter_ranges: Dict[str, List[float]] = Body(...),
    optimization_target: str = Body("sharpe_ratio")
):
    """
    AI参数优化
    
    使用AI分析并推荐最优参数组合
    """
    try:
        # 转换参数范围格式
        param_ranges = {k: tuple(v) for k, v in parameter_ranges.items()}
        
        recommendations = await ai_predictor.optimize_parameters(
            strategy_code=strategy_code,
            parameter_ranges=param_ranges,
            optimization_target=optimization_target
        )
        
        return {
            "status": "success",
            "data": recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect-market-regime")
async def detect_market_regime(request: TradingSignalRequest):
    """
    AI市场状态识别
    
    识别当前市场是趋势市还是震荡市，选择适合的策略
    """
    try:
        klines = await data_collector.fetch_ohlcv(
            exchange_name=request.exchange,
            symbol=request.symbol,
            timeframe=request.timeframe,
            limit=request.limit
        )
        
        if not klines:
            raise HTTPException(status_code=404, detail="No market data available")
        
        df = pd.DataFrame(klines)
        indicators = _calculate_technical_indicators(df)
        
        regime = await ai_predictor.detect_market_regime(
            historical_data=df,
            indicators=indicators
        )
        
        return {
            "status": "success",
            "data": regime
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/capabilities")
async def get_ai_capabilities():
    """
    获取AI功能列表
    
    返回系统支持的所有AI功能
    """
    return {
        "capabilities": [
            {
                "name": "市场分析",
                "endpoint": "/api/v1/ai/analyze-market",
                "description": "分析市场趋势、技术面、支撑阻力位",
                "status": "available"
            },
            {
                "name": "策略生成",
                "endpoint": "/api/v1/ai/generate-strategy",
                "description": "根据描述自动生成交易策略代码",
                "status": "available"
            },
            {
                "name": "交易信号",
                "endpoint": "/api/v1/ai/trading-signal",
                "description": "生成买卖信号和交易建议",
                "status": "available"
            },
            {
                "name": "智能问答",
                "endpoint": "/api/v1/ai/ask",
                "description": "回答量化交易相关问题",
                "status": "available"
            },
            {
                "name": "策略优化",
                "endpoint": "/api/v1/ai/optimize-strategy",
                "description": "提供策略参数优化建议",
                "status": "available"
            },
            {
                "name": "AI价格预测",
                "endpoint": "/api/v1/ai/predict-price",
                "description": "预测未来价格走势和目标价位",
                "status": "available"
            },
            {
                "name": "AI算法分析",
                "endpoint": "/api/v1/ai/analyze-algorithm",
                "description": "分析算法性能并提高准确率",
                "status": "available"
            },
            {
                "name": "AI参数优化",
                "endpoint": "/api/v1/ai/optimize-parameters",
                "description": "智能推荐最优参数组合",
                "status": "available"
            },
            {
                "name": "市场状态识别",
                "endpoint": "/api/v1/ai/detect-market-regime",
                "description": "识别趋势市/震荡市，选择适合策略",
                "status": "available"
            }
        ],
        "model": "OpenAI GPT",
        "status": "operational" if ai_service.client else "not_configured"
    }


def _calculate_simple_indicators(klines: List[Dict]) -> Dict[str, Any]:
    """计算简单技术指标"""
    if not klines or len(klines) < 20:
        return {}
    
    df = pd.DataFrame(klines)
    
    return {
        "ma_5": float(df['close'].tail(5).mean()),
        "ma_10": float(df['close'].tail(10).mean()),
        "ma_20": float(df['close'].tail(20).mean()),
        "volume_avg": float(df['volume'].tail(20).mean()),
        "price_change_5": float((df['close'].iloc[-1] / df['close'].iloc[-5] - 1) * 100),
        "price_change_20": float((df['close'].iloc[-1] / df['close'].iloc[-20] - 1) * 100)
    }


def _calculate_technical_indicators(df: pd.DataFrame) -> Dict[str, Any]:
    """计算技术指标（精准版）"""
    indicators = {}
    
    try:
        # 移动平均线（SMA & EMA）
        if len(df) >= 5:
            indicators['sma_5'] = float(df['close'].rolling(window=5).mean().iloc[-1])
            indicators['ema_5'] = float(df['close'].ewm(span=5, adjust=False).mean().iloc[-1])
        if len(df) >= 10:
            indicators['sma_10'] = float(df['close'].rolling(window=10).mean().iloc[-1])
            indicators['ema_10'] = float(df['close'].ewm(span=10, adjust=False).mean().iloc[-1])
        if len(df) >= 20:
            indicators['sma_20'] = float(df['close'].rolling(window=20).mean().iloc[-1])
            indicators['ema_20'] = float(df['close'].ewm(span=20, adjust=False).mean().iloc[-1])
        if len(df) >= 50:
            indicators['sma_50'] = float(df['close'].rolling(window=50).mean().iloc[-1])
            indicators['ema_50'] = float(df['close'].ewm(span=50, adjust=False).mean().iloc[-1])
        
        # RSI（相对强弱指标）
        if len(df) >= 14:
            delta = df['close'].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(window=14).mean()
            avg_loss = loss.rolling(window=14).mean()
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            indicators['rsi'] = float(rsi.iloc[-1])
            indicators['rsi_signal'] = 'oversold' if rsi.iloc[-1] < 30 else 'overbought' if rsi.iloc[-1] > 70 else 'neutral'
        
        # MACD（指数平滑异同移动平均线）
        if len(df) >= 26:
            exp1 = df['close'].ewm(span=12, adjust=False).mean()
            exp2 = df['close'].ewm(span=26, adjust=False).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9, adjust=False).mean()
            histogram = macd - signal
            indicators['macd'] = float(macd.iloc[-1])
            indicators['macd_signal'] = float(signal.iloc[-1])
            indicators['macd_histogram'] = float(histogram.iloc[-1])
            # MACD信号
            if len(macd) >= 2:
                if macd.iloc[-2] < signal.iloc[-2] and macd.iloc[-1] > signal.iloc[-1]:
                    indicators['macd_cross'] = 'golden_cross'  # 金叉
                elif macd.iloc[-2] > signal.iloc[-2] and macd.iloc[-1] < signal.iloc[-1]:
                    indicators['macd_cross'] = 'death_cross'  # 死叉
                else:
                    indicators['macd_cross'] = 'none'
        
        # 布林带（Bollinger Bands）
        if len(df) >= 20:
            sma = df['close'].rolling(window=20).mean()
            std = df['close'].rolling(window=20).std()
            bb_upper = sma + (std * 2)
            bb_lower = sma - (std * 2)
            indicators['bb_upper'] = float(bb_upper.iloc[-1])
            indicators['bb_middle'] = float(sma.iloc[-1])
            indicators['bb_lower'] = float(bb_lower.iloc[-1])
            # 布林带位置
            current_price = df['close'].iloc[-1]
            bb_position = (current_price - bb_lower.iloc[-1]) / (bb_upper.iloc[-1] - bb_lower.iloc[-1])
            indicators['bb_position'] = float(bb_position)  # 0-1之间，0.5为中轨
        
        # ATR（平均真实波动幅度）
        if len(df) >= 14:
            high_low = df['high'] - df['low']
            high_close = abs(df['high'] - df['close'].shift())
            low_close = abs(df['low'] - df['close'].shift())
            tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            atr = tr.rolling(window=14).mean()
            indicators['atr'] = float(atr.iloc[-1])
            indicators['atr_percent'] = float((atr.iloc[-1] / df['close'].iloc[-1]) * 100)
        
        # 成交量分析
        if len(df) >= 20:
            vol_ma = df['volume'].rolling(window=20).mean()
            indicators['volume_avg'] = float(vol_ma.iloc[-1])
            indicators['volume_ratio'] = float(df['volume'].iloc[-1] / vol_ma.iloc[-1])
            # 量价关系
            price_change = (df['close'].iloc[-1] - df['close'].iloc[-2]) / df['close'].iloc[-2]
            volume_change = (df['volume'].iloc[-1] - df['volume'].iloc[-2]) / df['volume'].iloc[-2]
            indicators['price_volume_correlation'] = 'bullish' if price_change > 0 and volume_change > 0 else 'bearish' if price_change < 0 and volume_change > 0 else 'neutral'
        
        # KDJ指标
        if len(df) >= 9:
            low_9 = df['low'].rolling(window=9).min()
            high_9 = df['high'].rolling(window=9).max()
            rsv = (df['close'] - low_9) / (high_9 - low_9) * 100
            k = rsv.ewm(com=2, adjust=False).mean()
            d = k.ewm(com=2, adjust=False).mean()
            j = 3 * k - 2 * d
            indicators['kdj_k'] = float(k.iloc[-1])
            indicators['kdj_d'] = float(d.iloc[-1])
            indicators['kdj_j'] = float(j.iloc[-1])
        
        # 价格动量
        if len(df) >= 5:
            price_change_1d = ((df['close'].iloc[-1] - df['close'].iloc[-2]) / df['close'].iloc[-2]) * 100
            price_change_5d = ((df['close'].iloc[-1] - df['close'].iloc[-5]) / df['close'].iloc[-5]) * 100
            indicators['price_change_1d'] = float(price_change_1d)
            indicators['price_change_5d'] = float(price_change_5d)
        
        # 趋势判断
        if 'sma_5' in indicators and 'sma_20' in indicators and 'sma_50' in indicators:
            if indicators['sma_5'] > indicators['sma_20'] > indicators['sma_50']:
                indicators['trend'] = 'strong_uptrend'
            elif indicators['sma_5'] > indicators['sma_20']:
                indicators['trend'] = 'uptrend'
            elif indicators['sma_5'] < indicators['sma_20'] < indicators['sma_50']:
                indicators['trend'] = 'strong_downtrend'
            elif indicators['sma_5'] < indicators['sma_20']:
                indicators['trend'] = 'downtrend'
            else:
                indicators['trend'] = 'sideways'
        
    except Exception as e:
        logger.error(f"Error calculating indicators: {e}")
    
    return indicators
