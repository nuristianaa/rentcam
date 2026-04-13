<template>
  <q-card flat style="border-radius: 0px 0px 0px 0px" class="q-pa-md">
    <div :class="`row col-12 q-py-sm q-mr-md items-end`">
        <!-- Back Button -->
        <div>
          <div class="text-left q-pb-sm">
            <div class="title text-grey q-pa-none">
              <strong class="text-capitalize text-primary">
                {{ meta.title ?? '' }}
              </strong>
            </div>
          </div>
        </div>
        <q-space />
      </div>
    <slot></slot>
  </q-card>
</template>
<script setup lang="ts">
  interface Meta {
    title?: string
  }
  const props = defineProps<{
    meta: Meta
  }>()
</script>

<script setup lang="ts"></script>

<!-- <style scoped lang="scss">
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
</style> -->
