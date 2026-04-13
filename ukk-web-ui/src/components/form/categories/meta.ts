export interface DataModel {
  id: number | null
  group: string | null
  code: string | null
  val_str: string | null
  val_int: number | null
  val_float: number | null
  timemillis: number | null
}

export const Meta = {
  app: 'crm',
  schema: 'master',
  name: 'categories',
  classname: 'Category',
  title: 'Categories',
  module: 'master/categories',
  permission: { browse: true, create: true, read: true, update: true, delete: true, restore: true },
  model: <DataModel>{
    id: null,
    group: null,
    code: null,
    val_str: null,
    val_int: null,
    val_float: null,
    timemillis: null
  },
  columns: <any>[
    { align: 'left', formatter: null, name: 'action', field: 'id', label: '#', style: 'width: 20px' },
    { align: 'left', formatter: null, name: 'code', field: 'code', label: 'Code' },
    { align: 'left', formatter: null, name: 'val_str', field: 'val_str', label: 'Remark' }
  ]
}
