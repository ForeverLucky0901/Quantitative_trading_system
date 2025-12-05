# AI功能快速开始指南

## 5分钟快速上手

### 第一步：配置OpenAI API密钥

1. 获取OpenAI API密钥
   - 访问 https://platform.openai.com/api-keys
   - 注册/登录账号
   - 创建新的API密钥

2. 配置环境变量
```bash
cd backend
cp .env.example .env
```

3. 编辑 `.env` 文件，添加你的API密钥：
```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo
```

### 第二步：安装依赖

```bash
# 后端
cd backend
pip install openai==1.3.0

# 前端（如果还没安装）
cd frontend
npm install
```

### 第三步：启动服务

```bash
# 启动后端
cd backend
uvicorn main:app --reload

# 启动前端（新终端）
cd frontend
npm run dev
```

### 第四步：访问AI助手

1. 打开浏览器访问：http://localhost:5173
2. 在左侧菜单找到"AI助手"
3. 开始使用AI功能！

## 快速体验示例

### 示例1：获取BTC交易信号（30秒）

1. 进入"AI助手" → "交易信号"标签
2. 输入：
   - 交易对：`BTC/USDT`
   - 交易所：`Binance`
   - 时间周期：`1h`
3. 点击"获取信号"
4. 查看AI生成的买卖建议、止损止盈位等

### 示例2：生成交易策略（1分钟）

1. 进入"AI助手" → "策略生成"标签
2. 在描述框输入：
```
创建一个RSI策略：
- 当RSI低于30时买入
- 当RSI高于70时卖出
- 使用80%的资金
- 包含止损保护
```
3. 选择策略类型：`技术分析`
4. 点击"生成策略"
5. 复制生成的代码到策略管理中使用

### 示例3：市场分析（1分钟）

1. 进入"AI助手" → "市场分析"标签
2. 输入：
   - 交易对：`ETH/USDT`
   - 交易所：`Binance`
3. 点击"开始分析"
4. 查看AI对市场趋势、支撑阻力位的分析

### 示例4：智能问答（随时）

1. 进入"AI助手" → "智能问答"标签
2. 输入问题，例如：
   - "什么是MACD指标？"
   - "如何设置合理的止损位？"
   - "双均线策略的优缺点是什么？"
3. 按Ctrl+Enter或点击"发送"
4. 查看AI的详细回答

## 使用技巧

### 💡 提示词优化

**策略生成时**：
- ✅ 好的描述："创建一个基于MACD和RSI的组合策略，当MACD金叉且RSI低于40时买入，MACD死叉或RSI高于80时卖出，每次使用70%资金，设置3%止损"
- ❌ 差的描述："做一个赚钱的策略"

**市场分析时**：
- 提供具体的交易对和时间范围
- 可以添加相关新闻增强分析

**交易信号时**：
- 选择合适的时间周期（短线用1h，中线用4h/1d）
- 结合多个时间周期综合判断

### 🎯 最佳实践

1. **先测试后使用**
   - 生成的策略必须先回测
   - 交易信号仅供参考，不要盲目跟随

2. **控制成本**
   - GPT-3.5-turbo：约$0.002/1K tokens
   - GPT-4：约$0.03/1K tokens
   - 建议先用3.5测试

3. **保存有用的结果**
   - 复制好的策略代码
   - 记录有价值的分析
   - 整理常见问题的答案

4. **组合使用**
   - 先用市场分析了解趋势
   - 再用交易信号获取具体建议
   - 用智能问答解决疑问
   - 用策略生成快速原型

## 常见问题

### Q1: API密钥无效怎么办？
**A**: 
1. 检查密钥是否正确复制（注意空格）
2. 确认密钥有足够的额度
3. 检查网络是否能访问OpenAI

### Q2: 响应很慢怎么办？
**A**: 
1. 使用gpt-3.5-turbo而不是gpt-4
2. 减少输入的数据量
3. 考虑使用国内API代理

### Q3: 生成的策略有错误？
**A**: 
1. 提供更详细的策略描述
2. 生成后手动检查代码
3. 进行充分的回测验证
4. 必要时手动调整

### Q4: 不想用OpenAI怎么办？
**A**: 可以使用其他LLM：
- **本地模型**：Ollama + Llama2/Mistral
- **国内API**：文心一言、通义千问、智谱AI
- **开源方案**：HuggingFace模型

修改 `backend/app/services/ai_service.py` 中的客户端初始化即可。

### Q5: 如何降低使用成本？
**A**: 
1. 使用gpt-3.5-turbo（便宜10倍）
2. 减少不必要的API调用
3. 缓存常见问题的答案
4. 考虑使用本地模型

## 进阶使用

### 自定义提示词

编辑 `backend/app/services/ai_service.py`，修改提示词模板：

```python
# 例如：修改市场分析的提示词
def _build_market_analysis_prompt(self, symbol, market_data, news):
    prompt = f"""
    你是一位资深的量化交易分析师...
    
    请分析 {symbol} 的市场情况：
    - 当前价格：{market_data.get('price')}
    - 24h涨跌：{market_data.get('change_percent')}
    
    请提供：
    1. 趋势判断
    2. 关键位置
    3. 交易建议
    """
    return prompt
```

### 添加新功能

1. 在 `ai_service.py` 添加新方法
2. 在 `ai.py` 添加新API端点
3. 在前端添加UI组件

### 集成其他AI服务

```python
# 例如：使用Claude API
from anthropic import AsyncAnthropic

class AIService:
    def __init__(self):
        if settings.USE_CLAUDE:
            self.client = AsyncAnthropic(
                api_key=settings.CLAUDE_API_KEY
            )
```

## 下一步

- 📖 阅读完整文档：[AI_FEATURES.md](./AI_FEATURES.md)
- 🎯 尝试生成自己的策略
- 📊 结合回测系统验证策略
- 💬 在智能问答中学习交易知识
- 🚀 探索更多AI应用场景

## 获取帮助

- 查看项目文档
- 提交Issue反馈问题
- 加入社区讨论
- 联系技术支持

---

**祝你使用愉快！🎉**
