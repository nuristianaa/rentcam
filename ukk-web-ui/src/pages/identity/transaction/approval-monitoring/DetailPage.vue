<template>
  <div>
    <s-loading v-if="loading" />
    <h-detail v-else :meta="Meta" @back="back" :model="dataModel">
      <div class="row q-pa-sm">
        <f-card :title="`${dataModel.module_name}`" col="12">
          <component
            v-if="detailEntry"
            :is="detailEntry.component"
            v-bind="detailProps"
          />
        </f-card>
        <f-card title="Approval" col="12">
          <r-table :meta="Meta" :columns="tableDetailMeta" v-model="dataModel.raw_details">
          </r-table>
        </f-card>

        <div class="col-12 row justify-end q-gutter-sm" v-if="!dataModel.result">
          <q-btn
            label="Approve"
            icon="playlist_add_check"
            color="positive"
            @click="submit('Approve')"
          />

          <q-btn
            label="Reject"
            icon="playlist_remove"
            color="negative"
            @click="showReject = true"
          />
        </div>
      </div>
    </h-detail>
    <q-dialog v-model="showReject" persistent>
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">Alasan Reject</div>
        </q-card-section>
  
        <q-card-section>
          <q-input
            v-model="rejectReason"
            type="textarea"
            autogrow
            label="Komentar / Alasan"
            outlined
            :rules="[val => !!val || 'Alasan wajib diisi']"
          />
        </q-card-section>
  
        <q-card-actions align="right">
          <q-btn flat label="Batal" color="grey" v-close-popup />
          <q-btn
            label="Reject"
            color="negative"
            :disable="!rejectReason"
            @click="submit('Reject')"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>

</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { useQuasar } from 'quasar'
import { ref, onMounted, computed, defineAsyncComponent } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Meta } from './meta'
import Detail from '../../auth/users/detail.vue'
import { detailRegistry } from 'src/pages/detail-registry'
import { authStore } from 'src/stores/auth'

const $q = useQuasar()
const route = useRoute()
const router = useRouter()
const API = new Api()
const id = Array.isArray(route.params?.id) ? route.params.id[0] : (route.params?.id ?? null)
const Auth = authStore()
const user = Auth.getUser()

const loading = ref(true)
const dataModel = ref(Meta.model)
const dataModelFeedback = ref(Meta.model_feedback)
const viewList = ref<{ label: string; value: any }[]>([])
const tableDetailMeta = Meta.tableDetail()
tableDetailMeta.splice(0, 0, { align: 'center', formatter: null, name: 'action', field: 'action', label: '#' });
const showReject = ref(false)
const rejectReason = ref(null)


/*** METHODS ***/
const init = () => {
  dataModel.value = Helper.unreactive(Meta.model)
  dataModelFeedback.value = Helper.unreactive(Meta.model_feedback)
  Handler.permissions(router, 'read', Meta, (status, data) => {
    Meta.permission = data
    if (status) onRefresh()
  })
}

const onRefresh = () => {
  if (id) getData(id)
  else loading.value = false
}

const getData = (id: string | number) => {
  loading.value = true
  const endpoint = `${Meta.module}/${id}`
  API.get(
    endpoint,
    (status: number, data: any) => {
      loading.value = false
      if (status === 200) {
        dataModel.value = data
        dataModelFeedback.value = {
          parent_id: dataModel.value.id,
          app: dataModel.value.app,
          module_name: dataModel.value.module_name,
          module_id: dataModel.value.module_id,
          code: dataModel.value.code,
          status: dataModel.value.status,
          approval_id: id,
          response: null,
        }
        const config = {
          app: 'identity',
          schema: 'transaction',
          name: 'approvals',
          exclude: ['id', 'raw_details', 'details'],
          float: [],
          integer: ['status_percentage'],
          date: [],
          datetime: [],
          constant: [],
          money: [],
          detail: []
        }
        viewList.value = Handler.viewList(dataModel.value, config)
      }
    },
    Meta.app
  )
}

const submit = (outcome: 'Reject' | 'Approve') => {
  Helper.confirm('Are you sure?', (result: boolean) => {
    if (result) {
      execSubmit(outcome)
    }
  })
}

const execSubmit = async (outcome: 'Reject' | 'Approve') => {
  let res = null
  loading.value = true

  if (!rejectReason.value && outcome == 'Reject') return

  loading.value = true

  const status = await feedback(outcome)

  if (status === 200) {
    Helper.showSuccess('Data has been successfully ' + outcome)
    getData(id)
  }
  loading.value = false
  // set reject var
  showReject.value = false
  rejectReason.value = null

}

const feedback = async (outcome: string) => {
  let statusapi = 600
  const payload = dataModelFeedback.value
  payload.response = {
    outcome: outcome,
    responded_by: user.username,
    responded_name: user.name,
    responded_date: Helper.today(),
    comments: rejectReason.value,
  }
  await API.post(Meta.module + '/feedback', payload, (status: number, _data: any) => {
    statusapi = status
  })
  return statusapi
}


const back = () => {
  router.back()
}

/*** MOUNTED | COMPUTED | WATCHERS ***/
onMounted(() => {
  init()
})

// render detail page
const detailEntry = computed(() => {
  const app = dataModel.value?.app
  const modulePath = dataModel.value?.module_name

  if (!app || !modulePath) return null

  const normalized = modulePath.replaceAll('/', '.')
  return detailRegistry[`${app}.${normalized}`] || null
})

const detailProps = computed(() => {
  if (!detailEntry.value) return {}
  return detailEntry.value.props
    ? detailEntry.value.props({ model: dataModel.value })
    : {}
})
</script>
