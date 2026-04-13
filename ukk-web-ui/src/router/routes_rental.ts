export const rentalUserRoutes = [
  {
    name: 'rental/user',
    path: '',
    component: () => import('pages/rental/user/IndexPage.vue')
  },
  {
    name: 'rental/user/items',
    path: 'items',
    component: () => import('pages/rental/user/items/IndexPage.vue')
  },
  {
    name: 'rental/user/rental',
    path: 'rental',
    component: () => import('pages/rental/user/rental/IndexPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    name: 'rental/user/rental-success',
    path: 'rental/success',
    component: () => import('pages/rental/user/rental/SuccessPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    name: 'rental/user/faq',
    path: 'faq',
    component: () => import('pages/rental/user/faq/IndexPage.vue')
  },
  {
    name: 'rental/user/about',
    path: 'about',
    component: () => import('pages/rental/user/about/IndexPage.vue')
  },
  {
    name: 'rental/user/contact',
    path: 'contact',
    component: () => import('pages/rental/user/contact/IndexPage.vue')
  },
  {
    name: 'rental/user/how-to',
    path: 'how-to',
    component: () => import('pages/rental/user/how-to/IndexPage.vue')
  },
  {
    name: 'rental/user/rental-histories',
    path: 'rental-histories',
    component: () => import('pages/rental/user/rental-histories/IndexPage.vue')
  },
  {
    name: 'user/rental/read',
    path: 'rental-histories/:id',
    component: () => import('pages/rental/user/rental-histories/ReadPage.vue')
  },
  {
    name: 'user-change-profile',
    path: 'update-profile',
    component: () => import('pages/identity/users/UpdateProfile.vue')
  },
  {
    name: 'user-change-password',
    path: 'update-password',
    component: () => import('pages/identity/users/UpdatePassword.vue')
  }
]

export const rentalRoutes = [
  // MASTER
  {
    name: 'rental/master/items',
    path: 'master/items',
    component: () => import('pages/rental/master/items/IndexPage.vue')
  },
  {
    name: 'rental/master/item-categories',
    path: 'master/item-categories',
    component: () => import('pages/rental/master/item-categories/IndexPage.vue')
  },

  // TRANSACTION
  { name: 'transaction/rental-histories', path: 'transaction/rental-histories', component: () => import('pages/rental/transaction/rental-histories/IndexPage.vue') },
  { name: 'read-transaction/rental-histories', path: 'transaction/rental-histories/read/:id', component: () => import('pages/rental/transaction/rentals/DetailPage.vue') },
  { name: 'transaction/rental-invoices', path: 'transaction/rental-invoices', component: () => import('pages/rental/transaction/rental-invoices/IndexPage.vue') },
  { name: 'transaction/rental-checkpoints', path: 'transaction/rental-checkpoints', component: () => import('pages/rental/transaction/rental-checkpoints/IndexPage.vue') },

  { name: 'transaction/rentals', path: 'transaction/rentals', component: () => import('pages/rental/transaction/rentals/IndexPage.vue') },
  { name: 'add-transaction/rentals', path: 'transaction/rentals/form', component: () => import('pages/rental/transaction/rentals/FormPage.vue') },
  { name: 'edit-transaction/rentals', path: 'transaction/rentals/form/:id', component: () => import('pages/rental/transaction/rentals/FormPage.vue') },
  { name: 'view-transaction/rentals', path: 'transaction/rentals/view/:id', component: () => import('pages/rental/transaction/rentals/DetailPage.vue') },

  { name: 'transaction/reports', path: 'transaction/reports', component: () => import('pages/rental/transaction/reports/IndexPage.vue') },

  { name: 'transaction/rental-items', path: 'transaction/rental-items', component: () => import('pages/rental/transaction/rental-items/IndexPage.vue') },
  { name: 'add-transaction/rental-items', path: 'transaction/rental-items/form', component: () => import('pages/rental/transaction/rental-items/FormPage.vue') },
  { name: 'edit-transaction/rental-items', path: 'transaction/rental-items/form/:id', component: () => import('pages/rental/transaction/rental-items/FormPage.vue') },
  { name: 'view-transaction/rental-items', path: 'transaction/rental-items/view/:id', component: () => import('pages/rental/transaction/rentals/DetailPage.vue') },

  { name: 'transaction/payments', path: 'transaction/payments', component: () => import('pages/rental/transaction/payments/IndexPage.vue') },
  { name: 'add-transaction/payments', path: 'transaction/payments/form', component: () => import('pages/rental/transaction/payments/FormPage.vue') },
  { name: 'edit-transaction/payments', path: 'transaction/payments/form/:id', component: () => import('pages/rental/transaction/payments/FormPage.vue') },
  { name: 'view-transaction/payments', path: 'transaction/payments/view/:id', component: () => import('pages/rental/transaction/payments/DetailPage.vue') },

  { name: 'transaction/reviews', path: 'transaction/reviews', component: () => import('pages/rental/transaction/reviews/IndexPage.vue') },
  { name: 'add-transaction/reviews', path: 'transaction/reviews/form', component: () => import('pages/rental/transaction/reviews/FormPage.vue') },
  { name: 'edit-transaction/reviews/', path: 'transaction/reviews/form/:id', component: () => import('pages/rental/transaction/reviews/FormPage.vue') },
  { name: 'view-transaction/reviews', path: 'transaction/reviews/view/:id', component: () => import('pages/rental/transaction/reviews/DetailPage.vue') }
]
