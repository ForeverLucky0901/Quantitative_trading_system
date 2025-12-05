/**
 * 策略相关 API
 */
import { request } from './request'

export interface Strategy {
  id: number
  user_id: number
  name: string
  description?: string
  code: string
  params?: Record<string, any>
  status: string
  is_backtest: boolean
  created_at: string
  updated_at?: string
}

export interface StrategyCreate {
  name: string
  description?: string
  code: string
  params?: Record<string, any>
}

export interface StrategyUpdate {
  name?: string
  description?: string
  code?: string
  params?: Record<string, any>
  status?: string
}

export interface BacktestCreate {
  strategy_id: number
  start_date: string
  end_date: string
  initial_capital?: number
}

export interface BacktestResult {
  id: number
  strategy_id: number
  start_date: string
  end_date: string
  initial_capital: number
  final_capital?: number
  total_return?: number
  sharpe_ratio?: number
  max_drawdown?: number
  win_rate?: number
  total_trades?: number
  result_data?: Record<string, any>
  created_at: string
}

// 获取策略列表
export const getStrategies = (params?: { skip?: number; limit?: number }) => {
  return request.get<Strategy[]>('/strategies/', { params })
}

// 获取策略详情
export const getStrategy = (id: number) => {
  return request.get<Strategy>(`/strategies/${id}`)
}

// 创建策略
export const createStrategy = (data: StrategyCreate) => {
  return request.post<Strategy>('/strategies/', data)
}

// 更新策略
export const updateStrategy = (id: number, data: StrategyUpdate) => {
  return request.put<Strategy>(`/strategies/${id}`, data)
}

// 删除策略
export const deleteStrategy = (id: number) => {
  return request.delete(`/strategies/${id}`)
}

// 启动策略
export const startStrategy = (id: number) => {
  return request.post(`/strategies/${id}/start`)
}

// 停止策略
export const stopStrategy = (id: number) => {
  return request.post(`/strategies/${id}/stop`)
}

// 创建回测
export const createBacktest = (data: BacktestCreate) => {
  return request.post<BacktestResult>('/strategies/backtest', data)
}

// 获取回测结果
export const getBacktest = (id: number) => {
  return request.get<BacktestResult>(`/strategies/backtest/${id}`)
}
