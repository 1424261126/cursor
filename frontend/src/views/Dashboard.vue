<template>
  <div class="dashboard">
    <h2>仪表盘</h2>
    
    <!-- 数据统计卡片 -->
    <el-row :gutter="20" class="data-cards">
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>总客户数</span>
              <el-icon><User /></el-icon>
            </div>
          </template>
          <div class="card-value">{{ statistics.totalCustomers }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>本月订单数</span>
              <el-icon><ShoppingCart /></el-icon>
            </div>
          </template>
          <div class="card-value">{{ statistics.monthlyOrders }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>本月销售额</span>
              <el-icon><Money /></el-icon>
            </div>
          </template>
          <div class="card-value">¥{{ statistics.monthlySales.toFixed(2) }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>待处理订单</span>
              <el-icon><Warning /></el-icon>
            </div>
          </template>
          <div class="card-value">{{ statistics.pendingOrders }}</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>销售趋势</span>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="salesTrendOption" autoresize />
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>订单状态分布</span>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="orderStatusOption" autoresize />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近订单列表 -->
    <el-card class="recent-orders">
      <template #header>
        <div class="card-header">
          <span>最近订单</span>
          <el-button type="primary" link @click="$router.push('/orders')">
            查看全部
          </el-button>
        </div>
      </template>
      <el-table :data="recentOrders" style="width: 100%">
        <el-table-column prop="customer_name" label="客户" />
        <el-table-column prop="product_name" label="产品" />
        <el-table-column prop="amount" label="金额">
          <template #default="scope">
            ¥{{ scope.row.amount.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { User, ShoppingCart, Money, Warning } from '@element-plus/icons-vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent
} from 'echarts/components'
import VChart from 'vue-echarts'

use([
  CanvasRenderer,
  LineChart,
  PieChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent
])

const store = useStore()

const statistics = ref({
  totalCustomers: 0,
  monthlyOrders: 0,
  monthlySales: 0,
  pendingOrders: 0
})

const recentOrders = ref([])

// 销售趋势图表配置
const salesTrendOption = ref({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['销售额']
  },
  xAxis: {
    type: 'category',
    data: ['1月', '2月', '3月', '4月', '5月', '6月']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: '销售额',
      type: 'line',
      data: [15000, 18000, 22000, 20000, 25000, 28000]
    }
  ]
})

// 订单状态分布图表配置
const orderStatusOption = ref({
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      name: '订单状态',
      type: 'pie',
      radius: '50%',
      data: [
        { value: 35, name: '已完成' },
        { value: 25, name: '待付款' },
        { value: 15, name: '已取消' }
      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
})

const getStatusType = (status) => {
  const types = {
    '待付款': 'warning',
    '已完成': 'success',
    '已取消': 'danger'
  }
  return types[status] || 'info'
}

const formatDate = (date) => {
  return new Date(date).toLocaleString()
}

onMounted(async () => {
  // 获取仪表盘数据
  try {
    const response = await store.dispatch('fetchDashboardData')
    statistics.value = response.statistics
    recentOrders.value = response.recentOrders
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  }
})

defineOptions({
  name: 'DashboardView'
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.data-cards {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  text-align: center;
  padding: 10px 0;
}

.charts {
  margin-bottom: 20px;
}

.chart-card {
  height: 400px;
}

.chart-container {
  height: 350px;
}

.recent-orders {
  margin-bottom: 20px;
}
</style> 