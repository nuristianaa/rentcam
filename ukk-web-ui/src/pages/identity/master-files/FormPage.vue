<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else @submit="submit" :meta="Meta" :modal="props" @back="back">
      <div class="row q-px-lg">
        <f-input col="4" v-model="dataModel.app" label="App" />
        <f-input col="4" v-model="dataModel.name" label="Name" />
        <f-input col="4" v-model="dataModel.description" label="Description" />
        <f-input col="4" v-model="dataModel.module" label="Module" />
        <f-input col="4" v-model="dataModel.reference_code" label="Reference Code" />
        <f-input col="4" v-model="dataModel.reference_id" label="Reference Id" />
        <f-toggle col="4" v-model="dataModel.is_public" label="Is Public?" />
        <f-uploader boxClass="col-12 col-md-6 q-pa-sm" v-model="dataModel.file" :oldFile="dataModel.public_path" />
        <div class="col-12">
          <div class="text-h3 q-pb-sm">Old File</div>
          <iframe v-if="iframes.content" :src="iframes.content" ref="iframe-content" frameborder="0" :class="$q.dark.isActive ? 'iframe-dark' : ''" style="height: 50vh; width: 100%" @load="adjustIframeHeight('iframe-content')"></iframe>
        </div>
      </div>
    </h-form>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { useTemplateRef, ref, onMounted } from 'vue'
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

const iframes = ref({ content: <string | null>null })
const iframe_content = useTemplateRef('iframe-content')

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

const getData = async (id: string | number) => {
  loading.value = true
  const endpoint = `${Meta.module}/${id}`
  await API.get(endpoint, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      dataModel.value = data
      getFile(data)
    }
  })
  if (dataModel.value.path) {
    dataModel.value.public_path = await Helper.blobFile(dataModel.value.path, dataModel.value.is_public, dataModel.value.storage_id)
  }
}

const submit = async () => {
  if (validateSubmit()) {
    loading.value = true

    const status = await save()
    // if (dataModel.value.id) status = await update()
    // else status = await save()

    if (status === 200) {
      Helper.showSuccess('Data has been successfully saved.')
      back()
    }
    loading.value = false
  }
}

const validateSubmit = () => {
  const msg = ''
  // Validations

  if (msg === '') return true
  else {
    Helper.showNotif(msg)
    return false
  }
}

const save = async () => {
  let status = 600
  await Handler.storeFile(dataModel.value, (data: any, _message: any) => {
    if (data) status = 200
  })
  return status
}

const getFile = async (data: DataModel) => {
  if (data.path) {
    let ep = `${Meta.module}/download?path=${data.path}`
    if (data.is_public) ep += '&mode=public'
    if (data.storage_id) ep += `&storage_id=${data.storage_id}`
    await API.get(
      ep,
      (status: number, _data: any, _message: string, response: any) => {
        if (status === 200) {
          const blob = new Blob([response.data], { type: data.filetype as any })
          iframes.value.content = URL.createObjectURL(blob)
        }
      },
      'main',
      'blob'
    )
  }
}

const adjustIframeHeight = (slug: string) => {
  let iframe = iframe_content.value
  if (slug == 'iframe-content') iframe = iframe_content.value
  if (iframe && iframe.contentWindow?.document) {
    const contentHeight = iframe.contentWindow.document.body.scrollHeight
    const height = contentHeight + 50
    iframe.style.height = `${height}px`
  }
}
// const update = async () => {
//   let statusapi = 600
//   await API.put(`${Meta.module}/${dataModel.value.id}`, dataModel.value, (status: number, _data: any) => {
//     statusapi = status
//   })
//   return statusapi
// }

const back = () => {
  emit('refreshEvent')
}

// MOUNTED | COMPUTED | WATHERS
onMounted(() => {
  init()
})
</script>
