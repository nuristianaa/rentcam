<template>
  <div>
    <q-table dense flat bordered virtual-scroll binary-state-sort :wrap-cells="props.wrapCells" :row-key="rowKey ?? 'id'" :rows="table.data" :columns="table.columns" :rows-per-page-options="[7, 25, 100, 1000, 0]" @request="getList" v-model:pagination="table.pagination">
      <template v-slot:top>
        <slot name="top">
          <div class="title">{{ props.title ?? 'Please choose a data item first!' }}</div>
        </slot>
      </template>

      <template v-slot:header-cell="prp">
        <HeaderTable :meta="props.meta" v-model="table" :props="prp" :refresh="refresh2" @refresh-event="onRefresh">
          <template v-slot:[`header-${prp.col.name}`]>
            <slot :name="`header-${prp.col.name}`">
              {{ prp.col.label.replaceAll(/_/g, ' ') ?? prp.col.name.replaceAll(/_/g, ' ') }}
            </slot>
          </template>
        </HeaderTable>
      </template>

      <template v-slot:body-cell-action="ps">
        <q-td :props="ps">
          <slot name="body-action" :props="ps">
            <q-btn dense  color="primary" @click="choose(ps.row)" label="Choose" no-caps />
          </slot>
        </q-td>
      </template>

      <template v-for="col in cols" :key="col" v-slot:[`body-cell-${col}`]="ps">
        <q-td :props="ps" :style="ps.col.style" :class="getTdClass?.(ps)">
          <slot :name="`body-cell-${col}`" :props="ps">
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
          </slot>
        </q-td>
      </template>
    </q-table>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { Helper } from 'src/services/helper'
import HeaderTable from './HeaderTable.vue'
import Api from 'src/services/api'
import { Handler } from 'src/services/handler'

const props = defineProps<{
  meta: any
  columns: any
  api: string
  app?: string
  wrapCells?: boolean
  noExport?: boolean
  rowKey?: string
  title?: string
  getTdClass?: (props: any) => string
}>()

const emit = defineEmits(['choose'])

const API = new Api()
const table = ref<any>({
  loading: false,
  data: [],
  pagination: {
    page: 1,
    rowsPerPage: 7,
    sortBy: '',
    descending: false,
    rowsNumber: 0
  },
  selected: [],
  visibleColumns: [],
  search: null, // native search
  searchBySelected: [], // array object while doing filters {'name': colName, 'value': 'like=colname:value'}
  config: null
})
const endpoint = ref('')
const cols = ref<string[]>([])
const refresh2 = ref(0)

const handleTable = () => {
  table.value = Handler.table(props.columns)
  table.value.pagination.rowsPerPage = 7
  const columnNames = table.value.columns.map((col: any) => col.name)
  cols.value = columnNames.filter((name: string) => name !== 'action')
  onRefresh()
}

// Refresh data
const onRefresh = (hard: boolean | number = false) => {
  if (hard === true) refresh2.value += 1
  endpoint.value = props.api
  if (endpoint.value.indexOf('?') > -1) endpoint.value += '&table=true'
  else endpoint.value += '?table=true'
  refreshList()
}

const refreshList = () => {
  getList({ pagination: table.value.pagination })
}

const getList = (prp: any) => {
  table.value.loading = true
  table.value.selected = []
  const { page, rowsPerPage, sortBy, descending } = prp.pagination
  const perpage = rowsPerPage === 0 ? table.value.pagination.rowsNumber : rowsPerPage
  const orderType = descending ? 'DESC' : 'ASC'
  let ep = endpoint.value
  ep += `&page=${page}`
  ep += `&limit=${perpage}`
  ep += `&order=${sortBy}:${orderType}`
  if (table.value.searchBySelected) {
    for (let i = 0; i < table.value.searchBySelected.length; i++) {
      const e = table.value.searchBySelected[i]
      if (e.value) ep += `&${e.value}`
    }
  }
  const app = props.app ?? props.meta?.app ?? ''
  API.get(
    ep,
    (status: number, data: any) => {
      table.value.loading = false
      if (status === 200) {
        table.value.data = data.items
        table.value.pagination = {
          rowsNumber: data.total,
          page: page,
          rowsPerPage: perpage,
          sortBy: sortBy,
          descending: descending
        }
      }
    },
    app
  )
}

const choose = (data: any) => {
  emit('choose', data)
}

// END OF EXPORT TABLE

onMounted(() => {
  handleTable()
})
</script>
