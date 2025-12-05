"""
AI服务模块
支持市场分析、策略生成、交易信号、智能问答等功能
"""
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd
from loguru import logger
from openai import AsyncOpenAI
from app.core.config import settings
from app.services.search_service import search_service


class AIService:
    """AI服务类 - 集成OpenAI/其他LLM"""
    
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY:
            self.client = AsyncOpenAI(
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_BASE_URL
            )
            logger.info("OpenAI client initialized")
        else:
            logger.warning("OpenAI API key not configured")
    
    async def analyze_market(
        self,
        symbol: str,
        market_data: Dict[str, Any],
        news: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        AI市场分析
        
        Args:
            symbol: 交易对/股票代码
            market_data: 市场数据（价格、成交量等）
            news: 相关新闻列表
        
        Returns:
            分析结果
        """
        if not self.client:
            return {"error": "AI service not configured"}
        
        try:
            # 获取实时新闻和市场情绪
            if not news:
                logger.info(f"Fetching real-time news for {symbol}")
                news = await search_service.search_crypto_news(symbol)
                sentiment = await search_service.get_market_sentiment(symbol)
                if sentiment:
                    news.append(f"恐惧贪婪指数: {sentiment.get('fear_greed_index')} ({sentiment.get('classification')})")
            
            # 构建分析提示词
            prompt = self._build_market_analysis_prompt(symbol, market_data, news)
            
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """你是一位资深的量化交易分析师，拥有10年以上的实盘经验。

你的专业能力：
1. 精通技术分析：RSI、MACD、布林带、KDJ等所有主流指标
2. 擅长量价分析：能够识别量价背离和量价配合
3. 熟悉市场微观结构：支撑位、阻力位、趋势线
4. 风险管理专家：始终把风险控制放在第一位
5. 数据驱动决策：基于实时数据和统计规律，不主观猜测

分析原则：
- 基于提供的实时数据进行分析
- 给出明确的数据支撑
- 提供具体的价位和信号
- 包含风险提示和止损建议
- 避免模棱两可的表述，给出明确结论"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # 降低随机性，提高精准度
                max_tokens=2000
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "symbol": symbol,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat(),
                "model": settings.OPENAI_MODEL
            }
            
        except Exception as e:
            logger.error(f"Market analysis failed: {e}")
            return {"error": str(e)}
    
    async def generate_strategy(
        self,
        description: str,
        strategy_type: str = "technical",
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        AI策略生成
        
        Args:
            description: 策略描述
            strategy_type: 策略类型（technical/fundamental/ml）
            params: 额外参数
        
        Returns:
            生成的策略代码和说明
        """
        if not self.client:
            return {"error": "AI service not configured"}
        
        try:
            prompt = self._build_strategy_generation_prompt(description, strategy_type, params)
            
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一位量化交易策略开发专家，精通Python和各种交易策略。请生成符合BaseStrategy基类的策略代码。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            
            # 提取代码和说明
            code, explanation = self._extract_code_and_explanation(content)
            
            return {
                "code": code,
                "explanation": explanation,
                "strategy_type": strategy_type,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Strategy generation failed: {e}")
            return {"error": str(e)}
    
    async def generate_trading_signal(
        self,
        symbol: str,
        market_data: pd.DataFrame,
        indicators: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        AI交易信号生成
        
        Args:
            symbol: 交易对
            market_data: 市场数据DataFrame
            indicators: 技术指标
        
        Returns:
            交易信号和建议
        """
        if not self.client:
            return {"error": "AI service not configured"}
        
        try:
            # 准备数据摘要
            data_summary = self._prepare_data_summary(market_data, indicators)
            
            prompt = f"""
请分析以下市场数据并给出交易信号：

交易对: {symbol}
最新价格: {market_data['close'].iloc[-1]:.2f}
24小时涨跌: {((market_data['close'].iloc[-1] / market_data['close'].iloc[-24] - 1) * 100):.2f}%

数据摘要:
{data_summary}

请提供：
1. 交易信号（BUY/SELL/HOLD）
2. 信号强度（1-10）
3. 建议仓位（0-100%）
4. 止损位
5. 止盈位
6. 分析理由

请以JSON格式返回结果。
"""
            
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一位专业的交易信号分析师，基于技术分析给出精准的交易建议。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            # 尝试解析JSON
            try:
                signal = json.loads(content)
            except:
                signal = {"raw_response": content}
            
            signal["symbol"] = symbol
            signal["timestamp"] = datetime.now().isoformat()
            
            return signal
            
        except Exception as e:
            logger.error(f"Trading signal generation failed: {e}")
            return {"error": str(e)}
    
    async def answer_question(
        self,
        question: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        AI问答助手
        
        Args:
            question: 用户问题
            context: 上下文信息
        
        Returns:
            回答结果
        """
        if not self.client:
            return {"error": "AI service not configured"}
        
        try:
            # 构建上下文
            context_str = ""
            if context:
                context_str = f"\n\n相关上下文:\n{json.dumps(context, ensure_ascii=False, indent=2)}"
            
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一位量化交易专家助手，精通金融市场、技术分析、量化策略等领域。请提供专业、准确、易懂的回答。"
                    },
                    {
                        "role": "user",
                        "content": f"{question}{context_str}"
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            answer = response.choices[0].message.content
            
            return {
                "question": question,
                "answer": answer,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Question answering failed: {e}")
            return {"error": str(e)}
    
    async def optimize_strategy_params(
        self,
        strategy_code: str,
        backtest_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        AI策略参数优化建议
        
        Args:
            strategy_code: 策略代码
            backtest_results: 回测结果列表
        
        Returns:
            优化建议
        """
        if not self.client:
            return {"error": "AI service not configured"}
        
        try:
            prompt = f"""
请分析以下策略和回测结果，提供参数优化建议：

策略代码:
```python
{strategy_code}
```

回测结果:
{json.dumps(backtest_results, ensure_ascii=False, indent=2)}

请提供：
1. 当前参数的问题分析
2. 建议的参数调整方向
3. 预期改进效果
4. 风险提示
"""
            
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一位策略优化专家，擅长分析回测结果并提供参数优化建议。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.6,
                max_tokens=1500
            )
            
            suggestions = response.choices[0].message.content
            
            return {
                "suggestions": suggestions,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Strategy optimization failed: {e}")
            return {"error": str(e)}
    
    def _build_market_analysis_prompt(
        self,
        symbol: str,
        market_data: Dict[str, Any],
        news: Optional[List[str]]
    ) -> str:
        """构建市场分析提示词"""
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        prompt = f"""
【重要】以下是实时市场数据（采集时间: {current_time}），请基于这些最新数据进行分析：

交易对/股票: {symbol}
当前价格: {market_data.get('price', 'N/A')}
24小时成交量: {market_data.get('volume', 'N/A')}
24小时涨跌幅: {market_data.get('change_percent', 'N/A')}
最高价: {market_data.get('high_24h', 'N/A')}
最低价: {market_data.get('low_24h', 'N/A')}
"""
        
        if 'technical_indicators' in market_data:
            prompt += f"\n技术指标:\n{json.dumps(market_data['technical_indicators'], ensure_ascii=False, indent=2)}\n"
        
        if news:
            prompt += f"\n相关新闻:\n"
            for i, item in enumerate(news[:5], 1):
                prompt += f"{i}. {item}\n"
        
        prompt += """
请提供：
1. 市场趋势分析（短期、中期、长期）
2. 技术面分析
3. 支撑位和阻力位
4. 交易建议
5. 风险提示
"""
        
        return prompt
    
    def _build_strategy_generation_prompt(
        self,
        description: str,
        strategy_type: str,
        params: Optional[Dict[str, Any]]
    ) -> str:
        """构建策略生成提示词"""
        prompt = f"""
请根据以下描述生成一个量化交易策略：

策略描述: {description}
策略类型: {strategy_type}
"""
        
        if params:
            prompt += f"额外参数: {json.dumps(params, ensure_ascii=False, indent=2)}\n"
        
        prompt += """
请生成完整的Python策略代码，继承自BaseStrategy基类，包含：
1. __init__方法初始化参数
2. on_bar方法处理K线数据
3. 必要的技术指标计算
4. 买卖信号逻辑
5. 风险控制逻辑

BaseStrategy基类示例：
```python
class BaseStrategy(ABC):
    def __init__(self, params: Dict[str, Any] = None):
        self.params = params or {}
        self.positions = {}
        self.orders = []
        self.capital = self.params.get('initial_capital', 100000.0)
    
    def on_bar(self, bar: Dict[str, Any]):
        pass
    
    def buy(self, price: float, amount: float, order_type: str = "market"):
        pass
    
    def sell(self, price: float, amount: float, order_type: str = "market"):
        pass
```

请提供完整代码和详细说明。
"""
        
        return prompt
    
    def _extract_code_and_explanation(self, content: str) -> tuple:
        """从AI响应中提取代码和说明"""
        # 简单的代码提取逻辑
        code = ""
        explanation = content
        
        # 查找代码块
        if "```python" in content:
            parts = content.split("```python")
            if len(parts) > 1:
                code_parts = parts[1].split("```")
                code = code_parts[0].strip()
                explanation = parts[0] + (code_parts[1] if len(code_parts) > 1 else "")
        elif "```" in content:
            parts = content.split("```")
            if len(parts) > 1:
                code = parts[1].strip()
                explanation = parts[0] + (parts[2] if len(parts) > 2 else "")
        
        return code, explanation.strip()
    
    def _prepare_data_summary(
        self,
        market_data: pd.DataFrame,
        indicators: Optional[Dict[str, Any]]
    ) -> str:
        """准备市场数据摘要"""
        summary = f"""
最近5根K线:
{market_data[['open', 'high', 'low', 'close', 'volume']].tail(5).to_string()}
"""
        
        if indicators:
            summary += f"\n\n技术指标:\n{json.dumps(indicators, ensure_ascii=False, indent=2)}"
        
        return summary


# 全局AI服务实例
ai_service = AIService()
