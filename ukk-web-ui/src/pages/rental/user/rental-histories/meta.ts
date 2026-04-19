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
}

export const Meta = {
  app: 'rental',
  schema: 'rental',
  name: 'rental-histories',
  title: 'Booking History',
  module: 'user/rental-histories',
  apiModule: 'transaction/rentals',
  route_ui: 'user/rental-histories',
  dialogMode: false,

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
  } as DataModel,

  paymentMethodOptions: [
    { label: 'Transfer', value: 'transfer' },
    { label: 'COD', value: 'cod' }
  ],

  statusOptions: [
    { label: 'Waiting for Payment', value: 'menunggu_bayar' },
    { label: 'Waiting for Verification', value: 'menunggu_verif' },
    { label: 'Processing', value: 'diproses' },
    { label: 'Active', value: 'aktif' },
    { label: 'Completed', value: 'selesai' },
    { label: 'Cancelled', value: 'dibatalkan' }
  ],

  statusColor: {
    menunggu_bayar: 'blue-6',
    menunggu_verif: 'blue-7',
    diproses:       'blue-8',
    aktif:          'blue-9',
    selesai:        'blue-10',
    dibatalkan:     'blue-grey-7',
  } as Record<string, string>,
}