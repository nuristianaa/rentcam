/* eslint-disable */
import { Helper } from '../helper/index'
import Api from '../api/index'
import { Config } from '../config/index'
import { Constant } from '../constant/index'
import { Lang } from '../lang'
import { authStore } from 'src/stores/auth'
import * as XLSX from 'xlsx'
import { Notify } from 'quasar'

type Table = {
  name: string
  label: string
  field: string
  align?: string
  style?: string
  sortable?: boolean
  hide?: boolean
  filterHide?: boolean
  colHide?: boolean
  is_date?: boolean
  millis?: boolean
  datetime?: boolean
  api?: string
  opt?: any
  config?: boolean
  rowsPerPage?: number
  sortBy?: string
  ascending?: boolean
}[]

type Config = {
  app?: string | null
  schema?: string | null
  name?: string | null
  exclude?: string[]
  float?: string[]
  integer?: string[]
  date?: string[]
  datetime?: string[]
  constant?: string[]
  money?: string[]
  detail?: string[]
}

type DataListConfig = {
  app?: string | null
  schema?: string | null
  name?: string | null
  exclude?: string[]
  float?: string[]
  integer?: string[]
  date?: string[]
  datetime?: string[]
  constant?: string[]
  money?: string[]
  items?: string[]
}

type Data = Record<string, any>

