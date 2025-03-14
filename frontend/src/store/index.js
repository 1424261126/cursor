import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
    state: {
        customers: [],
        currentCustomer: null,
        orders: [],
        messages: [],
        tags: [],
        dashboardData: {
            statistics: {
                totalCustomers: 0,
                monthlyOrders: 0,
                monthlySales: 0,
                pendingOrders: 0
            },
            recentOrders: []
        }
    },
    mutations: {
        SET_CUSTOMERS(state, customers) {
            state.customers = customers
        },
        SET_CURRENT_CUSTOMER(state, customer) {
            state.currentCustomer = customer
        },
        SET_ORDERS(state, orders) {
            state.orders = orders
        },
        SET_MESSAGES(state, messages) {
            state.messages = messages
        },
        SET_TAGS(state, tags) {
            state.tags = tags
        },
        SET_DASHBOARD_DATA(state, data) {
            state.dashboardData = data
        }
    },
    actions: {
        async fetchCustomers({ commit }) {
            try {
                const response = await axios.get('/customers/')
                commit('SET_CUSTOMERS', response.data)
            } catch (error) {
                console.error('Error fetching customers:', error)
            }
        },
        async fetchCustomerDetail({ commit }, customerId) {
            try {
                const response = await axios.get(`/customers/${customerId}`)
                commit('SET_CURRENT_CUSTOMER', response.data)
            } catch (error) {
                console.error('Error fetching customer detail:', error)
            }
        },
        async fetchCustomerOrders({ commit }, customerId) {
            try {
                const response = await axios.get(`/customers/${customerId}/orders/`)
                commit('SET_ORDERS', response.data)
            } catch (error) {
                console.error('Error fetching customer orders:', error)
            }
        },
        async fetchCustomerMessages({ commit }, customerId) {
            try {
                const response = await axios.get(`/customers/${customerId}/messages/`)
                commit('SET_MESSAGES', response.data)
            } catch (error) {
                console.error('Error fetching customer messages:', error)
            }
        },
        async fetchCustomerTags({ commit }, customerId) {
            try {
                const response = await axios.get(`/customers/${customerId}/tags/`)
                commit('SET_TAGS', response.data)
            } catch (error) {
                console.error('Error fetching customer tags:', error)
            }
        },
        async createCustomer({ dispatch }, customerData) {
            try {
                await axios.post('/customers/', customerData)
                dispatch('fetchCustomers')
            } catch (error) {
                console.error('Error creating customer:', error)
            }
        },
        async sendMessage({ dispatch }, { customerId, content }) {
            try {
                await axios.post('/messages/', {
                    customer_id: customerId,
                    content,
                    is_ai_generated: false
                })
                dispatch('fetchCustomerMessages', customerId)
            } catch (error) {
                console.error('Error sending message:', error)
            }
        },
        async fetchDashboardData({ commit }) {
            try {
                const response = await axios.get('/dashboard/')
                commit('SET_DASHBOARD_DATA', response.data)
                return response.data
            } catch (error) {
                console.error('Error fetching dashboard data:', error)
                throw error
            }
        }
    }
})