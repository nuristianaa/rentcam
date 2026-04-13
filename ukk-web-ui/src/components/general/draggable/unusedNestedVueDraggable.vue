<template>
  <VueDraggable class="dragArea" tag="ul" :list="modelValue" :group="{ name: 'g1' }" item-key="name">
    <template #item="{ element, index }">
      <q-list bordered separator dense>
        <q-item v-if="element" clickable v-ripple>
          <q-btn round flat color="negative" icon="cancel" @click="onDelete(index)" />
          <q-item-section avatar>
            <q-icon :name="element?.icon" />
          </q-item-section>
          <q-item-section>{{ element?.name }}</q-item-section>
          <q-item-section side>
            <q-icon name="swap_vertical_circle" />
          </q-item-section>
        </q-item>
        <nested-draggable :parent="index" v-model="element.children" />
      </q-list>
    </template>
  </VueDraggable>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import VueDraggable from 'vuedraggable'

interface Item {
  name: string
  icon?: string
  children?: Item[]
}

const props = defineProps<{
  modelValue: Item[]
  parent?: number
}>()

const emit = defineEmits(['update:modelValue'])

const data = ref<Item[]>(props.modelValue)

watch(
  () => props.modelValue,
  (newValue) => {
    data.value = newValue
  }
)

function onDelete(index: number) {
  data.value.splice(index, 1)
  emit('update:modelValue', data.value)
}
</script>

<style scoped>
.dragArea {
  outline: 0.1px dashed;
}
</style>
