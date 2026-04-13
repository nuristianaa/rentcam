<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else @submit="submit" :meta="Meta" :modal="true">
      <template v-if="dataModel.status == ConstApprovalStatus.pending">
        <s-banner color="blue-8" class="">
          <div class="text-h4">Approval Pending</div>
          Please complete the form and submit it for approval. &nbsp;
          <q-btn size="sm" @click="submit('run')"  color="green" class="q-px-sm q-pr-md" icon="sync" no-caps dense unelevated>&nbsp; Run Approval</q-btn>
        </s-banner>
      </template>
      <s-banner v-else-if="dataModel.status == ConstApprovalStatus.approve" color="green-8" class="">
        <div class="text-h4">Approval Competed</div>
        Do you have any issue? If you want to resubmit, you have to cancel first. &nbsp;
        <q-btn v-if="isAllowedCancel" size="sm"  label="Cancel Approval" color="red" class="q-px-md" no-caps dense>
          <q-popup-proxy>
            <q-banner>
              <div class="text-bold q-pb-sm">Approval Cancellation</div>
              <q-input type="textarea" outlined v-model="dataModel.cancel_remark" label="Cancel Remark" />
              <q-btn v-if="dataModel.cancel_remark" class="full-width q-mt-sm" color="primary" label="Submit" @click="submit('cancel')" />
            </q-banner>
          </q-popup-proxy>
        </q-btn>
      </s-banner>

      <s-banner v-else-if="dataModel.status == ConstApprovalStatus.ongoing" color="blue-8" class="">
        <div class="text-h4 q-pb-xs">Approval is Running</div>
        Approval is currently in progress, the system has sent an email to the "Approvers".

        <span v-if="isAllowedCancel">if you want to cancel this process you can click:</span>
        <q-btn v-if="isAllowedCancel" size="sm"  label="Cancel Approval" color="red" class="q-px-md" no-caps dense>
          <q-popup-proxy>
            <q-banner>
              <div class="text-bold q-pb-sm">Approval Cancellation</div>
              <q-input type="textarea" outlined v-model="dataModel.cancel_remark" label="Cancel Remark" />
              <q-btn v-if="dataModel.cancel_remark" class="full-width q-mt-sm" color="primary" label="Submit" @click="submit('cancel')" />
            </q-banner>
          </q-popup-proxy>
        </q-btn>
      </s-banner>

      <s-banner v-else-if="dataModel.status == ConstApprovalStatus.cancel" color="red-8" class="">
        <div class="text-h4 q-pb-xs">Approval has been Canceled by User</div>
        Reason : {{ dataModel.cancel_remark }}
        <br />
        <template v-if="isAllowedRenew">
          If you want to resubmit the approval, click &nbsp;
          <q-btn size="sm" @click="submit('renew')"  color="blue" class="q-px-md" icon="sync" no-caps dense>Renew Approval Now</q-btn>
        </template>
      </s-banner>
      
      <s-banner v-else-if="dataModel.status == ConstApprovalStatus.reject" color="red-8" class="">
        <div class="text-h4 q-pb-xs">Approval has been Rejected by Approver</div>
        <template v-if="isAllowedRenew">
          If you want to resubmit the approval, click &nbsp;
          <q-btn size="sm" @click="submit('renew')"  color="blue" class="q-px-md" icon="sync" no-caps dense>Renew Approval Now</q-btn>
        </template>
      </s-banner>
      <!-- BODY -->
      <div v-if="isNotReadonly" class="col-12 row q-pt-md">
        <!-- GENERAL INFO -->
        <div class="col-12">
          <div class="q-py-sm">
            <div class="title text-primary">General Info</div>
            <q-markup-table class="q-pb-md" unelevated flat dense separator="none">
              <tbody>
                <tr>
                  <td>Requester </td>
                  <td>
                    {{`${dataModel.requester_name} (${dataModel.requester}) ${requester_department ?? ''}`}}
                  </td>
                </tr>
                <tr>
                  <td>Title (Subject)</td>
                  <td><q-input dense class="form-sm" outlined v-model="dataModel.title" /></td>
                </tr>
                <tr>
                  <td>Description</td>
                  <td><q-editor v-model="dataModel.description" min-height="5rem" /></td>
                </tr>
              </tbody>
            </q-markup-table>
          </div>
        </div>

        <!-- DETAILS -->
        <div class="col-12 q-mt-md">
          <div class="col-12 row items-center" style="margin-bottom: 15px" v-if="dataModel.details.length && !ApproverList.length">
            <s-banner color="orange-9" icon="info">
              <div class="text-bold">Please add the approver first by pressing the "Add Approver" button in the Sequence list below, and make sure you have added the user to the approver table.</div>
            </s-banner>
          </div>

          <div class="row justify-between">
            <div class="title text-primary">Approvers</div>
            <div class="row q-gutter-x-sm items-end">
              <q-btn label="Add Sequence" icon="add" color="primary" @click="addSequence()" />
            </div>
          </div>

          <div v-for="(v, i) in dataModel.details" :key="i">
            <div v-if="i > 0" class="col-12 text-center">
              <q-icon name="keyboard_double_arrow_down" size="md" style="font-weight: 0 !important" tag="div"></q-icon>
            </div>
            <q-card class="q-mx-xs q-my-sm" flat bordered>
              <q-card-section>
                <!-- Top Buttons -->
                <div class="row justify-between">
                  <div class="column">
                    <div class="text-h5">Sequence {{ v.sequence_number = i + 1 }}</div>
                    <div class="row q-mt-xs q-gutter-sm">
                      <q-btn class="q-px-sm" dense no-caps color="negative" label="Delete sequence" @click="deleteSequence(i)" />
                      <q-btn class="q-px-sm" dense no-caps color="primary" label="Add Approver" @click="addApprover(v, i)" />
                    </div>
                  </div>
                  <q-markup-table class="q-px-sm q-pb-md table-no-padding" flat dense separator="horizontal">
                    <tbody>
                      <tr>
                        <td>
                          Approval Type
                          <q-icon name="info" color="info">
                            <q-tooltip>
                              FirstToRespond: The result is based on the first response from any approver.
                              <br />
                              Everyone: All approvers must respond.
                            </q-tooltip>
                          </q-icon>
                        </td>
                        <td>
                          <f-select-table must-fill hideBottomSpace v-model="v.type" :options="opt.approval_type" :disable="v.is_external" />
                        </td>
                      </tr>
                      <tr>
                        <td>
                          Approval Expires
                          <q-icon name="info" color="info">
                            <q-tooltip>If approver do not respond after this period, the approval is automatically approved. The max can be picked is 30 days from today.</q-tooltip>
                          </q-icon>
                        </td>
                        <td><f-date-table datetime v-model="v.expires" class="q-px-sm" /></td>
                      </tr>
                    </tbody>
                  </q-markup-table>
                </div>

                <q-markup-table class="q-pb-md table-no-padding" flat dense separator="cell">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Approver</th>
                      <th>Approver Title</th>
                    </tr>
                  </thead>
                  <tbody>
                    <s-drag v-model="v.approvers" container="tr">
                      <template #default="{ item: v2, index: i2 }">
                        <td>
                          <q-btn dense flat round color="negative" icon="delete" @click="deleteApprover(i, i2)" />
                          <q-icon name="drag_indicator" color="black" />
                        </td>
                        <td>
                          <f-select-table v-model="v2.approver" :options="handleOptApproval(opt.approvers)" optionValue="email" :optionLabel="(v: any) => (v.email ? v.email + ' - ' + v.name : (v.email ?? v))" @update:modelValue="onApproverChange(v2)" />
                        </td>
                        <td>
                          <f-input-table v-model="v2.approver_title" />
                        </td>
                      </template>
                    </s-drag>
                  </tbody>
                </q-markup-table>
              </q-card-section>
            </q-card>
          </div>

          <div v-if="!dataModel.details.length" class="text-center text-h4 text-grey-5 q-pa-xl">There are no approvers at this time, click "ADD SEQUENCE" to define approval PIC</div>
        </div>
      </div>

      <!-- Details -->
      <ApprovalDetail v-if="dataModel && !isNotReadonly" :model-value="dataModel" />
    </h-form>
  </div>
