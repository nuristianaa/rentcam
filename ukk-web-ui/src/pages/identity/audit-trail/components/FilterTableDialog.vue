<template>
  <q-dialog v-model="model">
    <q-card style="min-width: 300px; max-width: 40vw">
      <q-card-section class="text-h6">Table Filter</q-card-section>
      <q-separator />

      <q-card-section>
        <div class="row q-col-gutter-y-sm">
          <f-select v-model="filter.app" :options="options.app" label="Select App" filled dense @update:model-value="onAppChange" col="12" />

          <f-select v-if="Object.keys(moduleKeys).length" v-model="filter.module" :options="translateModules(Object.keys(moduleKeys))" label="Select Module" filled dense @update:model-value="onModuleChange" col="12" />

          <f-select v-if="filter.module && moduleKeys[filter.module]" v-model="filter.columns" :options="translateColumns(moduleKeys[filter.module])" label="Select Columns" multiple filled dense col="12" />
        </div>
      </q-card-section>

      <q-separator />
      <q-card-actions align="between">
        <q-btn label="Reset All" flat color="negative" @click="resetAllFilters" />
        <div>
          <q-btn label="Cancel" flat @click="closeDialog" />
          <q-btn label="Apply" color="primary" @click="apply" />
        </div>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { TableFilter } from '../meta'
import { Lang } from 'src/services/lang'

const props = defineProps<{
  modelValue: boolean
  options: { app: string[] }
  moduleKeys: Record<string, string[]>
  tableFilter: TableFilter
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', v: boolean): void
  (e: 'update:tableFilter', v: TableFilter): void
  (e: 'update-columns', v: TableFilter): void
  (e: 'load-module-keys', v: TableFilter): void
}>()

const model = ref(props.modelValue)

const filter = ref({ ...props.tableFilter })

const onAppChange = () => {
  filter.value.module = ''
  filter.value.columns = []
  emit('update:tableFilter', { ...filter.value })
  emit('load-module-keys', filter.value)
}

const onModuleChange = () => {
  filter.value.columns = []
}

const closeDialog = () => {
  model.value = false
}

const apply = () => {
  emit('update:tableFilter', { ...filter.value })
  emit('update-columns', filter.value)
  closeDialog()
}

const resetAllFilters = () => {
  filter.value = {
    app: '',
    module: '',
    columns: []
  }
  emit('update:tableFilter', { ...filter.value })
  emit('update-columns', filter.value)
}

const translateModules = (modules: string[]) => {
  return modules.map((module) => {
    const [app, schema, name] = module.split('.')
    return {
      id: module,
      name: Lang.module(
        {
          app,
          schema,
          name
        } as any,
        'title'
      )
    }
  })
}

const translateColumns = (columns: string[]) => {
  const [schema, name] = filter.value.module.split('.')

  return columns.map((column) => ({
    id: column,
    name: Lang.module(
      {
        app: filter.value.app,
        schema: schema,
        name
      } as any,
      column
    )
  }))
}

watch(
  () => props.modelValue,
  (val) => {
    model.value = val
  }
)

watch(
  () => model.value,
  (val) => {
    emit('update:modelValue', val)
  }
)

watch(
  () => props.tableFilter,
  (val) => {
    filter.value = { ...val }
    emit('update:tableFilter', filter.value)
  },
  { deep: true }
)
</script>
