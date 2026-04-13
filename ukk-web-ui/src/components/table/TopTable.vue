<template>
  <div v-if="meta" style="width: 100%">
    <div v-if="meta.tabs && showActionButtons" class="q-gutter-x-md column items-start">
      <q-btn-dropdown v-if="$q.screen.lt.sm" flat dense size="10px" color="info" :label="meta.tab">
        <q-btn v-for="v in meta.tabs" :key="v.name" :label="v.label" :icon="v.icon" flat dense size="10px" class="row" :color="tab == v.name ? 'positive' : 'grey'" @click="updateTab(v.name)" />
      </q-btn-dropdown>
      <q-btn-group v-else flat>
        <q-btn v-for="v in meta.tabs" :key="v.name" :label="v.label" :icon="v.icon" flat dense size="11px" class="q-pr-sm" :color="tab == v.name ? 'positive' : 'grey'" @click="updateTab(v.name)" />
      </q-btn-group>
    </div>
    <q-separator v-if="meta.tabs && showActionButtons" />
    <div class="row q-mt-sm">
      <!-- TOP LEFT | TITLE -->
      <div class="q-gutter-sm q-pb-sm">
        <div v-if="meta.tabs && !showActionButtons" class="q-gutter-x-md column items-start">
          <q-btn-dropdown v-if="$q.screen.lt.sm" flat dense size="10px" color="info" :label="meta.tab">
            <q-btn v-for="v in meta.tabs" :key="v.name" :label="v.label" :icon="v.icon" flat dense size="10px" class="row" :color="tab == v.name ? 'positive' : 'grey'" @click="updateTab(v.name)" />
          </q-btn-dropdown>
          <q-btn-group v-else flat>
            <q-btn v-for="v in meta.tabs" :key="v.name" :label="v.label" :icon="v.icon" flat dense size="11px" class="q-pr-sm" :color="tab == v.name ? 'positive' : 'grey'" @click="updateTab(v.name)" />
          </q-btn-group>
        </div>
        <!-- DELETE Button -->
        <q-btn v-if="meta.permission.delete && datatable && datatable.selected.length !== 0" :color="trash ? 'green' : 'negative'" :icon="trash ? 'refresh' : 'delete'" :label="trash ? 'Re-Activate' : 'Delete'" @click="deleteSelected" />
        <!-- ADD Button -->
        <q-btn v-if="!trash && meta.permission.create"  color="primary" icon="add" :label="meta.label_add ?? 'Add'" @click="$emit('addEvent')" />
        <!-- SLOT buttons -->
        <slot name="buttons" />
      </div>

      <q-space />

      <!-- BUTTONS -->
      <div class="q-gutter-sm q-pb-sm">
        <q-btn @click="onRefresh(true)" dense flat size="sm" color="deep-orange" icon="restart_alt">
          <q-tooltip>Reset filter</q-tooltip>
        </q-btn>
         <!-- TRASH BIN -->
        <q-btn v-if="meta.permission.restore && !trash && !meta.hide_trash" dense flat color="negative" icon="recycling" @click="updateTrash(true)">
          <q-tooltip>Trash</q-tooltip>
        </q-btn>
        <q-btn v-if="trash" dense flat color="grey-6" icon="chevron_left" @click="updateTrash(false)">
          <q-tooltip>Back</q-tooltip>
        </q-btn>
        <q-btn dense flat color="primary" icon="more_vert">
          <q-menu auto-close>
            <q-list dense>
              <q-item clickable dense class="q-py-xs q-px-sm">
                <q-item-section side class="q-pr-xs">
                  <q-icon name="archive" size="16px" />
                </q-item-section>
                <q-item-section class="text-caption">
                  Export to XLSX
                </q-item-section>
              </q-item>

              <q-item
                v-if="!hideSetting"
                clickable
                dense
                class="q-py-xs q-px-sm"
                @click="openSettingDrawer('settings')"
              >
                <q-item-section side class="q-pr-xs">
                  <q-icon name="settings" size="16px" />
                </q-item-section>
                <q-item-section class="text-caption">
                  Advance Settings
                </q-item-section>
              </q-item>

            </q-list>

          </q-menu>
        </q-btn>


      </div>
    </div>

    <!-- MODAL TABLE CONFIGS -->
    <q-drawer v-model="modal.show" bordered side="right" :width="300" class="">
      <div class="row justify-between q-pa-md">
        <div class="text-bold">Settings</div>
        <div>
          <q-btn dense outline  class="q-px-sm q-mr-sm" no-caps label="Cancel" size="sm" @click="modal.show = false" />
          <q-btn dense  class="q-px-sm" no-caps color="primary" icon-right="save" label="Apply" size="sm" @click="saveTemplate()" />
        </div>
      </div>

      <!-- TAB HEADER -->
      <div class="row q-pa-md q-gutter-sm">
        <q-btn label="Default" dense outline no-caps color="primary" icon="refresh" size="sm" @click="resetTemplate()" />
        <q-btn-group  v-for="(v, i) in templates" :key="i" size="xs">
          <q-btn dense  size="xs" :color="v.apply ? 'primary' : 'grey-3'" :text-color="v.apply ? 'white' : 'dark'" icon="check" @click="chooseTemplate(v, i)" />
          <q-btn dense no-caps class="q-px-sm"  size="sm" :color="v.apply ? 'primary' : 'grey-3'" :text-color="v.apply ? 'white' : 'dark'" :label="v.name">
            <q-popup-edit v-model="v.name" auto-save v-slot="scope">
              <q-input class="form-xs" v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
            </q-popup-edit>
          </q-btn>
          <q-btn no-caps dense  size="xs" :color="v.apply ? 'primary' : 'grey-3'" :text-color="v.apply ? 'white' : 'dark'" icon="delete" @click="deleteTemplate(i)" />
        </q-btn-group>
        <q-btn label="Save as new" dense outline no-caps color="primary" icon="add" size="sm" @click="addTemplate(col_applied)" />
      </div>

      <q-linear-progress v-if="loading" />
      <div v-else :style="'width: 90%; height: ' + ($q.screen.height - 220) + 'px;'">
        <s-drag v-model="col_applied">
          <template #default="{ item }">
            <q-list bordered separator dense>
              <q-item v-if="item" clickable dense>
                <q-toggle size="sm" dense v-model="item.show" color="primary" class="q-mr-sm" />
                <q-item-section>{{ item?.label ?? item?.name }}</q-item-section>
                <q-item-section side><q-icon size="sm" name="swap_vertical_circle" /></q-item-section>
              </q-item>
            </q-list>
          </template>
        </s-drag>
      </div>
    </q-drawer>

    <q-drawer v-model="summaryModal.show" bordered side="right" :width="300" class="">
      <div class="row justify-between q-pa-md">
        <div class="text-bold">Summaries</div>
        <div>
          <q-btn dense outline  class="q-px-sm q-mr-sm" no-caps label="Cancel" size="sm" @click="summaryModal.show = false" />
          <q-btn dense  class="q-px-sm" no-caps color="primary" icon-right="save" label="Apply" size="sm" @click="saveSummarySettings()" />
        </div>
      </div>

      <q-linear-progress v-if="loading" />
      <div v-else :style="'width: 90%; height: ' + ($q.screen.height - 220) + 'px;'">
        <q-list separator bordered>
          <q-item v-for="(col, index) in summary_cols" :key="index" class="flex items-center">
            <q-item-section side top>
              <q-checkbox v-model="col.selected" />
            </q-item-section>

            <q-item-section>
              <q-item-label>{{ col.label }}</q-item-label>
            </q-item-section>

            <q-item-section side>
              <q-select v-model="col.type" :options="summary_types" :disable="!col.selected" dense style="width: 90px" emit-value map-options />
            </q-item-section>
          </q-item>

          <q-item v-if="!summary_cols.length">
            <q-item-section class="text-grey">No numeric columns (integer/float) found in table definition.</q-item-section>
          </q-item>
        </q-list>
      </div>
    </q-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, onMounted, computed, useSlots } from 'vue'
