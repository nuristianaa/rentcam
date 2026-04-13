<template>
  <q-btn round flat :class="`${flat ? '' : 'bg-blue-1 text-blue-9'}`" dense>
    <q-icon name="help_outline" size="1.6em" />
    <q-popup-proxy>
      <f-card :title="title || 'Help'">
        <slot></slot>
      </f-card>
    </q-popup-proxy>
  </q-btn>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// Props
const props = defineProps<{
  title?: string
  flat?: boolean
}>()
</script>
