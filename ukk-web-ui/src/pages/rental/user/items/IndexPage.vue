<template>
  <div class="storefront bg-grey-1">
    <s-loading v-if="loading" />
    
    <template v-else>
      <!-- Hero Header -->
      <div class="store-hero q-pa-xl text-center text-white bg-primary">
        <h1 class="text-h3 text-weight-bolder q-mb-md" style="font-family: 'Syne', sans-serif;">Katalog Alat Foto</h1>
        <p class="text-subtitle1 text-blue-1">Temukan perlengkapan foto dan video terbaik untuk kebutuhan Anda.</p>
      </div>

      <!-- Filters container -->
      <div class="container q-pa-md q-mx-auto" style="max-width: 1200px; margin-top: -30px;">
        <q-card class="q-pa-md shadow-3 rounded-borders bg-white q-mb-xl">
          <div class="row items-center q-col-gutter-md">
            <div class="col-12 col-md-6">
              <q-input
                dense
                outlined
                rounded
                debounce="300"
                v-model="searchQuery"
                placeholder="Cari kamera, lensa, atau alat lainnya..."
                clearable
                class="full-width"
              >
                <template #prepend>
                  <q-icon name="search" />
                </template>
              </q-input>
            </div>
            <div class="col-12 col-md-4">
              <q-select
                dense
                outlined
                rounded
                clearable
                v-model="categoryFilter"
                :options="categoryOptions"
                option-label="name"
                option-value="id"
                emit-value
                map-options
                label="Kategori"
              />
            </div>
            <div class="col-12 col-md-auto text-right">
              <q-btn unelevated rounded color="primary" text-color="white" label="Reset Filter" icon="refresh" @click="resetFilters" />
            </div>
          </div>
        </q-card>

        <!-- Product Grid -->
        <div class="row q-col-gutter-xl">
          <div
            v-for="raw in filteredItems"
            :key="raw.id || raw.Item?.id"
            class="col-12 col-sm-6 col-md-4 col-lg-3"
          >
            <q-card class="product-card cursor-pointer shadow-1" @click="detail(itemModel(raw))">
              <div class="product-image-wrapper">
                <q-img
                  v-if="getImage(raw)"
                  :src="getImage(raw)"
                  fit="contain"
                  class="product-image"
                />
                <div v-else class="flex flex-center bg-grey-1 product-image">
                  <q-icon name="image_not_supported" size="48px" color="grey-4" />
                </div>
                
                <div class="product-badge" :style="{ backgroundColor: itemStatusColorHex(raw) }">
                   {{ itemStatusText(raw) }}
                 </div>
              </div>

              <q-card-section class="q-pa-md bg-white text-left">
                <div class="text-caption text-uppercase text-grey-5 text-weight-bold q-mb-xs tracking-wide">{{ itemBrand(raw) }}</div>
                <div class="text-subtitle1 text-weight-bold q-mb-xs text-dark product-title ellipsis-2-lines" :title="itemName(raw)">{{ itemName(raw) }}</div>
                
                <div class="row items-center justify-between">
                  <div class="text-h6 text-primary text-weight-bolder">{{ itemPrice(raw) }}</div>
                  <div class="text-caption" :class="itemStockClass(raw)">Sisa Stok: {{ itemStockNum(raw) }}</div>
                </div>
              </q-card-section>

              <q-card-actions class="q-px-md q-pb-md bg-white q-pt-none flex-center" align="between">
                <q-btn outline rounded color="primary" label="Detail" @click.stop="detail(itemModel(raw))" />
                <q-btn
                  unelevated
                  rounded
                  color="primary"
                  icon="shopping_cart"
                  label="Rent"
                  @click.stop="rent(itemModel(raw))"
                  :disable="itemStockNum(raw) <= 0"
                />
              </q-card-actions>
            </q-card>
          </div>
        </div>

        <div v-if="!loading && filteredItems.length === 0" class="flex flex-center column q-py-xl text-grey-5" style="min-height: 300px;">
          <q-icon name="search_off" size="80px" color="grey-4" class="q-mb-md" />
          <div class="text-h6">Ups! Item tidak ditemukan.</div>
          <div class="text-subtitle2">Coba reset filter atau cari dengan kata kunci lain.</div>
        </div>
      </div>
    </template>

    <s-dialog v-model="dialog">
      <FormModal v-if="dialog.type === 'form'"
                 :props="dialog.props"
                 :meta="Meta"
                 @refreshEvent="onRefresh" />
      <DetailModal v-else
                   :props="dialog.props"
                   :meta="Meta"
                   @refreshEvent="onRefresh"
                   @close="dialog.show = false" />
    </s-dialog>
  </div>
</template>


<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Handler } from 'src/services/handler'
import type { Dialog } from 'src/services/handler'
import { Meta } from './meta'
import DetailModal from './DetailPage.vue'
import Api from 'src/services/api'
import { Helper } from 'src/services/helper'
import { Config } from 'src/services/config'
import { authStore } from 'src/stores/auth'

const dialog = ref<Dialog>({
  show: false,
  type: 'form',
  title: 'Form',
  props: null,
})

const loading = ref(true)
const refresh = ref(0)
const router = useRouter()
const route = useRoute()
const items = ref<any[]>([])
const categoryOptions = ref<any[]>([])
const searchQuery = ref('')
const categoryFilter = ref<number | null>(null)
const apiStatus = ref<any>(null)

