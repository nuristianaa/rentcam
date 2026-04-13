<template>
  <div class="q-pa-md q-gutter-sm">
    <q-draggable-tree-node v-for="(item, index) in treeData" @input="updateItem" :key="index" :value="item" :group="group" :rowKey="rowKey" :ghostClass="ghostClass" :disabled="disabled" :animation="animation">
      <template #left="{ item, open }">
        <slot name="left" v-bind="{ item, open }"></slot>
      </template>

      <template v-if="hasDefaultSlot" #body="{ item, open }">
        <slot name="body" v-bind="{ item, open }"></slot>
      </template>

      <span v-if="!hasDefaultSlot">{{ item }}</span>
    </q-draggable-tree-node>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, useSlots } from 'vue'

interface TreeNode {
  id?: number
  name?: string
  children?: TreeNode[]
  [key: string]: any
}

const props = withDefaults(
  defineProps<{
    data: TreeNode[]
    group?: string | null
    rowKey?: string
    ghostClass?: string
    disabled?: boolean
    animation?: number
  }>(),
  {
    group: null,
    rowKey: 'id',
    ghostClass: 'ghost',
    disabled: false,
    animation: 200
  }
)

const emit = defineEmits<{
  (e: 'input', value: TreeNode[]): void
}>()

const localValue = ref<TreeNode[]>([...props.data])

const slots = useSlots()
const hasDefaultSlot = computed(() => !!slots.body)

const treeData = computed(() => props.data)

watch(
  () => props.data,
  (val) => {
    localValue.value = [...val]
  }
)

function updateItem(itemValue: TreeNode) {
  const index = localValue.value.findIndex((v) => v[props.rowKey ?? 'label'] === itemValue[props.rowKey ?? 'label'])
  if (index !== -1) {
    localValue.value[index] = itemValue
    emit('input', localValue.value)
  }
}
</script>

<style scoped>
.ghost {
  opacity: 0.5;
  background: lightgray;
}

.list-group {
  min-height: 20px;
}

.list-group-item {
  cursor: move;
}

.list-group-item i {
  cursor: pointer;
}
</style>
