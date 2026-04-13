<template>
  <q-layout view="hhh lpR fFf" class="body">
    <q-page-container>
      <s-loading v-if="loading" />
      <div v-else>
        <q-btn class="q-ma-lg" color="primary" unelevated to="/" label="Go Home" no-caps />
        <div class="row q-px-md">
          <f-card :title="dataModel.title" col="8">
            <div class="row q-pa-md">
              <q-avatar size="lg" class="q-pb-sm" :color="dataModel.type == 'success' || 'green' ? 'positive' : dataModel.type" text-color="white" :icon="dataModel.type == 'success' || 'green' ? 'check' : dataModel.type ? dataModel.type : 'info'" />
              <div class="col q-px-md" v-html="dataModel.description" />
            </div>
          </f-card>
          <f-card title="Log Info" col="4">
            <log-info :data="dataModel" />
          </f-card>
        </div>
      </div>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const API = new Api()
const route = useRoute()
const loading = ref(true)
const dataModel = ref({
  title: null,
  type: '',
  description: null
})

const id = Array.isArray(route.params?.id) ? route.params.id[0] : (route.params?.id ?? null)
if (id) {
  void API.get(`user-notifications/${id}/read`, (status: number, data: any) => {
    loading.value = false
    if (status == 200) dataModel.value = data
  })
}
</script>