// import { exportFile } from 'quasar'
// import * as XLSX from 'xlsx'
import XLSX from 'xlsx-js-style'
import Api from 'src/services/api'
import { Helper } from 'src/services/helper'
import { authStore } from 'src/stores/auth'
import { Dialog } from 'quasar'

const props = defineProps<{
  meta: any
  helper_message: string
  modelValue: any
  trash: boolean
  hideSetting: boolean
  tableConfigs: any
  cbBeforeDelete?: any // tambahkan "return false" untuk prevent next
  endpoint: string
}>()
const emit = defineEmits(['updateTab', 'update:modelValue', 'update:trash', 'update:meta', 'refreshEvent', 'addEvent'])

const API = new Api()
const SAuth = authStore()
const datatable = ref(props.modelValue)
const loading = ref(false)
const modal = reactive({ show: false })
const summaryModal = reactive({ show: false })
const templates = ref<any[]>([])
const col_all = ref<{ show: boolean; name: any; label: any }[]>([])
const col_applied = ref<{ show: boolean; name: any; label: any }[]>([])
const tab = ref(props.meta.tab)

const summary_cols = ref<any[]>([])
const summary_types = ['sum', 'avg', 'min', 'max', 'count']


const slots = useSlots()

const hasSlotButtons = computed(() => {
  const slot = slots.buttons?.()
  return slot && slot[0].children.length > 0
})

