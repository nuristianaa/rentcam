<template>
  <s-page :meta="Meta">
    <s-loading v-if="loading" />
    <s-table v-else :meta="Meta" :refreshColumns="refresh" :epQuery="epQuery" @getItems="getItems">
      <template v-slot:top-title>
        <div class="flex justify-between">
          <div class="q-gutter-x-md row items-center">
            <q-btn :label="`Date filter: ${dt?.from} to ${dt?.to}`" dense no-caps class="q-px-sm" color="primary">
              <q-popup-proxy ref="qDateProxy" transition-show="scale" transition-hide="scale">
                <q-date range v-model="dt" mask="YYYY-MM-DD">
                  <div class="row items-center justify-end">
                    <q-btn v-close-popup label="Submit" color="primary" flat @click="onSubmitFilter()" />
                  </div>
                </q-date>
              </q-popup-proxy>
            </q-btn>
            <q-btn :loading="!moduleOptions" label="Print PDF" dense no-caps color="primary" icon="picture_as_pdf" @click="showPrintPdfFilter = true" />
            <!-- <q-btn label="Table Filter" dense no-caps color="primary" icon="filter_list" @click="showTableFilter = true" /> -->
            <q-btn dense no-caps class="q-px-sm" color="primary">
              Add Columns:
              {{ auditCfg.cols && auditCfg.cols.length > 4 ? `${auditCfg.cols.length} Columns Applied` : auditCfg.cols.length > 0 ? auditCfg.cols.join(', ') : '' }}
              <q-menu class="q-pa-sm">
                <q-select label="Columns" hint="Press enter to add more value." v-model="auditCfg.cols" autofocus use-input use-chips multiple hide-dropdown-icon input-debounce="0" new-value-mode="add-unique" style="min-width: 250px" :options="select.opt" @filter="(val, update) => filterSelect(val, update)" />
                <q-toggle label="View as JSON?" v-model="auditCfg.as_json" />
                <q-btn label="Apply" @click="applyCustomCols()" class="full-width" color="primary" v-close-popup />
              </q-menu>
            </q-btn>
            <q-btn dense no-caps color="primary" icon="refresh" @click="clearAllFilter()" label="Clear All Filter" />
          </div>
        </div>
      </template>

      <template v-slot:body-cell-type="ps">
        <div>
          <q-btn dense size="xs" :label="ps.props.value" :color="defineColorByType(ps.props.value)" @click="getDetail(ps.props.row.id)" />
        </div>
      </template>
      <template v-for="col in auditCfg.cols" :key="col" v-slot:[`body-cell-${col}_data`]="ps">
        <template v-if="Array.isArray(ps.props.value) || (typeof ps.props.value === 'object' && ps.props.value !== null)">
          <pre v-if="auditCfg.as_json" style="white-space: pre; margin: 0">{{ normalizeValue(ps.props.value) }}</pre>
          <TableDetail v-else :node="ps.props.value" no-header />
        </template>
        <div v-else>{{ ps.props.value }}</div>
      </template>
    </s-table>

    <!-- Table Filter Dialog -->
    <!-- <FilterTableDialog v-model="showTableFilter" :options="options" :moduleKeys="moduleKeys" :tableFilter="tableFilter" @update-columns="newCol" @load-module-keys="loadModuleKeys" /> -->

    <!-- Print PDF Filter Dialog -->
    <FilterPrintPdfDialog v-if="moduleOptions" v-model="showPrintPdfFilter" :moduleOptions="moduleOptions" :approversList="approversList" @apply="applyFilters" />

    <s-dialog v-model="dialog">
      <TableDetail :node="dataDetail" />
    </s-dialog>
  </s-page>
</template>

<script setup lang="ts">
import TableDetail from './TableDetail.vue'
import FilterPrintPdfDialog from './components/FilterPrintPdfDialog.vue'

import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Handler } from 'src/services/handler'
import Meta from './meta'
import type { FilterItem, TableFilter, DataModel } from './meta'
import Api from 'src/services/api'
import { Helper } from 'src/services/helper'
import { configStore } from 'src/stores/config'
import { authStore } from 'src/stores/auth'
import type { Approver } from 'src/components/approval/meta'

const API = new Api()
const router = useRouter()
const company_code = authStore().getCompanyCode()

const loading = ref(true)
const refresh = ref(0)
const cfg = configStore()
cfg.getAuditTrailCfg()
const auditCfg = ref<{
  cols: string[]
  as_json: boolean
}>(Helper.unreactive(cfg.audit_trail_cfg))
const select = ref<any>({
  opt: [],
  optTmp: []
})

const dt = ref({
  from: Helper.subDate(Helper.today(), 30),
  to: Helper.addDate(Helper.today(), 1)
})

const moduleOptions = ref<Record<string, string[]> | null>(null)

const tableFilter = ref<TableFilter>({
  app: '',
  module: '',
  columns: []
})

