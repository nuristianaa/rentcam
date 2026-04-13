import { Helper } from 'src/services/helper'

function readUtc(dateStr: string) {
  const cleanedTimestamp = dateStr.replace('T', ' ').substring(0, 19)
  const utcDate = new Date(cleanedTimestamp)
  // Convert to UTC+7 by adding 7 hours (in milliseconds)
  const tzOffset = 7 * 60 * 60 * 1000
  const date = new Date(utcDate.getTime() + tzOffset)
  const day = String(date.getDate()).padStart(2, '0')
  const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  const month = monthNames[date.getMonth()]
  const year = String(date.getFullYear()).slice(2) // get last 2 digits
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')

  return `${day}-${month}-${year} ${hours}:${minutes}:${seconds}`
}

export enum ConstApprovalType {
  first_to_respond = 'FirstToRespond',
  everyone = 'Everyone'
}

export enum ConstApprovalStatus {
  pending = 'Pending',
  ongoing = 'Ongoing',
  reject = 'Reject',
  approve = 'Approve',
  cancel = 'Cancel'
}

export enum ConstUserType {
  approver = 'Approver',
  receiver = 'Receiver'
}

export enum ConstAction {
  cancel = 'Cancel',
  send = 'Send'
}

export interface Approver {
  approver: string | null
  approver_name: string | null
  approver_title: string | null
  approver_group: string | null
  id?: string | null
  sent?: string | null
  result?: string | null
  comment?: string | null
}

export interface Details {
  type: string | null
  sequence_number: number | null
  expires: string | null
  approvers: Approver[]
}

export interface insertedDataModel {
  app: string | null
  code: string | null
  module_name: string | null
  module_id: string | number | null
  title: string | null
  description: string
  requester: string | null
  requester_name: string | null
  requester_department: string | null
  approval_type: ConstApprovalType | null
  approval_method: ConstApprovalMethod | null
  details: Details[]
  status: string | null
  cancel_remark: string | null
}

export interface DataModel extends insertedDataModel {
  id: string | null
  status_percentage: number | null
  created_date: string | null
  expiration_date: string | null
  is_closed: boolean
  created_by: string | null
  raw_details?: any
}

export function generateDataModel(): DataModel {
  return {
    id: null,
    app: null,
    code: null,
    module_name: null,
    module_id: null,
    title: null,
    description: '',
    requester: null,
    requester_name: null,
    requester_department: null,
    approval_type: ConstApprovalType.everyone,
    approval_method: 'manual',
    cancel_remark: null,
    status: 'Pending',
    status_percentage: null,
    is_closed: false,
    details: [
      {
        type: ConstApprovalType.everyone,
        sequence_number: 1,
        expires: Helper.now(20),
        approvers: []
      }
    ],
    created_date: null,
    expiration_date: null,
    created_by: null
  }
}

export const Meta = {
  app: 'main',
  schema: 'transaction',
  name: 'approvals',
  classname: 'Approval',
  title: 'Approvals',
  module: 'transaction/approvals',
  route_ui: 'transaction/approvals',
  permission: { browse: true, create: true, read: true, update: true, delete: true, restore: true },
  tableDetail: () => {
    return [
      { align: 'left', formatter: null, name: 'type', field: 'type', label: 'Type' },
      { align: 'right', formatter: 'integer', name: 'sequence_number', field: 'sequence_number', label: 'Sequence' },
      { align: 'left', formatter: null, name: 'type', field: 'type', label: 'Approval Type' },
      { align: 'left', formatter: null, name: 'approver', field: 'approver', label: 'Approver email' },
      { align: 'left', formatter: null, name: 'approver_name', field: 'approver_name', label: 'Approver Name' },
      { align: 'left', formatter: null, name: 'result', field: 'result', label: 'Result' },
      { align: 'left', formatter: null, name: 'comment', field: 'comment', label: 'Comment' },
      { align: 'left', formatter: null, name: 'sent', field: 'sent', label: 'Sent' },
      { align: 'left', formatter: null, name: 'expires', field: 'expires', label: 'Expires' },
      { align: 'left', formatter: null, name: 'responded_date', field: (v: { responded_date: string }) => (v.responded_date ? readUtc(v.responded_date) : ''), label: 'Responded Date' },
    ]
  }
}

export default Meta
