<template>
  <div>
    <s-loading v-if="loading" />
    <h-detail v-else :meta="Meta" :modal="props" @back="back">
      <div class="row q-pa-xs">
        <!-- BADGE NOTIFICATION -->
        <q-card flat class="round bg-accent q-pa-md col-12 column q-gutter-xs" v-if="msg.success">
          <div class="row items-center justify-between">
            <div class="title">Result</div>
            <q-btn dense class="q-px-lg" @click="back" color="primary" label="Close" />
          </div>
          <div class="subtitle">
            - {{ msg.success }}
            <q-icon name="check" color="positive" />
          </div>
          <div class="" v-if="msg.failed && msg.failed.length > 0">
            <div class="subtitle">
              - Failed upload:
              <q-icon name="error" color="red" />
            </div>
            <r-table :columns="table.columns" :model-value="msg.failed" no-export>
              <template v-slot:body-cell-action="prp">
                <div v-if="prp.props.row?.msg" class="text-red">
                  {{ prp.props.row?.msg }}
                </div>
              </template>
            </r-table>
          </div>
        </q-card>
        <q-linear-progress indeterminate v-if="loading" class="q-mb-md" />
        <div v-else class="col-12">
          <q-stepper flat animated vertical header-nav v-model="step" color="primary">
            <q-step :name="1" title="Template Excel" icon="settings">
              <div class="col-12 q-pa-sm">
                Please make sure your xlsx file is following this template.
                <br />
                Download format from index table
                <q-btn @click="downloadTemplate" color="info" label="Download Example Format" />
              </div>
              <q-stepper-navigation>
                <q-btn @click="step = 2" color="primary" label="Continue" />
              </q-stepper-navigation>
            </q-step>
            <q-step :name="2" title="Please upload your .xlsx file" icon="create_new_folder">
              <div class="col-12 q-pa-sm">
                <input type="file" @change="onFileChange" />
              </div>
              <q-stepper-navigation>
                <q-btn @click="step = 1" outline color="primary" label="Back" class="q-mr-sm" />
                <q-btn :disabled="disableSubmit" @click="step = 3" color="primary" label="Continue" />
              </q-stepper-navigation>
            </q-step>

            <q-step :name="3" title="Review" icon="settings">
              <q-stepper-navigation></q-stepper-navigation>
              <r-table v-if="dataModel" :columns="table.columns" :model-value="dataModel" no-export />
              <q-stepper-navigation>
                <q-btn @click="step = 2" outline color="primary" label="Back" class="q-mr-sm" />
                <q-btn :disabled="disableSubmit" @click="submit" color="positive" label="Save" />
              </q-stepper-navigation>
            </q-step>
          </q-stepper>
        </div>
      </div>
    </h-detail>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import readXlsxFile from 'read-excel-file'
import { ref, reactive } from 'vue'
import { Constant } from 'src/services/constant'
import { Helper } from 'src/services/helper'
import { Lang } from 'src/services/lang'
import { Meta } from './meta'
import { Handler } from 'src/services/handler'

const props = defineProps<{ props?: { id?: string | number } }>()
const emit = defineEmits(['refreshEvent'])

const API = new Api()
const loading = ref(false)
const dataModel = ref(null)
const disableSubmit = ref(true)
const step = ref(1)
const msg = ref<any>({
  success: null,
  failed: []
})

const table = reactive({
  search: '',
  columns: Meta.table(Helper, Constant, Lang)
})

// METHODS
const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0] || null
  if (!file) {
    disableSubmit.value = true
    return
  }
  disableSubmit.value = false

  readXlsxFile(file)
    .then((result: any) => {
      mapExcelResult(result)
      step.value = 3
    })
    .catch((error: any) => {
      console.error('Error reading Excel file:', error)
      disableSubmit.value = true
    })
}

const mapExcelResult = (result: any) => {
  // Convert result → dataModel
  const headers = result[0]
  const rows = result.slice(1)

  // Build a map: label → field
  const metaTable = Meta.tableExport(Helper, Constant, Lang)
  const labelToField = metaTable.reduce<Record<string, string>>((acc, col) => {
    acc[col.label] = col.field
    return acc
  }, {})

  // Transform each row
  dataModel.value = rows.map((row: any) => {
    return headers.reduce((obj: any, header: any, index: any) => {
      const field = labelToField[header]
      if (field) obj[field] = row[index]
      return obj
    }, {})
  })
}

const submit = () => {
  disableSubmit.value = true
  loading.value = true

  void API.post(`${Meta.module}/bulk`, dataModel.value, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      msg.value.success = data.success
      msg.value.failed = data.failed || []
    } else {
      disableSubmit.value = false
    }
  })
}

const downloadTemplate = () => {
  Handler.exportXLS(Meta) // Must have tableExport & tableExportSample in Meta
}

const back = () => {
  emit('refreshEvent')
}
</script>
