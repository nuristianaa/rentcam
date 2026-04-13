<template>
  <q-dialog v-model="model">
    <q-card style="width: 900px; max-width: 85vw">
      <q-bar style="position: sticky; top: 0; width: 100%; z-index: 5; justify-content: space-between">
        <div>{{ meta.title || 'Table View' }}</div>
        <q-btn v-close-popup flat icon="close" size="sm" />
      </q-bar>
      <q-card-section class="q-pa-md">
        <q-table flat virtual-scroll binary-state-sort :style="'width: 100%; height: 72vh; min-height: 300px;'" :loading="table.loading" :row-key="'id'" :rows="table.data" :columns="table.columns" @request="refreshList" :rows-per-page-options="[]" :dense="true" v-model:pagination="table.pagination">
          <template v-for="col in columns" :key="col" v-slot:[`body-cell-${col.name}`]="ps">
            <q-td :props="ps" :style="ps.col.style">
              <span v-if="ps.col.formatter">
                <span v-if="ps.col.formatter == 'integer'">{{ Helper.formatNumber(ps.value, 0) }}</span>
                <span v-else-if="ps.col.formatter == 'float'">{{ Helper.formatNumber(ps.value) }}</span>
                <span v-else-if="ps.col.formatter == 'boolean'" :class="ps.value ? 'text-positive' : 'text-negative'">{{ ps.value }}</span>
                <span v-else-if="ps.col.formatter == 'date'">{{ Helper.readDate(ps.value) }}</span>
                <span v-else-if="ps.col.formatter == 'datetime'">{{ Helper.readDate(ps.value, true) }}</span>
                <span v-else-if="ps.col.formatter == 'time'">{{ Helper.toDate(ps.value, 'HH:mm:ss') }}</span>
                <span v-else-if="ps.col.formatter == 'millis'">{{ Helper.readDate(ps.value, true) }}</span>
                <span v-else>{{ ps.value }}</span>
              </span>
              <span v-else>{{ ps.value }}</span>
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script lang="ts" setup>
import Api from 'src/services/api'
import { Constant } from 'src/services/constant'
import { Helper } from 'src/services/helper'
import { Lang } from 'src/services/lang'
import { onMounted, ref } from 'vue'

const model = defineModel({ default: false })
const props = defineProps<{
  meta: any
  query?: string
}>()
const API = new Api()
const columns = props.meta.table(Helper, Constant, Lang).map((el: any) => {
  const row = { ...el }
  // Edit here if needed
  return row
})
const table = ref<any>({
  loading: false,
  data: [],
  columns: columns,
  pagination: {
    page: 1,
    rowsPerPage: 20,
    sortBy: 'created_at',
    descending: false,
    rowsNumber: 0
  },
  visibleColumns: [],
  search: null // native search
})

const refreshList = () => {
  getList({ pagination: table.value.pagination })
}

function getList(prop: any) {
  table.value.loading = true
  table.value.selected = []
  const { page, rowsPerPage, sortBy, descending } = prop.pagination
  const orderType = descending ? 'DESC' : 'ASC'
  let ep = `${props.meta.module}?table=true`
  ep += `&page=${page}`
  ep += `&limit=${rowsPerPage}`
  ep += `&order=${sortBy}:${orderType}`
  if (props.query) ep += `${props.query}`
  API.get(
    ep,
    (status: number, data: any) => {
      table.value.loading = false
      if (status === 200) {
        table.value.data = data['items']
        table.value.pagination = {
          rowsNumber: data.total,
          page: page,
          rowsPerPage: rowsPerPage,
          sortBy: sortBy,
          descending: descending
        }
      }
    },
    props.meta.app
  )
}

onMounted(() => {
  refreshList()
})
</script>
