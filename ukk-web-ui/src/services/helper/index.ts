import Api from '../api/index'
import { EventBus } from 'quasar'
import alert from './alert'
import date from './date'
import numbers from './numbers'
import text from './text'
import { Config } from '../config'
import { authStore } from 'src/stores/auth'
export const bus = new EventBus()

interface IFramePdf {
  content: string | null
}

export const Helper = {
  ...alert,
  ...date,
  ...numbers,
  ...text,
  bus,
  unreactive<T>(arr: T): T {
    return JSON.parse(JSON.stringify(arr))
  },
  makeAccessToken() {
    let result = ''
    const timemillis = new Date().getTime()
    const day = 60000 * 24 // valid for one day
    const num = Math.round(timemillis / day) * 7777777
    // console.log(num)
    const characters = 'Aa0Bb1Cc2Dd3Ee4Ff5Gg6Hh7Ii8Jj9KkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    const charactersLength = 62
    const myArr = String(num)
      .split('')
      .map((n) => {
        return Number(n)
      })
    const arrlen = myArr.length
    for (let i = 0; i < arrlen; i++) {
      const el = myArr[i]
      if (el !== undefined) {
        const iter = (el + i) * num
        const key = Number(String(iter).slice(-2))
        // console.log(el, i, iter, key)
        const to = Math.floor((key / 99) * charactersLength)
        const fr = to - 1
        result += characters.substring(fr, to)
      }
    }
    return result
  },

  path2UrlBlob(path: string, isPublic: boolean = false) {
    return Config.apiUrl('identity') + 'v1/auth/master-files/view'
  },

  viewBlobFile(path: string, isPublic: boolean | null = false, storageId: string | null = null) {
    const basePath = Config.apiUrl('identity') + 'v1/auth/master-files/view'
    const token = authStore().getToken()
    let res: string = `${basePath}?path=${path}&token=${token}`
    if (isPublic) res += '&mode=public'
    if (storageId) res += `&storage_id=${storageId}`
    return res
  },

  async blobFile(path: string, isPublic: boolean | null = false, storageId: string | null = null) {
    let file = ''
    const API = new Api()
    API.skipNotice = true
    const mode = isPublic ? 'public' : 'private'
    let ep = `auth/master-files/download?mode=${mode}&path=${path}`
    if (storageId) ep += `&storage_id=${storageId}`
    await API.get(
      ep,
      (status: number, _data: any, _message: string, response: any) => {
        API.skipNotice = false
        if (status === 200) {
          const contentType = response.headers['content-type'] || 'application/pdf'
          const blob = new Blob([response.data], { type: contentType })
          file = URL.createObjectURL(blob)
        }
      },
      'main',
      'blob'
    )
    return file
  },


  async getBlobFile(path: string, isPublic = false, storageId: string = null) {
    const API = new Api()
    API.skipNotice = true

    const mode = isPublic ? 'public' : 'private'
    let ep = `auth/master-files/download?mode=${mode}&path=${path}`
    if (storageId) ep += `&storage_id=${storageId}`

    

    return new Promise((resolve) => {
      API.get(
        ep,
        (status: number, _data: any, _message: string, response: any) => {
          API.skipNotice = false
          if (status === 200) {
            const contentType = response.headers['content-type'] || 'application/octet-stream'

            const blob = new Blob([response.data], { type: contentType })
            const filename = path.split('/').pop() || 'file.bin'
            const file = new File([blob], filename, { type: contentType })
            resolve(file) 
          } else {
            resolve(null)
          }
        },
        'main',
        'blob'
      )
    })
  },

  findArrayByKey(arr: any, key: string, value: any, getIndex = false) {
    if (arr === undefined) return null
    if (arr === null) return null

    for (let i = 0; i < arr.length; i++) {
      if (arr[i][key] === value) {
        if (getIndex) return i
        else return arr[i]
      }
    }
    return null
  },

  adjustIframeHeight(iframe: any) {
    // actual type <useTemplateRef>
    const _ifrm = iframe
    if (_ifrm && _ifrm.contentWindow?.document) {
      const contentHeight = _ifrm.contentWindow.document.body.scrollHeight
      const height = contentHeight + 50
      _ifrm.style.height = `${height}px`
    }
  },
  openIframeNewTab(iframe: any) {
    // actual type <useTemplateRef>
    if (iframe) window.open(iframe, '_blank')
  },
  openMergedView(iframeMain: IFramePdf, iframeAtt: IFramePdf) {
    const urlMain = iframeMain.content
    const urlAtt = iframeAtt.content

    if (!urlMain) return

    const newWindow = window.open('', '_blank')

    if (newWindow) {
      const htmlContent = `
        <!DOCTYPE html>
        <html>
        <head>
          <title>Full Document View</title>
          <style>
            body {
              margin: 0;
              padding: 20px;
              background-color: #525659; /* Standard PDF viewer gray */
              display: flex;
              flex-direction: column;
              align-items: center;
              gap: 30px;
            }
            iframe {
              border: none;
              box-shadow: 0 4px 10px rgba(0,0,0,0.25);
              background: white;
            }
            /* Portrait A4 */
            .page-main { width: 210mm; height: 297mm; }
            /* Landscape A4 */
            .page-att { width: 297mm; height: 210mm; }
          </style>
        </head>
        <body>
          <iframe src="${urlMain}" class="page-main"></iframe>
          ${urlAtt ? `<iframe src="${urlAtt}" class="page-att"></iframe>` : ''}
        </body>
        </html>
      `

      newWindow.document.write(htmlContent)
      newWindow.document.close()
    }
  },
  object2columns(obj: object, ignoreKeys: any = []) {
    return Object.keys(obj)
      .filter((key: any) => !ignoreKeys.includes(key))
      .map((key) => ({
        name: key,
        label: this.slug2label(key),
        align: 'left',
        field: key,
        sortable: true
      }))
  },
  /**
   * usage : getFilledArray(list, ['id','name'])
   */
  getFilledArray(details: any = [], exludeKey: string[] = []) {
    return details.filter((item: any) => {
      return Object.entries(item).some(([key, value]) => {
        return !exludeKey.includes(key) && value === true
      })
    })
  },
  printPage() {
    const Auth = authStore()
    Auth.setPrintMode(true)
    setTimeout(() => {
      window.print()
      Auth.setPrintMode(false)
    }, 500)
  }
}