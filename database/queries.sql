-- 量化交易系统 - 常用SQL查询

-- ============================================
-- 1. 用户相关查询
-- ============================================

-- 查看所有用户
SELECT id, username, email, is_active, is_superuser, created_at 
FROM users 
ORDER BY created_at DESC;

-- 查看用户的策略数量
SELECT 
    u.username,
    COUNT(s.id) as strategy_count,
    COUNT(CASE WHEN s.status = 'running' THEN 1 END) as running_count
FROM users u
LEFT JOIN strategies s ON u.id = s.user_id
GROUP BY u.id, u.username;

-- ============================================
-- 2. 策略相关查询
-- ============================================

-- 查看所有策略及其状态
SELECT 
    s.id,
    s.name,
    s.status,
    u.username as owner,
    s.created_at
FROM strategies s
JOIN users u ON s.user_id = u.id
ORDER BY s.created_at DESC;

-- 查看策略的交易统计
SELECT 
    s.name as strategy_name,
    COUNT(DISTINCT o.id) as total_orders,
    COUNT(DISTINCT CASE WHEN o.status = 'filled' THEN o.id END) as filled_orders,
    COUNT(DISTINCT t.id) as total_trades,
    COALESCE(SUM(t.pnl), 0) as total_pnl
FROM strategies s
LEFT JOIN orders o ON s.id = o.strategy_id
LEFT JOIN trades t ON s.id = t.strategy_id
GROUP BY s.id, s.name;

-- 查看正在运行的策略
SELECT id, name, status, created_at 
FROM strategies 
WHERE status = 'running';

-- ============================================
-- 3. 订单相关查询
-- ============================================

-- 查看最近的订单
SELECT 
    o.id,
    s.name as strategy,
    o.exchange,
    o.symbol,
    o.side,
    o.order_type,
    o.price,
    o.amount,
    o.filled,
    o.status,
    o.created_at
FROM orders o
JOIN strategies s ON o.strategy_id = s.id
ORDER BY o.created_at DESC
LIMIT 50;

-- 按状态统计订单
SELECT 
    status,
    COUNT(*) as count,
    SUM(amount) as total_amount
FROM orders
GROUP BY status;

-- 查看未完成的订单
SELECT 
    o.id,
    s.name as strategy,
    o.symbol,
    o.side,
    o.price,
    o.amount,
    o.filled,
    o.status,
    o.created_at
FROM orders o
JOIN strategies s ON o.strategy_id = s.id
WHERE o.status IN ('pending', 'partial')
ORDER BY o.created_at DESC;

-- 按交易对统计订单
SELECT 
    symbol,
    COUNT(*) as order_count,
    SUM(CASE WHEN side = 'buy' THEN 1 ELSE 0 END) as buy_count,
    SUM(CASE WHEN side = 'sell' THEN 1 ELSE 0 END) as sell_count
FROM orders
GROUP BY symbol
ORDER BY order_count DESC;

-- ============================================
-- 4. 持仓相关查询
-- ============================================

-- 查看当前所有持仓
SELECT 
    p.id,
    s.name as strategy,
    p.exchange,
    p.symbol,
    p.side,
    p.amount,
    p.entry_price,
    p.current_price,
    p.unrealized_pnl,
    p.realized_pnl,
    (p.unrealized_pnl + p.realized_pnl) as total_pnl,
    ROUND(((p.current_price - p.entry_price) / p.entry_price * 100)::numeric, 2) as pnl_percent
FROM positions p
JOIN strategies s ON p.strategy_id = s.id
ORDER BY total_pnl DESC;

-- 按策略汇总持仓
SELECT 
    s.name as strategy,
    COUNT(p.id) as position_count,
    SUM(p.unrealized_pnl + p.realized_pnl) as total_pnl
FROM strategies s
LEFT JOIN positions p ON s.id = p.strategy_id
GROUP BY s.id, s.name
ORDER BY total_pnl DESC;

-- 查看盈利的持仓
SELECT * FROM position_summary
WHERE total_pnl > 0
ORDER BY total_pnl DESC;

-- 查看亏损的持仓
SELECT * FROM position_summary
WHERE total_pnl < 0
ORDER BY total_pnl ASC;

-- ============================================
-- 5. 成交记录查询
-- ============================================

-- 查看最近的成交记录
SELECT 
    t.id,
    s.name as strategy,
    t.exchange,
    t.symbol,
    t.side,
    t.price,
    t.amount,
    t.fee,
    t.pnl,
    t.created_at
FROM trades t
JOIN strategies s ON t.strategy_id = s.id
ORDER BY t.created_at DESC
LIMIT 100;

-- 按日期统计成交
SELECT 
    DATE(created_at) as trade_date,
    COUNT(*) as trade_count,
    SUM(amount * price) as total_volume,
    SUM(pnl) as total_pnl
FROM trades
GROUP BY DATE(created_at)
ORDER BY trade_date DESC;

-- 按交易对统计成交
SELECT 
    symbol,
    COUNT(*) as trade_count,
    SUM(amount * price) as total_volume,
    SUM(pnl) as total_pnl,
    AVG(pnl) as avg_pnl
FROM trades
GROUP BY symbol
ORDER BY total_pnl DESC;

-- 查看今日成交
SELECT 
    t.*,
    s.name as strategy_name
