<template>
  <div :class="col ? `q-px-sm col-12 col-md-6 col-lg-${col}` : ''">
    <q-card flat bordered>
      <!-- TITLE -->
      <div class="row justify-between">
        <h4 class="form-title q-mx-md">{{ title || 'Upload Files' }}</h4>
        <div class="q-pr-md q-pt-md">
          <q-btn color="accent" icon="add" label="Add" @click="onAddUploadDoc">
            <q-tooltip>Add Data</q-tooltip>
          </q-btn>
        </div>
      </div>
      <!-- CONTENT -->
      <div class="row">
        <div v-for="(val, index) in files" :key="index" class="q-pa-sm col-12 col-md-4 col-lg-3">
          <q-card flat style="width: 100%">
            <!-- DELETE & BUTTONS -->
            <div class="row justify-left" style="width: 100%">
              <q-btn style="position: absolute; z-index: +1; left: 4px; top: -6px" dense round size="xs" color="negative" icon="delete" @click="onDeleteUploadDoc(index, val.id)">
                <q-tooltip>Delete</q-tooltip>
              </q-btn>
              <div class="q-px-sm">
                <f-uploader v-model="val.file" :old-file-label="val.filename" :old-file="val.path" label="Upload File" inline @delete-event="val.file = 'del'" @update="emiters()" :type="imageOnly ? 'image' : ''" />
                <f-input v-if="!imageOnly" v-model="val.name" label="Name" inline @update="emiters()" />
                <f-input v-if="!imageOnly" v-model="val.description" label="Description" inline @update="emiters()" />
              </div>
            </div>
          </q-card>
        </div>
      </div>
    </q-card>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { Helper } from 'src/services/helper'
import { ref, watch } from 'vue'

interface FileItem {
  id: number | null
  name: string | null
  description: string | null
  module: string | null
  file: string | null
  filename: string | null
  path: string | null
}

const props = defineProps<{
  modelValue: FileItem[]
  col?: string
  title?: string
  row?: boolean
  module?: string
  imageOnly?: boolean
}>()

const emit = defineEmits(['update:modelValue'])

const API = new Api()
const files = ref<FileItem[]>(props.modelValue)

watch(
  () => props.modelValue,
  (newValue) => {
    files.value = newValue
  }
)

const emiters = () => {
  emit('update:modelValue', files.value)
}

const onAddUploadDoc = () => {
  const params: FileItem = {
    id: null,
    name: null,
    description: null,
    module: props.module || null,
    file: null,
    filename: null,
    path: null
  }
  files.value.push(params)
  emiters()
}

const onDeleteUploadDoc = (index: number, id: number | null) => {
  files.value.splice(index, 1)
  if (id && id > 0) {
    Helper.confirm('Are you sure?', (result: boolean) => {
      if (result) {
        API.delete(
          `auth/master-files?id=${id}`,
          {},
          (status: number) => {
            if (status === 200) Helper.showToast('success delete file!')
          },
          'main'
        )
      }
    })
  }
  emiters()
}
</script>
