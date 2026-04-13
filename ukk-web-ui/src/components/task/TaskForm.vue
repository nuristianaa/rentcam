<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else @submit="submit" :meta="Meta" :modal="props" @back="back">
      <div class="row q-pa-sm">
        <f-card title="General" class="col-12">
          <div class="row">
            <f-input v-model="dataModel.title" col="12" :label="Lang.module(Meta, 'title')" required />
            <f-textarea v-model="dataModel.description" col="12" :label="Lang.module(Meta, 'description')" />
            <f-select v-model="dataModel.user_id" col="12" :label="Lang.module(Meta, 'task_assignees')" required api="auth/users" app="identity" optionValue="username" :optionLabel="v => v.username + ' - ' + v.name" multiple/>
            <q-separator />
            <f-select
              isButton
              toggleColor="accent"
              col="4"
              :label="Lang.module(Meta, 'activity_type')"
              v-model="dataModel.activity_type"
              :options="['CALL', 'VISIT', 'EMAIL', 'CANVASSING', 'OTHER']"
              required
            />
            <f-select
              isButton
              toggleColor="accent"
              col="4"
              :label="Lang.module(Meta, 'status')"
              v-model="dataModel.status"
              :options="['TODO', 'PROGRESS', 'DONE']"
              required
            />
            <f-select
              isButton
              toggleColor="accent"
              col="4"
              :label="Lang.module(Meta, 'priority')"
              v-model="dataModel.priority"
              :options="['LOW', 'MEDIUM', 'HIGH']"
              required
            />
            <f-date col="4" v-model="dataModel.start_date" :label="Lang.module(Meta, 'start_date')" />
            <f-date col="4" v-model="dataModel.due_date" :label="Lang.module(Meta, 'due_date')" />
            <f-input-tag
              v-model="inputTag"
              col="12"
              label="Tags"
            />
          </div>
        </f-card>

        <f-card class="col-12 q-mt-lg" v-if="props.props?.id">
          <q-expansion-item
            dense
            expand-separator
            label="Comments"
            header-class="text-h5"
            default-opened
          >
          <!-- input comment -->
          <f-textarea
            rich
            v-if="props.props?.id"
            v-model="dataModelNotes.content"
            col="12"
            @focus="isCommentFocused = true"
            @blur="onCommentBlur"
          />

          <div class="row col-12 justify-end q-mt-sm" v-if="isCommentFocused || !isCommentEmpty(dataModelNotes?.content)">
            <q-btn
              v-if="props.props?.id"
              
              label="Send"
              color="primary"
              icon="send"
              class="text-bold"
              type="button"
              @click="submitComment"
            />
          </div>

          <q-separator class="q-my-md" />

          <!-- list comments -->
          <div v-if="filteredNotes?.length" class="col-12 q-ml-lg">
            <div
              v-for="(note, index) in filteredNotes"
              :key="index"
              class="row q-mb-md"
            >
              <div
                class="q-pa-md bg-grey-2 text-dark"
                style="border-radius: 12px; width: 100%; max-width: 600px;"
              >
                <div class="row items-center justify-between">
                  <div class="text-h6">
                    {{ note?.created_by }} |
                    {{ Helper.toDate(note?.created_at,'YYYY-MM-DD HH:mm') }}
                  </div>

                  <!-- ⋮ MENU (only owner) -->
                  <q-btn
                    v-if="isNoteOwner(note)"
                    dense
                    flat
                    round
                    icon="more_vert"
                  >
                    <q-menu anchor="bottom right" self="top right">
                      <q-list dense style="min-width: 120px">
                        <q-item clickable v-close-popup @click="onEditNote(note)">
                          <q-item-section avatar>
                            <q-icon name="edit" />
                          </q-item-section>
                          <q-item-section>Edit</q-item-section>
                        </q-item>

                        <q-item clickable v-close-popup @click="onDeleteNote(note)">
                          <q-item-section avatar>
                            <q-icon name="delete" color="red" />
                          </q-item-section>
                          <q-item-section class="text-red">
                            Delete
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-menu>
                  </q-btn>
                </div>
                <div class="text-body1 q-mt-sm">
                  {{ note?.content }}
                </div>
              </div>
            </div>
          </div>
          </q-expansion-item>
        </f-card>
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

