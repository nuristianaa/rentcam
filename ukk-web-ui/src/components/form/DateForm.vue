<template>
  <div :class="col ? `q-px-sm col-12 col-md-6 col-lg-${col}` : ''">
    <label class="text-subtitle2 text-grey q-ml-sm">
      {{ required ? `${label}*` : label }}
    </label>
    <q-input
      dense
      v-model="dataModel"
      :hide-bottom-space="props.hideBottomSpace"
      :borderless="props.borderless"
      :outlined="props.borderless ? false : true"
      :class="props.boxClass"
      :style="props.style"
      :readonly="props.readonly"
      :placeholder="props.placeholder"
      :input-class="props.inputClass"
      :mask="masking"
      :prefix="props.prefix"
      :hint="props.hint"
      @blur="emiters(dataModel, $event)"
      @update:modelValue="directUpdate(dataModel)"
      @keydown.enter.prevent="handleEnter(dataModel)"
      :rules="props.norules ? undefined : [(val: string) => validate.validateDate(val, maskDate, props.range, props.required) || `${label} is not valid!`]"
    >
      <template v-slot:hint>
        <slot name="hint"></slot>
      </template>

      <template v-slot:prepend>
        <slot name="prepend"></slot>
      </template>
      <template v-slot:before>
        <slot name="before"></slot>
      </template>

      <template v-slot:append>
        <q-icon v-if="!time" name="event" class="cursor-pointer">
          <q-popup-proxy v-model="popupDate" ref="qDateProxy" transition-show="scale" transition-hide="scale">
            <q-date v-if="range" v-model="rangeDate" :mask="maskDate" @update:modelValue="setDateRangeValue(rangeDate)" :readonly="props.readonly" :options="props.options" range>
              <div class="row items-center justify-end q-gutter-sm">
                <q-btn label="Close" color="primary" flat v-close-popup />
              </div>
            </q-date>

            <DateYm v-else-if="yearMonth" v-model="dataModel" @updatevalue="emiters" @hide="popupDate = false" :readonly="props.readonly" />

            <q-date v-else v-model="dataModel" :mask="maskDate" default-view="Calendar" @update:modelValue="emiters($event)" @navigation="handlerNav" :readonly="props.readonly" :options="props.options">
              <div class="row items-center justify-end q-gutter-sm">
                <q-btn label="Close" color="primary" flat v-close-popup />
              </div>
            </q-date>
          </q-popup-proxy>
        </q-icon>

        <q-icon v-if="time || datetime" name="access_time" class="cursor-pointer">
          <q-popup-proxy ref="qTimeProxy" transition-show="scale" transition-hide="scale">
            <q-time v-model="dataModel" @update:modelValue="emiters($event)" :mask="maskDate" format24h :readonly="props.readonly">
              <div class="row items-center justify-end">
                <q-btn v-close-popup label="Close" color="primary" flat />
              </div>
            </q-time>
          </q-popup-proxy>
        </q-icon>
      </template>

      <template v-slot:after>
        <slot name="after"></slot>
      </template>
    </q-input>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import DateYm from './DateYm.vue'
import validate from 'src/services/helper/validate'
import { Helper } from 'src/services/helper'

interface RangeDate {
  from: string
  to: string
}

const props = defineProps<{
  modelValue: string | number | null
  col?: string
  boxClass?: string
  inputClass?: string
  style?: string
  label?: string
  placeholder?: string
  // mask?: string
  prefix?: string
  hint?: string
  required?: boolean
  readonly?: boolean
  borderless?: boolean
  norules?: boolean
  range?: boolean
  datetime?: boolean
  millis?: boolean
  time?: boolean
  yearMonth?: boolean
  hideBottomSpace?: boolean
  emitValue?: boolean
  options?: any
}>()

