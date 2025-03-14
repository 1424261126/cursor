<template>
  <div class="customer-list">
    <div class="page-header">
      <h2>客户管理</h2>
      <el-button type="primary" @click="showAddDialog">
        添加客户
      </el-button>
    </div>

    <el-card>
      <el-table :data="customers" style="width: 100%">
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="company" label="公司" />
        <el-table-column prop="phone" label="电话" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column label="标签">
          <template #default="scope">
            <el-tag
              v-for="tag in scope.row.tags"
              :key="tag.id"
              class="mx-1"
              :type="tag.is_auto_generated ? 'info' : 'success'"
            >
              {{ tag.tag_name }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button
              size="small"
              @click="viewCustomer(scope.row)"
            >
              查看
            </el-button>
            <el-button
              size="small"
              type="primary"
              @click="editCustomer(scope.row)"
            >
              编辑
            </el-button>
            <el-button
              size="small"
              type="danger"
              @click="deleteCustomer(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑客户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '添加客户' : '编辑客户'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="customerForm"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="customerForm.name" />
        </el-form-item>
        <el-form-item label="公司" prop="company">
          <el-input v-model="customerForm.company" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="customerForm.phone" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="customerForm.email" />
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
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useStore()
const router = useRouter()

const customers = ref([])
const dialogVisible = ref(false)
const dialogType = ref('add')
const formRef = ref(null)
const customerForm = ref({
  name: '',
  company: '',
  phone: '',
  email: ''
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入电话', trigger: 'blur' }],
  email: [{ type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }]
}

onMounted(async () => {
  await store.dispatch('fetchCustomers')
  customers.value = store.state.customers
})

const showAddDialog = () => {
  dialogType.value = 'add'
  customerForm.value = {
    name: '',
    company: '',
    phone: '',
    email: ''
  }
  dialogVisible.value = true
}

const editCustomer = (customer) => {
  dialogType.value = 'edit'
  customerForm.value = { ...customer }
  dialogVisible.value = true
}

const viewCustomer = (customer) => {
  router.push(`/customers/${customer.id}`)
}

const deleteCustomer = async (customer) => {
  try {
    await ElMessageBox.confirm('确定要删除该客户吗？', '提示', {
      type: 'warning'
    })
    // 调用删除API
    await store.dispatch('deleteCustomer', customer.id)
    ElMessage.success('删除成功')
  } catch (error) {
    console.error('Error deleting customer:', error)
  }
}

const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (dialogType.value === 'add') {
          await store.dispatch('createCustomer', customerForm.value)
          ElMessage.success('添加成功')
        } else {
          await store.dispatch('updateCustomer', {
            id: customerForm.value.id,
            ...customerForm.value
          })
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        await store.dispatch('fetchCustomers')
        customers.value = store.state.customers
      } catch (error) {
        console.error('Error submitting form:', error)
        ElMessage.error('操作失败')
      }
    }
  })
}
</script>

<style scoped>
.customer-list {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.el-tag {
  margin-right: 5px;
}
</style> 