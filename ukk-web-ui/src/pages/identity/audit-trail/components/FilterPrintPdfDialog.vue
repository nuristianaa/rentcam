<template>
  <q-dialog v-model="model" persistent>
    <q-card style="min-width: 500px; max-width: 40vw">
      <q-card-section class="text-h6">Filter Data</q-card-section>
      <q-separator />

      <q-card-section>
        <div v-for="(f, idx) in filters" :key="idx" class="q-mb-md q-pa-sm" style="border: 1px solid #ccc; border-radius: 8px; max-width: 500px">
          <div class="row items-center justify-between">
            <div @click="f.show = !f.show" style="cursor: pointer">
              <strong>{{ f.module || 'Select Module' }}</strong>
              <span v-if="f.columns && f.columns.length">({{ f.columns.length }} columns)</span>
            </div>

            <div class="row items-center q-gutter-x-sm">
              <q-btn icon="playlist_add" label="Add All" flat dense size="sm" color="primary" @click="addAllColumns(f)" :disable="!f.module" />
              <q-btn icon="delete" label="Remove" flat dense size="sm" color="negative" @click="filters.splice(idx, 1)" />
            </div>
          </div>

          <div v-show="f.show" class="q-mt-sm">
            <f-select v-model="f.module" :options="availableModules(idx)" label="Select Module" @update:model-value="f.columns = []" />

            <f-select v-if="f.module && moduleOptions[f.module]" v-model="f.columns" :options="translateColumns(f.module, moduleOptions[f.module])" label="Select Columns" multiple />
          </div>
        </div>

        <q-btn icon="add" color="primary" outline dense label="Add Module" @click="filters.push({ module: '', columns: [], show: true })" />
      </q-card-section>

      <q-separator />
      <q-card-actions align="between">
        <q-btn label="Reset All" flat color="negative" @click="resetAllFilters" />
        <div>
          <q-btn label="Cancel" flat @click="closeDialog" />
          <q-btn label="Print PDF" color="primary" @click="apply" />
        </div>
      </q-card-actions>
    </q-card>

    <s-dialog v-model="dialog">
      <sign-placement v-model="signModel.sign_placements" show-approver :approvers="approversList" hide-banner />
    </s-dialog>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { FilterItem, DataModel, Approver } from '../meta'
import Meta from '../meta'
import { Lang } from 'src/services/lang'

const props = defineProps<{
  modelValue: boolean
  moduleOptions: Record<string, string[]>
  approversList: Approver[]
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', v: boolean): void
  (e: 'apply', filters: FilterItem[]): void
}>()

const model = ref(props.modelValue)

const signModel = ref<DataModel>({
  sign_placements: []
})

const filters = ref<FilterItem[]>([{ module: '', columns: [], show: true }])

const dialog = ref({
  show: false,
  type: 'detail',
  title: 'Detail',
  props: null,
  persistent: true
})

const availableModules = (currentIdx: number) => {
  const selected = filters.value.filter((_, i) => i !== currentIdx).map((f) => f.module)
  return Object.keys(props.moduleOptions)
    .filter((m) => !selected.includes(m))
    .map((module) => {
      const [app, schema, name] = module.split('.')
      // const title = Lang.module(
      //   {
      //     app,
      //     schema,
      //     name
      //   } as any,
      //   'title'
      // )
      return {
        id: module,
        name: `${app} - ${schema} - ${name}`
      }
    })
}

const addAllColumns = (f: FilterItem) => {
  if (f.module && props.moduleOptions[f.module]) {
    f.columns = [...props.moduleOptions[f.module]]
  }
}

const resetAllFilters = () => {
  filters.value = [{ module: '', columns: [], show: true }]
}

const showDialog = (type: string, title: string, data: any = null) => {
  dialog.value.type = type
  dialog.value.title = `${title} | ${Meta.title}`
  dialog.value.show = true
  dialog.value.props = data
}

const closeDialog = () => {
  model.value = false
}

const apply = () => {
  emit('apply', filters.value, signModel.value.sign_placements)
  closeDialog()
}

const translateColumns = (module: string, columns: string[]) => {
  const [app, schema, name] = module.split('.')
  return columns.map((column) => ({
    id: column,
    name: Lang.module(
      {
        app,
        schema,
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
</script>
