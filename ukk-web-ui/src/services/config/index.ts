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
    return [25, 50, 100, 500, 1000, 10000, 20000, 50000, 100000]
  },
  denseTable() {
    // True: Table jadi compact
    return true
  },
  permissionOnLocal() {
    // True: Permission di simpen di sess storage
    return true
  },
  detetimeInt() {
    // True: Ubah tipe dateTime ke UTC
    return true
  },
  apiUrl(app = 'rental') {
    const appconfig = configStore().getConfig()
    let url = ''
    if (appconfig.login) {
      if (app == 'identity') url = appconfig.url
      else if (app == 'rental') url = appconfig.rental
      else url = appconfig.rental
    } else {
      const hostname = window.location.hostname
      if (hostname == 'ukk.com') {
        const prefix = 'https://api.ukk.com/'
        if (app == 'identity') url = `${prefix}identity/`
        else url = `${prefix}rental/`
      } else if (hostname == 'dev.ukk.com') {
        const prefix = 'https://dev-api.ukk.com/'
        if (app == 'identity') url = `${prefix}identity/`
        else url = `${prefix}rental/`
      } else {
        // localhost development
        if (app == 'identity') url = 'http://localhost:8190/'
        else url = 'http://localhost:8191/'
      }
    }
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