import { createRouter, createWebHistory } from 'vue-router'

const routes = [{
    path: '/',
    name: 'Layout',
    component: () =>
        import ('../views/Layout.vue'),
    children: [{
            path: '',
            name: 'Dashboard',
            component: () =>
                import ('../views/Dashboard.vue')
        },
        {
            path: 'customers',
            name: 'Customers',
            component: () =>
                import ('../views/customers/CustomerList.vue')
        },
        {
            path: 'customers/:id',
            name: 'CustomerDetail',
            component: () =>
                import ('../views/customers/CustomerDetail.vue')
        },
        {
            path: 'orders',
            name: 'Orders',
            component: () =>
                import ('../views/orders/OrderList.vue')
        }
    ]
}]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router