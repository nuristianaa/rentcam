<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else :meta="Meta" @submit="submit" @back="back">
      <div class="row q-col-gutter-md">

        <!-- ─── Section: Informasi Rental ─────────────────────── -->
        <div class="col-12">
          <div class="form-title q-mb-sm">Informasi Rental</div>
          <div class="row q-col-gutter-sm">
            <f-select
              v-model="dataModel.status"
              col="4"
              :label="Lang.module(Meta, 'status')"
              :options="Meta.statusOptions"
              :option-label="(v) => v.label"
              option-value="value"
              emit-value
              map-options
              required
            />
            <f-select
              v-model="dataModel.payment_method"
              col="4"
              :label="Lang.module(Meta, 'payment_method')"
              :options="Meta.paymentMethodOptions"
              :option-label="(v) => v.label"
              option-value="value"
              emit-value
              map-options
              required
            />
          </div>
        </div>

        <!-- ─── Section: Customer & Petugas ──────────────────── -->
        <div class="col-12">
          <div class="form-title q-mb-sm">Customer &amp; Petugas</div>
          <div class="row q-col-gutter-sm">
            <f-select
              v-model="dataModel.customer_id"
              col="6"
              :label="Lang.module(Meta, 'customer_id')"
              :options="customerOptions"
              :option-label="(v) => v.name"
              option-value="id"
              emit-value
              map-options
              required
              @update:model-value="onCustomerChange"
            />
            <f-input
              v-model="dataModel.customer_name"
              col="5"
              :label="Lang.module(Meta, 'customer_name')"
              readonly
            />
            <!-- Tombol lihat profil customer — hanya tampil untuk admin/petugas -->
            <div v-if="!isNormalUser" class="col-1 flex items-end q-pb-xs">
              <q-btn
                round flat dense
                icon="person_search"
                color="primary"
                :disable="!dataModel.customer_id"
                @click="openCustomerProfile"
              >
                <q-tooltip>Lihat Profil Customer</q-tooltip>
              </q-btn>
            </div>
            <f-select
              v-model="dataModel.petugas_id"
              col="6"
              :label="Lang.module(Meta, 'petugas_id')"
              :options="petugasOptions"
              :option-label="(v) => v.name"
              option-value="id"
              emit-value
              map-options
              clearable
              @update:model-value="onPetugasChange"
            />
            <f-input
              v-model="dataModel.petugas_name"
              col="6"
              :label="Lang.module(Meta, 'petugas_name')"
              readonly
            />
          </div>
        </div>

        <!-- ─── Section: Periode Pinjam ───────────────────────── -->
        <div class="col-12">
          <div class="form-title q-mb-sm">Periode Pinjam</div>
          <div class="row q-col-gutter-sm">
            <f-date
              v-model="dataModel.date_range"
              col="8"
              range
              :label="Lang.module(Meta, 'start_date')"
              required
              @update:modelValue="updateDateRange"
            />
            <f-number
              v-model="dataModel.duration_days"
              col="4"
              :label="Lang.module(Meta, 'duration_days')"
              suffix="hari"
              readonly
            />
            <f-textarea
              v-model="dataModel.notes"
              col="12"
              :label="Lang.module(Meta, 'notes')"
            />
          </div>
        </div>

        <!-- ─── Section: Daftar Item ──────────────────────────── -->
        <div class="col-12">
          <div class="row items-center justify-between q-mb-sm">
            <div class="form-title">{{ Lang.module(Meta, 'items') }}</div>
            <q-btn
              label="Tambah Item"
              icon="add"
              color="primary"
              size="sm"
              unelevated
              @click="() => addItem()"
            />
          </div>

          <q-table
            :rows="dataModel.items"
            :columns="itemColumns"
            row-key="uid"
            flat
            bordered
            dense
            hide-pagination
            :pagination="{ rowsPerPage: 0 }"
          >
            <!-- Kolom Gambar -->
            <template #body-cell-image="ps">
              <q-td :props="ps" style="width:90px; padding:4px 8px;">
                <q-img
                  v-if="getItemImage(ps.row)"
                  :src="getItemImage(ps.row)"
                  ratio="1"
                  fit="cover"
                  style="width:76px; height:76px; border-radius:6px; border:1px solid #e0e0e0;"
                  spinner-color="primary"
                >
                  <template #error>
                    <div class="absolute-full flex flex-center bg-grey-3 text-grey-6 text-caption">N/A</div>
                  </template>
                </q-img>
                <div
                  v-else
                  class="flex flex-center bg-grey-2 rounded-borders text-grey-5"
                  style="width:76px; height:76px; border:1px solid #e0e0e0; border-radius:6px;"
                >
                  <q-icon name="image_not_supported" size="26px" />
                </div>
              </q-td>
            </template>

            <!-- Kolom Item -->
            <template #body-cell-item_id="ps">
              <q-td :props="ps" class="q-pa-xs">
                <q-select
                  :model-value="ps.row.item_id"
                  :options="filteredItemOptions"
                  :option-label="(v) => v ? `[${resolveItemCode(v)}] ${resolveItemName(v) ?? ''}` : ''"
                  option-value="id"
                  emit-value
                  map-options
                  dense
                  borderless
                  use-input
                  hide-selected
                  fill-input
                  input-debounce="200"
                  style="min-width:240px;"
                  :placeholder="ps.row.item_id ? resolveSelectedLabel(ps.row.item_id) : 'Cari item...'"
                  @filter="filterItems"
                  @update:model-value="(val) => { onLineItemChange(ps.row, val); filterText = '' }"
                  @blur="filterText = ''"
                >
                  <template #prepend>
                    <q-icon name="search" size="xs" color="grey-6" class="q-ml-xs" />
                  </template>
                  <!-- Custom option slot: gambar + nama -->
                  <template #option="scope">
                    <q-item v-bind="scope.itemProps" class="q-py-xs">
                      <q-item-section side>
                        <template v-if="getItemImageById(scope.opt.id)">
                          <q-img
                            :src="getItemImageById(scope.opt.id)"
                            fit="cover"
                            style="width:48px; height:48px; border-radius:4px; border:1px solid #e0e0e0;"
                            spinner-color="primary"
                          >
                            <template #error>
                              <div class="flex flex-center bg-grey-3" style="width:48px;height:48px;">
                                <q-icon name="image_not_supported" color="grey-5" size="20px" />
                              </div>
                            </template>
                          </q-img>
                        </template>
                        <div v-else class="flex flex-center bg-grey-2 rounded-borders" style="width:48px;height:48px;border:1px solid #e0e0e0;">
                          <q-icon name="image_not_supported" color="grey-5" size="20px" />
                        </div>
                      </q-item-section>
                      <q-item-section>
                        <q-item-label class="text-weight-medium">[{{ resolveItemCode(scope.opt) }}]</q-item-label>
                        <q-item-label caption>{{ resolveItemName(scope.opt) }}</q-item-label>
                        <q-item-label caption class="text-grey-6">
                          Stok: {{ scope.opt.stock_available ?? '-' }} &nbsp;|&nbsp; {{ formatCurrency(scope.opt.price_per_day) }}/hari
                        </q-item-label>
                      </q-item-section>
                    </q-item>
                  </template>

                  <!-- No option slot -->
                  <template #no-option>
                    <q-item>
                      <q-item-section class="text-grey-6 text-caption">Item tidak ditemukan</q-item-section>
                    </q-item>
                  </template>
                </q-select>
                <div v-if="ps.row.checking_availability" class="text-caption text-blue-7 q-mt-xs q-ml-sm">
                  <q-spinner-dots size="xs" color="blue" class="q-mr-xs" /> Mengecek ketersediaan...
                </div>
                <div v-else-if="ps.row.has_clash" class="text-caption text-negative q-mt-xs q-ml-sm">
                  <q-icon name="error" /> Stok habis di tanggal ini!
                </div>
                <div v-else-if="ps.row.max_available !== null" class="text-caption text-positive q-mt-xs q-ml-sm">
                  <q-icon name="check_circle" /> Tersedia (Max: {{ ps.row.max_available }})
                </div>
              </q-td>
            </template>


            <!-- Jumlah -->
            <template #body-cell-quantity="ps">
              <q-td :props="ps">
                <q-input
                  :model-value="ps.row.quantity"
                  type="number"
                  dense
                  borderless
                  min="1"
                  style="width:70px"
                  @update:model-value="(val) => onQuantityChange(ps.row, val)"
                />
              </q-td>
            </template>

            <!-- Harga/hari -->
            <template #body-cell-price_per_day="ps">
              <q-td :props="ps" class="text-right">{{ formatCurrency(ps.row.price_per_day) }}</q-td>
            </template>

            <!-- Deposit -->
            <template #body-cell-deposit_amount="ps">
              <q-td :props="ps" class="text-right">{{ formatCurrency(ps.row.deposit_amount) }}</q-td>
            </template>

            <!-- Subtotal -->
            <template #body-cell-subtotal="ps">
              <q-td :props="ps" class="text-right">{{ formatCurrency(ps.row.subtotal) }}</q-td>
            </template>

            <!-- Hapus -->
            <template #body-cell-action="ps">
              <q-td :props="ps" class="text-center">
                <q-btn
                  round flat dense
                  color="negative"
                  icon="delete"
                  size="sm"
                  @click="removeItem(ps.rowIndex)"
                />
              </q-td>
            </template>

            <!-- Footer total -->
            <template #bottom-row>
              <q-tr class="bg-grey-2 text-weight-bold">
                <q-td colspan="4" class="text-right">Total</q-td>
                <q-td class="text-right">{{ formatCurrency(dataModel.deposit_total) }}</q-td>
                <q-td class="text-right">{{ formatCurrency(dataModel.subtotal) }}</q-td>
                <q-td />
              </q-tr>
            </template>
          </q-table>
        </div>

        <!-- ─── Section: Ringkasan Biaya ──────────────────────── -->
        <div class="col-12">
          <div class="form-title q-mb-sm">Ringkasan Biaya</div>
          <div class="row q-col-gutter-sm justify-end">
            <f-number
              v-model="dataModel.subtotal"
              col="4"
              :label="Lang.module(Meta, 'subtotal')"
              prefix="Rp"
              readonly
            />
            <f-number
              v-model="dataModel.deposit_total"
              col="4"
              :label="Lang.module(Meta, 'deposit_total')"
              prefix="Rp"
              readonly
            />
            <f-number
              v-model="dataModel.grand_total"
              col="4"
              :label="Lang.module(Meta, 'grand_total')"
              prefix="Rp"
              readonly
            />
          </div>
        </div>

      </div>
    </h-form>

    <!-- ─── Dialog: Profil Customer ───────────────────────────── -->
    <q-dialog v-model="customerProfileDialog.show">
      <q-card style="min-width: 420px; max-width: 560px; width: 100%;">
        <q-card-section class="bg-primary text-white row items-center q-py-sm">
          <q-avatar size="44px" class="q-mr-md" style="background: rgba(255,255,255,0.2);">
            <span class="text-h6 text-bold text-white" style="line-height:1;">{{ customerProfileDialog.initials }}</span>
          </q-avatar>
          <div>
            <div class="text-subtitle1 text-weight-bold">{{ customerProfileDialog.data?.name || 'Profil Customer' }}</div>
            <div class="text-caption opacity-80">{{ customerProfileDialog.data?.email || '-' }}</div>
          </div>
          <q-space />
          <q-btn flat round dense icon="close" color="white" v-close-popup />
        </q-card-section>

        <q-card-section class="q-pa-none">
          <q-list separator>
            <q-item>
              <q-item-section side><q-icon name="phone" color="primary" /></q-item-section>
              <q-item-section>
                <q-item-label overline class="text-grey-6">No. HP</q-item-label>
                <q-item-label>{{ customerProfileDialog.data?.phone || '-' }}</q-item-label>
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section side><q-icon name="cake" color="primary" /></q-item-section>
              <q-item-section>
                <q-item-label overline class="text-grey-6">Tanggal Lahir</q-item-label>
                <q-item-label>{{ customerProfileDialog.data?.birthday ? new Date(customerProfileDialog.data.birthday).toLocaleDateString('id-ID', { day:'2-digit', month:'long', year:'numeric' }) : '-' }}</q-item-label>
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section side><q-icon name="home" color="primary" /></q-item-section>
              <q-item-section>
                <q-item-label overline class="text-grey-6">Alamat</q-item-label>
                <q-item-label>{{ customerProfileDialog.data?.location || '-' }}</q-item-label>
              </q-item-section>
            </q-item>
            <q-item>
              <q-item-section side><q-icon name="badge" color="primary" /></q-item-section>
              <q-item-section>
                <q-item-label overline class="text-grey-6">Foto KTP</q-item-label>
                <q-item-label>
                  <template v-if="customerProfileDialog.data?.profile_picture">
                    <q-img
                      :src="resolveKtpUrl(customerProfileDialog.data)"
                      style="max-width: 100%; max-height: 220px; border-radius: 8px; border: 1px solid #e0e0e0; margin-top: 6px;"
                      fit="contain"
                      spinner-color="primary"
                    >
                      <template #error>
                        <div class="flex flex-center bg-grey-2 text-grey-5 text-caption" style="height: 80px;">
                          <q-icon name="broken_image" size="28px" />
                        </div>
                      </template>
                    </q-img>
                  </template>
                  <q-badge v-else color="negative" label="Belum Upload" />
                </q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>

        <q-card-section class="q-pt-none q-pb-md q-px-md">
          <q-banner
            v-if="!isProfileComplete(customerProfileDialog.data)"
            rounded
            dense
            class="bg-amber-1 text-amber-10 q-mt-sm"
          >
            <template #avatar><q-icon name="warning" color="amber-8" /></template>
            Profil customer <strong>belum lengkap</strong>. Pastikan customer mengisi nama, no. HP, alamat, dan foto KTP sebelum melanjutkan rental.
          </q-banner>
          <q-banner v-else rounded dense class="bg-green-1 text-green-9 q-mt-sm">
            <template #avatar><q-icon name="check_circle" color="green-7" /></template>
            Profil customer sudah lengkap dan siap rental.
          </q-banner>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { useQuasar } from 'quasar'
