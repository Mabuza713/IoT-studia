import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/RT_Dataset', component: () => import('../views/Air.vue') },
  { path: '/ETDataset', component: () => import('../views/ETD.vue') },
  { path: '/Reciever', component: () => import('../views/Reciever.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router