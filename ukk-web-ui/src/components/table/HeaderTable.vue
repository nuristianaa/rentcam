<template>
  <th v-if="props?.props?.col" :style="props.props.col.name != 'action' ? (props.props.col.width ? props.props.col.width : '') : ''">
    <q-th :props="props.props" class="header-label">
      <slot :name="`header-${props.props.col.name}`"></slot>
    </q-th>
    <div v-if="props.props.col" class="col-11">
      <HTSelect v-if="props.props.col.opt || props.props.col.api || props.props.col.formatter == 'boolean'" :refresh="refresh" :col="props.props.col" :modelValue="dataModel" @update:modelValue="submit" />
      <HTInput v-else :refresh="refresh" :col="props.props.col" :modelValue="dataModel" @update:modelValue="submit" />
    </div>
  </th>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import HTSelect from './HTSelect.vue'
import HTInput from './HTInput.vue'

const props = defineProps<{ meta: any; modelValue: any; props: any; refresh: number }>()
const emit = defineEmits(['update:modelValue', 'modelValue', 'refreshEvent'])

const dataModel = ref<string | null>(null)
const col_name = props.props.col.name

const submit = (model: string | null) => {
  // Transform value
  const value = transformValue(model)
  // Append to searchBySelected
  const query = props.modelValue.searchBySelected || []
  let isna = true
  query.forEach((item: any, index: number) => {
    if (item.name === col_name) {
      query[index] = { name: col_name, value: value }
      isna = false
    }
  })

  if (isna) {
    query.push({ name: col_name, value: value })
  }

  const data = props.modelValue
  data.searchBySelected = query

  emit('update:modelValue', data)
  emit('refreshEvent')
}

const transformValue = (value: string | null) => {
  const interpreters = [
    { key: 'notlike', slug: 'notlike:' },
    { key: 'start', slug: 'start:' },
    { key: 'end', slug: 'end:' },
    { key: 'where', slug: 'is:' },
    { key: 'isnot', slug: 'isnot:' },
    { key: 'in_', slug: 'in:' },
    { key: 'notbetween', slug: 'notbetween:' },
    { key: 'between', slug: 'between:' },
    { key: 'gt', slug: 'gt:' },
    { key: 'gte', slug: 'gte:' },
    { key: 'lt', slug: 'lt:' },
    { key: 'lte', slug: 'lte:' }
  ]

  let key = 'like'
  interpreters.forEach(({ key: k, slug }) => {
    if (value && value.includes(slug)) {
      key = k
      value = value.replace(slug, '')
    }
  })
  if (value) value = encodeURIComponent(value)
  if (value) return `${key}=${col_name}:${value}`
  else return null
}
</script>