import { ref, onMounted, watch, toRaw, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Config } from 'src/services/config'
import { Meta } from './meta'
import type { DataModel } from './meta'
import { Lang } from 'src/services/lang'
import { authStore } from 'src/stores/auth'

const emit = defineEmits(['refreshEvent'])

const route  = useRoute()
const router = useRouter()
const getRouteId = () => {
  const raw = route.params?.id
  return Array.isArray(raw) ? raw[0] : (raw ?? null)
}
const id = ref<string | null>(getRouteId())
const queryItemId = (() => {
  const raw = route.query?.item_id
  const value = Array.isArray(raw) ? raw[0] : raw
  const parsed = Number(value)
  return Number.isInteger(parsed) ? parsed : null
})()
const $q       = useQuasar()
const API      = new Api()

const checkAvailability = (row: any) => {
  const s = dataModel.value.start_date
  const e = dataModel.value.end_date
  if (!s || !e || !row.item_id) {
    row.has_clash = false
    row.max_available = null
    return
  }

  row.checking_availability = true
  const url = `master/items/${row.item_id}/availability?start_date=${s}&end_date=${e}`
  API.get(url, (status: number, data: any) => {
    row.checking_availability = false
    if (status === 200) {
      const availData = data?.data ?? data
      if (availData?.days && Array.isArray(availData.days)) {
        const min_avail = Math.min(...availData.days.map((d: any) => d.available_quantity))
        row.max_available = min_avail >= 0 ? min_avail : 0
        
        if (row.quantity > row.max_available) {
          if (row.max_available === 0) {
            $q.notify({ type: 'negative', message: `Stok [${row.item_code}] habis untuk tanggal terpilih.` })
            row.has_clash = true
          } else {
            $q.notify({ type: 'warning', message: `Menyesuaikan stok otomatis [${row.item_code}]: Sisa ${row.max_available}` })
            row.quantity = row.max_available
            row.has_clash = false
            recalcLineItem(row)
          }
        } else {
          row.has_clash = false
        }
      }
    }
  }, Meta.app) // atau bisa jadi beda app, try this first
}

