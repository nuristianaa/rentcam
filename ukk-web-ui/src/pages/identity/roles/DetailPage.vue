<template>
  <div>
    <s-loading v-if="loading" />
    <h-detail v-else :meta="Meta" :modal="props" @back="back" :model="dataModel">
      <div class="row q-pa-sm">
        <div class="col-12 col-md-6 q-pa-md">
          <s-list v-for="(value, index) in viewList" :key="index" :data="value" />
        </div>
        <div class="col-12 col-md-6 q-pa-md">
          <log-info :data="dataModel" />
        </div>
        <div class="col-12 row">
          <s-title>Assigned Users</s-title>
          <div class="q-pa-sm" style="width: 100%">
            <q-table flat dense no-border class="no-border sticky-table" style="width: 100%" :rows="table_users.data" :columns="table_users.columns" :rows-per-page-options="[5]" :filter="table_users.filter">
              <template v-slot:header-cell-app="prp">
                <th colspan="2">
                  <q-th :props="prp">App & Name</q-th>
                  <q-input class="form-sm" v-model="table_users.filter" outlined dense>
                    <template #append>
                      <q-icon size="xs" name="search" />
                    </template>
                  </q-input>
                </th>
              </template>
            </q-table>
          </div>
        </div>

        <div class="col-12 row">
          <s-title>Permissions List</s-title>
          <div class="q-pa-sm" style="width: 100%">
            <q-table flat dense no-border class="no-border sticky-table" style="width: 100%" :rows="table.data" :columns="table.columns" :rows-per-page-options="[0]" :style="'width: 100%; height: ' + (Constant.tableHeight() - 400) + 'px;'">
              <template v-for="v in Object.keys(features)" :key="v" v-slot:[`body-cell-${v}`]="props">
                <q-td class="text-center">
                  <q-checkbox dense :model-value="props.row[v]" disable />
                </q-td>
              </template>
              <template v-slot:body-cell-others="props">
                <q-td class="text-center">
                  {{ props?.value?.join(', ') }}
                </q-td>
              </template>
            </q-table>
          </div>
        </div>
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
import { Constant } from 'src/services/constant'
import { Meta } from './meta'
import type { DataModel } from './meta'

const props = defineProps<{ props?: { id?: string | number } }>()

const router = useRouter()
const API = new Api()

const loading = ref(true)
const dataModel = ref<DataModel>(Meta.model)
const viewList = ref<{ label: string; value: any }[]>([])
const table = ref({
  columns: [
    // { name: 'id', required: true, label: 'id', field: 'id', align: 'center', sortable: true },
    { align: <'left' | 'right' | 'center'>'left', name: 'app', label: 'App', field: 'app', sortable: true },
    { align: <'left' | 'right' | 'center'>'left', name: 'name', label: 'Name', field: 'name', sortable: true },
    { align: <'left' | 'right' | 'center'>'left', name: 'browse', label: 'Browse', field: 'browse', sortable: true },
    { align: <'left' | 'right' | 'center'>'left', name: 'read', label: 'Read', field: 'read', sortable: true },
    { align: <'left' | 'right' | 'center'>'left', name: 'create', label: 'Create', field: 'create', sortable: true },
    { align: <'left' | 'right' | 'center'>'left', name: 'update', label: 'Update', field: 'update', sortable: true },
    { align: <'left' | 'right' | 'center'>'left', name: 'delete', label: 'Delete', field: 'delete', sortable: true },
    { align: <'left' | 'right' | 'center'>'left', name: 'restore', label: 'Restore', field: 'restore', sortable: true },
    { align: <'left' | 'right' | 'center'>'left', name: 'others', label: 'Others', field: 'others', sortable: true }
  ],

  data: <any>[],
  dataTmp: <any>[],
  selected: [],
  search: {
    app: '',
    name: ''
  }
})

const table_users = ref({
  columns: [
    { align: <'left' | 'right' | 'center'>'left', name: 'name', label: 'Name', field: 'name', sortable: true },
    { align: <'left' | 'right' | 'center'>'left', name: 'username', label: 'Username', field: 'username', sortable: true }
  ],

  data: <any>[],
  dataTmp: <any>[],
  selected: [],
  search: {
    app: '',
    name: ''
  },
  filter: ''
})
const features = ref({
  browse: false,
  read: false,
  create: false,
  update: false,
  delete: false,
  restore: false
})

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
        exclude: ['permissions', 'id'],
        numbers: [],
        moneys: [],
        date: [],
        dateTime: []
      }
      viewList.value = Handler.viewList(dataModel.value, config)
      getPermissionsData()
      getUsersData(id)
    }
  })
}

const getPermissionsData = () => {
  loading.value = true
  const endpoint = 'auth/permissions?limit=0'
  API.get(endpoint, (status: number, data: { items: any }) => {
    loading.value = false
    if (status === 200) {
      let existing = dataModel.value.permissions
      if (!existing) existing = []
      if (existing.length > 0) {
        existing = existing.map((d) => {
          return {
            id: d.id,
            app: d.app,
            name: d.name,
            browse: d.detail?.browse ?? false,
            read: d.detail?.read ?? false,
            create: d.detail?.create ?? false,
            update: d.detail?.update ?? false,
            delete: d.detail?.delete ?? false,
            restore: d.detail?.restore ?? false,
            others: d.detail?.others ?? []
          }
        })
      }
      // FOREACH PERMISSIONS DB
      const target = []
      const items = data?.items ?? data
      for (let i = 0; i < items.length; i++) {
        const val = items[i]
        const perm = {
          ...val,
          browse: false,
          read: false,
          create: false,
          update: false,
          delete: false,
          restore: false,
          others: []
        }
        if (existing.length > 0) {
          const permission = existing.find((perm) => perm.id == val.id)
          if (permission) target.push(permission)
          else target.push(perm)
        } else target.push(perm)
      }
      // REPLACE VALUE
      // console.log('target', target)
      table.value.data = target
      table.value.dataTmp = target
    }
  })
}

const getUsersData = (id: string | number) => {
  loading.value = true
  const endpoint = `auth/users/role/${id}?limit=0`
  API.get(endpoint, (status: number, data: { items: any }) => {
    loading.value = false
    if (status === 200) {
      if (data) {
        table_users.value.data = data
        table_users.value.dataTmp = data
      } else {
        table_users.value.data = []
        table_users.value.dataTmp = []
      }
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
