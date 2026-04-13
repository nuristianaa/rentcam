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
            <r-table v-if="msg.failed" :columns="table.columns" :model-value="msg.failed" :meta="Meta">
              <template v-slot:body-cell-action="prp">
                {{ prp.props.row.msg }}
              </template>
            </r-table>
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
                <q-btn @click="downloadTemplate" color="info" label="Download Example Format" />
              </div>
              <q-stepper-navigation>
                <q-btn @click="step = 2" color="primary" label="Continue" />
              </q-stepper-navigation>
            </q-step>
            <q-step :name="2" title="Please upload your .xlsx file" icon="create_new_folder">
              <div class="col-12 q-pa-sm">
                <!-- Permissions File -->
                <div class="q-mb-md">
                  <label class="text-bold text-primary">Permissions File</label>
                  <div class="q-pa-sm q-mt-sm border -borders cursor-pointer bg-grey-2 hover:bg-grey-3">
                    <input type="file" class="w-full cursor-pointer" @change="onPermissionFileChange" />
                  </div>
                </div>

                <!-- Roles File -->
                <div>
                  <label class="text-bold text-primary">Roles File</label>
                  <div class="q-pa-sm q-mt-sm border -borders cursor-pointer bg-grey-2 hover:bg-grey-3">
                    <input type="file" class="w-full cursor-pointer" @change="onFileChange" />
                  </div>
                </div>
              </div>

              <q-stepper-navigation>
                <q-btn @click="step = 1" outline color="primary" label="Back" class="q-mr-sm" />
                <q-btn :disabled="disableSubmit" @click="step = 3" color="primary" label="Continue" />
              </q-stepper-navigation>
            </q-step>

            <q-step :name="3" title="Review" icon="settings">
              <q-stepper-navigation></q-stepper-navigation>
              <q-tabs v-model="tableTab" dense class="text-grey" active-color="primary" indicator-color="primary" align="justify" narrow-indicator>
                <q-tab name="roles" label="Roles" />
                <q-tab name="permissions" label="Permissions" />
              </q-tabs>

              <q-separator />

              <q-tab-panels v-model="tableTab" animated>
                <q-tab-panel name="roles">
                  <div class="text-h6">Roles</div>
                  <r-table v-if="dataModel" :columns="table.columns" :model-value="dataModel" no-export />
                </q-tab-panel>
                <q-tab-panel name="permissions">
                  <div class="text-h6">Permissions</div>
                  <r-table v-if="permissions" :columns="permissionsTable.columns" :model-value="permissions" no-export />
                </q-tab-panel>
              </q-tab-panels>
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
import { Handler } from 'src/services/handler'
import { Lang } from 'src/services/lang'
import { Meta } from './meta'
import { authStore } from 'src/stores/auth'

const props = defineProps<{ props?: { id?: string | number } }>()
const emit = defineEmits(['refreshEvent'])

const Auth = authStore()
const companies = Auth.getCompanies(true)
const API = new Api()
const loading = ref(false)
const permissions = ref([])
const dataModel = ref(null)
const disableSubmit = ref(true)
const tableTab = ref('roles')
const step = ref(1)
const msg = ref({
  success: null,
  failed: []
})

const table = reactive({
  search: '',
  columns: Meta.tableExport(Helper, Constant, Lang)
})

const permissionsTable = reactive({
  search: '',
  columns: Meta.tablePermissions(Helper, Constant, Lang)
})

// METHODS
const onPermissionFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files ? target.files[0] : null

  if (file) {
    const map = mapFromColumns(permissionsTable.columns)

    readXlsxFile(file, { map, ignoreEmptyRows: false })
      .then((result: { rows: any }) => {
        permissions.value = result.rows.map((row: any) => ({
          ...row
        }))
      })
      .catch((error: any) => {
        console.error('Error reading Excel file:', error)
        disableSubmit.value = true
      })
  }
}

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files ? target.files[0] : null

  if (file) {
    disableSubmit.value = false
    const map = mapFromColumns(table.columns)

    readXlsxFile(file, { map, ignoreEmptyRows: false })
      .then((result: { rows: any }) => {
        dataModel.value = result.rows.map((row: any) => ({
          ...row
        }))
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
    permissions: permissions.value,
    roles: dataModel.value
  }

  disableSubmit.value = true
  loading.value = true

  const ep = `${Meta.module}/bulk`
  API.post(ep, payload, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      table.columns.unshift({
        align: 'left',
        formatter: null,
        name: 'action',
        field: 'id',
        label: '#',
        style: 'width: 20px'
      })
      msg.value.success = data.success
      msg.value.failed = data.failed || []
    } else {
      disableSubmit.value = false
    }
  })
}

const downloadTemplate = () => {
  Handler.exportXLS(Meta)
}

const back = () => {
  emit('refreshEvent')
}
</script>
