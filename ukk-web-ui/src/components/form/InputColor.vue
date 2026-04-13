<template>
  <div :class="col ? `q-px-sm col-12 col-md-6 col-lg-${col}` : ''">
    <q-input
      dense
      :modelValue="modelValue"
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
      @update:modelValue="emiters($event)"
      @blur="emiterBlur"
      lazy-rules
      :rules="inputRules"
      :disable="disable"
      :error="error"
      :error-message="errorMessage"
    >
      <template v-slot:before>
        <slot name="before"></slot>
      </template>
      <template v-slot:prepend>
        <q-icon name="palette" :style="`color:${val ? val : '#000'};`" />
      </template>
      <template v-slot:append>
        <q-icon name="colorize" class="cursor-pointer">
          <q-popup-proxy cover transition-show="scale" transition-hide="scale">
            <q-color v-model="val" @update:modelValue="emiters($event)" />
          </q-popup-proxy>
        </q-icon>
      </template>
      <template v-slot:after>
        <slot name="after"></slot>
      </template>
    </q-input>
  </div>
</template>

<script setup lang="ts">
import validate from 'src/services/helper/validate'
import { computed, ref } from 'vue'

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
}>()

const val = ref(props.modelValue)

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
