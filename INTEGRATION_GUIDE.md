# 前后端联调指南

## 📋 当前状态检查

### ✅ 已完成的功能

#### 后端 API
- ✅ 用户认证 (`/api/v1/auth/*`)
  - POST `/auth/register` - 用户注册
  - POST `/auth/login` - 用户登录
  
- ✅ 用户管理 (`/api/v1/users/*`)
  - GET `/users/me` - 获取当前用户信息
  - GET `/users/{user_id}` - 获取指定用户信息

- ✅ 策略管理 (`/api/v1/strategies/*`)
  - GET `/strategies/` - 获取策略列表
  - POST `/strategies/` - 创建策略
  - GET `/strategies/{id}` - 获取策略详情
  - PUT `/strategies/{id}` - 更新策略
  - DELETE `/strategies/{id}` - 删除策略
  - POST `/strategies/{id}/start` - 启动策略
  - POST `/strategies/{id}/stop` - 停止策略
  - POST `/strategies/backtest` - 创建回测
  - GET `/strategies/backtest/{id}` - 获取回测结果

- ✅ 交易管理 (`/api/v1/trades/*`)
  - POST `/trades/orders` - 创建订单
  - GET `/trades/orders` - 获取订单列表
  - GET `/trades/orders/{id}` - 获取订单详情
  - POST `/trades/orders/{id}/cancel` - 取消订单
  - GET `/trades/positions` - 获取持仓列表
  - GET `/trades/trades` - 获取成交记录

- ✅ 行情数据 (`/api/v1/market/*`)
  - GET `/market/klines` - 获取K线数据
  - GET `/market/ticker` - 获取实时行情
  - GET `/market/symbols` - 获取交易对列表

- ✅ 数据采集 (`/api/v1/data/*`)
  - GET `/data/exchanges` - 获取支持的交易所
  - GET `/data/symbols` - 获取交易对列表
  - GET `/data/ticker` - 获取实时行情
  - GET `/data/klines` - 获取K线数据
  - POST `/data/collect` - 采集历史数据
  - GET `/data/popular-symbols` - 获取热门交易对

#### 前端功能
- ✅ API 请求封装 (`src/api/`)
  - request.ts - Axios 封装
  - auth.ts - 认证接口
  - strategy.ts - 策略接口
  - trade.ts - 交易接口
  - market.ts - 行情接口
  - data.ts - 数据采集接口

- ✅ 状态管理 (`src/stores/`)
  - user.ts - 用户状态管理

- ✅ 页面组件
  - Login.vue - 登录页面
  - Dashboard.vue - 仪表盘
  - Strategies.vue - 策略管理
  - Backtest.vue - 策略回测
  - Trading.vue - 实时交易
  - Positions.vue - 持仓管理
  - Orders.vue - 订单记录
  - Market.vue - 行情分析

### ⚠️ 需要完善的功能

#### 1. 前端页面接口联调

**需要修改的文件：**

##### Login.vue
```typescript
// 当前：使用模拟数据
// 需要：调用真实登录 API
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
await userStore.login({
  username: loginForm.username,
  password: loginForm.password
})
```

##### Dashboard.vue
```typescript
// 需要添加：
import { getStrategies, getOrders, getPositions } from '@/api'

// 获取策略统计
const strategies = await getStrategies()

// 获取最近交易
const trades = await getTrades({ limit: 10 })
```

##### Strategies.vue
```typescript
// 需要添加：
import { getStrategies, createStrategy, updateStrategy, deleteStrategy, startStrategy, stopStrategy } from '@/api'

// 获取策略列表
const loadStrategies = async () => {
  const data = await getStrategies()
  strategies.value = data
}
```

##### Backtest.vue
```typescript
// 需要添加：
import { createBacktest, getBacktest } from '@/api'

const handleBacktest = async () => {
  const result = await createBacktest({
    strategy_id: form.value.strategy_id,
    start_date: form.value.start_date,
    end_date: form.value.end_date,
    initial_capital: form.value.initial_capital
  })
  // 轮询获取回测结果
  const backtest = await getBacktest(result.id)
}
```

##### Trading.vue
```typescript
// 需要添加：
import { createOrder, getPositions } from '@/api'
import { getDataTicker, getDataKlines } from '@/api'

// 获取实时行情
const loadTicker = async () => {
  const data = await getDataTicker({
    exchange: 'binance_public',
    symbol: selectedSymbol.value
  })
  ticker.value = data
}

// 创建订单
const handleBuy = async () => {
  await createOrder({
    strategy_id: 1, // 需要选择策略
    exchange: 'binance',
    symbol: selectedSymbol.value,
    order_type: buyForm.value.orderType,
    side: 'buy',
    price: buyForm.value.price,
    amount: buyForm.value.amount
  })
}
```

