<template>
  <div>
    <s-page :meta="Meta">
      <s-loading v-if="loading" />
      <s-table v-else :meta="Meta" :refresh="refresh"
        @add="add" @edit="edit" @detail="detail">
        <template #body-cell-image="props">
          <q-td :props="props" class="q-pa-none">
            <q-img
              v-if="getFirstImageUrl(props.row.images)"
              :src="getFirstImageUrl(props.row.images)"
              style="width: 70px; height: 70px"
              :ratio="1"
              fit="cover"
              spinner-color="primary"
            >
              <template #error>
                <div class="absolute-full flex flex-center bg-grey-3 text-grey-6 text-caption text-center q-pa-sm">
                  No image
                </div>
              </template>
            </q-img>
            <div v-else class="flex flex-center bg-grey-2" style="width: 70px; height: 70px">
              <q-icon name="image_not_supported" size="20px" color="grey-5" />
            </div>
          </q-td>
        </template>
      </s-table>
    </s-page>

    <s-dialog v-model="dialog">
      <FormModal v-if="dialog.type === 'form'"
        :props="dialog.props"
        :meta="Meta"
        @refreshEvent="onRefresh" />

      <DetailModal v-else
        :props="dialog.props"
        :meta="Meta"
        @refreshEvent="onRefresh" />
    </s-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Config } from 'src/services/config'
import { authStore } from 'src/stores/auth'
import type { Dialog } from 'src/services/handler'
import { Meta } from './meta'
import FormModal from './FormPage.vue'
import DetailModal from './DetailPage.vue'

const dialog = ref<Dialog>({
  show: false,
  type: 'form',
  title: 'Form',
  props: null,
})

const loading = ref(true)
const refresh = ref(0)
const router = useRouter()
const auth = authStore()

const encodeStaticPath = (path: string) => path.split('/').map(encodeURIComponent).join('/')

const resolveImageUrl = (path: string, storage?: string | null): string | null => {
  if (!path) return null

  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }

  if (storage) {
    try {
      const url = (Helper as any).viewBlobFile(path, false, storage)
      return typeof url === 'string' ? url : null
    } catch {
      return null
    }
  }

  const token = auth.getToken?.() ?? authStore().getToken()
  const baseUrl = Config.apiUrl('rental')
  return `${baseUrl}static_files/${encodeStaticPath(path)}${token ? `?token=${token}` : ''}`
}

const getFirstImageUrl = (raw: any): string | null => {
  if (!raw) return null
  if (typeof raw === 'string') return resolveImageUrl(raw)
  if (Array.isArray(raw)) {
    for (const item of raw) {
      const url = getFirstImageUrl(item)
      if (url) return url
    }
    return null
  }
  if (typeof raw === 'object') {
    if ('path' in raw) return resolveImageUrl(raw.path, raw.storage ?? null)
    if ('url' in raw) return raw.url
    return getFirstImageUrl(Object.values(raw))
  }
  return null
}

const init = () => {
  Handler.permissions(router, 'browse', Meta, (status, data) => {
    Meta.permission = data
    if (status) loading.value = false
  })
}

const onRefresh = () => {
  refresh.value++
  dialog.value.show = false
  dialog.value.props = null
}

const showDialog = (type: string, title: string, data: any = null) => {
  dialog.value.type = type
  dialog.value.title = `${title} | ${Meta.title}`
  dialog.value.show = true
  dialog.value.props = data
}

const add = () => showDialog('form', 'Add')
const edit = (data: any) => showDialog('form', 'Edit', data)
const detail = (data: any) => showDialog('detail', 'Detail', data)

onMounted(() => init())
</script>
