<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else :meta="Meta" title="Edit Profile" @back="back" @submit="submit">
      <div class="row q-pa-lg">
        <f-input col="4" v-model="dataModel.name" label="name" required />
        <f-input col="4" v-model="dataModel.phone" label="mobile phone" />
        <!-- <f-select col="4" v-model="dataModel.gender" label="gender" :options="$Constant.gender" /> -->
        <!-- <f-input col="4" v-model="dataModel.birth_place" label="birth place" /> -->
        <f-date col="4" v-model="dataModel.birthday" label="birth date" />
        <!-- <f-input col="4" v-model="dataModel.religion" label="religion" /> -->
        <f-textarea col="12" v-model="dataModel.location" label="address" />

        <div class="col-12 col-md-4 q-px-sm">
          <f-uploader label="Foto KTP" type="image" v-model="ktp" :old-file="oldFile" />
        </div>
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

const router = useRouter()
const API = new Api()
const loading = ref(false)
const dataModel = ref(Meta.model)
const ktp = ref<any>(null)
const oldFile = ref<string | null>(null)

// METHODS
const init = () => {
  dataModel.value = Helper.unreactive(Meta.model)
  getData()
}

const getData = async () => {
  loading.value = true
  await API.get(
    'me',
    (status: number, data: any) => {
      loading.value = false
      if (status === 200) {
        dataModel.value = data
        if (data.profile_picture) oldFile.value = Helper.viewBlobFile(data.profile_picture, false, data.storage_id)
      }
    },
    'identity'
  )
}

const submit = async () => {
  if (validateSubmit()) {
    loading.value = true

    let status = 600
    status = await save()
    status = await checkUploadFile(dataModel.value)

    if (status === 200) {
      Helper.showSuccess('Data has been successfully saved.')
      back()
    }
    loading.value = false
  }
}

const validateSubmit = () => {
  const msg = ''
  if (msg === '') return true
  else {
    Helper.showNotif(msg)
    return false
  }
}

const save = async () => {
  let statusapi = 600
  await API.put(
    'me/update',
    dataModel.value,
    (status: number, data: any) => {
      statusapi = status
    },
    'identity'
  )
  return statusapi
}

const checkUploadFile = async (data: any) => {
  let statusapi = 200
  if (ktp.value && data.id) {
    const model = new FormData()
    model.append('file', ktp.value)
    await API.post(
      'me/change-picture',
      model,
      (status: number) => {
        statusapi = status
      },
      'identity',
      true
    )
  }
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
