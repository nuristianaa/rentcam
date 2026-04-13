import { defineStore } from 'pinia'
import func from './func'

const defaultData = {
  refresh_token: '',
  token: '',
  token_expire: 0,
  remember: false,
  user: {
    id: 0,
    username: '',
    name: '',
    email: '',
    phone: '',
    profile_picture: '',
    user_type: 'user',
    companies: '',
    vendors: '',
    role_code: 'user',
    role: {
      code: 'user',
      permissions: [
        {
          app: 'identity',
          name: 'home',
          detail: {
            browse: false,
            read: false,
            create: false,
            update: false,
            delete: false,
            restore: false
          }
        }
      ]
    },
    permissions: [
      {
        app: 'identity',
        name: 'home',
        detail: {
          browse: false,
          read: false,
          create: false,
          update: false,
          delete: false,
          restore: false
        }
      }
    ],
    menu: {
      menu_items: [
        { app: 'rental', name: 'Beranda', slug: 'rental/user', path: '/rental/user', icon: 'home' },
        { app: 'rental', name: 'Alat Foto', slug: 'rental/user/items', path: '/rental/user/items', icon: 'photo_camera' },
        { app: 'rental', name: 'Cara Sewa', slug: 'rental/user/how-to', path: '/rental/user/how-to', icon: 'menu_book' },
        { app: 'rental', name: 'Kontak', slug: 'rental/user/contact', path: '/rental/user/contact', icon: 'contacts' },
        { app: 'rental', name: 'Booking', slug: 'rental/user/rental', path: '/rental/user/rental', icon: 'shopping_cart' },
        { app: 'rental', name: 'FAQ', slug: 'rental/user/faq', path: '/rental/user/faq', icon: 'help' },
        { app: 'rental', name: 'About', slug: 'rental/user/about', path: '/rental/user/about', icon: 'info' }
      ]
    },
    menu_favorites: [
      { app: 'rental', name: 'Alat Foto', slug: 'rental/user/items', path: '/rental/user/items', icon: 'photo_camera' }
    ],
    table_configs: [
      {
        app: 'identity',
        module: 'auth/users',
        templates: [{ apply: false, name: 'Test', value: ['id', 'name', 'username'] }]
      }
    ],
    table_summaries: [
      {
        app: 'identity',
        module: 'auth/users',
        summaries: []
      }
    ],
    tracker_token: null,
    additional_permissions: null
  },
  notifications: [],
  company_code: '',
  vendor_code: '',
  app: '',
  printMode: false
}