const API = new Api()
const auth = authStore()
const isLoggedIn = computed(() => !!auth.getToken())

const itemModel = (raw: any) => raw?.Item || raw || {}
const itemName = (raw: any) => itemModel(raw)?.name || '-' 
const itemCode = (raw: any) => itemModel(raw)?.code || '-' 
const itemBrand = (raw: any) => itemModel(raw)?.brand || '-' 
const itemDescription = (raw: any) => itemModel(raw)?.description || '-' 
const itemStockNum = (raw: any) => {
  const item = itemModel(raw)
  return item.stock_available ?? 0
}
const itemStockClass = (raw: any) => {
  const stock = itemStockNum(raw)
  return stock > 0 ? 'text-positive' : 'text-negative text-weight-bold'
}
const itemPrice = (raw: any) => {
  const item = itemModel(raw)
  return `Rp ${Number(item.price_per_day ?? 0).toLocaleString('id-ID')} /hr`
}
const itemStatusText = (raw: any) => {
  const item = itemModel(raw)
  if (!item?.is_active) return 'Nonaktif'
  return (item.stock_available ?? 0) > 0 ? 'Tersedia' : 'Habis'
}
const itemStatusColorHex = (raw: any) => {
  const item = itemModel(raw)
  if (!item?.is_active) return '#94a3b8'
  return (item.stock_available ?? 0) > 0 ? '#1976d2' : '#dc2626'
}

const getImage = (item: any): string | null => {
  const images = itemModel(item)?.images
  const first = getFirstImage(images)
  if (!first) return null

  if (typeof first === 'object') {
    if ('path' in first) return resolveImageUrl(first.path, first.storage ?? null)
    if (first.url) return first.url
    return null
  }

  if (typeof first === 'string') {
    return resolveImageUrl(first)
  }

  return null
}

const getFirstImage = (images: any): any => {
  if (!images) return null
  if (Array.isArray(images)) return images.length > 0 ? images[0] : null
  if (typeof images === 'object') {
    const values = Object.values(images)
    return values.length > 0 ? values[0] : null
  }
  return images
}

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

const init = () => {
  if (route.query.category) {
    searchQuery.value = String(route.query.category)
  }
  fetchData()
  fetchCategories()
}

const fetchData = () => {
  loading.value = true
  API.get(`${Meta.apiModule || Meta.module}?limit=0`, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      if (Array.isArray(data)) {
        items.value = data
      } else if (Array.isArray(data?.data)) {
        items.value = data.data
      } else {
        items.value = []
      }
    } else {
      items.value = []
    }
  })
}

const fetchCategories = () => {
  API.get('master/item-categories?limit=0', (status: number, data: any) => {
    if (status === 200) {
      const raw = data?.data?.data ?? data?.data ?? data
      categoryOptions.value = Array.isArray(raw)
        ? raw.map((cat: any) => ({ ...cat, id: cat.id != null ? Number(cat.id) : cat.id }))
        : []
    }
  }, Meta.app)
}

const filteredItems = computed(() => {
  return items.value.filter((raw: any) => {
    const model = itemModel(raw)
    
    // Sembunyikan item yang statusnya nonaktif (is_active === false / 0) untuk user
    if (!model.is_active) {
      return false
    }

    const search = searchQuery.value.trim().toLowerCase()
    const matchText = [
      model.name,
      model.code,
      model.brand,
      model.description,
    ].filter(Boolean).join(' ').toLowerCase()

    const matchSearch = !search || matchText.includes(search)
    const itemCategoryId = model.category_id != null ? String(model.category_id) : ''
    const selectedCategoryId = categoryFilter.value != null ? String(categoryFilter.value) : ''
    const matchCategory = !selectedCategoryId || itemCategoryId === selectedCategoryId
    return matchSearch && matchCategory
  })
})

const resetFilters = () => {
  searchQuery.value = ''
  categoryFilter.value = null
}

const onRefresh = () => {
  refresh.value++
  dialog.value.show = false
  dialog.value.props = null
  fetchData()
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
const rent = (item: any) => {
  const id = item?.id
  if (!id) return
  if (!isLoggedIn.value) {
    router.push({ name: 'login', query: { redirect: `/rental/user/rental?item_id=${id}` } })
    return
  }
  router.push({ name: 'rental/user/rental', query: { item_id: String(id) } })
}

onMounted(() => init())
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Figtree:wght@400;500;600&display=swap');

.storefront {
  font-family: 'Figtree', sans-serif;
  min-height: 100vh;
}

.store-hero {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  padding-top: 100px;
  padding-bottom: 80px;
  border-bottom-left-radius: 40px;
  border-bottom-right-radius: 40px;
}

.product-card {
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  height: 100%;
}

.product-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 32px rgba(0,0,0,0.08);
  border-color: rgba(251,191,36,0.3);
}

.product-image-wrapper {
  position: relative;
  overflow: hidden;
  height: 220px;
  background-color: #ffffff;
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #f1f5f9;
}

.product-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  color: white;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  letter-spacing: 0.5px;
  z-index: 2;
}

.product-image {
  height: auto;
  max-height: 100%;
  width: 100%;
  transition: transform 0.4s ease;
}

.product-card:hover .product-image {
  transform: scale(1.08);
}

.product-title {
  font-size: 15px;
  line-height: 1.4;
  height: 42px; /* For 2 lines */
}

.tracking-wide {
  letter-spacing: 0.05em;
}

.ellipsis-2-lines {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