const init = () => {
  const existing_summary_map = props.modelValue.summary_map || []
  const summaryMap = new Map(
    existing_summary_map.map((s: string) => {
      const parts = s.split(':')
      return [parts[0], parts[1]]
    })
  )

  if (props.modelValue) {
    if (props.modelValue?.columns?.length) {
      props.modelValue.columns.forEach((el: { name: any; label: any; colHide: any; formatter?: string | null }) => {
        const row = { show: true, name: el.name, label: el.label }
        if (el.colHide) row.show = false
        col_all.value.push(row)
        col_applied.value.push(row)

        if (el.formatter === 'integer' || el.formatter === 'float') {
          const savedType = summaryMap.get(el.name)
          summary_cols.value.push({
            selected: !!savedType, // True if it was in the map
            name: el.name,
            label: el.label,
            type: savedType || 'sum' // Use saved type or default to 'sum'
          })
        }
      })
    }
  }

  const configs = props.tableConfigs
  if (configs && configs.length > 0) {
    for (let i = 0; i < configs.length; i++) {
      const e = configs[i]
      if (e?.app == props?.meta?.app && e?.module == props?.meta?.module) {
        templates.value = e.templates ?? []
        templates.value.forEach((el, ii) => {
          if (el.apply) chooseTemplate(el, ii)
        })
      }
    }
  }
}

const onRefresh = (reset = false) => {
  if (reset) {
    const config = datatable.value?.config
    datatable.value.search = null
    datatable.value.searchBySelected = []
    if (config) {
      datatable.value.pagination.sortBy = config.sortBy
      datatable.value.pagination.descending = !config.ascending
    } else {
      datatable.value.pagination.sortBy = 'created_at'
      datatable.value.pagination.descending = true
    }
  }
  emit('update:modelValue', datatable.value)
  emit('refreshEvent', reset)
}

const updateTrash = (val: boolean) => {
  emit('update:trash', val)
  onRefresh(true)
}

