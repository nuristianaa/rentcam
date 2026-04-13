<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else @submit="submit" :meta="Meta" :modal="dataModel" @back="back">
      <div class="row">
        <div class="col-12 q-pa-sm">
          <div class="form-title">Informasi Kategori</div>
        </div>
        <f-input    col="12" v-model="dataModel.name"        label="Nama Kategori" required />
        <f-textarea col="12" v-model="dataModel.description" label="Deskripsi" />
        <f-toggle   col="6"  v-model="dataModel.is_active"   label="Status Aktif" active-mode />
      </div>
    </h-form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Api from 'src/services/api'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import type { DataModel } from './meta'
import { Meta } from './meta'

const props = defineProps<{ props?: { id?: string | number } }>()
const emit = defineEmits(['refreshEvent'])

const router = useRouter()
const API = new Api()

const loading = ref(true)
const dataModel = ref<DataModel>(Meta.model)

const init = () => {
  dataModel.value = Helper.unreactive(Meta.model)
  const action = props.props?.id ? 'update' : 'create'
  Handler.permissions(router, action, Meta, (status: boolean, data: any) => {
    Meta.permission = data
    if (status) {
      if (props.props?.id) getData(props.props.id)
      else loading.value = false
    }
  })
}

const getData = (id: string | number) => {
  loading.value = true
  API.get(`${Meta.module}/${id}`, (status: number, data: any) => {
    loading.value = false
    if (status === 200) dataModel.value = data
  })
}

const submit = async () => {
  if (validateSubmit()) {
    loading.value = true
    let status = 600
    if (dataModel.value.id) status = await update()
    else status = await save()
    if (status === 200) {
      Helper.showSuccess('Data berhasil disimpan.')
      back()
    }
    loading.value = false
  }
}

const validateSubmit = () => {
  if (!dataModel.value.name) {
    Helper.showNotif('Nama kategori wajib diisi.')
    return false
  }
  return true
}

const save = async () => {
  let statusapi = 600
  await API.post(Meta.module, dataModel.value, (status: number, data: any) => {
    statusapi = status
    dataModel.value.id = data.id
  })
  return statusapi
}

const update = async () => {
  let statusapi = 600
  await API.put(`${Meta.module}/${dataModel.value.id}`, dataModel.value, (status: number) => {
    statusapi = status
  })
  return statusapi
}

const back = () => emit('refreshEvent')

onMounted(() => init())
</script>