<template>
  <div>
    <f-card title="Download Document" row class="q-mt-md">
      <div class="col-12 row items-start justify-between">
        <f-select v-model="downloadDocumentFilter.templateId" :api="`master/printout-templates?where=ref_module:${props.meta.ref_module}`" app="crm" optionValue="id" :optionLabel="(v: any) => v.name" dense col="6" />
        <f-select v-model="downloadDocumentFilter.exportType" :options="documentTypeOptions" col="4" />
        <div class="col-12 col-md-2 q-mt-sm">
          <q-btn label="Download" icon="download" dense  color="primary" class="q-px-sm" :disabled="!downloadDocumentFilter.templateId" @click.prevent="downloadDocument" />
        </div>
      </div>
    </f-card>
    <f-card title="Document Histories" class="q-mt-md">
      <q-table bordered :columns="table.columns" dense :filter="table.search" flat row-key="id" :rows="table.data" :rows-per-page-options="[10, 50, 100, 0]" separator="cell" wrap-cells>
        <template v-slot:body-cell-created_at="props">
          <q-td :props="props">
            {{ Helper.readDate(props.row.created_at, true) }}
          </q-td>
        </template>
      </q-table>
    </f-card>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, onMounted } from 'vue'
import { Helper } from 'src/services/helper'
import { Handler } from 'src/services/handler'
import { Meta } from './meta'
import { authStore } from 'src/stores/auth'

const props = defineProps<{
  meta: {
    app: string
    module: string
    ref_module?: string
  }
  data: {
    id: string | number
    code?: string
    name?: string
  }
}>()
const emit = defineEmits(['refreshEvent', 'callbackApi'])

const API = new Api()
const table = ref<any>({
  loading: false,
  data: [],
  pagination: {
    page: 1,
    rowsPerPage: 7,
    sortBy: '',
    descending: false,
    rowsNumber: 0
  },
  search: null // native search
})

const downloadDocumentFilter = ref({
  templateId: <string | null>null,
  exportType: <string>'pdf'
})

const company_code = authStore().getCompanyCode()

const documentTypeOptions = ['pdf', 'docx']

// METHODS
const handleTable = () => {
  table.value = Handler.table(Meta.columns)
  table.value.pagination.rowsPerPage = 7
  getDocumentHistories()
}

const init = () => {
  handleTable()
}

const getDocumentHistories = async () => {
  table.value.loading = true
  let ep = Meta.module
  ep += `?where=app:${props.meta.app}`
  ep += `&where=module:${props.meta.ref_module}`
  ep += `&where=module_id:${props.data.id}`
  ep += '&limit=0'
  await API.get(
    ep,
    (status: number, data: any) => {
      table.value.loading = false
      if (status === 200) {
        table.value.data = data
      }
    },
    'main'
  )
}

const downloadDocument = async () => {
  if (!props.data.id) return

  let ep = props.meta.module
  ep += `/${props.data.id}/generate-document`
  ep += `?company_code=${company_code}`
  if (downloadDocumentFilter.value.templateId) ep += `&template_id=${downloadDocumentFilter.value.templateId}`
  ep += `&export_type=${downloadDocumentFilter.value.exportType}`

  await API.get(
    ep,
    (status: number, _data: any, _message: string, response: any) => {
      if (status === 200) {
        const contentDisposition = response.headers['content-disposition']

        const blob = new Blob([response.data], { type: response.data.type })
        const link = document.createElement('a')

        const filenameMatch = contentDisposition && contentDisposition.match(/filename="?([^"]+)"?/)
        const filename = filenameMatch ? filenameMatch[1] : 'downloaded-file'

        link.href = URL.createObjectURL(blob)
        link.download = filename
        link.click()
        URL.revokeObjectURL(link.href)
      }
    },
    props.meta.app,
    'blob'
  )

  await getDocumentHistories()
}

// MOUNTED | COMPUTED | WATCHERS
onMounted(() => {
  init()
})
</script>
