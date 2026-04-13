<template>
  <div class="col-12 row">
    <f-card title="Detail" col="6">
      <s-list v-for="(value, index) in viewList" :key="index" :data="value" />
    </f-card>
    <f-card title="Log" col="6">
      <log-info :data="dataModel" />
    </f-card>
    <f-card title="Details" col="12">
      <r-table :meta="Meta" :columns="Meta.tableDetail()" v-model="dataModel.raw_details" />
    </f-card>
    <div class="q-pa-sm"> 
      <q-btn  size="sm" @click="sync_approval"  label="Sync Approval Info" color="primary" class="q-px-md" no-caps dense icon="autorenew" >
        <q-tooltip>Sync the approval info with main approval data</q-tooltip>
      </q-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, onMounted } from 'vue'
import { Handler } from 'src/services/handler'
import { Meta } from './meta'
import { Helper } from 'src/services/helper'

const props = defineProps<{ modelValue: any }>()
const API = new Api()
const emit = defineEmits(['refreshEvent'])
const loading = ref(false)
const dataModel = ref(props.modelValue)
const viewList = ref<{ label: string; value: any; is_html?: boolean }[]>([])

/*** METHODS ***/
const init = () => {
  getData()
}

const getData = () => {
  const d = dataModel.value
  if (d.url_files) {
    dataModel.value.url_files.forEach((v: any) => {
      v.src = Helper.viewBlobFile(v.clean_path, v.is_public, v.storage_id)
    })
  }
  viewList.value = [
    { label: 'Requester', value: `${d.requester_name} (${d.requester}) ${d.requester_department ?? ''}` },
    { label: 'Title / Subject', value: d.title },
    { label: 'Description', value: d.description, is_html: true },
    { label: 'Title / Subject', value: d.title },
    { label: 'Module', value: d.module_name },
    { label: 'Code', value: d.code }
  ]
}

const sync_approval = async () => {
  loading.value = true
  const status = await update()
  if (status === 200){
    genFile()
  }
  if (status == 200) {
    Helper.showSuccess('Data has been successfully saved.')
    back()
  }
  loading.value = false
}

const update = async () => {
  let statusapi = 600
  await API.put(
    `${Meta.module}/sync-origin/${dataModel.value.id}`,
    {},
    (status: number, _data: any) => {
      statusapi = status
    },
    Meta.app
  )

  return statusapi
}


const back = () => {
  // if (!props.props) router.back()
  emit('refreshEvent')
}

/*** MOUNTED | COMPUTED | WATCHERS ***/
onMounted(() => {
  init()
})
</script>
