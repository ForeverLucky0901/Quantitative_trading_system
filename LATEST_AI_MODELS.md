# 2024年最新AI模型配置指南

## 🏆 推荐排行（2024年12月更新）

### 第1名：Claude 3.5 Sonnet（最强推荐）⭐⭐⭐⭐⭐

**发布时间**：2024年10月22日  
**训练数据**：2024年4月  
**价格**：$3/百万输入tokens，$15/百万输出tokens

**为什么选它**：
- 🥇 综合能力最强，超越GPT-4
- 💻 代码生成能力顶级
- 📊 金融分析专业
- 💰 性价比高

**配置方法**：

```bash
# 1. 安装依赖
pip install anthropic

# 2. 配置环境变量
CLAUDE_API_KEY=sk-ant-your-key-here
AI_PROVIDER=claude
AI_MODEL=claude-3-5-sonnet-20241022
```

**修改代码**（`ai_service.py`）：

```python
from anthropic import AsyncAnthropic

class AIService:
    def __init__(self):
        if settings.AI_PROVIDER == "claude":
            self.client = AsyncAnthropic(
                api_key=settings.CLAUDE_API_KEY
            )
            self.provider = "claude"
        
    async def analyze_market(self, symbol, market_data, news=None):
        if self.provider == "claude":
            response = await self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            return response.content[0].text
```

---

### 第2名：DeepSeek V3（国产之光）⭐⭐⭐⭐⭐

**发布时间**：2024年12月（最新！）  
**训练数据**：2024年中  
**价格**：$0.27/百万输入tokens（超便宜！）

**为什么选它**：
- 🇨🇳 国产开源，性能超GPT-4
- 💰 价格超低，是Claude的1/10
- ⚡ 速度快
- 🔓 可本地部署

**配置方法**（兼容OpenAI格式）：

```bash
# .env配置
OPENAI_API_KEY=your-deepseek-key
OPENAI_MODEL=deepseek-chat
OPENAI_BASE_URL=https://api.deepseek.com/v1
```

**无需修改代码**，直接使用！

**申请地址**：https://platform.deepseek.com/

---

### 第3名：GPT-4o（OpenAI最新）⭐⭐⭐⭐

**发布时间**：2024年5月  
**训练数据**：2023年10月  
**价格**：$2.5/百万输入tokens

**为什么选它**：
- ⚡ 比GPT-4快2倍
- 💰 便宜50%
- 🎯 多模态支持

**配置方法**：

```bash
# .env配置
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=gpt-4o  # 或 gpt-4o-mini（更便宜）
OPENAI_BASE_URL=https://api.openai.com/v1
```

---

### 第4名：Gemini 1.5 Pro（Google最新）⭐⭐⭐⭐

**发布时间**：2024年2月  
**训练数据**：2024年初  
**价格**：有免费额度！

**为什么选它**：
- 📚 超长上下文（200万tokens）
- 🆓 有免费额度
- 🔍 可以搜索实时信息

**配置方法**：

```bash
pip install google-generativeai
```

```python
import google.generativeai as genai

class AIService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.client = genai.GenerativeModel('gemini-1.5-pro-latest')
```

---

### 第5名：Qwen2.5-72B（阿里最新）⭐⭐⭐⭐

**发布时间**：2024年9月  
**训练数据**：2024年中  
**价格**：便宜

**为什么选它**：
- 🇨🇳 中文理解强
- 💰 价格便宜
- 📊 金融数据较新

**配置方法**：

