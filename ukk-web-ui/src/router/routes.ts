
import type { RouteRecordRaw } from 'vue-router'
import identity from './routes_identity'
import { rentalRoutes, rentalUserRoutes } from './routes_rental'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/rental/user'
  },
  {
    path: '/login',
    component: () => import('layouts/AuthLayout.vue'),
    children: [{ name: 'login', path: '', component: () => import('pages/auth/LoginPage.vue') }]
  },
  {
    path: '/signup',
    component: () => import('layouts/AuthLayout.vue'),
    children: [{ name: 'signup', path: '', component: () => import('pages/auth/SignupPage.vue') }]
  },
  {
    path: '/oauth',
    component: () => import('layouts/AuthLayout.vue'),
    children: [{ name: 'login-oauth', path: '', component: () => import('pages/auth/LoginOauth.vue') }]
  },
  {
    path: '/reset-password',
    component: () => import('layouts/AuthLayout.vue'),
    children: [{ name: 'reset-password', path: '', component: () => import('pages/auth/ResetPassword.vue') }]
  },
  {
    path: '/',
    component: () => import('layouts/DashboardLayout.vue'),
    children: [
      { path: '', redirect: '/rental/user' },
      { name: 'home', path: 'home', component: () => import('pages/identity/home/IndexPage.vue') },
      { name: 'audit-trails', path: 'audit-trails', component: () => import('pages/identity/audit-trail/IndexPage.vue') },
      { name: 'user-home', path: 'user-home', redirect: '/rental/user/items' },
      ...identity
    ]
  },
  {
    path: '/rental/user',
    component: () => import('layouts/UserLayout.vue'),
    children: [...rentalUserRoutes]
  },
  {
    path: '/rental',
    component: () => import('layouts/DashboardLayout.vue'),
    children: [...rentalRoutes]
  },
  {
    name: 'config',
    path: '/config',
    component: () => import('pages/auth/config/IndexPage.vue')
  },
  {
    name: 'read-notif',
    path: '/read-notif/:id',
    component: () => import('pages/system/ReadNotif.vue')
  },
  {
    name: '403',
    path: '/403',
    component: () => import('pages/system/ErrorPermission.vue')
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/system/ErrorNotFound.vue')
  }
]

export default routes
