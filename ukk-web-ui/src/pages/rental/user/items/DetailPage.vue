
<template>
  <div>
    <s-loading v-if="loading" />

    <div v-else class="q-pa-md">
      <div class="row items-center q-col-gutter-md q-mb-md">
        <div class="col-auto">
          <q-btn dense flat color="primary" icon="arrow_back" label="Back" @click="back" />
        </div>
        <div class="col-auto">
          <q-btn dense flat color="positive" icon="shopping_cart" label="Rent" @click="rent" :disable="!dataModel.id || !dataModel.is_active || dataModel.stock_total <= 0" />
        </div>
        <div class="col">
          <div class="text-h5 text-primary q-mb-xs">{{ dataModel.name || 'Item Detail' }}</div>
          <div class="text-subtitle2 text-grey-7">{{ dataModel.code || '-' }}</div>
        </div>
      </div>

      <div class="row q-col-gutter-md">
        <div class="col-12 col-lg-6">
          <q-card flat bordered class="shadow-1">
            <q-img
              v-if="activeImage"
              :src="activeImage"
              ratio="1"
              class="bg-white"
              spinner-color="primary"
              style="min-height: 380px; padding: 16px;"
              fit="contain"
            >
              <template #error>
                <div class="absolute-full flex flex-center bg-grey-3 text-grey-6 text-caption text-center q-pa-sm">
                  Image not available
                </div>
              </template>
            </q-img>
            <div v-else class="flex flex-center bg-grey-2" style="min-height: 380px;">
              <q-icon name="image_not_supported" size="60px" color="grey-5" />
            </div>

            <div class="row q-col-gutter-sm q-pa-sm">
              <div
                v-for="(img, index) in imageList"
                :key="index"
                class="col-3"
              >
                <q-img
                  :src="img.url"
                  :ratio="1"
                  class="cursor-pointer bg-white"
                  style="border-radius: 12px; min-height: 90px; padding: 4px;"
                  :class="activeImageIndex === index ? 'border-primary' : 'border-grey-4'"
                  fit="contain"
                  spinner-color="primary"
                  @click="activeImageIndex = index"
                >
                  <template #error>
                    <div class="absolute-full flex flex-center bg-grey-3 text-grey-6 text-caption text-center q-pa-sm">
                      Failed to load
                    </div>
                  </template>
                </q-img>
              </div>
            </div>
          </q-card>
        </div>

        <div class="col-12 col-lg-6">
          <q-card flat bordered class="shadow-1">
            <q-card-section class="q-pa-lg">
              <div class="text-h6 text-primary q-mb-sm">Product Information</div>

              <div class="row q-col-gutter-lg q-mb-md">
                <div class="col-12">
                  <div class="text-caption text-grey-6">Brand</div>
                  <div class="text-subtitle1">{{ dataModel.brand || '-' }}</div>
                </div>
                <div class="col-12">
                  <div class="text-caption text-grey-6">Category</div>
                  <div class="text-subtitle1">{{ dataModel.category_id || '-' }}</div>
                </div>
                <div class="col-6">
                  <div class="text-caption text-grey-6">Price / Day</div>
                  <div class="text-subtitle1">{{ formattedPrice }}</div>
                </div>
                <div class="col-6">
                  <div class="text-caption text-grey-6">Deposit</div>
                  <div class="text-subtitle1">{{ formattedDeposit }}</div>
                </div>
                <div class="col-6">
                  <div class="text-caption text-grey-6">Stock</div>
                  <div class="text-subtitle1">{{ itemStock }}</div>
                </div>
                <div class="col-6">
                  <div class="text-caption text-grey-6">Condition</div>
                  <div class="text-subtitle1">{{ dataModel.condition || '-' }}</div>
                </div>
              </div>

              <q-separator />

              <div class="q-mt-md text-caption text-grey-6">Description</div>
              <div class="text-body1 q-mt-xs">{{ dataModel.description || 'No description for this item.' }}</div>

              <div class="row items-center q-col-gutter-md q-mt-md">
                <div class="col-auto">
                  <q-badge :color="dataModel.is_active ? 'green' : 'red'" outline>
                    {{ dataModel.is_active ? 'Active' : 'Inactive' }}
                  </q-badge>
                </div>
              </div>

              <div class="q-mt-xl">
                <div class="text-h6 text-primary q-mb-sm">Availability Calendar</div>
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
                          Available Stock: <strong :class="selectedAvailabilityData.available_quantity > 0 ? 'text-green' : 'text-red'">{{ selectedAvailabilityData.available_quantity }}</strong> / {{ availabilityData?.stock_total }}
                        </div>
                        <div class="text-grey-7">Rented: {{ selectedAvailabilityData.reserved_quantity }}</div>
                        
                        <q-btn
                          v-if="selectedAvailabilityData.available_quantity > 0"
                          :disable="!dataModel.is_active"
                          outline
                          color="primary"
                          label="Select This Date"
                          class="q-mt-md"
                          @click="rent"
                        />
                        <div v-else class="text-red q-mt-md text-weight-bold row items-center justify-center">
                          <q-icon name="warning" size="sm" class="q-mr-xs"/> Out of Stock
                        </div>
                      </div>
                      <div v-else class="text-grey-6 row items-center justify-center">
                        <div class="q-mr-md text-center">
                          <q-icon name="event" size="30px" class="q-mb-xs" />
                          <div class="text-caption">Select a date on the calendar<br/>to see available stock.</div>
                        </div>
                        <div class="text-caption text-left" style="line-height: 1.5; border-left: 1px solid #ccc; padding-left: 16px;">
                          <q-icon name="circle" color="green" size="10px"/> Fully Available<br/>
                          <q-icon name="circle" color="orange" size="10px"/> Partially Rented<br/>
                          <q-icon name="circle" color="red" size="10px"/> Out of Stock
                        </div>
                      </div>
                    </q-card>
                  </div>
                </div>
              </div>

              <!-- Ulasan Produk -->
              <div class="q-mt-xl">
                <div class="text-h6 text-primary q-mb-md">User Reviews</div>
                <div v-if="reviewsLoading" class="text-center q-pa-md">
                  <q-spinner color="primary" size="2em" />
                </div>
                <div v-else-if="reviews.length === 0" class="text-grey-7 text-center q-pa-md bg-grey-1" style="border-radius: 8px;">
                  No reviews for this item yet.
                </div>
                <div v-else class="q-gutter-y-md">
                  <q-card v-for="rev in reviews" :key="rev.id" flat bordered>
                    <q-card-section>
                      <div class="row items-center justify-between q-mb-xs">
                        <div class="text-weight-bold">{{ rev.created_by || 'Anonymous' }}</div>
                        <div class="text-caption text-grey-6">{{ formatDate(rev.created_at) }}</div>
                      </div>
                      <q-rating :model-value="rev.rating" max="5" size="1.2em" color="warning" readonly icon="star_border" icon-selected="star" class="q-mb-sm" />
                      <div class="text-body2">{{ rev.comment || '-' }}</div>
                    </q-card-section>
                  </q-card>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import Api from 'src/services/api'
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Helper } from 'src/services/helper'
import { Config } from 'src/services/config'
import { authStore } from 'src/stores/auth'
import { Meta } from './meta'

