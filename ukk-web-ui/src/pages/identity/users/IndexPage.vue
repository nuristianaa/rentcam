<template>
  <div>
    <s-page :meta="Meta">
      <s-loading v-if="loading" />
      <s-table v-else :meta="Meta" :refresh="refresh" @add="add" @edit="edit" @detail="detail" @onRefresh="onRefresh">
        <template v-slot:top-buttons>
          <q-btn color="primary" dense icon="group" label="Update User Role"  @click="updateBulkRoles()" style="width: 140px; padding: 5px" />
        </template>
        <template v-slot:header-action>
          <span class="bg-yellow-3">
            Action
            <q-tooltip>Custom Slot</q-tooltip>
          </span>
        </template>
        <template v-slot:body-action="ps">
          <q-btn v-if="Meta.permission.update" class="bg-soft" dense round flat color="secondary" @click="changePass(ps.props.row)" icon="lock">
            <q-tooltip>Change Password</q-tooltip>
          </q-btn>
        </template>
        <template v-slot:body-cell-updated_at="ps">
          <log-info :data="ps.props.row" table />
        </template>
      </s-table>
    </s-page>

    <s-dialog v-model="dialog" @hide="onRefresh">
      <FormModal v-if="dialog.type == 'form'" :props="dialog.props" :meta="Meta" @refreshEvent="onRefresh" />
      <UpdateBulkRoles v-else-if="dialog.type == 'update-bulk-roles'" :data="dialog.props" :meta="Meta" @refreshEvent="onRefresh" />
      <DetailModal v-else :props="dialog.props" :meta="Meta" @refreshEvent="onRefresh" />
    </s-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Api from 'src/services/api'
import { useRouter } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Meta } from './meta'
import FormModal from './FormPage.vue'
import DetailModal from './DetailPage.vue'
import UpdateBulkRoles from './UpdateBulkRoles.vue'

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
const API = new Api()
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
  dialog.value.title = `${title} | ${(Meta as any).tab}`
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

const updateBulkRoles = () => {
  showDialog('update-bulk-roles', 'Update User Role')
  dialog.value.maximize = false
}

const changePass = (row: any) => {
  const prompt = {
    model: 'default123@sdf',
    type: 'text' // optional
  }
  Helper.confirm(
    'Change Password. Enter new password!',
    (result: boolean, data: any) => {
      if (result) {
        const req = { password: data }
        const ep = `${Meta.module}/${row.id}/reset-password`
        API.put(ep, req, (status: number, _data: any) => {
          if (status == 200) Helper.showSuccess('Password changed!')
        })
      }
    },
    undefined,
    prompt
  )
}

// MOUNTED | COMPUTED | WATCHERS
onMounted(() => {
  init()
})
</script>
