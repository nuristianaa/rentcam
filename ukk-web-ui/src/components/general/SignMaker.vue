<template>
  <div class="signature-wrapper row text-center relative-position" :style="`width: ${signConfig.width}px`">
    <VueSignaturePad
      ref="signature"
      :height="`${signConfig.height}px`"
      :width="`${signConfig.width}px`"
      :max-width="signConfig.maxWidth"
      :min-width="signConfig.minWidth"
      :options="{
        penColor: signConfig.penColor,
        backgroundColor: signConfig.backgroundColor
      }"
    />
    <div class="signature-config q-pt-sm text-center col-12">
      <!-- <q-btn v-if="signModel.sign" outline size="sm" dense color="primary" label="upload" icon="upload" class="q-pr-md" unelevated  @click="upload(signModel.sign)"/> &nbsp;  -->
      <q-btn size="sm" dense color="primary" label="save" icon="check_circle" class="q-pr-md" unelevated  @click="handleSaveSignature" />
      &nbsp;
      <q-btn size="sm" dense color="red" label="Clear" icon="close" class="q-pr-md" unelevated  @click="onDelete" />
    </div>
    <q-inner-loading :showing="loading">
      <q-spinner-facebook size="50px" color="primary" />
    </q-inner-loading>
  </div>
</template>

<script setup lang="ts">
import { uid } from 'quasar'
import { ref, onMounted, watch } from 'vue'
import { Helper } from 'src/services/helper'
import { VueSignaturePad } from '@selemondev/vue3-signature-pad'
import type { Signature } from '@selemondev/vue3-signature-pad'
import Api from 'src/services/api'

const props = defineProps<{
  modelValue?: string
  title?: string
  name?: string
  width?: number
  height?: number
  base64Mode?: boolean
  withDelete?: string
  app?: string
  module?: string
  referenceId?: string
  masterFileId?: string
}>()

const emit = defineEmits(['clear', 'save', 'update:modelValue'])

const API = new Api()

const loading = ref(false)
const model = ref(props.modelValue)

const signModel: any = ref({
  name: props.name,
  title: props.title,
  sign: null,
  path: null,
  fileName: null
})

const signConfig = ref({
  // pad area
  width: props.width || 320,
  height: props.height || 200,
  // pencil
  penColor: 'rgb(0,0,0)',
  backgroundColor: 'rgb(255, 255, 255)',
  maxWidth: 2,
  minWidth: 1
})

const signature = ref<Signature>()

const clearSign = () => {
  signature.value?.clearCanvas()
  handleAddWaterMark()
  emit('clear', null)
}

const emmiter = (val: any) => {
  model.value = val
  emit('update:modelValue', val)
  emit('save', val)
}

const handleSaveSignature = () => {
  if (signature.value?.saveSignature()) {
    signModel.value.sign = signature.value?.saveSignature()
    if (!props.base64Mode) upload(signModel.value.sign)
    else emmiter(signModel.value.sign)
  } else console.warn('Error generate signature')
}

const measureTextWidth = (text: any, font: any) => {
  const canvas = document.createElement('canvas')
  const ctx: any = canvas.getContext('2d')
  ctx.font = font
  return ctx.measureText(text).width
}

const defineWaterMark = (label: any, fontSize: string = '14', yPercent: number = 90, xPercent: number = 50) => {
  const width = signConfig.value.width
  const height = signConfig.value.height

  const font = `${fontSize}pt Arial`
  const textWidth = measureTextWidth(label, font)

  // Pusat kanvas - setengah teks
  const centerX = width * (xPercent / 100) - textWidth / 2
  const centerY = height * (yPercent / 100)

  const cfg = {
    text: label,
    font,
    style: 'all',
    fillStyle: 'black',
    x: centerX,
    y: centerY,
    strokeStyle: 'white',
    sx: 0,
    sy: 0
  }

  // console.log(`defineWaterMark: ${label}`, cfg);
  return signature.value?.addWaterMark(cfg)
}

const handleAddWaterMark = () => {
  defineWaterMark(signModel.value.name, '14', 85)
  defineWaterMark(`(${signModel.value.title})`, '11', 92, 50)
  // console.log('sign', signature.value)
}

const base64ToBlob = (base64Data: string) => {
  const parts: any = base64Data.split(',')
  const mime = parts[0].match(/:(.*?);/)?.[1] || ''
  const byteString = atob(parts[1])
  const ab = new ArrayBuffer(byteString.length)
  const ia = new Uint8Array(ab)
  for (let i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i)
  }
  return new Blob([ab], { type: mime })
}

const upload = async (base64: any = null) => {
  if (!base64) return false

  loading.value = true
  const req = new FormData()
  const blob = base64ToBlob(base64)
  req.append('app', props.app)
  req.append('name', signModel.value.fileName)
  req.append('description', `${props.app}-${props.module}-${signModel.value.name}-${signModel.value.title}`)
  req.append('module', props.module)
  req.append('file', blob, signModel.value.fileName)

  if (props.referenceId) req.append('reference_id', props.referenceId)

  const ep: any = `auth/master-files`
  await API.post(
    ep,
    req,
    (status: number, data: any) => {
      loading.value = false
      if (status === 200) {
        signModel.value.path = data?.path
        emmiter(signModel.value.path)
      }
    },
    'main',
    true
  )
}

const removeSign = (skipNotif = false) => {
  // console.log(props)
  if (!props.masterFileId) return

  const ep = 'auth/master-files/delete'
  loading.value = true
  API.skipNotice = true
  API.delete(ep, { id: [props.masterFileId] }, (status: number) => {
    API.skipNotice = false
    loading.value = false
    if (status === 200) {
      clearSign()
      Helper.showSuccess('Signature was deleted!')
    }
  })
}

const onDelete = () => {
  const path = model.value
  if (!path) {
    clearSign()
    return false
  }

  Helper.confirm('Area you sure want to delete current sign?', (result: boolean) => {
    if (!result) return false
    removeSign()
  })
}

const init = () => {
  setTimeout(() => {
    // init watermark
    handleAddWaterMark()
  }, 300)
}

watch(
  () => [props.name, props.title],
  (newValue) => {
    signModel.value.name = newValue[0]
    signModel.value.title = newValue[1]

    signature.value?.clearCanvas()
    handleAddWaterMark()
    signModel.value.fileName = Helper.label2slug(`${signModel.value.name} ${signModel.value.title}`, '-')
  }
)

onMounted(() => {
  init()
  signModel.value.fileName = Helper.label2slug(`${signModel.value.name} ${signModel.value.title}`, '-') + '' + uid()

  if (props.withDelete) removeSign(props.withDelete, true)
})
</script>
