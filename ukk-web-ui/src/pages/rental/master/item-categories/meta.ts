export interface DataModel {
  id: number | null
  name: string | null
  description: string | null
  is_active: boolean
}

export const Meta = {
  app: 'rental',
  schema: 'rental',
  name: 'item_categories',
  title: 'Kategori Alat',
  module: 'master/item-categories',
  route_ui: 'master/item-categories',
  dialogMode: true,

  permission: {
    browse: true,
    create: true,
    read: true,
    update: true,
    delete: true,
    restore: true
  },

  model: <DataModel>{
    id: null,
    name: null,
    description: null,
    is_active: true,
  },

  table: (_H: any, _C: any, L: any) => {
    const meta = { app: 'rental', schema: 'rental', name: 'item_categories' }
    return [
      { align: 'left', name: 'action',      field: 'id',          label: '#',                           style: 'width: 20px' },
      { align: 'left', name: 'name',        field: 'name',        label: L.module(meta, 'name') },
      { align: 'left', name: 'description', field: 'description', label: L.module(meta, 'description') },
      { align: 'left', formatter: 'boolean', name: 'is_active', field: 'is_active', label: L.module(meta, 'is_active') },
      { align: 'left', formatter: 'date', name: 'updated_at', field: 'updated_at', label: L.module(meta, 'updated_at'), is_date: true },
    ]
  }
}