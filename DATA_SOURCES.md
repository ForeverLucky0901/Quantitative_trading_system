# 数据源配置指南

## 🌐 支持的数据源

### 1. 加密货币数据（推荐）

#### CCXT - 统一交易所接口
- **支持交易所**：100+ 交易所
- **数据类型**：实时行情、K线、订单簿、成交记录
- **费用**：免费（公开数据）
- **配置**：无需API密钥即可获取公开数据

**热门交易所：**
- Binance（币安）
- OKX
- Bybit
- Coinbase
- Kraken

**使用示例：**
```python
# 获取币安BTC/USDT的K线数据
GET /api/v1/data/klines?exchange=binance_public&symbol=BTC/USDT&interval=1h&limit=100

# 获取实时行情
GET /api/v1/data/ticker?exchange=binance_public&symbol=BTC/USDT
```

### 2. 股票数据

#### Yahoo Finance（推荐）
- **支持市场**：美股、港股、A股等全球市场
- **数据类型**：日线、分钟线、财务数据
- **费用**：完全免费
- **延迟**：15分钟延迟

**安装：**
```bash
pip install yfinance
```

**使用示例：**
```python
import yfinance as yf

# 获取苹果股票数据
ticker = yf.Ticker("AAPL")
df = ticker.history(period="1mo", interval="1d")
```

**常用股票代码：**
- 美股：AAPL, MSFT, GOOGL, TSLA, NVDA
- 港股：0700.HK（腾讯）, 9988.HK（阿里）
- A股：000001.SS（上证指数）

#### Tushare（A股专用）
- **支持市场**：A股、港股、期货
- **数据类型**：日线、分钟线、财务数据、指标
- **费用**：免费（需注册获取token）
- **注册地址**：https://tushare.pro/register

**安装：**
```bash
pip install tushare
```

**配置：**
```python
# 在 .env 文件中添加
TUSHARE_TOKEN=your_token_here
```

**使用示例：**
```python
import tushare as ts

ts.set_token('your_token_here')
pro = ts.pro_api()

# 获取贵州茅台日线数据
df = pro.daily(ts_code='600519.SH', start_date='20240101', end_date='20241231')
```

#### AKShare（免费替代方案）
- **支持市场**：A股、期货、外汇、基金
- **数据类型**：实时行情、历史数据
- **费用**：完全免费，无需注册
- **限制**：数据更新可能有延迟

**安装：**
```bash
pip install akshare
```

**使用示例：**
```python
import akshare as ak

# 获取A股实时行情
df = ak.stock_zh_a_spot_em()

# 获取历史K线
df = ak.stock_zh_a_hist(symbol="000001", period="daily")
```

### 3. 期货数据

#### CTP（期货公司提供）
- **支持市场**：国内期货市场
- **数据类型**：实时行情、Tick数据
- **费用**：需要期货账户
- **特点**：最专业的期货数据

#### Wind、同花顺iFinD
- **支持市场**：全市场
- **数据类型**：全面的金融数据
- **费用**：付费（较贵）
- **特点**：专业机构使用

## 🚀 快速开始

### 方案一：加密货币（最简单）

1. **无需配置，直接使用**
```bash
# 启动后端
cd backend
uvicorn main:app --reload

# 访问API文档
http://localhost:8000/docs

# 测试数据采集
curl "http://localhost:8000/api/v1/data/klines?exchange=binance_public&symbol=BTC/USDT&interval=1h&limit=10"
```

2. **采集历史数据**
```bash
# 采集最近30天的BTC数据
curl -X POST "http://localhost:8000/api/v1/data/collect?exchange=binance_public&symbol=BTC/USDT&interval=1h&days=30"
```

### 方案二：股票数据（Yahoo Finance）

1. **安装依赖**
```bash
pip install yfinance
```

2. **使用Python脚本采集**
```python
from app.services.data_collector import YahooFinanceCollector
from datetime import datetime, timedelta

collector = YahooFinanceCollector()

# 获取苹果股票最近1个月数据
df = await collector.fetch_stock_data(
    symbol='AAPL',
    start_date=datetime.now() - timedelta(days=30),
    end_date=datetime.now(),
    interval='1d'
)
```

