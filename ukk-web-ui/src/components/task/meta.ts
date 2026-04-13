export interface DataModel {
  id: string | null
  app: string | null
  ref_module: string | null
  ref_id: string | null
  title: string | null
  description: string | null
  activity_type: string | null
  status: string | null
  priority: string | null
  start_date: string | null
  due_date: string | null
  tags: [] | null
  user_id: list | null
  notes: TaskNote[]
  approval_status: string | null
  approval_meta: string | null
}

export interface TaskNote {
  title: string | null
  content: string | null
  type: string | null
}

export const Meta = {
  app: 'crm',
  schema: 'transaction',
  name: 'tasks',
  title: 'Tasks',
  module: 'transaction/tasks',
  module_comment: 'transaction/notes',
  route_ui: 'transaction/tasks',
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
    description: null,
    activity_type: null,
    status: "TODO",
    priority: "MEDIUM",
    start_date: null,
    due_date: null,
    tags: [],
    user_id: null,
    approval_status: 'Pending',
    approval_meta: null
  },
  notes_model: {
    id: null,
    ref_app: null,
    ref_module: null,
    ref_id: null,
    title: null,
    content: null,
    type: 'comments'
  },
  table: (H: any, C: any, L: any) => {
    const meta = { app: 'crm', schema: 'transaction', name: 'tasks' }
    return [
      { name: 'action', label: '#', field: 'id', align: 'center', style: 'width: 20px' },
      { name: 'title', label: L.module(meta, 'title'), field: 'title', align: 'center' },
      { name: 'activity_type', label: L.module(meta, 'activity_type'), field: 'activity_type', align: 'center' },
      { name: 'status', label: L.module(meta, 'status'), field: 'status', align: 'center' },
      { name: 'priority', label: L.module(meta, 'priority'), field: 'priority', align: 'center' },
      { name: 'due_date', label: L.module(meta, 'due_date'), field: 'due_date', align: 'center', formatter: 'date' },
      { name: 'updated_at', label: 'Last Log', field: 'updated_at', align: 'center'}

    ]
  },
}
