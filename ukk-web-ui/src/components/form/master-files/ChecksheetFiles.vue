<template>
  <q-btn color="primary" outline icon="attachment" :label="dataModel.length ? `${dataModel.length} Files` : 'Attachments'" no-caps unelevated dense @click="show_dialog = true" :disable="props.disable"></q-btn>
  <q-dialog v-model="show_dialog" full-height>
    <q-card style="width: 900px; max-width: 85vw">
      <q-bar style="position: sticky; top: 0; width: 100%; z-index: 5; justify-content: space-between">
        <div>File</div>
        <q-btn v-close-popup flat icon="close" size="sm" />
      </q-bar>
      <q-card-section class="q-pa-md">
        <h-form :meta="{ hide_cancel: true }" :modal="true" @back="back" @submit="submit">
          <q-table bordered :columns="Meta.columns" dense flat row-key="id_" :rows="dataModel" :rows-per-page-options="[0]" separator="cell" wrap-cells>
            <template v-slot:top>
              <slot name="top">
                <div class="row q-my-sm">
                  <!-- TOP LEFT | TITLE -->
                  <div class="row q-gutter-sm">
                    <q-btn v-if="props.type === 'image'" class="q-px-sm" color="primary" dense icon="add" label="add"  @click="onAdd()" :disable="dataModel.length >= 1" />
                    <q-btn v-else class="q-px-sm" color="primary" dense icon="add" label="add"  @click="onAdd()" />
                  </div>
                  <q-space />
                </div>
              </slot>
            </template>

            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td key="action" class="no-padding" :props="props">
                  <div class="row q-mx-xs">
                    <q-btn color="negative" dense flat icon="delete" round size="xs" @click="onDelete(props.row, props.rowIndex)" />
                    <q-btn :color="props.row.path ? 'positive' : 'grey-9'" dense flat icon="visibility" round size="xs" @click="preview(props.row)" />
                  </div>
                </q-td>
                <q-td key="file" class="no-padding" :props="props">
                  <f-file-table :image-only="type === 'image'" v-model="props.row.file" class="q-mx-xs" />
                </q-td>
                <q-td key="name" class="no-padding" :props="props">
                  <f-input-table v-model="props.row.name" class="q-mx-xs" />
                </q-td>
                <q-td key="description" class="no-padding" :props="props">
                  <f-input-table v-model="props.row.description" class="q-mx-xs" />
                </q-td>
              </q-tr>
            </template>
          </q-table>
        </h-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, onMounted } from 'vue'
import { Helper } from 'src/services/helper'
import { Meta } from './meta'
import type { DataModel } from './meta'
import { Dialog } from 'quasar'
import { meta } from 'eslint-plugin-vue'

const props = withDefaults(
  defineProps<{
    app: string
    module: string
    disable?: boolean
    type: string
  }>(),
  {
    type: 'files'
  }
)
const emit = defineEmits(['refreshEvent', 'callbackApi'])

const API = new Api()
const loading = ref(true)
// Model is the id for reference
const model = defineModel<string | number>({ required: true })
const dataModel = ref<DataModel[]>([])
const show_dialog = ref(false)

// METHODS
const init = () => {
  getData()
}

const getData = () => {
  loading.value = true
  let ep = Meta.module
  ep += '?per_reference_id=true'
  ep += `&app=${props.app}`
  ep += `&module=${props.module}`
  ep += `&reference_id=${model.value}`
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
      back()
    }
    loading.value = false
  }
}

const validateSubmit = () => {
  let msg = ''
  // Validations
  for (let i = 0; i < dataModel.value.length; i++) {
    const e = dataModel.value[i]
    if (!e?.name) msg += 'Please input name first. '
  }

  if (msg === '') return true
  else {
    Helper.showNotif(msg)
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
    app: props.app,
    name: null,
    description: null,
    // filename: null,
    // filetype: null,
    // path: null,
    module: props.module,
    reference_id: String(model.value),
    reference_code: null,
    is_public: false,
    file: null
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

const preview = (data: DataModel) => {
  if (!data.path) {
    Helper.showAlert('File is not uploaded yet.')
    return
  }
  const blobUrl = Helper.viewBlobFile(data.path)
  Dialog.create({
    html: true,
    cancel: true,
    ok: 'Download',
    message: `
      <div style="display:flex; flex-direction:column; height:50vh; width:100%;">
        <iframe src="${blobUrl}" style="flex:1; border:none;"></iframe>
      </div>
    `
  })
    .onOk(() => {
      const filename = data.filename ?? 'docs'
      const link = document.createElement('a')
      link.href = blobUrl
      link.download = `${filename}.pdf`
      link.click()
    })
    .onCancel(() => {
      // console.log('Cancel')
    })
    .onDismiss(() => {
      // console.log('I am triggered on both OK and Cancel')
    })
}

// MOUNTED | COMPUTED | WATCHERS
onMounted(() => {
  init()
})
</script>
