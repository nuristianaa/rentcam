<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else @submit="submit" :meta="Meta" :modal="props" @back="back">
      <div class="row">
        <div class="q-pa-sm" style="width: 100%">
          <q-table
            flat
            dense
            style="width: 100%"
            class="sticky-table"
            :binary-state-sort="false"
            :rows="table.data"
            :columns="table.columns"
            :filter="table.filter"
            row-key="id"
            selection="multiple"
            v-model:selected="table.selected"
            @selection="onRowSelection"
            :rows-per-page-options="[0]"
            :style="'width: 100%; height: ' + Constant.tableHeight(40) + 'px;'"
          >
            <template v-slot:top>
              <div class="clickable subtitle q-py-sm">
                <q-icon name="info" />
                Info
                <q-menu>
                  <q-card flat class="q-pa-sm">
                    <div>B: Browse -> Get multiple data.</div>
                    <div>R: Read -> Get one data with detail information.</div>
                    <div>C: Create -> Creating data.</div>
                    <div>U: Update -> Updating data.</div>
                    <div>D: Delete -> Deleting data.</div>
                    <div>Re: Restore -> Restoring data from trash.</div>
                  </q-card>
                </q-menu>
              </div>
              <div class="col-12">
                <f-input v-model="dataModel.name" :label="Lang.module(Meta, 'name')" required />
              </div>
            </template>
            <template v-slot:header-cell-app="prp">
              <th colspan="2">
                <q-th :props="prp">App & Name</q-th>
                <q-input class="form-sm" v-model="table.filter" outlined dense>
                  <template #append>
                    <q-icon size="xs" name="search" />
                  </template>
                </q-input>
              </th>
            </template>
            <template v-slot:header-cell-name></template>
            <template v-for="v in Object.keys(features)" :key="v" v-slot:[`header-cell-${v}`]="prp">
              <th class="justify-center text-center">
                <q-th :props="prp" class="row justify-center">{{ prp.col.label }}</q-th>
                <q-checkbox dense :model-value="features[v]" @update:model-value="(val) => onFeatureToggle(v, val)" />
              </th>
            </template>
            <template v-for="v in Object.keys(features)" :key="v" v-slot:[`body-cell-${v}`]="props">
              <q-td class="text-center">
                <q-checkbox dense v-model="props.row[v]" @update:model-value="(val) => onRowPermissionToggle(props.row, v, val)" />
              </q-td>
            </template>
            <template v-slot:body-cell-others="props">
              <q-td class="text-center">
                <div clickable class="clickable">
                  {{ props.row.others && props.row.others.length > 0 ? props.row.others.join(', ') : 'NA' }}
                  <q-menu class="q-pa-sm">
                    <q-select label="Permissions" hint="Press enter to add more value." v-model="props.row.others" autofocus use-input use-chips multiple hide-dropdown-icon input-debounce="0" new-value-mode="add-unique" style="min-width: 250px" />
                  </q-menu>
                </div>
              </q-td>
            </template>
          </q-table>
        </div>
      </div>
    </h-form>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Meta } from './meta'
import type { DataModel } from './meta'
import { Constant } from 'src/services/constant'
import { Lang } from 'src/services/lang'

/* -------------------------
  Props / Emits
------------------------- */
const props = defineProps<{ props?: { id?: string | number } }>()
const emit = defineEmits(['refreshEvent'])

/* -------------------------
  Services / State
------------------------- */
const router = useRouter()
const API = new Api()

const loading = ref(true)
const dataModel = ref<DataModel>(Meta.model)

const table = reactive<any>({
  columns: [
    // { name: 'id', required: true, label: 'id', field: 'id', align: 'center', sortable: true },
    { name: 'app', label: 'App', field: 'app', sortable: true },
    { align: 'left', name: 'name', label: 'Name', field: 'name', sortable: true },
    { align: 'center', name: 'browse', label: 'B', field: 'browse', sortable: false },
    { align: 'center', name: 'read', label: 'R', field: 'read', sortable: false },
    { align: 'center', name: 'create', label: 'C', field: 'create', sortable: false },
    { align: 'center', name: 'update', label: 'U', field: 'update', sortable: false },
    { align: 'center', name: 'delete', label: 'D', field: 'delete', sortable: false },
    { align: 'center', name: 'restore', label: 'Re', field: 'restore', sortable: false },
    { align: 'center', name: 'others', label: 'Others', field: 'others', sortable: false }
  ],
  data: <any>[],
  selected: [],
  search: {
    app: '',
    name: ''
  },
  filter: ''
})
const features = ref<any>({
  browse: false,
  read: false,
  create: false,
  update: false,
  delete: false,
  restore: false
})

