<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else @submit="submit" :meta="Meta" :model="dataModel" @back="back">
      <div class="row">
        <f-input col="6" v-model="dataModel.code" label="Kode Item" required />
        <f-input col="6" v-model="dataModel.name" label="Nama Item" required />
        <f-input col="6" v-model="dataModel.brand" label="Brand" />
        <f-select col="6" v-model="dataModel.category_id" label="Kategori" :options="categoryOptions" option-label="name" option-value="id" emit-value map-options />
        <f-textarea col="6" v-model="dataModel.description" label="Deskripsi" />
        <f-input col="6" v-model="dataModel.condition" label="Kondisi" />
        <f-input col="4" v-model="dataModel.stock_total" label="Stok Total" type="number" />
        <f-input col="4" v-model="dataModel.stock_available" label="Stok Tersedia" type="number" />
        <f-input col="4" />
        <f-input col="6" v-model="dataModel.price_per_day" label="Harga per Hari" type="number" />
        <f-input col="6" v-model="dataModel.deposit_amount" label="Deposit" type="number" />
        <f-toggle col="6" v-model="dataModel.is_active" label="Status Aktif" active-mode />
      </div>
      <div class="row q-mt-md">
        <div class="col-12 q-mb-sm">
          <!-- Image Preview Grid (saat edit/view existing item) -->
          <div v-if="imageList.length > 0" class="q-mb-lg">
            <div class="form-title q-mb-md">Pratinjau Foto Alat</div>
            <div class="row q-gutter-sm q-pa-sm">
              <div
                v-for="(img, index) in imageList"
                :key="index"
                style="text-align: center;"
              >
                <q-img
                  :src="img.url"
                  :ratio="1"
                  style="width: 150px; height: 150px; border-radius: 8px; border: 1px solid #e0e0e0;"
                  fit="cover"
                  spinner-color="primary"
                >
                  <template #error>
                    <div class="absolute-full flex flex-center bg-grey-3 text-grey-6 text-caption text-center q-pa-sm">
                      Gambar tidak tersedia
                    </div>
                  </template>
                </q-img>
                <div class="text-caption text-grey-7 q-mt-xs">Foto {{ index + 1 }}</div>
              </div>
            </div>
          </div>
          <!-- Image Uploader -->
          <f-image-uploader
            v-model="files"
            v-model:deleted-ids="deletedIds"
            :raw-images="dataModel.images"
            :col-attributes="[]"
          />
        </div>
      </div>
    </h-form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import Api from 'src/services/api'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Config } from 'src/services/config'
import { authStore } from 'src/stores/auth'
import { storeFile } from 'src/services/api/uploader'
import type { DataModel } from './meta'
import { Meta } from './meta'

const props = defineProps<{ props?: { id?: string | number } }>()
const emit = defineEmits(['refreshEvent'])

const router = useRouter()
const API = new Api()

type FileItem = {
  uid: string
  attachmentId?: string | null
  tempId?: string | null
  file?: File | null
  previewUrl?: string | null
}

const loading = ref(true)
const dataModel = ref<DataModel>(Meta.model)

// ✅ Start empty — ImageUploader populates from rawImages on mount/watch
const files = ref<FileItem[]>([])
const deletedIds = ref<string[]>([])
const categoryOptions = ref<any[]>([])

const init = () => {
  dataModel.value = Helper.unreactive(Meta.model)
  loadCategories()
  const action = props.props?.id ? 'update' : 'create'
  Handler.permissions(router, action, Meta, (status: boolean, data: any) => {
    Meta.permission = data
    if (status) {
      if (props.props?.id) getData(props.props.id)
      else loading.value = false
    }
  })
}

const getData = (id: string | number) => {
  loading.value = true
  API.get(`${Meta.module}/${id}`, (status: number, data: any) => {
    loading.value = false
    if (status === 200) dataModel.value = data?.data ?? data
  }, Meta.app)
}

const loadCategories = () => {
  API.get('master/item-categories', (status: number, data: any) => {
    if (status === 200) {
      const raw = data?.data?.data ?? data?.data ?? data
      categoryOptions.value = Array.isArray(raw) ? raw : []
    }
  }, Meta.app)
}

/** Resolve image URL — returns null on failure, never throws */
const resolveImageUrl = (path: string, storage?: string | null): string | null => {
  if (!path) return null

  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }

  const token = authStore().getToken()
  const baseUrl = Config.apiUrl('rental')

  if (path.startsWith('rental/') || path.startsWith('crm/') || path.startsWith('static_files/') || (storage && storage.startsWith('STATIC'))) {
    return `${baseUrl}static_files/${encodeURIComponent(path)}${token ? `?token=${token}` : ''}`
  }

  try {
    const url = (Helper as any).viewBlobFile(path, false, storage)
    return typeof url === 'string' ? url : null
  } catch {
    return null
  }
}

/** Image preview list — displays current images during edit */
const imageList = computed<{ url: string }[]>(() => {
  const raw = (dataModel.value as any)?.images
  if (!raw || typeof raw !== 'object') return []

  return Object.values(raw)
    .map((val: any) => {
      let url: string | null = null
      if (val && typeof val === 'object' && 'path' in val) {
        url = resolveImageUrl(val.path, val.storage ?? null)
      } else if (val && typeof val === 'object' && 'url' in val && val.url) {
        url = val.url
      } else if (typeof val === 'string') {
        url = resolveImageUrl(val)
      }
      return url ? { url } : null
    })
    .filter(Boolean) as { url: string }[]
})

const submit = async () => {
  if (validateSubmit()) {
    loading.value = true
    let status = 600
    if (dataModel.value.id) status = await update()
    else status = await save()

    if (status === 200) {
      // ✅ Only upload if there are actual new files or IDs to delete
      const hasNewFiles = files.value.some(f => f.file != null)
      const hasDeletedIds = deletedIds.value.length > 0

      if (hasNewFiles || hasDeletedIds) {
        await storeFile(
          `${Meta.module}/upload-files`,
          dataModel.value.id,
          dataModel.value.code,
          files,
          deletedIds,
          'rental'
        )
      }

      Helper.showSuccess('Data berhasil disimpan.')
      back()
    }
    loading.value = false
  }
}

const validateSubmit = () => {
  if (!dataModel.value.code) {
    Helper.showNotif('Kode item wajib diisi.')
    return false
  }
  if (!dataModel.value.name) {
    Helper.showNotif('Nama item wajib diisi.')
    return false
  }
  return true
}

const save = async () => {
  let statusapi = 600
  const payload = { ...dataModel.value, images: undefined }
  await API.post(Meta.module, payload, (status: number, data: any) => {
    statusapi = status
    dataModel.value.id = data?.data?.id ?? data?.id ?? null
  }, Meta.app)
  return statusapi
}

const update = async () => {
  let statusapi = 600
  const payload = { ...dataModel.value, images: undefined }
  await API.put(`${Meta.module}/${dataModel.value.id}`, payload, (status: number) => {
    statusapi = status
  }, Meta.app)
  return statusapi
}

const back = () => emit('refreshEvent')

onMounted(() => init())
</script>