<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else :meta="Meta" :modal="props.data" @back="back" @submit="submit">
      <slot name="top">
        <div class="row q-mb-md">
          <!-- TOP LEFT | TITLE -->
          <div class="row q-gutter-sm">
            <q-input v-model="search" class="form-sm" debounce="300" dense outlined placeholder="Search">
              <template v-slot:append>
                <q-icon name="search" />
              </template>
            </q-input>
            <q-btn class="q-px-md" color="primary" dense icon="add" label="add"  @click="onAdd()" />
          </div>
          <q-space />
        </div>
      </slot>
      <q-table :columns="Meta.columns" dense :filter="search" flat row-key="id_" :rows="dataModel" table-class="table-no-padding table-bordered q-pb-md" :rows-per-page-options="[0]" separator="none" hide-bottom>
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td key="action" :props="props">
              <q-btn round dense flat size="xs" icon="delete" color="negative" @click="onDelete(props.row, props.rowIndex)" />
              <q-btn round dense flat size="xs" icon="visibility" :color="props.row.path ? 'info' : 'grey'" :disable="props.row.path ? false : true" @click="preview(props.row)">
                <q-tooltip>View File</q-tooltip>
              </q-btn>
            </q-td>
            <q-td key="file" :props="props">
              <f-file-table v-model="props.row.file" class="q-mx-xs" />
            </q-td>
            <q-td key="name" :props="props">
              <f-input-table v-model="props.row.name" class="q-mx-xs" />
            </q-td>
            <q-td key="description" :props="props">
              <f-input-table v-model="props.row.description" class="q-mx-xs" />
            </q-td>
            <q-td key="filename" :props="props">
              {{ props.row.filename }}
            </q-td>
          </q-tr>
        </template>
      </q-table>
    </h-form>
    <s-dialog v-model="dialog">
      <q-linear-progress style="height: 60px" v-if="get_pdf_loading"></q-linear-progress>
      <q-card flat square v-else style="display: flex; flex-direction: column; height: 100%">
        <q-card-section style="display: flex; justify-content: center; flex-grow: 1; max-height: 48rem">
          <iframe v-if="iframes.content" :src="iframes.content" ref="iframe-content" frameborder="0" :class="$q.dark.isActive ? 'iframe-dark' : ''" style="height: 100%; width: 100%"></iframe>
        </q-card-section>
        <div style="position: absolute; right: 2rem; bottom: 2rem">
          <q-btn size="md" fab icon="download" color="primary" @click="download()" />
        </div>
      </q-card>
    </s-dialog>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, onMounted } from 'vue'
import { Helper } from 'src/services/helper'
import { Meta } from './meta'
import type { DataModel } from './meta'
import { Dialog } from 'quasar'
import { authStore } from 'src/stores/auth'

const props = defineProps<{
  meta: {
    app: string
    module: string
    ref_module?: string
  }
  data: {
    id: string | number
    code?: string
    name?: string
  }
  perReferenceId?: boolean
  stay_after_save?: boolean
}>()
const emit = defineEmits(['refreshEvent', 'callbackApi'])

const API = new Api()
const loading = ref(true)
const dataModel = ref<DataModel[]>([])
const search = ref('')
const get_pdf_loading = ref(false)
const iframes = ref({
  content: <string | null>null
})
const dialog = ref({
  show: false,
  width: '98vw',
  show_header: true
})

// METHODS
const init = () => {
  getData()
}

const getData = () => {
  loading.value = true
  let ep = Meta.module
  ep += `?app=${props.meta.app}`
  // ep += '&per_reference_id=true'
  ep += '&get_previous_list=true'
  ep += `&module=${props.meta.module}`
  ep += `&reference_id=${props.data.id}`
  ep += `&reference_code=${props.data.code}`
  if (props.perReferenceId) ep += `&per_reference_id=true`
  API.get(ep, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      if (data.items && data.items.length > 0) dataModel.value = data.items
      else if (data.history && data.history.length > 0) dataModel.value = data.history
    }
  })
}

const submit = async () => {
  if (validateSubmit()) {
    loading.value = true

    let status = 200
    const datas = []
    for (let i = 0; i < dataModel.value.length; i++) {
      const model = dataModel.value[i]
      if (model) {
        const res = await save(model)
        if (status < 400) status = res.status // handle when there is failed, save failed
        datas.push(res.data)
      }
    }

    if (status === 200) {
      emit('callbackApi', datas)
      Helper.showSuccess('Data has been successfully saved.')
      if (!props.stay_after_save) back()
      getData()
    }
    loading.value = false
  }
}

const validateSubmit = () => {
  let msg = ''
  // Validations
  for (let i = 0; i < dataModel.value.length; i++) {
    const e = dataModel.value[i]
    if (!e?.name) msg += `Please input name in row ${i + 1}.<br> `
  }

  if (msg === '') return true
  else {
    Helper.showAlert('Stop!', msg)
    return false
  }
}

const save = async (model: DataModel) => {
  let statusapi = 600
  const req = new FormData()
  if (model.id) req.append('id', String(model.id))
  req.append('app', String(model.app))
  req.append('name', String(model.name))
  req.append('description', String(model.description))
  if (model.file) req.append('file', model.file)
  req.append('module', String(model.module))
  req.append('reference_id', String(model.reference_id))
  req.append('reference_code', String(model.reference_code))

  let dataapi = null
  let msg = 'upload failed'
  let ep = Meta.module
  if (model.id) ep += `/${model.id}`
  await API.post(
    ep,
    model,
    (status: number, data: any) => {
      if (status === 200) {
        dataapi = data
        statusapi = status
        msg = 'upload success'
      }
    },
    'main',
    true
  )
  return { status: statusapi, data: dataapi }
}

const back = () => {
  emit('refreshEvent')
}


const onAdd = () => {
  const row: DataModel = {
    id_: new Date().getTime(),
    id: null,
    app: props.meta.app,
    name: null,
    description: null,
    // filename: null,
    // filetype: null,
    // path: null,
    module: props.meta.module,
    reference_id: String(props.data.id),
    reference_code: props.data.code ?? props.data.name ?? '',
    is_public: false,
    file: null,
  }
  dataModel.value.push(row)
}

const onDelete = (row: DataModel, i: number) => {
  if (row.id) {
    Helper.confirm('Are you sure?', (result: boolean) => {
      if (result) {
        const ep = Meta.module + '/delete?id=' + row.id
        API.delete(ep, {}, (status: number) => {
          if (status === 200) {
            Helper.showSuccess('Data deleted!')
            dataModel.value.splice(i, 1)
          }
        })
      }
    })
  } else {
    dataModel.value.splice(i, 1)
  }
}

const preview = async (data: DataModel) => {
  if (!data.path) {
    Helper.showAlert('File is not uploaded yet.')
    return
  }
  dialog.value.show = true
  get_pdf_loading.value = true
  iframes.value.content = await Helper.blobFile(data.path, data.is_public, data.storage_id)
  get_pdf_loading.value = false
}

const download = () => {
  if (!iframes.value.content) return
  window.open(iframes.value.content, '_blank')
}

// MOUNTED | COMPUTED | WATCHERS
onMounted(() => {
  init()
})
</script>

<style lang="scss" scoped>
.q-table__bottom {
  border: none !important;
  border-top: none !important;
}
</style>