// Delete or Restore Selected Data
const deleteSelected = () => {
  let next = true
  if (props.cbBeforeDelete) {
    next = props.cbBeforeDelete(datatable.value.selected)
  }
  // if (props.cbBeforeRestore) {
  //   next = props.cbBeforeRestore(datatable.value.selected)
  // }

  if (next === false) return false

  const type = !props.trash ? 'delete' : 'restore'
  const msg = `Are you sure want to ${type} (${datatable.value.selected.length}) selected data  ?`
  Helper.confirm(msg, (result: boolean) => {
    if (result) deleteDataSelected(type)
  })
}

const deleteDataSelected = async (type: string) => {
  const app = props.meta?.app ?? ''

  Helper.loadingOverlay()
  const ids = []
  for (const row of datatable.value.selected) {
    ids.push(row.id)
  }
  let ep = ''
  if (type === 'delete') ep = `${props.meta.module}/delete`
  else ep = `${props.meta.module}/restore`
  const request = {
    id: ids
  }
  await API.delete(
    ep,
    request,
    (status: number, _data: any, message: string) => {
      if (status === 200) Helper.showToast(message)
    },
    app
  )
  datatable.value.selected = []
  Helper.loadingOverlay(false)
  onRefresh()
}

// EXPORT TABLE
const exportTable = () => {
  Helper.confirm('Area you sure want to export to Excel based on your filtered data?', (result: boolean) => {
    if (result) {
      getListAndExport()
    }
  })
}

const getListAndExport = async () => {
  const exportData: any[] = []
  const { rowsNumber, sortBy, descending } = props.modelValue.pagination
  const orderType = descending ? 'DESC' : 'ASC'
  let ep = props.endpoint
  ep += `&order=${sortBy}:${orderType}`
  if (props.trash) ep += '&trash=true'
  if (props.modelValue.searchBySelected) {
    for (let i = 0; i < props.modelValue.searchBySelected.length; i++) {
      const e = props.modelValue.searchBySelected[i]
      if (e.value) ep += `&${e.value}`
    }
  }
  const app = props.meta?.app ?? ''

  const dlg = Dialog.create({
    title: 'Exporting data...',
    message: `0/${rowsNumber} data`,
    progress: true, // we enable default settings
    persistent: true, // cannot close by clicking outside
    ok: false, // hide default OK
    cancel: {
      label: 'Cancel',
      color: 'negative'
    }
  })
  let condition = true
  dlg.onCancel(() => {
    condition = false
  })
  const limit = 10000
  const loop = Math.round(rowsNumber / limit) + 1
  for (let i = 1; i <= loop; i++) {
    if (condition) {
      await API.get(
        `${ep}&limit=${limit}&page=${i}`,
        (status: number, data: any) => {
          if (status === 200) {
            if (data.items && data.items.length > 0) {
              let downloaded = i * limit
              if (downloaded >= rowsNumber) downloaded = rowsNumber
              dlg.update({ message: `${downloaded}/${rowsNumber} downloaded` })
              const items = transformData(data.items)
              exportData.push(...items)
            } else {
              condition = false
            }
          } else {
            condition = false
          }
        },
        app
      )
    }
  }
  exportXLS(exportData)
  dlg.hide()
  condition = false
}

const transformData = (items: any) => {
  const tempArr: any[] = []
  items.forEach((x: any, xIndex: string | number) => {
    const tempData = <any>{}
    props.modelValue.columns.forEach((y: { label: any; field: (arg0: any) => any; name: any; formatter: string }) => {
      const label = y.label
      const field = typeof y.field === 'function' ? y.name : y.field
      tempData[label] = items[xIndex][field]
      if (typeof tempData[label] === 'object') tempData[label] = JSON.stringify(tempData[label])
      if (typeof y.field === 'function') tempData[label] = y.field(x)
      if (Array.isArray(tempData[label])) tempData[label] = JSON.stringify(tempData[label])
      if (y.formatter) {
        const val = items[xIndex][field]
        if (y.formatter == 'float') tempData[label] = val ? parseFloat(val) : 0
        else if (y.formatter == 'integer') tempData[label] = val ? parseInt(val) : 0
        else if (y.formatter == 'date') tempData[label] = Helper.toDate(val, 'YYYY-MM-DD')
        else if (y.formatter == 'time') tempData[label] = Helper.toDate(val, 'HH:mm:ss')
        else if (y.formatter == 'datetime') tempData[label] = Helper.toDate(val, 'YYYY-MM-DD HH:mm:ss')
        else if (y.formatter == 'millis') tempData[label] = Helper.toDate(val, 'YYYY-MM-DD HH:mm:ss')
      }
    })
    tempArr.push(tempData)
  })
  return tempArr
}

