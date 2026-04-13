<template>
  <div :class="col ? `q-px-sm col-12 col-md-6 col-lg-${col}` : ''">
    <q-select
      v-if="!pickerMode"
      :ref="refs[refName]"
      dense
      v-model="selected"
      :loading="loading"
      :hide-bottom-space="hideBottomSpace"
      :borderless="borderless"
      :outlined="borderless ? false : true"
      :label="required ? `${label}*` : label"
      :class="boxClass"
      :style="style"
      :readonly="readonly"
      :placeholder="placeholder"
      :input-class="inputClass"
      :mask="mask"
      :prefix="prefix"
      :hint="hint"
      fill-input
      input-debounce="0"
      map-options
      :options="select.options"
      @filter="(val, update) => filterSelect(val, update)"
      :option-value="optValue"
      :option-label="optionLabel || ((v) => (v.code ? `${v.code} ${v.name ? '(' + v.name + ')' : ''}` : (v.name ?? v)))"
      :emit-value="raw ? false : true"
      :clearable="showClearable"
      :multiple="multiple"
      :use-chips="multiple"
      :hide-selected="!multiple"
      @blur="onBlur($event)"
      @update:modelValue="emiters($event)"
      :disable="disable"
      :popup-content-style="{ display: 'none' }"
      hide-dropdown-icon
      use-input
      @click="openPicker"
      @clear="handleClear"
      lazy-rules
      :rules="norules ? undefined : required ? [(val) => validate.validateRequired(val) || label + ' must be filled!'] : [(val) => val !== ' ' || 'clear space!']"
    >
      <template v-slot:no-option>
        <q-item>
          <q-item-section class="text-grey">No results</q-item-section>
        </q-item>
      </template>
      <template v-slot:prepend>
        <q-btn v-if="showRefresh" @click="loadSource" icon="refresh" flat size="sm" color="primary" dense round />
        <slot name="prepend"></slot>
      </template>
      <template v-slot:append>
        <slot name="append"></slot>
      </template>
      <template v-slot:after>
        <slot name="after"></slot>
      </template>
    </q-select>
  </div>

  <s-dialog v-model="dialog">
    <q-table dense flat :filter="table.search" :rows="select.options" :columns="tableColumns" :row-key="optionValue" :selected-rows-label="getSelectedString" :selection="multiple ? 'multiple' : 'single'" v-model:selected="table.selected" :pagination="{ rowsPerPage: 10 }">
      <template v-slot:top-right>
        <q-input filled dense debounce="300" v-model="table.search" placeholder="Search..." clearable>
          <template v-slot:append>
            <q-icon name="search" />
          </template>
          <template v-slot:after>
            <q-btn unelevated label="Choose" no-caps color="primary" class="text-bold" size="md" @click="onChoosed" />
          </template>
        </q-input>
      </template>
    </q-table>
    <div v-if="!pickerMode && selected">
      <b>Choosed :</b>
      <template v-if="multiple">
        <q-badge v-for="(v, i) in selected" :key="i" class="q-ml-xs">{{ v }}</q-badge>
        &nbsp;
      </template>
      <q-badge v-else>{{ selected }}</q-badge>
    </div>
  </s-dialog>
  <slot name="trigger" :show="dialog.show" :openPicker="openPicker"></slot>
</template>

<script setup lang="ts">
import { uid } from 'quasar'
import Api from 'src/services/api'
import validate from 'src/services/helper/validate'
import { ref, watch, onMounted, computed, onBeforeMount } from 'vue'
import type { Dialog } from 'src/services/handler'
import { Helper } from 'src/services/helper'

type Column = {
  name: string
  label: string
  align?: string
  field?: string | ((row: any) => any)
  sortable?: boolean
  format?: (val: any) => any
  [key: string]: any
}

type CustomColumnInput = string | { [key: string]: (col: Column) => Column }

interface Option {
  id?: string | number
  code?: string
  name?: string
  [key: string]: any
}

const props = defineProps<{
  modelValue?: any
  col?: string
  boxClass?: string
  inputClass?: string
  style?: string
  label?: string
  placeholder?: string
  mask?: string
  prefix?: string
  hint?: string
  required?: boolean
  readonly?: boolean
  borderless?: boolean
  norules?: boolean
  hideBottomSpace?: boolean
  options?: Option[]
  optionValue?: string
  optionLabel?: (option: Option) => string
  multiple?: boolean
  raw?: boolean
  mustFill?: boolean
  api?: string
  app?: string
  showRefresh?: boolean
  defaultData?: any
  disable?: boolean
  pickerMode?: boolean
  title?: string
  columns?: CustomColumnInput[]
  hideOptions?: any[]
}>()

const dialog = ref<Dialog>({
  show: false,
  type: 'form',
  title: props?.title || 'Picker',
  props: null,
  maximize: false,
  persistent: false
})

const emit = defineEmits(['update:modelValue', 'updateEvent', 'choosed', 'choosedRaw', 'blur'])
const onBlur = (evt: any) => {
  emit('blur', selected.value, evt)
}
const API = new Api()
const loading = ref(true)
const selected = ref(props.modelValue)
const select = ref({
  options: [] as Option[],
  optionsTmp: [] as Option[] // Temporary storage for unfiltered options
})
const searchVal = ref<string | null>(null)
const refs: any = {}
const table = ref({
  search: '',
  selected: [] as Option[]
})

const showClearable: any = computed(() => {
  let res: any = !props.multiple && !props.mustFill ? true : false
  if (props.required) res = false
  return res
})

