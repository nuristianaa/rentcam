export const Meta = {
  app: 'identity',
  schema: 'auth',
  name: 'Notifications',
  title: 'Notifications',
  module: 'me/notifications',
  route_ui: 'notifications',
  permission: {
    browse: true,
    create: false,
    read: true,
    update: false,
    delete: false,
    restore: false
  },
  model: {
    title: null,
    description: null,
    type: null,
    path: null,
    icon: null,
    color: null
  },
  tabs: [
    { name: 'notifications', label: 'unread', icon: 'mark_chat_unread', api: 'me/notifications?where=is_read:false' },
    { name: 'all-notifications', label: 'all', icon: 'mark_chat_read', api: 'me/notifications?' }
  ],
  tab: 'notifications',
  table: (H: any, C: any, L: any) => {
    const meta = { schema: 'auth', name: 'user_notifications' }
    return [
      { name: 'action', label: '#', field: 'id', align: 'center', style: 'width: 20px' },
      { name: 'title', label: L.module(meta, 'title'), field: 'title', align: 'left' },
      { name: 'description', label: L.module(meta, 'description'), field: 'description', align: 'left' },
      { name: 'type', label: L.module(meta, 'type'), field: 'type', align: 'center' },
      { name: 'path', label: L.module(meta, 'path'), field: 'path', align: 'left', colHide: true },
      { formatter: 'datatime', name: 'created_at', label: L.module(meta, 'created at'), field: 'created_at', align: 'left', datetime: true }
    ]
  }
}
