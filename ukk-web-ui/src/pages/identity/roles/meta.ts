import { name } from '@vue/eslint-config-prettier/skip-formatting'

export interface DataModel {
  id: number | null
  app: string | null
  name: string | null
  slug: string | null
  permissions: Array<any> | null
  active: boolean | null
}

export const Meta = {
  app: 'identity',
  page: {
    index: 'IndexRoles',
    form: 'FormRoles',
    detail: 'DetailRoles'
  },
  schema: 'auth',
  name: 'Roles',
  title: 'Roles',
  module: 'auth/roles',
  route_ui: 'auth/roles',
  dialogMode: true,
  permission: {
    browse: true,
    create: true,
    read: true,
    update: true,
    delete: true,
    restore: true
  },
  model: {
    id: null,
    app: null,
    name: null,
    slug: null,
    permissions: [],
    active: true
  },
  table: (H: any, C: any, L: any) => {
    const meta = { app: 'identity', schema: 'auth', name: 'roles' }
    return [
      { name: 'action', label: '#', field: '_id', align: 'center', style: 'width: 20px' },
      // { name: 'app', label: L.module(meta, 'app'), field: 'app', align: 'center' },
      { name: 'name', label: L.module(meta, 'name'), field: 'name', align: 'left' },
    ]
  },

  tablePermissions: (H: any, C: any, L: any) => {
    const meta = { app: 'identity', schema: 'auth', name: 'Roles' }
    return [
      {
        align: 'left',
        formatter: null,
        name: 'app',
        field: 'app',
        label: L.module(meta, 'app'),
        filterHide: true
      },
      {
        align: 'left',
        formatter: null,
        name: 'permission',
        field: 'permission',
        label: L.module(meta, 'permission')
      },
      {
        align: 'left',
        formatter: null,
        name: 'no',
        field: 'no',
        label: L.module(meta, 'no')
      }
    ]
  },

  tableExport: (H: any, C: any, L: any) => {
    const meta = { app: 'identity', schema: 'auth', name: 'Roles' }
    return [
      {
        align: 'left',
        formatter: null,
        name: 'name',
        field: 'name',
        label: L.module(meta, 'name'),
        filterHide: true
      },
      {
        align: 'left',
        formatter: null,
        name: 'permissions',
        field: 'permissions',
        label: L.module(meta, 'permissions')
      },
      {
        align: 'left',
        formatter: 'boolean',
        name: 'browse',
        field: 'browse',
        label: L.module(meta, 'browse')
      },
      {
        align: 'left',
        formatter: 'boolean',
        name: 'create',
        field: 'create',
        label: L.module(meta, 'create')
      },
      {
        align: 'left',
        formatter: 'boolean',
        name: 'read',
        field: 'read',
        label: L.module(meta, 'read')
      },
      {
        align: 'left',
        formatter: 'boolean',
        name: 'update',
        field: 'update',
        label: L.module(meta, 'update')
      },
      {
        align: 'left',
        formatter: 'boolean',
        name: 'delete',
        field: 'delete',
        label: L.module(meta, 'delete')
      },
      {
        align: 'left',
        formatter: 'boolean',
        name: 'restore',
        field: 'restore',
        label: L.module(meta, 'restore')
      }
    ]
  },

  tableExportSample: [
    {
      name: 'GEAGLE-GA-MANAGER',
      permissions: '1-20, 25',
      create: true,
      update: true,
      browse: true,
      read: true,
      delete: true,
      restore: true
    }
  ]
}
