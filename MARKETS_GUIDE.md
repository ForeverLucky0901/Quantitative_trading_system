# 多市场数据接入指南

## 🌍 支持的市场

### 1. 加密货币市场 💰

#### 支持的交易所（8个）

| 交易所 | 代码 | 说明 | 需要API密钥 |
|--------|------|------|-------------|
| Binance | `binance_public` | 全球最大，流动性最好 | ❌ |
| Coinbase | `coinbase` | 美国最大合规交易所 | ❌ |
| Kraken | `kraken` | 欧洲老牌交易所 | ❌ |
| Bybit | `bybit` | 衍生品交易所 | ❌ |
| OKX | `okx` | 全球领先交易所 | ❌ |
| Huobi | `huobi` | 老牌交易所 | ❌ |
| Gate.io | `gateio` | 币种丰富 | ❌ |
| KuCoin | `kucoin` | 人民的交易所 | ❌ |

#### 热门交易对
```
BTC/USDT, ETH/USDT, BNB/USDT, SOL/USDT, XRP/USDT
ADA/USDT, DOGE/USDT, AVAX/USDT, DOT/USDT, MATIC/USDT
```

#### API示例
```bash
# 获取交易所列表
GET /api/v1/markets/crypto/exchanges

# 获取交易对列表
GET /api/v1/markets/crypto/symbols?exchange=binance_public

# 获取实时行情
GET /api/v1/markets/crypto/ticker?exchange=binance_public&symbol=BTC/USDT
```

---

### 2. 美国股市 🇺🇸

#### 市场代码：`US`

#### 主要指数
- **S&P 500** (`^GSPC`)
- **道琼斯** (`^DJI`)
- **纳斯达克** (`^IXIC`)

#### 热门股票

**科技股：**
- AAPL - Apple Inc. (苹果)
- MSFT - Microsoft Corporation (微软)
- GOOGL - Alphabet Inc. (谷歌)
- AMZN - Amazon.com Inc. (亚马逊)
- META - Meta Platforms Inc. (Meta)
- NVDA - NVIDIA Corporation (英伟达)
- TSLA - Tesla Inc. (特斯拉)

**金融股：**
- JPM - JPMorgan Chase (摩根大通)
- BAC - Bank of America (美国银行)
- WFC - Wells Fargo (富国银行)
- GS - Goldman Sachs (高盛)

#### API示例
```bash
# 获取美股列表
GET /api/v1/markets/stocks/us

# 获取股票数据
GET /api/v1/markets/stocks/data?symbol=AAPL&market=US&start_date=2024-01-01&end_date=2024-12-31
```

---

### 3. 香港股市 🇭🇰

#### 市场代码：`HK`

#### 主要指数
- **恒生指数** (`^HSI`)
- **恒生中国企业指数** (`^HSCE`)

#### 热门股票

**科技股：**
- 0700.HK - 腾讯控股
- 9988.HK - 阿里巴巴
- 1810.HK - 小米集团
- 9618.HK - 京东集团
- 3690.HK - 美团

**金融股：**
- 0005.HK - 汇丰控股
- 0939.HK - 建设银行
- 1398.HK - 工商银行
- 3988.HK - 中国银行

**地产股：**
- 0001.HK - 长和
- 0002.HK - 中电控股
- 0003.HK - 香港中华煤气

#### API示例
```bash
# 获取港股列表
GET /api/v1/markets/stocks/hk

# 获取股票数据（腾讯）
GET /api/v1/markets/stocks/data?symbol=0700&market=HK
```

---

### 4. A股市场 🇨🇳

#### 市场代码：`CN`（上海）、`SZ`（深圳）

#### 主要指数
- **上证指数** (`000001.SS`)
- **深证成指** (`399001.SZ`)
- **创业板指** (`399006.SZ`)

#### 热门股票

**上海交易所（CN）：**
- 600519.SS - 贵州茅台
- 600036.SS - 招商银行
- 601318.SS - 中国平安
- 600887.SS - 伊利股份
- 601888.SS - 中国中免

**深圳交易所（SZ）：**
- 000001.SZ - 平安银行
- 000002.SZ - 万科A
- 000858.SZ - 五粮液
- 000333.SZ - 美的集团
- 002594.SZ - 比亚迪

#### API示例
```bash
# 获取A股列表
GET /api/v1/markets/stocks/cn

# 获取股票数据（贵州茅台）
GET /api/v1/markets/stocks/data?symbol=600519&market=CN

# 获取股票数据（比亚迪）
GET /api/v1/markets/stocks/data?symbol=002594&market=SZ
```

---

### 5. 新加坡股市 🇸🇬

#### 市场代码：`SG`

#### 主要指数
- **海峡时报指数** (`^STI`)

#### 热门股票（STI成分股）

**银行股：**
- D05.SI - DBS Group Holdings (星展银行)
- O39.SI - Oversea-Chinese Banking Corp (华侨银行)
- U11.SI - United Overseas Bank (大华银行)

**其他蓝筹股：**
- Z74.SI - Singapore Telecommunications (新加坡电信)
- C6L.SI - Singapore Airlines (新加坡航空)
- BN4.SI - Keppel Corporation (吉宝集团)
- C52.SI - ComfortDelGro Corporation (康福德高)
- S68.SI - Singapore Exchange (新加坡交易所)

