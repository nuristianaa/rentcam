<template>
  <div>
    <s-loading v-if="loading" />
    <h-detail v-else :meta="Meta" :modal="props" @back="back">
      <!-- BADGE NOTIFICATION -->
      <div class="row q-pa-xs">
        <q-card flat class="round bg-lime-3 col-12 q-ma-sm q-px-md" v-if="msg.success">
          <h3 v-if="msg.success">
            {{ msg.success }}
            <q-icon name="check" color="green" />
          </h3>
          <div v-if="msg.failed && msg.failed.length > 0">
            <h3>
              Failed upload:
              <q-icon name="error" color="red" />
            </h3>
            <ul>
              <li v-for="val in msg.failed" :key="val">
                <div v-if="val">{{ val.app }} {{ val.name }} {{ val.msg }}</div>
              </li>
            </ul>
          </div>
          <q-btn dense class="q-my-sm q-px-lg" @click="back" color="primary" label="Close" />
        </q-card>
        <q-linear-progress indeterminate v-if="loading" class="q-mb-md" />
        <div v-else class="col-12">
          <q-stepper flat animated vertical header-nav v-model="step" color="primary">
            <q-step :name="1" title="Template Excel" icon="settings">
              <div class="col-12 q-pa-sm">
                Please make sure your xlsx file is following this template.
                <br />
                Download format from index table
                <!-- <s-link src="/template-excel/template-delivery-orders.xlsx" color="info" label="Download Example Format"></s-link> <br> -->
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
  const file = target.files ? target.files[0] : null

  if (file) {
    disableSubmit.value = false
    const map = mapFromColumns(table.columns)

    readXlsxFile(file, { map, ignoreEmptyRows: false })
      .then((result: { rows: null }) => {
        dataModel.value = result.rows
        step.value = 3
      })
      .catch((error: any) => {
        console.error('Error reading Excel file:', error)
        disableSubmit.value = true
      })
  } else {
    disableSubmit.value = true
  }
}

const mapFromColumns = (columns: { label: string; field: string }[]) => {
  return columns.reduce(
    (acc, col) => {
      acc[col.label] = col.field
      return acc
    },
    {} as Record<string, string>
  )
}

const submit = () => {
  const payload = {
    bulk: true,
    items: dataModel.value
  }

  disableSubmit.value = true
  loading.value = true

  API.post(Meta.module, payload, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      msg.value.success = data.success
      msg.value.failed = data.failed || []
    } else {
      disableSubmit.value = false
    }
  })
}

const back = () => {
  emit('refreshEvent')
}
</script>
