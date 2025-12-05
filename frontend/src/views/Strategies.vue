<template>
  <div class="strategies">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>策略管理</span>
          <el-button type="primary" @click="handleCreate">
            <el-icon><Plus /></el-icon>
            新建策略
          </el-button>
        </div>
      </template>
      
      <el-table :data="strategies" stripe>
        <el-table-column prop="name" label="策略名称" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="return" label="收益率">
          <template #default="{ row }">
            <span :style="{ color: row.return >= 0 ? '#67C23A' : '#F56C6C' }">
              {{ row.return >= 0 ? '+' : '' }}{{ row.return }}%
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column label="操作" width="300">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button
              size="small"
              :type="row.status === 'active' ? 'warning' : 'success'"
              @click="handleToggle(row)"
            >
              {{ row.status === 'active' ? '停止' : '启动' }}
            </el-button>
            <el-button size="small" type="info" @click="handleBacktest(row)">回测</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 策略编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑策略' : '新建策略'"
      width="800px"
    >
      <el-form :model="form" label-width="100px">
        <el-form-item label="策略名称">
          <el-input v-model="form.name" placeholder="请输入策略名称" />
        </el-form-item>
        <el-form-item label="策略描述">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入策略描述"
          />
        </el-form-item>
        <el-form-item label="策略代码">
          <el-input
            v-model="form.code"
            type="textarea"
            :rows="15"
            placeholder="请输入策略代码"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const strategies = ref([
  { id: 1, name: 'MA均线策略', description: '基于移动平均线的交易策略', status: 'active', return: 12.5, created_at: '2024-01-10 10:00:00' },
  { id: 2, name: 'MACD策略', description: 'MACD指标交易策略', status: 'inactive', return: -3.2, created_at: '2024-01-11 14:30:00' },
  { id: 3, name: 'RSI策略', description: 'RSI超买超卖策略', status: 'active', return: 8.7, created_at: '2024-01-12 09:15:00' },
])

const dialogVisible = ref(false)
const isEdit = ref(false)
const form = ref({
  name: '',
  description: '',
  code: ''
})

const getStatusType = (status: string) => {
  const map: Record<string, any> = {
    active: 'success',
    inactive: 'info',
    paused: 'warning'
  }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    active: '运行中',
    inactive: '已停止',
    paused: '已暂停'
  }
  return map[status] || status
}

const handleCreate = () => {
  isEdit.value = false
  form.value = { name: '', description: '', code: '' }
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  isEdit.value = true
  form.value = { ...row }
  dialogVisible.value = true
}

const handleSave = () => {
  // TODO: 调用API保存策略
  ElMessage.success('保存成功')
  dialogVisible.value = false
}

const handleToggle = (row: any) => {
  const action = row.status === 'active' ? '停止' : '启动'
  ElMessageBox.confirm(`确定要${action}该策略吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    row.status = row.status === 'active' ? 'inactive' : 'active'
    ElMessage.success(`${action}成功`)
  })
}

const handleBacktest = (row: any) => {
  ElMessage.info('跳转到回测页面')
}

const handleDelete = (row: any) => {
  ElMessageBox.confirm('确定要删除该策略吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    ElMessage.success('删除成功')
  })
}
</script>

<style scoped lang="scss">
.strategies {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style>
