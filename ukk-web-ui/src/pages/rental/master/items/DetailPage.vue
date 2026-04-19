<template>
  <div>
    <s-loading v-if="loading" />

    <h-detail v-else :meta="Meta" :modal="props.data" @back="back" :model="dataModel">
      <div class="row q-pa-sm">

        <f-card title="Detail" col="6">
          <s-list
            v-for="(value, index) in viewList"
            :key="index"
            :data="value"
          />
        </f-card>

        <f-card title="Log" col="6">
          <log-info :data="dataModel" />
        </f-card>

        <!-- Foto Alat: ada gambar -->
        <f-card title="Foto Alat" col="12" v-if="imageList.length > 0">
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
        </f-card>

        <!-- Foto Alat: kosong -->
        <f-card title="Foto Alat" col="12" v-else>
          <div class="text-center q-py-lg text-grey-5">
            <q-icon name="image_not_supported" size="40px" />
            <div class="q-mt-sm">No photos available for this item yet.</div>
          </div>
        </f-card>

        <!-- Kalender Ketersediaan -->
        <f-card title="Kalender Ketersediaan" col="12">
          <div class="row q-col-gutter-md">
            <div class="col-12 flex flex-center">
               <q-date
                v-model="selectedAvailabilityDate"
                mask="YYYY-MM-DD"
                :events="dateEvents"
                :event-color="getEventColor"
                minimal
                flat bordered
                class="full-width"
                style="max-width: 400px;"
              />
            </div>
            <div class="col-12">
              <q-card flat bordered class="q-pa-md bg-grey-1 text-center">
                <div v-if="selectedAvailabilityData">
                  <div class="text-h6 text-primary font-weight-bold">{{ selectedAvailabilityDate }}</div>
                  <div class="q-mt-md text-subtitle1">
                    Stok Tersedia: <strong :class="selectedAvailabilityData.available_quantity > 0 ? 'text-green' : 'text-red'">{{ selectedAvailabilityData.available_quantity }}</strong> / {{ availabilityData?.stock_total }}
                  </div>
                  <div class="text-grey-7">Telah Disewa: {{ selectedAvailabilityData.reserved_quantity }}</div>
                </div>
                <div v-else class="text-grey-6 row items-center justify-center">
                  <div class="q-mr-md text-center">
                    <q-icon name="event" size="30px" class="q-mb-xs" />
                    <div class="text-caption">Pilih tanggal pada kalender<br/>untuk melihat stok tersedia.</div>
                  </div>
                  <div class="text-caption text-left" style="line-height: 1.5; border-left: 1px solid #ccc; padding-left: 16px;">
                    <q-icon name="circle" color="green" size="10px"/> Tersedia Penuh<br/>
                    <q-icon name="circle" color="orange" size="10px"/> Sebagian Disewa<br/>
                    <q-icon name="circle" color="red" size="10px"/> Habis
                  </div>
                </div>
              </q-card>
            </div>
          </div>
        </f-card>

      </div>
    </h-detail>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Config } from 'src/services/config'
import { authStore } from 'src/stores/auth'
import { Meta } from './meta'

const props = defineProps<{ props?: { id?: string | number }; data?: any }>()

const route = useRoute()
const router = useRouter()
const API = new Api()

const loading = ref(true)
const dataModel = ref(Meta.model)
const viewList = ref<any[]>([])

/** Resolve image URL — returns null on failure, never throws */
const resolveImageUrl = (path: string, storage?: string | null): string | null => {
  if (!path) return null

  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }

  const token = authStore().getToken()
  const baseUrl = Config.apiUrl('rental')

  // Gunakan static_files jika path dimulai dengan prefix yang dikenal,
  // atau jika storage bertipe STATIC (sama seperti logika di FormPage)
  if (
    path.startsWith('rental/') ||
    path.startsWith('crm/') ||
    path.startsWith('static_files/') ||
    (storage && storage.startsWith('STATIC'))
  ) {
    return `${baseUrl}static_files/${encodeURIComponent(path)}${token ? `?token=${token}` : ''}`
  }

  try {
    const url = (Helper as any).viewBlobFile(path, false, storage)
    return typeof url === 'string' ? url : null
  } catch {
    return null
  }
}

/** Image list derived from dataModel.images — only entries with valid URLs */
const imageList = computed<{ url: string }[]>(() => {
  const raw = (dataModel.value as any)?.images
  if (!raw || typeof raw !== 'object') return []

  return Object.values(raw)
    .map((val: any) => {
      let url: string | null = null
      if (val && typeof val === 'object') {
        if ('path' in val) {
          url = resolveImageUrl(val.path, val.storage ?? null)
        } else if (val.url) {
          url = val.url
        }
      } else if (typeof val === 'string') {
        url = resolveImageUrl(val)
      }
      return url ? { url } : null
    })
    .filter(Boolean) as { url: string }[]
})

const init = () => {
  dataModel.value = Helper.unreactive(Meta.model)
  onRefresh()
}

const onRefresh = () => {
  const id: any = props?.props?.id ?? route?.params?.id
  if (id) {
    getData(id)
    loadAvailability(id)
  }
  else loading.value = false
}

const availabilityData = ref<any>(null)
const selectedAvailabilityDate = ref<string>('')

const dateEvents = computed(() => {
  if (!availabilityData.value?.days) return []
  return availabilityData.value.days.map((d: any) => d.date.replace(/-/g, '/'))
})

const getEventColor = (dateStr: string) => {
  if (!availabilityData.value?.days) return 'primary'
  const day = availabilityData.value.days.find((d: any) => d.date === dateStr.replace(/\//g, '-'))
  if (!day) return 'primary'
  if (day.available_quantity === 0) return 'red'
  if (day.reserved_quantity > 0) return 'orange'
  return 'green'
}

const selectedAvailabilityData = computed(() => {
  if(!selectedAvailabilityDate.value || !availabilityData.value?.days) return null
  return availabilityData.value.days.find((d: any) => d.date === selectedAvailabilityDate.value)
})

const loadAvailability = (id: string | number) => {
  const d = new Date()
  const start = d.toISOString().split('T')[0]
  const dEnd = new Date()
  dEnd.setDate(dEnd.getDate() + 90)
  const end = dEnd.toISOString().split('T')[0]
  
  API.get(`${Meta.module}/${id}/availability?start_date=${start}&end_date=${end}`, (status: number, res: any) => {
    if (status === 200) {
      availabilityData.value = res.data || res
    }
  })
}

const getData = (id: string | number) => {
  API.get(`${Meta.module}/${id}`, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      dataModel.value = data?.data ?? data

      viewList.value = Handler.viewList(dataModel.value, {
        app: Meta.app,
        schema: Meta.schema,
        name: Meta.name,
        exclude: ['id', 'images'],  // ✅ images rendered separately
      })
    }
  })
}

const back = () => {
  if (!props.data) router.back()
}

onMounted(() => init())
</script>