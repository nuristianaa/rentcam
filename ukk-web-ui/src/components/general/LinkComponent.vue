<template>
  <q-btn no-caps :href="source || src" :flat="flat === ''" :loading="loading || false" :label="label || 'See File'" :icon="icon" :color="color || 'primary'" target="_blank">
    <!-- :disabled="isDisabled" -->
  </q-btn>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'

interface Props {
  src?: string
  flat?: string
  icon?: string
  label?: string
  color?: string
  loading?: boolean
  disable?: string | boolean
}

const props = defineProps<Props>()

const source = ref<string | null>(null)

// Update `source` when `src` changes
watch(
  () => props.src,
  (newSrc) => {
    source.value = newSrc || null
  },
  { immediate: true }
)

// Computed property for `disabled` state
const isDisabled = computed(() => {
  if (props.disable === '' || props.disable === true) return true
  if (!source.value || source.value === '') return true
  return false
})
</script>

<style scoped>
a:link {
  text-decoration: none;
}
</style>
