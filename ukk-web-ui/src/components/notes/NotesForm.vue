<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else @submit="submit" :meta="Meta" :modal="props" @back="back">
      <div class="row q-pa-sm">
        <f-input v-model="dataModel.title" col="8" :label="Lang.module(Meta, 'title')" required/>
        <f-auto-complete col="4" v-model="dataModel.type" :label="Lang.module(Meta, 'type')" :api="Meta.module" :app="Meta.app" column="type"/>
        <f-textarea v-model="dataModel.content" col="12" :label="Lang.module(Meta, 'content')" rich/>
      </div>
    </h-form>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Meta } from './meta'
import type { DataModel } from './meta'
import type { TaskNote } from './meta'
import { Lang } from 'src/services/lang'
import { authStore } from 'src/stores/auth'


const props = defineProps<{ 
  props?: { id?: string | number }
  module_data?: any // { id: string | number; code?: string }
  module_meta?: any // { app: string; module: string; title?: string }
}>()

const emit = defineEmits(['refreshEvent'])

const router = useRouter()
const API = new Api()
const auth = authStore()
const user = auth.getUser()

const loading = ref(true)
const loadingNotes = ref(false)
const dataModel = ref<DataModel>(Meta.model)
const dataModelNotes = ref<TaskNote>(Meta.notes_model)
const inputTag = ref('')
const editingNote = ref<any | null>(null)
const isCommentFocused = ref(false)

// METHODS
const init = () => {
  dataModel.value = Helper.unreactive(Meta.model)
  const action = props.props?.id ? 'update' : 'create'
  Handler.permissions(router, action, Meta, (status: boolean, data: any) => {
    Meta.permission = data
    if (status) {
      if (props.props?.id) getData(props.props?.id)
      else{
        setDefaultValue()
        onRefresh()
      }
    }
  })
}

const getData = (id: string | number) => {
  loading.value = true
  const endpoint = `${Meta.module}/${id}`
  API.get(endpoint, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      dataModel.value = data
    }
  })
}

const filteredNotes = computed(() => {
  const notes = dataModel.value.notes || []
  const type = dataModelNotes.value.type

  if (!type || type === 'all') return notes
  return notes.filter(n => n.type === type)
})

const isCommentEmpty = (val?: string | null) => {
  if (!val) return true

  // buang tag html, spasi, & nbsp
  const text = val
    .replace(/<br\s*\/?>/gi, '')
    .replace(/<[^>]*>/g, '')
    .replace(/&nbsp;/gi, '')
    .trim()

  return text.length === 0
}

const onRefresh = () => {
  loading.value = false
  loadingNotes.value = false
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

const setDefaultValue = () => {
  dataModel.value.ref_module = props.module_meta.module
  dataModel.value.ref_id = props.module_data.id
  dataModel.value.app = props.module_meta.app
}

// MOUNTED | COMPUTED | WATHERS
onMounted(() => {
  init()
})
</script>
