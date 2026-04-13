<template>
  <div>
    <s-page :meta="Meta">
      <s-loading v-if="loading" />
      <s-table v-else :meta="Meta" :refresh="refresh" @add="add" @edit="edit" @detail="detail">
        <template v-slot:top-buttons>
          <q-btn v-if="Meta.permission.create"  outline color="primary" icon="attachment" label="Import Excel" @click="importExcel()" />
        </template>
        <template v-slot:body-action="{ props, isTrash }">
        </template>
      </s-table>
    </s-page>

    <s-dialog v-model="dialog">
      <FormModal v-if="dialog.type == 'form'" :props="dialog.props" :meta="Meta" @refreshEvent="onRefresh" />
      <ImportExcel v-else-if="dialog.type == 'import'" :props="dialog.props" :meta="Meta" @refreshEvent="onRefresh" />
      <DetailModal v-else :props="dialog.props" :meta="Meta" @refreshEvent="onRefresh" />
    </s-dialog>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Meta } from './meta'
import FormModal from './FormPage.vue'
import DetailModal from './DetailPage.vue'
import ImportExcel from './ImportExcel.vue'
import { Helper } from 'src/services/helper'

const API = new Api()

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
  maximize: true,
  persistent: false
})
const loading = ref(true)
const refresh = ref(0)
const router = useRouter()

// METHODS
const init = () => {
  Handler.permissions(router, 'browse', Meta, (status, data) => {
    Meta.permission = data
    if (status) loading.value = false
  })
}

const onRefresh = () => {
  refresh.value += 1
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

const detail = (data: any) => {
  showDialog('detail', 'Detail', data)
}

const importExcel = () => {
  showDialog('import', 'Import Excel')
}

const copy = (row: any) => {
  Helper.confirm('Would you like to copy this data?', (result: boolean) => {
    if (result) {
      loading.value = true
      API.get(Meta.module + '/' + row.id, (status: number, data: any) => {
        if (status === 200) {
          const send = Helper.unreactive(data)
          send.id = null
          send.name = `${send.name}-COPY`
          API.post(Meta.module, send, (status: number) => {
            loading.value = false
            if (status === 200) {
              Helper.showSuccess('Data Cloned!')
              onRefresh()
            }
          })
        } else loading.value = false
      }) // end fetch
    } // result
  })
}

// MOUNTED | COMPUTED | WATCHERS
onMounted(() => {
  init()
})
</script>
