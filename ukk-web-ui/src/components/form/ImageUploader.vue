<template>
  <!-- Images -->
  <div class="col-12">
    <div class="row q-px-md justify-between items-center">
      <div class="form-title">{{ label || 'Images'}}</div>
      <q-btn flat label="Add Image" icon="add" @click="addImage" />
    </div>

    <div class="row q-px-sm">
      <div
        class="col-6 col-sm-4 q-py-lg q-px-sm"
        v-for="img in filesLocal"
        :key="img.uid"
      >
        <f-uploader
          :label="`Image ${filesLocal.indexOf(img) + 1}`"
          type="image"
          v-model="img.file"
          :old-file="img.previewUrl"
        >
          <template #button>
            <q-btn
              label="Delete"
              color="negative"
              class="text-bold"
              @click="deleteFile(img.uid)"
            />

            <q-btn color="primary" flat dense icon="tune"
              v-if="props.colAttributes.length > 0"
              @click="img.config = !img.config"
            />
          </template>

          <template #input>
            <div v-if="img.config" class="row q-px-sm justify-center">
              <f-select
                v-if="props.colAttributes.includes('colSize')"  
                col="6" hide-clearable
                v-model="img.colSize"
                :options="colOptions"
                label="Column Size"
                outlined
                dense
              />
              <f-input
              v-if="props.colAttributes.includes('maxHeight')"  
              col="6"
              v-model="img.maxHeight"
              label="Max Height (px)"
              outlined
              dense
              />
              <f-textarea
                v-if="props.colAttributes.includes('remark')"  
                col="12"
                v-model="img.remark"
                label="Remark"
                outlined
                dense
              />
              
            </div>
          </template>
        </f-uploader>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { Helper } from 'src/services/helper'
import { authStore } from 'src/stores/auth'
import { Config } from 'src/services/config'
import { ref, watch, onMounted, computed } from 'vue'
import type { QUploaderFactoryObject } from 'quasar'

/** USAGE
 * 
 * # Props
  type FileItem = {
    uid: string
    attachmentId?: string | null
    tempId?: string | null
    file?: File | null
    previewUrl?: string | null
  }

  const files = ref<FileItem[]>([
    { uid: crypto.randomUUID(), attachmentId: null, tempId: crypto.randomUUID(), file: null, previewUrl: null },
    { uid: crypto.randomUUID(), attachmentId: null, tempId: crypto.randomUUID(), file: null, previewUrl: null },
    { uid: crypto.randomUUID(), attachmentId: null, tempId: crypto.randomUUID(), file: null, previewUrl: null }
  ])
  const deletedIds = ref<string[]>([])

  # Template
  <f-image-uploader 
    v-model="files"
    v-model:deleted-ids="deletedIds"
    :raw-images="dataModel.images"
    :col-attributes="['colSize', 'remark', 'maxHeight']"
  />

  Set :col-attributes="[]" if want to disable configuration
 */


/* =====================
 * Props
 * ===================== */
interface Props {
  label?: string
  modelValue: any[]
  deletedIds: string[]
  rawImages?: Record<string, any> | null
  colAttributes: string[] // colSize, remarks, maxHeight
}

const props =  defineProps<Props>()
    
const emit = defineEmits<{
  (e: 'update:modelValue', val: any[]): void
  (e: 'update:deletedIds', val: string[]): void
}>()

// Local State
const filesLocal = ref<any[]>([])
const deletedLocal = ref<string[]>([])
const colOptions = Array.from({ length: 12 }, (_, i) => i + 1)

// Helpers
const emitAll = () => {
  emit('update:modelValue', filesLocal.value)
  emit('update:deletedIds', deletedLocal.value)
}


const getImagePreviewUrl = (path: string, storage?: string | null): string | null => {
  if (!path) return null

  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }

  const token = authStore().getToken()
  const baseUrl = Config.apiUrl('rental')

  if (path.startsWith('rental/') || path.startsWith('crm/') || path.startsWith('static_files/') || (storage && storage.startsWith('STATIC'))) {
    return `${baseUrl}static_files/${encodeURIComponent(path)}${token ? `?token=${token}` : ''}`
  }

  try {
    const url = (Helper as any).viewBlobFile(path, false, storage)
    return typeof url === 'string' ? url : null
  } catch {
    return null
  }
}

const initFromRawImages = () => {
    filesLocal.value = []

    if (props.rawImages && typeof props.rawImages === 'object'){
        for (const [key, val] of Object.entries<any>(props.rawImages)){
            let attachmentId: string | null = null
            let path: string | null = null
            let storage: string | null = null

            if (val && typeof val === 'object' && 'path' in val){
                attachmentId = val.id ? String(val.id) : key
                path = val.path
                storage = val.storage ?? null
            } else if (val && typeof val === 'object' && 'url' in val && val.url) {
                attachmentId = val.id ? String(val.id) : key
                path = val.url
            } else if (typeof val == 'string') {
                attachmentId = key
                path = val
            }

            const file = {
                uid: crypto.randomUUID(),
                attachmentId,
                tempId: null,
                file: null,
                previewUrl: null,
                colSize: val?.colSize || 6,
                remark: val?.remark || null,
                maxHeight: val?.maxHeight || null,
                config: false,
            }

            if (path) {
                file.previewUrl = getImagePreviewUrl(path, storage)
            }

            filesLocal.value.push(file)
        }
    }
    if (filesLocal.value.length === 0) {
        addImage()
    }

    emitAll()
}

// Actions
const addImage = () => {
  filesLocal.value.push({
    uid: crypto.randomUUID(),
    attachmentId: null,
    tempId: crypto.randomUUID(),
    file: null,
    previewUrl: null,
    colSize: 6,
    config: false
  })
  emitAll()
}

const deleteFile = (id: string) => {
  const idx = filesLocal.value.findIndex(
    f => f.uid === id || f.attachmentId === id
  )

  if (idx === -1) return

  const item = filesLocal.value[idx]

  if (item.attachmentId) {
    if (!deletedLocal.value.includes(item.attachmentId)) {
      deletedLocal.value.push(item.attachmentId)
    }
  }

  filesLocal.value.splice(idx, 1)
  emitAll()
}


onMounted(() => {
  initFromRawImages()
})

watch(
  () => props.rawImages,
  () => initFromRawImages(),
  { deep: true }
)

watch(
  () => props.deletedIds,
  v => {
    deletedLocal.value = [...v]
  },
  { immediate: true }
)


</script>