import type { SignBlock } from 'src/components/sign-placements/meta'

export interface FilterItem {
  module: string
  columns: string[]
  show?: boolean
}

export interface TableFilter {
  app: string
  module: string
  columns: string[]
}

export interface DataModel {
  sign_placements: SignBlock[]
}

const Meta = {
  schema: '',
  name: 'LogActivity',
  title: 'Log Activity',
  module: 'audit-trails',
  route_ui: 'audit-trails',
  hide_trash: true,
  permission: {
    browse: true,
    create: false,
    read: true,
    update: false,
    delete: false,
    restore: false
  },
  model: {
    id: null,
    name: null,
    slug: null
  },
  custom_table: <any>null,
  table: () => {
    return [
      // { align: 'left', name: 'id', label: '#', field: 'id', style: 'width: 20px' },
      { align: 'left', name: 'name', label: 'Name', field: 'name' },
      { align: 'left', name: 'type', label: 'Type', field: 'type' },
      { align: 'left', name: 'schema', label: 'Schema', field: 'schema' },
      { align: 'left', name: 'module', label: 'Module', field: 'module' },
      { align: 'left', name: 'username', label: 'Changed By', field: 'username' },
      {
        align: 'left',
        formatter: 'datetime',
        name: 'created_at',
        label: 'Date',
        field: 'created_at',
        is_date: true,
        datetime: true,
        filterHide: true
      }
    ]
  }
}

export default Meta
