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
      </div>
    </h-detail>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Meta } from './meta'

const props = defineProps<{ props?: { id?: string | number } }>()

const router = useRouter()
const API = new Api()

const loading = ref(true)
const dataModel = ref(Meta.model)
const viewList = ref<{ label: string; value: any }[]>([])

// METHODS
const init = () => {
  dataModel.value = Helper.unreactive(Meta.model)
  Handler.permissions(router, 'read', Meta, (status, data) => {
    Meta.permission = data
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
      const config = {
        exclude: ['id'],
        numbers: [],
        moneys: [],
        date: [],
        dateTime: []
      }
      viewList.value = Handler.viewList(dataModel.value, config)
    }
  })
}

const back = () => {
  // if (!props.props) router.back()
}

// MOUNTED | COMPUTED | WATCHERS
onMounted(() => {
  init()
})
</script>
