<template>
  <div class="container">
    <div class="list">
      <div
        v-for="(parent, parentIndex) in list"
        :key="parentIndex"
        draggable="true"
        @dragstart="dragStart(parentIndex)"
        @dragover="allowDrop($event, parentIndex)"
        @dragleave="dragLeave"
        @drop="drop(parentIndex)"
        @touchstart="onTouchStart($event, parentIndex)"
        @touchmove="onTouchMove($event)"
        @touchend="onTouchEnd"
        :class="{ 'dragover-highlight': dropTargetIndex === parentIndex && dropTargetChildIndex === null }"
      >
        <div class="item" :id="`parent-${parentIndex}`">
          <slot name="item" :item="{ parent, parentIndex }">
            <q-icon v-if="parent?.icon" :name="parent?.icon"></q-icon>
            {{ parent?.name }}
            <q-btn v-if="props.withDelete" style="position: absolute; right: 30px" flat round dense size="xs" icon="delete" color="negative" @click="deleteRow(parentIndex)" />
          </slot>
        </div>

        <div v-if="parent?.children?.length > 0" class="nested-list">
          <div
            v-for="(child, childIndex) in parent?.children"
            :key="childIndex"
            draggable="true"
            @dragstart="dragStart(parentIndex, childIndex)"
            @dragover="allowDrop($event, parentIndex, childIndex)"
            @dragleave="dragLeave"
            @drop="drop(parentIndex, childIndex)"
            @touchstart="onTouchStart($event, parentIndex, childIndex)"
            @touchmove="onTouchMove($event)"
            @touchend="onTouchEnd"
            :class="{ 'dragover-highlight-child': dropTargetIndex === parentIndex && dropTargetChildIndex === childIndex }"
          >
            <div class="nested-item" :id="`child-${parentIndex}-${childIndex}`">
              <slot name="nestedItem" :item="{ parentIndex, child, childIndex }">
                <q-icon v-if="child?.icon" :name="child?.icon"></q-icon>
                {{ child?.name }}
                <q-btn v-if="props.withDelete" style="position: absolute; right: 30px" flat round dense size="xs" icon="delete" color="negative" @click="deleteRow(parentIndex, childIndex)" />
              </slot>
            </div>
          </div>
        </div>
        <div v-else class="nested-list">
          <div v-for="(child, childIndex) in [{ name: '', icon: '' }]" :key="childIndex" @dragover="allowDrop($event, parentIndex, childIndex)" @dragleave="dragLeave" @drop="drop(parentIndex, childIndex)" :class="{ 'dragover-highlight-child': dropTargetIndex === parentIndex && dropTargetChildIndex === childIndex }">
            <div class="nested-item" :id="`child-${parentIndex}-${childIndex}`"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
// import { Helper } from 'src/services/helper'

const props = defineProps<{
  modelValue: any
  withDelete?: boolean
}>()
const emit = defineEmits(['update:modelValue'])

const list = ref<any>(props.modelValue)
const draggedItem = ref<any>(null)
const draggedItemIndex = ref<any>(null)
const draggedParentIndex = ref<any>(null)
const preventParent = ref<number>(0)
// 0: init, 1: exec, 2: do not exec & restart to 0

const dropTargetIndex = ref<number | null>(null)
const dropTargetChildIndex = ref<number | null>(null)

const touchParentIndex = ref<number | undefined>()
const touchChildIndex = ref<number | undefined>()

// const list = ref([
//   { name: 'Parent 1', children: [{ name: 'Child 1-1' }, { name: 'Child 1-2' }] },
//   { name: 'Parent 2', children: [{ name: 'Child 2-1' }] },
// ]);

const dragStart = (parentIndex: number, childIndex?: number) => {
  if (childIndex !== undefined) {
    preventParent.value = 1
    draggedItem.value = list.value[parentIndex]?.children[childIndex]
    draggedItemIndex.value = childIndex
    draggedParentIndex.value = parentIndex
  } else if (preventParent.value != 1) {
    draggedItem.value = list.value[parentIndex]
    draggedItemIndex.value = childIndex
    draggedParentIndex.value = parentIndex
  }
  // console.log('start: ', preventParent.value, draggedParentIndex.value, draggedItemIndex.value)
}

