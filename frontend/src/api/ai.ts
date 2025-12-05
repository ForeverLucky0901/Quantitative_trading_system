import request from './request'

export interface MarketAnalysisRequest {
  symbol: string
  exchange?: string
  include_news?: boolean
  news_items?: string[]
}

export interface StrategyGenerationRequest {
  description: string
  strategy_type?: string
  params?: Record<string, any>
}

export interface TradingSignalRequest {
  symbol: string
  exchange?: string
  timeframe?: string
  limit?: number
}

export interface QuestionRequest {
  question: string
  context?: Record<string, any>
}

export interface StrategyOptimizationRequest {
  strategy_code: string
  backtest_results: any[]
}

export const aiApi = {
  analyzeMarket(data: MarketAnalysisRequest) {
    return request.post('/ai/analyze-market', data)
  },

  generateStrategy(data: StrategyGenerationRequest) {
    return request.post('/ai/generate-strategy', data)
  },

  getTradingSignal(data: TradingSignalRequest) {
    return request.post('/ai/trading-signal', data)
  },

  askQuestion(data: QuestionRequest) {
    return request.post('/ai/ask', data)
  },

  optimizeStrategy(data: StrategyOptimizationRequest) {
    return request.post('/ai/optimize-strategy', data)
  },

  getCapabilities() {
    return request.get('/ai/capabilities')
  }
}