// const exportXLS = (arrData: any) => {
//   const data = XLSX.utils.json_to_sheet(arrData)
//   const wb = XLSX.utils.book_new()
//   XLSX.utils.book_append_sheet(wb, data, 'data')
//   XLSX.writeFile(wb, `${props.meta.name}-table-export.xlsx`)
// }
const exportXLS = (arrData: any[]) => {
  if (!arrData.length) return

  const name = props.meta.title ?? props.meta.name
  const header = Object.keys(arrData[0] || {})
  const title = `${name} data export (${Helper.readDate(Helper.now(), true)})`.toUpperCase()

  const ws: any = {}

  // Build 3 sections (title, empty row, header + data)
  const dataWithHeader = [header, ...arrData.map((row) => header.map((h) => row[h] ?? ''))]

  XLSX.utils.sheet_add_aoa(ws, [[title]], { origin: 'A1' }) // title in first row
  XLSX.utils.sheet_add_aoa(ws, [[]], { origin: 'A2' }) // blank second row
  XLSX.utils.sheet_add_aoa(ws, dataWithHeader, { origin: 'A3' }) // header + data start from row 3

  // Title style
  const titleCell = ws['A1']
  if (titleCell) {
    titleCell.s = {
      font: { bold: true, sz: 16 },
      alignment: { horizontal: 'left', vertical: 'center' }
    }
  }
  // Header style (row 3)
  header.forEach((_, c) => {
    const cell = XLSX.utils.encode_cell({ r: 2, c })
    ws[cell].s = {
      font: { bold: true, color: { rgb: 'FFFFFF' } },
      fill: { fgColor: { rgb: '545454' } },
      alignment: { horizontal: 'center' }
    }
  })

  // Auto width (limit to first 50 rows)
  const sampleSize = Math.min(50, arrData.length)
  ws['!cols'] = header.map((h) => {
    const sample = arrData.slice(0, sampleSize)
    const maxLen = Math.max(h.length, ...sample.map((r) => String(r[h] ?? '').length))
    return { wch: maxLen + 2 }
  })

  // Freeze at 3rd row (header)
  ws['!freeze'] = { xSplit: 0, ySplit: 3 }

  // Export
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Data')
  XLSX.writeFile(wb, `${name} export - ${Helper.now()}.xlsx`)
}
// END OF EXPORT TABLE

// TABLE TEMPLATES | SHOW HIDE SORTING COLUMNS
const resetTemplate = () => {
  col_applied.value = []
  templates.value = templates.value.map((p) => ({ ...p, apply: false }))
  col_all.value.forEach((col) => {
    col.show = true
    col_applied.value.push(col)
  })
}

const addTemplate = (colsList: any[]) => {
  const list = colsList.filter((e) => e.show).map((e) => e.name)
  const template = { apply: true, name: 'new', value: list }
  templates.value.push(template)
  chooseTemplate(template, templates.value.length - 1)
}

const deleteTemplate = (i: number) => {
  templates.value.splice(i, 1)
}

