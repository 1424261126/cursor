<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <el-menu
        :router="true"
        class="el-menu-vertical"
        :default-active="$route.path"
      >
        <el-menu-item index="/">
          <el-icon><DataLine /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/customers">
          <el-icon><User /></el-icon>
          <span>客户管理</span>
        </el-menu-item>
        <el-menu-item index="/orders">
          <el-icon><ShoppingCart /></el-icon>
          <span>订单管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header>
        <div class="header-content">
          <h2>销售管理系统</h2>
          <el-dropdown>
            <span class="user-info">
              管理员 <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>个人信息</el-dropdown-item>
                <el-dropdown-item>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { DataLine, User, ShoppingCart, ArrowDown } from '@element-plus/icons-vue'

defineOptions({
  name: 'MainLayout'
})
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.el-aside {
  background-color: #304156;
}

.el-menu {
  border-right: none;
}

.el-header {
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
  padding: 0 20px;
}

.header-content {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.el-main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style> 