watch(
  () => route.params.id,
  () => {
    id.value = getRouteId()
    init()
  }
)

const loading        = ref(true)
const dataModel      = ref<DataModel>({ ...Meta.model })
const customerOptions = ref<any[]>([])
const petugasOptions  = ref<any[]>([])
const itemOptions     = ref<any[]>([])
const auth            = authStore()

// ─── Role detection ─────────────────────────────────────────
const isNormalUser = computed(() => {
  const u = auth.user || auth.getUser()
  if (!u) return false
  const rc  = typeof u.role_code === 'string' ? u.role_code.toLowerCase() : null
  const roc = u.role && typeof u.role.code === 'string' ? u.role.code.toLowerCase() : null
  return rc === 'user' || roc === 'user' || u.role_id === 3 || u.user_type === 'user'
})

// ─── Dialog profil customer ─────────────────────────────────
const customerProfileDialog = ref({
  show: false,
  data: null as any,
  initials: '-',
})

const isProfileComplete = (user: any): boolean => {
  if (!user) return false
  return !!user.name && !!user.phone && !!user.location && !!user.profile_picture
}

const resolveKtpUrl = (user: any): string => {
  if (!user?.profile_picture) return ''
  return Helper.viewBlobFile(user.profile_picture, false, user.storage_id ?? null)
}