const refName = computed(() => {
  let res = 'SLC_'
  if (props.label) res = props.label
  res = uid() + '_' + res.toLowerCase()
  res = res.replace(/ /g, '_').replace(/-/g, '_')
  return res
})

const optValue: any = computed(() => {
  return props?.optionValue || 'id'
})

const processColumns = (defaultColumns: Column[], customColumns: CustomColumnInput[]): Column[] =>
  customColumns.map((col) => {
    if (typeof col === 'string') {
      const found = defaultColumns.find((c) => c.name === col)
      if (found) return found
      return {
        name: col,
        label: Helper.slug2label(col),
        align: 'left',
        field: col,
        sortable: true
      }
    }
    if (typeof col === 'object') {
      const key: any = Object.keys(col)[0]
      const callback: any = col[key]
      let baseCol = defaultColumns.find((c) => c.name === key)
      if (!baseCol) {
        baseCol = {
          name: key,
          label: Helper.slug2label(key),
          align: 'left',
          field: key,
          sortable: true
        }
      }
      return callback(baseCol)
    }
    return col as Column
  })

const tableColumns: any = computed(() => {
  let defaultCols: Column[] = []

  if (select.value.options.length) {
    const obj: any = select.value.options[0]
    defaultCols = Helper.object2columns(obj, ['id'])
  }

  if (props.columns && Array.isArray(props.columns)) {
    return processColumns(defaultCols, props.columns)
  }

  return defaultCols
})

watch(
  () => props.options,
  (newOptions) => {
    if (newOptions && (!searchVal.value || searchVal.value === '')) {
      select.value.options = select.value.optionsTmp = newOptions
    }
  }
)

watch(
  () => props.modelValue,
  (newValue) => {
    selected.value = newValue
    searchVal.value = null
  }
)

watch(
  () => props.defaultData,
  (dd) => {
    select.value.options = []
    if (dd) select.value.options.push(dd)
  }
)

const emiters = (value: any) => {
  if (!props.pickerMode) {
    emit('update:modelValue', value)
    emit('updateEvent', value)
  }
  emit('choosed', value)
}

const filterSelect = (val: string, update: (fn: () => void) => void) => {
  searchVal.value = val
  if (val === '') {
    update(() => {
      select.value.options = select.value.optionsTmp
    })
    return
  }
  update(() => {
    const needle = val.toLowerCase()
    select.value.options = select.value.optionsTmp.filter((option) => JSON.stringify(option).toLowerCase().includes(needle))
  })
}

const loadSource = async () => {
  let options: Option[] = []
  if (props.api) {
    const endpoint = props.api.includes('?') ? `${props.api}&limit=0` : `${props.api}?limit=0`
    await API.get(
      endpoint,
      (status: number, data: Option[]) => {
        if (status === 200) options = data
      },
      props.app
    )
  } else if (props.options) {
    options = props.options
    if (options.length === 1 && typeof options[0] === 'string') emiters(options[0])
  }
  select.value.options = select.value.optionsTmp = options
  selected.value = props.modelValue
  loading.value = false
}

const openPicker = () => {
  select.value.options = select.value.optionsTmp

  if (props.pickerMode) {
    selected.value = props.multiple ? [] : null
    table.value.selected = []
  }
  handleHideOptions()
  handleSelected()
  dialog.value.show = !dialog.value.show
}

const getSelectedString = () => {
  const selected = table.value.selected
  return selected.length === 0 ? '' : `${selected.length} record${selected.length > 1 ? 's' : ''} selected of ${select.value.options.length}`
}

const onChoosed = () => {
  if (!table.value.selected.length) return false
  emit('choosedRaw', table.value.selected)
  let finalValue: any = table.value.selected.map((r: any) => {
    return r[optValue.value]
  })
  if (!props.multiple && finalValue.length) finalValue = finalValue[0]

  selected.value = finalValue
  emiters(selected.value)
  dialog.value.show = false
}

const handleClear = () => {
  table.value.selected = []
}

const handleSelected = () => {
  const key: any = props.optionValue
  let val: any = selected.value
  const fix: any[] = []
  // console.log('va;', val)
  if (props.multiple) {
    if (val && !val.length) return false
  } else {
    if (!val) return false
    val = [val] // pastikan val array
  }

  if (Array.isArray(val) && key) {
    val.forEach((v) => {
      // cari item di options berdasarkan key dan nilai v
      const found = select.value.options.find((item) => item[key] === v)
      if (found) {
        fix.push(found)
      } else {
        // jika tidak ditemukan, buat objek baru hanya dengan key: v
        fix.push({ [key]: v })
      }
    })
  } else {
    console.warn('failed setter: handleSelected - val bukan array atau key kosong')
  }

  table.value.selected = fix
  return fix
}

const hidingOptions = (options: any = [], hideOptions: any = [], key: any = null) => {
  // console.log('hidingOptions', { key, options, hideOptions })
  if (!key) return options
  const hideValues = hideOptions.map((item: any) => item[key])
  return options.filter((item: any) => !hideValues.includes(item[key]))
}

const handleHideOptions = () => {
  // console.log('hiding opt')
  if (!props.hideOptions?.length) {
    select.value.options = select.value.optionsTmp
    return select.value.options
  }

  const hide = props.hideOptions.map((r: any) => {
    return { [`${props.optionValue}`]: r }
  })
  select.value.options = hidingOptions(select.value.options, hide, props.optionValue)
}

onBeforeMount(() => {
  refs[refName.value] = ref(1) // init refs
})

onMounted(() => {
  void loadSource()
})
</script>
