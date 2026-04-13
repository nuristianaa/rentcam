<template>
  <div v-if="!inline" class="col-12">
    <q-card class="q-py-xs" flat>
      <!-- DELETE & BUTTONS -->
      <div v-if="modelValue" class="q-px-xs" style="position: absolute">
        <q-btn v-if="withDelete !== undefined" color="negative" flat icon="delete" dense class="q-pl-none row" @click="$emit('deleteEvent')">
          <q-tooltip>Delete</q-tooltip>
        </q-btn>
        <q-btn v-if="withEdit !== undefined" color="positive" flat icon="edit" dense class="q-pl-none row" @click="$emit('editEvent')">
          <q-tooltip>Edit</q-tooltip>
        </q-btn>
      </div>
      <!-- CONTENT -->
      <div :class="row === '' ? 'row q-pl-lg' : 'q-pa-md'">
        <slot />
      </div>
    </q-card>
  </div>
  <div v-else :class="col ? `q-pa-sm col-12 col-md-${col}` : 'col-12 q-pa-sm'">
    <q-card flat>
      <h4 class="q-pl-md q-pt-md text-capitalize">{{ title }}</h4>
      <!-- DELETE & BUTTONS -->
      <div v-if="modelValue" class="col-12 row justify-end">
        <f-toggle v-if="defaultField" :model-value="rowValue[defaultField]" @click="$emit('defaultEvent')" tooltip="Default" />
        <q-btn v-if="withDelete !== undefined" color="negative" flat icon="delete" @click="$emit('deleteEvent')" dense class="q-pl-none">
          <q-tooltip>Delete</q-tooltip>
        </q-btn>
      </div>
      <!-- CONTENT -->
      <div :class="row === '' ? 'row q-pa-sm' : 'q-pa-md'">
        <slot />
      </div>
    </q-card>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  col?: number
  title?: string
  row?: string
  modelValue?: boolean
  rowValue?: Record<string, any>
  index?: number
  defaultField?: string
  withDelete?: boolean
  withEdit?: boolean
  inline?: string
}>()

defineEmits<{
  (e: 'deleteEvent'): void
  (e: 'editEvent'): void
  (e: 'defaultEvent'): void
}>()
</script>
