<template>
  <template v-if="props.container == 'tr'">
    <tr
      v-for="(item, index) in props.modelValue"
      :key="item?.id ?? item?.name"
      class="draggable-item"
      :class="{ dragging: draggingIndex === index }"
      draggable="true"
      @dragstart="onDragStart(index)"
      @dragover.prevent
      @dragenter="onDragEnter(index, props.modelValue)"
      @drop="onDrop"
      @touchstart="onTouchStart($event, index)"
      @touchmove="onTouchMove($event)"
      @touchend="onTouchEnd"
    >
      <slot :item="item" :index="index"></slot>
    </tr>
  </template>
  <div v-else class="draggable-container">
    <div
      v-for="(item, index) in props.modelValue"
      :key="item?.id ?? item?.name"
      class="draggable-item"
      :class="{ dragging: draggingIndex === index }"
      draggable="true"
      @dragstart="onDragStart(index)"
      @dragover.prevent
      @dragenter="onDragEnter(index, props.modelValue)"
      @drop="onDrop"
      @touchstart="onTouchStart($event, index)"
      @touchmove="onTouchMove($event)"
      @touchend="onTouchEnd"
    >
      <slot :item="item" :index="index"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  modelValue: any
  container?: 'div' | 'tr'
}>()

const draggedIndex = ref<number | null>(null)
const draggingIndex = ref<number | null>(null)
const touchStartY = ref<number | null>(null)

// Handle drag start (mouse/keyboard)
function onDragStart(index: number) {
  draggedIndex.value = index
  draggingIndex.value = index
}

// Handle drag enter (hovered item)
function onDragEnter(index: number, items: any) {
  if (draggedIndex.value !== null && draggedIndex.value !== index) {
    const item = items.splice(draggedIndex.value, 1)[0]
    items.splice(index, 0, item)
    draggedIndex.value = index
    draggingIndex.value = index
  }
}

// Handle drop (clean up state)
function onDrop() {
  draggedIndex.value = null
  draggingIndex.value = null
}

// Handle touch start
function onTouchStart(event: any, index: number) {
  touchStartY.value = event.touches[0].clientY
  draggedIndex.value = index
  draggingIndex.value = index
}

// Handle touch move
function onTouchMove(event: any) {
  if (draggedIndex.value === null) return

  const touchY = event.touches[0].clientY
  const elements = document.elementsFromPoint(event.touches[0].clientX, touchY)

  const targetElement = elements.find((el) => el.classList.contains('draggable-item'))

  if (targetElement) {
    const targetIndex = Array.from(targetElement.parentNode?.children || []).indexOf(targetElement)
    if (targetIndex !== -1 && targetIndex !== draggedIndex.value) {
      onDragEnter(targetIndex, props.modelValue)
    }
  }
}

// Handle touch end
function onTouchEnd() {
  draggedIndex.value = null
  draggingIndex.value = null
  touchStartY.value = null
}
</script>

<style scoped>
.draggable-container {
  display: flex;
  flex-direction: column;
}
.draggable-item {
  transition: transform 0.2s ease;
  user-select: none;
}
.draggable-item.dragging {
  opacity: 0.5;
}
</style>
