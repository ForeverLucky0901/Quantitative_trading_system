<template>
  <div class="backtest">
    <el-card>
      <template #header>
        <span>策略回测</span>
      </template>
      
      <el-form :model="form" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="选择策略">
              <el-select v-model="form.strategy_id" placeholder="请选择策略" style="width: 100%">
                <el-option label="MA均线策略" :value="1" />
                <el-option label="MACD策略" :value="2" />
                <el-option label="RSI策略" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="初始资金">
              <el-input-number v-model="form.initial_capital" :min="1000" :step="1000" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="开始日期">
              <el-date-picker
                v-model="form.start_date"
                type="date"
                placeholder="选择开始日期"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结束日期">
              <el-date-picker
                v-model="form.end_date"
                type="date"
                placeholder="选择结束日期"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleBacktest">
            开始回测
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card v-if="result" style="margin-top: 20px">
      <template #header>
        <span>回测结果</span>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="6" v-for="item in metrics" :key="item.label">
          <div class="metric-item">
            <div class="metric-label">{{ item.label }}</div>
            <div class="metric-value" :style="{ color: item.color }">
              {{ item.value }}
            </div>
          </div>
        </el-col>
      </el-row>
      
      <div ref="chartRef" style="height: 400px; margin-top: 20px"></div>
      
      <el-table :data="result.trades" style="margin-top: 20px" max-height="300">
        <el-table-column prop="time" label="时间" width="180" />
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'

const form = ref({
  strategy_id: null,
  initial_capital: 100000,
  start_date: '',
  end_date: ''
})

const loading = ref(false)
const result = ref<any>(null)
const chartRef = ref()

const metrics = computed(() => {
  if (!result.value) return []
  return [
    { label: '总收益率', value: `${result.value.total_return}%`, color: result.value.total_return >= 0 ? '#67C23A' : '#F56C6C' },
    { label: '夏普比率', value: result.value.sharpe_ratio, color: '#1890ff' },
    { label: '最大回撤', value: `${result.value.max_drawdown}%`, color: '#F56C6C' },
    { label: '胜率', value: `${result.value.win_rate}%`, color: '#52c41a' }
  ]
})

const handleBacktest = async () => {
  if (!form.value.strategy_id) {
    ElMessage.warning('请选择策略')
    return
  }
  
  loading.value = true
  try {
    // TODO: 调用回测API
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    result.value = {
      total_return: 15.6,
      sharpe_ratio: 1.85,
      max_drawdown: -8.3,
      win_rate: 62.5,
      equity_curve: [100000, 102000, 105000, 103500, 108000, 112000, 115600],
      trades: [
        { time: '2024-01-10 10:00:00', side: 'buy', price: 42000, amount: 0.1, pnl: 0 },
        { time: '2024-01-11 14:30:00', side: 'sell', price: 43000, amount: 0.1, pnl: 100 },
        { time: '2024-01-12 09:15:00', side: 'buy', price: 42500, amount: 0.15, pnl: 0 },
      ]
    }
    
    ElMessage.success('回测完成')
    initChart()
  } catch (error) {
    ElMessage.error('回测失败')
  } finally {
    loading.value = false
  }
}

const initChart = () => {
  if (!chartRef.value || !result.value) return
  
  const chart = echarts.init(chartRef.value)
  const option = {
    title: {
      text: '收益曲线'
    },
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: result.value.equity_curve.map((_: any, i: number) => `Day ${i + 1}`)
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      data: result.value.equity_curve,
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

watch(() => result.value, () => {
  if (result.value) {
    setTimeout(initChart, 100)
  }
})
</script>

<style scoped lang="scss">
.backtest {
  .metric-item {
    text-align: center;
    padding: 20px;
    background: #f5f7fa;
    border-radius: 4px;
    
    .metric-label {
      font-size: 14px;
      color: #666;
      margin-bottom: 10px;
    }
    
    .metric-value {
      font-size: 24px;
      font-weight: bold;
    }
  }
}
</style>
