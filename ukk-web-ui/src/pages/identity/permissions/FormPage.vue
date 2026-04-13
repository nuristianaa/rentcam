<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else @submit="submit" :meta="Meta" :modal="props" @back="back">
      <div class="row q-px-lg">
        <f-input v-model="dataModel.name" col="6" label="Name" required />
        <f-input v-model="dataModel.app" col="6" label="App" />
      </div>
    </h-form>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Meta } from './meta'
import type { DataModel } from './meta'

const props = defineProps<{ props?: { id?: string | number } }>()
const emit = defineEmits(['refreshEvent'])

const router = useRouter()
const API = new Api()

const loading = ref(true)
const dataModel = ref<DataModel>(Meta.model)

// METHODS
const init = () => {
  dataModel.value = Helper.unreactive(Meta.model)
  const action = props.props?.id ? 'update' : 'create'
  Handler.permissions(router, action, Meta, (status: boolean, data: any) => {
    Meta.permission = data
    if (status) {
      if (props.props?.id) getData(props.props?.id)
      else onRefresh()
    }
  })
}

const onRefresh = () => {
  loading.value = false
}

const getData = (id: string | number) => {
  loading.value = true
  const endpoint = `${Meta.module}/${id}`
  API.get(endpoint, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      dataModel.value = data
    }
  })
}

const submit = async () => {
  if (validateSubmit()) {
    loading.value = true

    let status = 600
    if (dataModel.value.id) status = await update()
    else status = await save()

    if (status === 200) {
      Helper.showSuccess('Data has been successfully saved.')
      back()
    }
    loading.value = false
  }
}

const validateSubmit = () => {
  let msg = ''
  // Validations
  const apps = ['identity', 'crm', 'engineering', 'finance', 'hris', 'procurement', 'project_management']
  if (dataModel.value.app == null) msg += 'App cannot be null'
  else if (!apps.includes(dataModel.value.app)) msg += 'App must between identity, crm, engineering, finance, hris, procurement, project_management'

  if (msg === '') return true
  else {
    Helper.showNotif(msg)
    return false
  }
}

const save = async () => {
  let statusapi = 600
  await API.post(Meta.module, dataModel.value, (status: number, _data: any) => {
    statusapi = status
  })
  return statusapi
}

const update = async () => {
  let statusapi = 600
  await API.put(`${Meta.module}/${dataModel.value.id}`, dataModel.value, (status: number, _data: any) => {
    statusapi = status
  })
  return statusapi
}

const back = () => {
  emit('refreshEvent')
}

// MOUNTED | COMPUTED | WATHERS
onMounted(() => {
  init()
})
</script>
