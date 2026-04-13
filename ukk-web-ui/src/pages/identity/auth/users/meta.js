const Meta = {
  name: 'Users',
  page: {
    index: 'indexsUsers',
    form: 'formsUsers',
    view: 'viewsUsers',
  },
  module: 'auth/users',
  route_ui: '/users',
  formModal: false,
  show_detail: true,
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
    username: null,
    email: null,
    password: null,
    name: null,
    phone: null,
    birthday: null,
    profile_picture: null,
    role_id: null,
    menus: null,
  },
  table: (H, C, L) => {
    // const meta = { schema: 'sales', name: 'user_notifications' }
    return [
      { name: 'action', label: '#', field: 'id', align: 'left', style: 'width: 20px' },
      { name: 'name', label: 'Name', field: 'name', align: 'left' },
      { name: 'username', label: 'Username', field: 'username', align: 'left' },
      { name: 'email', label: 'Email', field: 'email', align: 'left' },
      { name: 'phone', label: 'Phone', field: 'phone', align: 'left' },
      { name: 'updated_at', label: 'Last Log', field: 'updated_at', align: 'left' },
    ]
  },
}

export default Meta
