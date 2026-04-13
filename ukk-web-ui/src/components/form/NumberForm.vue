<template>
  <div :class="col ? `q-px-sm col-12 col-md-6 col-lg-${col}` : ''">
    <label class="text-subtitle2 text-grey q-ml-sm">
      {{ required ? `${label}*` : label }}
    </label>
    <q-input
      dense
      reverse-fill-mask
      :modelValue="onkey ? dataModel : dataFormatted"
      :hide-bottom-space="props.hideBottomSpace"
      :borderless="borderless"
      :outlined="borderless ? false : true"
      :class="boxClass"
      :style="style"
      :readonly="readonly"
      :placeholder="placeholder"
      :input-class="inputClass ?? 'text-right'"
      :mask="mask"
      :prefix="prefix"
      :hint="hint"
      @update:modelValue="emiters($event)"
      @blur="emiterBlur($event)"
      @keyup="onkey = true"
      @click="onkey = true"
      lazy-rules
      :rules="fixRules"
      :type="free ? 'number' : undefined"
    >
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
    </q-input>
  </div>
</template>

<script setup lang="ts">
import { Constant } from 'src/services/constant'
import { Helper } from 'src/services/helper'
import validate from 'src/services/helper/validate'
import { ref, watch, computed } from 'vue'

const props = defineProps<{
  modelValue: string | number | null
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
  rules?: any
  currency?: boolean
  free?: boolean
  precision?: number
  hideBottomSpace?: boolean
}>()

const emit = defineEmits(['update:modelValue', 'blur', 'updateEvent'])

const dataModel = ref<string | number | null>(props.modelValue)
const dataFormatted = ref<string | null>(null)
const onkey = ref(false)
const rounding = ref<number>(5)

const fixRules = computed(() => {
  let res = props.norules ? undefined : props.required ? [(val: any) => validate.validateNumber(val, props.required) || props.label + ' must be filled!'] : [(val: any) => val != ' ' || 'clear space!']
  if (props.rules) res = props.rules
  return res
})

const updateFormattedValue = () => {
  if (props.free) {
    dataFormatted.value = dataModel.value as string | null
  } else if (props.currency) {
    dataFormatted.value = Helper.formatMoney(dataModel.value)
    rounding.value = Constant.moneyPrecision
  } else {
    dataFormatted.value = Helper.formatNumber(dataModel.value, props.precision)
    if (props.precision !== undefined) rounding.value = props.precision
    else rounding.value = Constant.numberPrecision
  }
}

const emiters = (e: string | number | null) => {
  let withoutSeparator = e
  if (typeof withoutSeparator == 'string') withoutSeparator = Helper.replace(',', '', withoutSeparator)
  withoutSeparator = safeParseFloat(withoutSeparator)
  emit('update:modelValue', withoutSeparator)
}

const safeParseFloat = (value: string | number | null, withRounding: boolean = false) => {
  if (value != null) {
    const val = parseFloat(value.toString())
    if (!isNaN(val)) {
      if (withRounding) {
        const factor = 10 ** rounding.value
        return Math.round(val * factor) / factor
      } else {
        return val
      }
    }
  }
  // console.error("Invalid input: Not a number")
  return null
}

const emiterBlur = (_e: Event) => {
  let withoutSeparator = dataModel.value
  if (typeof withoutSeparator == 'string') withoutSeparator = Helper.replace(',', '', withoutSeparator)
  withoutSeparator = safeParseFloat(withoutSeparator, true)
  emit('update:modelValue', withoutSeparator)
  emit('updateEvent', withoutSeparator)
  emit('blur')
  onkey.value = false
}

watch(
  () => props.modelValue,
  (newValue) => {
    dataModel.value = newValue
    updateFormattedValue()
  }
)
updateFormattedValue()
</script>