const props = defineProps<{ props?: { id?: string | number }; data?: any }>()
const emit = defineEmits(['close'])

const route = useRoute()
const router = useRouter()
const API = new Api()
const auth = authStore()
const isLoggedIn = computed(() => !!auth.getToken())

const loading = ref(true)
const dataModel = ref(Meta.model)
const activeImageIndex = ref(0)

// Resolve image URL — returns null on failure, never throws
const encodeStaticPath = (path: string) => path.split('/').map(encodeURIComponent).join('/')
const isLocalStaticStorage = (storage?: string | null) => !!storage?.toUpperCase().startsWith('STATIC')

const resolveImageUrl = (path: string, storage?: string | null): string | null => {
  if (!path) return null
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  if (storage && !isLocalStaticStorage(storage)) {
    try {
      const url = (Helper as any).viewBlobFile(path, false, storage)
      return typeof url === 'string' ? url : null
    } catch { return null }
  }
  const token = authStore().getToken()
  const baseUrl = Config.apiUrl('rental')
  return `${baseUrl}static_files/${encodeStaticPath(path)}${token ? `?token=${token}` : ''}`
}

// Image list derived from dataModel.images — only entries with valid URLs
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

const activeImage = computed(() => {
  if (imageList.value.length === 0) return null
  const index = activeImageIndex.value >= imageList.value.length ? 0 : activeImageIndex.value
  return imageList.value[index]?.url ?? imageList.value[0]?.url
})

const formattedPrice = computed(() => {
  return `Rp ${Number(dataModel.value.price_per_day ?? 0).toLocaleString('id-ID')}`
})

const formattedDeposit = computed(() => {
  return `Rp ${Number(dataModel.value.deposit_amount ?? 0).toLocaleString('id-ID')}`
})

const itemStock = computed(() => {
  return `${dataModel.value.stock_available ?? 0} / ${dataModel.value.stock_total ?? 0}`
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
    loadReviews(id)
  }
  else loading.value = false
}

const reviews = ref<any[]>([])
const reviewsLoading = ref(true)

const loadReviews = (id: string | number) => {
  reviewsLoading.value = true
  API.get(`transaction/reviews/by-item/${id}`, (status: number, res: any) => {
    reviewsLoading.value = false
    if (status === 200) {
      reviews.value = res?.data || res || []
    }
  })
}

const formatDate = (val: string) => {
  if (!val) return '-'
  return new Date(val).toLocaleDateString('id-ID', { year: 'numeric', month: 'long', day: 'numeric' })
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
  
  API.get(`master/items/${id}/availability?start_date=${start}&end_date=${end}`, (status: number, res: any) => {
    if (status === 200) {
      availabilityData.value = res.data || res
    }
  })
}

const getData = (id: string | number) => {
  API.get(`${Meta.apiModule || Meta.module}/${id}`, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      dataModel.value = data?.data ?? data
    }
  })
}

const rent = () => {
  if (!dataModel.value.id) return
  if (!isLoggedIn.value) {
    goToLogin()
    return
  }
  router.push({ name: 'rental/user/rental', query: { item_id: String(dataModel.value.id) } })
}

const goToLogin = () => {
  router.push({ name: 'login', query: { redirect: route.fullPath } })
}

const back = () => {
  if (props?.props?.id) {
    emit('close')
    return
  }
  router.back()
}

onMounted(() => init())
</script>