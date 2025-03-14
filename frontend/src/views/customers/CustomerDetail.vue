<template>
  <div class="customer-detail">
    <div class="page-header">
      <el-button @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h2>客户详情</h2>
    </div>

    <el-row :gutter="20">
      <!-- 客户基本信息 -->
      <el-col :span="8">
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <span>基本信息</span>
              <el-button type="primary" link @click="editCustomer">
                编辑
              </el-button>
            </div>
          </template>
          <div v-if="customer" class="info-content">
            <div class="info-item">
              <span class="label">姓名：</span>
              <span>{{ customer.name }}</span>
            </div>
            <div class="info-item">
              <span class="label">公司：</span>
              <span>{{ customer.company }}</span>
            </div>
            <div class="info-item">
              <span class="label">电话：</span>
              <span>{{ customer.phone }}</span>
            </div>
            <div class="info-item">
              <span class="label">邮箱：</span>
              <span>{{ customer.email }}</span>
            </div>
          </div>
        </el-card>

        <el-card class="tags-card">
          <template #header>
            <div class="card-header">
              <span>客户标签</span>
              <el-button type="primary" link @click="showAddTagDialog">
                添加标签
              </el-button>
            </div>
          </template>
          <div class="tags-content">
            <el-tag
              v-for="tag in tags"
              :key="tag.id"
              class="mx-1"
              :type="tag.is_auto_generated ? 'info' : 'success'"
              closable
              @close="deleteTag(tag)"
            >
              {{ tag.tag_name }}
            </el-tag>
          </div>
        </el-card>
      </el-col>

      <!-- 订单列表 -->
      <el-col :span="8">
        <el-card class="orders-card">
          <template #header>
            <div class="card-header">
              <span>订单记录</span>
              <el-button type="primary" link @click="showAddOrderDialog">
                新增订单
              </el-button>
            </div>
          </template>
          <el-table :data="orders" style="width: 100%">
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
      </el-col>

      <!-- 聊天记录 -->
      <el-col :span="8">
        <el-card class="chat-card">
          <template #header>
            <div class="card-header">
              <span>聊天记录</span>
            </div>
          </template>
          <div class="chat-content">
            <div
              v-for="message in messages"
              :key="message.id"
              class="message"
              :class="{ 'ai-message': message.is_ai_generated }"
            >
              <div class="message-content">
                {{ message.content }}
              </div>
              <div class="message-time">
                {{ formatDate(message.created_at) }}
              </div>
            </div>
          </div>
          <div class="chat-input">
            <el-input
              v-model="newMessage"
              type="textarea"
              :rows="3"
              placeholder="输入消息..."
            />
            <el-button type="primary" @click="sendMessage">
              发送
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 添加标签对话框 -->
    <el-dialog
      v-model="tagDialogVisible"
      title="添加标签"
      width="400px"
    >
      <el-form
        ref="tagFormRef"
        :model="tagForm"
        :rules="tagRules"
        label-width="80px"
      >
        <el-form-item label="标签名称" prop="tag_name">
          <el-input v-model="tagForm.tag_name" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="tagDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitTag">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 添加订单对话框 -->
    <el-dialog
      v-model="orderDialogVisible"
      title="新增订单"
      width="500px"
    >
      <el-form
        ref="orderFormRef"
        :model="orderForm"
        :rules="orderRules"
        label-width="100px"
      >
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
          <el-button @click="orderDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitOrder">
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
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'

const store = useStore()
const route = useRoute()

const customer = ref(null)
const orders = ref([])
const messages = ref([])
const tags = ref([])
const newMessage = ref('')

// 标签相关
const tagDialogVisible = ref(false)
const tagFormRef = ref(null)
const tagForm = ref({
  tag_name: ''
})
const tagRules = {
  tag_name: [{ required: true, message: '请输入标签名称', trigger: 'blur' }]
}

