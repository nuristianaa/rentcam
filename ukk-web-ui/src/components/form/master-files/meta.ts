export interface DataModel {
  id_: number | null
  id: number | null
  app: string | null
  name: string | null
  description: string | null
  filename?: string | null
  filetype?: string | null
  path?: string | null
  public_path?: string | null
  module: string | null
  reference_id: string | number | null
  reference_code: string | null
  is_public: boolean | null
  storage_id?: string | null
  url?: string | null
  file: any
  identifier?: string | null
}

export const Meta = {
  schema: 'auth',
  name: 'MasterFiles',
  title: 'Master Files',
  module: 'auth/master-files',
  route_ui: 'auth/master-files',
  permission: {
    browse: true,
    create: true,
    read: true,
    update: true,
    delete: true,
    restore: true
  },
  model: {
    id_: null,
    id: null,
    app: null,
    name: null,
    description: null,
    filename: null,
    filetype: null,
    path: null,
    public_path: null,
    module: null,
    reference_id: null,
    reference_code: null,
    is_public: false,
    url: null,
    storage_id: null,
    file: null
  },
  columns: <any>[
    { name: 'action', label: '#', field: 'id_', align: 'left', style: 'width: 50px' },
    { name: 'file', label: 'File', field: 'file', align: 'left' },
    { name: 'name', label: 'Name', field: 'name', align: 'left' },
    { name: 'description', label: 'Description', field: 'description', align: 'left' },
    { name: 'filename', label: 'Original Name', field: 'filename', align: 'left' }
  ]
}

export default Meta
