<template>
  <q-page class="q-pl-sm" style="height: 90vh; overflow: hidden">
    <div :class="$q.dark.isActive ? 'bg-dark' : 'bg-white'" style="height: 100%; overflow: hidden; border-radius: 8px 0px 0px 0px">
      <!-- HEADER -->
      <div v-if="meta" class="row justify-between q-pt-md q-px-md">
        <div v-if="hideTitle === undefined && $q.screen.lt.md && (meta.buttons || meta.tabs)"></div>
        <div v-else-if="hideTitle === undefined" class="title text-primary">
          {{ titleName }}
        </div>

        <div v-if="buttons.length > 0" class="text-right q-gutter-sm">
          <q-btn v-for="b in buttons" :key="b.url" :color="b.color" :icon="b.icon" :label="b.label" @click="customUrl(b.url, b.data)" />
        </div>
        <div v-if="tabOpt.length > 0" class="text-right">
          <q-tabs v-model="tab" dense inline-label class="text-body2" active-color="primary" indicator-color="primary" align="left" no-caps :style="`max-width: ${$q.screen.width - 150}px`">
            <div v-for="val in tabOpt" :key="val.id">
              <q-tab v-if="$q.screen.lt.md" :name="val.name" :icon="val.icon ?? 'table_view'">
                <q-tooltip>{{ val.label }}</q-tooltip>
              </q-tab>
              <q-tab v-else :name="val.name" :label="val.label" :icon="val.icon ?? 'table_view'" />
            </div>
          </q-tabs>
        </div>
      </div>
      <!-- BODY -->
      <div style="height: 90vh; overflow: auto">
        <slot></slot>
        <div v-if="meta.add_bottom_space" class="q-py-md"></div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRouter } from 'vue-router'

interface Meta {
  title?: string
  buttons?: Button[]
  tabs?: TabOption[]
  tabValue?: string
  add_bottom_space?: boolean
  slug?: string
  module?: string
  back_query?: Record<string, any>
}

interface Button {
  url: string
  color: string
  icon: string
  label: string
  data?: Record<string, any>
}

interface TabOption {
  id: number | string
  name: string
  label: string
  icon?: string
}

const props = defineProps<{
  meta: Meta
  trash?: boolean
  type?: string
  model?: any
  typeName?: string
  title?: string
  hideTitle?: boolean
}>()

const emit = defineEmits(['tabEvent'])
const router = useRouter()
const typeName = ref(props.typeName || null)
const titleName = computed(() => props.meta?.title || typeName.value || '')
const buttons = ref<Button[]>(props.meta?.buttons || [])
const tab = ref<string | null>(props.meta?.tabValue || null)
const tabOpt = ref<TabOption[]>(props.meta?.tabs || [])

watch(
  () => props.meta?.buttons,
  () => {
    buttons.value = props.meta?.buttons || []
  }
)

watch(tab, (newTab) => {
  if (newTab) emit('tabEvent', newTab)
})

function customUrl(url: string, data?: Record<string, any>) {
  const query = data ? { query: data } : {}
  router.push({ name: url, ...query })
}
</script>

<style scoped lang="scss">
.q-toolbar {
  background-color: white;
  border-bottom: solid 1pt $grey-5;
  color: $grey-9;
}
.body--dark .q-toolbar {
  background-color: $dark;
  color: white;
}
.header-toolbar {
  background-color: $grey-2;
  color: $grey-9;
}
.body--dark .header-toolbar {
  background-color: $grey-9;
  color: white;
}
</style>
