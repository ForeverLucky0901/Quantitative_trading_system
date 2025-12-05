<template>
  <div class="ai-assistant">
    <el-card class="header-card">
      <div class="header-content">
        <div class="title-section">
          <h2>🤖 AI 交易助手</h2>
          <p class="subtitle">智能分析 · 策略生成 · 交易信号 · 问答助手</p>
        </div>
        <el-tag :type="aiStatus === 'operational' ? 'success' : 'danger'" size="large">
          {{ aiStatus === 'operational' ? 'AI 已就绪' : 'AI 未配置' }}
        </el-tag>
      </div>
    </el-card>

    <el-tabs v-model="activeTab" class="ai-tabs">
      <!-- 市场分析 -->
      <el-tab-pane label="📊 市场分析" name="market">
        <el-card>
          <el-form :model="marketForm" label-width="100px">
            <el-form-item label="交易对">
              <el-input v-model="marketForm.symbol" placeholder="例如: BTC/USDT" />
            </el-form-item>
            <el-form-item label="交易所">
              <el-select v-model="marketForm.exchange" placeholder="选择交易所">
                <el-option label="Binance" value="binance_public" />
                <el-option label="Coinbase" value="coinbase" />
                <el-option label="Kraken" value="kraken" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="analyzeMarket" :loading="loading.market">
                开始分析
              </el-button>
            </el-form-item>
          </el-form>

          <div v-if="results.market" class="result-box">
            <h3>分析结果</h3>
            <div class="analysis-content" v-html="formatMarkdown(results.market.analysis)"></div>
            <el-divider />
            <div class="meta-info">
              <span>分析时间: {{ results.market.timestamp }}</span>
              <span>模型: {{ results.market.model }}</span>
            </div>
          </div>
        </el-card>
      </el-tab-pane>

      <!-- 策略生成 -->
      <el-tab-pane label="⚡ 策略生成" name="strategy">
        <el-card>
          <el-form :model="strategyForm" label-width="100px">
            <el-form-item label="策略描述">
              <el-input
                v-model="strategyForm.description"
                type="textarea"
                :rows="4"
                placeholder="描述你想要的交易策略，例如：基于RSI和MACD的双指标策略，当RSI低于30且MACD金叉时买入..."
              />
            </el-form-item>
            <el-form-item label="策略类型">
              <el-select v-model="strategyForm.strategy_type">
                <el-option label="技术分析" value="technical" />
                <el-option label="基本面分析" value="fundamental" />
                <el-option label="机器学习" value="ml" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="generateStrategy" :loading="loading.strategy">
                生成策略
              </el-button>
            </el-form-item>
          </el-form>

          <div v-if="results.strategy" class="result-box">
            <h3>生成的策略</h3>
            <div class="explanation">{{ results.strategy.explanation }}</div>
            <el-divider />
            <h4>策略代码</h4>
            <pre class="code-block"><code>{{ results.strategy.code }}</code></pre>
            <el-button type="success" @click="copyCode" style="margin-top: 10px">
              复制代码
            </el-button>
          </div>
        </el-card>
      </el-tab-pane>

      <!-- 交易信号 -->
      <el-tab-pane label="📈 交易信号" name="signal">
        <el-card>
          <el-form :model="signalForm" label-width="100px">
            <el-form-item label="交易对">
              <el-input v-model="signalForm.symbol" placeholder="例如: BTC/USDT" />
            </el-form-item>
            <el-form-item label="交易所">
              <el-select v-model="signalForm.exchange">
                <el-option label="Binance" value="binance_public" />
                <el-option label="Coinbase" value="coinbase" />
                <el-option label="Kraken" value="kraken" />
              </el-select>
            </el-form-item>
            <el-form-item label="时间周期">
              <el-select v-model="signalForm.timeframe">
                <el-option label="1分钟" value="1m" />
                <el-option label="5分钟" value="5m" />
                <el-option label="15分钟" value="15m" />
                <el-option label="1小时" value="1h" />
                <el-option label="4小时" value="4h" />
                <el-option label="1天" value="1d" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="getTradingSignal" :loading="loading.signal">
                获取信号
              </el-button>
            </el-form-item>
          </el-form>

          <div v-if="results.signal" class="result-box">
            <h3>交易信号</h3>
            <el-row :gutter="20">
              <el-col :span="8">
                <el-card class="signal-card">
                  <div class="signal-item">
                    <div class="label">信号</div>
                    <div :class="['value', `signal-${results.signal.signal?.toLowerCase()}`]">
                      {{ results.signal.signal || 'N/A' }}
                    </div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card class="signal-card">
                  <div class="signal-item">
                    <div class="label">信号强度</div>
                    <div class="value">{{ results.signal.strength || 'N/A' }}/10</div>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card class="signal-card">
                  <div class="signal-item">
                    <div class="label">建议仓位</div>
                    <div class="value">{{ results.signal.position || 'N/A' }}%</div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
            <el-divider />
            <div class="signal-details">
              <p><strong>止损位:</strong> {{ results.signal.stop_loss || 'N/A' }}</p>
              <p><strong>止盈位:</strong> {{ results.signal.take_profit || 'N/A' }}</p>
              <p><strong>分析理由:</strong></p>
              <div class="reason">{{ results.signal.reason || results.signal.raw_response }}</div>
            </div>
          </div>
        </el-card>
      </el-tab-pane>

      <!-- 智能问答 -->
      <el-tab-pane label="💬 智能问答" name="qa">
        <el-card>
          <div class="chat-container">
            <div class="chat-history" ref="chatHistory">
              <div
                v-for="(msg, index) in chatHistory"
                :key="index"
                :class="['chat-message', msg.type]"
              >
                <div class="message-avatar">{{ msg.type === 'user' ? '👤' : '🤖' }}</div>
                <div class="message-content">
                  <div class="message-text">{{ msg.content }}</div>
                  <div class="message-time">{{ msg.time }}</div>
                </div>
              </div>
            </div>

            <el-divider />

            <el-form @submit.prevent="askQuestion">
              <el-form-item>
                <el-input
                  v-model="questionForm.question"
                  type="textarea"
                  :rows="3"
                  placeholder="问我任何关于量化交易的问题..."
                  @keydown.enter.ctrl="askQuestion"
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="askQuestion" :loading="loading.qa">
                  发送 (Ctrl+Enter)
                </el-button>
                <el-button @click="clearChat">清空对话</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { aiApi } from '@/api/ai'

