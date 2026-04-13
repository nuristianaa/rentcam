<template>
  <q-card-actions align="right" class="q-px-md">
    <q-btn v-if="$q.screen.gt.sm && noCancel === undefined" flat label="Cancel" color="primary" icon="cancel" @click="$emit('back')" />
    <q-btn v-else-if="noCancel === undefined" flat dense round color="primary" icon="cancel" @click="$emit('back')">
      <q-tooltip v-if="$q.screen.lt.md">Cancel</q-tooltip>
    </q-btn>

    <q-btn v-if="$q.screen.gt.sm" label="Save" color="primary" icon="check_circle" :disable="disableSubmit" type="submit" />
    <q-btn v-else flat dense round color="primary" icon="check_circle" :disable="disableSubmit" type="submit">
      <q-tooltip>Save</q-tooltip>
    </q-btn>
  </q-card-actions>
</template>

<script setup lang="ts">
const props = defineProps<{
  noCancel?: boolean
  disableSubmit?: boolean
}>()
</script>
