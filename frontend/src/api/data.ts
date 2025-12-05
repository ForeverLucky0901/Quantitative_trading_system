/**
 * 数据采集相关 API
 */
import { request } from './request'

export interface Exchange {
  exchanges: string[]
  description: Record<string, string>
}

// 获取支持的交易所列表
export const getExchanges = () => {
  return request.get<Exchange>('/data/exchanges')
}

// 获取交易对列表
export const getDataSymbols = (params: { exchange: string }) => {
  return request.get<{ exchange: string; symbols: string[]; count: number }>(
    '/data/symbols',
    { params }
  )
}

// 获取实时行情
export const getDataTicker = (params: { exchange: string; symbol: string }) => {
  return request.get('/data/ticker', { params })
}

// 获取K线数据
export const getDataKlines = (params: {
  exchange: string
  symbol: string
  interval: string
  limit?: number
}) => {
  return request.get('/data/klines', { params })
}

// 采集历史数据
export const collectHistoricalData = (params: {
  exchange: string
  symbol: string
  interval: string
  days: number
}) => {
  return request.post('/data/collect', null, { params })
}

// 获取热门交易对
export const getPopularSymbols = () => {
  return request.get<{
    crypto: string[]
    stocks: string[]
    a_stocks: string[]
  }>('/data/popular-symbols')
}
