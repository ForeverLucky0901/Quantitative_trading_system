# 🚀 快速启动指南

## 问题：页面空白？

如果你看到空白页面，是因为**还没有安装依赖包**。

## ✅ 解决方法

### 步骤1：安装前端依赖

```bash
cd /Users/lucky/Desktop/Quantitative_trading_system/frontend

# 安装依赖（首次运行必须执行）
npm install

# 等待安装完成（可能需要3-5分钟）
```

### 步骤2：启动前端

```bash
# 在 frontend 目录下
npm run dev
```

### 步骤3：访问系统

打开浏览器访问：http://localhost:5173

现在应该能看到完整的界面了！

---

## 🎯 完整启动流程

### 方式一：只启动前端（查看UI）

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖（首次）
npm install

# 3. 启动
npm run dev

# 4. 访问
# http://localhost:5173
```

**注意**：这种方式只能看界面，不能真实交易（因为后端没启动）

### 方式二：启动前后端（完整功能）

#### 终端1 - 启动后端

```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境（首次）
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖（首次）
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env

# 5. 初始化数据库（首次）
# 先确保 PostgreSQL 已安装并运行
brew install postgresql@14
brew services start postgresql@14
createdb quant_trading

# 运行初始化脚本
python init_db.py

# 6. 启动后端
uvicorn main:app --reload
```

#### 终端2 - 启动前端

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖（首次）
npm install

# 3. 启动前端
npm run dev
```

#### 访问系统

- 前端：http://localhost:5173
- 后端API文档：http://localhost:8000/docs

---

## 🐳 方式三：使用Docker（最简单）

```bash
# 1. 确保已安装 Docker Desktop

# 2. 一键启动所有服务
docker-compose up -d

# 3. 查看状态
docker-compose ps

# 4. 访问
# 前端：http://localhost:5173
# 后端：http://localhost:8000/docs
```

---

## ❓ 常见问题

### Q1: npm install 很慢怎么办？

```bash
# 使用国内镜像
npm install --registry=https://registry.npmmirror.com
```

### Q2: Python 依赖安装失败？

```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: 数据库连接失败？

```bash
# 检查 PostgreSQL 是否运行
brew services list | grep postgresql

# 重启 PostgreSQL
brew services restart postgresql@14

# 检查数据库是否存在
psql -l | grep quant_trading
```

### Q4: 端口被占用？

```bash
# 查看端口占用
lsof -i :5173  # 前端端口
lsof -i :8000  # 后端端口

# 杀死进程
kill -9 <PID>
```

### Q5: 页面显示但没有数据？

这是正常的！因为：
1. 后端没启动 - 无法获取真实数据
2. 数据库没数据 - 需要先运行策略或手动添加

**解决方法**：
- 启动后端服务
- 访问 http://localhost:8000/docs 测试API
- 在前端登录（测试账号：admin/admin123）

---

## 📋 检查清单

启动前检查：

- [ ] Node.js 已安装（`node -v`）
- [ ] Python 已安装（`python3 --version`）
- [ ] PostgreSQL 已安装（`psql --version`）
- [ ] Redis 已安装（`redis-cli --version`）

或者：

- [ ] Docker Desktop 已安装

---

## 🎯 推荐启动方式

### 对于开发者：
**方式二**（前后端分别启动）- 方便调试

### 对于普通用户：
**方式三**（Docker）- 一键启动，最简单

### 对于只想看界面：
**方式一**（只启动前端）- 最快

---

## 💡 提示

1. **首次启动**需要安装依赖，会比较慢
2. **TypeScript 错误**在安装依赖后会自动消失
3. **空白页面**通常是依赖没安装
4. **数据为空**是正常的，需要先配置交易所API

---

## 🆘 还是不行？

1. 确认是否在正确的目录
2. 确认是否执行了 `npm install`
3. 查看终端是否有错误信息
4. 尝试清除缓存：`npm cache clean --force`
5. 删除 node_modules 重新安装：`rm -rf node_modules && npm install`

---

## 📞 下一步

启动成功后，你可以：

1. ✅ 浏览全球市场（/global-markets）
2. ✅ 查看仪表盘（/dashboard）
3. ✅ 创建交易策略（/strategies）
4. ✅ 进行策略回测（/backtest）
5. ✅ 查看实时行情（/market）

**开始你的量化交易之旅吧！** 🚀