const openCustomerProfile = () => {
  const customerId = dataModel.value.customer_id
  if (!customerId) return
  API.get(`auth/users/${customerId}`, (status: number, data: any) => {
    if (status === 200) {
      const u = data?.data ?? data
      customerProfileDialog.value = {
        show:     true,
        data:     u,
        initials: (u?.name ?? '?').charAt(0).toUpperCase(),
      }
    } else {
      $q.notify({ type: 'negative', message: 'Failed to load customer profile.' })
    }
  }, 'identity')
}

// ─── Search filter untuk dropdown item ─────────────────────
const filterText = ref('')
const filteredItemOptions = computed(() => {
  const q = filterText.value.toLowerCase().trim()
  if (!q) return itemOptions.value
  return itemOptions.value.filter((item: any) => {
    const code = (item?.code ?? item?.item_code ?? '').toLowerCase()
    const name = (item?.name ?? item?.item_name ?? '').toLowerCase()
    return code.includes(q) || name.includes(q)
  })
})

const filterItems = (val: string, update: (fn: () => void) => void) => {
  update(() => { filterText.value = val })
}

// ─── Kolom tabel items ──────────────────────────────────────
const itemColumns = [
  { name: 'image',         label: 'Gambar',      field: 'image',        align: 'center' as const, style: 'width: 100px' },
  { name: 'item_id',       label: 'Item',        field: 'item_id',       align: 'left'  as const },
  { name: 'quantity',      label: 'Qty',         field: 'quantity',      align: 'right' as const },
  { name: 'price_per_day', label: 'Harga/Hari',  field: 'price_per_day', align: 'right' as const },
  { name: 'deposit_amount',label: 'Deposit',     field: 'deposit_amount',align: 'right' as const },
  { name: 'subtotal',      label: 'Subtotal',    field: 'subtotal',      align: 'right' as const },
  { name: 'action',        label: '',            field: 'id',            align: 'center' as const, style: 'width: 40px' },
]

