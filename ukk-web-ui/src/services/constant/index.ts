import { Screen, Dark } from 'quasar'
import Cfunction from './function'
import crmConstant from './crmConstant'
import procurementConstant from './procurementConstant'
import engineeringConstant from './engineeringConstant'
import projectConstant from './projectConstant'
import financeConstant from './financeConstant'
import hrisConstant from './hrisConstant'

type TranslationObject = { id: string | number; name: string }

export const Constant = {
  ...Cfunction,
  ...crmConstant,
  ...financeConstant,
  ...procurementConstant,
  ...engineeringConstant,
  ...projectConstant,
  ...hrisConstant,
  modalBodyHeight: null,
  numberPrecision: 3,
  moneyPrecision: 2,
  editColor() {
    return Dark.isActive ? '' : 'primary'
  },
  edit2Color() {
    return Dark.isActive ? '' : 'primary'
  },
  edit3Color() {
    return Dark.isActive ? '' : 'primary'
  },
  edit4Color() {
    return Dark.isActive ? '' : ''
  },
  viewColor() {
    return Dark.isActive ? '' : 'primary'
  },
  tableHeight(minus: number = 0) {
    return Screen.height - 150 - minus
  },
  colors(val: number) {
    const col = ['white', 'positive', 'info', 'accent', 'primary', 'negative', 'secondary', 'dark']
    const i = val
    if (i >= 0) return col[i]
    else return 'primary'
  },
  default: [
    { id: 1, name: 'Yes' },
    { id: 0, name: 'No' }
  ],
  active: [
    { id: 1, name: 'Active' },
    { id: 0, name: 'Inactive' }
  ],
  years: [2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040],
  quartals: [1, 2, 3, 4],
  groupSp: ['dashboard_item'],
  language: ['ID', 'EN'],
  gender: ['Male / Laki-laki', 'Female / Perempuan'],
  religions: ['Islam', 'Kristen Katolik', 'Kristen Protestan', 'Hindu', 'Buddha', 'konghucu', 'Lainnya'],
  csvdelimiter: [
    { id: ';', name: 'Semicolon (;)' },
    { id: ',', name: 'Comma (,)' }
  ],
  // CONSTANT
  componentTesting: [
    { name: 'form-examples', label: 'Form Examples', query: {} },
    { name: 'generator', label: 'Generator', query: {} },
    { name: 'qr-code-testing', label: 'QR Code Testing', query: {} }
    // {name: 'gmaps-testing', label: 'GMaps Testing', query: {} },
    // {name: 'calendar-testing', label: 'Calendar Testing', query: {} },
    // {name: 'gantt-testing', label: 'Gantt Chart Testing', query: {} }
  ],
  weekdays: [
    { label: 'Monday', value: 'monday' },
    { label: 'Tuesday', value: 'tuesday' },
    { label: 'Wednesday', value: 'wednesday' },
    { label: 'Thursday', value: 'thursday' },
    { label: 'Friday', value: 'friday' },
    { label: 'Saturday', value: 'saturday' },
    { label: 'Sunday', value: 'sunday' }
  ],
  month_days() {
    return Array.from({ length: 31 }, (_, i) => ({ label: `${i + 1}`, value: i + 1 }))
  },

  translate(value: string | number, constant_slug: string): string {
    let translate = ''
    try {
      const dots = constant_slug.split('.')
      const len = dots.length

      interface MyObject {
        [key: string]: any
      }
      let obj: MyObject | undefined

      if (dots[0]) {
        if (dots[0] == 'crm') obj = this.crm
        if (obj && dots[1]) {
          obj = obj?.[dots[1]]
          if (obj && dots[2]) {
            obj = obj?.[dots[2]]
            if (obj && dots[3]) {
              obj = obj?.[dots[3]]
            }
          }
        }
      }

      if (obj && Array.isArray(obj)) {
        const found = obj.find((e) => e.id === value)
        if (found) translate = found.name
      }
    } catch {
      translate = ''
    }
    return translate
  },

  identity: {
    apps: ['identity', 'crm', 'engineering', 'finance', 'procurement', 'project_management', 'hris'],
    auth: {
      event_notifications: {
        channel: [
          { label: 'Email', value: 'email' },
          { label: 'Push', value: 'push' }
        ],
        schedule_type: [
          { label: 'Day', value: 'day' },
          // { label: 'Weekly', value: 'weekly' },
          // { label: 'Monthly', value: 'monthly' },
          { label: 'CRUD', value: 'crud' },
          { label: 'Event Based', value: 'event_based' },
          { label: 'Custom', value: 'custom' }
        ],
        crud_events: {
          label: { label: 'Data identifier' },
          type: { label: 'CRUD Event' },
          user: { label: 'Username who triggered it' }
        }
      }
    },
    transaction: {
      approvals: {
        status: ['Pending', 'Ongoing', 'Reject', 'Approve'],
        sync_status: [
          { id: 1, name: 'unsync' },
          { id: 2, name: 'sync' }
        ]
      },
      approval_details: {
        type: ['email'],
        sync_status: [
          { id: 1, name: 'unsync' },
          { id: 2, name: 'sync' }
        ]
      },
      sync_logs: {
        status: [
          { id: 1, name: 'success' },
          { id: 2, name: 'failed' }
        ]
      }
    }
  }
}