// METHODS
const init = () => {
  dataModel.value = Helper.unreactive(Meta.model)
  const action = props.props?.id ? 'update' : 'create'
  Handler.permissions(router, action, Meta, (status: boolean, data: any) => {
    Meta.permission = data
    if (status) {
      if (props.props?.id) getData(props.props?.id)
      else onRefresh()
    }
  })
}

const onRefresh = () => {
  getPermissionsData()
  loading.value = false
}

const getData = (id: string | number) => {
  loading.value = true
  const endpoint = `${Meta.module}/${id}`
  void API.get(endpoint, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      dataModel.value = data
      getPermissionsData()
    }
  })
}

const submit = async () => {
  if (validateSubmit()) {
    loading.value = true

    let status = 600
    if (dataModel.value.id) status = await update()
    else status = await save()

    if (status === 200) {
      Helper.showSuccess('Data has been successfully saved.')
      back()
    }
    loading.value = false
  }
}

const validateSubmit = () => {
  // Transform
  transformData()

  const msg = ''
  // Validations

  if (msg === '') return true
  else {
    Helper.showNotif(msg)
    return false
  }
}

const save = async () => {
  let statusapi = 600
  await API.post(Meta.module, dataModel.value, (status: number, _data: any) => {
    statusapi = status
  })
  return statusapi
}

const update = async () => {
  let statusapi = 600
  await API.put(`${Meta.module}/${dataModel.value.id}`, dataModel.value, (status: number, _data: any) => {
    statusapi = status
  })
  return statusapi
}

const back = () => {
  emit('refreshEvent')
}

const getPermissionsData = () => {
  loading.value = true
  const endpoint = 'auth/permissions?limit=0'
  void API.get(endpoint, (status: number, data: { items: any }) => {
    loading.value = false
    if (status === 200) {
      let existing = dataModel.value.permissions ?? []
      if (existing.length > 0) {
        existing = existing.map((d: any) => {
          return {
            id: d.id,
            app: d.app,
            name: d.name,
            browse: d.detail?.browse ?? false,
            read: d.detail?.read ?? false,
            create: d.detail?.create ?? false,
            update: d.detail?.update ?? false,
            delete: d.detail?.delete ?? false,
            restore: d.detail?.restore ?? false,
            others: d.detail?.others ?? []
          }
        })
      }
      // FOREACH PERMISSIONS DB
      const target: any[] = []
      const items = data?.items ?? data
      for (let i = 0; i < items.length; i++) {
        const val = items[i]
        const perm = {
          ...val,
          browse: false,
          read: false,
          create: false,
          update: false,
          delete: false,
          restore: false,
          others: []
        }
        if (existing.length > 0) {
          const permission = existing.find((p: any) => p.id == val.id)
          if (permission) target.push(permission)
          else target.push(perm)
        } else target.push(perm)
      }
      // REPLACE VALUE
      table.data = target.map((item) => ({ ...item }))
      syncFeaturesFromData()
    }
  })
}

const transformData = () => {
  dataModel.value.permissions = []
  for (const e of table.data) {
    const row = {
      id: e.id,
      app: e.app,
      name: e.name,
      detail: {
        browse: !!e.browse,
        read: !!e.read,
        create: !!e.create,
        update: !!e.update,
        delete: !!e.delete,
        restore: !!e.restore,
        others: e.others
      }
    }
    dataModel.value.permissions.push(row)
  }
}

const onRowSelection = ({ rows, added }: { rows: readonly any[]; keys: readonly any[]; added: boolean; evt: Event }) => {
  if (!rows || rows.length === 0) return

  for (const r of rows) {
    const id = r.id
    const keys = Object.keys(features.value)
    for (const k of keys) {
      const idx = table.data.findIndex((d: any) => d.id == id)
      if (idx !== -1) table.data[idx][k] = added
    }
  }
  syncFeaturesFromData()
}

// When user clicks header checkbox for a column
const onFeatureToggle = (action: string, value: boolean) => {
  table.data = table.data.map((val: any) => ({ ...val, [action]: value }))
  features.value[action] = value
}

// When user toggles an individual row permission checkbox
const onRowPermissionToggle = (row: any, action: string, value: boolean) => {
  const idx = table.data.findIndex((d: any) => d.id == row.id)
  if (idx !== -1) table.data[idx][action] = value
  syncFeaturesFromData()
}

const syncFeaturesFromData = () => {
  const keys = Object.keys(features)
  for (const k of keys) {
    if (table.data.length === 0) {
      features.value[k] = false
      continue
    }
    // feature true only if all rows have it true
    const allTrue = table.data.every((r: any) => !!r[k])
    features.value[k] = allTrue
  }
}

// MOUNTED | COMPUTED | WATHERS
onMounted(() => {
  init()
})
</script>
