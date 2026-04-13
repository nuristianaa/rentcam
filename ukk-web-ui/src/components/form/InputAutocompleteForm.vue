<template>
  <div :class="col ? `q-px-sm col-12 col-md-6 col-lg-${col}` : ''">
    <label class="text-subtitle2 text-grey q-ml-sm">{{ required ? `${label}*` : label }}</label>
    <q-select
      dense
      v-model="selected"
      :hide-bottom-space="hideBottomSpace"
      :borderless="borderless"
      :outlined="borderless ? false : true"
      :class="props.class"
      :style="style"
      :readonly="readonly"
      :placeholder="placeholder"
      :input-class="inputClass"
      :mask="mask"
      :prefix="prefix"
      :hint="hint"
      use-input
      fill-input
      input-debounce="0"
      map-options
      :options="select.options"
      @filter="(val, update) => onFilter(val, update)"
      emit-value
      use-chips
      hide-selected
      hide-dropdown-icon
      @update:modelValue="emiters($event)"
      @new-value="createValue"
      lazy-rules
      :rules="norules ? undefined : required ? [(val) => validate.validateRequired(val) || label + ' must be filled!'] : [(val) => val !== ' ' || 'clear space!']"
      @click="onClick"
      @keydown="onKeyDown"
    >
      <template v-slot:no-option>
        <q-item v-if="!modelValue">
          <q-item-section class="text-grey">Entry min 2 word to find previous data.</q-item-section>
        </q-item>
      </template>
      <template v-slot:before>
        <slot name="before"></slot>
      </template>
      <template v-slot:prepend>
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

const props = defineProps<{
  modelValue: any
  api: string
  app: string
  column: string
  col?: string
  class?: string
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
}>()

const emit = defineEmits(['update:modelValue', 'updateEvent', 'newValue', 'selected'])

const API = new Api()
const selected = ref(props.modelValue)
const select = ref({
  options: [] as any[]
})
const searchVal = ref<string | null>(null)
const startClick = ref(false)

watch(
  () => props.modelValue,
  (newValue) => {
    selected.value = newValue
    searchVal.value = null
  }
)

const emiters = (value: any) => {
  emit('update:modelValue', value)
}

let filterTimeout: any = null
const onFilter = (val: string, update: (fn: () => void) => void) => {
  if (filterTimeout) clearTimeout(filterTimeout)

  filterTimeout = setTimeout(() => {
    filterSelect(val, update)
  }, 500) // 0.5 second
}

const filterSelect = async (val: string, update: (fn: () => void) => void) => {
  if (val == '' && startClick.value) {
    update(() => {})
    return
  } else startClick.value = false
  // console.log(val)
  emiters(val)
  let opt: any[] = []
  searchVal.value = val
  if (val.length > 1) {
    let ep = props.api?.indexOf('?') > -1 ? props.api : `${props.api}?`
    ep += `&group_select=${props.column}&like=${props.column}:${val}`
    await API.get(
      ep,
      (status: number, data: Option[]) => {
        if (status === 200 && data) opt = data
      },
      props.app
    )
    update(() => {
      select.value.options = opt
    })
  } else {
    update(() => {})
  }
}

const createValue = (val: any, done: any) => {
  done(val, 'add-unique')
  emit('newValue', val)
}

const onClick = (e: any) => {
  startClick.value = true
  // console.log('click: ', startClick.value)
}

const onKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Backspace') startClick.value = false
  // console.log('keydown: ', startClick.value)
}

onMounted(async () => {
  // let options: Option[] = []
  // if (props.api) {
  //   const endpoint = props.api.includes('?') ? `${props.api}&limit=0` : `${props.api}?limit=0`
  //   await API.get(endpoint, (status: number, data: Option[]) => {
  //     if (status === 200) options = data
  //   }, props.app)
  // } else if (props.options) {
  //   options = props.options
  //   if (options.length === 1 && typeof options[0] === 'string') emiters(options[0])
  // }
  // select.value.options = select.value.optionsTmp = options
  // selected.value = props.modelValue
  // loading.value = false
})
</script>
