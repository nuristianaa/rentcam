import { defineStore } from 'pinia'
import { Dark } from 'quasar'
import func from './func'

const state = {
  dark_mode: <boolean | 'auto'>false,
  sidebar: '',
  lang: '',
  audit_trail_cfg: <
    {
      cols: string[]
      as_json: boolean
    }
  >{
    cols: [],
    as_json: false
  },
  appconfig: {
    login: false,
    url: 'https://discerning-success-production-c616.up.railway.app/',
    rental: 'https://rentcam-production.up.railway.app/',
  },
  csvdelimiter: ','
}

export const configStore = defineStore('config', {
  state: () => state,
  actions: {
    getDarkMode() {
      this.dark_mode = func.getData(this.$id, 'dark_mode', state)
      Dark.set(this.dark_mode)
      return this.dark_mode
    },
    setDarkMode(type: boolean | 'auto') {
      this.dark_mode = func.saveData(this.$id, 'dark_mode', state, type)
      Dark.set(type)
      // Dark.toggle()
      return this.dark_mode
    },

    getConfig() {
      this.appconfig = func.getData(this.$id, 'appconfig', this.$state)
      return this.appconfig
    },
    saveConfig(data: any) {
      this.appconfig = func.saveData(this.$id, 'appconfig', this.$state, data)
      return this.appconfig
    },

    getData(index: string) {
      return func.getData(this.$id, index, this.$state)
    },
    setData(index: string, data: any) {
      func.saveData(this.$id, index, this.$state, data)
    },

    // AUDIT TRAILS CONFIG
    getAuditTrailCfg() {
      this.audit_trail_cfg = func.getData(this.$id, 'audit_trail_cfg', this.$state, 'session')
      if (!this.audit_trail_cfg) this.$patch({ audit_trail_cfg: { cols: [], as_json: false } })
      return this.audit_trail_cfg
    },
    setAuditTrailCfg(item: any) {
      this.audit_trail_cfg = func.saveData(this.$id, 'audit_trail_cfg', this.$state, item, 'session')
      return this.audit_trail_cfg
    }
  }
})
