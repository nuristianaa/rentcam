const Meta = {
  page: 'LayoutDashboard',
  schema: 'auth',
  name: 'me',
  module: 'auth/users/me',
  permission: [
    {
      name: 'auth/users',
      detail: {
        browse: true,
        create: true,
        read: true,
        update: true,
        delete: true,
        restore: true
      }
    }
  ],
  menus: [
    {
      _id: '63f81612c4df77e9700d0995',
      group: 'crm',
      name: 'Dashboard',
      slug: 'dashboard',
      path: '/',
      icon: 'home'
    },
    {
      _id: '63f81612c4df77e9700d0996',
      group: 'crm',
      name: 'Master Data',
      slug: 'master-data',
      path: '/master-data',
      icon: 'folder',
      children: [
        {
          _id: '63f81612c4df77e9700d0997',
          group: 'crm',
          name: 'Companies',
          slug: 'companies',
          path: '/companies',
          icon: 'business'
        },
        {
          _id: '63f81612c4df77e9700d0998',
          group: 'crm',
          name: 'Buyers',
          slug: 'buyers',
          path: '/buyers',
          icon: 'emoji_emotions'
        },
        {
          _id: '644de0676281bc91410a402e',
          name: 'Vendors',
          slug: 'vendors',
          icon: 'add_business',
          group: 'crm',
          path: '/vendors',
          created_by: 'superuser'
        },
        {
          _id: '63f81612c4df77e9700d0999',
          group: 'crm',
          name: 'Surveyors',
          slug: 'surveyors',
          path: '/surveyors',
          icon: 'policy'
        },
        {
          _id: '63f81612c4df77e9700d099a',
          group: 'crm',
          name: 'Agents',
          slug: 'agents',
          path: '/agents',
          icon: 'where_to_vote'
        }
      ]
    },
    {
      _id: '63f81612c4df77e9700d09a3',
      group: 'crm',
      name: 'Index',
      slug: 'index',
      path: '/index',
      icon: 'trending_up'
    },
    {
      _id: '644de1062ebbc29b820adb7f',
      name: 'Procurement',
      slug: 'procurement',
      icon: 'request_quote',
      group: 'crm',
      path: '/procurement',
      created_by: 'superuser',
      children: [
        {
          _id: '644de194122cd3303c0a05e6',
          name: 'Purchase Order',
          slug: 'procurement/po',
          icon: 'list_alt',
          group: 'crm',
          path: '/procurement/po',
          created_by: 'superuser',
          updated_by: 'superuser'
        },
        {
          _id: '644de1cfe1844fd7ac02e2f5',
          name: 'Good Receipt',
          slug: 'procurement/gr',
          icon: 'receipt_long',
          group: 'crm',
          path: '/procurement/gr',
          created_by: 'superuser',
          updated_by: 'superuser'
        }
      ]
    }
  ]
}

export default Meta
