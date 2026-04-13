<template>
  <q-select
    class="form-select-sm"
    dense
    behavior="menu"
    v-model="selected"
    :loading="loading"
    hide-bottom-space
    borderless
    input-debounce="0"
    :placeholder="placeholder"
    use-input
    fill-input
    map-options
    hide-selected
    :options="select.options"
    @filter="(val: any, update: any) => filterSelect(val, update)"
    :option-value="optionValue || 'id'"
    :option-label="optionLabel || ((v: { code: any; name: string }) => (v.code ? `${v.code} ${v.name ? '(' + v.name + ')' : ''}` : (v.name ?? v)))"
    :emit-value="raw ? false : true"
    @update:modelValue="emiters($event)"
    :hide-dropdown-icon="hideDropdownIcon"
    :clearable="props.clearable"
  >
    <template v-slot:no-option>
      <q-item>
        <q-item-section class="text-grey">No results</q-item-section>
      </q-item>
    </template>
    <template v-slot:prepend>
      <slot name="prepend"></slot>
    </template>
    <template v-slot:append>
      <slot name="append"></slot>
    </template>
    <template v-if="$slots.option" v-slot:option="scope">
      <slot name="option" v-bind="scope"></slot>
    </template>
  </q-select>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, watch, onMounted } from 'vue'

interface Option {
  id?: string | number
  code?: string
  name?: string
  [key: string]: any
}

const props = defineProps<{
  modelValue: any
  placeholder?: string
  options?: Option[]
  optionValue?: string
  optionLabel?: (option: Option) => string
  multiple?: boolean
  raw?: boolean
  api?: string
  app?: string
  clearable?: boolean
  hideDropdownIcon?: boolean
}>()

const emit = defineEmits(['update:modelValue', 'updateEvent'])

const API = new Api()
const loading = ref(true)
const selected = ref(props.modelValue)
const select = ref({
  options: [] as Option[],
  optionsTmp: [] as Option[] // Temporary storage for unfiltered options
})
const searchVal = ref<string | null>(null)

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

const emiters = (value: any) => {
  emit('update:modelValue', value)
  emit('updateEvent', value)
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

onMounted(() => {
  void loadSource()
})
</script>
