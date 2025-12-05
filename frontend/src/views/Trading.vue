<template>
  <div class="trading">
    <el-row :gutter="20">
      <!-- 左侧：交易面板 -->
      <el-col :span="16">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>交易面板</span>
              <el-select v-model="selectedSymbol" placeholder="选择交易对" style="width: 200px">
                <el-option
                  v-for="symbol in symbols"
                  :key="symbol"
                  :label="symbol"
                  :value="symbol"
                />
              </el-select>
            </div>
          </template>
          
          <el-row :gutter="20">
            <!-- 买入 -->
            <el-col :span="12">
              <div class="trade-panel buy-panel">
                <h3>买入 {{ selectedSymbol }}</h3>
                <el-form :model="buyForm" label-width="80px">
                  <el-form-item label="价格">
                    <el-input-number
                      v-model="buyForm.price"
                      :precision="2"
                      :step="0.01"
                      style="width: 100%"
                    />
                  </el-form-item>
                  <el-form-item label="数量">
                    <el-input-number
                      v-model="buyForm.amount"
                      :precision="4"
                      :step="0.01"
                      style="width: 100%"
                    />
                  </el-form-item>
                  <el-form-item label="订单类型">
                    <el-radio-group v-model="buyForm.orderType">
                      <el-radio label="market">市价</el-radio>
                      <el-radio label="limit">限价</el-radio>
                    </el-radio-group>
                  </el-form-item>
                  <el-form-item>
                    <div class="trade-info">
                      <span>总额: {{ buyTotal }} USDT</span>
                    </div>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="success" style="width: 100%" @click="handleBuy">
                      买入
                    </el-button>
                  </el-form-item>
                </el-form>
              </div>
            </el-col>
            
            <!-- 卖出 -->
            <el-col :span="12">
              <div class="trade-panel sell-panel">
                <h3>卖出 {{ selectedSymbol }}</h3>
                <el-form :model="sellForm" label-width="80px">
                  <el-form-item label="价格">
                    <el-input-number
                      v-model="sellForm.price"
                      :precision="2"
                      :step="0.01"
                      style="width: 100%"
                    />
                  </el-form-item>
                  <el-form-item label="数量">
                    <el-input-number
                      v-model="sellForm.amount"
                      :precision="4"
                      :step="0.01"
                      style="width: 100%"
                    />
                  </el-form-item>
                  <el-form-item label="订单类型">
                    <el-radio-group v-model="sellForm.orderType">
                      <el-radio label="market">市价</el-radio>
                      <el-radio label="limit">限价</el-radio>
                    </el-radio-group>
                  </el-form-item>
                  <el-form-item>
                    <div class="trade-info">
                      <span>总额: {{ sellTotal }} USDT</span>
                    </div>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="danger" style="width: 100%" @click="handleSell">
                      卖出
                    </el-button>
                  </el-form-item>
                </el-form>
              </div>
            </el-col>
          </el-row>
        </el-card>
        
        <!-- K线图 -->
        <el-card style="margin-top: 20px">
          <template #header>
            <div class="card-header">
              <span>K线图</span>
              <el-radio-group v-model="interval" size="small">
                <el-radio-button label="1m">1分钟</el-radio-button>
                <el-radio-button label="5m">5分钟</el-radio-button>
                <el-radio-button label="15m">15分钟</el-radio-button>
                <el-radio-button label="1h">1小时</el-radio-button>
                <el-radio-button label="4h">4小时</el-radio-button>
                <el-radio-button label="1d">1天</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div ref="chartRef" style="height: 400px"></div>
        </el-card>
      </el-col>
      
      <!-- 右侧：行情信息 -->
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>实时行情</span>
          </template>
          <div class="ticker-info">
            <div class="price-display">
              <div class="current-price">{{ currentPrice }}</div>
              <div class="price-change" :class="priceChangeClass">
                {{ priceChange >= 0 ? '+' : '' }}{{ priceChange }}%
              </div>
            </div>
            <el-divider />
            <div class="ticker-details">
              <div class="detail-item">
                <span class="label">24h最高</span>
                <span class="value">{{ ticker.high }}</span>
              </div>
              <div class="detail-item">
                <span class="label">24h最低</span>
                <span class="value">{{ ticker.low }}</span>
              </div>
              <div class="detail-item">
                <span class="label">24h成交量</span>
                <span class="value">{{ ticker.volume }}</span>
              </div>
              <div class="detail-item">
                <span class="label">买一价</span>
                <span class="value buy">{{ ticker.bid }}</span>
              </div>
              <div class="detail-item">
                <span class="label">卖一价</span>
                <span class="value sell">{{ ticker.ask }}</span>
              </div>
            </div>
          </div>
        </el-card>
        
        <!-- 账户信息 -->
        <el-card style="margin-top: 20px">
          <template #header>
            <span>账户信息</span>
          </template>
          <div class="account-info">
            <div class="account-item">
              <span class="label">可用余额</span>
              <span class="value">10,000.00 USDT</span>
            </div>
            <div class="account-item">
              <span class="label">冻结余额</span>
              <span class="value">500.00 USDT</span>
            </div>
            <div class="account-item">
              <span class="label">总资产</span>
              <span class="value">10,500.00 USDT</span>
            </div>
          </div>
        </el-card>
        
        <!-- 当前持仓 -->
        <el-card style="margin-top: 20px">
          <template #header>
            <span>当前持仓</span>
          </template>
          <el-table :data="positions" size="small">
            <el-table-column prop="symbol" label="交易对" width="100" />
            <el-table-column prop="amount" label="数量" />
            <el-table-column prop="avgPrice" label="均价" />
            <el-table-column prop="pnl" label="盈亏">
              <template #default="{ row }">
                <span :style="{ color: row.pnl >= 0 ? '#67C23A' : '#F56C6C' }">
                  {{ row.pnl >= 0 ? '+' : '' }}{{ row.pnl }}
                </span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'

