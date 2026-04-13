<template>
  <div :class="col ? `q-px-sm col-12 col-md-6 col-lg-${col}` : ''">
    <label class="text-subtitle2 text-grey q-ml-sm">
      {{ required ? `${label}*` : label }}
    </label>

    <q-select
      dense
      behavior="menu"
      v-model="selected"
      :loading="loading"
      :hide-bottom-space="hideBottomSpace"
      :borderless="borderless"
      :outlined="!borderless"
      :class="`${boxClass} ${uppercase ? 'select-uppercase' : ''}`"
      :style="style"
      :popup-content-class="`${uppercase ? 'select-uppercase-options' : ''}`"
      :readonly="readonly"
      :placeholder="placeholder"
      :input-class="inputClass"
      :mask="mask"
      :prefix="prefix"
      :hint="hint"
      use-input
      :fill-input="!autocomplete"
      input-debounce="0"
      map-options
      :options="select.options"
      @filter="(val: any, update: any) => filterSelect(val, update)"
      :option-value="optionValue || 'id'"
      :option-label="optionLabel || ((v) => (v.code ? `${v.code} ${v.name ? '(' + v.name + ')' : ''}` : (v.name ?? v)))"
      :emit-value="raw ? false : true"
      :clearable="showClearable"
      :multiple="multiple"
      :use-chips="useChip"
      :hide-selected="!useChip"
      @update:modelValue="emiters($event)"
      @blur="onBlur($event)"
      :disable="disable"
      :hide-dropdown-icon="hideDropdownIcon"
      @new-value="createValue"
      lazy-rules
      :rules="norules ? undefined : required ? [(val: any) => validate.validateRequired(val) || label + ' must be filled!'] : [(val) => val !== ' ' || 'clear space!']"
    >
      <template v-slot:no-option>
        <q-item>
          <q-item-section class="text-grey">{{ autocomplete ? 'Enter to create new' : 'No results' }}</q-item-section>
        </q-item>
      </template>

      <template v-slot:before>
        <slot name="before"></slot>
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

      <template v-if="$slots.option" v-slot:option="scope">
        <slot name="option" v-bind="scope"></slot>
      </template>
    </q-select>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import validate from 'src/services/helper/validate'
import { ref, watch, onMounted, computed } from 'vue'

interface Option {
  id?: string | number
  code?: string
  name?: string
  [key: string]: any
}

// const props = defineProps<{
//   modelValue: any
//   col?: string
//   boxClass?: string
//   inputClass?: string
//   style?: string
//   label?: string
//   placeholder?: string
//   mask?: string
//   prefix?: string
//   hint?: string
//   required?: boolean
//   readonly?: boolean
//   borderless?: boolean
//   norules?: boolean
//   hideBottomSpace?: boolean
//   options?: Option[]
//   optionValue?: string
//   optionLabel?: (option: Option) => string | string
//   multiple?: boolean
//   raw?: boolean | false
//   mustFill?: boolean
//   api?: string
//   app?: string
//   showRefresh?: boolean
//   defaultData?: any
//   disable?: boolean
//   hideDropdownIcon?: boolean
//   hideClearable?: boolean
//   autocomplete?: boolean
//   uppercase?: boolean | false
// }>()

interface Props {
  modelValue: any
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
  hideDropdownIcon?: boolean
  hideClearable?: boolean
  autocomplete?: boolean
  uppercase?: boolean
  autoFill?: boolean //to set the value of select when options length 1
}

const props = withDefaults(defineProps<Props>(), {
  raw: false,
  uppercase: false,
  required: false,
  readonly: false,
  borderless: false,
  norules: false,
  hideBottomSpace: false,
  multiple: false,
  disable: false,
  hideDropdownIcon: false,
  hideClearable: false,
  autocomplete: false,
  autoFill: true
})

const emit = defineEmits(['update:modelValue', 'updateEvent', 'newValue', 'selected', 'blur', 'loaded'])

const API = new Api()
const loading = ref(true)
const selected = ref(props.modelValue)
const select = ref({
  options: [] as Option[],
  optionsTmp: [] as Option[] // Temporary storage for unfiltered options
})
const searchVal = ref<string | null>(null)

const showClearable: any = computed(() => {
  let res: any = !props.multiple && !props.mustFill ? true : false
  if (props.required) res = false
  if (props.hideClearable) res = false
  return res
})

const useChip = computed(() => {
  let res = props.multiple ? true : false
  if (props.autocomplete) res = true
  return res
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

const getRawSelected = (val: any) => {
  if (!val) return null

  const src = JSON.parse(JSON.stringify(select.value.options))
  const key = props.optionValue || 'id'
  const list = src.filter((r: any) => r[key] === val)
  if (!list.length) return null
  else return list[0]
}

const emiters = (value: any) => {
  emit('update:modelValue', value)
  emit('updateEvent', value)
  emit('selected', getRawSelected(value))
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
    if (options.length === 1 && typeof options[0] === 'string' && props.autoFill) emiters(options[0])
  }
  select.value.options = select.value.optionsTmp = options
  selected.value = props.modelValue
  loading.value = false

  emit('loaded', options)
}

const onBlur = (evt: any) => {
  emit('blur', selected.value, evt)
}

const createValue = (val: any, done: any) => {
  if (!props.autocomplete) return false
  done(val, 'add-unique')
  emit('newValue', val)
}

onMounted(() => {
  void loadSource()
})
</script>
