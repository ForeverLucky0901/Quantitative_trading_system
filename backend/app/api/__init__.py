from fastapi import APIRouter
from app.api.endpoints import auth, users, strategies, trades, market, data, markets

api_router = APIRouter()

# 注册各模块路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户"])
api_router.include_router(strategies.router, prefix="/strategies", tags=["策略"])
api_router.include_router(trades.router, prefix="/trades", tags=["交易"])
api_router.include_router(market.router, prefix="/market", tags=["行情"])
api_router.include_router(data.router, prefix="/data", tags=["数据采集"])
api_router.include_router(markets.router, prefix="/markets", tags=["多市场数据"])