### 方案三：A股数据（Tushare）

1. **注册获取Token**
   - 访问：https://tushare.pro/register
   - 注册账号并获取token

2. **配置Token**
```bash
# 编辑 .env 文件
echo "TUSHARE_TOKEN=your_token_here" >> .env
```

3. **使用**
```python
from app.services.data_collector import TushareCollector

collector = TushareCollector(token='your_token_here')

# 获取贵州茅台数据
df = await collector.fetch_stock_daily(
    ts_code='600519.SH',
    start_date='20240101',
    end_date='20241231'
)
```

## 📊 数据采集API

### 获取支持的交易所
```
GET /api/v1/data/exchanges
```

### 获取交易对列表
```
GET /api/v1/data/symbols?exchange=binance_public
```

### 获取实时行情
```
GET /api/v1/data/ticker?exchange=binance_public&symbol=BTC/USDT
```

### 获取K线数据
```
GET /api/v1/data/klines?exchange=binance_public&symbol=BTC/USDT&interval=1h&limit=100
```

### 采集历史数据
```
POST /api/v1/data/collect?exchange=binance_public&symbol=BTC/USDT&interval=1h&days=30
```

### 获取热门交易对
```
GET /api/v1/data/popular-symbols
```

## ⚙️ 定时采集配置

系统支持使用Celery进行定时数据采集：

```bash
# 启动Celery Worker
celery -A app.tasks.data_tasks worker --loglevel=info

# 启动Celery Beat（定时任务）
celery -A app.tasks.data_tasks beat --loglevel=info
```

## 💡 推荐配置

### 新手推荐
1. **加密货币**：使用CCXT + Binance公开数据（免费，无需配置）
2. **股票**：使用Yahoo Finance（免费，全球市场）

### 专业用户
1. **加密货币**：CCXT + 交易所API密钥（实时数据，可交易）
2. **A股**：Tushare Pro（需注册，数据全面）
3. **期货**：CTP接口（需期货账户）

## 🔒 API密钥配置（可选）

如果需要实时交易功能，需要配置交易所API密钥：

```bash
# 编辑 .env 文件
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
BINANCE_TESTNET=True  # 测试网络

OKX_API_KEY=your_api_key
OKX_API_SECRET=your_api_secret
OKX_PASSPHRASE=your_passphrase
OKX_TESTNET=True
```

**注意事项：**
- 测试阶段建议使用测试网络
- 不要将API密钥提交到代码仓库
- 建议使用只读权限的API密钥进行数据采集
- 交易权限的API密钥需要严格保管

## 📈 数据存储

采集的数据会自动保存到PostgreSQL数据库的`klines`表中，包含：
- 交易所名称
- 交易对
- 时间间隔
- OHLCV数据（开高低收量）
- 时间戳

可以通过以下方式查询：
```sql
SELECT * FROM klines 
WHERE exchange = 'binance_public' 
  AND symbol = 'BTC/USDT' 
  AND interval = '1h'
ORDER BY timestamp DESC 
LIMIT 100;
```

## 🆘 常见问题

### Q: 数据采集失败？
A: 检查网络连接，某些交易所可能需要代理访问

### Q: 如何提高采集速度？
A: 使用Celery异步任务，并行采集多个交易对

### Q: 数据延迟多少？
A: 
- CCXT公开数据：实时
- Yahoo Finance：15分钟延迟
- Tushare：日线数据T+1

### Q: 可以采集多长时间的历史数据？
A: 
- 加密货币：通常2-3年
- 股票：10年以上
- 具体限制取决于数据源

## 📚 更多资源

- CCXT文档：https://docs.ccxt.com/
- Yahoo Finance：https://pypi.org/project/yfinance/
- Tushare文档：https://tushare.pro/document/2
- AKShare文档：https://akshare.akfamily.xyz/