export const Handler = {
  /* MODULE HANDLER */
  table(cols: Table = []) {
    // Default Value
    const columns = []
    let rowsPerPage = Config.rowsPerPage()[0] !== undefined ? Config.rowsPerPage()[0] : 10
    let sortBy = 'created_at'
    let descending = true

    // Convert Cols
    let config = null
    for (const col of cols) {
      if (col.name !== 'action' && col?.sortable !== false) col.sortable = true
      else col.sortable = false
      if (col.hide !== true && col.config !== true) columns.push(col)

      // Custom Config in first array | sorted by
      if (col.config === true) {
        config = col
        if (col.rowsPerPage) rowsPerPage = col.rowsPerPage
        if (col.sortBy) sortBy = col.sortBy
        if (col.ascending) descending = false
      }
    }

    // searchBy & Columns Visibility
    const visibleColumns = []
    // const columnFields = []
    for (const col of columns) {
      const obj = {
        id: col.name,
        name: col.label ?? col.name,
        field: col.name, // (col.search) ? col.search : col.field
        api: col.api ?? null, // select opt api
        opt: col.opt ?? null, // select opt static
        is_date: col.is_date ?? null,
        value: null
      }
      if (col.config !== true && col.hide !== true) {
        if (col.colHide !== true) visibleColumns.push(col.name)
      }
      // if(col.config !== true) {
      // if (col.name !== 'action') columnFields.push(col.name)
      // else columnFields.push(col.field)
      // }
    }

    const table = {
      loading: false,
      data: [],
      columns: columns,
      pagination: {
        page: 1,
        rowsPerPage: rowsPerPage,
        sortBy: sortBy,
        descending: descending,
        rowsNumber: 0
      },
      selected: [],
      visibleColumns: visibleColumns,
      // columnFields: columnFields,
      search: null, // native search
      searchBySelected: [], // array object while doing filters {'name': colName, 'value': 'like=colname:value'}
      config: config
    }
    return table
  },
  viewList(data: Data, config: Config, _this: any = null): { label: string; value: any }[] {
    const app = config?.app ?? null
    const schema = config?.schema ?? null
    const name = config?.name ?? null
    const meta = { app, schema, name }
    const modules = app ? `${app}.${schema}.${name}` : `${schema}.${name}`

    const exclude = config?.exclude ?? []
    const float = config?.float ?? []
    const integer = config?.integer ?? []
    const date = config?.date ?? []
    const datetime = config?.datetime ?? []
    const constant = config?.constant ?? []
    const money = config?.money ?? []
    const detail = config?.detail ?? []

    const excludes = [...exclude, 'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'deleted_by']

    const list: { label: string; value: any }[] = []

    for (const key in data) {
      if (!excludes.includes(key)) {
        const label = Lang.module(meta, key) // Assuming Lang.module is a valid utility function
        let value = data[key]

        // Apply transformations based on config
        if (float.includes(key)) {
          value = Helper.formatNumber(value) // Assuming Helper.formatNumber exists
        } else if (integer.includes(key)) {
          value = Helper.formatNumber(value, 0) // Format as integer
        } else if (date.includes(key)) {
          value = Helper.readDate(value) // Format as date
        } else if (datetime.includes(key)) {
          value = Helper.readDate(value, true) // Format as datetime
        } else if (constant.includes(key)) {
          value = Constant.translate(value, `${modules}.${key}`) // Assuming Constant.translate exists
        } else if (money.includes(key)) {
          value = Helper.formatMoney(value) // Format as money
        } else if (detail.includes(key)) {
          value = value?.code ?? value?.name ?? '-' // Handle detail objects
        } else if (Array.isArray(value)) {
          value = JSON.stringify(value) // Serialize arrays
        }

        list.push({ label, value })
      }
    }
    list.sort((a, b) => a.label.localeCompare(b.label))
    return list
  },
  dataList(data: Data, config: DataListConfig): { label: string; value: any }[] {
    const app = config?.app ?? null
    const schema = config?.schema ?? null
    const name = config?.name ?? null
    const meta = { app, schema, name }
    const modules = app ? `${app}.${schema}.${name}` : `${schema}.${name}`
    const items = config.items ? config.items : []

    const float = config?.float ?? []
    const integer = config?.integer ?? []
    const date = config?.date ?? []
    const datetime = config?.datetime ?? []
    const constant = config?.constant ?? []
    const money = config?.money ?? []

    const list: { label: string; value: any }[] = []

    items.forEach((key) => {
      const label = Lang.module(meta, key)
      let value = data[key]

      // Apply transformations based on config
      if (float.includes(key)) {
        value = Helper.formatNumber(value) // Assuming Helper.formatNumber exists
      } else if (integer.includes(key)) {
        value = Helper.formatNumber(value, 0) // Format as integer
      } else if (date.includes(key)) {
        value = Helper.readDate(value) // Format as date
      } else if (datetime.includes(key)) {
        value = Helper.readDate(value, true) // Format as datetime
      } else if (constant.includes(key)) {
        value = Constant.translate(value, `${modules}.${key}`) // Assuming Constant.translate exists
      } else if (money.includes(key)) {
        value = Helper.formatMoney(value) // Format as money
      } else if (Array.isArray(value)) {
        value = JSON.stringify(value) // Serialize arrays
      }

      list.push({
        label: label,
        value: value
      })
    })
    return list
  },
  permissions(router: any, action: string, meta: any, callback: { (status: any, data: any): void; (arg0: boolean, arg1: any): void }) {
    const app = meta.app
    const slug = meta.module
    const permissions = authStore().getPermissions() ?? []
    let status = false
    for (const e of permissions) {
      if (e && slug && ((app && app === e.app && slug === e.name) || (!app && slug === e.name))) {
        meta.permission = e.detail
        if (meta.permission[action]) status = true
        break
      }
    }
    const permissionName = `${app} - ${slug}.${action}`
    if (!status) {
      router.push({
        name: '403',
        state: {
          permission: permissionName
        }
      })
    }
    callback(status, meta.permission)
  },
  /* END OF MODULE HANDLER */

  /* HANDLING FILES */
  formData(data: any) {
    const dataModel = new FormData()
    // if(data.id || data._id) dataModel.append('_method', 'PUT')
    for (const key in data) {
      if (data[key]) dataModel.append(key, data[key])
    }
    return dataModel
  },
  async storeFile(dataModel: any, callback: any, endpoint = 'auth/master-files') {
    const model = this.formData(dataModel)
    const API = new Api()
    let dataapi = null
    let msg = 'upload failed'
    let ep = endpoint
    if (dataModel.id > 0) ep += `/${dataModel.id}`
    await API.post(
      ep,
      model,
      (status: number, data: any) => {
        if (status === 200) {
          dataapi = data
          msg = 'upload success'
        }
      },
      'identity',
      true
    )
    callback(dataapi, msg)
  },
  exportData(data: any, filename: string) {
    let blob = new Blob([data], { type: 'application/octet-stream' })
    let link = document.createElement('a')
    link.href = window.URL.createObjectURL(blob)
    link.download = `${filename}.xlsx`
    link.click()
  },
  exportXLS(meta: { tableExport: any; tableExportSample: any[]; name: string }) {
    const tempArr: any[] = []
    const columns = meta.tableExport(Helper, Constant, Lang)
    meta.tableExportSample.forEach((x: any, xIndex: string | number) => {
      const tempData = <any>{}
      columns.forEach((y: { label: any; field: (arg0: any) => any; name: any; formatter: string }) => {
        const label = y.label
        const field = typeof y.field === 'function' ? y.name : y.field

        // Get value from original data
        let value = x[field]

        if (typeof value === 'object') value = JSON.stringify(value)
        if (typeof y.field === 'function') value = y.field(x)
        if (Array.isArray(value)) value = JSON.stringify(value)

        if (y.formatter) {
          if (y.formatter == 'float') value = value ? parseFloat(value) : 0
          else if (y.formatter == 'integer') value = value ? parseInt(value) : 0
          else if (y.formatter == 'date') value = Helper.toDate(value, 'YYYY-MM-DD')
          else if (y.formatter == 'time') value = Helper.toDate(value, 'HH:mm:ss')
          else if (y.formatter == 'datetime') value = Helper.toDate(value, 'YYYY-MM-DD HH:mm:ss')
          else if (y.formatter == 'millis') value = Helper.toDate(value, 'YYYY-MM-DD HH:mm:ss')
        }

        tempData[label] = value
      })
      tempArr.push(tempData)
    })
    const data = XLSX.utils.json_to_sheet(tempArr)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, data, 'data')
    XLSX.writeFile(wb, `${meta.name}-table-import-template.xlsx`)
  },
  /* _type avail :
    min-char-{lenght}
    max-char-{lenght}
    min-numb-{lenght}
    max-numb-{lenght}
    min-max-char-{lenghtMin}-{lengthMax}
    min-max-numb-{lenghtMin}-{lengthMax}
    required
  */
  rules(_type = 'required', _msg = null, _raw = false, t = null) {
    let mxVal = null
    let minVal = 0
    let maxVal = 0
    let msg = ''
    let length = 0
    let res: any = []
    let minChar: any = _type.split(/min-char-/)
    let maxChar: any = _type.split(/max-char-/)
    let minNumb: any = _type.split(/min-numb-/)
    let maxNumb: any = _type.split(/max-numb-/)
    let minMaxChar: any = _type.split(/min-max-char-/)
    let minMaxNumb: any = _type.split(/min-max-numb-/)

    // minumum character
    if (minChar.length === 2 && minChar[0] === '') {
      length = parseInt(minChar[1])
      msg = `Minimal ${length} characters`
      msg = _msg ? _msg : msg
      res = [(val: any) => (!!val && val.length >= length) || msg]
    }
    // maximum character
    else if (maxChar.length === 2 && maxChar[0] === '') {
      length = parseInt(maxChar[1])
      msg = `Maximum ${length} characters`
      msg = _msg ? _msg : msg
      res = [(val: any) => (!!val && val.length <= length) || msg]
    }
    // minumum number value
    else if (minNumb.length === 2 && minNumb[0] === '') {
      length = parseInt(minNumb[1])
      msg = `Minimal value is ${length}`
      msg = _msg ? _msg : msg
      res = [(val: any) => (!!val && val >= length) || msg]
    }
    // maximum number value
    else if (maxNumb.length === 2 && maxNumb[0] === '') {
      length = parseInt(maxNumb[1])
      msg = `Maximum value is ${length}`
      msg = _msg ? _msg : msg
      res = [(val: any) => val <= length || msg]
    }
    // minumum & maximum character
    else if (minMaxChar.length === 2 && minMaxChar[0] === '') {
      mxVal = minMaxChar[1].split('-')
      if (mxVal.length === 2) {
        minVal = parseInt(mxVal[0])
        maxVal = parseInt(mxVal[1])

        const minMsg = `Min ${minVal} characters`
        const maxMsg = `Max ${maxVal} characters`
        res = [(val: any) => ((!!val && val.length >= minVal) || _msg ? _msg : minMsg), (val: any) => ((!!val && val.length <= maxVal) || _msg ? _msg : maxMsg)]
      }
    }
    // minumum & maximum number
    else if (minMaxNumb.length === 2 && minMaxNumb[0] === '') {
      mxVal = minMaxNumb[1].split('-')
      if (mxVal.length === 2) {
        minVal = parseInt(mxVal[0])
        maxVal = parseInt(mxVal[1])
        const minMsg = `Min value is ${minVal}`
        const maxMsg = `Max value is ${maxVal}`
        res = [(val: any) => ((!!val && val >= minVal) || _msg ? _msg : minMsg), (val: any) => ((!!val && val <= maxVal) || _msg ? _msg : maxMsg)]
      }
    }
    // required
    else {
      msg = `Field is required!`
      msg = _msg ? _msg : msg
      res = [(val: any) => (!!val && val !== '' && val !== ' ' && val !== '  ' && val !== '   ') || msg]
    }

    if (_raw) return res[0]
    return res
  },
  showSuccess(message: string) {
  Notify.create({
    type: 'positive',
    message
  })
},

showError(message: string) {
  Notify.create({
    type: 'negative',
    message
  })
},

  approvalIsRunning(approval_status: any) {
    if (!approval_status || approval_status === 'Pending') return false
    return true
  },
  hasAdditionalPermision(type: string) {
    const Auth = authStore()
    const user = Auth.getUser()

    if (user && user.additional_permissions !== undefined && user.additional_permissions !== null) {
      const permissionsArray = user.additional_permissions.split(',')
      return permissionsArray.includes(type)
    }
    return false
  }
}

export interface Dialog {
  [props: string]: any
  show: boolean
  title?: string
  width?: string
  maximize?: boolean
  persistent?: boolean
}

export interface DataFile {
  id: number | null
  name: string | null
  description: string | null
  filename: string | null
  path: string | null
  cdn_path: string | null
  module: string | null
  reference_id: string | number | null
  reference_code: string | null
  file: any
}
