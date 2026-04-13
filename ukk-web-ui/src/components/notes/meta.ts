export interface DataModel {
  id: string | null
  app: string | null
  ref_module: string | null
  ref_id: string | null
  title: string | null
  content: string | null
  type: string | null
}

export const Meta = {
  app: 'crm',
  schema: 'transaction',
  name: 'notes',
  title: 'Notes',
  module: 'transaction/notes',
  route_ui: 'transaction/notes',
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
    ref_module: null,
    ref_id: null,
    title: null,
    content: null,
    type: null
  },
  table: (H: any, C: any, L: any) => {
    const meta = { app: 'crm', schema: 'transaction', name: 'notes' }
    return [
      { name: 'action', label: '#', field: 'id', align: 'center', style: 'width: 80px' },
      { name: 'type', label: L.module(meta, 'type'), field: 'type', align: 'center' },
      { name: 'title', label: L.module(meta, 'title'), field: 'title', align: 'left' },
      { name: 'content', label: L.module(meta, 'content'), field: 'content', align: 'left', style: 'width: 40%  ' },
      { name: 'updated_at', label: 'Last Log', field: 'updated_at', align: 'center'}
    ]
  },
}
