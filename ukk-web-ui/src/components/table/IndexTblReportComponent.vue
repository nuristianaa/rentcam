<template>
  <q-table
    flat
    bordered
    virtual-scroll
    binary-state-sort
    :wrap-cells="props.wrapCells"
    :row-key="rowKey ?? 'id'"
    :rows="props.modelValue"
    :columns="props.columns"
    :rows-per-page-options="[0]"
    dense
    :filter="search"
    class="q-pb-md sticky-table"
    :style="`${props.style ? props.style : ''} ${heightTable}`"
    :selection="selection ? 'multiple' : 'none'"
    v-model:selected="selectedData"
  >
    <template v-slot:top>
      <slot name="top" :exportTable="exportTable">
        <div class="row q-my-sm">
          <!-- TOP LEFT | TITLE -->
          <div class="row q-gutter-sm">
            <q-input class="form-sm" outlined dense debounce="300" v-model="search" placeholder="Search">
              <template v-slot:append>
                <q-icon name="search" />
              </template>
            </q-input>
            <q-btn v-if="!noExport" dense flat color="primary" icon="archive" @click="exportTable" label="Export" />
          </div>
          <q-space />
          <slot name="top-left"></slot>
        </div>
        <q-space />
        <slot name="top-right"></slot>
      </slot>
    </template>

    <template v-for="col in cols" :key="col" v-slot:[`header-cell-${col}`]="props">
      <q-th :props="props">
        <slot :name="`header-cell-${col}`" :props="props">
          {{ props.col.label }}
        </slot>
      </q-th>
    </template>

    <template v-for="col in cols" :key="col" v-slot:[`body-cell-${col}`]="props">
      <q-td :props="props" :style="props.col.style" :class="`${getTdClass?.(props)} ${props.col.tdClass ? props.col.tdClass : ''} `">
        <slot :name="`body-cell-${col}`" :props="props">
          <span v-if="props.col.formatter">
            <span v-if="props.col.formatter == 'integer'">{{ Helper.formatNumber(props.value, 0) }}</span>
            <span v-else-if="props.col.formatter == 'float'">{{ Helper.formatNumber(props.value) }}</span>
            <span v-else-if="props.col.formatter == 'tonnage'">{{ Helper.formatNumber(props.value, props.col?.precision ? props.col.precision : 3) }}</span>
            <span v-else-if="props.col.formatter == 'accounting'">{{ Helper.formatNumberAccounting(props.value, props.col?.precision ? props.col.precision : 3) }}</span>
            <span v-else-if="props.col.formatter == 'boolean'" :class="props.value ? 'text-positive' : 'text-negative'">{{ props.value }}</span>
            <span v-else-if="props.col.formatter == 'date'">{{ Helper.readDate(props.value) }}</span>
            <span v-else-if="props.col.formatter == 'datetime'">{{ Helper.readDate(props.value, true) }}</span>
            <span v-else-if="props.col.formatter == 'time'">{{ Helper.toDate(props.value, 'HH:mm:ss') }}</span>
            <span v-else-if="props.col.formatter == 'millis'">{{ Helper.readDate(props.value, true) }}</span>
            <span v-else>{{ props.value }}</span>
          </span>
          <span v-else>{{ props.value }}</span>
        </slot>
      </q-td>
    </template>
  </q-table>
</template>

<script setup lang="ts">
import * as XLSX from 'xlsx'
import { onMounted, ref, watch, computed } from 'vue'
import { exportFile } from 'quasar'
import { Helper } from 'src/services/helper'
import { Constant } from 'src/services/constant'

const props = defineProps<{
  columns: any
  modelValue: any
  meta?: any
  wrapCells?: boolean
  noExport?: boolean
  selection?: boolean
  rowKey?: string
  search?: string
  height?: string
  style?: string
  selected?: any
  getTdClass?: (props: any) => string
}>()

const emit = defineEmits(['selected'])

const datatable = ref(props.modelValue)
const csvdelimiter = ';'
const cols = ref<Array<string>>([])
const search = ref<any>(props.search)
const selectedData = ref<any>([])

watch(
  () => props.search,
  (s) => {
    if (s) search.value = props.search
    else search.value = null
  }
)

watch(
  () => props.selected,
  (s) => {
    selectedData.value= s
  }
)

watch(
  () => selectedData.value,
  (val) => {
    // console.log('sel', val)
    emit('selected', val)
  }
)

const heightTable = computed(() => {
  let res = ''
  if (props.height) res = ` height: ${props.height};`
  return res
})

const handleTable = () => {
  props.columns.forEach((e: { name: string }) => {
    // if (e.name !== 'action')
    cols.value.push(e.name)
  })
}

// EXPORT TABLE
const exportTable = () => {
  Helper.confirm('Click "OK" to export Excel file.', (result: boolean) => {
    if (result) exportXLS()
  })
}

const exportXLS = () => {
  const tempArr: any[] = []
  props.modelValue.forEach((x: any, xIndex: string | number) => {
    const tempData = <any>{}
    props.columns.forEach((y: { label: any; field: (arg0: any) => any; name: any; formatter: string }) => {
      const label = y.label
      const field = typeof y.field === 'function' ? y.name : y.field
      tempData[label] = props.modelValue[xIndex][field]
      if (typeof tempData[label] === 'object') tempData[label] = JSON.stringify(tempData[label])
      if (typeof y.field === 'function') tempData[label] = y.field(x)
      if (Array.isArray(tempData[label])) tempData[label] = JSON.stringify(tempData[label])
      if (y.formatter) {
        const val = props.modelValue[xIndex][field]
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
  const data = XLSX.utils.json_to_sheet(tempArr)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, data, 'data')
  XLSX.writeFile(wb, `${props.meta?.name ?? 'Report'}-table-export.xlsx`)
}
// END OF EXPORT TABLE

onMounted(() => {
  handleTable()
})
</script>
