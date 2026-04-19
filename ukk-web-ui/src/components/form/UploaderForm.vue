<!-- eslint-disable -->
<template>
  <div :class="boxClass">
    <div v-if="showFile" class="text-center">
      <div class="text-bold text-primary q-mb-sm text-h5">{{ label }}</div>
      <div class="q-gutter-sm justify-center">
        <q-img v-if="oldFile && props.type === 'image'" :src="oldFile" :style="`${props.thumbStyle ? props.thumbStyle : 'height: 140px; max-width: 150px'}`">
          <template v-slot:error>
            <div class="absolute-full flex flex-center bg-negative text-white">
              <q-icon name="broken_image" style="font-size: 42px" />
              <br />
              Cannot load image
              <small><a :href="oldFile" target="_blank" class="text-white">Open Link</a></small>
            </div>
          </template>
          <template v-if="props.thumbCaption">
            <div class="absolute-bottom text-subtitle1 text-center">
              <small>{{ props.thumbCaption }}</small>
            </div>
          </template>
        </q-img>
        <br />
        <q-btn flat no-caps class="text-primary bg-grey-3 text-bold" icon="file_upload" clickable @click="onChange">Change File</q-btn>
        <slot name="button"></slot>
        <slot name="input">
          
        </slot>
      </div>
    </div>
    <q-uploader v-else bordered flat :label="props.label" max-files="1" :accept="acceptFile" @added="onFileAdded" @rejected="onRejected" :no-thumbnails="false">
      <template v-slot:header="scope">
        <div class="row no-wrap items-center q-pa-sm q-gutter-xs">
          <q-btn v-if="scope.queuedFiles.length > 0" icon="clear_all" @click="scope.removeQueuedFiles" round dense flat>
            <q-tooltip>Clear All</q-tooltip>
          </q-btn>
          <q-btn v-if="scope.uploadedFiles.length > 0" icon="done_all" @click="scope.removeUploadedFiles" round dense flat>
            <q-tooltip>Remove Uploaded Files</q-tooltip>
          </q-btn>
          <q-spinner v-if="scope.isUploading" class="q-uploader__spinner" />
          <div class="col">
            <div class="q-uploader__title">{{ props.label ? props.label : 'Upload your files' }}</div>
            <div class="q-uploader__subtitle">{{ scope.uploadSizeLabel }} / {{ scope.uploadProgressLabel }}</div>
          </div>
          <q-btn v-if="scope.canAddFiles" type="a" icon="add_box" @click="scope.pickFiles" round dense flat>
            <q-uploader-add-trigger />
            <q-tooltip>Pick Files</q-tooltip>
          </q-btn>
          <q-btn v-if="scope.canUpload" icon="cloud_upload" @click="scope.upload" round dense flat>
            <q-tooltip>Upload Files</q-tooltip>
          </q-btn>

          <q-btn v-if="scope.isUploading" icon="clear" @click="scope.abort" round dense flat>
            <q-tooltip>Abort Upload</q-tooltip>
          </q-btn>
          <slot name="button"></slot>
        </div>
      </template>
    </q-uploader>
    <div v-if="!showFile" class="q-mt-md">
      <slot name="input"></slot>
    </div>
    <!-- max-file-size="10048576" -->
  </div>
</template>

<script setup lang="ts">
import { Helper } from 'src/services/helper'
import { ref, watch, onMounted, computed } from 'vue'

// Define Props
interface Props {
  styles?: string
  label?: string
  modelValue?: File | null
  type?: string
  oldFile?: string | null
  oldFileLabel?: string
  boxClass?: string
  thumbStyle?: string
  thumbCaption?: string
  accept?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'image'
})

// Define Emits
const emits = defineEmits<{
  (e: 'update:modelValue', file: File): void
}>()

const acceptFile = computed(() => {
  let res = props.type === 'image' ? '.jpg, .png, image/*' : '*'
  if (props.accept) res = props.accept
  return res
})

// State
const H = Helper
const showFile = ref(!!props.oldFile)

// Watchers
watch(
  () => props.oldFile,
  (newVal) => {
    showFile.value = !!newVal
  }
)

// Methods
const onFileAdded = (files: readonly File[]) => {
  const file = files[0]
  if (file) emits('update:modelValue', file)
}

const onChange = () => {
  showFile.value = !showFile.value
}

const onRejected = () => {
  H.showAlert('Max 1MB file size')
}

// Lifecycle Hook
onMounted(() => {
  showFile.value = !!props.oldFile
})
</script>

<style scoped>
.q-uploader__subtitle {
  font-size: 12px;
  line-height: 18px;
  display: none !important;
}
</style>
