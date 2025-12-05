<template>
  <div class="positions">
    <!-- 资产概览 -->
    <el-row :gutter="20">
      <el-col :span="6" v-for="item in assetStats" :key="item.title">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" :style="{ background: item.color }">
              <el-icon :size="30">
                <component :is="item.icon" />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-title">{{ item.title }}</div>
              <div class="stat-value">{{ item.value }}</div>
              <div class="stat-desc">{{ item.desc }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 持仓列表 -->
    <el-card style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <span>持仓列表</span>
          <div>
            <el-button type="primary" size="small" @click="handleRefresh">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
            <el-button size="small" @click="handleCloseAll">
              全部平仓
            </el-button>
          </div>
        </div>
      </template>
      
      <el-table :data="positions" stripe>
        <el-table-column prop="symbol" label="交易对" width="120" />
        <el-table-column prop="side" label="方向" width="80">
          <template #default="{ row }">
            <el-tag :type="row.side === 'long' ? 'success' : 'danger'" size="small">
              {{ row.side === 'long' ? '做多' : '做空' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="持仓数量" />
        <el-table-column prop="entryPrice" label="开仓均价" />
        <el-table-column prop="currentPrice" label="当前价格">
          <template #default="{ row }">
            <span :style="{ color: row.currentPrice >= row.entryPrice ? '#67C23A' : '#F56C6C' }">
              {{ row.currentPrice }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="unrealizedPnl" label="未实现盈亏">
          <template #default="{ row }">
            <span :style="{ color: row.unrealizedPnl >= 0 ? '#67C23A' : '#F56C6C' }">
              {{ row.unrealizedPnl >= 0 ? '+' : '' }}{{ row.unrealizedPnl }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="pnlPercent" label="收益率">
          <template #default="{ row }">
            <span :style="{ color: row.pnlPercent >= 0 ? '#67C23A' : '#F56C6C' }">
              {{ row.pnlPercent >= 0 ? '+' : '' }}{{ row.pnlPercent }}%
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="strategy" label="所属策略" />
        <el-table-column prop="createdAt" label="开仓时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="handleAdjust(row)">
              调整
            </el-button>
            <el-button size="small" type="warning" @click="handleClose(row)">
              平仓
            </el-button>
            <el-button size="small" type="info" @click="handleDetail(row)">
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 持仓分布图 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>持仓分布</span>
          </template>
          <div ref="pieChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>盈亏分析</span>
          </template>
          <div ref="barChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 调整持仓对话框 -->
    <el-dialog v-model="adjustDialogVisible" title="调整持仓" width="500px">
      <el-form :model="adjustForm" label-width="100px">
        <el-form-item label="交易对">
          <el-input v-model="adjustForm.symbol" disabled />
        </el-form-item>
        <el-form-item label="止损价">
          <el-input-number v-model="adjustForm.stopLoss" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="止盈价">
          <el-input-number v-model="adjustForm.takeProfit" :precision="2" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="adjustDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveAdjust">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as echarts from 'echarts'

const assetStats = ref([
  { title: '总资产', value: '125,680 USDT', desc: '≈ $125,680', color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', icon: 'Wallet' },
  { title: '可用余额', value: '85,420 USDT', desc: '可用于交易', color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', icon: 'Coin' },
  { title: '持仓价值', value: '40,260 USDT', desc: '当前持仓', color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', icon: 'TrendCharts' },
  { title: '未实现盈亏', value: '+3,240 USDT', desc: '+8.75%', color: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)', icon: 'DataAnalysis' }
])

const positions = ref([
  {
    id: 1,
    symbol: 'BTC/USDT',
    side: 'long',
    amount: 0.5,
    entryPrice: 40000,
    currentPrice: 42000,
    unrealizedPnl: 1000,
    pnlPercent: 5.0,
    strategy: 'MA策略',
    createdAt: '2024-01-15 10:30:00'
  },
  {
    id: 2,
    symbol: 'ETH/USDT',
    side: 'long',
    amount: 5,
    entryPrice: 2200,
    currentPrice: 2180,
    unrealizedPnl: -100,
    pnlPercent: -0.91,
    strategy: 'MACD策略',
    createdAt: '2024-01-15 14:20:00'
  },
  {
    id: 3,
    symbol: 'BNB/USDT',
    side: 'long',
    amount: 50,
    entryPrice: 320,
    currentPrice: 335,
    unrealizedPnl: 750,
    pnlPercent: 4.69,
    strategy: 'RSI策略',
    createdAt: '2024-01-15 16:45:00'
  }
])

const adjustDialogVisible = ref(false)
const adjustForm = ref({
  symbol: '',
  stopLoss: 0,
  takeProfit: 0
})

const pieChartRef = ref()
const barChartRef = ref()

const handleRefresh = () => {
  ElMessage.success('数据已刷新')
}

const handleCloseAll = () => {
  ElMessageBox.confirm('确定要全部平仓吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('全部平仓成功')
  })
}

const handleAdjust = (row: any) => {
  adjustForm.value = {
    symbol: row.symbol,
    stopLoss: row.entryPrice * 0.95,
    takeProfit: row.entryPrice * 1.1
  }
  adjustDialogVisible.value = true
}

const handleClose = (row: any) => {
  ElMessageBox.confirm(`确定要平仓 ${row.symbol} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('平仓成功')
  })
}

const handleDetail = (row: any) => {
  ElMessage.info(`查看 ${row.symbol} 详情`)
}

const handleSaveAdjust = () => {
  ElMessage.success('调整成功')
  adjustDialogVisible.value = false
}

onMounted(() => {
  initPieChart()
  initBarChart()
})

const initPieChart = () => {
  if (!pieChartRef.value) return
  
  const chart = echarts.init(pieChartRef.value)
  const option = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      bottom: '5%',
      left: 'center'
    },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 20,
          fontWeight: 'bold'
        }
      },
      data: [
        { value: 20000, name: 'BTC/USDT' },
        { value: 10900, name: 'ETH/USDT' },
        { value: 16750, name: 'BNB/USDT' }
      ]
    }]
  }
  chart.setOption(option)
}

const initBarChart = () => {
  if (!barChartRef.value) return
  
  const chart = echarts.init(barChartRef.value)
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      data: [
        { value: 1000, itemStyle: { color: '#67C23A' } },
        { value: -100, itemStyle: { color: '#F56C6C' } },
        { value: 750, itemStyle: { color: '#67C23A' } }
      ],
      type: 'bar',
      barWidth: '60%'
    }]
  }
  chart.setOption(option)
}
</script>

<style scoped lang="scss">
.positions {
  .stat-card {
    .stat-content {
      display: flex;
      align-items: center;
      gap: 15px;
      
      .stat-icon {
        width: 60px;
        height: 60px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
      }
      
      .stat-info {
        flex: 1;
        
        .stat-title {
          font-size: 14px;
          color: #666;
          margin-bottom: 5px;
        }
        
        .stat-value {
          font-size: 20px;
          font-weight: bold;
          color: #333;
          margin-bottom: 5px;
        }
        
        .stat-desc {
          font-size: 12px;
          color: #999;
        }
      }
    }
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style>
