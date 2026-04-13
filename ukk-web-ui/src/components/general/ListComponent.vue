<template>
  <div class="row items-start q-pb-xs" :class="props.uppercase ? 'text-uppercase' : ''">
    <div class="col-5 col-md-4">
      <slot name="left">
        <div class="row items-start justify-between">
          <div class="col-10 text-capital" style="text-transform: capitalize">
            {{ data.label }}
            <slot name="after-label"></slot>
          </div>
          <div class="text-right q-mr-sm">:</div>
        </div>
      </slot>
    </div>
    <div class="col-7 col-md-8 text-bold">
      <div class="row items-start">
        <slot name="right">
          <span v-if="data.value === true">
            Yes <q-icon name="check" color="green" />
          </span>
          <span v-else-if="data.value === false">
            No <q-icon name="cancel" color="red" />
          </span>
          <span v-else-if="data.link">
            <q-btn class="q-mb-xs" size="xs" unelevated :href="data.link" target="_blank" :color="data.color" :label="data.value" />
          </span>
          <span v-else-if="data.is_badge">
            <q-btn class="q-mb-xs" size="xs" unelevated :color="data.color" :label="data.value" />
          </span>
          <span v-else-if="data.is_html" v-html="data.value"></span>
          <span v-else :class="data.color ? `text-${data.color}` : ''">
            {{ data.value }}
          </span>

          <span v-if="data.subValue" class="col-12">
            <span v-if="data.subValue !== '' && data.subValue !== 'null'" class="bg-blue text-white q-px-xs text-bold">
              {{ data.subValue }}
            </span>
          </span>

          <slot name="after-value"></slot>
        </slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Data {
  label: string
  value: string | boolean | number | undefined
  color?: string
  link?: string
  is_badge?: boolean
  is_html?: boolean
  subValue?: string | null
  details?: Data[]
}

const props = defineProps<{
  data: Data
  uppercase?: boolean
}>()
</script>
