const Meta = {
  schema: 'master',
  name: 'Config',
  title: 'Config',
  page: {
    index: 'indexConfig',
    form: 'formConfig',
    view: 'viewConfig'
  },
  module: 'master/drivers',
  route_ui: 'master/drivers',
  permission: {
    browse: true,
    create: true,
    read: true,
    update: true,
    delete: true,
    restore: true
  },
  model: {
    login: true,
    url: 'http://localhost:8190/',
    rental: 'http://localhost:8191/',
  }
}

export default Meta