#### API示例
```bash
# 获取新加坡股票列表
GET /api/v1/markets/stocks/sg

# 获取股票数据（星展银行）
GET /api/v1/markets/stocks/data?symbol=D05&market=SG
```

---

## 📊 统一API接口

### 1. 获取市场概览
```bash
GET /api/v1/markets/summary
```

返回所有支持的市场信息。

### 2. 获取股票历史数据
```bash
GET /api/v1/markets/stocks/data
```

**参数：**
- `symbol` - 股票代码（必填）
- `market` - 市场代码：US, HK, CN, SZ, SG（必填）
- `start_date` - 开始日期 YYYY-MM-DD（可选，默认30天前）
- `end_date` - 结束日期 YYYY-MM-DD（可选，默认今天）
- `interval` - 时间间隔：1d, 1wk, 1mo（可选，默认1d）

**示例：**
```bash
# 美股苹果
GET /api/v1/markets/stocks/data?symbol=AAPL&market=US

# 港股腾讯
GET /api/v1/markets/stocks/data?symbol=0700&market=HK

# A股茅台
GET /api/v1/markets/stocks/data?symbol=600519&market=CN

# 新加坡星展银行
GET /api/v1/markets/stocks/data?symbol=D05&market=SG
```

---

## 🔧 使用示例

### Python示例

```python
import requests

# 获取美股苹果数据
response = requests.get(
    'http://localhost:8000/api/v1/markets/stocks/data',
    params={
        'symbol': 'AAPL',
        'market': 'US',
        'start_date': '2024-01-01',
        'end_date': '2024-12-31'
    }
)
data = response.json()
print(f"获取到 {data['count']} 条数据")

# 获取加密货币行情
response = requests.get(
    'http://localhost:8000/api/v1/markets/crypto/ticker',
    params={
        'exchange': 'binance_public',
        'symbol': 'BTC/USDT'
    }
)
ticker = response.json()
print(f"BTC价格: ${ticker['last']}")
```

### JavaScript示例

```javascript
// 获取港股腾讯数据
const response = await fetch(
  '/api/v1/markets/stocks/data?symbol=0700&market=HK'
);
const data = await response.json();
console.log(`获取到 ${data.count} 条数据`);

// 获取加密货币交易所列表
const exchanges = await fetch('/api/v1/markets/crypto/exchanges');
const exchangeData = await exchanges.json();
console.log(`支持 ${exchangeData.total} 个交易所`);
```

---

## 📈 数据格式

### 股票数据格式
```json
{
  "symbol": "AAPL",
  "market": "US",
  "interval": "1d",
  "data": [
    {
      "date": "2024-01-01",
      "open": 185.50,
      "high": 187.20,
      "low": 184.80,
      "close": 186.90,
      "volume": 45678900
    }
  ],
  "count": 252
}
```

### 加密货币行情格式
```json
{
  "symbol": "BTC/USDT",
  "last": 42000.50,
  "bid": 41999.00,
  "ask": 42001.00,
  "high": 43500.00,
  "low": 41000.00,
  "volume": 25000.5,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🎯 策略示例

### 跨市场套利策略
```python
# 同时监控美股和港股的同一公司
us_data = get_stock_data('BABA', 'US')  # 阿里巴巴美股
hk_data = get_stock_data('9988', 'HK')  # 阿里巴巴港股

# 寻找套利机会
if us_data['close'] > hk_data['close'] * exchange_rate:
    # 买入港股，卖出美股
    pass
```

### 加密货币与股票对冲
```python
# 监控加密货币相关股票
btc_price = get_crypto_ticker('binance_public', 'BTC/USDT')
coin_stock = get_stock_data('COIN', 'US')  # Coinbase股票

# 对冲策略
if btc_price['change'] > 5 and coin_stock['change'] < 2:
    # 买入COIN股票
    pass
```

---

## 💡 最佳实践

### 1. 数据缓存
```python
# 使用Redis缓存行情数据，减少API调用
cache_key = f"ticker:{exchange}:{symbol}"
cached_data = redis.get(cache_key)
if cached_data:
    return cached_data
else:
    data = fetch_ticker(exchange, symbol)
    redis.setex(cache_key, 60, data)  # 缓存60秒
    return data
```

### 2. 批量获取
```python
# 批量获取多个股票数据
symbols = ['AAPL', 'MSFT', 'GOOGL']
for symbol in symbols:
    data = get_stock_data(symbol, 'US')
    # 处理数据
```

### 3. 错误处理
```python
try:
    data = get_stock_data(symbol, market)
except Exception as e:
    logger.error(f"Failed to fetch data: {e}")
    # 使用备用数据源或缓存数据
```

---

## 🔒 注意事项

1. **数据延迟**
   - Yahoo Finance数据有15分钟延迟
   - 加密货币数据实时

2. **API限制**
   - 公开API有请求频率限制
   - 建议使用缓存减少请求

3. **交易时间**
   - 美股：周一至周五 9:30-16:00 EST
   - 港股：周一至周五 9:30-16:00 HKT
   - A股：周一至周五 9:30-15:00 CST
   - 新加坡：周一至周五 9:00-17:00 SGT
   - 加密货币：24/7

4. **数据质量**
   - 建议对数据进行清洗和验证
   - 注意处理停牌、除权等特殊情况

---

## 📚 相关文档

- [数据采集指南](DATA_SOURCES.md)
- [前后端联调指南](INTEGRATION_GUIDE.md)
- [API文档](http://localhost:8000/docs)
