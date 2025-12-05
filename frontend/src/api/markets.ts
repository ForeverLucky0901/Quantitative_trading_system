/**
 * 全球市场API接口
 */
import { request } from './request'

// ========== 加密货币市场 ==========

export interface CryptoExchange {
  name: string
  description: string
  requires_api_key: boolean
  supported_markets: string[]
}

export interface CryptoExchanges {
  exchanges: Record<string, CryptoExchange>
  total: number
}

// 获取加密货币交易所列表
export const getCryptoExchanges = () => {
  return request.get<CryptoExchanges>('/markets/crypto/exchanges')
}

// 获取加密货币交易对
export const getCryptoSymbols = (exchange: string) => {
  return request.get('/markets/crypto/symbols', { params: { exchange } })
}

// 获取加密货币实时行情
export const getCryptoTicker = (exchange: string, symbol: string) => {
  return request.get('/markets/crypto/ticker', { params: { exchange, symbol } })
}

// ========== 股票市场 ==========

export interface StockMarket {
  code: string
  name: string
  exchange: string
  index?: string
  stocks_count: number
}

export interface MarketsByRegion {
  [region: string]: StockMarket[]
}

// 获取所有市场列表
export const getAllMarkets = () => {
  return request.get<{
    markets: StockMarket[]
    by_region: MarketsByRegion
    total: number
  }>('/markets/all')
}

// 获取市场概览
export const getMarketsSummary = () => {
  return request.get('/markets/summary')
}

// 获取全球主要指数
export const getMajorIndices = () => {
  return request.get<{
    indices: Record<string, string>
    total: number
  }>('/markets/indices')
}

// 获取指定市场详情
export const getMarketDetail = (marketCode: string) => {
  return request.get(`/markets/${marketCode}`)
}

// 获取美股列表
export const getUSStocks = () => {
  return request.get('/markets/stocks/us')
}

// 获取港股列表
export const getHKStocks = () => {
  return request.get('/markets/stocks/hk')
}

// 获取A股列表
export const getCNStocks = () => {
  return request.get('/markets/stocks/cn')
}

// 获取新加坡股票列表
export const getSGStocks = () => {
  return request.get('/markets/stocks/sg')
}

// 获取股票历史数据
export const getStockData = (params: {
  symbol: string
  market: string
  start_date?: string
  end_date?: string
  interval?: string
}) => {
  return request.get('/markets/stocks/data', { params })
}

// ========== 通用接口 ==========

export interface MarketDataParams {
  symbol: string
  market: string
  exchange?: string
  start_date?: string
  end_date?: string
  interval?: string
}

// 统一获取市场数据接口
export const getMarketData = (params: MarketDataParams) => {
  // 根据市场类型选择不同的API
  if (params.market === 'CRYPTO') {
    return getCryptoTicker(params.exchange!, params.symbol)
  } else {
    return getStockData(params)
  }
}
