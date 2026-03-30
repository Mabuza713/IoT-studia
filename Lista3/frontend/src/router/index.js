import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
    { path: '/', component: Home },
    { path: '/GOV', component: () => import('../views/GOV.vue') },
    { path: '/ETDataset', component: () => import('../views/ETD.vue') },
    { path: '/SOLAR', component: () => import('../views/SOLAR.vue') },
    { path: '/ENERGY', component: () => import('../views/ENERGY.vue') },
    { path: '/Reciever', component: () => import('../views/Reciever.vue') },
    { path: '/NEWYORK', component: () => import('../views/NEWYORK.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router