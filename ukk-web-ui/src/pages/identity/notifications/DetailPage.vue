<template>
  <div>
    <s-loading v-if="loading" />
    <h-detail v-else :meta="Meta" :modal="props.props" @back="back" :model="dataModel">
      <div class="row q-pa-lg">
        <div class="" style="width: 100%">
          <div class="row justify-between">
            <div class="title q-pt-sm">{{ dataModel.title }}</div>
            <q-icon v-if="dataModel.icon" size="md" :color="dataModel.color ?? undefined" text-color="white" :name="dataModel.icon" />
          </div>
          <q-separator class="q-my-md" color="primary" />
          <div class="row q-my-md">
            <div class="col" v-html="dataModel.description" />
          </div>
          <q-btn v-if="dataModel.path && dataModel.path != '/home'" class="q-my-md" color="primary" icon="open_in_new" label="View" :to="dataModel.path" />
          <log-info :data="dataModel" />
        </div>
      </div>
    </h-detail>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, onMounted } from 'vue'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Meta } from './meta'

const props = defineProps<{ props?: { id?: string | number } }>()

const API = new Api()

const loading = ref(true)
const dataModel = ref(Meta.model)
const viewList = ref<{ label: string; value: any }[]>([])

// METHODS
const init = () => {
  dataModel.value = Helper.unreactive(Meta.model)
  onRefresh()
}

const onRefresh = () => {
  const id = props?.props?.id
  if (id) getData(id)
  else loading.value = false
}

const getData = (id: string | number) => {
  loading.value = true
  const endpoint = `auth/notifications/${id}`
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
