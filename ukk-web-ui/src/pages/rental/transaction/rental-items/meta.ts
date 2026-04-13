export interface DataModel {
  id: string | null
  rental_id: string | null
  rental_code?: string | null
  item_id: number | null
  item_name?: string | null
  item_code?: string | null
  quantity: number | null
  price_per_day: number | null
  deposit_amount: number | null
  subtotal: number | null
}

export const Meta = {
  app: 'rental',
  schema: 'rental',
  name: 'rental_items',
  title: 'Item Rental',
  module: 'transaction/rental-items',
  route_ui: 'rental/transaction/rental-items',
  dialogMode: false,

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
    rental_id: null,
    rental_code: null,
    item_id: null,
    item_name: null,
    item_code: null,
    quantity: 1,
    price_per_day: 0,
    deposit_amount: 0,
    subtotal: 0,
  },

  table: (_H: any, _C: any, L: any) => {
    const meta = { app: 'rental', schema: 'rental', name: 'rental_items' }
    return [
      { align: 'left',  name: 'action',       field: 'id',           label: '#',                            style: 'width: 20px' },
      { align: 'left',  name: 'rental_code',  field: 'rental_code',  label: L.module(meta, 'rental_code') },
      { align: 'left',  name: 'item_code',    field: 'item_code',    label: L.module(meta, 'item_code') },
      { align: 'left',  name: 'item_name',    field: 'item_name',    label: L.module(meta, 'item_name') },
      { align: 'right', formatter: 'number',   name: 'quantity',     field: 'quantity',      label: L.module(meta, 'quantity') },
      { align: 'right', formatter: 'currency', name: 'price_per_day',field: 'price_per_day', label: L.module(meta, 'price_per_day') },
      { align: 'right', formatter: 'currency', name: 'deposit_amount',field: 'deposit_amount',label: L.module(meta, 'deposit_amount') },
      { align: 'right', formatter: 'currency', name: 'subtotal',     field: 'subtotal',      label: L.module(meta, 'subtotal') },
      { align: 'left',  formatter: 'date', name: 'created_at',       field: 'created_at',    label: L.module(meta, 'created_at'), is_date: true },
    ]
  }
}