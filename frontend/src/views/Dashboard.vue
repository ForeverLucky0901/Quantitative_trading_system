<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6" v-for="item in stats" :key="item.title">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-info">
              <div class="stat-title">{{ item.title }}</div>
              <div class="stat-value">{{ item.value }}</div>
              <div class="stat-trend" :class="item.trend > 0 ? 'up' : 'down'">
                <el-icon v-if="item.trend > 0"><CaretTop /></el-icon>
                <el-icon v-else><CaretBottom /></el-icon>
                {{ Math.abs(item.trend) }}%
              </div>
            </div>
            <el-icon :size="50" :color="item.color">
              <component :is="item.icon" />
            </el-icon>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="16">
        <el-card>
          <template #header>
            <span>收益曲线</span>
          </template>
          <div ref="equityChartRef" style="height: 400px"></div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>策略状态</span>
          </template>
          <div ref="strategyChartRef" style="height: 400px"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>最近交易</span>
          </template>
          <el-table :data="recentTrades" stripe>
            <el-table-column prop="time" label="时间" width="180" />
            <el-table-column prop="strategy" label="策略" />
            <el-table-column prop="symbol" label="交易对" />
            <el-table-column prop="side" label="方向">
              <template #default="{ row }">
                <el-tag :type="row.side === 'buy' ? 'success' : 'danger'">
                  {{ row.side === 'buy' ? '买入' : '卖出' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="price" label="价格" />
            <el-table-column prop="amount" label="数量" />
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
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const stats = ref([
  { title: '总资产', value: '¥125,680', trend: 12.5, color: '#1890ff', icon: 'Wallet' },
  { title: '今日收益', value: '¥2,340', trend: 8.2, color: '#52c41a', icon: 'TrendCharts' },
  { title: '活跃策略', value: '5', trend: 0, color: '#faad14', icon: 'Document' },
  { title: '持仓数量', value: '12', trend: -3.1, color: '#f5222d', icon: 'Coin' }
])

const recentTrades = ref([
  { time: '2024-01-15 14:30:25', strategy: 'MA策略', symbol: 'BTC/USDT', side: 'buy', price: '42,500', amount: '0.1', pnl: 125 },
  { time: '2024-01-15 13:20:15', strategy: 'MACD策略', symbol: 'ETH/USDT', side: 'sell', price: '2,250', amount: '1.5', pnl: -45 },
  { time: '2024-01-15 12:10:05', strategy: 'MA策略', symbol: 'BNB/USDT', side: 'buy', price: '320', amount: '5', pnl: 80 },
])

const equityChartRef = ref()
const strategyChartRef = ref()

onMounted(() => {
  initEquityChart()
  initStrategyChart()
})

const initEquityChart = () => {
  const chart = echarts.init(equityChartRef.value)
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['01-10', '01-11', '01-12', '01-13', '01-14', '01-15']
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      data: [100000, 102000, 105000, 103500, 108000, 112000],
      type: 'line',
      smooth: true,
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(24, 144, 255, 0.3)' },
          { offset: 1, color: 'rgba(24, 144, 255, 0.05)' }
        ])
      },
      itemStyle: {
        color: '#1890ff'
      }
    }]
  }
  chart.setOption(option)
}

const initStrategyChart = () => {
  const chart = echarts.init(strategyChartRef.value)
  const option = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [{
      type: 'pie',
      radius: '60%',
      data: [
        { value: 3, name: '运行中' },
        { value: 2, name: '已停止' },
        { value: 1, name: '回测中' }
      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }
  chart.setOption(option)
}
</script>

<style scoped lang="scss">
.dashboard {
  .stat-card {
    .stat-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .stat-info {
        .stat-title {
          font-size: 14px;
          color: #666;
          margin-bottom: 10px;
        }
        
        .stat-value {
          font-size: 24px;
          font-weight: bold;
          color: #333;
          margin-bottom: 5px;
        }
        
        .stat-trend {
          font-size: 12px;
          display: flex;
          align-items: center;
          gap: 4px;
          
          &.up {
            color: #52c41a;
          }
          
          &.down {
            color: #f5222d;
          }
        }
      }
    }
  }
}
</style>
