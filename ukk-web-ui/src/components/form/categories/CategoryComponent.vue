<template>
  <q-btn @click="openMenu" :label="label ?? 'Categories'" no-caps  color="primary" />
  <template>
    <s-dialog v-model="dialog" width="50vw">
      <s-loading v-if="loading" />
      <h-form v-else :meta="Meta" :modal="dataModel" @back="back" @submit="submit">
        <q-table bordered :columns="Meta.columns" dense :filter="search" flat row-key="id" :rows="dataModel" :rows-per-page-options="[0]" separator="cell" wrap-cells>
          <template v-slot:top>
            <slot name="top">
              <div class="row q-my-sm">
                <div class="row q-gutter-sm">
                  <q-input v-model="search" class="form-sm" debounce="300" dense outlined placeholder="Search">
                    <template v-slot:append>
                      <q-icon name="search" />
                    </template>
                  </q-input>
                  <q-btn class="q-px-sm" color="primary" dense icon="add" label="add"  @click="onAdd()" />
                </div>
                <q-space />
              </div>
            </slot>
          </template>

          <template v-slot:body="prp">
            <q-tr :props="prp">
              <q-td key="action" class="no-padding" :props="prp">
                <div class="row q-mx-xs">
                  <q-btn tabindex="-1" color="negative" dense flat icon="delete" round size="xs" @click="onDelete(prp.row, prp.rowIndex)" />
                </div>
              </q-td>
              <q-td key="code" class="no-padding" :props="prp">
                <f-input-table v-model="prp.row.code" class="q-mx-xs" />
              </q-td>
              <q-td key="val_str" class="no-padding" :props="prp">
                <f-input-table v-model="prp.row.val_str" class="q-mx-xs" />
              </q-td>
            </q-tr>
          </template>
        </q-table>
      </h-form>
    </s-dialog>
  </template>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref } from 'vue'
import type { Dialog } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Meta } from './meta'
import type { DataModel } from './meta'

const props = defineProps<{
  app: string
  group: string
  label?: string
}>()
// const emit = defineEmits(['refreshEvent'])

const dialog = ref<Dialog>({
  show: false,
  type: 'form',
  title: `Add or Update Categories ${props.label ?? ''}`,
  props: null,
  maximize: false,
  persistent: false,
  width: '70vw'
})

const API = new Api()
const loading = ref(true)
const dataModel = ref<DataModel[]>([])
const search = ref('')

// METHODS
const init = () => {
  getData()
}

const getData = () => {
  loading.value = true
  let ep = Meta.module
  ep += '?limit=0'
  ep += `&where=group:${props.group}`
  API.get(
    ep,
    (status: number, data: any) => {
      loading.value = false
      if (status === 200) {
        dataModel.value = data
      }
    },
    props.app
  )
}

const submit = async () => {
  if (validateSubmit()) {
    loading.value = true

    let status = 200
    const datas = []
    for (let i = 0; i < dataModel.value.length; i++) {
      const model = dataModel.value[i]
      if (model) {
        const res = await update(model)
        if (status < 400) status = res.status // handle when there is failed, save failed
        datas.push(res.data)
      }
    }

    if (status === 200) {
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
    if (!e?.code) msg += 'Please input code first. '
  }

  if (msg === '') return true
  else {
    Helper.showNotif(msg)
    return false
  }
}

const update = async (model: DataModel) => {
  let statusapi = 600
  let dataapi = {}
  const ep = Meta.module + `/${model.id}`
  await API.put(
    ep,
    model,
    (status: number, data: any) => {
      if (status === 200) {
        dataapi = data
        statusapi = status
      }
    },
    props.app
  )
  return { status: statusapi, data: dataapi }
}

const back = () => {
  dialog.value.show = false
}

const onAdd = () => {
  loading.value = true
  const ep = Meta.module
  const model = {
    group: props.group
    // code: null
  }
  API.post(
    ep,
    model,
    (status: number, data: any) => {
      loading.value = false
      if (status === 200) {
        dataModel.value.push(data)
      }
    },
    props.app
  )
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

const openMenu = () => {
  dialog.value.show = true
  init()
}

// MOUNTED | COMPUTED | WATCHERS
// onMounted(() => { })
</script>
