<template>
  <div>
    <r-table :meta="Meta" :columns="Meta.table(Helper, Constant, Lang)" v-model="dataModel" :selected="selectedData" @selected="selectedFunc" selection>
      <template #top-right>
        <div class="flex q-gutter-sm">
          <q-btn v-if="Meta.permission.delete && selectedData && selectedData.length" :color="'negative'" :icon="'delete'" :label="'Delete'" @click="deleteSelected" />
          <q-btn v-if="Meta.permission.create"  color="primary" icon="add" label="Add" @click="add" />
        </div>
      </template>
      <template v-slot:body-cell-action="prp">
        <q-btn v-if="Meta.permission.update" class="bg-soft" dense round flat :color="Constant.editColor()" @click="edit(prp.props.row)" icon="visibility">
          <q-tooltip>View</q-tooltip>
        </q-btn>
        <q-btn v-if="Meta.permission.update" class="bg-soft" dense round flat @click="masterFiles(prp.props.row)" color="primary" icon="upload">
          <q-tooltip>Upload Files</q-tooltip>
        </q-btn>
      </template>
      <template v-slot:body-cell-updated_at="prp">
          <log-info table :data="prp.props.row" />
        </template>
    </r-table>

    <s-dialog v-model="dialog">
      <f-files v-if="dialog.type == 'master-files'" :data="dialog.props" :meta="Meta" @refreshEvent="onRefresh" :per-reference-id="true" :identifiers="dialog.props" />
      <FormModal v-else-if="dialog.type == 'form'" :props="dialog.props" :meta="Meta" @refreshEvent="onRefresh" :module_data="props.module_data" :module_meta="props.module_meta" />
    </s-dialog>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Meta } from './meta'
import type { DataModel } from './meta'
import { Lang } from 'src/services/lang';
import { Constant } from 'src/services/constant';
import { Helper } from 'src/services/helper';
import FormModal from './TaskForm.vue'

const props = defineProps<{
  module_data?: any // { id: string | number; code?: string }
  module_meta?: any // { app: string; module: string; title?: string }
}>()

interface Dialog {
  [props: string]: any
  show: boolean
  title?: string
  width?: string
  maximize?: boolean
  persistent?: boolean
}

const dialog = ref<Dialog>({
  show: false,
  type: 'form',
  title: 'Form',
  props: null,
  maximize: false,
  persistent: false
})
const loading = ref(true)
const refresh = ref(0)
const router = useRouter()
const API = new Api()
const dataModel= ref<DataModel[]>([])
const selectedData = ref<any>([])

// METHODS
const init = () => {
  console.log(props)
  onRefresh()
}

const getData = () => {
  const endpoint = `${Meta.module}?limit=0&where=ref_module:${props.module_meta.module}&where=ref_id:${props.module_data.id}&where=app:${props.module_meta.app}`
  API.get(endpoint, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      dataModel.value = data
    }
  })
}

const onRefresh = () => {
  getData()
  dialog.value.show = false
  dialog.value.props = null
}

const showDialog = (type: string, title: string, data: any = null) => {
  dialog.value.type = type
  dialog.value.title = `${title} | ${Meta.title}`
  dialog.value.show = true
  dialog.value.props = data
}

const add = () => {
  showDialog('form', 'Add')
}

const edit = (data: any) => {
  showDialog('form', 'Edit', data)
}

const masterFiles = (data: any) => {
  showDialog('master-files', 'Master Files', data)
}

const selectedFunc = (d:any) => {
  selectedData.value = d
}

// Delete or Restore Selected Data
const deleteSelected = () => {
  const type = 'delete'
  const msg = `Are you sure want to ${type} (${selectedData.value.length}) selected data  ?`
  Helper.confirm(msg, (result: boolean) => {
    if (result) deleteDataSelected(type)
  })
}

const deleteDataSelected = async (type: string) => {
  const app = Meta.app ?? ''

  Helper.loadingOverlay()
  const ids = []
  for (const row of selectedData.value) {
    ids.push(row.id)
  }
  const ep = `${Meta.module}/delete`
  const request = {
    id: ids
  }
  await API.delete(
    ep,
    request,
    (status: number, _data: any, message: string) => {
      if (status === 200) Helper.showToast(message)
    },
    app
  )
  selectedData.value = []
  Helper.loadingOverlay(false)
  onRefresh()
}

// MOUNTED | COMPUTED | WATCHERS
onMounted(() => {
  init()
})
</script>
