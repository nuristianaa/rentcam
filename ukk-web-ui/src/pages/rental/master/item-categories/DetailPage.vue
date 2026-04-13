<template>
  <div>
    <s-loading v-if="loading" />

    <h-detail v-else :meta="Meta" :modal="props.data"
      @back="back" :model="dataModel">

      <div class="row q-pa-sm">

        <f-card title="Detail" col="6">
          <s-list
            v-for="(value, index) in viewList"
            :key="index"
            :data="value"
          />
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
import { useRoute, useRouter } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Meta } from './meta'

const props = defineProps<{ props?: { id?: string | number }; data?: any }>()

const route = useRoute()
const router = useRouter()
const API = new Api()

const loading = ref(true)
const dataModel = ref(Meta.model)
const viewList = ref<any[]>([])

const init = () => {
  dataModel.value = Helper.unreactive(Meta.model)
  onRefresh()
}

const onRefresh = () => {
  const id: any = props?.props?.id ?? route?.params?.id
  if (id) getData(id)
  else loading.value = false
}

const getData = (id: string | number) => {
  API.get(`${Meta.module}/${id}`, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      dataModel.value = data?.data ?? data

      const config = {
        app: Meta.app,
        schema: Meta.schema,
        name: Meta.name,
        exclude: ['id', 'warehouse_id', 'item_id', 'project_id'],
      }

      viewList.value = Handler.viewList(dataModel.value, config)
    }
  })
}

const back = () => {
  if (!props.data) router.back()
}

onMounted(() => init())
</script>
