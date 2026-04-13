<template>
  <div :class="`f-toggle ${col ? `q-px-md col-12 col-md-6 col-lg-${col}` : ''}`">
    <span v-if="label" class="text-bold label" style="margin-right: 10px">
      {{ required ? `${label}*` : label }}
      <span v-if="label">:</span>
    </span>
    <q-btn-toggle
      v-if="isButton"
      v-model="dataModel"
      :borderless="borderless"
      :outlined="borderless ? false : true"
      :class="boxClass"
      :style="style"
      :readonly="readonly"
      :placeholder="placeholder"
      :input-class="inputClass"
      :mask="mask"
      :hint="hint"
      :toggle-color="toggleColor"
      :options="optionList"
      :spread="spread || false"
      @update:model-value="handleUpdate"
      :size="size || 'sm'"
      :no-caps="noCaps"
    >
      <q-tooltip v-if="tooltip">{{ tooltip }}</q-tooltip>
    </q-btn-toggle>
    <q-toggle v-else v-model="dataModel" checked-icon="check" unchecked-icon="clear" :false-value="falseValue" :true-value="trueValue" :class="boxClass" :style="style" :size="size || 'xs'" :readonly="readonly" :toggle-color="toggleColor" @update:model-value="handleUpdate">
      <q-tooltip v-if="tooltip">{{ tooltip }}</q-tooltip>
    </q-toggle>
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import validate from 'src/services/helper/validate'
import { ref, computed, watch } from 'vue'

interface Options {
  [props: string]: any
  attrs?: any
  label?: string
  icon?: string
  value: any
  slot?: string
}

const props = defineProps({
  modelValue: { required: true },
  col: { type: String, default: '' },
  boxClass: { type: String, required: false },
  inputClass: { type: String, required: false },
  style: { type: String, default: '' },
  label: { type: String, required: false },
  placeholder: { type: String, required: false },
  mask: { type: String, required: false },
  hint: { type: String, required: false },
  required: { type: Boolean, required: false },
  readonly: { type: Boolean, required: false },
  borderless: { type: Boolean, required: false },
  norules: { type: Boolean, required: false },
  isButton: { type: Boolean, default: true },
  options: {
    type: Array<Options>,
    default: () => [
      { value: true, label: 'Yes' },
      { value: false, label: 'No' }
    ]
  },
  tooltip: { type: String },
  size: { type: String },
  spread: { type: Boolean },
  toggleColor: { type: String, default: 'primary' },
  activeMode: { type: Boolean },
  noCaps: { type: Boolean, default: false }
})

const optionList = computed(() => {
  let res = []
  res = [
    { value: true, label: 'Yes' },
    { value: false, label: 'No' }
  ]
  if (props.options) res = props.options
  if (props.activeMode) {
    res = [
      { value: true, label: 'ACTIVE' },
      { value: false, label: 'INACTIVE' }
    ]
  }
  return res
})

const emit = defineEmits(['updateEvent', 'update:modelValue'])

const dataModel = ref(props.modelValue)

const trueValue = computed(() => {
  let value: number | boolean = true
  if (Number.isInteger(dataModel.value)) value = 1
  return value
})

const falseValue = computed(() => {
  let value: number | boolean = false
  if (Number.isInteger(dataModel.value)) value = 0
  return value
})

watch(
  () => props.modelValue,
  (newValue) => {
    dataModel.value = newValue
  }
)

const handleUpdate = (value: any) => {
  dataModel.value = value
  emit('update:modelValue', value)
  emit('updateEvent', value)
}
</script>