const resolveItemCode = (item: any) => item?.item_code ?? item?.code ?? item?.name ?? ''
const resolveItemName = (item: any) => item?.item_name ?? item?.name ?? item?.code ?? null

const normalizeId = (id: any) => {
  if (id == null) return id
  const parsed = Number(id)
  return Number.isInteger(parsed) ? parsed : id
}

const getItemById = (id: any) => {
  if (id == null) return null
  if (typeof id === 'object' && 'id' in id) {
    id = (id as any).id
  }
  const found = itemOptions.value.find((i) => String(i.id) === String(id))
  return found ? toRaw(found) : null
}

const getItemImage = (row: any): string | null => {
  const item = getItemById(row.item_id)
  if (!item) return null

  const images = item?.images
  const first = getFirstImage(images)
  if (!first) return null

  if (typeof first === 'object') {
    if ('path' in first) return resolveImageUrl(first.path, first.storage ?? null)
    if (first.url) return first.url
    return null
  }

  if (typeof first === 'string') return resolveImageUrl(first)
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

/** Ambil URL gambar berdasarkan item id — untuk slot option di dropdown */
const getItemImageById = (itemId: any): string | null => {
  const item = getItemById(itemId)
  if (!item) return null
  const first = getFirstImage(item?.images)
  if (!first) return null
  if (typeof first === 'object') {
    if ('path' in first) return resolveImageUrl(first.path, first.storage ?? null)
    if (first.url) return first.url
    return null
  }
  if (typeof first === 'string') return resolveImageUrl(first)
  return null
}

/** Label teks item yang sedang dipilih (untuk placeholder saat use-input) */
const resolveSelectedLabel = (itemId: any): string => {
  const item = getItemById(itemId)
  if (!item) return ''
  return `[${resolveItemCode(item)}] ${resolveItemName(item) ?? ''}`
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
    } catch {
      return null
    }
  }
  const token = authStore().getToken()
  const baseUrl = Config.apiUrl('rental')
  return `${baseUrl}static_files/${encodeStaticPath(path)}${token ? `?token=${token}` : ''}`
}