FROM trades t
JOIN strategies s ON t.strategy_id = s.id
WHERE DATE(t.created_at) = CURRENT_DATE
ORDER BY t.created_at DESC;

-- ============================================
-- 6. K线数据查询
-- ============================================

-- 查看某个交易对的最新K线
SELECT *
FROM klines
WHERE exchange = 'binance_public' 
  AND symbol = 'BTC/USDT' 
  AND interval = '1h'
ORDER BY timestamp DESC
LIMIT 100;

-- 统计K线数据量
SELECT 
    exchange,
    symbol,
    interval,
    COUNT(*) as kline_count,
    MIN(timestamp) as earliest,
    MAX(timestamp) as latest
FROM klines
GROUP BY exchange, symbol, interval
ORDER BY kline_count DESC;

-- 查看数据缺失
SELECT 
    exchange,
    symbol,
    interval,
    DATE(timestamp) as date,
    COUNT(*) as count
FROM klines
WHERE interval = '1d'
GROUP BY exchange, symbol, interval, DATE(timestamp)
HAVING COUNT(*) < 24
ORDER BY date DESC;

-- ============================================
-- 7. 回测相关查询
-- ============================================

-- 查看所有回测结果
SELECT 
    b.id,
    s.name as strategy,
    b.start_date,
    b.end_date,
    b.initial_capital,
    b.final_capital,
    b.total_return,
    b.sharpe_ratio,
    b.max_drawdown,
    b.win_rate,
    b.total_trades,
    b.created_at
FROM backtests b
JOIN strategies s ON b.strategy_id = s.id
ORDER BY b.created_at DESC;

-- 查看最佳回测结果
SELECT 
    s.name as strategy,
    b.total_return,
    b.sharpe_ratio,
    b.max_drawdown,
    b.win_rate,
    b.created_at
FROM backtests b
JOIN strategies s ON b.strategy_id = s.id
WHERE b.total_return IS NOT NULL
ORDER BY b.total_return DESC
LIMIT 10;

-- 按策略统计回测次数
SELECT 
    s.name as strategy,
    COUNT(b.id) as backtest_count,
    AVG(b.total_return) as avg_return,
    MAX(b.total_return) as max_return
FROM strategies s
LEFT JOIN backtests b ON s.id = b.strategy_id
GROUP BY s.id, s.name
ORDER BY backtest_count DESC;

-- ============================================
-- 8. 性能分析查询
-- ============================================

-- 查看每日交易统计
SELECT 
    DATE(created_at) as date,
    COUNT(DISTINCT strategy_id) as active_strategies,
    COUNT(*) as total_trades,
    SUM(pnl) as daily_pnl,
    SUM(fee) as total_fees
FROM trades
GROUP BY DATE(created_at)
ORDER BY date DESC
LIMIT 30;

-- 查看策略胜率
SELECT 
    s.name as strategy,
    COUNT(t.id) as total_trades,
    COUNT(CASE WHEN t.pnl > 0 THEN 1 END) as winning_trades,
    ROUND((COUNT(CASE WHEN t.pnl > 0 THEN 1 END)::numeric / 
           NULLIF(COUNT(t.id), 0) * 100), 2) as win_rate,
    SUM(t.pnl) as total_pnl
FROM strategies s
LEFT JOIN trades t ON s.id = t.strategy_id
GROUP BY s.id, s.name
HAVING COUNT(t.id) > 0
ORDER BY win_rate DESC;

-- 查看最活跃的交易对
SELECT 
    symbol,
    COUNT(*) as trade_count,
    SUM(amount * price) as volume,
    COUNT(DISTINCT strategy_id) as strategy_count
FROM trades
WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY symbol
ORDER BY trade_count DESC
LIMIT 20;

-- ============================================
-- 9. 数据维护查询
-- ============================================

-- 清理旧的K线数据（保留最近1年）
-- DELETE FROM klines 
-- WHERE timestamp < CURRENT_DATE - INTERVAL '1 year';

-- 归档旧订单（示例，需要先创建归档表）
-- INSERT INTO orders_archive 
-- SELECT * FROM orders 
-- WHERE created_at < CURRENT_DATE - INTERVAL '1 year';

-- 查看表大小
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    pg_total_relation_size(schemaname||'.'||tablename) AS size_bytes
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY size_bytes DESC;

-- 查看索引使用情况
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- ============================================
-- 10. 实用查询
-- ============================================

-- 查看系统概览
SELECT 
    (SELECT COUNT(*) FROM users) as total_users,
    (SELECT COUNT(*) FROM strategies) as total_strategies,
    (SELECT COUNT(*) FROM strategies WHERE status = 'running') as running_strategies,
    (SELECT COUNT(*) FROM orders) as total_orders,
    (SELECT COUNT(*) FROM trades) as total_trades,
    (SELECT COUNT(*) FROM positions) as open_positions,
    (SELECT SUM(unrealized_pnl + realized_pnl) FROM positions) as total_pnl;

-- 查看今日概览
SELECT 
    COUNT(DISTINCT o.id) as today_orders,
    COUNT(DISTINCT t.id) as today_trades,
    COALESCE(SUM(t.pnl), 0) as today_pnl,
    COALESCE(SUM(t.fee), 0) as today_fees
FROM orders o
LEFT JOIN trades t ON o.id = t.order_id
WHERE DATE(o.created_at) = CURRENT_DATE;
