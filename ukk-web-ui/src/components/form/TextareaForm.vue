<template>
  <div :class="col ? `q-px-sm col-10 col-md-6 col-lg-${col}` : ''">
    <div v-if="rich">
      <div class="text-bold q-pb-md">{{ required ? `${label} *` : label }}</div>
      <q-editor outlined :rows="rows" :class="boxClass" :style="style" :modelValue="dataModel" @update:modelValue="handleUpdate" @blur="handleBlur" :min-height="`${rows ? rows : 3}rem`" dense />
    </div>
    <div v-else>
      <label class="text-subtitle2 text-grey q-ml-sm">
        {{ required ? `${label}*` : label }}
      </label>
      <q-input
        outlined
        dense
        type="textarea"
        :rows="rows"
        :hideBottomSpace="hideBottomSpace"
        :class="boxClass"
        :style="style"
        :modelValue="dataModel"
        @update:modelValue="handleUpdate"
        @blur="handleBlur"
        lazy-rules
        :rules="norules ? undefined : required ? [(val) => validate.validateRequired(val) || label + ' must be filled!'] : [(val) => val != ' ' || 'clear space!']"
        :readonly="readonly"
        :placeholder="placeholder"
        :hint="hint"
      >
        <template v-slot:prepend>
          <slot name="prepend"></slot>
        </template>
        <template v-slot:before>
          <slot name="before"></slot>
        </template>
        <template v-slot:append>
          <slot name="append"></slot>
        </template>
        <template v-slot:after>
          <slot name="after"></slot>
        </template>
      </q-input>
    </div>
  </div>
</template>

<script setup lang="ts">
import validate from 'src/services/helper/validate'
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: { type: [String, null], required: true },
  col: { type: [String], default: '' },
  boxClass: { type: String, required: false },
  inputClass: { type: String, required: false },
  style: { type: String, required: false },
  label: { type: String, required: false },
  placeholder: { type: String, required: false },
  mask: { type: String, required: false },
  prefix: { type: String, required: false },
  hint: { type: String, required: false },
  required: { type: Boolean, required: false },
  readonly: { type: Boolean, required: false },
  borderless: { type: Boolean, required: false },
  norules: { type: Boolean, required: false },
  inline: { type: Boolean, default: false },
  rich: { type: Boolean, default: false },
  hideBottomSpace: { type: Boolean, default: false },
  rows: { type: Number, default: 3 }
})

const emit = defineEmits(['update:modelValue', 'blur', 'updateEvent'])

const dataModel = ref(props.modelValue as string)

watch(
  () => props.modelValue,
  (newVal) => {
    dataModel.value = newVal as string
  }
)

const handleUpdate = (value: string | number | null) => {
  dataModel.value = value as string
  emit('update:modelValue', value)
  emit('updateEvent', value)
}

const handleBlur = (event: Event) => {
  emit('blur', event)
}
</script>
