<template>
  <div>
    <!-- CONTENT ON PAGE -->
    <q-page v-if="modal === undefined" style="height: 90vh; overflow: hidden">
      <div :class="$q.dark.isActive ? 'bg-dark' : 'bg-white'" style="height: 100%; overflow: hidden; border-radius: 8px 0px 0px 0px" class="q-pl-sm">
        <!-- HEADER -->
        <div class="row col-12 q-py-sm q-px-lg q-ml-xs q-mr-md items-end">
          <!-- Back Button -->
          <div>
            <q-btn v-if="!meta.hide_back" flat dense no-caps class="q-pb-none text-grey text-bold" label="back" icon="chevron_left" @click="back" />
            <div class="text-left q-pb-sm q-pl-sm">
              <div class="subtitle text-grey q-pa-none">
                <strong class="text-capitalize text-info">
                  {{ meta.title ?? '' }}
                </strong>
                Detail
              </div>
            </div>
          </div>

          <q-space />

          <!-- Action -->
          <div class="q-pb-sm q-gutter-sm self-end">
            <slot name="buttons"></slot>
            <q-btn outline :label="$q.screen.gt.sm ? 'Edit' : ''" color="info" icon="edit" @click="edit" v-if="meta.permission.update && !meta.hide_edit && model" />
          </div>
        </div>
        <!-- BODY -->
        <div style="height: 90vh; overflow: auto">
          <slot></slot>
          <div class="q-py-lg"></div>
        </div>
      </div>
    </q-page>
    <div v-else>
      <!-- HEADER -->
        <div class="row col-12 q-py-sm q-ml-xs q-mr-md items-end">
          <!-- Back Button -->
          <div>
            <!-- <q-btn v-if="!meta.hide_back" flat dense no-caps class="q-pb-none text-grey text-bold" label="back" icon="chevron_left" @click="back" /> -->
            <div class="text-left q-pb-sm q-pl-sm">
              <div class="subtitle text-grey q-pa-none">
                <strong class="text-capitalize text-info">
                  {{ meta.title ?? '' }}
                </strong>
                Detail
              </div>
            </div>
          </div>

          <q-space />
          <div class="row q-gutter-x-sm" v-if="!props.hide_header">
            <slot name="additional-buttons"></slot>
            <q-btn v-if="!meta.hide_cancel" outline label="Close" v-close-popup />
          </div>
        </div>
      <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'

interface Meta {
  title?: string
  hide_back?: boolean
  permission: {
    update: boolean
  }
  hide_edit?: boolean
  module: string
  back_query?: Record<string, any>
}

interface Model {
  id: number | string
}

const props = defineProps<{
  meta: Meta
  model?: Model
  title?: string
  modal?: any
}>()

const emit = defineEmits(['back'])
const router = useRouter()
const route = useRoute()

function edit() {
  const url = props.meta.module
  const id = props.model ? { id: props.model.id } : {}
  console.log(`edit-${url}`)
  router.push({ name: `edit-${url}`, params: id, query: route.query })
}

function back() {
  // const url = props.meta.module;
  // let query = props.meta.back_query ?? {};
  // if (route.query.page) query = route.query;
  // router.push({ name: url, query });
  emit('back')
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
