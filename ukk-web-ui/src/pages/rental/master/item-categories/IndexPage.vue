<template>
  <div>
    <s-page :meta="Meta">
      <s-loading v-if="loading" />
      <s-table v-else :meta="Meta" :refresh="refresh"
        @add="add" @edit="edit" @detail="detail">
      </s-table>
    </s-page>

    <s-dialog v-model="dialog">
      <FormModal v-if="dialog.type === 'form'"
        :props="dialog.props"
        :meta="Meta"
        @refreshEvent="onRefresh" />

      <DetailModal v-else
        :props="dialog.props"
        :meta="Meta"
        @refreshEvent="onRefresh" />
    </s-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Handler } from 'src/services/handler'
import type { Dialog } from 'src/services/handler'
import { Meta } from './meta'
import FormModal from './FormPage.vue'
import DetailModal from './DetailPage.vue'

const dialog = ref<Dialog>({
  show: false,
  type: 'form',
  title: 'Form',
  props: null,
})

const loading = ref(true)
const refresh = ref(0)
const router = useRouter()

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

const add = () => showDialog('form', 'Add')
const edit = (data: any) => showDialog('form', 'Edit', data)
const detail = (data: any) => showDialog('detail', 'Detail', data)

onMounted(() => init())
</script>
