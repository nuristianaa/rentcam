export interface DataModel {
  id: string | null
  rental_id: string | null
  type: string | null
  actual_at: string | null
  condition: string | null
  condition_notes: string | null
  officer_name: string | null
}

export const Meta = {
  app: 'rental',
  schema: 'rental',
  name: 'rental-checkpoints',
  title: 'Checkpoints Rental',
  module: 'transaction/rental-checkpoints',
  route_ui: 'rental/transaction/rental-checkpoints',
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
    rental_id: null,
    type: null,
    actual_at: null,
    condition: null,
    condition_notes: null,
    officer_name: null,
  },

  table: (_H: any, _C: any, L: any) => {
    const meta = { app: 'rental', schema: 'rental', name: 'rental-checkpoints' }
    return [
      { align: 'left',  name: 'action',       field: 'id',            label: '#',                               style: 'width: 20px' },
      { align: 'left',  name: 'type',         field: 'type',          label: L.module(meta, 'type') },
      { align: 'left',  name: 'condition',    field: 'condition',     label: L.module(meta, 'condition') },
      { align: 'left',  name: 'officer_name', field: 'officer_name',  label: L.module(meta, 'officer_name') },
      { align: 'left',  formatter: 'date', name: 'actual_at', field: 'actual_at', label: L.module(meta, 'actual_at'), is_date: true },
    ]
  }
}
