<template>
  <div class="q-pa-md">
    <div class="row q-pa-sm justify-between">
      <div class="title">Category</div>
      <q-btn label="Add" icon="add" color="primary" @click="add" />
    </div>
    <q-table v-if="!loading" flat :rows="rows" :columns="columns" row-key="name" binary-state-sort :rows-per-page-options="[0]">
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td key="action" :props="props">
            <q-btn dense round flat color="negative" @click="onDelete(props.row.id, props.pageIndex)" icon="delete">
              <q-tooltip>Delete</q-tooltip>
            </q-btn>
          </q-td>
          <q-td key="name" :props="props">
            {{ props.row.name }}
            <q-popup-edit v-model="props.row.name" buttons v-slot="scope" @update:model-value="update(props.row)">
              <q-input v-model="scope.value" dense autofocus @keyup.enter="scope.set" />
            </q-popup-edit>
          </q-td>
          <q-td key="description" :props="props">
            {{ props.row.description }}
            <q-popup-edit v-model="props.row.description" buttons v-slot="scope" @update:model-value="update(props.row)">
              <q-input type="text" v-model="scope.value" dense autofocus @keyup.enter="scope.set" />
            </q-popup-edit>
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { Helper } from 'src/services/helper'
import { ref, onMounted } from 'vue'

interface Column {
  name: string
  label: string
  field: string | ((row: any) => any)
  required?: boolean
  align?: 'left' | 'right' | 'center'
  sortable?: boolean
  style?: string
}

interface Row {
  id?: string
  name: string
  description: string
}

const props = defineProps({
  app: {
    type: String,
    required: false
  },
  group: {
    type: String,
    required: true
  }
})

const API = new Api()
const H = Helper
const loading = ref(true)
const columns: Column[] = [
  { name: 'action', align: 'left', label: 'action', field: 'id', sortable: false, style: 'width:20px' },
  { name: 'name', align: 'left', label: 'name', field: 'name', sortable: true },
  { name: 'description', align: 'left', label: 'description', field: 'description', sortable: true }
]
const rows = ref<Row[]>([
  {
    name: 'Frozen Yogurt',
    description: 'adsasdas'
  },
  {
    name: 'Ice cream sandwich',
    description: '237'
  }
])
const endpoint = `master/categories`
const app = props.app ?? 'crm'

const fetchData = () => {
  const ep = `${endpoint}?limit=0&where=group:${props.group}`
  API.get(
    ep,
    (status: number, data: Row[]) => {
      loading.value = false
      if (status === 200) rows.value = data
    },
    app
  )
}

const add = () => {
  const req = { group: props.group, name: '<click to edit>', description: '' }
  loading.value = true
  API.post(
    endpoint,
    req,
    (status: number, data: Row) => {
      loading.value = false
      if (status === 200) rows.value.push(data)
    },
    app
  )
}

const update = (row: Row) => {
  const id = row.id
  const req = {
    name: row.name,
    description: row.description
  }
  // Replace with your API call
  API.put(
    `${endpoint}/${id}`,
    req,
    (status: number) => {
      loading.value = false
      if (status === 200) H.showSuccess('Update Success')
    },
    app
  )
}

const onDelete = (id: string, index: number) => {
  H.confirm('Are you sure?', (result: boolean) => {
    if (result) {
      loading.value = true
      API.delete(
        `${endpoint}/${id}`,
        {},
        (status: number) => {
          loading.value = false
          if (status === 200) {
            rows.value.splice(index, 1)
          }
        },
        app
      )
    }
  })
}

onMounted(fetchData)
</script>
