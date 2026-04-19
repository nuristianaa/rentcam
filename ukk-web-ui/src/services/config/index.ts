import { authStore } from 'src/stores/auth'
import { configStore } from 'src/stores/config'
import version from './version'

export const Config = {
  ...version,
  appName() {
    return 'RENTCAM'
  },
  app() {
    return 'rental'
  },
  copyright() {
    return '© 2026'
  },
  ukkCopyright() {
    return '© 2026 RENTCAM | rental alat photo'
  },
  rowsPerPage() {
    return [10, 25, 50, 100]
  },
  denseTable() {
    return true
  },
  permissionOnLocal() {
    return true
  },
  detetimeInt() {
    return true
  },
  apiUrl(app = 'rental') {
    const appconfig = configStore().getConfig()
    let url = ''
    
    // Priority 1: Check process.env (Vercel/Production)
    if (app == 'identity' && process.env.API_URL) {
      url = process.env.API_URL
    } else if (app == 'rental' && process.env.RENTAL_API_URL) {
      url = process.env.RENTAL_API_URL
    } 
    // Priority 2: Check remote config
    else if (appconfig.login) {
      if (app == 'identity') url = appconfig.url
      else url = appconfig.rental
    } 
    // Priority 3: Hardcoded logic
    else {
      const hostname = window.location.hostname
      const isLocal = hostname === 'localhost' || hostname === '127.0.0.1'

      if (hostname == 'ukk.com') {
        const prefix = 'https://api.ukk.com/'
        if (app == 'identity') url = `${prefix}identity/`
        else url = `${prefix}rental/`
      } else if (hostname == 'dev.ukk.com') {
        const prefix = 'https://dev-api.ukk.com/'
        if (app == 'identity') url = `${prefix}identity/`
        else url = `${prefix}rental/`
      } else if (isLocal) {
        // localhost development
        if (app == 'identity') url = 'http://localhost:8190/'
        else url = 'http://localhost:8191/'
      } else {
        // PRODUCTION FALLBACK (Railway)
        if (app == 'identity') url = 'https://discerning-success-production-c616.up.railway.app/'
        else url = 'https://rentcam-production.up.railway.app/'
        
        console.log(`[Config] Using production Railway API for: ${app}`)
      }
    }

    // Ensure trailing slash
    if (url && !url.endsWith('/')) url += '/'
    return url
  },
  getApiRoot(app = 'rental') {
    const version = 'v1/'
    return this.apiUrl(app) + version
  },
  logout() {
    authStore().clearData()
    window.location.assign('/rental/user')
  }
}