// const props = defineProps({
// modelValue: { type: [String, Number, null], required: true },
// col: { type: [String, Number], required: false },
// boxClass: { type: String, required: false },
// inputClass: { type: String, required: false },
// style: { type: String, required: false },
// label: { type: String, required: false },
// placeholder: { type: String, required: false },
// mask: { type: String, required: false },
// prefix: { type: String, required: false },
// hint: { type: String, required: false },
// required: { type: Boolean, required: false },
// readonly: { type: Boolean, required: false },
// borderless: { type: Boolean, required: false },
// norules: { type: Boolean, required: false },
// range: { type: Boolean, required: false },
// datetime: { type: Boolean, required: false },
// millis: { type: Boolean, required: false },
// time: { type: Boolean, required: false },
// yearMonth: { type: Boolean, required: false },
// })

const emits = defineEmits(['update:modelValue', 'enterEvent', 'updateRange', 'blur'])

const H = Helper
const rangeDate = ref<RangeDate | null>(null)
const dataModel = ref<string | null>(null)
const popupDate = ref(false)

const masking = computed(() => {
  if (props.datetime) return '####-##-## ##:##'
  if (props.millis) return '####-##-## ##:##'
  if (props.time) return '##:##'
  if (props.range) return ''
  if (props.yearMonth) return 'SSS ####'
  return '####-##-##'
})

const maskDate = computed(() => {
  if (props.datetime) return 'YYYY-MM-DD HH:mm'
  if (props.millis) return 'YYYY-MM-DD HH:mm'
  if (props.time) return 'HH:mm'
  if (props.yearMonth) return 'MMM YYYY'
  return 'YYYY-MM-DD'
})

const init = () => {
  let date = ''
  if (props.modelValue) {
    if (props.range) {
      if (typeof props.modelValue === 'string') {
        const split = props.modelValue.split(' to ')
        if (split[1] !== undefined) {
          const from = split[0]
          const to = split[1]
          if (from && to) {
            const fromDate = H.toDate(from, 'YYYY-MM-DD')
            const toDate = H.toDate(to, 'YYYY-MM-DD')
            date = `${fromDate} to ${toDate}`
            rangeDate.value = { from: fromDate, to: toDate }
          }
        }
      }
    } else if (props.yearMonth) date = H.toDate(props.modelValue, 'MMM YYYY')
    else if (props.datetime) date = H.toDate(props.modelValue, 'YYYY-MM-DD HH:mm')
    else if (props.millis) date = H.toDate(props.modelValue, 'YYYY-MM-DD HH:mm')
    else if (props.time === undefined) date = H.toDate(props.modelValue, 'YYYY-MM-DD')
    else date = props.modelValue.toString()
  }
  dataModel.value = date
}

const handlerNav = (e: any) => {
  if (!e.year && !e.month) (globalThis as any).$refs.qDateProxy.hide()
}

const emiters = (e: any, event: any = null) => {
  let doupdate = false
  if (!event) {
    doupdate = true
  } else if (event && event.relatedTarget) {
    doupdate = true
  } else if (event && event.relatedTarget == null) {
    doupdate = false
  }

  if (doupdate) {
    let value = e
    if (props.millis) value = H.date2millis(e)
    if (props.yearMonth) value = H.ym2date(e)
    if (value == '') value = null
    emits('update:modelValue', value)
    emits('blur', value)
  }
}

const directUpdate = (e: any) => {
  if (props.emitValue) {
    if (e == '') e = null
    emits('update:modelValue', e)
  }
}

const handleEnter = (e: any) => {
  let value = e
  if (props.millis) value = H.date2millis(e)
  if (props.yearMonth) value = H.ym2date(e)
  if (value == '') value = null
  emits('update:modelValue', value)
  emits('enterEvent', value)
}

const setDateRangeValue = (val: any) => {
  if (val) {
    emits('updateRange', val)
    let value
    if (typeof val === 'string') {
      value = val
      dataModel.value = value
    } else {
      let from = val.from
      let to = val.to
      if (props.millis) {
        from = H.date2millis(val.from, true)
        to = H.date2millis(val.to, true) + 86399000
      }
      value = `${from} to ${to}`
      dataModel.value = `${val.from} to ${val.to}`
    }
    emiters(value)
  }
}

watch(() => props.modelValue, init)

onMounted(init)
</script>
