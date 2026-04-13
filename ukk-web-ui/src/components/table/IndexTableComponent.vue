<template>
  <div>
    <q-table
      v-if="!loading"
      flat
      bordered
      virtual-scroll
      binary-state-sort
      class="sticky-table"
      selection="multiple"
      :wrap-cells="wrapCells"
      :style="'width: 100%; height: ' + Constant.tableHeight(props.meta.minus_height ?? 0) + 'px;'"
      :loading="table.loading"
      :row-key="rowKey ?? 'id'"
      :rows="table.data"
      :columns="table.columns"
      :rows-per-page-options="Config.rowsPerPage()"
      :visible-columns="table.visibleColumns"
      :dense="Config.denseTable()"
      @request="getList"
      v-model:selected="table.selected"
      v-model:pagination="table.pagination"
    >
      <template v-slot:top>
        <TopTable
          v-if="props.meta"
          :meta="props.meta"
          :endpoint="endpoint"
          :helper_message="props?.helper_message ?? ''"
          :tableConfigs="tableConfigs"
          v-model="table"
          v-model:trash="is_trash"
          @refresh-event="onRefresh"
          @add-event="add"
          @update-tab="updateTab"
          :cb-before-delete="cbBeforeDelete"
          :cb-before-restore="cbBeforeRestore"
          :hideSetting="Boolean(hideSetting)"
        >
          <template v-slot:title>
            <slot name="top-title" />
          </template>
          <template v-slot:buttons>
            <slot name="top-buttons" />
          </template>
        </TopTable>
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
          {{ is_trash ? ps.row._id : '' }}
          <q-btn v-if="props.meta.permission.update && !is_trash" class="bg-soft" dense round flat :color="Constant.editColor()" @click="edit(ps.row)" icon="edit">
            <q-tooltip>Edit</q-tooltip>
          </q-btn>
          <q-btn v-if="props.meta.permission.read && !is_trash" class="bg-soft" dense round flat :color="Constant.viewColor()" @click="detail(ps.row)" icon="visibility">
            <q-tooltip>View</q-tooltip>
          </q-btn>
          <slot name="body-action" :props="ps" :isTrash="is_trash"></slot>
        </q-td>
      </template>

      <template v-for="col in cols" :key="col" v-slot:[`body-cell-${col}`]="ps">
        <q-td :props="ps" :style="ps.col.style" :class="`${ps.col.tdClass ? ps.col.tdClass : ''}`">
          <slot :name="`body-cell-${col}`" :props="ps">
            <span v-if="ps.col.formatter">
              <span v-if="ps.col.formatter == 'integer'">{{ Helper.formatNumber(ps.value, 0) }}</span>
              <span v-else-if="ps.col.formatter == 'float'">{{ Helper.formatNumber(ps.value) }}</span>
              <span v-else-if="ps.col.formatter == 'boolean'" :class="`${ps.value ? 'text-positive' : 'text-negative'} text-uppercase text-bold text-italic`">{{ ps.value }}</span>
              <span v-else-if="ps.col.formatter == 'date'">{{ Helper.readDate(ps.value) }}</span>
              <span v-else-if="ps.col.formatter == 'datetime'">{{ Helper.readDate(ps.value, true) }}</span>
              <span v-else-if="ps.col.formatter == 'time'">{{ Helper.toDate(ps.value, 'HH:mm:ss') }}</span>
              <span v-else-if="ps.col.formatter == 'millis'">{{ Helper.readDate(ps.value, true) }}</span>
              <q-badge v-else-if="ps.col.formatter == 'badge'" color="grey">{{ ps.value }}</q-badge>
              <span v-else>{{ ps.value }}</span>
            </span>
            <span v-else>{{ ps.value }}</span>
          </slot>
        </q-td>
      </template>
    </q-table>

    <div v-if="table.summary_data && Object.keys(table.summary_data).length > 0" class="row q-gutter-sm q-pa-sm" style="width: 100%">
      <q-card v-for="(value, key) in table.summary_data" :key="key" flat bordered class="col-auto">
        <q-card-section class="q-pa-sm">
          <div class="text-caption text-grey-8">{{ getSummaryLabel(key.toString()) }}</div>
          <div class="text-h6 text-bold text-primary">{{ getSummaryValue(key.toString(), value) }}</div>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import HeaderTable from './HeaderTable.vue'
import TopTable from './TopTable.vue'
import Api from 'src/services/api'
import { Config } from 'src/services/config'
import { Constant } from 'src/services/constant'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Lang } from 'src/services/lang'
import { authStore } from 'src/stores/auth'
import { ref, watch, onMounted } from 'vue'

