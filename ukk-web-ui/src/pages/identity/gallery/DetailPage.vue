<template>
  <div>
    <s-loading v-if="loading" />
    <h-detail v-else :meta="Meta" :modal="props.props" @back="back" :model="dataModel">
      <div class="row q-pa-sm">
        <f-card title="Detail" col="6">
          <s-list v-for="(value, index) in viewList" :key="index" :data="value" />
        </f-card>
        <f-card title="Log" col="6">
          <log-info :data="dataModel" />
        </f-card>
        <f-card title="File" col="12">
          Public Path:
          <s-link v-if="dataModel.is_public" :src="dataModel.public_path" class="q-my-sm" />
          <iframe v-if="iframes.content" :src="iframes.content" ref="iframe-content" frameborder="0" :class="$q.dark.isActive ? 'iframe-dark' : ''" style="height: 50vh; width: 100%" @load="adjustIframeHeight('iframe-content')"></iframe>
        </f-card>
      </div>
    </h-detail>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { useTemplateRef, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import type { DataModel } from './meta'
import { Meta } from './meta'

const props = defineProps<{ props?: { id?: string | number } }>()

const router = useRouter()
const API = new Api()

const loading = ref(true)
const dataModel = ref(Meta.model)
const viewList = ref<{ label: string; value: any }[]>([])

const iframes = ref({ content: <string | null>null })
const iframe_content = useTemplateRef('iframe-content')

// METHODS
const init = () => {
  dataModel.value = Helper.unreactive(Meta.model)
  Handler.permissions(router, 'read', Meta, (status, data) => {
    Meta.permission = data
    Meta.permission.delete = false
    Meta.permission.restore = false
    if (status) onRefresh()
  })
}

const onRefresh = () => {
  const id = props?.props?.id
  if (id) getData(id)
  else loading.value = false
}

const getData = (id: string | number) => {
  loading.value = true
  const endpoint = `${Meta.module}/${id}`
  API.get(endpoint, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      dataModel.value = data
      getFile(data)
      const config = {
        exclude: ['id', 'path', 'public_path', 'base_url'],
        numbers: [],
        moneys: [],
        date: [],
        dateTime: []
      }
      viewList.value = Handler.viewList(dataModel.value, config)
    }
  })
}

const getFile = async (data: DataModel) => {
  if (data.path) {
    const mode = data.is_public ? 'public' : 'private'
    const storage_id = data.storage_id
    let ep = `${Meta.module}/download?mode=${mode}&path=${data.path}`
    if (data.storage_id) ep += `&storage_id=${data.storage_id}`
    await API.get(
      ep,
      (status: number, _data: any, _message: string, response: any) => {
        if (status === 200) {
          const blob = new Blob([response.data], { type: data.filetype ?? '' })
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

const back = () => {
  // if (!props.props) router.back()
}

// MOUNTED | COMPUTED | WATCHERS
onMounted(() => {
  init()
})
</script>
