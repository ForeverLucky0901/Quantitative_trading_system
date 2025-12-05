/**
 * 交易相关 API
 */
import { request } from './request'

export interface Order {
  id: number
  strategy_id: number
  exchange: string
  symbol: string
  order_type: string
  side: string
  price?: number
  amount: number
  filled: number
  status: string
  order_id?: string
  created_at: string
  updated_at?: string
}

export interface OrderCreate {
  strategy_id: number
  exchange: string
  symbol: string
  order_type: string
  side: string
  price?: number
  amount: number
}

export interface Position {
  id: number
  strategy_id: number
  exchange: string
  symbol: string
  side: string
  amount: number
  entry_price: number
  current_price?: number
  unrealized_pnl: number
  realized_pnl: number
  created_at: string
  updated_at?: string
}

export interface Trade {
  id: number
  order_id: number
  strategy_id: number
  exchange: string
  symbol: string
  side: string
  price: number
  amount: number
  fee: number
  pnl?: number
  trade_id?: string
  created_at: string
}

// 创建订单
export const createOrder = (data: OrderCreate) => {
  return request.post<Order>('/trades/orders', data)
}

// 获取订单列表
export const getOrders = (params?: { strategy_id?: number; skip?: number; limit?: number }) => {
  return request.get<Order[]>('/trades/orders', { params })
}

// 获取订单详情
export const getOrder = (id: number) => {
  return request.get<Order>(`/trades/orders/${id}`)
}

// 取消订单
export const cancelOrder = (id: number) => {
  return request.post(`/trades/orders/${id}/cancel`)
}

// 获取持仓列表
export const getPositions = (params?: { strategy_id?: number }) => {
  return request.get<Position[]>('/trades/positions', { params })
}

// 获取成交记录
export const getTrades = (params?: { strategy_id?: number; skip?: number; limit?: number }) => {
  return request.get<Trade[]>('/trades/trades', { params })
}
