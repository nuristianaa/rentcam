<template>
  <div class="row">
    <div class="col-12 col-sm-6 row q-pa-md">
      <FormulaParser class="col-12" v-model="dataModel.result" :sources="dataModel.sources" :formula="dataModel.formula" :references="dataModel.references" @update:modelValue="onUpdated" cleanFields @change="(val, err, err_raw, raw) => onChange(val, err, err_raw, raw)" />
    </div>
    <div class="col-12 col-sm-6 row">
      <json-viewer :data="{ result, error, error_raw, raw_fields }" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import FormulaParser from './FormulaParser.vue'

const dataModel = ref({
  code: 'GAR',
  formula: '{base price}*{demmurage_rate}',
  sources: [
    { refCol: 'shipment.base_price', key: 'base price', value: 14.56 },
    { refCol: 'shipment.quality_result', key: 'quality_result', value: 13.245 },
    { refCol: 'shipment.quality_min', key: 'quality_min', value: 300 },
    { refCol: 'shipment.quality_max', key: 'quality_max', value: 400 },
    { refCol: 'shipment.loading_time', key: 'loading_time', value: 150 }
  ],
  references: [
    { referenceName: 'demmurage', label: 'Demmurage', formula: 'if ({loading_time}>100, "Charge", "-")' },
    { referenceName: 'demmurage_rate', label: 'Demmurage Rate', formula: 'if ({demmurage}="Charge", {base price}*{quality_result}-(10*100), {base price}*{quality_result}+(10*100))' }
  ],
  result: null
})

const result = ref('')
const error = ref(null)
const raw_fields = ref(null)
const error_raw = ref([])

const onUpdated = (v: any) => {
  result.value = v
}

const onChange = (val: any, err: any = null, err_raw: any = [], raw: any = null) => {
  error.value = err
  error_raw.value = err_raw
  raw_fields.value = raw
}
</script>
