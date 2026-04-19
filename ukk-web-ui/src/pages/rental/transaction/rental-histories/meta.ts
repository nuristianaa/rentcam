export interface CheckpointModel {
  id: string
  rental_id: string
  type: 'checkout' | 'checkin'
  actual_at: string
  condition: string | null
  condition_notes: string | null
  checklist: any[] | null
  officer_id: number | null
  officer_name: string | null
  customer_signature: string | null
  notes: string | null
  created_at: string
}

export interface HistoryModel {
  id: string
  rental_id: string
  event: string
  old_status: string | null
  new_status: string | null
  actor: string | null
  actor_id: number | null
  notes: string | null
  data: any
  created_at: string
}

export interface InvoiceModel {
  id: string
  invoice_code: string
  type: string | null
  rental_code: string | null
  grand_total: number | null
  payment_method: string | null
  paid_at: string | null
  verified_at: string | null
  pdf_status: string | null
  pdf_url: string | null
  created_at: string
}

export interface DataModel {
  id: string | null
  rental_code: string | null
  customer_id: number | null
  customer_name?: string | null
  petugas_id: number | null
  petugas_name?: string | null
  start_date: string | null
  end_date: string | null
  duration_days: number | null
  subtotal: number | null
  deposit_total: number | null
  grand_total: number | null
  payment_method: string | null
  status: string | null
  notes: string | null
  items?: any[]
  histories?: HistoryModel[]
  checkpoints?: CheckpointModel[]
  invoices?: InvoiceModel[]
}

export const Meta = {
  app: 'rental',
  schema: 'rental',
  name: 'rental-histories',
  title: 'Rental History',
  module: 'transaction/rental-histories',
  apiModule: 'transaction/rentals',
  route_ui: 'transaction/rental-histories',
  dialogMode: false,

  permission: {
    browse: true,
    create: false,
    read: true,
    update: false,
    delete: false,
    restore: false
  },

  model: <DataModel>{
    id: null,
    rental_code: null,
    customer_id: null,
    customer_name: null,
    petugas_id: null,
    petugas_name: null,
    start_date: null,
    end_date: null,
    duration_days: null,
    subtotal: 0,
    deposit_total: 0,
    grand_total: 0,
    payment_method: null,
    status: null,
    notes: null,
    items: [],
    histories: [],
    checkpoints: [],
    invoices: [],
  },

  paymentMethodOptions: [
    { label: 'Transfer', value: 'transfer' },
    { label: 'COD',      value: 'cod' },
  ],

  statusOptions: [
    { label: 'Waiting for Payment',       value: 'menunggu_bayar' },
    { label: 'Waiting for Verification',  value: 'menunggu_verif' },
    { label: 'Processing',             value: 'diproses' },
    { label: 'Active',                value: 'aktif' },
    { label: 'Completed',              value: 'selesai' },
    { label: 'Cancelled',           value: 'dibatalkan' },
  ],

  statusColor: {
    menunggu_bayar: 'orange',
    menunggu_verif: 'blue',
    diproses:       'purple',
    aktif:          'green',
    selesai:        'teal',
    dibatalkan:     'red',
  } as Record<string, string>,

  statusFlowOptions: <Record<string, { label: string; value: string }[]>>{
    menunggu_bayar: [
      { label: 'Waiting for Verification', value: 'menunggu_verif' },
      { label: 'Cancelled',          value: 'dibatalkan' },
    ],
    menunggu_verif: [
      { label: 'Processing',       value: 'diproses' },
      { label: 'Waiting for Payment', value: 'menunggu_bayar' },
      { label: 'Cancelled',     value: 'dibatalkan' },
    ],
    diproses: [
      { label: 'Cancelled', value: 'dibatalkan' },
    ],
    aktif:      [],
    selesai:    [],
    dibatalkan: [],
  },

  table: (_H: any, _C: any, L: any) => {
    const meta = { app: 'rental', schema: 'rental', name: 'rentals' }
    return [
      { align: 'left',  name: 'action',         field: 'id',             label: '#',                              style: 'width: 20px' },
      { align: 'left',  name: 'rental_code',    field: 'rental_code',    label: L.module(meta, 'rental_code') },
      { align: 'left',  name: 'customer_name',  field: 'customer_name',  label: L.module(meta, 'customer_name') },
      { align: 'left',  name: 'start_date',     field: 'start_date',     label: L.module(meta, 'start_date') },
      { align: 'left',  name: 'end_date',       field: 'end_date',       label: L.module(meta, 'end_date') },
      { align: 'right', name: 'duration_days',  field: 'duration_days',  label: L.module(meta, 'duration_days') },
      { align: 'right', formatter: 'currency', name: 'grand_total',      field: 'grand_total',   label: L.module(meta, 'grand_total') },
      { align: 'left',  name: 'payment_method', field: 'payment_method', label: L.module(meta, 'payment_method') },
      { align: 'left',  name: 'status',         field: 'status',         label: L.module(meta, 'status') },
      { align: 'left',  formatter: 'date', name: 'created_at',           field: 'created_at',    label: L.module(meta, 'created_at'), is_date: true },
    ]
  }
}
