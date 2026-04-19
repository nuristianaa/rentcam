import { defineRouter } from '#q-app/wrappers'
import { createMemoryHistory, createRouter, createWebHashHistory, createWebHistory } from 'vue-router'
import { authStore } from 'src/stores/auth'
import routes from './routes'
// import { configStore } from 'src/stores/config'
// import { Dark } from 'quasar'

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default defineRouter(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER ? createMemoryHistory : process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.VUE_ROUTER_BASE)
  })

  Router.beforeEach((to: any, from: any, next) => {
    const auth = authStore()
    const token = auth.getToken()

    if (to.meta?.requiresAuth && !token) {
      return next({ name: 'login', query: { redirect: to.fullPath } })
    }

    let path = to?.name
    if (!path) path = to?.path
    path = path.replaceAll('/', ' ')
    path = path.replaceAll('-', ' ')
    document.title = 'RentCam rental alat photo | ' + path.replace(/(^\w{1})|(\s+\w{1})/g, (letter: string) => letter.toUpperCase())
    next()
  })

  // Router.beforeEach((to, from, next) => {
  //   const darkMode = configStore().getDarkMode()
  //   if (to.name === 'home') {
  //     Dark.set(true)
  //     setTimeout(() => { Dark.set(true) }, 150)
  //   } else {
  //     Dark.set(darkMode)
  //   }
  //   next()
  // })

  // router/index.ts or router setup file

  return Router
})