const symbols = ref(['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT'])
const selectedSymbol = ref('BTC/USDT')
const interval = ref('1h')

const buyForm = ref({
  price: 42000,
  amount: 0.01,
  orderType: 'limit'
})

const sellForm = ref({
  price: 42000,
  amount: 0.01,
  orderType: 'limit'
})

const ticker = ref({
  high: 43500,
  low: 41000,
  volume: 25000,
  bid: 41950,
  ask: 42000
})

const currentPrice = ref(42000)
const priceChange = ref(2.5)

const positions = ref([
  { symbol: 'BTC/USDT', amount: 0.5, avgPrice: 40000, pnl: 1000 },
  { symbol: 'ETH/USDT', amount: 5, avgPrice: 2200, pnl: -150 }
])

const chartRef = ref()

const buyTotal = computed(() => (buyForm.value.price * buyForm.value.amount).toFixed(2))
const sellTotal = computed(() => (sellForm.value.price * sellForm.value.amount).toFixed(2))
const priceChangeClass = computed(() => priceChange.value >= 0 ? 'positive' : 'negative')

const handleBuy = () => {
  ElMessage.success('买入订单已提交')
}

const handleSell = () => {
  ElMessage.success('卖出订单已提交')
}

onMounted(() => {
  initChart()
  // 模拟实时价格更新
  setInterval(() => {
    currentPrice.value = currentPrice.value + (Math.random() - 0.5) * 100
    priceChange.value = ((Math.random() - 0.5) * 5).toFixed(2) as any
  }, 3000)
})

const initChart = () => {
  if (!chartRef.value) return
  
  const chart = echarts.init(chartRef.value)
  
  // 模拟K线数据
  const data = []
  let basePrice = 42000
  for (let i = 0; i < 100; i++) {
    const open = basePrice
    const close = open + (Math.random() - 0.5) * 500
    const high = Math.max(open, close) + Math.random() * 200
    const low = Math.min(open, close) - Math.random() * 200
    data.push([open, close, low, high])
    basePrice = close
  }
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    xAxis: {
      type: 'category',
      data: data.map((_, i) => i)
    },
    yAxis: {
      scale: true
    },
    series: [{
      type: 'candlestick',
      data: data,
      itemStyle: {
        color: '#ef5350',
        color0: '#26a69a',
        borderColor: '#ef5350',
        borderColor0: '#26a69a'
      }
    }]
  }
  
  chart.setOption(option)
}
</script>

<style scoped lang="scss">
.trading {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .trade-panel {
    padding: 20px;
    border-radius: 8px;
    
    h3 {
      margin: 0 0 20px 0;
      text-align: center;
    }
    
    &.buy-panel {
      background: rgba(103, 194, 58, 0.05);
      border: 1px solid rgba(103, 194, 58, 0.2);
    }
    
    &.sell-panel {
      background: rgba(245, 108, 108, 0.05);
      border: 1px solid rgba(245, 108, 108, 0.2);
    }
    
    .trade-info {
      text-align: center;
      font-size: 16px;
      font-weight: bold;
      color: #333;
    }
  }
  
  .ticker-info {
    .price-display {
      text-align: center;
      padding: 20px 0;
      
      .current-price {
        font-size: 36px;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
      }
      
      .price-change {
        font-size: 18px;
        font-weight: bold;
        
        &.positive {
          color: #67C23A;
        }
        
        &.negative {
          color: #F56C6C;
        }
      }
    }
    
    .ticker-details {
      .detail-item {
        display: flex;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid #f0f0f0;
        
        .label {
          color: #666;
        }
        
        .value {
          font-weight: bold;
          
          &.buy {
            color: #67C23A;
          }
          
          &.sell {
            color: #F56C6C;
          }
        }
      }
    }
  }
  
  .account-info {
    .account-item {
      display: flex;
      justify-content: space-between;
      padding: 15px 0;
      border-bottom: 1px solid #f0f0f0;
      
      .label {
        color: #666;
      }
      
      .value {
        font-weight: bold;
        font-size: 16px;
      }
    }
  }
}
</style>
