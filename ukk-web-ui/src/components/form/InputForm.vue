<template>
  <div :class="col ? `q-px-sm col-12 col-md-6 col-lg-${col}` : ''">
    <div class="q-mb-md column">
      <label class="text-subtitle2 text-grey q-ml-sm">{{ required ? `${label}*` : label }}</label>
      <q-input
        dense
        :modelValue="modelValue"
        :hide-bottom-space="hideBottomSpace"
        :outlined="!borderless"
        :readonly="readonly"
        :placeholder="placeholder"
        @update:modelValue="emiters($event)"
        @blur="emiterBlur"
        :clearable="clearable"
        lazy-rules
        :rules="inputRules"
        :disable="disable"
        :error="error"
        :error-message="errorMessage"
      >
        <template v-slot:prepend>
          <slot name="prepend"></slot>
        </template>
        <template v-slot:before>
          <slot name="before"></slot>
        </template>
        <template v-slot:append>
          <slot name="append"></slot>
        </template>
        <template v-slot:after>
          <slot name="after"></slot>
        </template>
      </q-input>
    </div>

  </div>
</template>

<script setup lang="ts">
import validate from 'src/services/helper/validate'
import { computed } from 'vue'

const props = defineProps<{
  modelValue: string | number | null | undefined
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
  disable?: boolean
  error?: boolean
  errorMessage?: string
  clearable?: boolean
}>()

const emit = defineEmits(['update:modelValue', 'blur'])

const emiters = (e: string | number | null) => {
  emit('update:modelValue', e)
}

const emiterBlur = () => {
  emit('blur')
}

const inputRules = computed(() => {
  if (props.norules) return undefined

  const rules = []

  if (props.required) {
    rules.push((val: any) => validate.validateRequired(val) || `${props.label} must be filled!`)
  } else {
    rules.push((val: any) => val !== ' ' || 'Clear space!')
  }

  return rules
})
</script>
