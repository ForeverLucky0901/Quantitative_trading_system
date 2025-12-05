-- 量化交易系统数据库表结构
-- PostgreSQL 14+

-- 删除已存在的表（开发环境使用，生产环境请谨慎）
DROP TABLE IF EXISTS trades CASCADE;
DROP TABLE IF EXISTS positions CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS backtests CASCADE;
DROP TABLE IF EXISTS strategies CASCADE;
DROP TABLE IF EXISTS klines CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ============================================
-- 1. 用户表
-- ============================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用户表索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- 用户表注释
COMMENT ON TABLE users IS '用户表';
COMMENT ON COLUMN users.id IS '用户ID';
COMMENT ON COLUMN users.username IS '用户名';
COMMENT ON COLUMN users.email IS '邮箱';
COMMENT ON COLUMN users.hashed_password IS '加密后的密码';
COMMENT ON COLUMN users.is_active IS '是否激活';
COMMENT ON COLUMN users.is_superuser IS '是否超级用户';

-- ============================================
-- 2. 策略表
-- ============================================
CREATE TABLE strategies (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    code TEXT NOT NULL,
    params JSONB,
    status VARCHAR(20) DEFAULT 'stopped',
    is_backtest BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 策略表索引
CREATE INDEX idx_strategies_user_id ON strategies(user_id);
CREATE INDEX idx_strategies_status ON strategies(status);

-- 策略表注释
COMMENT ON TABLE strategies IS '交易策略表';
COMMENT ON COLUMN strategies.id IS '策略ID';
COMMENT ON COLUMN strategies.user_id IS '用户ID';
COMMENT ON COLUMN strategies.name IS '策略名称';
COMMENT ON COLUMN strategies.description IS '策略描述';
COMMENT ON COLUMN strategies.code IS '策略代码';
COMMENT ON COLUMN strategies.params IS '策略参数（JSON格式）';
COMMENT ON COLUMN strategies.status IS '策略状态：running, stopped, error';

-- ============================================
-- 3. 回测结果表
-- ============================================
CREATE TABLE backtests (
    id SERIAL PRIMARY KEY,
    strategy_id INTEGER NOT NULL REFERENCES strategies(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    initial_capital DECIMAL(20, 2) DEFAULT 100000.00,
    final_capital DECIMAL(20, 2),
    total_return DECIMAL(10, 4),
    sharpe_ratio DECIMAL(10, 4),
    max_drawdown DECIMAL(10, 4),
    win_rate DECIMAL(10, 4),
    total_trades INTEGER,
    result_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 回测表索引
CREATE INDEX idx_backtests_strategy_id ON backtests(strategy_id);
CREATE INDEX idx_backtests_created_at ON backtests(created_at DESC);

-- 回测表注释
COMMENT ON TABLE backtests IS '策略回测结果表';
COMMENT ON COLUMN backtests.initial_capital IS '初始资金';
COMMENT ON COLUMN backtests.final_capital IS '最终资金';
COMMENT ON COLUMN backtests.total_return IS '总收益率';
COMMENT ON COLUMN backtests.sharpe_ratio IS '夏普比率';
COMMENT ON COLUMN backtests.max_drawdown IS '最大回撤';
COMMENT ON COLUMN backtests.win_rate IS '胜率';
COMMENT ON COLUMN backtests.result_data IS '详细回测数据（JSON格式）';

-- ============================================
-- 4. 订单表
-- ============================================
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    strategy_id INTEGER NOT NULL REFERENCES strategies(id) ON DELETE CASCADE,
    exchange VARCHAR(50) NOT NULL,
    symbol VARCHAR(50) NOT NULL,
    order_type VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    price DECIMAL(20, 8),
    amount DECIMAL(20, 8) NOT NULL,
    filled DECIMAL(20, 8) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending',
    order_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 订单表索引
CREATE INDEX idx_orders_strategy_id ON orders(strategy_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_symbol ON orders(symbol);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);

-- 订单表注释
COMMENT ON TABLE orders IS '交易订单表';
COMMENT ON COLUMN orders.exchange IS '交易所名称';
COMMENT ON COLUMN orders.symbol IS '交易对（如 BTC/USDT）';
COMMENT ON COLUMN orders.order_type IS '订单类型：market, limit';
COMMENT ON COLUMN orders.side IS '买卖方向：buy, sell';
COMMENT ON COLUMN orders.price IS '价格';
COMMENT ON COLUMN orders.amount IS '数量';
COMMENT ON COLUMN orders.filled IS '已成交数量';
COMMENT ON COLUMN orders.status IS '订单状态：pending, filled, partial, cancelled';
COMMENT ON COLUMN orders.order_id IS '交易所订单ID';

-- ============================================
-- 5. 持仓表
-- ============================================
CREATE TABLE positions (
    id SERIAL PRIMARY KEY,
    strategy_id INTEGER NOT NULL REFERENCES strategies(id) ON DELETE CASCADE,
    exchange VARCHAR(50) NOT NULL,
    symbol VARCHAR(50) NOT NULL,
    side VARCHAR(10) NOT NULL,
    amount DECIMAL(20, 8) NOT NULL,
    entry_price DECIMAL(20, 8) NOT NULL,
    current_price DECIMAL(20, 8),
    unrealized_pnl DECIMAL(20, 8) DEFAULT 0,
    realized_pnl DECIMAL(20, 8) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 持仓表索引
CREATE INDEX idx_positions_strategy_id ON positions(strategy_id);
CREATE INDEX idx_positions_symbol ON positions(symbol);

-- 持仓表注释
COMMENT ON TABLE positions IS '持仓表';
COMMENT ON COLUMN positions.side IS '持仓方向：long, short';
COMMENT ON COLUMN positions.amount IS '持仓数量';
COMMENT ON COLUMN positions.entry_price IS '开仓均价';
COMMENT ON COLUMN positions.current_price IS '当前价格';
COMMENT ON COLUMN positions.unrealized_pnl IS '未实现盈亏';
COMMENT ON COLUMN positions.realized_pnl IS '已实现盈亏';

-- ============================================
-- 6. 成交记录表
-- ============================================
CREATE TABLE trades (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    strategy_id INTEGER NOT NULL REFERENCES strategies(id) ON DELETE CASCADE,
    exchange VARCHAR(50) NOT NULL,
    symbol VARCHAR(50) NOT NULL,
    side VARCHAR(10) NOT NULL,
    price DECIMAL(20, 8) NOT NULL,
    amount DECIMAL(20, 8) NOT NULL,
    fee DECIMAL(20, 8) DEFAULT 0,
    pnl DECIMAL(20, 8),
    trade_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 成交记录表索引
CREATE INDEX idx_trades_order_id ON trades(order_id);
CREATE INDEX idx_trades_strategy_id ON trades(strategy_id);
CREATE INDEX idx_trades_symbol ON trades(symbol);
CREATE INDEX idx_trades_created_at ON trades(created_at DESC);

-- 成交记录表注释
COMMENT ON TABLE trades IS '成交记录表';
COMMENT ON COLUMN trades.fee IS '手续费';
COMMENT ON COLUMN trades.pnl IS '盈亏';
COMMENT ON COLUMN trades.trade_id IS '交易所成交ID';

-- ============================================
-- 7. K线数据表
-- ============================================
CREATE TABLE klines (
    id SERIAL PRIMARY KEY,
    exchange VARCHAR(50) NOT NULL,
    symbol VARCHAR(50) NOT NULL,
    interval VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    open DECIMAL(20, 8) NOT NULL,
    high DECIMAL(20, 8) NOT NULL,
    low DECIMAL(20, 8) NOT NULL,
    close DECIMAL(20, 8) NOT NULL,
    volume DECIMAL(30, 8) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- K线数据表索引（重要：用于快速查询）
CREATE UNIQUE INDEX idx_klines_unique ON klines(exchange, symbol, interval, timestamp);
CREATE INDEX idx_klines_symbol ON klines(symbol);
CREATE INDEX idx_klines_timestamp ON klines(timestamp DESC);

-- K线数据表注释
COMMENT ON TABLE klines IS 'K线数据表（OHLCV）';
COMMENT ON COLUMN klines.exchange IS '交易所名称';
COMMENT ON COLUMN klines.symbol IS '交易对';
COMMENT ON COLUMN klines.interval IS '时间周期：1m, 5m, 15m, 1h, 4h, 1d';
COMMENT ON COLUMN klines.timestamp IS 'K线时间戳';
COMMENT ON COLUMN klines.open IS '开盘价';
COMMENT ON COLUMN klines.high IS '最高价';
COMMENT ON COLUMN klines.low IS '最低价';
COMMENT ON COLUMN klines.close IS '收盘价';
COMMENT ON COLUMN klines.volume IS '成交量';

-- ============================================
-- 8. 插入测试数据（可选）
-- ============================================

-- 创建测试用户
INSERT INTO users (username, email, hashed_password, is_superuser) VALUES
('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVqN4qBYi', TRUE),
('test_user', 'test@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVqN4qBYi', FALSE);
-- 密码都是: admin123

-- 创建测试策略
INSERT INTO strategies (user_id, name, description, code, params, status) VALUES
(1, 'MA均线策略', '简单移动平均线交叉策略', 'def on_bar(bar): pass', '{"ma_short": 5, "ma_long": 20}', 'stopped'),
(1, 'MACD策略', 'MACD指标策略', 'def on_bar(bar): pass', '{"fast": 12, "slow": 26, "signal": 9}', 'stopped');

-- ============================================
-- 9. 视图（可选）
-- ============================================

-- 策略统计视图
CREATE OR REPLACE VIEW strategy_stats AS
SELECT 
    s.id,
    s.name,
    s.status,
    COUNT(DISTINCT o.id) as total_orders,
    COUNT(DISTINCT CASE WHEN o.status = 'filled' THEN o.id END) as filled_orders,
    COUNT(DISTINCT t.id) as total_trades,
    SUM(t.pnl) as total_pnl,
    s.created_at
FROM strategies s
LEFT JOIN orders o ON s.id = o.strategy_id
LEFT JOIN trades t ON s.id = t.strategy_id
GROUP BY s.id, s.name, s.status, s.created_at;

COMMENT ON VIEW strategy_stats IS '策略统计视图';

-- 持仓汇总视图
CREATE OR REPLACE VIEW position_summary AS
SELECT 
    p.strategy_id,
    s.name as strategy_name,
    p.exchange,
    p.symbol,
    p.side,
    p.amount,
    p.entry_price,
    p.current_price,
    p.unrealized_pnl,
    p.realized_pnl,
    (p.unrealized_pnl + p.realized_pnl) as total_pnl,
    CASE 
        WHEN p.entry_price > 0 THEN 
            ((p.current_price - p.entry_price) / p.entry_price * 100)
        ELSE 0 
    END as pnl_percent
FROM positions p
JOIN strategies s ON p.strategy_id = s.id;

COMMENT ON VIEW position_summary IS '持仓汇总视图';

-- ============================================
-- 10. 触发器（自动更新时间戳）
-- ============================================

-- 创建更新时间戳函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 为需要的表添加触发器
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_strategies_updated_at BEFORE UPDATE ON strategies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_positions_updated_at BEFORE UPDATE ON positions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 完成
-- ============================================

-- 查看所有表
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- 显示表大小
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