```bash
# 使用阿里云百炼平台
OPENAI_API_KEY=your-dashscope-key
OPENAI_MODEL=qwen-plus
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

---

## 🌐 终极方案：实时联网模型

### Perplexity API（最推荐）

**特点**：
- ✅ 实时搜索互联网
- ✅ 获取最新新闻和数据
- ✅ 兼容OpenAI格式

**配置方法**：

```bash
OPENAI_API_KEY=your-perplexity-key
OPENAI_MODEL=llama-3.1-sonar-large-128k-online  # 在线模式
OPENAI_BASE_URL=https://api.perplexity.ai
```

**申请地址**：https://www.perplexity.ai/settings/api

---

## 💡 实战配置建议

### 方案A：最强性能（推荐专业用户）

```bash
# 使用Claude 3.5 Sonnet
AI_PROVIDER=claude
CLAUDE_API_KEY=your-key
AI_MODEL=claude-3-5-sonnet-20241022
```

**适合**：对精准度要求高，预算充足

---

### 方案B：最佳性价比（推荐大多数用户）⭐

```bash
# 使用DeepSeek V3
OPENAI_API_KEY=your-deepseek-key
OPENAI_MODEL=deepseek-chat
OPENAI_BASE_URL=https://api.deepseek.com/v1
```

**适合**：追求性价比，国内访问快

---

### 方案C：实时信息（推荐交易用户）

```bash
# 使用Perplexity（联网）
OPENAI_API_KEY=your-perplexity-key
OPENAI_MODEL=llama-3.1-sonar-large-128k-online
OPENAI_BASE_URL=https://api.perplexity.ai
```

**适合**：需要最新市场新闻和数据

---

### 方案D：免费方案

```bash
# 使用Gemini（有免费额度）
GEMINI_API_KEY=your-gemini-key
AI_PROVIDER=gemini
```

**适合**：测试和学习

---

## 🔧 快速切换配置

### 1. 修改 `config.py`

```python
class Settings(BaseSettings):
    # AI配置
    AI_PROVIDER: str = "openai"  # openai/claude/gemini/deepseek
    
    # OpenAI/DeepSeek/Perplexity（兼容格式）
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Claude
    CLAUDE_API_KEY: str = ""
    
    # Gemini
    GEMINI_API_KEY: str = ""
```

### 2. 修改 `ai_service.py`

```python
class AIService:
    def __init__(self):
        self.provider = settings.AI_PROVIDER
        
        if self.provider == "claude":
            from anthropic import AsyncAnthropic
            self.client = AsyncAnthropic(api_key=settings.CLAUDE_API_KEY)
        
        elif self.provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.client = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        else:  # openai/deepseek/perplexity
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_BASE_URL
            )
```

---

## 📊 性能对比表

| 模型 | 发布时间 | 训练数据 | 价格 | 速度 | 精准度 | 推荐度 |
|------|---------|---------|------|------|--------|--------|
| Claude 3.5 Sonnet | 2024.10 | 2024.04 | $$$ | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| DeepSeek V3 | 2024.12 | 2024中 | $ | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| GPT-4o | 2024.05 | 2023.10 | $$ | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Gemini 1.5 Pro | 2024.02 | 2024初 | 🆓 | ⚡⚡⚡ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Perplexity | 2024 | 实时 | $$ | ⚡⚡⚡ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🎯 我的推荐

### 如果你是新手
→ 使用 **Gemini**（免费）或 **DeepSeek**（便宜）

### 如果你追求性能
→ 使用 **Claude 3.5 Sonnet**

### 如果你需要最新信息
→ 使用 **Perplexity**（联网）+ 本系统的实时数据

### 如果你在国内
→ 使用 **DeepSeek** 或 **Qwen**

---

## ⚡ 立即开始

### 1. 选择模型（推荐DeepSeek）

```bash
# 注册DeepSeek账号
https://platform.deepseek.com/

# 获取API密钥
```

### 2. 配置环境变量

```bash
cd backend
nano .env

# 添加：
OPENAI_API_KEY=your-deepseek-key
OPENAI_MODEL=deepseek-chat
OPENAI_BASE_URL=https://api.deepseek.com/v1
```

### 3. 重启服务

```bash
uvicorn main:app --reload
```

### 4. 测试

访问 http://localhost:5173 → AI助手 → 开始使用！

---

## 🆘 常见问题

### Q: 哪个模型最便宜？
**A**: DeepSeek V3（$0.27/百万tokens）

### Q: 哪个模型最强？
**A**: Claude 3.5 Sonnet

### Q: 哪个模型数据最新？
**A**: Perplexity（实时联网）

### Q: 国内访问哪个快？
**A**: DeepSeek、Qwen

### Q: 有免费的吗？
**A**: Gemini有免费额度

---

## 📝 更新日志

- **2024-12-06**: 添加DeepSeek V3（最新）
- **2024-12-06**: 添加实时搜索功能
- **2024-12-06**: 添加多模型切换支持

---

**选择适合你的模型，开始智能交易！** 🚀
