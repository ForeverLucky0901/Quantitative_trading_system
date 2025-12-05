<template>
  <div class="market">
    <!-- 市场概览 -->
    <el-card>
      <template #header>
        <div class="card-header">
          <span>市场概览</span>
          <el-radio-group v-model="marketType" size="small">
            <el-radio-button label="crypto">加密货币</el-radio-button>
            <el-radio-button label="stock">股票</el-radio-button>
            <el-radio-button label="futures">期货</el-radio-button>
          </el-radio-group>
        </div>
      </template>
      
      <el-table :data="marketData" stripe @row-click="handleRowClick">
        <el-table-column type="index" label="#" width="50" />
        <el-table-column prop="symbol" label="交易对" width="150">
          <template #default="{ row }">
            <div class="symbol-cell">
              <span class="symbol-name">{{ row.symbol }}</span>
              <span class="symbol-desc">{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="最新价" sortable>
          <template #default="{ row }">
            <span :style="{ color: row.change >= 0 ? '#67C23A' : '#F56C6C' }">
              {{ row.price }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="change" label="24h涨跌" sortable>
          <template #default="{ row }">
            <span :style="{ color: row.change >= 0 ? '#67C23A' : '#F56C6C' }">
              {{ row.change >= 0 ? '+' : '' }}{{ row.change }}%
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="high" label="24h最高" />
        <el-table-column prop="low" label="24h最低" />
        <el-table-column prop="volume" label="24h成交量" sortable>
          <template #default="{ row }">
            {{ formatVolume(row.volume) }}
          </template>
        </el-table-column>
        <el-table-column label="趋势" width="150">
          <template #default="{ row }">
            <div ref="sparklineRef" class="sparkline" :data-trend="row.trend"></div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click.stop="handleTrade(row)">
              交易
            </el-button>
            <el-button size="small" @click.stop="handleAddWatch(row)">
              自选
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 详细图表 -->
    <el-card style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <span>{{ selectedSymbol }} 详细分析</span>
          <div>
            <el-radio-group v-model="chartInterval" size="small">
              <el-radio-button label="1m">1分钟</el-radio-button>
              <el-radio-button label="5m">5分钟</el-radio-button>
              <el-radio-button label="15m">15分钟</el-radio-button>
              <el-radio-button label="1h">1小时</el-radio-button>
              <el-radio-button label="4h">4小时</el-radio-button>
              <el-radio-button label="1d">1天</el-radio-button>
            </el-radio-group>
          </div>
        </div>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="18">
          <div ref="mainChartRef" style="height: 500px"></div>
        </el-col>
        <el-col :span="6">
          <div class="market-info">
            <h3>市场信息</h3>
            <div class="info-item">
              <span class="label">最新价</span>
              <span class="value">42,000.00</span>
            </div>
            <div class="info-item">
              <span class="label">24h涨跌</span>
              <span class="value positive">+2.5%</span>
            </div>
            <div class="info-item">
              <span class="label">24h最高</span>
              <span class="value">43,500.00</span>
            </div>
            <div class="info-item">
              <span class="label">24h最低</span>
              <span class="value">41,000.00</span>
            </div>
            <div class="info-item">
              <span class="label">24h成交量</span>
              <span class="value">25,000 BTC</span>
            </div>
            <div class="info-item">
              <span class="label">24h成交额</span>
              <span class="value">1.05B USDT</span>
            </div>
            
            <el-divider />
            
            <h3>技术指标</h3>
            <div class="indicator-item">
              <span class="label">MA(5)</span>
              <span class="value">41,850</span>
            </div>
            <div class="indicator-item">
              <span class="label">MA(10)</span>
              <span class="value">41,200</span>
            </div>
            <div class="indicator-item">
              <span class="label">MA(30)</span>
              <span class="value">40,500</span>
            </div>
            <div class="indicator-item">
              <span class="label">RSI(14)</span>
              <span class="value">65.5</span>
            </div>
            <div class="indicator-item">
              <span class="label">MACD</span>
              <span class="value positive">+125</span>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
    
    <!-- 市场热度 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>涨幅榜</span>
          </template>
          <el-table :data="gainers" size="small" :show-header="false">
            <el-table-column prop="symbol" width="120" />
            <el-table-column prop="price" />
            <el-table-column prop="change">
              <template #default="{ row }">
                <span style="color: #67C23A">+{{ row.change }}%</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>跌幅榜</span>
          </template>
          <el-table :data="losers" size="small" :show-header="false">
            <el-table-column prop="symbol" width="120" />
            <el-table-column prop="price" />
            <el-table-column prop="change">
              <template #default="{ row }">
                <span style="color: #F56C6C">{{ row.change }}%</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'

const router = useRouter()

const marketType = ref('crypto')
const chartInterval = ref('1h')
const selectedSymbol = ref('BTC/USDT')

const marketData = ref([
  { symbol: 'BTC/USDT', name: '比特币', price: 42000, change: 2.5, high: 43500, low: 41000, volume: 25000, trend: [1, 3, 2, 5, 4, 6, 5, 7] },
  { symbol: 'ETH/USDT', name: '以太坊', price: 2250, change: 1.8, high: 2300, low: 2200, volume: 150000, trend: [2, 3, 4, 3, 5, 6, 5, 6] },
  { symbol: 'BNB/USDT', name: '币安币', price: 335, change: -1.2, high: 340, low: 330, volume: 80000, trend: [5, 4, 3, 4, 3, 2, 3, 2] },
  { symbol: 'SOL/USDT', name: 'Solana', price: 98, change: 5.6, high: 102, low: 92, volume: 120000, trend: [2, 3, 5, 6, 7, 8, 9, 10] },
  { symbol: 'XRP/USDT', name: '瑞波币', price: 0.58, change: -2.3, high: 0.60, low: 0.56, volume: 500000, trend: [6, 5, 4, 3, 4, 3, 2, 1] },
])

const gainers = ref([
  { symbol: 'SOL/USDT', price: 98.00, change: 5.6 },
  { symbol: 'AVAX/USDT', price: 35.20, change: 4.8 },
  { symbol: 'MATIC/USDT', price: 0.85, change: 3.9 },
  { symbol: 'DOT/USDT', price: 6.50, change: 3.2 },
  { symbol: 'LINK/USDT', price: 14.80, change: 2.8 }
])

const losers = ref([
  { symbol: 'XRP/USDT', price: 0.58, change: -2.3 },
  { symbol: 'ADA/USDT', price: 0.42, change: -1.8 },
  { symbol: 'BNB/USDT', price: 335.00, change: -1.2 },
  { symbol: 'DOGE/USDT', price: 0.08, change: -0.9 },
  { symbol: 'TRX/USDT', price: 0.10, change: -0.5 }
])

const mainChartRef = ref()

const formatVolume = (volume: number) => {
  if (volume >= 1000000) {
    return (volume / 1000000).toFixed(2) + 'M'
  } else if (volume >= 1000) {
    return (volume / 1000).toFixed(2) + 'K'
  }
  return volume.toString()
}

const handleRowClick = (row: any) => {
  selectedSymbol.value = row.symbol
  ElMessage.info(`查看 ${row.symbol} 详情`)
}

const handleTrade = (row: any) => {
  router.push('/trading')
  ElMessage.success(`跳转到交易页面: ${row.symbol}`)
}

const handleAddWatch = (row: any) => {
  ElMessage.success(`已添加 ${row.symbol} 到自选`)
}

onMounted(() => {
  initMainChart()
})

const initMainChart = () => {
  if (!mainChartRef.value) return
  
  const chart = echarts.init(mainChartRef.value)
  
  // 生成K线数据
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
    grid: [
      { left: '10%', right: '8%', height: '50%' },
      { left: '10%', right: '8%', top: '65%', height: '15%' }
    ],
    xAxis: [
      { type: 'category', data: data.map((_, i) => i), gridIndex: 0 },
      { type: 'category', data: data.map((_, i) => i), gridIndex: 1 }
    ],
    yAxis: [
      { scale: true, gridIndex: 0 },
      { scale: true, gridIndex: 1 }
    ],
    dataZoom: [{
      type: 'inside',
      xAxisIndex: [0, 1],
      start: 50,
      end: 100
    }],
    series: [
      {
        type: 'candlestick',
        data: data,
        itemStyle: {
          color: '#ef5350',
          color0: '#26a69a',
          borderColor: '#ef5350',
          borderColor0: '#26a69a'
        },
        xAxisIndex: 0,
        yAxisIndex: 0
      },
      {
        type: 'bar',
        data: data.map(d => Math.abs(d[1] - d[0]) * 1000),
        xAxisIndex: 1,
        yAxisIndex: 1,
        itemStyle: {
          color: (params: any) => {
            return data[params.dataIndex][1] >= data[params.dataIndex][0] ? '#26a69a' : '#ef5350'
          }
        }
      }
    ]
  }
  
  chart.setOption(option)
}
</script>

<style scoped lang="scss">
.market {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .symbol-cell {
    display: flex;
    flex-direction: column;
    
    .symbol-name {
      font-weight: bold;
      color: #333;
    }
    
    .symbol-desc {
      font-size: 12px;
      color: #999;
    }
  }
  
  .sparkline {
    height: 30px;
    background: linear-gradient(to right, #e3f2fd, #bbdefb);
  }
  
  .market-info {
    h3 {
      margin: 0 0 15px 0;
      font-size: 16px;
      color: #333;
    }
    
    .info-item, .indicator-item {
      display: flex;
      justify-content: space-between;
      padding: 10px 0;
      border-bottom: 1px solid #f0f0f0;
      
      .label {
        color: #666;
        font-size: 14px;
      }
      
      .value {
        font-weight: bold;
        font-size: 14px;
        
        &.positive {
          color: #67C23A;
        }
        
        &.negative {
          color: #F56C6C;
        }
      }
    }
  }
}
</style>
