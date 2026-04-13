import axios from 'axios'
import Alert from '../helper/alert'
import { Config } from '../config/index'
import { authStore } from 'src/stores/auth'

type Position = 'top' | 'right' | 'bottom' | 'left' | 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'center' | undefined

export default class Api {
  apiService: any = {}
  token = ''
  app = Config.app()
  skipNotice = false
  multipart_formdata = false
  static get: any

  private static isRefreshing = false
  private static failedQueue: {
    resolve: (token: string) => void
    reject: (err: any) => void
  }[] = []

  constructor() {
    this.apiService = axios.create({
      // timeout: 10000,
      // headers: { 'x-access-token': Alert.makeAccessToken() }
    })
    this.token = authStore().getToken()
  }

  setFormMultipart() {
    this.apiService.defaults.headers['Content-Type'] = 'multipart/form-data'
  }

  // =========================================================
  // REQUEST PER METHOD
  // =========================================================
  get(path: string, callback: any, app = '', resType = 'json') {
    return this.req('GET', app, path, null, callback, false, resType)
  }
  post(path: string, request: any, callback: any, app = '', isMultipart = false, resType = 'json') {
    return this.req('POST', app, path, request, callback, isMultipart, resType)
  }
  put(path: string, request: any, callback: any, app = '', isMultipart = false) {
    return this.req('PUT', app, path, request, callback, isMultipart, 'json')
  }
  patch(path: string, request: any, callback: any, app = '') {
    return this.req('PATCH', app, path, request, callback, false, 'json')
  }
  delete(path: string, request: any, callback: any, app = '') {
    return this.req('DELETE', app, path, request, callback, false, 'json')
  }

  // =========================================================
  // CORE HTTP HANDLER
  // =========================================================
  async req(type: string, app: string, path: string, request: any, callback: any, isMultipart = false, resType = 'json') {
    const config = this.buildConfig(type, app, path, request, isMultipart, resType)

    try {
      const response = await this.apiService.request(config)
      if (config.responseType === 'blob') {
        callback(200, null, null, response)
        return
      }
      const res = this.transformRes(response)

      if (this.validateResponseData(res, path)) callback(res.status, res.data, res.message, response)
    } catch (error: any) {
      console.warn('api_res_error', error)
      if (error?.response) {
        const res = this.transformRes(error?.response ?? error)

        if (res.status === 401) return this.handle401Retry(config, callback)
        else this.validateResponseData(res, path)
        callback(res.status, res.data, res.message, error)
      } else {
        Alert.showToast('Failed to load resource from server.', 'negative', 5000, 'bottom')
        callback(500, null, null, error)
      }
    }
  }

  private buildConfig(type: string, app: string, path: string, request: any, isMultipart = false, resType = 'json') {
    const headers: Record<string, string> = {}
    headers['Access-Control-Allow-Origin'] = '*'

    // Content Type
    if (isMultipart) headers['Content-Type'] = 'multipart/form-data'
    else if (this.multipart_formdata) headers['Content-Type'] = 'multipart/form-data'
    else if (path == 'token') headers['Content-Type'] = 'application/x-www-form-urlencoded'
    else headers['Content-Type'] = 'application/json'

    // BASE URL Resolver
    let apiroot = ''
    const loc_hash = window.location.pathname

    if (app) apiroot = Config.getApiRoot(app)
    else if (path.indexOf('auth/') == 0) apiroot = Config.getApiRoot('identity')
    else if (path.indexOf('me/') == 0) apiroot = Config.getApiRoot('identity')
    else if (loc_hash.indexOf('/rental/') == 0) apiroot = Config.getApiRoot('rental')
    else apiroot = Config.getApiRoot('identity')

    // Attach JWT only when token exists
    if (path !== 'token' && path !== 'auth/users/public') {
      this.token = authStore().getToken()
      if (this.token) {
        headers['Authorization'] = `Bearer ${this.token}`
      }
    }

    // Axios config
    const config: any = { method: type, url: apiroot + path, responseType: resType, headers }
    // STORE OR UPDATE | Attach request for data
    if (type !== 'GET') Object.assign(config, { data: request })

    return config
  }

