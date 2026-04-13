export interface DataModel {
  id: string | null
  invoice_code: string | null
  type: string | null
  rental_code: string | null
  grand_total: number | null
  payment_method: string | null
  paid_at: string | null
  verified_at: string | null
  pdf_status: string | null
  pdf_url: string | null
}

export const Meta = {
  app: 'rental',
  schema: 'rental',
  name: 'rental-invoices',
  title: 'Invoice Rental',
  module: 'transaction/rental-invoices',
  route_ui: 'rental/transaction/rental-invoices',
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
    invoice_code: null,
    type: null,
    rental_code: null,
    grand_total: 0,
    payment_method: null,
    paid_at: null,
    verified_at: null,
    pdf_status: null,
    pdf_url: null,
  },

  table: (_H: any, _C: any, L: any) => {
    const meta = { app: 'rental', schema: 'rental', name: 'rental-invoices' }
    return [
      { align: 'left',  name: 'action',          field: 'id',             label: '#',                               style: 'width: 20px' },
      { align: 'left',  name: 'invoice_code',    field: 'invoice_code',   label: L.module(meta, 'invoice_code') },
      { align: 'left',  name: 'rental_code',     field: 'rental_code',    label: L.module(meta, 'rental_code') },
      { align: 'left',  name: 'type',            field: 'type',           label: L.module(meta, 'type') },
      { align: 'right', formatter: 'currency', name: 'grand_total', field: 'grand_total', label: L.module(meta, 'grand_total') },
      { align: 'left',  name: 'payment_method',  field: 'payment_method', label: L.module(meta, 'payment_method') },
      { align: 'left',  name: 'pdf_status',      field: 'pdf_status',     label: L.module(meta, 'pdf_status') },
      { align: 'left',  formatter: 'date', name: 'created_at', field: 'created_at', label: L.module(meta, 'created_at'), is_date: true },
    ]
  }
}
