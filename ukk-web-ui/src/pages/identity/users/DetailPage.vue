<template>
  <div>
    <s-loading v-if="loading" />
    <h-detail v-else :meta="Meta" :modal="props" @back="back" :model="dataModel">
      <div class="row q-pa-sm">
        <f-card title="Picture" col="4">
          <q-img :src="oldFile ?? ''" :ratio="1" />
        </f-card>
        <f-card title="Detail" col="8">
          <s-list v-for="(value, index) in viewList" :key="index" :data="value" class="scroll" />
          <!-- <q-btn v-if="dataModel.unsync" size="sm" color="red" icon="priority_high" label="Sync Data" class="q-my-sm" @click="popupSync(dataModel, 'sync')" /> -->
        </f-card>
        <f-card title="Log" col="12">
          <log-info :data="dataModel" />
        </f-card>
      </div>
    </h-detail>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Api from 'src/services/api'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Meta } from './meta'

const props = defineProps<{ props?: { id?: string | number } }>()

const router = useRouter()
const API = new Api()

const loading = ref(true)
const dataModel = ref(Meta.model)
const viewList = ref<{ label: string; value: any }[]>([])
const oldFile = ref<string | null>(null)
const oldFileSign = ref<string | null>(null)
const oldFileSignWithSignature = ref<string | null>(null)

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
  if (id) {
    getData(id)
  } else loading.value = false
}

const getData = (id: string | number) => {
  loading.value = true
  const endpoint = `${Meta.module}/${id}`
  API.get(endpoint, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      if (data.roles) data.role_names = data.roles.map((role: any) => role.name).join(', ')
      dataModel.value = data
      const config = {
        app: 'user',
        schema: 'auth',
        name: 'User',
        exclude: ['id', 'profile_picture', 'table_configs', 'dashboards', 'menu_id', 'role_id', 'signatures', 'storage_id', 'storage_signatures', 'menu_favorites', 'roles'],
        float: [],
        integer: [],
        date: ['birthday'],
        datetime: ['activated_at'],
        constant: [],
        money: [],
        detail: ['role', 'menu']
      }
      viewList.value = Handler.viewList(dataModel.value, config)

      if (data.profile_picture) oldFile.value = Helper.viewBlobFile(data.profile_picture, false, data.storage_id)
      if (data.signatures) oldFileSign.value = Helper.viewBlobFile(data.signatures.default, false, data.storage_signatures.default)
      if (data.signatures) oldFileSignWithSignature.value = Helper.viewBlobFile(data.signatures.with_stamp, false, data.storage_signatures.default)
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
