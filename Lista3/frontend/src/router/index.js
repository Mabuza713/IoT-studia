import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/RT_Dataset', component: () => import('../views/RtDatasetView.vue') },
  { path: '/5G_Dataset', component: () => import('../views/FiveG_Dataset.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router