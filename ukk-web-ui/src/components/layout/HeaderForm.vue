<template>
  <div>
    <!-- CONTENT ON PAGE -->
    <q-page v-if="modal === undefined" style="height: 90vh; overflow: hidden">
      <div :class="`${page_class} ${$q.dark.isActive ? 'bg-dark' : 'bg-white'}`" style="height: 100%; overflow: hidden; border-radius: 8px 0px 0px 0px">
        <q-form @submit.prevent="onSubmit()">
          <!-- HEAD -->
          <div :class="`row col-12 q-py-sm q-px-lg q-ml-xs q-mr-md items-end ${header_class}`" v-if="!props.hide_header">
            <!-- Back Button -->
            <div>
              <q-btn v-if="!meta.hide_back" flat dense no-caps class="q-pb-none text-grey text-bold" label="back" icon="chevron_left" @click="$emit('back')" />
              <div class="text-left q-pb-sm q-pl-sm">
                <div class="subtitle text-grey q-pa-none">
                  <strong class="text-capitalize text-info">
                    {{ meta.title ?? '' }}
                  </strong>
                  <template v-if="!meta.hide_subtitle">Form</template>
                </div>
              </div>
            </div>

            <slot name="top-left"></slot>

            <q-space />

            <!-- Action on Form -->
            <div class="q-pb-sm q-gutter-sm self-end q-mt-sm">
              <slot name="buttons">
                <q-btn v-if="!meta.hide_cancel" outline rounded label="Cancel" @click="$emit('back')" />
                <q-btn unelevated rounded label="Save" color="primary" icon="check_circle" type="submit" class="text-bold" :disable="disableSubmit" />
              </slot>
            </div>
          </div>
          <!-- BODY -->
          <div style="height: 90vh; overflow: auto" :class="content_class">
            <div class="q-px-md q-pb-md">
              <slot></slot>
            </div>
            <div class="q-py-lg"></div>
          </div>
        </q-form>
      </div>
    </q-page>

    <!-- HEADER ON MODAL -->
    <div v-else>
      <q-form @submit.prevent="onSubmit()">
        <div>
          <!-- HEADER -->
          <div class="form-actions row items-center justify-between q-px-sm q-py-sm">
            
            <!-- LEFT SIDE -->
            <div class="row items-center q-gutter-sm">
              <template v-if="$slots['top-left']">
                <slot name="top-left"></slot>
              </template>

              <div class="column q-pa-none">
                <div class="subtitle text-grey q-pa-none">
                  <strong class="text-capitalize text-info">
                    {{ meta.title ?? '' }}
                  </strong>
                </div>
              </div>
            </div>

            <!-- RIGHT SIDE: buttons -->
            <div class="row q-gutter-x-sm" v-if="!props.hide_header">
              <slot name="buttons">
                <q-btn v-if="!meta.hide_cancel" outline label="Cancel" v-close-popup />
                <q-btn unelevated label="Save" color="primary" icon="check_circle" type="submit" class="text-bold" :disable="disableSubmit" />
              </slot>
            </div>

          </div>

          <q-separator></q-separator>


          <!-- BODY -->
          <div class="q-pt-sm q-mt-md q-px-md q-pb-md" :style="`height: ${autoHeight}; overflow: auto`">
            <slot></slot>
          </div>
        </div>
      </q-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { nextTick, onMounted, onUnmounted, ref } from 'vue'

interface Meta {
  title?: string
  hide_back?: boolean
  hide_cancel?: boolean
  hide_subtitle?: boolean
}

const emit = defineEmits(['back', 'submit'])
const props = defineProps<{
  meta: Meta
  disableSubmit?: boolean
  modal?: any
  hide_header?: boolean
  hide_subtitle?: boolean
  page_class?: string | null
  header_class?: string | null
  content_class?: string | null
}>()
const autoHeight = ref<string>('87vh')
let observer: ResizeObserver | null = null

const getHeight = (modalHeight: number | null = null) => {
  // height for responsive calculation
  let height = window.innerHeight
  if (modalHeight) height = modalHeight
  else {
    const modalCard = document.querySelector('.modal-card')
    if (modalCard) height = modalCard.getBoundingClientRect().height
  }
  const modalBar = document.querySelector('.modal-bar')
  if (modalBar) height -= modalBar.getBoundingClientRect().height
  const formActions = document.querySelector('.form-actions')
  if (formActions) height -= formActions.getBoundingClientRect().height
  // if (modalCard) console.log('modalCard: ', modalCard.getBoundingClientRect().height)
  // if (modalBar) console.log('modalBar: ', modalBar.getBoundingClientRect().height)
  // if (formActions) console.log('formActions: ', formActions.getBoundingClientRect().height)
  autoHeight.value = `${height - 45}px`
}

const onSubmit = () => {
  requestAnimationFrame(() => {
    emit('submit')
  })
}

onMounted(() => {
  nextTick(() => {
    const modalCard = document.querySelector('.modal-card')
    if (modalCard) {
      observer = new ResizeObserver((entries) => {
        for (const entry of entries) {
          const height = entry.contentRect.height
          if (height) {
            getHeight(height)
          }
        }
      })
      observer.observe(modalCard)
    }
  })
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
    observer = null
    // console.log('Observer disconnected')
  }
})
</script>

<style scoped lang="scss">
// .q-toolbar {
//   background-color: white;
//   border-bottom: solid 1pt $grey-5;
//   color: $grey-9;
// }

// .body--dark .q-toolbar {
//   background-color: $dark;
//   color: white;
// }

// .header-toolbar {
//   background-color: $grey-2;
//   color: $grey-9;
// }

// .body--dark .header-toolbar {
//   background-color: $grey-9;
//   color: white;
// }
</style>