  private transformRes(response: any) {
    const res = response?.data

    return {
      status: response?.status ?? 401,
      data: res?.data !== undefined ? res.data : res,
      message: res?.status?.message ?? res?.message ?? response?.statusText,
      response: response
    }
  }

  private validateResponseData(res: any, path: string) {
    if (this.skipNotice) return false

    let color = 'negative'
    const timeout = 10000
    let msg = 'Failed to load resource from server.'
    let pos = <Position>'center'
    if (res.status === 200) {
      return true
    } else if (res.status === 400) {
      msg = res.message
      color = 'info'
      pos = 'center'
    } else if (res.status === 403) {
      msg = `Forbidden (403) | ${res.message ?? ''}`
      color = 'deep-orange-7'
      pos = 'center'
    } else if (res.status === 404) {
      msg = 'Not Found 404'
      color = 'accent'
      pos = 'bottom'
    } else if (405 <= res.status && res.status < 500) {
      msg = res.message
      color = 'accent'
      pos = 'bottom'
    } else if (500 <= res.status && res.status < 600) {
      msg = `Server Error ${res.status} | ${res.message}`
      color = 'negative'
      pos = 'bottom'
    } else if (res.message == 'Network Error') {
      msg = 'Network Error. The server is unreachable.'
      color = 'negative'
      pos = 'bottom'
    } else {
      msg = 'Error in UI Section. ' + JSON.stringify(res)
      pos = 'bottom'
      console.warn(`path: ${path}`, msg, JSON.stringify(res))
      if (window.location.host.indexOf('localhost') == -1) return false
    }

    Alert.showToast(msg, color, timeout, pos)
    return false
  }

  // =========================================================
  // REFRESH TOKEN + QUEUE
  // =========================================================
  private async handle401Retry(originalConfig: any, callback: any) {
    const refreshToken = authStore().getRefreshToken()
    if (!refreshToken) {
      Alert.showToast('Session expired. Please login again.', 'negative', 12000, 'center')
      return Config.logout()
    }

    // Already refreshing → add to queue
    if (Api.isRefreshing) {
      return new Promise<string>((resolve, reject) => {
        Api.failedQueue.push({ resolve, reject })
      })
      .then((newToken: string) => {
        originalConfig.headers.Authorization = `Bearer ${newToken}`
        return this.apiService.request(originalConfig).then((response: any) => {
          const res = this.transformRes(response)
          callback(res.status, res.data, res.message, response)
        })
      })
      .catch((err) => {
        console.warn(err)
        Alert.showToast('Session expired. Please login again.', 'negative', 12000, 'center')
        return Config.logout()
      })
    }

    Api.isRefreshing = true

    return new Promise<string>((resolve, reject) => {
      void (async () => {
        try {
          const newToken = await this.doRefreshToken()

          Api.failedQueue.forEach((p) => p.resolve(newToken))
          Api.failedQueue = []

          // Retrying original request
          originalConfig.headers.Authorization = `Bearer ${newToken}`
          const retryResponse = await this.apiService.request(originalConfig)

          const res = this.transformRes(retryResponse)
          callback(res.status, res.data, res.message, retryResponse)

          resolve(retryResponse)
        } catch (err) {
          Api.failedQueue.forEach((p) => p.reject(err))
          Api.failedQueue = []

          Alert.showToast('Session expired. Please login again.', 'negative', 12000, 'center')
          Config.logout()

          reject(err instanceof Error ? err : new Error(String(err)))
        } finally {
          Api.isRefreshing = false
        }
      })()
    })
  }

  // =========================================================
  // DO REFRESH TOKEN
  // =========================================================
  private async doRefreshToken(): Promise<string> {
    const apiUrl = Config.getApiRoot('main')
    const refreshToken = authStore().getRefreshToken()

    const r = await axios.post(`${apiUrl}refresh-token`, {refresh_token: refreshToken})

    if (r.status !== 200 || !r.data?.access_token) throw new Error('Invalid refresh token')

    authStore().setTokenInfo({
      access_token: r.data.access_token,
      refresh_token: r.data.refresh_token,
      token_expire: r.data.expire_token
    })

    return r.data.access_token
  }
}