// ─── Load master data ───────────────────────────────────────
const loadOptions = () => {
  const currentUser = auth.user || auth.getUser()
  const roleCode = typeof currentUser?.role_code === 'string' ? currentUser.role_code.toLowerCase() : null
  const roleObjectCode = currentUser?.role && typeof currentUser.role.code === 'string' ? currentUser.role.code.toLowerCase() : null
  const isNormalUser = currentUser != null && (
    roleCode === 'user' || roleObjectCode === 'user' || currentUser.role_id === 3 || currentUser.user_type === 'user'
  )

  if (isNormalUser && currentUser) {
    customerOptions.value = [currentUser]
    petugasOptions.value = [currentUser]

    if (!id.value) {
      dataModel.value.customer_id = currentUser.id
      dataModel.value.customer_name = currentUser.name
      dataModel.value.petugas_id = currentUser.id
      dataModel.value.petugas_name = currentUser.name
    }
  } else if (currentUser) {
    API.get('auth/users?limit=0', (s: number, d: any) => {
      if (s === 200) {
        const users = d?.data ?? d
        customerOptions.value = users
        petugasOptions.value = users
      }
    }, 'identity')
  }

  API.get('master/items?limit=0', (s: number, d: any) => {
    if (s === 200) {
      const items = d?.data ?? d
      itemOptions.value = Array.isArray(items)
        ? items.map((item: any) => ({ ...item, id: normalizeId(item.id) }))
        : []
      if (queryItemId && !id.value && (!dataModel.value.items || dataModel.value.items.length === 0)) {
        addItem(normalizeId(queryItemId))
      }
    }
  }, Meta.app)
}

