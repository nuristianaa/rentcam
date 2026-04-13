<template>
  <div>
    <s-page :meta="Meta">
      <s-loading v-if="loading" />
      <s-table
        v-else
        :meta="Meta"
        :refresh="refresh"
        @add="add"
        @edit="edit"
        @detail="detail"
      >
        <template v-slot:top-buttons>
           <q-btn class="bg-primary text-white q-mr-sm" dense flat @click="$router.push('/rental/transaction/reports')" icon="print" label="Laporan Transaksi" />
        </template>
        <template v-slot:body-action="props">
          <q-btn v-if="Meta.permission.update" class="bg-soft" dense round flat @click="masterFiles(props.props.row)" color="primary" icon="upload">
            <q-tooltip>Upload Files</q-tooltip>
          </q-btn> -->
        </template>
      </s-table>
    </s-page>

    <s-dialog v-model="dialog">
      <f-files v-if="dialog.type == 'master-files'" :data="dialog.props" :meta="Meta" @refreshEvent="onRefresh" :per-reference-id="true" :identifiers="dialog.props" :upload-url="`${Meta.module}/upload-files`" />
    </s-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Meta } from './meta'

interface Dialog {
  [props: string]: any
  show: boolean
  title?: string
  width?: string
  maximize?: boolean
  persistent?: boolean
}

const router = useRouter()
const route = useRoute()
const loading = ref(true)
const refresh = ref(0)

const dialog = ref<Dialog>({
  show: false,
  type: '',
  title: '',
  props: null,
  maximize: false,
  persistent: false
})

const init = () => {
  Handler.permissions(router, 'browse', Meta, (status, data) => {
    Meta.permission = data
    if (status) loading.value = false
  })
}

const onRefresh = () => {
  refresh.value++
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
  router.push({
    name: `add-${Meta.module}`,
    query: route.query
  })
}

const edit = (data: any) => {
  router.push({
    name: `edit-${Meta.module}`,
    params: { id: data.id },
    query: route.query
  })
}

const detail = (data: any) => {
  router.push({
    name: `view-${Meta.module}`,
    params: { id: data.id },
    query: route.query
  })
}

const masterFiles = (data: any) => {
  showDialog('master-files', 'Master Files', data)
}

onMounted(init)
</script>