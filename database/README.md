# 数据库文档

## 📊 数据库结构

### 表列表

1. **users** - 用户表
2. **strategies** - 策略表
3. **backtests** - 回测结果表
4. **orders** - 订单表
5. **positions** - 持仓表
6. **trades** - 成交记录表
7. **klines** - K线数据表

## 🚀 快速开始

### 方式一：使用 init_db.py（推荐）

```bash
cd backend
python init_db.py
```

这会自动创建所有表结构。

### 方式二：手动执行SQL

```bash
# 连接到数据库
psql -U postgres -d quant_trading

# 执行SQL文件
\i /Users/lucky/Desktop/Quantitative_trading_system/database/schema.sql
```

## 📋 表结构详情

### 1. users（用户表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| username | VARCHAR(50) | 用户名（唯一） |
| email | VARCHAR(100) | 邮箱（唯一） |
| hashed_password | VARCHAR(255) | 加密密码 |
| is_active | BOOLEAN | 是否激活 |
| is_superuser | BOOLEAN | 是否超级用户 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

**测试账号**：
- 用户名：`admin` / 密码：`admin123`
- 用户名：`test_user` / 密码：`admin123`

### 2. strategies（策略表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| user_id | INTEGER | 用户ID（外键） |
| name | VARCHAR(100) | 策略名称 |
| description | TEXT | 策略描述 |
| code | TEXT | 策略代码 |
| params | JSONB | 策略参数（JSON） |
| status | VARCHAR(20) | 状态：running/stopped/error |
| is_backtest | BOOLEAN | 是否为回测策略 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### 3. orders（订单表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| strategy_id | INTEGER | 策略ID（外键） |
| exchange | VARCHAR(50) | 交易所 |
| symbol | VARCHAR(50) | 交易对 |
| order_type | VARCHAR(20) | 订单类型：market/limit |
| side | VARCHAR(10) | 方向：buy/sell |
| price | DECIMAL(20,8) | 价格 |
| amount | DECIMAL(20,8) | 数量 |
| filled | DECIMAL(20,8) | 已成交数量 |
| status | VARCHAR(20) | 状态：pending/filled/partial/cancelled |
| order_id | VARCHAR(100) | 交易所订单ID |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### 4. positions（持仓表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| strategy_id | INTEGER | 策略ID（外键） |
| exchange | VARCHAR(50) | 交易所 |
| symbol | VARCHAR(50) | 交易对 |
| side | VARCHAR(10) | 方向：long/short |
| amount | DECIMAL(20,8) | 持仓数量 |
| entry_price | DECIMAL(20,8) | 开仓均价 |
| current_price | DECIMAL(20,8) | 当前价格 |
| unrealized_pnl | DECIMAL(20,8) | 未实现盈亏 |
| realized_pnl | DECIMAL(20,8) | 已实现盈亏 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### 5. trades（成交记录表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| order_id | INTEGER | 订单ID（外键） |
| strategy_id | INTEGER | 策略ID（外键） |
| exchange | VARCHAR(50) | 交易所 |
| symbol | VARCHAR(50) | 交易对 |
| side | VARCHAR(10) | 方向：buy/sell |
| price | DECIMAL(20,8) | 成交价格 |
| amount | DECIMAL(20,8) | 成交数量 |
| fee | DECIMAL(20,8) | 手续费 |
| pnl | DECIMAL(20,8) | 盈亏 |
| trade_id | VARCHAR(100) | 交易所成交ID |
| created_at | TIMESTAMP | 创建时间 |

### 6. klines（K线数据表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| exchange | VARCHAR(50) | 交易所 |
| symbol | VARCHAR(50) | 交易对 |
| interval | VARCHAR(10) | 周期：1m/5m/15m/1h/4h/1d |
| timestamp | TIMESTAMP | K线时间戳 |
| open | DECIMAL(20,8) | 开盘价 |
| high | DECIMAL(20,8) | 最高价 |
| low | DECIMAL(20,8) | 最低价 |
| close | DECIMAL(20,8) | 收盘价 |
| volume | DECIMAL(30,8) | 成交量 |
| created_at | TIMESTAMP | 创建时间 |

