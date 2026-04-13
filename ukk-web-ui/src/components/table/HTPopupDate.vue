<template>
  <q-btn flat dense icon="calendar_month" size="xs">
    <q-popup-proxy>
      <div class="q-gutter-md row items-start">
        <q-date flat today-btn v-model="dataModel" mask="YYYY-MM-DD HH:mm:ss" @update:model-value="submit" />
        <q-time flat with-seconds now-btn v-model="dataModel" mask="YYYY-MM-DD HH:mm:ss" @update:model-value="submit" />
      </div>
    </q-popup-proxy>
  </q-btn>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{ modelValue: any; type?: any }>()
const emit = defineEmits(['update:modelValue'])

const dataModel = ref(props.modelValue)

const submit = () => {
  emit('update:modelValue', dataModel.value)
}
</script>
