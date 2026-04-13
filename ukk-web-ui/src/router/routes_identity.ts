// import About from "remote/About"
// { path: "/about", component: About }

export default [
  { name: 'auth/users', path: 'users', component: () => import('pages/identity/users/IndexPage.vue') },
  {
    name: 'change-profile',
    path: '/update-profile',
    component: () => import('pages/identity/users/UpdateProfile.vue')
  },
  {
    name: 'change-password',
    path: '/update-password',
    component: () => import('pages/identity/users/UpdatePassword.vue')
  },
  {
    name: 'auth/permissions',
    path: 'permissions',
    component: () => import('pages/identity/permissions/IndexPage.vue')
  },
  { name: 'auth/roles', path: 'roles', component: () => import('pages/identity/roles/IndexPage.vue') },
  {
    name: 'auth/menu-items',
    path: 'menu-items',
    component: () => import('pages/identity/menu-items/IndexPage.vue')
  },
  {
    name: 'auth/master-files',
    path: 'master-files',
    component: () => import('pages/identity/master-files/IndexPage.vue')
  },
  {
    name: 'notifications',
    path: 'notifications',
    component: () => import('pages/identity/notifications/IndexPage.vue')
  },
  {
    name: 'auth/gallery',
    path: 'gallery',
    component: () => import('pages/identity/gallery/IndexPage.vue')
  },
]
