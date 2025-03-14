# 销售管理系统

这是一个基于FastAPI和Vue 3的销售管理系统,包含客户管理、订单管理、AI自动回复等功能。

## 功能特点

- 客户管理
  - 客户信息管理
  - 客户标签管理
  - AI自动生成客户标签
- 订单管理
  - 订单创建和跟踪
  - 订单状态管理
  - 订单历史记录
- AI对话
  - 智能客服回复
  - 对话历史记录
- 数据统计
  - 销售数据统计
  - 可视化图表展示
  - 实时数据更新

## 技术栈

### 后端
- Python 3.8+
- FastAPI
- SQLAlchemy
- PostgreSQL
- OpenAI API

### 前端
- Vue 3
- Element Plus
- Vuex
- Vue Router
- ECharts
- Axios

## 环境要求

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- OpenAI API密钥

## 安装步骤

### 1. 克隆项目

```bash
git clone <项目地址>
cd demo1
```

### 2. 后端设置

1. 创建并激活虚拟环境:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2. 安装依赖:
```bash
cd backend
pip install -r requirements.txt
```

3. 配置环境变量:
创建 `.env` 文件并添加以下内容:
```
DATABASE_URL=postgresql://user:password@localhost:5432/sales_db
OPENAI_API_KEY=your_api_key
```

4. 初始化数据库:
```bash
python init_db.py
```

### 3. 前端设置

1. 安装依赖:
```bash
cd frontend
npm install
```

2. 配置环境变量:
创建 `.env` 文件并添加:
```
VUE_APP_API_URL=http://localhost:8000
```

## 运行项目

### 1. 启动后端服务

```bash
cd backend
uvicorn main:app --reload
```

后端服务将在 http://localhost:8000 运行

### 2. 启动前端服务

```bash
cd frontend
npm run serve
```

前端服务将在 http://localhost:8080 运行

## 使用说明

1. 访问 http://localhost:8080 打开系统
2. 使用默认管理员账号登录:
   - 用户名: admin
   - 密码: admin123

## 目录结构

```
demo1/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── crud/
│   │   ├── services/
│   │   └── api/
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   ├── store/
│   │   └── App.vue
│   └── package.json
└── README.md
```

## 常见问题

1. 数据库连接失败
   - 检查PostgreSQL服务是否运行
   - 验证数据库连接字符串是否正确

2. 前端API请求失败
   - 确认后端服务是否正常运行
   - 检查API地址配置是否正确

3. AI服务无响应
   - 验证OpenAI API密钥是否有效
   - 检查网络连接是否正常

## 开发团队

- 后端开发: [ken]
- 前端开发: [ken]
- UI设计: [ken]

## 许可证

MIT License 