export interface DataModel {
  id: number | null
  category_id: number | null
  code: string | null
  name: string | null
  brand: string | null
  description: string | null
  condition: string | null
  stock_total: number | null
  stock_available: number | null
  price_per_day: number | null
  deposit_amount: number | null
  is_active: boolean | null
  images: any[] | null
  created_by: string | null
  updated_by: string | null
  deleted_by: string | null
  created_at: string | null
  updated_at: string | null
  deleted_at: string | null
}

export const Meta = {
  app: 'rental',
  schema: 'rental',
  name: 'items',
  title: 'Items',
  module: 'user/items',
  apiModule: 'master/items',
  route_ui: 'user/items',
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
    category_id: null,
    code: null,
    name: null,
    brand: null,
    description: null,
    condition: null,
    stock_total: 0,
    stock_available: 0,
    price_per_day: 0,
    deposit_amount: 0,
    is_active: true,
    images: null,
    created_by: null,
    updated_by: null,
    deleted_by: null,
    created_at: null,
    updated_at: null,
    deleted_at: null,
  },

  table: (_H: any, _C: any, L: any) => {
    const meta = { app: 'rental', schema: 'rental', name: 'items' }
    return [
      { align: 'left', name: 'action', field: 'id', label: '#', style: 'width: 20px' },
      { align: 'left', name: 'code', field: 'code', label: L.module(meta, 'code') },
      { align: 'left', name: 'name', field: 'name', label: L.module(meta, 'name') },
      { align: 'left', name: 'brand', field: 'brand', label: L.module(meta, 'brand') },
      { align: 'left', name: 'category_id', field: 'category_id', label: L.module(meta, 'category_id') },
      { align: 'left', name: 'condition', field: 'condition', label: L.module(meta, 'condition') },
      { align: 'right', formatter: 'integer', name: 'stock_total', field: 'stock_total', label: L.module(meta, 'stock_total') },
      { align: 'right', formatter: 'integer', name: 'stock_available', field: 'stock_available', label: L.module(meta, 'stock_available') },
      { align: 'right', formatter: 'float', name: 'price_per_day', field: 'price_per_day', label: L.module(meta, 'price_per_day') },
      { align: 'right', formatter: 'float', name: 'deposit_amount', field: 'deposit_amount', label: L.module(meta, 'deposit_amount') },
      { align: 'left', formatter: 'boolean', name: 'is_active', field: 'is_active', label: L.module(meta, 'is_active') },
      { align: 'left', formatter: 'date', name: 'updated_at', field: 'updated_at', label: L.module(meta, 'updated_at'), is_date: true },
    ]
  }
}