</template>

<script setup lang="ts">
import { authStore } from 'src/stores/auth'
import { Config } from 'src/services/config'
import { Dark } from 'quasar'
import { Helper } from 'src/services/helper'
import { Handler } from 'src/services/handler'
import { Meta, generateDataModel, ConstApprovalStatus, ConstApprovalType } from './meta'
import { ref, onMounted, computed, watch } from 'vue'
import Api from 'src/services/api'
import ApprovalDetail from './ApprovalDetail.vue'
import type { DataModel, Approver } from './meta'
import type { Dialog } from 'src/services/handler'
import type { SignBlock } from 'src/components/sign-placements/meta'

const props = defineProps<{
  data?: any
  module_data?: any // { id: string | number; code?: string }
  module_meta?: any // { app: string; module: string; title?: string }
  title?: string
  requester_department?: string
}>()

const emit = defineEmits(['refreshEvent'])

const API = new Api()
const Auth = authStore()
const user = Auth.getUser()
const dialog = ref<Dialog>({
  show: false,
  type: 'form',
  title: 'Form',
  props: null,
  maximize: false,
  persistent: true,
  width: '75vw'
})

const loading = ref(true)
const dataModel = ref<DataModel>(generateDataModel())
const dataModelTransaction = ref<any>(null)

const showSignatureCard = ref<boolean>(false)
const signatureCards = ref<SignBlock[]>([])
const approversList = computed<Approver[]>(() =>
  dataModel.value?.raw_details
    ? dataModel.value?.raw_details?.map((item: Approver) => ({
        id: item.id,
        email: item.approver,
        name: item.approver_name,
        title: item.approver_title
      }))
    : []
)

