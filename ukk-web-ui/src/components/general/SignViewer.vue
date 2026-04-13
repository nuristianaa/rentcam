<template>
  <q-img :src="url" :style="`height: ${height ? height : '140px'}; max-width: ${width ? width : '150px'};`" class="q-mb-sm">
    <template v-slot:error>
      <div class="absolute-full flex flex-center bg-negative text-white">Cannot load signature</div>
    </template>
  </q-img>
</template>

<script setup lang="ts">
import { uid } from 'quasar'
import { ref, computed, onMounted, watch } from 'vue'
import { Helper } from 'src/services/helper'

const props = defineProps<{
  path?: string
  width?: number
  height?: number
}>()

const url: any = ref(null)

const updateUrl = () => {
  url.value = props.path ? Helper.viewBlobFile(props.path) : null
}

watch(() => props.path, updateUrl)

onMounted(() => {
  updateUrl()
})
</script>
