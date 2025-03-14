<template>
  <div class="order-list">
    <div class="page-header">
      <h2>订单管理</h2>
      <el-button type="primary" @click="showAddDialog">
        新增订单
      </el-button>
    </div>

    <el-card>
      <el-table :data="orders" style="width: 100%">
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
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button
              size="small"
              @click="viewOrder(scope.row)"
            >
              查看
            </el-button>
            <el-button
              size="small"
              type="primary"
              @click="editOrder(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              size="small"
              type="danger"
              @click="deleteOrder(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑订单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增订单' : '编辑订单'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="orderForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="客户" prop="customer_id">
          <el-select v-model="orderForm.customer_id" placeholder="请选择客户">
            <el-option
              v-for="customer in customers"
              :key="customer.id"
              :label="customer.name"
              :value="customer.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="产品名称" prop="product_name">
          <el-input v-model="orderForm.product_name" />
        </el-form-item>
        <el-form-item label="金额" prop="amount">
          <el-input-number v-model="orderForm.amount" :precision="2" :step="0.1" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="orderForm.status">
            <el-option label="待付款" value="待付款" />
            <el-option label="已完成" value="已完成" />
            <el-option label="已取消" value="已取消" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { ElMessage, ElMessageBox } from 'element-plus'

defineOptions({
  name: 'OrderListView'
})

const store = useStore()

const orders = ref([])
const customers = ref([])
const dialogVisible = ref(false)
const dialogType = ref('add')
const formRef = ref(null)
const orderForm = ref({
  customer_id: '',
  product_name: '',
  amount: 0,
  status: '待付款'
})

const rules = {
  customer_id: [{ required: true, message: '请选择客户', trigger: 'change' }],
  product_name: [{ required: true, message: '请输入产品名称', trigger: 'blur' }],
  amount: [{ required: true, message: '请输入金额', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

onMounted(async () => {
  await Promise.all([
    store.dispatch('fetchCustomers'),
    store.dispatch('fetchOrders')
  ])
  customers.value = store.state.customers
  orders.value = store.state.orders
})

const showAddDialog = () => {
  dialogType.value = 'add'
  orderForm.value = {
    customer_id: '',
    product_name: '',
    amount: 0,
    status: '待付款'
  }
  dialogVisible.value = true
}

const editOrder = (order) => {
  dialogType.value = 'edit'
  orderForm.value = { ...order }
  dialogVisible.value = true
}

const viewOrder = (order) => {
  console.log('Viewing order:', order)
}

const deleteOrder = async (order) => {
  try {
    await ElMessageBox.confirm('确定要删除该订单吗？', '提示', {
      type: 'warning'
    })
    // 调用删除API
    await store.dispatch('deleteOrder', order.id)
    ElMessage.success('删除成功')
  } catch (error) {
    console.error('Error deleting order:', error)
  }
}

const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (dialogType.value === 'add') {
          await store.dispatch('createOrder', orderForm.value)
          ElMessage.success('添加成功')
        } else {
          await store.dispatch('updateOrder', {
            id: orderForm.value.id,
            ...orderForm.value
          })
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        await store.dispatch('fetchOrders')
        orders.value = store.state.orders
      } catch (error) {
        console.error('Error submitting form:', error)
        ElMessage.error('操作失败')
      }
    }
  })
}

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
</script>

<style scoped>
.order-list {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style> 