const activeTab = ref('market')
const aiStatus = ref('not_configured')

const loading = reactive({
  market: false,
  strategy: false,
  signal: false,
  qa: false
})

const results = reactive({
  market: null as any,
  strategy: null as any,
  signal: null as any
})

const marketForm = reactive({
  symbol: 'BTC/USDT',
  exchange: 'binance_public'
})

const strategyForm = reactive({
  description: '',
  strategy_type: 'technical'
})

const signalForm = reactive({
  symbol: 'BTC/USDT',
  exchange: 'binance_public',
  timeframe: '1h'
})

const questionForm = reactive({
  question: ''
})

const chatHistory = ref<Array<{ type: string; content: string; time: string }>>([])
const chatHistoryRef = ref<HTMLElement>()

onMounted(async () => {
  try {
    const res = await aiApi.getCapabilities()
    aiStatus.value = res.data.status
  } catch (error) {
    console.error('Failed to get AI capabilities:', error)
  }
})

const analyzeMarket = async () => {
  if (!marketForm.symbol) {
    ElMessage.warning('请输入交易对')
    return
  }

  loading.market = true
  try {
    const res = await aiApi.analyzeMarket(marketForm)
    results.market = res.data.data
    ElMessage.success('分析完成')
  } catch (error: any) {
    ElMessage.error(error.message || '分析失败')
  } finally {
    loading.market = false
  }
}

const generateStrategy = async () => {
  if (!strategyForm.description) {
    ElMessage.warning('请输入策略描述')
    return
  }

  loading.strategy = true
  try {
    const res = await aiApi.generateStrategy(strategyForm)
    results.strategy = res.data.data
    ElMessage.success('策略生成完成')
  } catch (error: any) {
    ElMessage.error(error.message || '生成失败')
  } finally {
    loading.strategy = false
  }
}

