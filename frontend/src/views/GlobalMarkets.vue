<template>
  <div class="global-markets">
    <el-card class="header-card">
      <h2>🌍 全球市场</h2>
      <p>支持全球50+个股票市场和8个加密货币交易所</p>
    </el-card>

    <!-- 市场选择标签 -->
    <el-card class="market-tabs">
      <el-tabs v-model="activeTab" @tab-change="handleTabChange">
        <el-tab-pane label="🌏 亚洲市场" name="asia"></el-tab-pane>
        <el-tab-pane label="🌍 欧洲市场" name="europe"></el-tab-pane>
        <el-tab-pane label="🌎 美洲市场" name="america"></el-tab-pane>
        <el-tab-pane label="🌊 大洋洲市场" name="oceania"></el-tab-pane>
        <el-tab-pane label="💰 加密货币" name="crypto"></el-tab-pane>
      </el-tabs>

      <!-- 市场列表 -->
      <div class="markets-grid">
        <el-card 
          v-for="market in currentMarkets" 
          :key="market.code"
          class="market-card"
          shadow="hover"
          @click="selectMarket(market)"
        >
          <div class="market-info">
            <div class="market-flag">{{ getMarketFlag(market.code) }}</div>
            <div class="market-details">
              <h3>{{ market.name }}</h3>
              <p class="market-exchange">{{ market.exchange }}</p>
              <el-tag size="small">{{ market.stocks_count || 0 }} 只股票</el-tag>
            </div>
          </div>
        </el-card>
      </div>
    </el-card>

    <!-- 选中市场的详情 -->
    <el-card v-if="selectedMarket" class="market-detail">
      <template #header>
        <div class="detail-header">
          <span>{{ getMarketFlag(selectedMarket.code) }} {{ selectedMarket.name }}</span>
          <el-button type="primary" @click="goToTrading">开始交易</el-button>
        </div>
      </template>

      <!-- 热门股票列表 -->
      <el-table :data="popularStocks" stripe>
        <el-table-column prop="symbol" label="代码" width="120"></el-table-column>
        <el-table-column prop="name" label="名称"></el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="viewChart(scope.row)">查看图表</el-button>
            <el-button size="small" type="primary" @click="trade(scope.row)">交易</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 全球指数 -->
    <el-card class="indices-card">
      <template #header>
        <span>📊 全球主要指数</span>
      </template>
      <el-row :gutter="20">
        <el-col :span="6" v-for="(name, code) in majorIndices" :key="code">
          <div class="index-item">
            <div class="index-name">{{ name }}</div>
            <div class="index-code">{{ code }}</div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getAllMarkets, getMajorIndices, getMarketDetail } from '@/api/markets'

const router = useRouter()

const activeTab = ref('asia')
const allMarkets = ref<any>({})
const selectedMarket = ref<any>(null)
const popularStocks = ref<any[]>([])
const majorIndices = ref<Record<string, string>>({})

// 市场区域映射
const regionMap: Record<string, string> = {
  'asia': '亚洲',
  'europe': '欧洲',
  'america': '美洲',
  'oceania': '大洋洲',
  'crypto': '加密货币'
}

// 国旗emoji映射
const flagMap: Record<string, string> = {
  'US': '🇺🇸', 'HK': '🇭🇰', 'CN': '🇨🇳', 'SZ': '🇨🇳',
  'JP': '🇯🇵', 'KS': '🇰🇷', 'IN': '🇮🇳', 'SG': '🇸🇬',
  'TW': '🇹🇼', 'TH': '🇹🇭', 'MY': '🇲🇾', 'ID': '🇮🇩',
  'UK': '🇬🇧', 'DE': '🇩🇪', 'FR': '🇫🇷', 'CH': '🇨🇭',
  'NL': '🇳🇱', 'IT': '🇮🇹', 'ES': '🇪🇸', 'SE': '🇸🇪',
  'CA': '🇨🇦', 'BR': '🇧🇷', 'MX': '🇲🇽', 'AR': '🇦🇷',
  'AU': '🇦🇺', 'NZ': '🇳🇿', 'SA': '🇸🇦', 'ZA': '🇿🇦'
}

// 当前显示的市场列表
const currentMarkets = computed(() => {
  if (activeTab.value === 'crypto') {
    return [] // 加密货币单独处理
  }
  return allMarkets.value[regionMap[activeTab.value]] || []
})

// 获取市场国旗
const getMarketFlag = (code: string) => {
  return flagMap[code] || '🌐'
}

// 加载所有市场
const loadMarkets = async () => {
  try {
    const res = await getAllMarkets()
    allMarkets.value = res.by_region
  } catch (error) {
    console.error('加载市场失败:', error)
  }
}

// 加载主要指数
const loadIndices = async () => {
  try {
    const res = await getMajorIndices()
    majorIndices.value = res.indices
  } catch (error) {
    console.error('加载指数失败:', error)
  }
}

// 选择市场
const selectMarket = async (market: any) => {
  selectedMarket.value = market
  try {
    const res = await getMarketDetail(market.code)
    // 转换热门股票格式
    popularStocks.value = Object.entries(res.popular_stocks || {}).map(([symbol, name]) => ({
      symbol,
      name,
      market: market.code
    }))
  } catch (error) {
    console.error('加载市场详情失败:', error)
  }
}

// 切换标签
const handleTabChange = (tab: string) => {
  selectedMarket.value = null
  popularStocks.value = []
}

// 查看图表
const viewChart = (stock: any) => {
  router.push({
    name: 'Market',
    query: {
      symbol: stock.symbol,
      market: stock.market
    }
  })
}

// 交易
const trade = (stock: any) => {
  router.push({
    name: 'Trading',
    query: {
      symbol: stock.symbol,
      market: stock.market
    }
  })
}

// 前往交易页面
const goToTrading = () => {
  router.push({ name: 'Trading' })
}

onMounted(() => {
  loadMarkets()
  loadIndices()
})
</script>

<style scoped lang="scss">
.global-markets {
  padding: 20px;

  .header-card {
    margin-bottom: 20px;
    text-align: center;

    h2 {
      margin: 0 0 10px 0;
      font-size: 28px;
    }

    p {
      margin: 0;
      color: #666;
    }
  }

  .market-tabs {
    margin-bottom: 20px;
  }

  .markets-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 20px;

    .market-card {
      cursor: pointer;
      transition: all 0.3s;

      &:hover {
        transform: translateY(-5px);
      }

      .market-info {
        display: flex;
        align-items: center;
        gap: 15px;

        .market-flag {
          font-size: 40px;
        }

        .market-details {
          flex: 1;

          h3 {
            margin: 0 0 5px 0;
            font-size: 18px;
          }

          .market-exchange {
            margin: 0 0 10px 0;
            font-size: 12px;
            color: #999;
          }
        }
      }
    }
  }

  .market-detail {
    margin-bottom: 20px;

    .detail-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 20px;
      font-weight: bold;
    }
  }

  .indices-card {
    .index-item {
      padding: 15px;
      background: #f5f7fa;
      border-radius: 8px;
      text-align: center;
      margin-bottom: 10px;

      .index-name {
        font-size: 14px;
        color: #666;
        margin-bottom: 5px;
      }

      .index-code {
        font-size: 12px;
        color: #999;
      }
    }
  }
}
</style>