const chooseTemplate = (template: any, i: number) => {
  templates.value = templates.value.map((p) => ({ ...p, apply: false }))
  templates.value[i].apply = true
  const choosen = template.value
  const colsList: any[] = []

  choosen.forEach((c: any) => {
    const col = col_all.value.find((e: { name: any }) => e?.name == c)
    if (col) {
      col.show = true
      colsList.push(col)
    }
  })

  const others = col_all.value.filter((e: { name: any }) => !choosen.includes(e.name))
  others.forEach((col: { show: boolean }) => {
    col.show = false
    colsList.push(col)
  })
  col_applied.value = colsList
}

const saveTemplate = () => {
  loading.value = true
  const update: string[] = []
  col_applied.value.forEach((e: { show: any; name: string }) => {
    if (e.show) update.push(e.name)
  })
  templates.value = templates.value.map((e) => (e.apply ? { ...e, value: update } : e))

  let insert = true
  let configs = props.tableConfigs?.map((e: { app: any; module: any }) => {
    if (e.app == props.meta.app && e.module == props.meta.module) {
      insert = false
      return { ...e, templates: templates.value }
    }
    return e
  })

  if (!configs) configs = []

  if (insert) configs.push({ app: props.meta.app, module: props.meta.module, templates: templates.value })

  API.put(
    'me/update',
    { table_configs: configs },
    (status: number, _data: any) => {
      if (status === 200) {
        SAuth.setTblConfigs(configs)
        setTimeout(() => {
          window.location.reload()
        }, 300)
      }
    },
    'main'
  )
}
// END OF TABLE TEMPLATES | SHOW HIDE SORTING COLUMNS

// const csvdelimiter = ';'
// const exportCsv = () => {
//   const ws = XLSX.utils.json_to_sheet(datatable.value.rows)
//   const csv = XLSX.utils.sheet_to_csv(ws, { FS: csvdelimiter })
//   exportFile(csv, `${props.meta.label}.csv`, 'csv')
// }

const openSettingDrawer = (type: 'settings' | 'summary') => {
  switch (type) {
    case 'settings':
      summaryModal.show = false
      modal.show = !modal.show
      break
    case 'summary':
      modal.show = false
      summaryModal.show = !summaryModal.show
      break
  }
}

const saveSummarySettings = () => {
  const new_summary_map: string[] = []

  summary_cols.value.forEach((col) => {
    if (col.selected && col.type) {
      new_summary_map.push(`${col.name}:${col.type}`)
    }
  })

  // Make sure to handle null/undefined cases
  const allSummaries = SAuth.getTblSummaries() || []
  let found = false

  const updatedSummaries = allSummaries.map((s: any) => {
    if (s.app === props.meta.app && s.module === props.meta.module) {
      found = true
      // Update existing entry
      return { ...s, summaries: new_summary_map }
    }
    return s
  })

  if (!found) {
    updatedSummaries.push({
      app: props.meta.app,
      module: props.meta.module,
      summaries: new_summary_map
    })
  }

  API.put(
    'me/update',
    { table_summaries: updatedSummaries },
    (status: number) => {
      if (status === 200) {
        SAuth.setTblSummaries(updatedSummaries)

        datatable.value.summary = new_summary_map.length > 0
        datatable.value.summary_map = new_summary_map
        emit('update:modelValue', datatable.value)
        emit('refreshEvent', false)

        Helper.showToast('Summary settings saved!')
        summaryModal.show = false
      }
    },
    'main'
  )
}

const updateTab = (value: string) => {
  tab.value = value
  emit('updateTab', value)
}

// MOUNTED | WATHCERS
onMounted(() => {
  init()
})

watch(
  () => props.modelValue,
  (newValue) => {
    datatable.value = newValue
  }
)

const showActionButtons = computed(() => {
  if (!props.meta || !datatable.value) return false

  const hasDelete =
    props.meta.permission?.delete &&
    datatable.value.selected?.length > 0

  const hasCreate =
    !props.trash &&
    props.meta.permission?.create

  return hasDelete || hasCreate || hasSlotButtons.value
})
</script>