##### Positions.vue
```typescript
// 需要添加：
import { getPositions } from '@/api'

const loadPositions = async () => {
  const data = await getPositions()
  positions.value = data
}
```

##### Orders.vue
```typescript
// 需要添加：
import { getOrders, cancelOrder } from '@/api'

const loadOrders = async () => {
  const data = await getOrders({
    skip: (currentPage.value - 1) * pageSize.value,
    limit: pageSize.value
  })
  orders.value = data
}
```

##### Market.vue
```typescript
// 需要添加：
import { getDataKlines, getDataTicker } from '@/api'

const loadMarketData = async () => {
  // 获取多个交易对的行情
  for (const symbol of symbols) {
    const ticker = await getDataTicker({
      exchange: 'binance_public',
      symbol: symbol
    })
    // 更新市场数据
  }
}
```

#### 2. 后端功能完善

##### 需要添加的功能：

**用户认证中间件**
```python
# backend/app/api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.core.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前登录用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_token(token)
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # 从数据库获取用户
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    return user
```

**WebSocket 实时行情推送**
```python
# backend/app/api/endpoints/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/market")
async def websocket_market(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # 接收客户端消息
            data = await websocket.receive_text()
            # 推送实时行情
            await manager.broadcast({"type": "ticker", "data": {}})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

#### 3. 数据库初始化

**创建初始数据**
```python
# backend/scripts/init_data.py
import asyncio
from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.user import User

async def init_data():
    async with AsyncSessionLocal() as db:
        # 创建测试用户
        user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_superuser=True
        )
        db.add(user)
        await db.commit()
        print("初始数据创建成功")

if __name__ == "__main__":
    asyncio.run(init_data())
```

## 🚀 联调步骤

### 1. 启动后端服务

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库连接

# 初始化数据库
python init_db.py

# 创建初始数据（可选）
python scripts/init_data.py

# 启动服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

访问 API 文档：http://localhost:8000/docs

### 2. 启动前端服务

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问前端：http://localhost:5173

### 3. 测试接口联调

#### 测试登录
1. 打开浏览器访问 http://localhost:5173/login
2. 输入用户名密码（如果创建了初始数据：admin/admin123）
3. 查看浏览器控制台，确认 API 请求成功
4. 查看 localStorage 是否保存了 token

#### 测试策略管理
1. 访问策略管理页面
2. 创建新策略
3. 查看策略列表
4. 启动/停止策略

#### 测试数据采集
1. 访问行情分析页面
2. 查看实时行情数据
3. 测试数据采集功能

## 📝 常见问题

### 1. CORS 跨域问题
**问题**：前端请求后端 API 时出现 CORS 错误

**解决**：确保后端 `main.py` 中配置了正确的 CORS：
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. 401 未授权错误
**问题**：请求 API 时返回 401 错误

**解决**：
1. 检查是否已登录
2. 检查 localStorage 中是否有 access_token
3. 检查 token 是否过期

### 3. 数据库连接失败
**问题**：后端启动时数据库连接失败

**解决**：
1. 确保 PostgreSQL 已启动
2. 检查 .env 文件中的数据库配置
3. 确保数据库已创建

### 4. 依赖安装失败
**问题**：npm install 或 pip install 失败

**解决**：
- 前端：使用 `npm install --legacy-peer-deps`
- 后端：使用国内镜像 `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple`

## 🔧 调试技巧

### 前端调试
1. 使用浏览器开发者工具的 Network 标签查看 API 请求
2. 在 Vue DevTools 中查看组件状态
3. 使用 `console.log` 输出调试信息

### 后端调试
1. 查看终端输出的日志
2. 访问 http://localhost:8000/docs 测试 API
3. 使用 Postman 或 curl 测试接口

## 📊 性能优化建议

1. **前端优化**
   - 使用防抖/节流处理频繁请求
   - 实现请求缓存
   - 使用虚拟滚动处理大量数据

2. **后端优化**
   - 添加 Redis 缓存
   - 使用数据库索引
   - 实现分页查询

3. **实时数据**
   - 使用 WebSocket 推送实时行情
   - 实现数据增量更新

## 🎯 下一步计划

1. ✅ 完成所有页面的 API 联调
2. ⏳ 添加 WebSocket 实时推送
3. ⏳ 实现策略执行引擎
4. ⏳ 添加更多技术指标
5. ⏳ 完善错误处理和日志
6. ⏳ 添加单元测试
7. ⏳ 性能优化
8. ⏳ 部署到生产环境
