<template>
  <div>
    <div style="border-radius: 3px" :class="hasChildren ? 'q-tree__node--link' : 'q-tree__node--link q-treeview-node--leaf bottom-item-tree'">
      <div style="padding-top: 6px" class="row q-treeview-node__root" @click="open = !open">
        <q-icon size="sm" v-if="hasChildren" name="arrow_right" :class="open ? 'text-grey-8 q-tree__arrow--rotate' : 'text-grey-8'" />
        <slot name="left" v-bind="{ item: value, open }" />
        <slot v-if="hasDefaultSlot" name="body" v-bind="{ item: value, open }" />
        <div v-if="!hasDefaultSlot" class="q-tree__node-header-content q-pa-xs">
          {{ value.name }}
        </div>
      </div>

      <div v-if="open && (value.children?.length ?? 0) > 0" class="q-tree__children" style="padding-top: 6px">
        <draggable :list="value.children" @input="updateValue" class="dragArea" :item-key="rowKey" :ghost-class="ghostClass" :group="group" :animation="animation" @start="drag = true" @end="drag = false">
          <q-draggable-tree-node v-for="(item, index) in value.children" @input="updateChildValue" :key="index" :value="item" :group="group" :rowKey="rowKey" :ghost-class="ghostClass" :disabled="disabled" :animation="animation">
            <template #left="{ item: element, open }">
              <slot name="left" v-bind="{ item: element, open }"></slot>
            </template>

            <template v-if="hasDefaultSlot" #body="{ item: element, open }">
              <slot name="body" v-bind="{ item: element, open }"></slot>
            </template>

            <span v-if="!hasDefaultSlot">{{ item.name }}</span>
          </q-draggable-tree-node>
        </draggable>
      </div>

      <div v-else class="q-tree__children">
        <draggable :list="value.children" @input="updateValue" class="dragArea" :item-key="rowKey" :ghost-class="ghostClass" :group="group" :animation="animation" @start="drag = true" @end="drag = false"></draggable>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, useSlots } from 'vue'
import { VueDraggableNext as draggable } from 'vue-draggable-next'

// ----------------- Types -----------------
export interface TreeNode {
  id?: number | string
  name?: string
  children?: TreeNode[]
  [k: string]: any
}

const props = withDefaults(
  defineProps<{
    value: TreeNode
    root?: boolean
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
  (e: 'input', value: TreeNode): void
}>()

// ----------------- Local state -----------------
const open = ref(true)
const drag = ref(false)
const localValue = ref<TreeNode>({ ...(props.value ?? { id: 0, name: '', children: [] }) })

// ----------------- Slots & computed -----------------
const slots = useSlots()
const hasDefaultSlot = computed(() => !!(slots && slots.body))
const hasChildren = computed(() => Array.isArray(props.value?.children) && props.value.children.length > 0)

// ----------------- Watchers -----------------
watch(
  () => props.value,
  (v) => {
    localValue.value = { ...(v ?? {}) }
  },
  { deep: true, immediate: true }
)

// ----------------- Methods -----------------
function updateValue(value: any) {
  if (Array.isArray(value)) {
    // ensure children array exists
    if (!localValue.value.children) localValue.value.children = []
    localValue.value.children = [...value]
    emit('input', localValue.value)
    open.value = true
  }
}

function updateChildValue(value: TreeNode) {
  if (!localValue.value.children) return
  const key = props.rowKey ?? 'name'
  const index = localValue.value.children.findIndex((c: any) => c?.[key] === value?.[key])
  if (index !== -1) {
    // replace child and emit
    localValue.value.children[index] = value
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

.dragArea {
  min-height: 11px;
}

.bottom-item-tree {
  padding-left: 15px;
}
</style>
