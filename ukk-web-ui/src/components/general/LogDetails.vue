<template>
  <div :class="col ? 'col-' + col : ''">
    <s-loading skeleton v-if="loading && !table" />
    <div v-else>
      <f-card row title="Last 10 Data Logs">
        <div class="col-12 q-px-sm">
          <q-table :grid="$q.screen.gt.sm ? false : true" bordered flat binary-state-sort row-key="id" :rows="table.data" :columns="table.columns" :rows-per-page-options="[0]" :filter="table.search" dense>
            <template v-slot:loading><loading-table /></template>
            <!-- GRID STYLES -->
            <template v-slot:item="props">
              <div class="q-pa-xs col-xs-12 col-sm-6 col-md-4">
                <q-card flat bordered>
                  <q-card-section class="text-center">
                    <span>
                      <q-chip size="sm">
                        <q-avatar icon="person" :color="defineColorByType(props.row.type)" text-color="white" />
                        {{ props.row.type }} |
                        {{ Helper.readDate(props.row.created_at, true) }}
                      </q-chip>
                    </span>
                  </q-card-section>
                  <q-separator />
                  <q-card-section class="flex flex-center">
                    <div clickable>
                      {{ props.row.name }}
                      <q-btn dense flat size="xs" icon="info" color="info" label="Detail" @click="getDetail(props.row.data_id)">
                        <q-popup-proxy v-if="props.row.data_id">
                          <f-card col="12">
                            <s-list v-for="(value, index) in viewList(dataDetail)" :key="index" :data="value" />
                          </f-card>
                        </q-popup-proxy>
                      </q-btn>
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </template>

            <!-- TABLE STYLES -->
            <template v-slot:body-cell-type="props">
              <div>
                <q-btn dense size="xs" :label="props.value" :color="defineColorByType(props.value)" @click="getDetail(props.row.data_id)">
                  <q-popup-proxy v-if="props.row.data_id">
                    <f-card col="12">
                      <s-list v-for="(value, index) in viewList(dataDetail)" :key="index" :data="value" />
                    </f-card>
                  </q-popup-proxy>
                </q-btn>
              </div>
            </template>
          </q-table>
        </div>
      </f-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { Helper } from 'src/services/helper'
import { ref, onMounted } from 'vue'

const props = defineProps<{
  col?: number | string
  data: { id: number }
  module: string
  app: string
}>()

interface Table {
  data: any[]
  columns: any[]
  search: string | null
}

const API = new Api()
const loading = ref(true)
const dataDetail = ref({})
const table = <{ data: any[]; columns: any[]; search: string | null }>{
  data: [],
  columns: [
    { align: 'left', name: 'type', label: 'type', field: 'type' },
    { align: 'left', name: 'username', label: 'changed by', field: 'username' },
    { align: 'left', formatter: 'datetime', name: 'created_at', label: 'date', field: 'created_at', is_date: true, datetime: true, millis: true },
    { align: 'left', name: 'app', label: 'app', field: 'app' },
    { align: 'left', name: 'name', label: 'name', field: 'name' }
  ],
  search: null
}

const getList = () => {
  loading.value = true
  let endpoint = 'audit-trails?table=true'
  endpoint += `&where=app:${props.app}`
  endpoint += `&where=module:${props.module}`
  endpoint += `&where=module_id:${props.data.id}`
  endpoint += '&limit=10'
  endpoint += '&order=id:desc'
  API.get(
    endpoint,
    (status: number, data: any[]) => {
      loading.value = false
      if (status === 200) table.data = data
    },
    'main'
  )
}

function viewList(data: Record<string, any>) {
  return Object.keys(data)
    .sort()
    .map((key) => ({
      label: key,
      value: data[key]
    }))
}

const getDetail = (data_id: string) => {
  if (data_id) {
    API.get(
      `audit-trails/${data_id}`,
      (status: number, data: any) => {
        if (status === 200) dataDetail.value = data
      },
      'main'
    )
  }
}

const defineColorByType = (name: string | null) => {
  if (name == 'create') return 'positive'
  else if (name == 'update') return 'info'
  else if (name == 'delete') return 'negative'
  else if (name == 'restore') return 'orange'
}

onMounted(getList)
</script>
