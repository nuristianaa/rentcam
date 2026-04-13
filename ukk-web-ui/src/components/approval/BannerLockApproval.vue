<template>
  <s-banner class="q-mb-lg" color="red-8">
    <q-icon name="warning" class="q-mr-sm" size="21px" />
    <span class="text-h4 q-pt-xs" style="position: relative; top: 2px">
      Cannot Edit this document because Approval status is
      <b>{{ status }}</b>
      !
    </span>
  </s-banner>
</template>

<script setup lang="ts">
interface Props {
  mode?: string // edit
  status: string //
}

const props = defineProps<Props>()
</script>
