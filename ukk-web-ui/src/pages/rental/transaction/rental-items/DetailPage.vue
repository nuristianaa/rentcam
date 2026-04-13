<template>
  <div>
    <s-loading v-if="loading" />
    <h-detail v-else :meta="Meta" :model="dataModel" @back="back">
      <div class="row q-pa-sm">
        <f-card title="Detail" col="6">
          <s-list v-for="(item, i) in viewList" :key="i" :data="item" />
        </f-card>
        <f-card title="Log" col="6">
          <log-info :data="dataModel" />
        </f-card>
        <f-card v-if="dataModel.images && Object.keys(dataModel.images).length > 0" title="Images" col="12">
          <f-image-viewer :images="dataModel.images" />
        </f-card>
      </div>
    </h-detail>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Api from 'src/services/api'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Meta } from './meta'

const route = useRoute()
const router = useRouter()
const id = Array.isArray(route.params?.id) ? route.params.id[0] : (route.params?.id ?? null)
const API = new Api()

const loading = ref(true)
const dataModel = ref<any>({})
const viewList = ref<{ label: string; value: any }[]>([])

const init = () => {
  dataModel.value = Helper.unreactive(Meta.model)
  Handler.permissions(router, 'read', Meta, (status) => {
    if (status) getData(id)
  })
}

const getData = (id?: string | number) => {
  if (!id) return (loading.value = false)

  API.get(`${Meta.module}/${id}`, (status: number, data: any) => {
    if (status === 200) {
      const payload = data?.data ?? data ?? {}
      dataModel.value = { ...payload }
      const config = {
        exclude: ['id', 'images', 'created_by', 'updated_by', 'deleted_by', 'created_at', 'updated_at', 'deleted_at'],
        numbers: [],
        moneys: [],
        date: [],
        dateTime: []
      }
      viewList.value = Handler.viewList(dataModel.value, config)
    }
    loading.value = false
  })
}

const back = () => {
  router.back()
}

onMounted(init)
</script>