// ─── Event handlers ─────────────────────────────────────────
const onCustomerChange = (val: number) => {
  const found = customerOptions.value.find((c) => c.id === val)
  if (found) dataModel.value.customer_name = found.name
}

const onPetugasChange = (val: number | null) => {
  if (val == null) {
    dataModel.value.petugas_name = null
    return
  }
  const found = petugasOptions.value.find((p) => p.id === val)
  if (found) dataModel.value.petugas_name = found.name
}

const recalcDuration = () => {
  const s = dataModel.value.start_date
  const e = dataModel.value.end_date
  if (s && e) {
    const diff = Math.ceil(
      (new Date(e).getTime() - new Date(s).getTime()) / (1000 * 60 * 60 * 24)
    )
    dataModel.value.duration_days = diff >= 0 ? diff + 1 : 0
    // Recalculate ALL line item subtotals based on new duration
    ;(dataModel.value.items ?? []).forEach((row: any) => {
      row.subtotal = (row.quantity ?? 0) * (row.price_per_day ?? 0) * (dataModel.value.duration_days ?? 1)
    })
    recalcTotals()
  }
}

const updateDateRange = (range: string) => {
  const split = (range ?? '').split(' ')
  if (split.length > 1) {
    dataModel.value.start_date = split[0] ?? null
    dataModel.value.end_date = split[2] ?? null
  } else {
    dataModel.value.start_date = split[0] ?? null
    dataModel.value.end_date = split[0] ?? null
  }
  recalcDuration()
  dataModel.value.items?.forEach((row: any) => checkAvailability(row))
}

// ─── Item line management ────────────────────────────────────
const makeItem = () => ({
  uid:            crypto.randomUUID(),
  item_id:        null,
  item_code:      null,
  item_name:      null,
  quantity:       1,
  price_per_day:  0,
  deposit_amount: 0,
  subtotal:       0,
  max_available:  null,
  has_clash:      false,
  checking_availability: false,
})

const addItem = (itemId?: number | null) => {
  const item = makeItem()
  if (itemId != null) {
    const found = getItemById(itemId)
    if (found) {
      item.item_id        = normalizeId(found.id)
      item.item_code      = resolveItemCode(found)
      item.item_name      = resolveItemName(found)
      item.price_per_day  = found.price_per_day ?? 0
      item.deposit_amount = found.deposit_amount ?? 0
    }
  }
  item.subtotal = 0
  dataModel.value.items = [...(dataModel.value.items ?? []), item]
  if (itemId != null) {
    recalcLineItem(item)
  }
}

const removeItem = (idx: number) => {
  dataModel.value.items?.splice(idx, 1)
  recalcTotals()
}

const onLineItemChange = (row: any, val: any) => {
  // val adalah primitive id (karena emit-value + option-value="id")
  if (val == null) {
    if (row.item_id == null) return  // guard: no changes
    row.item_id        = null
    row.item_code      = null
    row.item_name      = null
    row.price_per_day  = 0
    row.deposit_amount = 0
    row.subtotal       = 0
    recalcTotals()
    return
  }
  const newId = normalizeId(val)
  if (String(row.item_id) === String(newId)) return  // guard: cegah recursive update QTd
  const found = getItemById(newId)
  row.item_id        = newId
  row.item_code      = found ? resolveItemCode(found) : null
  row.item_name      = found ? resolveItemName(found) : null
  row.price_per_day  = found?.price_per_day  ?? 0
  row.deposit_amount = found?.deposit_amount ?? 0
  recalcLineItem(row)
  checkAvailability(row)
}

