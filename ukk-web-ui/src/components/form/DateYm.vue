<template>
  <q-date v-model="date3" default-view="Years" emit-immediately @update:model-value="onUpdate" minimal mask="MMM YYYY" ref="date3ref">
    <div class="row items-center justify-end">
      <q-btn v-close-popup label="Close" color="primary" flat />
    </div>
  </q-date>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, null],
    required: false
  }
})

const emit = defineEmits(['update:modelValue', 'updatevalue', 'hide'])

const date3 = ref<string | null>(null)
const currentView = ref<'Years' | 'Months'>('Years')
// eslint-disable-next-line @typescript-eslint/consistent-type-imports
const date3ref = ref<InstanceType<(typeof import('quasar'))['QDate']> | null>(null)

const init = () => {
  date3.value = props.modelValue as string | null
}

const onUpdate = () => {
  currentView.value = currentView.value === 'Years' ? 'Months' : 'Years'
  date3ref.value?.setView(currentView.value)

  if (currentView.value === 'Years') {
    emit('update:modelValue', date3.value)
    emit('updatevalue', date3.value)
    emit('hide')
  }
}

watch(() => props.modelValue, init)
onMounted(init)
</script>
