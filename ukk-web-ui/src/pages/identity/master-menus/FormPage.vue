<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else @submit="submit" :meta="Meta" :modal="props" @back="back">
      <div class="row q-pa-sm">
        <div class="col-12 q-px-sm">
          <f-input v-model="dataModel.name" label="Name" required />
        </div>
        <f-card row col="12" title="Menus">
          <div class="col-12 col-md-8">
            <div class="row">
              <f-select col="8" multiple label="Select Menu" v-model="addMenus" api="auth/menu-items" :option-label="(opt: any) => `${opt.app} - ${opt.name}`" />
              <div class="col-4">
                <div class="row no-wrap q-gutter-sm">
                  <q-btn class="text-capitalize bold" no-wrap color="info" label="Add" icon="add" @click="onAdd" />
                  <q-btn class="text-capitalize bold" no-wrap color="green" label="Add All" icon="add" @click="onAddAll" />
                </div>
              </div>
            </div>
          </div>
        </f-card>
        <f-card row col="12" title="Sorting Menus">
          <div class="col-12 q-pa-xm">
            <div class="alert alert-info">
              <p class="q-mb-auto">Drag and drop column for change the layout.</p>
              <p class="q-mb-auto">Only three levels are covered.</p>
            </div>
          </div>
          <q-tabs v-model="tab" dense indicator-color="blue" active-class="text-bold text-blue" align="justify">
            <q-tab name="identity" label="Identity" />
            <q-tab name="crm" label="CRM" />
            <q-tab name="engineering" label="Engineering" />
            <q-tab name="finance" label="Finance" />
            <q-tab name="hris" label="HRIS" />
            <q-tab name="procurement" label="Procurement" />
            <q-tab name="project_management" label="Project-Management" />
          </q-tabs>

          <div class="row col-12">
            <q-tab-panels v-model="tab" animated>
              <q-tab-panel v-for="(v, idx) in items" :key="idx" :name="v.name">
                <div class="row" v-if="!loading_nested">
                  <nested-draggable v-model="v.menu_items" withDelete @delete="onDeleteItem(v.name, $event)" @update:modelValue="onUpdateMenuItems(v.name, $event)"></nested-draggable>
                </div>
              </q-tab-panel>
            </q-tab-panels>
          </div>
        </f-card>
      </div>
    </h-form>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Meta } from './meta'
import type { DataModel } from './meta'

const props = defineProps<{ props?: { id?: string | number } }>()
const emit = defineEmits(['refreshEvent'])

const router = useRouter()
const API = new Api()

const loading = ref(true)
const loading_nested = ref(false)
const dataModel = ref<DataModel>(Meta.model)
const addMenus = ref<any>([])
const items = ref<any>([{ name: 'user', menu_items: [] }])
const tab = ref('identity')

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
  loading.value = false
}

const getData = (id: string | number) => {
  loading.value = true
  const endpoint = `${Meta.module}/${id}`
  API.get(endpoint, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      dataModel.value = data
      items.value = groupingByApp(data.menu_items)
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
  dataModel.value.menu_items = transformFromGroup()

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

const onAdd = async () => {
  if (addMenus.value.length > 0) {
    loading_nested.value = true
    for (let i = 0; i < addMenus.value.length; i++) {
      const id = addMenus.value[i]
      await API.get(`auth/menu-items/${id}`, (status: number, data: any) => {
        if (status == 200) {
          const e = data
          dataModel.value.menu_items?.push({
            id: e.id,
            app: e.app,
            name: e.name,
            slug: e.slug,
            path: e.path,
            icon: e.icon,
            children: []
          })
        }
      })
    }
    items.value = groupingByApp(dataModel.value.menu_items)
    setTimeout(() => {
      loading_nested.value = false
    }, 300)
    addMenus.value = []
  }
}

const onAddAll = () => {
  loading_nested.value = true
  API.get('auth/menu-items?limit=0&order=id:asc', (status: number, data: any[]) => {
    loading_nested.value = false
    if (status === 200) {
      data.forEach((e) => {
        dataModel.value.menu_items?.push({
          id: e.id,
          app: e.app,
          name: e.name,
          slug: e.slug,
          path: e.path,
          icon: e.icon,
          children: []
        })
      })
      items.value = groupingByApp(dataModel.value.menu_items)
    }
  })
}

const onDeleteItem = (tabName: string, { parentIndex, childIndex }) => {
  const group = items.value.find((group) => group.name === tabName)
  if (!group) return

  const item = group.menu_items[parentIndex]
  if (!item) return

  if (childIndex !== undefined) {
    item.children?.splice(childIndex, 1)
  } else {
    group.menu_items.splice(parentIndex, 1)
  }

  // update ke dataModel
  dataModel.value.menu_items = items.value.flatMap((group) => group.menu_items)
}

const onUpdateMenuItems = (tabName: string, updatedList: any[]) => {
  const group = items.value.find((group) => group.name === tabName)
  if (group) group.menu_items = updatedList

  const newList: any[] = []
  for (const group of items.value) {
    newList.push(...group.menu_items)
  }
  dataModel.value.menu_items = newList
}

const groupingByApp = (menus: any) => {
  const identity = []
  const crm = []
  const engineering = []
  const finance = []
  const hris = []
  const procurement = []
  const project_management = []
  for (let i = 0; i < menus.length; i++) {
    const e = menus[i]
    if (e.app == 'identity') identity.push(e)
    if (e.app == 'crm') crm.push(e)
    if (e.app == 'engineering') engineering.push(e)
    if (e.app == 'finance') finance.push(e)
    if (e.app == 'hris') hris.push(e)
    if (e.app == 'procurement') procurement.push(e)
    if (e.app == 'project_management') project_management.push(e)
  }
  return [
    { name: 'identity', menu_items: identity },
    { name: 'crm', menu_items: crm },
    { name: 'engineering', menu_items: engineering },
    { name: 'finance', menu_items: finance },
    { name: 'hris', menu_items: hris },
    { name: 'procurement', menu_items: procurement },
    { name: 'project_management', menu_items: project_management },
  ]
}

const transformFromGroup = () => {
  const data = []
  for (let i = 0; i < items.value.length; i++) {
    const e = items.value[i]
    for (let ii = 0; ii < e.menu_items.length; ii++) {
      const el = e.menu_items[ii]
      data.push(el)
    }
  }
  return data
}

// MOUNTED | COMPUTED | WATHERS
onMounted(() => {
  init()
})
</script>
