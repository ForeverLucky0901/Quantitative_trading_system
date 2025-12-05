<template>
  <div class="orders">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>订单记录</span>
          <div>
            <el-button type="primary" size="small" @click="handleRefresh">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
            <el-button size="small" @click="handleExport">
              <el-icon><Download /></el-icon>
              导出
            </el-button>
          </div>
        </div>
      </template>
      
      <!-- 筛选条件 -->
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="交易对">
          <el-select v-model="filterForm.symbol" placeholder="全部" clearable style="width: 150px">
            <el-option label="BTC/USDT" value="BTC/USDT" />
            <el-option label="ETH/USDT" value="ETH/USDT" />
            <el-option label="BNB/USDT" value="BNB/USDT" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="订单类型">
          <el-select v-model="filterForm.orderType" placeholder="全部" clearable style="width: 120px">
            <el-option label="市价单" value="market" />
            <el-option label="限价单" value="limit" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="方向">
          <el-select v-model="filterForm.side" placeholder="全部" clearable style="width: 100px">
            <el-option label="买入" value="buy" />
            <el-option label="卖出" value="sell" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-select v-model="filterForm.status" placeholder="全部" clearable style="width: 120px">
            <el-option label="已成交" value="filled" />
            <el-option label="部分成交" value="partial" />
            <el-option label="待成交" value="pending" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="filterForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 240px"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleFilter">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 订单列表 -->
      <el-table :data="orders" stripe>
        <el-table-column prop="orderId" label="订单ID" width="180" />
        <el-table-column prop="symbol" label="交易对" width="120" />
        <el-table-column prop="side" label="方向" width="80">
          <template #default="{ row }">
            <el-tag :type="row.side === 'buy' ? 'success' : 'danger'" size="small">
              {{ row.side === 'buy' ? '买入' : '卖出' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="orderType" label="类型" width="100">
          <template #default="{ row }">
            <el-tag size="small" :type="row.orderType === 'market' ? 'warning' : 'info'">
              {{ row.orderType === 'market' ? '市价' : '限价' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="价格" />
        <el-table-column prop="amount" label="数量" />
        <el-table-column prop="filled" label="已成交" />
        <el-table-column prop="total" label="总额" />
        <el-table-column prop="fee" label="手续费" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="strategy" label="策略" />
        <el-table-column prop="createdAt" label="创建时间" width="180" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'pending' || row.status === 'partial'"
              size="small"
              type="danger"
              @click="handleCancel(row)"
            >
              取消
            </el-button>
            <el-button size="small" type="info" @click="handleDetail(row)">
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        style="margin-top: 20px; justify-content: flex-end"
      />
    </el-card>
    
    <!-- 统计信息 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="6" v-for="stat in stats" :key="stat.title">
        <el-card>
          <div class="stat-item">
            <div class="stat-label">{{ stat.title }}</div>
            <div class="stat-value" :style="{ color: stat.color }">{{ stat.value }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const filterForm = ref({
  symbol: '',
  orderType: '',
  side: '',
  status: '',
  dateRange: []
})

const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(100)

const orders = ref([
  {
    orderId: 'ORD20240115001',
    symbol: 'BTC/USDT',
    side: 'buy',
    orderType: 'limit',
    price: 42000,
    amount: 0.1,
    filled: 0.1,
    total: 4200,
    fee: 4.2,
    status: 'filled',
    strategy: 'MA策略',
    createdAt: '2024-01-15 10:30:25'
  },
  {
    orderId: 'ORD20240115002',
    symbol: 'ETH/USDT',
    side: 'sell',
    orderType: 'market',
    price: 2250,
    amount: 2,
    filled: 2,
    total: 4500,
    fee: 4.5,
    status: 'filled',
    strategy: 'MACD策略',
    createdAt: '2024-01-15 11:20:15'
  },
  {
    orderId: 'ORD20240115003',
    symbol: 'BNB/USDT',
    side: 'buy',
    orderType: 'limit',
    price: 320,
    amount: 10,
    filled: 5,
    total: 3200,
    fee: 1.6,
    status: 'partial',
    strategy: 'RSI策略',
    createdAt: '2024-01-15 12:10:05'
  },
  {
    orderId: 'ORD20240115004',
    symbol: 'BTC/USDT',
    side: 'buy',
    orderType: 'limit',
    price: 41500,
    amount: 0.05,
    filled: 0,
    total: 2075,
    fee: 0,
    status: 'pending',
    strategy: 'MA策略',
    createdAt: '2024-01-15 13:45:30'
  },
  {
    orderId: 'ORD20240115005',
    symbol: 'SOL/USDT',
    side: 'sell',
    orderType: 'limit',
    price: 100,
    amount: 50,
    filled: 0,
    total: 5000,
    fee: 0,
    status: 'cancelled',
    strategy: '手动交易',
    createdAt: '2024-01-15 14:20:00'
  }
])

const stats = ref([
  { title: '今日订单', value: '25', color: '#409EFF' },
  { title: '成交订单', value: '20', color: '#67C23A' },
  { title: '待成交', value: '3', color: '#E6A23C' },
  { title: '已取消', value: '2', color: '#909399' }
])

const getStatusType = (status: string) => {
  const map: Record<string, any> = {
    filled: 'success',
    partial: 'warning',
    pending: 'info',
    cancelled: 'info'
  }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    filled: '已成交',
    partial: '部分成交',
    pending: '待成交',
    cancelled: '已取消'
  }
  return map[status] || status
}

const handleRefresh = () => {
  ElMessage.success('数据已刷新')
}

const handleExport = () => {
  ElMessage.success('导出成功')
}

const handleFilter = () => {
  ElMessage.info('查询中...')
}

const handleReset = () => {
  filterForm.value = {
    symbol: '',
    orderType: '',
    side: '',
    status: '',
    dateRange: []
  }
}

const handleCancel = (row: any) => {
  ElMessageBox.confirm(`确定要取消订单 ${row.orderId} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    row.status = 'cancelled'
    ElMessage.success('订单已取消')
  })
}

const handleDetail = (row: any) => {
  ElMessage.info(`查看订单 ${row.orderId} 详情`)
}
</script>

<style scoped lang="scss">
.orders {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .filter-form {
    background: #f5f7fa;
    padding: 20px;
    border-radius: 4px;
    margin-bottom: 20px;
  }
  
  .stat-item {
    text-align: center;
    padding: 20px;
    
    .stat-label {
      font-size: 14px;
      color: #666;
      margin-bottom: 10px;
    }
    
    .stat-value {
      font-size: 28px;
      font-weight: bold;
    }
  }
}
</style>