let isInitialDetailsWatch = true
let isRevertingDetails = false
let prevDetails: DataModel['details'] | null = null
watch(
  () => dataModel.value.details,
  (newVal, oldVal) => {
    if (isInitialDetailsWatch) {
      isInitialDetailsWatch = false
      prevDetails = JSON.parse(JSON.stringify(newVal))
      return
    }
    if (isRevertingDetails) {
      isRevertingDetails = false
      prevDetails = JSON.parse(JSON.stringify(dataModel.value.details))
      return
    }
    prevDetails = JSON.parse(JSON.stringify(dataModel.value.details))
  },
  { deep: true }
)

const opt = ref<{
  approval_type: string[]
  status: string[]
  approvers: any[]
}>({
  approval_type: [],
  status: [],
  approvers: []
})

/*** MOUNTED | COMPUTED | WATCHERS ***/
onMounted(() => {
  init()
})

const isNotReadonly = computed(() => {
  if (dataModel.value.status != ConstApprovalStatus.pending) return false
  return true
})

/*** METHODS ***/
const init = () => {
  dataModel.value.requester = user.username
  dataModel.value.requester_name = user.name
  dataModel.value.requester_department = props?.requester_department || ''
  if (props?.module_meta) {
    dataModel.value.app = props.module_meta.app
    dataModel.value.module_name = props.module_meta.module || ''
    dataModel.value.title = props.module_meta.title || ''
    dataModel.value.description = ''
    dataModel.value.module_id = props.module_data?.id || ''
    dataModel.value.code = props.module_data?.code || ''
  }
  if (props?.title) dataModel.value.title = props.title || ''
  onRefresh()
}

const onRefresh = async () => {
  loading.value = true
  getOpt()
  if (props.data?.id || props.module_data?.id) await getData()
  if (props.module_data?.id) await getDataModelModule()
  loading.value = false
}

const getOpt = () => {
  const ep = `${Meta.module}?option=true&current_status=${dataModel.value.status}`
  API.get(
    ep,
    (status: number, data: any) => {
      if (status === 200) opt.value = data
    },
    'main'
  )
}


const getData = async () => {
  let ep = `${Meta.module}`
  if (props.data?.id) ep += `/${props.data?.id}`
  else if (props?.module_meta) ep += `/by-module?app=${props.module_meta.app}&module_name=${props.module_meta.module}&module_id=${props.module_data.id}`
  await API.get(
    ep,
    (status: number, data: any) => {
      if (status === 200) {
        if (data) dataModel.value = data
        // console.log('getData: ', ep, data)
        if (!dataModel.value.description) dataModel.value.description = ''
        // console.log(props)
        if (!data && props?.module_data?.default_title) dataModel.value.title = props?.module_data?.default_title

        getOpt() // refresh list ketika mendapatkan update data terbaru
      }
    },
    Meta.app
  )
  return
}

const getDataModelModule = async () => {
  if (!props.module_data?.id) return
  const ep = `${props.module_meta.module}/${props.module_data.id}`
  await API.get(
    ep,
    (status: number, data: any) => {
      if (status === 200 && data) dataModelTransaction.value = data
    },
    props.module_meta.app
  )
}

const handleOptApproval = (opt: any[], is_external: boolean | null = false) => {
  return opt.filter((v) => v.is_contact != 1)
}

/*** STORE DATA ***/
const validateSubmit = () => {
  const max30Day = Helper.now(30)
  let msg = ''
  let totalApprover = 0
  if (dataModel.value?.details && dataModel.value?.details.length) {
    dataModel.value.details.map((d: any, i: any) => {
      if (d.approvers.length == 0) msg += `Approver on sequence ${d.sequence_number} is is None!<br>`
      if (new Date(max30Day).getTime() < new Date(d.expires).getTime()) msg += `Expires on sequence ${d.sequence_number} is more than 30 days!<br>`
      d.approvers.map((r: any, i2: any) => {
        if (!r.approver) msg += `Approver on sequence ${d.sequence_number}.${i2 + 1} is empty!<br>`
        if (!r.approver_title) msg += `Approver title on sequence ${d.sequence_number}.${i2 + 1} is empty!<br>`
        totalApprover++
      })
    })
  }
  if (totalApprover == 0) msg += 'No approvers have been selected yet!'

  if (msg === '') {
    return true
  } else {
    Helper.showAlert('Opps!', msg)
    return false
  }
}

