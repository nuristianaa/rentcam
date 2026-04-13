<template>
  <div class="fm-colored-input">
    <div
      :class="{
        'fm-colored-input__wrapper--focused': isFocused
      }"
      class="fm-colored-input__wrapper"
    >
      <textarea ref="textareaRef" v-model="model" class="fm-colored-input__textarea" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" rows="1" @focus="isFocused = true" @blur="onBlur" />
      <div class="fm-colored-input__highlight">
        <span v-for="(highlightEntry, highlightEntryIndex) in highlight" :key="highlightEntry.value + highlightEntryIndex" :class="highlightEntry.css">
          {{ highlightEntry.value }}
        </span>
      </div>
    </div>
    <div v-if="props.validationErrors?.length" class="fm-colored-input__validation">
      {{ props.validationErrors?.map((error) => error.errorType).join(', ') }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onBeforeUnmount } from 'vue'
import type { Token, ValidationError } from 'src/services/formula-parser'

type Props = {
  modelValue: string
  tokens?: Token[]
  validationErrors?: ValidationError[]
}

const props = defineProps<Props>()
const emit = defineEmits(['update:model-value', 'blur'])
const isFocused = ref(false)
const model = ref('')
const textareaRef = ref<HTMLTextAreaElement>()

const highlight = computed(() => {
  const errorsByTokenIndexes = props.validationErrors?.reduce((out: Record<number, boolean>, error) => {
    if (error.tokenIndex || error.tokenIndex === 0) {
      out[error.tokenIndex] = true
    }
    return out
  }, {})
  return props.tokens?.map((token, tokenIndex) => ({
    value: token.value,
    css: `fm-colored-input__highlight--${token.type}` + (errorsByTokenIndexes?.[tokenIndex] ? ' fm-colored-input__highlight--error' : '')
  }))
})

const updateHeight = () => {
  const el = textareaRef.value
  if (el) {
    el.style.height = 'auto'
    el.style.height = el.scrollHeight + 'px'
  }
}

const onBlur = () => {
  isFocused.value = false
  emit('blur', model.value)
}

watch(
  () => props.modelValue,
  (value) => {
    model.value = value
  },
  { immediate: true }
)

watch(
  model,
  (value) => {
    emit('update:model-value', value)
    updateHeight()
  },
  { immediate: true }
)

const resizeObserver = new ResizeObserver(() => {
  requestAnimationFrame(() => {
    updateHeight()
  })
})

watch(textareaRef, (value, oldValue) => {
  if (oldValue) resizeObserver.unobserve(oldValue)
  if (value) resizeObserver.observe(value)
})

onBeforeUnmount(() => {
  resizeObserver.disconnect()
})
</script>