// 订单相关
const orderDialogVisible = ref(false)
const orderFormRef = ref(null)
const orderForm = ref({
  product_name: '',
  amount: 0,
  status: '待付款'
})
const orderRules = {
  product_name: [{ required: true, message: '请输入产品名称', trigger: 'blur' }],
  amount: [{ required: true, message: '请输入金额', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

onMounted(async () => {
  const customerId = parseInt(route.params.id)
  await Promise.all([
    store.dispatch('fetchCustomerDetail', customerId),
    store.dispatch('fetchCustomerOrders', customerId),
    store.dispatch('fetchCustomerMessages', customerId),
    store.dispatch('fetchCustomerTags', customerId)
  ])
  
  customer.value = store.state.currentCustomer
  orders.value = store.state.orders
  messages.value = store.state.messages
  tags.value = store.state.tags
})

const formatDate = (date) => {
  return new Date(date).toLocaleString()
}

const getStatusType = (status) => {
  const types = {
    '待付款': 'warning',
    '已完成': 'success',
    '已取消': 'danger'
  }
  return types[status] || 'info'
}

const showAddTagDialog = () => {
  tagForm.value.tag_name = ''
  tagDialogVisible.value = true
}

const submitTag = async () => {
  if (!tagFormRef.value) return
  
  await tagFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await store.dispatch('createCustomerTag', {
          customer_id: customer.value.id,
          ...tagForm.value
        })
        ElMessage.success('添加标签成功')
        tagDialogVisible.value = false
        await store.dispatch('fetchCustomerTags', customer.value.id)
        tags.value = store.state.tags
      } catch (error) {
        console.error('Error adding tag:', error)
        ElMessage.error('添加标签失败')
      }
    }
  })
}

const deleteTag = async (tag) => {
  try {
    await store.dispatch('deleteCustomerTag', tag.id)
    ElMessage.success('删除标签成功')
    await store.dispatch('fetchCustomerTags', customer.value.id)
    tags.value = store.state.tags
  } catch (error) {
    console.error('Error deleting tag:', error)
    ElMessage.error('删除标签失败')
  }
}

const showAddOrderDialog = () => {
  orderForm.value = {
    product_name: '',
    amount: 0,
    status: '待付款'
  }
  orderDialogVisible.value = true
}

const submitOrder = async () => {
  if (!orderFormRef.value) return
  
  await orderFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await store.dispatch('createOrder', {
          customer_id: customer.value.id,
          ...orderForm.value
        })
        ElMessage.success('创建订单成功')
        orderDialogVisible.value = false
        await store.dispatch('fetchCustomerOrders', customer.value.id)
        orders.value = store.state.orders
      } catch (error) {
        console.error('Error creating order:', error)
        ElMessage.error('创建订单失败')
      }
    }
  })
}

const sendMessage = async () => {
  if (!newMessage.value.trim()) return
  
  try {
    await store.dispatch('sendMessage', {
      customerId: customer.value.id,
      content: newMessage.value
    })
    newMessage.value = ''
    await store.dispatch('fetchCustomerMessages', customer.value.id)
    messages.value = store.state.messages
  } catch (error) {
    console.error('Error sending message:', error)
    ElMessage.error('发送消息失败')
  }
}
</script>

<style scoped>
.customer-detail {
  padding: 20px;
}

.page-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0 20px;
}

.info-card,
.tags-card,
.orders-card,
.chat-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-content {
  padding: 10px 0;
}

.info-item {
  margin-bottom: 10px;
}

.label {
  font-weight: bold;
  margin-right: 10px;
}

.tags-content {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.chat-content {
  height: 400px;
  overflow-y: auto;
  padding: 10px;
}

.message {
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 5px;
  background-color: #f4f4f5;
}

.ai-message {
  background-color: #ecf5ff;
  margin-left: 20px;
}

.message-time {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.chat-input {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.chat-input .el-input {
  flex: 1;
}
</style> 