const props = defineProps<{
  meta: any
  refresh?: number
  refreshColumns?: number
  epCustom?: string
  helper_message?: string
  epQuery?: string
  wrapCells?: boolean
  hideSetting?: boolean
  rowKey?: string
  cbBeforeDelete?: any // tambahkan "return false" untuk prevent next
  cbBeforeRestore?: any // tambahkan "return false" untuk prevent next
  selected?: {
    type: any
    default: () => []
  }
}>()

const emit = defineEmits(['add', 'edit', 'detail', 'selected', 'getTab', 'getItems', 'update:selected'])

// VARIABLES
const API = new Api()
const SAuth = authStore()
const loading = ref(true)
const table = ref<any>({
  loading: false,
  data: [],
  pagination: {
    page: 1,
    rowsPerPage: 10,
    sortBy: '',
    descending: false,
    rowsNumber: 0
  },
  selected: [],
  visibleColumns: [],
  search: null, // native search
  searchBySelected: [], // array object while doing filters {'name': colName, 'value': 'like=colname:value'}
  config: null,
  summary: false,
  summary_map: [],
  summary_data: null
})
const endpoint = ref('')
const tableConfigs = ref<any>(null)
const is_trash = ref(false)
const cols = ref<string[]>([])
const refresh2 = ref(0)
const tmpSearch = ref<any>({
  search: null,
  searchBySelected: []
})

// METHODS
const init = () => {
  loading.value = true
  let tableData = null
  let tab: any = null
  if (props.meta.tab) {
    tab = props.meta.tab
    props.meta.tabs.forEach((e: any) => {
      if (e.name === props.meta.tab) {
        if (e.table) tableData = e.table(Helper, Constant, Lang, tab)
      }
    })
  }
  if (!tableData) {
    if (props.meta.custom_table) tableData = props.meta.custom_table
    else tableData = props.meta.table(Helper, Constant, Lang, tab)
  }
  handleTable(tableData, true)
}

const handleTable = (tableData: any, hard: boolean = true) => {
  const configs = SAuth.getTblConfigs()
  tableConfigs.value = configs
  let columns: string[] = []
  if (configs && configs.length > 0) {
    for (let i = 0; i < configs.length; i++) {
      const e: any = configs[i]
      if (e.app === props.meta.app && e.module === props.meta.module) {
        for (let ii = 0; ii < e.templates.length; ii++) {
          const e2 = e.templates[ii]
          if (e2.apply) columns = e2.value
        }
      }
    }
  }

  const table2: any[] = []
  if (columns.length > 0) {
    for (let i = 0; i < columns.length; i++) {
      const c = columns[i]
      const col = tableData.find((e: any) => e?.name === c)
      if (col) {
        col.colHide = undefined
        table2.push(col)
      }
    }
    const others = tableData.filter((e: any) => !columns.includes(e.name))
    others.forEach((col: any) => {
      col.colHide = true
      table2.push(col)
    })
  }
  if (table2.length > 0) tableData = table2

  table.value = Handler.table(tableData)

  // Read summary settings
  const summaries = SAuth.getTblSummaries()
  if (summaries && summaries.length > 0) {
    const foundSummary = summaries.find((s: any) => s.app === props.meta.app && s.module === props.meta.module)

    if (foundSummary && foundSummary.summaries && foundSummary.summaries.length > 0) {
      table.value.summary = true
      table.value.summary_map = foundSummary.summaries
    } else {
      table.value.summary = false
      table.value.summary_map = []
    }
  } else {
    table.value.summary = false
    table.value.summary_map = []
  }
  table.value.summary_data = null

  const columnNames = table.value.columns.map((col: any) => col.name)
  cols.value = columnNames.filter((name: string) => name !== 'action')
  onRefresh(hard)
}

// Refresh data
const onRefresh = (hard: boolean | number = false) => {
  if (hard === true) {
    refresh2.value += 1
    tmpSearch.value.search = null
    tmpSearch.value.searchBySelected = []
  } else {
    if (tmpSearch.value.searchBySelected.length > 0) table.value.searchBySelected = tmpSearch.value.searchBySelected
    if (tmpSearch.value.search) table.value.search = tmpSearch.value.search
  }

  endpoint.value = `${props.meta.module}?table=true`
  if (props.epCustom) endpoint.value = props.epCustom
  else if (props.meta.tab)
    props.meta.tabs.forEach((e: any) => {
      if (e.name === props.meta.tab) endpoint.value = e.api
    })
  if (props.epQuery) endpoint.value += `&${props.epQuery}`

  refreshList()
}

const refreshList = () => {
  getList({ pagination: table.value.pagination })
  getSummary({ pagination: table.value.pagination })
}

