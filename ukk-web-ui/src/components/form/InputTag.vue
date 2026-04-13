<template>
  <div :class="col ? `q-px-sm col-12 col-md-6 col-lg-${col}` : ''">
    <!-- INPUT -->
    <f-input
      hide-bottom-space
      v-model="inputValue"
      :label="label"
      :placeholder="placeholder"
      @keydown.enter.prevent="addTag"
    />

    <!-- TAG LIST -->
    <div class=" row">
      <q-chip
        v-for="(tag, i) in model"
        :key="i"
        removable
        @remove="removeTag(i)"
        color="primary"
        text-color="white"
        dense
      >
        {{ tag }}
      </q-chip>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
  modelValue: string[]
  label?: string
  placeholder?: string
  col?: string
}>()

console.log(props)

const emit = defineEmits(['update:modelValue'])

/* =========================
   INTERNAL INPUT STATE
========================= */
const inputValue = ref<string>('')

/* =========================
   V-MODEL HANDLER
========================= */
const model = computed<string[]>({
  get: () => props.modelValue ?? [],
  set: (val) => emit('update:modelValue', val)
})

/* =========================
   METHODS
========================= */
const addTag = () => {
  console.log(model.value)
  const value = inputValue.value?.trim()
  if (!value) return

  // Prevent duplicate
  if (model.value.includes(value)) {
    inputValue.value = ''
    return
  }

  model.value = [...model.value, value]
  inputValue.value = ''
}

const removeTag = (index: number) => {
  const newTags = [...model.value]
  newTags.splice(index, 1)
  model.value = newTags
}
</script>