const allowDrop = (event: DragEvent, parentIndex: number, childIndex?: number) => {
  event.preventDefault()
  // dropTargetIndex.value = parentIndex; // BIKIN DELAY
  // dropTargetChildIndex.value = childIndex ?? null; // BIKIN DELAY
}

const dragLeave = () => {
  // dropTargetIndex.value = null;
  // dropTargetChildIndex.value = null;
}

const drop = (parentIndex: number, childIndex?: number) => {
  // console.log('drop: ', preventParent.value, draggedParentIndex.value, draggedItemIndex.value,  ' --> ', parentIndex, childIndex)
  if (preventParent.value < 2) {
    if (draggedParentIndex.value === parentIndex && draggedItemIndex.value === childIndex) {
      return // Dropping on the same item
    }

    // Delete dragged item
    if (draggedItemIndex.value !== undefined) {
      list.value[draggedParentIndex.value]?.children?.splice(draggedItemIndex.value, 1)
    } else {
      list.value.splice(draggedParentIndex.value, 1)
    }

    if (childIndex !== undefined) {
      // Dropping on a child item
      if (preventParent.value == 0) preventParent.value = 2
      if (draggedItemIndex.value === undefined && parentIndex > draggedParentIndex.value) {
        if (!list.value[parentIndex - 1]?.children) list.value[parentIndex - 1].children = []
        list.value[parentIndex - 1]?.children.splice(childIndex, 0, draggedItem.value)
      } else {
        if (!list.value[parentIndex]?.children) list.value[parentIndex].children = []
        list.value[parentIndex].children.splice(childIndex, 0, draggedItem.value)
      }
    } else {
      // Dropping on a parent item
      list.value.splice(parentIndex, 0, draggedItem.value)
    }

    if (preventParent.value == 1) preventParent.value = 2
    draggedItem.value = null
    draggedItemIndex.value = null
    draggedParentIndex.value = null

    emit('update:modelValue', list.value)
  } else preventParent.value = 0
  dropTargetIndex.value = null
  dropTargetChildIndex.value = null
}

const deleteRow = (parentIndex: number, childIndex: number | undefined = undefined) => {
  if (childIndex !== undefined) {
    list.value[parentIndex]?.children?.splice(childIndex, 1)
  } else {
    list.value.splice(parentIndex, 1)
  }
}

const onTouchStart = (event: any, parentIndex: number, childIndex?: number) => {
  event.preventDefault()
  dragStart(parentIndex, childIndex)
  // touchStartY.value = event.touches[0].clientY
  // console.log('start: ', parentIndex, childIndex)
}

// Handle touchmove (dragging)
function onTouchMove(event: any) {
  const touchX = event.touches[0].clientX
  const touchY = event.touches[0].clientY
  const element = document.elementFromPoint(touchX, touchY)
  // console.log(element?.id)
  if (element?.id) {
    if (element?.id.indexOf('child') > -1) {
      const splt = element?.id.split('-')
      if (splt[1] && splt[2]) {
        touchParentIndex.value = parseInt(splt[1])
        touchChildIndex.value = parseInt(splt[2])
      }
    } else if (element?.id.indexOf('parent') > -1) {
      const splt = element?.id.split('-')
      if (splt[1]) {
        touchParentIndex.value = parseInt(splt[1])
        touchChildIndex.value = undefined
      }
    }
  }
}

// Handle touchend, simulate dragend
const onTouchEnd = () => {
  // console.log('end: ', event)
  if (touchParentIndex.value !== undefined) drop(touchParentIndex.value, touchChildIndex.value)
}
</script>

<style scoped>
.container {
  min-width: 300px;
}

.list {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}

.nested-list {
  margin-left: 20px;
}

.item,
.nested-item {
  padding: 7px;
  cursor: move;
}

.nested-item {
  border: 0.5px dashed #224f75;
}

.dragover-highlight {
  border: 2px dashed #007bff;
}

.dragover-highlight-child {
  border: 2px dashed red;
}
</style>