const onQuantityChange = (row: any, val: any) => {
  const quantity = Number(val)
  const newQty = Number.isFinite(quantity) && quantity > 0 ? quantity : 1
  if (Number(row.quantity) === newQty) return  // guard: q-input type=number emit string, compare as number
  if (typeof row.max_available === 'number' && newQty > row.max_available) {
    $q.notify({ type: 'warning', message: `Maksimal stok yang tersedia hanya ${row.max_available}` })
    row.quantity = row.max_available
    row.has_clash = row.max_available === 0
  } else {
    row.quantity = newQty
    row.has_clash = false
  }

  recalcLineItem(row)
}

const recalcLineItem = (row: any) => {
  const days = dataModel.value.duration_days ?? 1
  row.subtotal = (row.quantity ?? 0) * (row.price_per_day ?? 0) * days
  recalcTotals()
}

const recalcTotals = () => {
  const items = dataModel.value.items ?? []
  dataModel.value.subtotal      = items.reduce((s, i) => s + (i.subtotal       ?? 0), 0)
  dataModel.value.deposit_total = items.reduce((s, i) => s + (i.deposit_amount ?? 0) * (i.quantity ?? 0), 0)
  dataModel.value.grand_total   = dataModel.value.subtotal + dataModel.value.deposit_total
}

// ─── Helper display ──────────────────────────────────────────
const formatCurrency = (val: number | null) =>
  new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(val ?? 0)

// ─── CRUD ────────────────────────────────────────────────────
const init = () => {
  loading.value = true
  dataModel.value = Helper.unreactive(Meta.model)
  loadOptions()
  const action = id.value ? 'update' : 'create'
  Handler.permissions(router, action, Meta, (status: boolean, data: any) => {
    Meta.permission = data
    if (status) {
      if (id.value) getData(id.value)
      else loading.value = false
    } else {
      loading.value = false
    }
  })
}

const getData = (id: string | number) => {
  API.get(`${Meta.module}/${id}`, (status: number, data: any) => {
    if (status === 200) {
      dataModel.value = data
      dataModel.value.items = (dataModel.value.items ?? []).map((item: any) => ({
        uid: item.uid ?? crypto.randomUUID(),
        ...item,
        item_id: normalizeId(item.item_id)
      }))
      if (data.start_date && data.end_date) {
        dataModel.value.date_range = `${data.start_date} to ${data.end_date}`
      } else if (data.start_date) {
        dataModel.value.date_range = data.start_date
      }
      recalcTotals()
    }
    loading.value = false
  }, Meta.app)
}

const save = async () => {
  let statusapi = 600
  await API.post(Meta.module, dataModel.value, (status: number, _data: any) => {
    statusapi = status
    dataModel.value.id          = _data.id
    dataModel.value.rental_code = _data.rental_code
  }, Meta.app)
  return statusapi
}

const update = async () => {
  let statusapi = 600
  await API.put(`${Meta.module}/${dataModel.value.id}`, dataModel.value, (status: number, _data: any) => {
    statusapi = status
  }, Meta.app)
  return statusapi
}

const submit = async () => {
  loading.value = true

  // Guard: jika user biasa, pastikan profil lengkap dulu
  if (isNormalUser.value) {
    const currentUser = auth.user || auth.getUser()
    if (!isProfileComplete(currentUser)) {
      loading.value = false
      $q.dialog({
        title: 'Profil Belum Lengkap',
        message: 'Lengkapi profil Anda (nama, no. HP, alamat, dan foto KTP) terlebih dahulu sebelum melakukan pemesanan rental.',
        html: true,
        ok: { label: 'Lengkapi Profil', color: 'primary', unelevated: true },
        cancel: { label: 'Batal', flat: true },
      }).onOk(() => {
        router.push({ name: 'user-change-profile' })
      })
      return
    }
  }

  const status = dataModel.value.id ? await update() : await save()

  if (status === 200) {
    Helper.showSuccess('Data successfully saved.')
    back()
  }

  loading.value = false
}

const back = () => {
  emit('refreshEvent')
  router.back()
}

onMounted(init)
</script>