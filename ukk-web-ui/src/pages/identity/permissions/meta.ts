export interface DataModel {
  id: number | null
  app: string | null
  name: string | null
}

export const Meta = {
  app: 'identity',
  schema: 'auth',
  name: 'Permissions',
  title: 'Permissions',
  module: 'auth/permissions',
  route_ui: 'auth/permissions',
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
    name: null
  },
  table: (H: any, C: any, L: any) => {
    const meta = { app: 'identity', schema: 'auth', name: 'permissions' }
    return [
      { name: 'action', label: '#', field: '_id', align: 'left', style: 'width: 20px' },
      { name: 'app', label: L.module(meta, 'app'), field: 'app', align: 'left' },
      { name: 'name', label: L.module(meta, 'name'), field: 'name', align: 'left' }
      // { name: 'slug', label: L.module(meta, 'slug'), field: 'slug', align: 'left' }
    ]
  },
  tableExport: (H: any, C: any, L: any) => {
    const meta = { app: 'identity', schema: 'auth', name: 'Roles' }
    return [
      { name: 'app', label: L.module(meta, 'app'), field: 'app', align: 'left' },
      { name: 'name', label: L.module(meta, 'name'), field: 'name', align: 'left' }
    ]
  },
  tableExportSample: [
    {
      app: 'identity',
      name: 'master/warehouses'
    }
  ]
}
