<template>
  <div>
    <q-dialog v-model="dataModel.show" @hide="onHide()" transition-show="slide-left" transition-hide="slide-right" :maximized="true" :persistent="dataModel.persistent" full-height position="right">
      <q-card v-if="dataModel.show" style="overflow: hidden" class="modal-card" :style="!dataModel.maximize ? `max-width: 98vw; width: ${optimizeWidth()};` : ''">
        <q-bar class="modal-bar bg-primary text-white" v-if="props.modelValue.show_header">
          <div class="text-bold text-light">{{ dataModel.title }}</div>
          <q-space />
          <q-btn dense flat icon="minimize" @click="dataModel.maximize = false" :disable="!dataModel.maximize">
            <q-tooltip v-if="dataModel.maximize" class="bg-white text-primary">Minimize</q-tooltip>
          </q-btn>
          <q-btn dense flat icon="crop_square" @click="dataModel.maximize = true" :disable="dataModel.maximize">
            <q-tooltip v-if="!dataModel.maximize" class="bg-white text-primary">Maximize</q-tooltip>
          </q-btn>
          <q-btn dense flat icon="close" v-close-popup @click="onHide()">
            <q-tooltip class="bg-white text-primary">Close</q-tooltip>
          </q-btn>
        </q-bar>

        <q-separator />

        <q-card-section class="modal-body scroll" :style="`height: ${autoHeight}`">
          <slot></slot>
          <!-- <div class="q-py-lg"></div> -->
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import { Screen } from 'quasar'
import { nextTick, ref, watch, onUnmounted } from 'vue'

interface Configs {
  [props: string]: any
  show: boolean
  type?: string
  title?: string
  width?: string
  maximize?: boolean
  persistent?: boolean
  show_header?: boolean
}

const emits = defineEmits(['update:modelValue', 'hide'])
const props = defineProps({
  modelValue: { type: Object as () => Configs, required: true }
  // noscroll: { type: Boolean, required: false },
})
const autoHeight = ref<string>('90vh')
let observer: ResizeObserver | null = null

const normalizeModel = (value: Configs) => {
  return {
    ...value,
    width: value?.width ?? '60vw',
    maximize: Screen.lt.sm ? true : (value?.maximize || false),
    persistent: value?.persistent ?? true,
  }
}

const dataModel = ref<Configs>(normalizeModel(props.modelValue))

const optimizeWidth = () => {
  let res = dataModel.value.width
  if (Screen.lt.md) res = '95vw'
  return res
}

const onHide = () => {
  if (dataModel.value.show) {
    dataModel.value.show = false
    emits('update:modelValue', { ...dataModel.value, show: false })
  }
  emits('hide', false)
}

const getHeight = (modalHeight: number | null = null) => {
  let height = window.innerHeight // Use window height for responsive calculation
  if (modalHeight) height = modalHeight
  else {
    const modalCard = document.querySelector('.modal-card')
    if (modalCard) height = modalCard.getBoundingClientRect().height
  }

  const modalBar = document.querySelector('.modal-bar')
  if (modalBar) height -= modalBar.getBoundingClientRect().height
  autoHeight.value = `${height}px`
}

const watchDialogProps = () => {
  if (!props.modelValue) return

  dataModel.value = normalizeModel(props.modelValue)

  if (props.modelValue.show) {
    nextTick(() => {
      const modalCard = document.querySelector('.modal-card')
      if (modalCard) {
        observer = new ResizeObserver((entries) => {
          for (const entry of entries) {
            const height = entry.contentRect.height
            if (height) getHeight(height)
          }
        })
        observer.observe(modalCard)
      }
    })
  }
}

watch(
  () => props.modelValue?.show,
  () => {
    watchDialogProps()
  },
  { immediate: true }
)

watch(
  () => props.modelValue?.maximize,
  () => {
    if (props.modelValue?.maximize !== undefined) {
      dataModel.value.maximize = props.modelValue.maximize
    }
  },
  { immediate: true }
)

watch(
  () => dataModel.value.show,
  (show) => {
    if (show !== props.modelValue?.show) {
      emits('update:modelValue', { ...dataModel.value })
    }
  }
)

watch(
  () => dataModel.value.maximize,
  (maximize) => {
    if (maximize !== props.modelValue?.maximize) {
      emits('update:modelValue', { ...dataModel.value })
    }
  }
)

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
    observer = null
    // console.log('Observer disconnected')
  }
})

watch(
  () => dataModel.value.show,
  (val) => {
    if (val) {
      history.pushState(null, '', location.href)
      window.addEventListener('popstate', onHide)
    } else {
      window.removeEventListener('popstate', onHide)
    }
  }
)
</script>