const submit = (type: 'run' | 'renew' | 'cancel' | null = null) => {
  if (validateSubmit()) {
    Helper.confirm('Are you sure?', (result: boolean) => {
      if (result) {
        if (type == 'cancel') {
          if (!isAllowedCancel.value) {
            Helper.showAlert('Cancel Not Allowed!.')
            back()
            return
          } else {
            execSubmit(type)
          }
        } else {
          execSubmit(type)
        }
      }
    })
  }
}

const execSubmit = async (type: 'run' | 'renew' | 'cancel' | null = null) => {
  let res = null
  loading.value = true

  if (dataModel.value.id) res = await update()
  else res = await save()

  if (res.status_api === 200) {
    if (type == 'run') res = await run()
    if (type == 'renew') res = await renewApproval()
    if (type == 'cancel') res = await cancel()
  }

  loading.value = false
  if (res.status_api === 200) {
    Helper.showSuccess('Data saved.')
    back()
  }
}

const save = async () => {
  let statusapi = 600
  let dataapi = null
  await API.post(
    Meta.module,
    dataModel.value,
    (status: number, data: any) => {
      statusapi = status
      dataapi = data
      dataModel.value.id = data.id
    },
    Meta.app
  )

  return { status_api: statusapi, data_response: dataapi }
}

const update = async () => {
  let statusapi = 600
  let dataapi = null
  await API.put(
    `${Meta.module}/${dataModel.value.id}`,
    dataModel.value,
    (status: number, data: any) => {
      statusapi = status
      dataapi = data
      dataModel.value.id = data.id
    },
    Meta.app
  )

  return { status_api: statusapi, data_response: dataapi }
}

const run = async () => {
  let statusapi = 600
  let dataapi = null
  await API.put(
    `${Meta.module}/run/${dataModel.value.id}`,
    dataModel.value,
    (status: number, data: any) => {
      statusapi = status
      dataapi = data
    },
    Meta.app
  )

  return { status_api: statusapi, data_response: dataapi }
}

const renewApproval = async () => {
  let statusapi = 600
  let dataapi = null

  await API.put(
    `${Meta.module}/renew/${dataModel.value.id}`,
    dataModel.value,
    (status: number, data: any) => {
      loading.value = true
      statusapi = status
      dataapi = data
      Helper.showAlert('Renewal Success', 'The approval has been reset, you can resend the approval or set it first before resending this approval.')
      onRefresh()
    },
    Meta.app
  )

  return { status_api: statusapi, data_response: dataapi }
}

const cancel = async () => {
  let statusapi = 600
  let dataapi = null
  await API.put(
    `${Meta.module}/cancel/${dataModel.value.id}`,
    dataModel.value,
    (status: number, data: any) => {
      statusapi = status
      dataapi = data
      if (data) {
        Helper.showAlert('Cancel Success', 'Cancellation emails have been sent to all "Approvers"')
      } else {
        Helper.showAlert('Cancel Success [Wihtout Email]', 'Cancellation process has been completed, but emails not sent to all "Approvers"')
      }
    },
    Meta.app
  )
  return { status_api: statusapi, data_response: dataapi }
}

const back = () => {
  emit('refreshEvent')
}

// DETAILS & FILES
const addSequence = () => {
  const lenSeq = dataModel.value.details.length + 1
  dataModel.value.details.push({
    type: ConstApprovalType.everyone,
    sequence_number: lenSeq,
    expires: Helper.now(20),
    approvers: []
  })
}

const onApproverChange = (v2: any) => {
  const user = opt.value.approvers.find((v) => v.email == v2.approver)
  if (user) {
    v2.approver = user.email || ''
    v2.approver_name = user.name || ''
    v2.approver_title = user.title || ''
  } else {
    v2.approver_name = ''
    v2.approver_title = ''
  }
}

const deleteSequence = (index: number) => {
  dataModel.value.details?.splice(index, 1)
}

const addApprover = (_v: any, i: number) => {
  const row = {
    approver: null,
    approver_name: null,
    approver_title: null,
  }
  dataModel.value.details[i]?.approvers.push(row)
}

const deleteApprover = (i: number, i2: number) => {
  dataModel.value.details[i]?.approvers?.splice(i2, 1)
}

const statusColor = (status: string) => {
    switch (status) {
      case 'Approve': return 'positive'
      case 'Pending': return 'warning'
      case 'Cancel': return 'negative'
      default: return 'info'
    }
  }

const isAllowedCancel = computed(() => {
  if (dataModel.value.created_by === user.username || Handler.hasAdditionalPermision('allow_cancel_approval')) return true
  else return false
})

const isAllowedRenew = computed(() => {
  return isAllowedCancel.value
})

const ApproverList = computed(() => {
  const res: any = []
  if (dataModel.value.details.length) {
    dataModel.value.details.map((r) => {
      r.approvers.map((ap) => {
        if (ap.approver) res.push(ap)
      })
    })
  }
  return res
})
</script>