const dialog = ref({
  show: false,
  type: 'detail',
  title: 'Detail',
  props: null,
  persistent: false
})

const dataDetail = ref(null)
const showPrintPdfFilter = ref(false)

const approversList = ref<Approver[]>([])

const epQuery = computed(() =>
  [
    dt.value?.from && dt.value?.to ? `date_from=${dt.value.from}&date_to=${dt.value.to}` : '',
    'with_data=true',
    // auditCfg.value?.cols ? 'with_data=true' : ''
    tableFilter.value?.app ? `app=${tableFilter.value.app}` : '',
    tableFilter.value?.module ? `module=${tableFilter.value.module}` : ''
  ]
    .filter(Boolean)
    .join('&')
)

// METHODS
const init = () => {
  Handler.permissions(router, 'browse', Meta, (status, data) => {
    Meta.permission = data
    Meta.permission.create = false
    Meta.permission.delete = false
    if (auditCfg.value?.cols?.length > 0) applyCustomCols()
    loading.value = false
    if (status) Promise.all([getModules(), getUsers()])
  })
}

const showDialog = (type: string, title: string, data: any = null) => {
  dialog.value.type = type
  dialog.value.title = `${title} | ${Meta.title}`
  dialog.value.show = true
  dialog.value.props = data
}

const getUsers = async () => {
  await API.get(
    'auth/users?limit=0',
    (status: number, data: any) => {
      if (status === 200) approversList.value = data
    },
    'identity'
  )
}

const getModules = async () => {
  await API.get(
    `${Meta.module}?fetch_module=True&${epQuery.value}`,
    (status: number, data: any) => {
      if (status === 200) moduleOptions.value = data
    },
    'identity'
  )
}

const getDetail = async (data_id: string) => {
  await API.get(
    `audit-trails/${data_id}`,
    (status: number, data: any) => {
      if (status === 200) {
        dataDetail.value = data
        showDialog('detail', 'Detail', data)
      }
    },
    'identity'
  )
}

const onSubmitFilter = () => {
  if (dt.value?.from && dt.value?.to) {
    loading.value = true
    setTimeout(() => (loading.value = false), 100)
  }
}

const applyFilters = async (filters: FilterItem[], signPlacements: DataModel[]) => {
  const request = {
    configs: filters,
    date_from: dt.value.from,
    date_to: dt.value.to,
    company_code: company_code,
    sign_placements: signPlacements
  }

  await API.post(
    `${Meta.module}/generate-pdf`,
    request,
    (status: number, _data: any, _message: any, response: any) => {
      if (status === 200) {
        const blob = new Blob([response.data], { type: 'text/html' })
        const url = URL.createObjectURL(blob)
        window.open(url, '_blank')
      }
    },
    'identity',
    false,
    'blob'
  )
}

const defineColorByType = (name: string) => {
  if (name === 'create') return 'positive'
  if (name === 'update') return 'info'
  if (name === 'delete') return 'negative'
  if (name === 'restore') return 'orange'
  return 'grey'
}

const applyCustomCols = () => {
  const existing = Meta.table()
  if (auditCfg.value.cols.length > 0) {
    for (let i = 0; i < auditCfg.value.cols.length; i++) {
      const e = auditCfg.value.cols[i]
      if (e) {
        const col1: any = {
          align: 'left',
          name: `${e}_data`,
          label: `${e}`,
          field: (v: any) => v?.data?.[e],
          sortable: false,
          filterHide: true
        }
        existing.push(col1)
      }
    }
  }
  Meta.custom_table = existing
  cfg.setAuditTrailCfg(auditCfg.value)
  refresh.value++
  // loading.value = true
  // setTimeout(() => { loading.value = false }, 300)
}

const normalizeValue = (val: any): string => {
  if (Array.isArray(val) || (typeof val === 'object' && val !== null)) {
    return JSON.stringify(val, null, 2) // pretty print with 2 spaces
  }
  return String(val ?? '')
}

const clearAllFilter = () => {
  auditCfg.value = {
    cols: [],
    as_json: false
  }
  cfg.setAuditTrailCfg(auditCfg.value)
  Meta.custom_table = null
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 300)
}

const getItems = (data: any[]) => {
  let opt = []
  if (!Array.isArray(data)) {
    opt = []
    return
  }

  const uniqueKeys = new Set<string>()
  for (const item of data) {
    const d = item?.data
    if (d && typeof d === 'object') {
      for (const key in d) {
        uniqueKeys.add(key)
      }
    }
  }
  opt = Array.from(uniqueKeys)
  select.value.opt = opt
  select.value.optTmp = opt
}

const filterSelect = (val: string, update: (fn: () => void) => void) => {
  if (val === '') {
    update(() => {
      select.value.opt = select.value.optTmp
    })
    return
  }
  update(() => {
    const needle = val.toLowerCase()
    select.value.opt = select.value.optTmp.filter((opt: any) => JSON.stringify(opt).toLowerCase().includes(needle))
  })
}

onMounted(init)
</script>