const getList = (prp: any) => {
  tmpSearch.value = {
    searchBySelected: table.value.searchBySelected,
    search: table.value.search
  }
  loading.value = false
  table.value.loading = true
  table.value.selected = []
  const { page, rowsPerPage, sortBy, descending } = prp.pagination
  const perpage = rowsPerPage === 0 ? table.value.pagination.rowsNumber : rowsPerPage
  const orderType = descending ? 'DESC' : 'ASC'
  let ep = endpoint.value
  ep += `&page=${page}`
  ep += `&limit=${perpage}`
  ep += `&order=${sortBy}:${orderType}`
  if (is_trash.value) ep += '&trash=true'
  if (table.value.searchBySelected) {
    for (let i = 0; i < table.value.searchBySelected.length; i++) {
      const e = table.value.searchBySelected[i]
      if (e.value) ep += `&${e.value}`
    }
  }
  const app = props.meta?.app ?? ''
  API.get(
    ep,
    (status: number, data: any) => {
      table.value.loading = false
      if (status === 200) {
        let items = 'items'
        if (props.meta?.data_items) items = props.meta.data_items
        table.value.data = data[items]
        emit('getItems', table.value.data)
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

const getSummary = (prp: any) => {
  if (table.value.summary && table.value.summary_map?.length > 0) {
    tmpSearch.value = {
      searchBySelected: table.value.searchBySelected,
      search: table.value.search
    }
    loading.value = false
    table.value.loading = true
    table.value.selected = []
    const { page, rowsPerPage, sortBy, descending } = prp.pagination
    const perpage = rowsPerPage === 0 ? table.value.pagination.rowsNumber : rowsPerPage
    const orderType = descending ? 'DESC' : 'ASC'

    let ep = ''
    ep = `${props.meta.module}?summary=true`
    if (props.epCustom) ep = props.epCustom
    else if (props.meta.tab)
      props.meta.tabs.forEach((e: any) => {
        if (e.name === props.meta.tab) ep = e.api
      })
    if (props.epQuery) ep += `&${props.epQuery}`

    ep += `&page=${page}`
    ep += `&limit=${perpage}`
    ep += `&order=${sortBy}:${orderType}`

    if (is_trash.value) ep += '&trash=true'
    if (table.value.searchBySelected) {
      for (let i = 0; i < table.value.searchBySelected.length; i++) {
        const e = table.value.searchBySelected[i]
        if (e.value) ep += `&${e.value}`
      }
    }

    table.value.summary_map.forEach((mapItem: string) => {
      ep += `&summary_map=${mapItem}`
    })

    const app = props.meta?.app ?? ''
    API.get(
      ep,
      (status: number, data: any) => {
        table.value.loading = false
        if (status === 200) {
          table.value.summary_data = data
        }
      },
      app
    )
  }
}

const getSummaryLabel = (key: string): string => {
  if (!key) return ''
  const parts = key.split('_')
  if (parts.length < 2) return key

  const fnName = parts.pop()?.toUpperCase() || ''
  const colName = parts.join('_')

  const col = table.value.columns.find((c: any) => c.name === colName)
  const label = col ? col.label : colName.replaceAll('_', ' ')

  return `${label} (${fnName})`
}

const getSummaryValue = (key: string, value: any): string | null => {
  if (value === null || value === undefined) return '-'

  const parts = key.split('_')
  parts.pop()
  const colName = parts.join('_')

  const col = table.value.columns.find((c: any) => c.name === colName)

  if (col?.formatter === 'integer') {
    return Helper.formatNumber(value, 0)
  }
  if (col?.formatter === 'float') {
    return Helper.formatNumber(value)
  }

  return Helper.formatNumber(value)
}

const add = () => {
  emit('add')
}

const edit = (data: any) => {
  emit('edit', data)
}

const detail = (data: any) => {
  emit('detail', data)
}

const updateTab = (value: any) => {
  emit('getTab', value)
  // eslint-disable-next-line vue/no-mutating-props
  props.meta.tab = value
  init()
}

const refreshCols = () => {
  if (props.meta.custom_table) {
    const tableData = props.meta.custom_table
    handleTable(tableData, false)
  }
}

// Initialize on mount
onMounted(() => {
  init()
})

watch(() => props.refresh, onRefresh)
watch(() => props.refreshColumns, refreshCols)
watch(
  () => table.value.selected,
  () => emit('selected', table.value.selected)
)
watch(
  () => props.selected,
  (val) => {
    table.value.selected = val
  }
)

watch(
  () => table.value.selected,
  (val) => {
    emit('update:selected', val)
  }
)
</script>
