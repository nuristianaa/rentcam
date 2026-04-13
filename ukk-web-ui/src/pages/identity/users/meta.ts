export interface DataModel {
  id: number | null
  username: string | null
  email: string | null
  current_password: string | null
  password: string | null
  name: string | null
  phone: string | null
  title: string | null

  role_ids: number[]
  role_code: string | null
  companies?: string | Array<string> | null
  vendors?: string | Array<string> | null
  additional_permissions?: string | Array<string> | null
  user_type: string | null



  location: string | null
  country_code: string | null
  birthday: string | null
  profile_picture: string | null
  department_code: string | null
  is_suspend: boolean
  is_active: boolean
}

export interface Company {
  code: string
  name: string
  [key: string]: any
}

export const Meta = {
  // app: 'identity',
  schema: 'auth',
  name: 'Users',
  title: 'Users',
  module: 'auth/users',
  route_ui: 'auth/users',
  dialogMode: true,
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
    username: null,
    email: null,
    current_password: null,
    password: null,
    name: null,
    phone: null,
    title: null,

    role_ids: [],
    role_code: null,
    additional_permissions: null,



    location: null,
    country_code: null,
    birthday: null,
    profile_picture: null,
    is_active: true
  },
  table: (_H: any, _C: any, L: any) => {
    const meta = { app: 'identity', schema: 'auth', name: 'users' }
    return [
      { align: 'left', name: 'action', label: '#', field: 'id', style: 'width: 20px' },
      { align: 'left', name: 'name', label: L.module(meta, 'name'), field: 'name' },
      { align: 'left', name: 'username', label: L.module(meta, 'username'), field: 'username' },
      { align: 'left', name: 'email', label: L.module(meta, 'email'), field: 'email' },
      { align: 'left', name: 'phone', label: L.module(meta, 'phone'), field: 'phone' },
      { align: 'left', name: 'title', label: L.module(meta, 'title'), field: 'title' },
      { align: 'left', formatter: 'boolean', name: 'is_active', field: 'is_active', label: L.module(meta, 'is_active') },
      { align: 'left', name: 'role_names', label: L.module(meta, 'role_names'), field: 'role_names' },

      { align: 'left', name: 'additional_permissions', label: L.module(meta, 'additional_permissions'), field: 'additional_permissions' },
      { align: 'left', formatter: 'date', name: 'birthday', label: L.module(meta, 'birthday'), field: 'birthday', is_date: true },
      { align: 'left', formatter: 'date', name: 'updated_at', label: L.module(meta, 'updated_at'), field: 'updated_at', is_date: true }
    ]
  }
}
