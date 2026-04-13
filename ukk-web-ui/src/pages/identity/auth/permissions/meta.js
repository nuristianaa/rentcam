const Meta = {
  name: 'Permissions',
  page: {
    index: 'indexsUsers',
    form: 'formsUsers',
    view: 'viewsUsers',
  },
  module: 'auth/permissions',
  route_ui: '/permissions',
  formModal: false,
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
    name: null,
    slug: null,
  },

  table: (H, C, L) => {
    // const meta = { schema: 'sales', name: 'user_notifications' }
    return [
      { name: 'action', label: '#', field: 'id', align: 'left', style: 'width: 20px' },
      { name: 'name', label: 'Name', field: 'name', align: 'left' },
      { name: 'slug', label: 'Slug', field: 'slug', align: 'left' },
      { name: 'updated_at', label: 'Last Log', field: 'updated_at', align: 'left' },
    ]
  },
}

export default Meta
