export interface DataModel {
  id: string|null
  date: string|null
  clock_in: string|null
  clock_out: string|null
  status: string|null
  location_type: string|null
  gps_coordinates: string|null
  project_id: string|null
  employee_id: string|null
  nik: string|null
  username: string|null
  remark: string|null
}


export const Meta = {
  app: 'hris',
  schema: 'transaction',
  name: 'attendance',
  classname: 'Attendance',
  title: 'Attendance',
  module: 'transaction/attendance',
  route_ui: 'transaction/attendance',
  permission: { browse: true, create: true, read: true, update: true, delete: true, restore: true },
  model: <DataModel>{
    id: null,
    date: null,
    clock_in: null,
    clock_out: null,
    status: null,
    location_type: 'OFFICE',
    gps_coordinates: [],
    project_id: null,
    employee_id: null,
    nik: null,
    username: null,
    remark: null,
  },

  table: (H: any, C: any, L: any) => {
    const meta = { app: 'hris', schema: 'transaction', name: 'Attendance' }
    return [
      { align: 'left',  formatter: null,       name: 'action', field: 'id', label: '#', style: 'width: 20px' },
      { align: 'left',  formatter: 'date',     name: 'date', field: 'date', label: L.module(meta, 'date'), is_date: true },
      { align: 'left',  formatter: 'time', name: 'clock_in', field: 'clock_in', label: L.module(meta, 'clock_in'), is_date: true, datetime: true },
      { align: 'left',  formatter: 'time', name: 'clock_out', field: 'clock_out', label: L.module(meta, 'clock_out'), is_date: true, datetime: true },
      { align: 'left',  formatter: null,       name: 'status', field: 'status', label: L.module(meta, 'status') },
      { align: 'left',  formatter: null,       name: 'location_type', field: 'location_type', label: L.module(meta, 'location_type') },
      { align: 'left',  formatter: null,       name: 'gps_coordinates', field: 'gps_coordinates', label: L.module(meta, 'gps_coordinates') },
      { align: 'left',  formatter: null,       name: 'project_id', field: 'project_id', label: L.module(meta, 'project_id') },
      { align: 'left',  formatter: null,       name: 'nik', field: 'nik', label: L.module(meta, 'nik') },
      { align: 'left',  formatter: null,       name: 'username', field: 'username', label: L.module(meta, 'username') },
    ]
  }
}
