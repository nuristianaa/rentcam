<template>
  <q-tabs v-model="tabValue" dense shrink inline-label align="left" mobile-arrows swipeable narrow-indicator breakpoint="600" :class="Dark.isActive ? 'text-grey-2' : 'text-grey-9'" active-class="bg-primary-black text-white" :indicator-color="Dark.isActive ? 'white' : 'dark'" @update:model-value="onUpdateTab">
    <div v-for="(val, i) in tabs" :key="i">
      <q-tab :name="val?.name ?? val" :label="val?.label ?? val" />
    </div>
  </q-tabs>
</template>

<script setup lang="ts">
import { Dark } from 'quasar'
import { ref, watch } from 'vue'

// Props
const props = defineProps<{
  tabs?: any[]
  // tab?: string | null
  modelValue?: string | null
}>()

// Emits
const emit = defineEmits(['update:modelValue'])

// Data
const tabValue = ref<string | null>(props.modelValue ?? null)

watch(
  () => props.modelValue,
  (newVal) => {
    tabValue.value = newVal ?? null
  }
)

// Methods
const onUpdateTab = () => {
  emit('update:modelValue', tabValue.value)
}
</script>
