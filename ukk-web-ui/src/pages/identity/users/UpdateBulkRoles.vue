<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else @submit="submit" :meta="Meta" :modal="dataModel" @back="back">
      <div class="row">
        <f-select col="6" v-model="role_ids" label="Role" api="auth/roles" must-fill multiple />
        <f-select col="6" v-model="user_ids" label="User" api="auth/users?in_=is_active:True" must-fill multiple />
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
import { Lang } from 'src/services/lang'
import type { DataModel, Company } from './meta'
import { Meta } from './meta'

const props = defineProps<{ props?: { id?: string | number } }>()
const emit = defineEmits(['refreshEvent'])

const role_ids = ref([])
const user_ids = ref([])

const router = useRouter()
const API = new Api()

const loading = ref(true)
const dataModel = ref<DataModel>(Meta.model)
const avatar = ref<any>(null)

const opt = ref<any>({
  companies: [],
  vendors: [],
  user_type: []
})

// METHODS
const init = () => {
  Handler.permissions(router, 'browse', Meta, (status, data) => {
    Meta.permission = data
    if (status) onRefresh()
  })
}

const onRefresh = () => {
  loading.value = false
}

const submit = async () => {
  if (validateSubmit()) {
    loading.value = true

    let status = 600
    // Handle File
    status = await save()

    if (status === 200) {
      Helper.showSuccess('Data has been successfully saved.')
      back()
    }
    loading.value = false
  }
}

const save = async () => {
  let statusapi = 600
  const payload = { role_ids: role_ids.value }
  statusapi = 400

  if (role_ids.value.length > 0 && user_ids.value.length > 0) {
    Helper.loadingOverlay(true, 'Process saving data...')
    for (let i = 0; i < user_ids.value.length; i++) {
      Helper.loadingOverlay(true, `Process saving ${i + 1} of ${user_ids.value.length}...`)
      const ep = `${Meta.module}/${user_ids.value[i]}`
      await API.put(ep, payload, (status: number) => {
        if (status === 200) statusapi = status
      })
    }
    Helper.loadingOverlay(false)
    onRefresh()
  }

  return statusapi
}

const validateSubmit = () => {
  const msg = ''

  if (msg === '') return true
  else {
    Helper.showNotif(msg)
    return false
  }
}

const back = () => {
  emit('refreshEvent')
}

// MOUNTED | COMPUTED | WATHERS
onMounted(() => {
  init()
})
</script>
