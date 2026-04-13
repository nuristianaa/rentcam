<template>
  <q-input dense :modelValue="modelValue" :style="style" class="form-sm" borderless :readonly="readonly" :placeholder="placeholder" :mask="mask" :prefix="prefix" @update:modelValue="emiters($event)" @blur="emiterBlur" :outlined="props.outlined" autocomplete="off" autocorrect="off" spellcheck="false">
    <template v-slot:prepend>
      <slot name="prepend"></slot>
    </template>
    <template v-slot:append>
      <slot name="append"></slot>
    </template>
  </q-input>
</template>

<script setup lang="ts">
const props = defineProps<{
  modelValue: string | number | null | undefined
  style?: string
  placeholder?: string
  mask?: string
  prefix?: string
  readonly?: boolean
  outlined?: boolean
}>()

const emit = defineEmits(['update:modelValue', 'blur'])

const emiters = (e: string | number | null) => {
  emit('update:modelValue', e)
}

const emiterBlur = () => {
  emit('blur')
}
</script>
