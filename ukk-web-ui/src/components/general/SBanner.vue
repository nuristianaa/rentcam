<template>
  <div :class="`col-${col ? col : '12'}`">
    <q-banner  dense inline-actions :class="`text-${textColor ? textColor : 'white'} bg-${color ? color : 'blue-6'} s-banner`">
      <template v-if="icon" v-slot:avatar><q-icon :name="icon" size="sm" :color="iconColor ? iconColor : 'white'" /></template>
      <slot></slot>
    </q-banner>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  col?: string
  icon?: string
  color?: string
  textColor?: string
  iconColor?: string
}>()
</script>

<style>
.s-banner .q-banner__content {
  padding: 5px;
}
</style>
