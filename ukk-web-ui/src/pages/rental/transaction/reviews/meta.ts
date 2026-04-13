export interface DataModel {
  id: string | null
  rental_id: string | null
  rental_code?: string | null
  item_id: number | null
  item_name?: string | null
  customer_id: number | null
  customer_name?: string | null
  rating: number | null
  comment: string | null
  is_visible: boolean
}

export const Meta = {
  app: 'rental',
  schema: 'rental',
  name: 'reviews',
  title: 'Ulasan',
  module: 'transaction/reviews',
  route_ui: 'transaction/reviews',
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
    customer_id: null,
    customer_name: null,
    rating: null,
    comment: null,
    is_visible: true,
  },

  ratingOptions: [
    { label: '⭐ 1 - Sangat Buruk',  value: 1 },
    { label: '⭐ 2 - Buruk',          value: 2 },
    { label: '⭐ 3 - Cukup',          value: 3 },
    { label: '⭐ 4 - Baik',           value: 4 },
    { label: '⭐ 5 - Sangat Baik',    value: 5 },
  ],

  table: (_H: any, _C: any, L: any) => {
    const meta = { app: 'rental', schema: 'rental', name: 'reviews' }
    return [
      { align: 'left',  name: 'action',        field: 'id',            label: '#',                            style: 'width: 20px' },
      { align: 'left',  name: 'rental_code',   field: 'rental_code',   label: L.module(meta, 'rental_code') },
      { align: 'left',  name: 'item_name',     field: 'item_name',     label: L.module(meta, 'item_id') },
      { align: 'left',  name: 'customer_name', field: 'customer_name', label: L.module(meta, 'customer_id') },
      { align: 'center', formatter: 'rating',  name: 'rating',         field: 'rating',       label: L.module(meta, 'rating') },
      { align: 'left',  name: 'comment',       field: 'comment',       label: L.module(meta, 'comment') },
      { align: 'left',  formatter: 'boolean',  name: 'is_visible',     field: 'is_visible',   label: L.module(meta, 'is_visible') },
      { align: 'left',  formatter: 'date',     name: 'created_at',     field: 'created_at',   label: L.module(meta, 'created_at'), is_date: true },
    ]
  }
}