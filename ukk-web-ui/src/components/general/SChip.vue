<template>
  <div :class="col ? `q-px-sm col-12 col-md-6 col-lg-${col}` : ''">
    <q-chip square class="chip-box">
      <q-avatar :icon="icon" :color="props.color" text-color="white" />
      <div class="row chip-box_wrapper">
        <div class="chip-box_title col-12">{{ props.title }}</div>
        <div class="chip-box_label col-12">{{ props.label }}</div>
      </div>
    </q-chip>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  col: { type: [String], default: '3' },
  icon: { type: String, default: 'info_outline' },
  color: { type: String, default: 'primary' },
  title: { type: String, default: '' },
  label: { type: String, default: '' }
})
</script>

<style>
.chip-box {
  height: 3.1em;
  width: 100%;
}

.chip-box .q-avatar {
  height: 1.55em;
  width: 1.54em;
}

.chip-box .q-avatar i {
  font-size: 18pt;
}

.chip-box_wrapper {
  padding-left: 5px;
}

.chip-box_title {
  font-size: 8pt;
}

.chip-box_label {
  font-size: 11pt;
  opacity: 0.5;
  font-weight: bold;
}
</style>
