<template>
  <div>
    <q-table dense flat :rows="rows" :columns="columns" row-key="key" hide-pagination virtual-scroll :rows-per-page-options="[0]" :filter="filter">
      <template v-slot:top v-if="!noHeader">
        <div class="row q-gutter-sm items-center">
          <q-btn dense class="q-px-md" color="primary" label="Copy Value" icon="content_copy" @click="copyValue(props.node)" />
          <q-input v-model="filter" filled dense placeholder="search" class="form-sm">
            <template v-slot:append><q-icon name="search" size="xs"></q-icon></template>
          </q-input>
        </div>
      </template>
      <!-- <template v-slot:body-cell-value="props">

      </template> -->
      <template v-slot:body-cell="props">
        <q-td :props="props">
          <span v-if="props.value === null" class="text-grey italic">null</span>
          <span v-else-if="typeof props.value === 'object'">
            <TableDetail :node="props.value" no-header />
            <!-- {{ truncateText(JSON.stringify(props.value, null, 2)) }} -->
          </span>
          <span v-else>
            {{ Helper.truncateText(props.value, 35) }}
            <q-tooltip>{{ props.value }}</q-tooltip>
          </span>
        </q-td>
      </template>
    </q-table>
  </div>
</template>

<script setup lang="ts">
import { Helper } from 'src/services/helper'
import { computed, ref } from 'vue'

const props = defineProps({
  noHeader: { type: [Boolean, null], required: false },
  node: { type: [Object, Array, String, Number, Boolean, null], required: true }
})

// const columns: any = [
//   { align: 'left', name: 'key', label: 'Key', field: 'key', sortable: true },
//   { align: 'left', name: 'value', label: 'Value', field: 'value' }
// ]

// const rows = computed(() =>
//   Object.entries(props.node || {}).map(([key, value]) => ({
//     key,
//     value
//   }))
// )

const columns: any = computed(() => {
  if (Array.isArray(props.node)) {
    const first = props.node[0]
    if (first && typeof first === 'object' && !Array.isArray(first)) {
      return Object.keys(first).map((key) => ({
        name: key,
        label: key,
        field: key,
        align: 'left',
        sortable: true
      }))
    } else {
      // Array of primitives (string/number/etc)
      return [{ name: 'value', label: 'Value', field: 'value', align: 'left' }]
    }
  } else {
    // node is object
    return [
      { name: 'key', label: 'Key', field: 'key', align: 'left', sortable: true },
      { name: 'value', label: 'Value', field: 'value', align: 'left' }
    ]
  }
})

const rows = computed(() => {
  if (Array.isArray(props.node)) {
    const first = props.node[0]
    if (first && typeof first === 'object' && !Array.isArray(first)) {
      // Array of objects
      return props.node
    } else {
      // Array of primitives
      return props.node.map((val, i) => ({ value: val, index: i }))
    }
  } else {
    // node is object
    return Object.entries(props.node || {}).map(([key, value]) => ({
      key,
      value
    }))
  }
})

const filter = ref('')

const copyValue = (val: any) => {
  const text = typeof val === 'string' ? val : JSON.stringify(val)
  navigator.clipboard
    .writeText(text)
    .then(() => {
      Helper.showSuccess('Data Copied')
    })
    .catch(() => {
      Helper.showAlert('Cannot Copy')
    })
}
</script>

<style scoped>
.italic {
  font-style: italic;
}
</style>