const getTradingSignal = async () => {
  if (!signalForm.symbol) {
    ElMessage.warning('请输入交易对')
    return
  }

  loading.signal = true
  try {
    const res = await aiApi.getTradingSignal(signalForm)
    results.signal = res.data.data
    ElMessage.success('信号获取完成')
  } catch (error: any) {
    ElMessage.error(error.message || '获取失败')
  } finally {
    loading.signal = false
  }
}

const askQuestion = async () => {
  if (!questionForm.question.trim()) {
    ElMessage.warning('请输入问题')
    return
  }

  const userMessage = {
    type: 'user',
    content: questionForm.question,
    time: new Date().toLocaleTimeString()
  }
  chatHistory.value.push(userMessage)

  const question = questionForm.question
  questionForm.question = ''

  loading.qa = true
  try {
    const res = await aiApi.askQuestion({ question })
    const aiMessage = {
      type: 'ai',
      content: res.data.data.answer,
      time: new Date().toLocaleTimeString()
    }
    chatHistory.value.push(aiMessage)

    await nextTick()
    scrollToBottom()
  } catch (error: any) {
    ElMessage.error(error.message || '提问失败')
  } finally {
    loading.qa = false
  }
}

const clearChat = () => {
  chatHistory.value = []
}

const scrollToBottom = () => {
  if (chatHistoryRef.value) {
    chatHistoryRef.value.scrollTop = chatHistoryRef.value.scrollHeight
  }
}

const copyCode = () => {
  if (results.strategy?.code) {
    navigator.clipboard.writeText(results.strategy.code)
    ElMessage.success('代码已复制到剪贴板')
  }
}

const formatMarkdown = (text: string) => {
  if (!text) return ''
  return text.replace(/\n/g, '<br>')
}
</script>

<style scoped lang="scss">
.ai-assistant {
  padding: 20px;

  .header-card {
    margin-bottom: 20px;

    .header-content {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .title-section {
        h2 {
          margin: 0 0 8px 0;
          font-size: 24px;
        }

        .subtitle {
          margin: 0;
          color: #666;
          font-size: 14px;
        }
      }
    }
  }

  .ai-tabs {
    margin-top: 20px;
  }

  .result-box {
    margin-top: 20px;
    padding: 20px;
    background: #f5f7fa;
    border-radius: 8px;

    h3 {
      margin-top: 0;
    }

    .analysis-content {
      line-height: 1.8;
      white-space: pre-wrap;
    }

    .explanation {
      padding: 15px;
      background: white;
      border-radius: 4px;
      line-height: 1.6;
    }

    .code-block {
      background: #282c34;
      color: #abb2bf;
      padding: 15px;
      border-radius: 4px;
      overflow-x: auto;
      font-family: 'Courier New', monospace;
      font-size: 13px;
    }

    .meta-info {
      display: flex;
      gap: 20px;
      font-size: 12px;
      color: #999;
    }
  }

  .signal-card {
    .signal-item {
      text-align: center;

      .label {
        font-size: 14px;
        color: #666;
        margin-bottom: 10px;
      }

      .value {
        font-size: 24px;
        font-weight: bold;

        &.signal-buy {
          color: #67c23a;
        }

        &.signal-sell {
          color: #f56c6c;
        }

        &.signal-hold {
          color: #909399;
        }
      }
    }
  }

  .signal-details {
    p {
      margin: 10px 0;
    }

    .reason {
      padding: 15px;
      background: white;
      border-radius: 4px;
      line-height: 1.6;
    }
  }

  .chat-container {
    .chat-history {
      max-height: 500px;
      overflow-y: auto;
      padding: 10px;

      .chat-message {
        display: flex;
        margin-bottom: 20px;

        &.user {
          flex-direction: row-reverse;

          .message-content {
            background: #409eff;
            color: white;
          }
        }

        &.ai {
          .message-content {
            background: #f5f7fa;
          }
        }

        .message-avatar {
          font-size: 32px;
          margin: 0 10px;
        }

        .message-content {
          max-width: 70%;
          padding: 12px 16px;
          border-radius: 8px;

          .message-text {
            line-height: 1.6;
            white-space: pre-wrap;
          }

          .message-time {
            font-size: 12px;
            margin-top: 5px;
            opacity: 0.7;
          }
        }
      }
    }
  }
}
</style>