const isNoteOwner = (note: any) => {
  return user?.username === note.created_by
}

const onEditNote = (note: any) => {
  dataModelNotes.value = {
    ...note
  }
}

const onCommentBlur = () => {
  if (isCommentEmpty(dataModelNotes.value.content)) {
    isCommentFocused.value = false
  }
}

const getData = (id: string | number) => {
  loading.value = true
  const endpoint = `${Meta.module}/${id}`
  API.get(endpoint, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      dataModel.value = data
      getDataNotes(id, Meta.module, null)
    }
  })
}

const getDataNotes = (
  ref_id: string, 
  ref_module?: string,
  type?: string[]
) => {
  loadingNotes.value = true
  let endpoint = `${Meta.module_comment}?get_by_module=true&limit=0`
  if (ref_id) endpoint += `&ref_id=${ref_id}`
  if (ref_module) endpoint += `&ref_module=${ref_module}`
  if (type && type.length) endpoint += `&type=${type}`
  API.get(endpoint, (status: number, data: any) => {
    loadingNotes.value = false
    if (status === 200) {
      dataModel.value.notes = data
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
  if (
    !dataModel.value.user_id ||
    (Array.isArray(dataModel.value.user_id) && dataModel.value.user_id.length === 0)
  ) {

    if (user?.username) {
      dataModel.value.user_id = [user.username]
    }
  }

  dataModel.value.ref_module = props.module_meta.module
  dataModel.value.ref_id = props.module_data.id
  dataModel.value.app = props.module_meta.app

}

const appendTag = () => {
  const tag = inputTag.value?.trim()
  if (!tag) return

  // pastikan array
  if (!Array.isArray(dataModel.value.tags)) {
    dataModel.value.tags = []
  }

  // cegah duplikat
  if (!dataModel.value.tags.includes(tag)) {
    dataModel.value.tags = [...dataModel.value.tags, tag]
  }

  inputTag.value = ''
}

  const submitComment = async () => {
    if (validateSubmitComment()) {
      loadingNotes.value = true

      let status = 600
      
      status = await saveComment()

      if (status === 200) {
        Helper.showSuccess('Comment has been successfully saved.')
        dataModelNotes.value.content = null
        isCommentFocused.value = false
      }
      loadingNotes.value = false
    }
  }

  const validateSubmitComment = () => {
    let msg = ''
    // Validations
    if (!dataModelNotes.value.content) {
      msg = 'Comment tidak boleh kosong'
    }
    if (msg === '') return true
    else {
      Helper.showNotif(msg)
      return false
    }
  }

  const saveComment = async () => {
    if (!dataModelNotes.value.content) return
    let statusapi = 600
    loadingNotes.value = true
    const payload = {
      type: dataModelNotes.value.type,
      content: dataModelNotes.value.content,
      ref_id: props.props.id ?? null,
      ref_module: Meta.module,
      title: null,
      app: Meta.app
    }
    if (dataModelNotes.value.id) {
      await API.put(
        `${Meta.module_comment}/${dataModelNotes.value.id}`,
        payload,
        (status: number, _data: any) => {
          loadingNotes.value = false
          getDataNotes(props.props.id, Meta.module, null)
          statusapi = status
        }
      )
      return statusapi
    }
    await API.post(Meta.module_comment, payload, (status: number, _data: any) => {
      loadingNotes.value = false
      getDataNotes(props.props.id, Meta.module, null)
      statusapi = status
    })
    return statusapi
  }

  const onDeleteNote = (note: any) => {
    const msg = 'Are you sure you want to delete this comment?'

    Helper.confirm(msg, async (result: boolean) => {
      if (!result) return

      let statusapi = 600
      await API.delete(
        `${Meta.module_comment}/delete`,
        { id: [note.id] },
        (status: number) => {
          statusapi = status
        }
      )

      if (statusapi === 200) {
        Helper.showSuccess('Comment deleted')
        getDataNotes(id, Meta.module, null)
      }
    })
  }

// MOUNTED | COMPUTED | WATHERS
onMounted(() => {
  init()
})
</script>