export const authStore = defineStore('auth', {
  state: () => ({ ...defaultData }),
  actions: {
    getToken() {
      this.token = func.getData(this.$id, 'token', this.$state, 'local')
      return this.token
    },
    getRefreshToken() {
      this.refresh_token = func.getData(this.$id, 'refresh_token', this.$state, 'local')
      return this.refresh_token
    },
    setTokenInfo(data: { access_token: string | null; token_expire: number | null; refresh_token: string | null }) {
      if (data.access_token) {
        this.token = data.access_token
        func.saveData(this.$id, 'token', this.$state, this.token, 'local')
      }
      if (data.refresh_token) {
        this.refresh_token = data.refresh_token
        func.saveData(this.$id, 'refresh_token', this.$state, this.refresh_token, 'local')
      }
      if (data.token_expire) {
        this.token_expire = data.token_expire
        func.saveData(this.$id, 'token_expire', this.$state, this.token_expire, 'local')
      }
    },

    getTokenExpire() {
      this.token_expire = func.getData(this.$id, 'token_expire', this.$state, 'local')
      return this.token_expire
    },
    setTokenExpire(token_expire = 0) {
      func.saveData(this.$id, 'token_expire', this.$state, token_expire, 'local')
      this.token_expire = token_expire
    },

    normalizeUserMenu(data: any) {
      if (!data) return data
      if (Array.isArray(data.menu)) {
        data.menu = { menu_items: data.menu }
      } else {
        data.menu = data.menu || {}
      }
      data.menu.menu_items = Array.isArray(data.menu.menu_items) ? data.menu.menu_items : []
      data.menu_favorites = Array.isArray(data.menu_favorites) ? data.menu_favorites : []
      return data
    },

    fillUserMenuFallback(data: any) {
      // Deteksi role user dengan benar
      const isUserRole = () => {
        if (data.menu?.name === 'user') return true
        if (Array.isArray(data.roles)) {
          return data.roles.some((role: any) => role.name?.toLowerCase() === 'user')
        }
        return false
      }

      // Jika ada menu items dari API, jangan ditimpa - gunakan apa adanya
      if (Array.isArray(data.menu?.menu_items) && data.menu.menu_items.length > 0) {
        // Menu sudah ada dari API, hanya pastikan permissions lengkap
        if (!Array.isArray(data.permissions)) data.permissions = []
        return data
      }

      // Jika menu kosong, isi dengan fallback menu berdasarkan role
      if (isUserRole()) {
        // USER FALLBACK MENU - menu lengkap
        if (!Array.isArray(data.menu?.menu_items) || data.menu.menu_items.length === 0) {
          data.menu.menu_items = [
            { app: 'rental', name: 'Beranda', slug: 'rental/user', path: '/rental/user', icon: 'home' },
            { app: 'rental', name: 'Alat Foto', slug: 'rental/user/items', path: '/rental/user/items', icon: 'photo_camera' },
            { app: 'rental', name: 'Cara Sewa', slug: 'rental/user/how-to', path: '/rental/user/how-to', icon: 'menu_book' },
            { app: 'rental', name: 'Kontak', slug: 'rental/user/contact', path: '/rental/user/contact', icon: 'contacts' },
            { app: 'rental', name: 'Booking', slug: 'rental/user/rental', path: '/rental/user/rental', icon: 'shopping_cart' },
            { app: 'rental', name: 'FAQ', slug: 'rental/user/faq', path: '/rental/user/faq', icon: 'help' },
            { app: 'rental', name: 'About', slug: 'rental/user/about', path: '/rental/user/about', icon: 'info' }
          ]
        }
        if (!Array.isArray(data.menu_favorites) || data.menu_favorites.length === 0) {
          data.menu_favorites = [
            { app: 'rental', name: 'Alat Foto', slug: 'rental/user/items', path: '/rental/user/items', icon: 'photo_camera' }
          ]
        }
        if (!Array.isArray(data.permissions)) data.permissions = []
        return data
      }

      // ADMIN & PETUGAS FALLBACK MENU
      const isAdmin = () => {
        if (Array.isArray(data.roles)) {
          return data.roles.some((role: any) => {
            const roleName = role.name?.toLowerCase() ?? ''
            return roleName.includes('admin') || roleName.includes('super')
          })
        }
        return data?.email === 'superuser@gmail.com' || data?.email === 'admin@gmail.com'
      }

      if (isAdmin()) {
        // ADMIN MENU
        data.menu.menu_items = [
          {
            app: 'RentCam', icon: 'menu', name: 'Menu', path: '/menu', slug: 'menu',
            children: [
              { app: 'core', icon: 'home', name: 'Home', path: '/home', slug: 'home' },
              {
                app: 'core', icon: 'manage_accounts', name: 'User Managements', path: '/user-managements', slug: 'user-managements',
                children: [
                  { app: 'core', icon: 'person', name: 'Users', path: '/users', slug: 'auth/users' },
                  { app: 'core', icon: 'people', name: 'Roles', path: '/roles', slug: 'auth/roles' }
                ]
              },
              { app: 'core', icon: 'web_stories', name: 'Log Activity', path: '/audit-trails', slug: 'logs/audit-trails' },
              { app: 'core', icon: 'settings', name: 'Master Files', path: '/master-files', slug: '"auth/master-files' },
              {
                app: 'core', icon: 'inventory_2', name: 'Master Data', path: '/master', slug: 'master',
                children: [
                  { app: 'core', icon: 'category', name: 'Kategori Alat', path: '/rental/master/item-categories', slug: 'rental/master/item-categories' },
                  { app: 'core', icon: 'camera_alt', name: 'Alat Foto', path: '/rental/master/items', slug: 'rental/master/items' }
                ]
              },
              {
                app: 'core', icon: 'receipt_long', name: 'Transaksi', path: '/transaction', slug: 'transaction',
                children: [
                  { app: 'core', icon: 'assignment', name: 'Rental', path: '/rental/transaction/rentals', slug: 'rental/transaction/rentals' },
                  { app: 'core', icon: 'list_alt', name: 'Item Rental', path: '/rental/transaction/rental-items', slug: 'rental/transaction/rental-items' },
                  { app: 'core', icon: 'history', name: 'Riwayat Rental', path: '/rental/transaction/rental-histories', slug: 'rental/transaction/rental-histories' },
                  { app: 'core', icon: 'payments', name: 'Pembayaran', path: '/rental/transaction/payments', slug: 'rental/transaction/payments' },
                  { app: 'core', icon: 'rate_review', name: 'Ulasan', path: '/rental/transaction/reviews', slug: 'rental/transaction/reviews' }
                ]
              },
              { app: 'core', icon: 'analytics', name: 'Laporan', path: '/rental/transaction/reports', slug: 'rental/transaction/reports' }
            ]
          }
        ]
      } else {
        // PETUGAS MENU
        data.menu.menu_items = [
          {
            app: 'RentCam', icon: 'menu', name: 'Menu', path: '/menu', slug: 'menu',
            children: [
              { app: 'core', icon: 'home', name: 'Home', path: '/home', slug: 'home' },
              { app: 'core', icon: 'assignment', name: 'Rental', path: '/rental/transaction/rentals', slug: 'rental/transaction/rentals' },
              { app: 'core', icon: 'list_alt', name: 'Item Rental', path: '/rental/transaction/rental-items', slug: 'rental/transaction/rental-items' },
              { app: 'core', icon: 'history', name: 'Riwayat Rental', path: '/rental/transaction/rental-histories', slug: 'rental/transaction/rental-histories' },
              { app: 'core', icon: 'payments', name: 'Pembayaran', path: '/rental/transaction/payments', slug: 'rental/transaction/payments' },
              { app: 'core', icon: 'rate_review', name: 'Ulasan', path: '/rental/transaction/reviews', slug: 'rental/transaction/reviews' }
            ]
          }
        ]
      }

      if (!Array.isArray(data.permissions)) data.permissions = []
      return data
    },

    setUser(data: any) {
      if (!data) return
      data = this.normalizeUserMenu(data)
      data = this.fillUserMenuFallback(data)
      func.saveData(this.$id, 'user', this.$state, data, 'local')
      this.user = data
      this.company_code = func.getData(this.$id, 'company_code', this.$state, 'local')
      if (data.company_code && !this.company_code) {
        if (data.company_code.indexOf(',') > -1) {
          const companies = data.company_code.split(',')
          if (companies[0] !== undefined) this.company_code = companies[0]
        } else {
          this.company_code = data.company_code
        }
        func.saveData(this.$id, 'company_code', this.$state, this.company_code, 'local')
      }
    },
    getUser() {
      const token = this.getToken()
      if (!token) {
        const guestUser = this.fillUserMenuFallback(JSON.parse(JSON.stringify(defaultData.user)))
        this.user = guestUser
        func.saveData(this.$id, 'user', this.$state, this.user, 'local')
        return this.user
      }

      this.user = func.getData(this.$id, 'user', this.$state, 'local')
      if (this.user) {
        this.user = this.normalizeUserMenu(this.user)
        this.user = this.fillUserMenuFallback(this.user)
        func.saveData(this.$id, 'user', this.$state, this.user, 'local')
      }
      return this.user
    },

    getMenu() {
      const user = this.getUser()
      const menu = user?.menu
      const menuItems = Array.isArray(menu)
        ? menu
        : Array.isArray(menu?.menu_items)
          ? menu.menu_items
          : []

      const filterGuestMenu = (items: any[]): any[] => {
        return items
          .map((item: any) => {
            const filteredChildren = item.children ? filterGuestMenu(item.children) : []
            return {
              ...item,
              children: filteredChildren.length > 0 ? filteredChildren : item.children ? [] : undefined
            }
          })
          .filter((item: any) => {
            if (!this.getToken() && item.path === '/rental/user/rental') return false
            return true
          })
      }

      return this.getToken() ? menuItems : filterGuestMenu(menuItems)
    },
    getPermissions() {
      const user = this.getUser()
      return user?.permissions ?? []
    },

    setFavs(favs: any) {
      this.user = func.getData(this.$id, 'user', this.$state, 'local')
      this.user.menu_favorites = favs
      func.saveData(this.$id, 'user', this.$state, this.user, 'local')
      return this.user?.menu_favorites
    },
    getFavs() {
      this.user = func.getData(this.$id, 'user', this.$state, 'local')
      return this.user?.menu_favorites
    },

    setTblConfigs(configs: any) {
      this.user = func.getData(this.$id, 'user', this.$state, 'local')
      this.user.table_configs = configs
      func.saveData(this.$id, 'user', this.$state, this.user, 'local')
      return this.user?.table_configs
    },
    getTblConfigs() {
      this.user = func.getData(this.$id, 'user', this.$state, 'local')
      return this.user?.table_configs
    },

    setCompany(data: string) {
      this.company_code = data
      func.saveData(this.$id, 'company_code', this.$state, this.company_code, 'local')
    },
    getCompanyCode() {
      let company_code = func.getData(this.$id, 'company_code', this.$state, 'local')
      // console.log('company_code', company_code)
      // console.log('this', this.company_code)
      if (!company_code) {
        try {
          const companies = this.getCompanies()
          if (companies) company_code = companies[0]
        } catch {
          //
        }
      }

      this.company_code = company_code
      if (company_code && company_code.trim().toLowerCase() == 'all') return null

      return this.company_code
    },
    getCompanies(opt = false, string = false) {
      const user = func.getData(this.$id, 'user', this.$state, 'local')
      const company_code = user.companies
      if (string) return company_code
      if (company_code) {
        const lists = company_code?.split(',')
        const allList = lists.filter((item: string) => item.trim().toLowerCase() != 'all')
        if (opt) return allList
        else {
          if (allList.length > 1) allList.push('All')
          return allList
        }
      } else return []
    },

    setVendor(data: string) {
      this.vendor_code = data
      func.saveData(this.$id, 'vendor_code', this.$state, this.vendor_code, 'local')
    },
    getVendorCode() {
      let vendor_code = func.getData(this.$id, 'vendor_code', this.$state, 'local')
      if (vendor_code == '') return null
      if (!vendor_code) {
        try {
          const vendors = this.getVendors()
          if (vendors) vendor_code = vendors[0]
        } catch {
          //
        }
      }
      this.vendor_code = vendor_code
      if (vendor_code && vendor_code.trim().toLowerCase() == 'all') return null
      return this.vendor_code
    },
    getVendors(opt = false, string = false) {
      const user = func.getData(this.$id, 'user', this.$state, 'local')
      const vendor_code = user.vendors
      if (!vendor_code) return false
      else if (vendor_code == '') return false

      if (string) return vendor_code
      if (vendor_code) {
        const lists = vendor_code?.split(',')
        const allList = lists.filter((item: string) => item.trim().toLowerCase() != 'all')
        if (opt) return allList
        else {
          if (allList.length > 1) allList.push('All')
          return allList
        }
      } else return []
    },

    setApp(data: string) {
      this.app = data
      func.saveData(this.$id, 'app', this.$state, this.app, 'local')
    },
    getApp() {
      this.app = func.getData(this.$id, 'app', this.$state, 'local')
      return this.app
    },

    setData(index: string, data: any) {
      func.saveData(this.$id, index, this.$state, data, 'local')
    },
    getData(index: string) {
      return func.getData(this.$id, index, this.$state, 'local')
    },
    clearData() {
      const data = defaultData
      this.$state = data
      localStorage.setItem(this.$id, JSON.stringify(data))
    },

    getPrintMode() {
      return this.printMode
    },
    setPrintMode(mode: boolean) {
      this.printMode = mode
    },

    setTblSummaries(summaries: any) {
      this.user = func.getData(this.$id, 'user', this.$state, 'local')
      this.user.table_summaries = summaries
      func.saveData(this.$id, 'user', this.$state, this.user, 'local')
      return this.user?.table_summaries
    },

    getTblSummaries() {
      this.user = func.getData(this.$id, 'user', this.$state, 'local')
      return this.user?.table_summaries
    }
  }
})