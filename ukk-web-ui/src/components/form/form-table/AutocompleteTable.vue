<template>
  <q-select
    dense
    v-model="selected"
    hide-bottom-space
    borderless
    class="form-select-sm q-px-sm"
    :placeholder="props.placeholder"
    use-input
    fill-input
    input-debounce="0"
    map-options
    :options="select.options"
    @filter="(val, update) => filterSelect(val, update)"
    @click="onClick"
    emit-value
    use-chips
    hide-selected
    hide-dropdown-icon
    @update:modelValue="emiters($event)"
    @new-value="createValue"
  >
    <template v-slot:no-option>
      <!-- <q-item>
        <q-item-section class="text-grey">Enter to add new data. | Entry 3 word to find previous data.</q-item-section>
      </q-item> -->
    </template>
  </q-select>
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
  placeholder?: string
  outlined?: boolean
  norules?: boolean
  hideBottomSpace?: boolean
  customOpt?: any[]
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

const filterSelect = async (val: string, update: (fn: () => void) => void) => {
  if (val == '' && startClick.value) {
    update(() => {})
    return
  } else startClick.value = false
  emiters(val)
  let opt: any[] = []
  if (props.customOpt && props.customOpt.length) opt = props.customOpt
  searchVal.value = val
  if (val.length > 2) {
    let ep = props.api?.indexOf('?') > -1 ? props.api : `${props.api}?`
    ep += `&group_select=${props.column}&like=${props.column}:${val}`
    await API.get(
      ep,
      (status: number, data: Option[]) => {
        if (status === 200 && data) {
          opt = [...(props.customOpt || []), ...data.filter((d) => !(props.customOpt || []).some((c) => c === d))]
        }
      },
      props.app
    )
    // console.log('opt', opt)
    update(() => {
      const s = val.toLowerCase()
      select.value.options = opt.filter((item) =>
        String(item || '')
          .toLowerCase()
          .includes(s)
      )
      // console.log('select_filter', select.value.options)
    })
  } else {
    update(() => {})
    // console.log('select', select.value.options)
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

onMounted(() => {
  const custom_opt = props.customOpt || []
  select.value.options.push(...custom_opt)
})
</script>
