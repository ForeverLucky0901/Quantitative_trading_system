/**
 * 行情相关 API
 */
import { request } from './request'

export interface Kline {
  timestamp: string
  open: number
  high: number
  low: number
  close: number
  volume: number
}

export interface Ticker {
  symbol: string
  last: number
  bid: number
  ask: number
  high: number
  low: number
  volume: number
  timestamp: string
}

// 获取K线数据
export const getKlines = (params: {
  exchange: string
  symbol: string
  interval: string
  start_time?: string
  end_time?: string
  limit?: number
}) => {
  return request.get<{ exchange: string; symbol: string; interval: string; data: Kline[] }>(
    '/market/klines',
    { params }
  )
}

// 获取实时行情
export const getTicker = (params: { exchange: string; symbol: string }) => {
  return request.get<Ticker>('/market/ticker', { params })
}

// 获取交易对列表
export const getSymbols = (params: { exchange: string }) => {
  return request.get<{ exchange: string; symbols: string[] }>('/market/symbols', { params })
}
