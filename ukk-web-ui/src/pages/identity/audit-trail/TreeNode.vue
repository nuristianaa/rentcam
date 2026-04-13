<template>
  <div class="q-ml-sm">
    <template v-if="isObject(node)">
      <div v-for="(value, key) in node" :key="key" class="q-mb-xs">
        <span v-if="isObject(value) || Array.isArray(value)" @click="toggle(key)" class="collapser">{{ isCollapsed(key) ? '▶' : '▼' }}</span>
        <span class="json-key">"{{ key }}"</span>
        <span>:</span>
        <template v-if="isObject(value)">
          <span class="json-type">{{ Array.isArray(value) ? '[...]' : '{...}' }}</span>
          <div v-show="!isCollapsed(key)">
            <TreeNode :node="value" />
          </div>
        </template>
        <template v-else>
          <span v-html="formatValue(value)" />
        </template>
      </div>
    </template>
    <template v-else>
      <span v-html="formatValue(node)" />
    </template>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'

const props = defineProps({
  node: { type: [Object, Array, String, Number, Boolean, null], required: true }
})

const collapsed = reactive<Record<string, boolean>>({})

function toggle(key: string) {
  collapsed[key] = !collapsed[key]
}

function isCollapsed(key: string) {
  return collapsed[key]
}

function isObject(val: any) {
  return typeof val === 'object' && val !== null
}

function formatValue(val: any) {
  if (val === null) return `<span class="json-null">null</span>`
  if (typeof val === 'string') return `<span class="json-string">"${val}"</span>`
  if (typeof val === 'number') return `<span class="json-number">${val}</span>`
  if (typeof val === 'boolean') return `<span class="json-bool">${val}</span>`
  return `<span>${val}</span>`
}
</script>

<style scoped>
.collapser {
  cursor: pointer;
  margin-right: 6px;
  color: #999;
}

.json-key {
  color: #00177e;
  margin-right: 4px;
}

.json-string {
  color: #ce9178;
}

.json-number {
  color: #b5cea8;
}

.json-bool {
  color: #569cd6;
}

.json-null {
  color: #808080;
}

.json-type {
  color: #6a9955;
  margin-left: 4px;
}
</style>
