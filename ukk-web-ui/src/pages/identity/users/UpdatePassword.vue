<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else :meta="Meta" @submit="submit" title="Change Password" @back="back">
      <div class="row q-pa-md">
        <f-input col="4" v-model="dataModel.current_password" label="Current Password" required />
        <f-input col="4" v-model="dataModel.password" label="Password" required />
      </div>
    </h-form>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { Meta } from './meta'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Helper } from 'src/services/helper'

const API = new Api()
const loading = ref(false)
const dataModel = ref(Meta.model)
const router = useRouter()

// METHODS
const init = () => {
  dataModel.value = Helper.unreactive(Meta.model)
  dataModel.value.current_password = null
  dataModel.value.password = null
}

const submit = async () => {
  if (validateSubmit()) {
    loading.value = true

    let status = 600
    status = await save()

    if (status === 200) {
      Helper.showSuccess('Data has been successfully saved.')
      back()
    }
    loading.value = false
  }
}

const validateSubmit = () => {
  let msg = ''

  const d = dataModel.value
  if (!d.current_password) msg += 'Current Password is required. '
  if (!d.password) msg += 'Password is required. '

  if (msg === '') return true
  else {
    Helper.showNotif(msg)
    return false
  }
}

const save = async () => {
  let statusapi = 600
  const model = {
    current_password: dataModel.value.current_password,
    password: dataModel.value.password
  }
  await API.put('me/change-password', model, (status: number) => {
    statusapi = status
  })
  return statusapi
}

const back = () => {
  router.back()
}

// MOUNTED | COMPUTED | WATHERS
onMounted(() => {
  init()
})
</script>
