<template>
  <div v-if="table" class="log-info-table">
    <span v-if="data.deleted_by">
      <q-badge color="red">D</q-badge>
      {{ data.deleted_by }} | {{ Helper.readDate(data.deleted_at, true) }}
    </span>
    <span v-else-if="data.updated_by">
      <q-badge color="info">U</q-badge>
      {{ data.updated_by }} | {{ Helper.readDate(data.updated_at, true) }}
    </span>
    <span v-else-if="data.created_by">
      <q-badge color="primary">C</q-badge>
      {{ data.created_by }} | {{ Helper.readDate(data.created_at, true) }}
    </span>
    <q-tooltip>
      <span v-if="data.created_by">
        <q-badge color="primary">C</q-badge>
        {{ data.created_by }} | {{ Helper.readDate(data.created_at, true) }}
      </span>
      <br />
      <span v-if="data.updated_by">
        <q-badge color="info">U</q-badge>
        {{ data.updated_by }} | {{ Helper.readDate(data.updated_at, true) }}
      </span>
      <br />
      <span v-if="data.deleted_by">
        <q-badge color="red">D</q-badge>
        {{ data.deleted_by }} | {{ Helper.readDate(data.deleted_at, true) }}
      </span>
    </q-tooltip>
  </div>
  <div v-else class="log-info">
    <span v-if="data.created_by">
      <q-badge color="primary">C</q-badge>
      {{ Helper.readDate(data.created_at, true) }} | {{ data.created_by }}
    </span>
    <br />
    <span v-if="data.updated_by">
      <q-badge color="info">U</q-badge>
      {{ Helper.readDate(data.updated_at, true) }} | {{ data.updated_by }}
    </span>
    <br />
    <span v-if="data.deleted_by">
      <q-badge color="red">D</q-badge>
      {{ Helper.readDate(data.deleted_at, true) }} | {{ data.deleted_by }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { Helper } from 'src/services/helper'
const props = defineProps<{
  data?: any
  table?: boolean
}>()
</script>
