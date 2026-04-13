<template>
  <div :class="`col-${col ? col : '12'}`">
    <div class="form-title q-ma-sm q-mb-sm"><slot></slot></div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  col?: string
}>()
</script>