**重要索引**：
```sql
CREATE UNIQUE INDEX idx_klines_unique 
ON klines(exchange, symbol, interval, timestamp);
```

### 7. backtests（回测结果表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| strategy_id | INTEGER | 策略ID（外键） |
| start_date | DATE | 回测开始日期 |
| end_date | DATE | 回测结束日期 |
| initial_capital | DECIMAL(20,2) | 初始资金 |
| final_capital | DECIMAL(20,2) | 最终资金 |
| total_return | DECIMAL(10,4) | 总收益率 |
| sharpe_ratio | DECIMAL(10,4) | 夏普比率 |
| max_drawdown | DECIMAL(10,4) | 最大回撤 |
| win_rate | DECIMAL(10,4) | 胜率 |
| total_trades | INTEGER | 总交易次数 |
| result_data | JSONB | 详细回测数据 |
| created_at | TIMESTAMP | 创建时间 |

## 📈 视图

### strategy_stats（策略统计视图）

汇总每个策略的订单、成交和盈亏统计。

```sql
SELECT * FROM strategy_stats;
```

### position_summary（持仓汇总视图）

显示所有持仓的详细信息和盈亏百分比。

```sql
SELECT * FROM position_summary;
```

## 🔍 常用查询

查看 `queries.sql` 文件获取更多示例。

### 快速查询示例

```sql
-- 查看系统概览
SELECT 
    (SELECT COUNT(*) FROM users) as total_users,
    (SELECT COUNT(*) FROM strategies) as total_strategies,
    (SELECT COUNT(*) FROM orders) as total_orders,
    (SELECT SUM(unrealized_pnl + realized_pnl) FROM positions) as total_pnl;

-- 查看最近的交易
SELECT * FROM trades ORDER BY created_at DESC LIMIT 10;

-- 查看当前持仓
SELECT * FROM position_summary ORDER BY total_pnl DESC;
```

## 🛠️ 数据维护

### 备份数据库

```bash
pg_dump quant_trading > backup_$(date +%Y%m%d).sql
```

### 恢复数据库

```bash
psql quant_trading < backup_20241206.sql
```

### 清理旧数据

```sql
-- 清理1年前的K线数据
DELETE FROM klines WHERE timestamp < CURRENT_DATE - INTERVAL '1 year';

-- 清理已取消的订单
DELETE FROM orders WHERE status = 'cancelled' AND created_at < CURRENT_DATE - INTERVAL '3 months';
```

## 📊 性能优化

### 重要索引

系统已创建以下关键索引：

- `idx_klines_unique` - K线数据唯一索引
- `idx_orders_strategy_id` - 订单策略索引
- `idx_trades_created_at` - 成交时间索引
- `idx_positions_symbol` - 持仓交易对索引

### 查看索引使用情况

```sql
SELECT * FROM pg_stat_user_indexes ORDER BY idx_scan DESC;
```

### 分析表

```sql
ANALYZE users;
ANALYZE strategies;
ANALYZE orders;
ANALYZE positions;
ANALYZE trades;
ANALYZE klines;
```

## 🔐 安全建议

1. **修改默认密码**：生产环境必须修改数据库密码
2. **限制访问**：只允许应用服务器访问数据库
3. **定期备份**：每天自动备份数据库
4. **加密连接**：使用SSL连接数据库
5. **最小权限**：应用使用的数据库用户只给必要权限

## 📞 故障排查

### 连接失败

```bash
# 检查PostgreSQL是否运行
brew services list | grep postgresql

# 重启PostgreSQL
brew services restart postgresql@14
```

### 查看日志

```bash
# PostgreSQL日志位置
tail -f /usr/local/var/log/postgresql@14.log
```

### 重置数据库

```bash
# 删除并重建数据库
dropdb quant_trading
createdb quant_trading
python init_db.py
```
