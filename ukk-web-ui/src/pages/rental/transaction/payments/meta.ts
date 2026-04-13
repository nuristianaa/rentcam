export interface DataModel {
  id: string | null
  rental_id: string | null
  rental_code?: string | null
  verified_by: number | null
  verified_by_name?: string | null
  amount: number | null
  type: string | null             // pembayaran | denda | refund_deposit
  status: string | null           // menunggu | terverifikasi | ditolak
  bank_name: string | null
  account_number: string | null
  notes: string | null
  paid_at: string | null
  verified_at: string | null
}

export const Meta = {
  app: 'rental',
  schema: 'rental',
  name: 'payments',
  title: 'Pembayaran',
  module: 'transaction/payments',
  route_ui: 'rental/transaction/payments',
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
    verified_by: null,
    verified_by_name: null,
    amount: 0,
    type: null,
    status: null,
    bank_name: null,
    account_number: null,
    notes: null,
    paid_at: null,
    verified_at: null,
  },

  typeOptions: [
    { label: 'Pembayaran',     value: 'pembayaran' },
    { label: 'Denda',          value: 'denda' },
    { label: 'Refund Deposit', value: 'refund_deposit' },
  ],

  statusOptions: [
    { label: 'Menunggu',       value: 'menunggu' },
    { label: 'Terverifikasi',  value: 'terverifikasi' },
    { label: 'Ditolak',        value: 'ditolak' },
  ],

  table: (_H: any, _C: any, L: any) => {
    const meta = { app: 'rental', schema: 'rental', name: 'payments' }
    return [
      { align: 'left',  name: 'action',          field: 'id',             label: '#',                               style: 'width: 20px' },
      { align: 'left',  name: 'rental_code',     field: 'rental_code',    label: L.module(meta, 'rental_code') },
      { align: 'left',  name: 'type',            field: 'type',           label: L.module(meta, 'type') },
      { align: 'right', formatter: 'currency', name: 'amount',            field: 'amount',         label: L.module(meta, 'amount') },
      { align: 'left',  name: 'status',          field: 'status',         label: L.module(meta, 'status') },
      { align: 'left',  name: 'bank_name',       field: 'bank_name',      label: L.module(meta, 'bank_name') },
      { align: 'left',  name: 'account_number',  field: 'account_number', label: L.module(meta, 'account_number') },
    ]
  }
}