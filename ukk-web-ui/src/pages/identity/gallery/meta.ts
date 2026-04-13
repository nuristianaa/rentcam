export interface DataModel {
  id: number | null
  app: string | null
  name: string | null
  description: string | null
  filename: string | null
  filetype: string | null
  path: string | null
  public_path: string | null
  base_url: string | null
  module: string | null
  reference_id: string | number | null
  reference_code: string | null
  is_public: boolean | null
  storage_id: string | null
  file: any
}

export const Meta = {
  app: 'identity',
  schema: 'auth',
  name: 'master_files',
  title: 'Gallery',
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
    id: null,
    app: 'identity',
    name: null,
    description: null,
    filename: null,
    filetype: null,
    path: null,
    public_path: null,
    base_url: null,
    module: 'gallery',
    reference_id: null,
    reference_code: null,
    is_public: true,
    storage_id: null,
    file: null
  },
  table: (H: any, C: any, L: any) => {
    const meta = { app: 'identity', schema: 'auth', name: 'master_files' }
    return [
      { name: 'action', label: '#', field: 'id', align: 'left', style: 'width: 20px' },
      { name: 'name', label: L.module(meta, 'name'), field: 'name', align: 'left' },
      { name: 'filetype', label: L.module(meta, 'filetype'), field: 'filetype', align: 'left' },
      // { name: 'filename', label: L.module(meta, 'filename'), field: 'filename', align: 'left' },
      { name: 'path', label: L.module(meta, 'path'), field: 'path', align: 'left' },
      // { name: 'module', label: L.module(meta, 'module'), field: 'module', align: 'left' },
      // {
      //   name: 'reference_code',
      //   label: L.module(meta, 'reference_code'),
      //   field: 'reference_code',
      //   align: 'left',
      // },
      // {
      //   name: 'is_public',
      //   formatter: 'boolean',
      //   label: L.module(meta, 'is_public'),
      //   field: 'is_public',
      //   align: 'left',
      // },
      {
        name: 'description',
        label: L.module(meta, 'description'),
        field: 'description',
        align: 'left'
      }
    ]
  }
}

export default Meta
