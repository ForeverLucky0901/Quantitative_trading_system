# 量化交易系统 (Quantitative Trading System)

一个功能完整的量化交易系统，支持策略回测、实时交易、风险控制等核心功能。

## 技术栈

### 后端
- **Python 3.10+**
- **FastAPI** - 高性能异步Web框架
- **SQLAlchemy** - ORM数据库操作
- **PostgreSQL** - 主数据库
- **Redis** - 缓存和消息队列
- **Celery** - 异步任务处理
- **pandas/numpy** - 数据分析
- **TA-Lib** - 技术指标计算
- **ccxt** - 交易所API统一接口

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具
- **Element Plus** - UI组件库
- **ECharts** - 数据可视化
- **Pinia** - 状态管理

## 核心功能

### 1. 策略管理
- 策略编写和编辑
- 策略参数配置
- 策略启动/停止
- 策略性能监控

### 2. 回测系统
- 历史数据回测
- 多策略对比
- 性能指标分析（夏普比率、最大回撤等）
- 回测报告生成

### 3. 实时交易
- 多交易所支持
- 实时行情订阅
- 自动下单执行
- 订单管理

### 4. 风险控制
- 仓位管理
- 止损止盈
- 资金监控
- 风险预警

### 5. 数据分析
- K线图表展示
- 技术指标计算
- 收益曲线分析
- 交易记录统计

## 项目结构

```
.
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据库模型
│   │   ├── schemas/        # Pydantic模型
│   │   ├── services/       # 业务逻辑
│   │   ├── strategies/     # 交易策略
│   │   └── utils/          # 工具函数
│   ├── tests/              # 测试代码
│   ├── requirements.txt    # Python依赖
│   └── main.py            # 入口文件
│
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── api/           # API接口
│   │   ├── components/    # 组件
│   │   ├── views/         # 页面
│   │   ├── stores/        # 状态管理
│   │   ├── router/        # 路由
│   │   └── utils/         # 工具函数
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml      # Docker编排
└── README.md
```

## 快速开始

### 环境要求
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库等信息

# 初始化数据库
python init_db.py

# 启动服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### Docker启动（推荐）

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## API文档

启动后端服务后，访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 配置说明

### 后端配置 (.env)

```env
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/quant_trading

# Redis配置
REDIS_URL=redis://localhost:6379/0

# JWT密钥
SECRET_KEY=your-secret-key-here

# 交易所API配置
BINANCE_API_KEY=your-api-key
BINANCE_API_SECRET=your-api-secret
```

## 开发指南

### 添加新策略

1. 在 `backend/app/strategies/` 创建策略文件
2. 继承 `BaseStrategy` 类
3. 实现 `on_bar()` 方法
4. 在策略管理界面配置和启动

示例：

```python
from app.strategies.base import BaseStrategy

class MyStrategy(BaseStrategy):
    def __init__(self, params):
        super().__init__(params)
        self.ma_period = params.get('ma_period', 20)
    
    def on_bar(self, bar):
        # 策略逻辑
        if self.should_buy():
            self.buy(bar.close, quantity=1)
        elif self.should_sell():
            self.sell(bar.close, quantity=1)
```

## 安全建议

- 不要将API密钥提交到代码仓库
- 使用环境变量管理敏感信息
- 启用双因素认证
- 设置合理的风控参数
- 定期备份数据库

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题，请提交Issue或联系开发团队。
# Quantitative_trading_system
