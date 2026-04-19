<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else :meta="Meta" @submit="submit" @back="back">
      <template #buttons>
        <q-btn flat rounded label="Rental History" icon="history" color="secondary" @click="$router.push({ name: 'user/rental-histories' })" class="q-mr-sm" />
        <q-btn outline rounded label="Cancel" @click="back" />
        <q-btn unelevated rounded label="Submit" color="primary" icon="check_circle" type="submit" class="text-bold" />
      </template>
      <div class="row q-col-gutter-md">

        <!-- ─── Section: Informasi Pemesanan ──────────────────── -->
        <div class="col-12">
          <div class="form-title q-mb-sm">Booking Information</div>
          <div class="row q-col-gutter-sm">
            <f-select
              v-model="dataModel.payment_method"
              col="6"
              :label="Lang.module(Meta, 'payment_method')"
              :options="Meta.paymentMethodOptions"
              :option-label="(v) => v.label"
              option-value="value"
              emit-value
              map-options
              required
            />
            <f-input
              v-model="dataModel.customer_name"
              col="6"
              :label="Lang.module(Meta, 'customer_name')"
              readonly
            />

            <div v-if="dataModel.payment_method === 'transfer'" class="col-12">
              <q-banner rounded dense class="bg-blue-1 text-blue-9">
                <template #avatar>
                  <q-icon name="info" color="blue-7" />
                </template>
                <div class="text-caption text-weight-bold q-mb-xs">Transfer Payment Instructions</div>
                <div class="text-caption q-mb-xs">Please transfer to the following account, then send the payment proof via WhatsApp:</div>
                <div class="text-caption q-mb-xs">🏦 <b>BCA Bank</b> — Account No: <b>083851071957</b> a.n. <b>Nuristiana Izatul</b></div>
                <div class="text-caption q-mb-xs">Payment is primarily via bank transfer. After transferring, send the receipt via WA to speed up verification and confirmation.</div>
                <div class="text-caption">
                  📱 Admin WhatsApp:
                  <a
                    :href="`https://wa.me/6283851071957?text=Hello Admin, I am ${dataModel.customer_name ?? ''} sending the transfer receipt for my camera rental booking.`"
                    target="_blank"
                    class="text-blue-9 text-weight-bold"
                  >0838-5107-1957</a>
                </div>
              </q-banner>
            </div>
          </div>
        </div>

        <!-- ─── Section: Periode Sewa ─────────────────────────── -->
        <div class="col-12">
          <div class="form-title q-mb-sm">Rental Period</div>
          <div class="row q-col-gutter-sm">
            <f-date
              v-model="dataModel.date_range"
              col="8"
              range
              :label="Lang.module(Meta, 'start_date')"
              :options="isFutureDate"
              required
              @update:modelValue="updateDateRange"
            />
            <f-number
              v-model="dataModel.duration_days"
              col="4"
              :label="Lang.module(Meta, 'duration_days')"
              suffix="days"
              readonly
              precision="0"
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
              label="Add Item"
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
            <!-- Gambar -->
            <template #body-cell-image="ps">
              <q-td :props="ps" style="width:90px; padding:4px 8px;">
                <q-img
                  v-if="resolveItemImage(ps.row)"
                  :src="resolveItemImage(ps.row)"
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

            <!-- Item dengan search + gambar -->
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
                  :placeholder="ps.row.item_id ? resolveSelectedLabel(ps.row.item_id) : 'Search items...'"
                  @filter="filterItems"
                  @update:model-value="(val) => { onLineItemChange(ps.row, val); filterText = '' }"
                  @blur="filterText = ''"
                >
                  <template #option="scope">
                    <q-item v-bind="scope.itemProps" class="q-py-xs">
                      <q-item-section side>
                        <q-img
                          v-if="getFirstImageUrl(itemOptions.find(i => String(i.id) === String(scope.opt.id))?.images)"
                          :src="getFirstImageUrl(itemOptions.find(i => String(i.id) === String(scope.opt.id))?.images)"
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
                        <div v-else class="flex flex-center bg-grey-2 rounded-borders" style="width:48px;height:48px;border:1px solid #e0e0e0;">
                          <q-icon name="image_not_supported" color="grey-5" size="20px" />
                        </div>
                      </q-item-section>
                      <q-item-section>
                        <q-item-label class="text-weight-medium">[{{ resolveItemCode(scope.opt) }}]</q-item-label>
                        <q-item-label caption>{{ resolveItemName(scope.opt) }}</q-item-label>
                        <q-item-label caption class="text-grey-6">
                          Stock: {{ scope.opt.stock_available ?? '-' }} &nbsp;|&nbsp; {{ formatCurrency(scope.opt.price_per_day) }}/day
                        </q-item-label>
                      </q-item-section>
                    </q-item>
                  </template>
                  <template #no-option>
                    <q-item>
                      <q-item-section class="text-grey-6 text-caption">Item not found</q-item-section>
                    </q-item>
                  </template>
                </q-select>
                <div v-if="ps.row.checking_availability" class="text-caption text-blue-7 q-mt-xs q-ml-sm">
                  <q-spinner-dots size="xs" color="blue" class="q-mr-xs" /> Checking availability...
                </div>
                <div v-else-if="ps.row.has_clash" class="text-caption text-negative q-mt-xs q-ml-sm">
                  <q-icon name="error" /> Out of stock on this date!
                </div>
                <div v-else-if="ps.row.max_available !== null" class="text-caption text-positive q-mt-xs q-ml-sm">
                  <q-icon name="check_circle" /> Available (Max: {{ ps.row.max_available }})
                </div>
              </q-td>
            </template>

            <!-- Qty -->
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

            <template #body-cell-price_per_day="ps">
              <q-td :props="ps" class="text-right">{{ formatCurrency(ps.row.price_per_day) }}</q-td>
            </template>

            <template #body-cell-deposit_amount="ps">
              <q-td :props="ps" class="text-right">{{ formatCurrency(ps.row.deposit_amount) }}</q-td>
            </template>

            <template #body-cell-subtotal="ps">
              <q-td :props="ps" class="text-right">{{ formatCurrency(ps.row.subtotal) }}</q-td>
            </template>

            <template #body-cell-action="ps">
              <q-td :props="ps" class="text-center">
                <q-btn round flat dense color="negative" icon="delete" size="sm" @click="removeItem(ps.rowIndex)" />
              </q-td>
            </template>

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
          <div class="form-title q-mb-sm">Cost Summary</div>
          <div class="row q-col-gutter-sm justify-end">
            <f-number v-model="dataModel.subtotal" col="4" :label="Lang.module(Meta, 'subtotal')" prefix="Rp" readonly />
            <f-number v-model="dataModel.deposit_total" col="4" :label="Lang.module(Meta, 'deposit_total')" prefix="Rp" readonly />
            <f-number v-model="dataModel.grand_total" col="4" :label="Lang.module(Meta, 'grand_total')" prefix="Rp" readonly />
          </div>
        </div>

        <div class="col-12">
          <q-card flat bordered class="bg-grey-1 q-pa-md q-mt-md">
            <div class="text-subtitle2 text-weight-bold q-mb-sm">Store Location</div>
            <div class="text-caption q-mb-xs">
              📍 Karyawangi, Parongpong
            </div>
            <div class="text-caption q-mb-sm">
              <a
                class="text-blue text-weight-bold"
                href="https://maps.app.goo.gl/tW7X2aR8Z6B2u4E81"
                target="_blank"
                rel="noopener noreferrer"
              >View on Google Maps</a>
            </div>
            <div class="text-caption q-mb-sm">Visit our store for self-pickup. Equipment is available at our Karyawangi branch.</div>
            <q-separator class="q-my-sm" />
            <div class="q-mt-sm" style="width:100%;height:240px;overflow:hidden;border-radius:12px;">
              <iframe
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d247.60451684904584!2d107.57977535754856!3d-6.809660242751447!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e68e17ed9f03a1b%3A0x46378751ba103981!2sKaryawangi!5e0!3m2!1sid!2sid!4v1776600509593!5m2!1sid!2sid"
                width="100%"
                height="100%"
                style="border:0;"
                allowfullscreen
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade"
              />
            </div>
          </q-card>
        </div>

      </div>
    </h-form>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Lang } from 'src/services/lang'
import { authStore } from 'src/stores/auth'
import { Config } from 'src/services/config'
import { Meta } from './meta'
import type { DataModel } from './meta'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const route = useRoute()
const router = useRouter()
const API = new Api()
const auth = authStore()

const loading = ref(true)
const dataModel = ref<DataModel>({ ...Meta.model })
const itemOptions = ref<any[]>([])

const isFutureDate = (date: string) => {
  const today = new Date()
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')
  return date >= `${year}/${month}/${day}`
}

// ─── Search filter dropdown item ────────────────────────────
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
const resolveSelectedLabel = (itemId: any): string => {
  const item = itemOptions.value.find((i) => String(i.id) === String(itemId))
  if (!item) return ''
  return `[${resolveItemCode(item)}] ${resolveItemName(item) ?? ''}`
}

const queryItemId = (() => {
  const raw = route.query?.item_id
  const value = Array.isArray(raw) ? raw[0] : raw
  const parsed = Number(value)
  return Number.isInteger(parsed) ? parsed : null
})()

const itemColumns = [
  { name: 'image', label: 'Photo', field: 'image', align: 'center' as const, style: 'width: 90px' },
  { name: 'item_id', label: 'Item', field: 'item_id', align: 'left' as const },
  { name: 'quantity', label: 'Qty', field: 'quantity', align: 'right' as const },
  { name: 'price_per_day', label: 'Price/Day', field: 'price_per_day', align: 'right' as const },
  { name: 'deposit_amount', label: 'Deposit', field: 'deposit_amount', align: 'right' as const },
  { name: 'subtotal', label: 'Subtotal', field: 'subtotal', align: 'right' as const },
  { name: 'action', label: '', field: 'id', align: 'center' as const, style: 'width: 40px' }
]

const resolveItemCode = (item: any) => item?.item_code ?? item?.code ?? item?.name ?? ''
const resolveItemName = (item: any) => item?.item_name ?? item?.name ?? item?.code ?? null

// Cache values to avoid repeated Lookups
const currentToken = ref('')
const currentBaseUrl = ref('')

const resolveImageUrl = (path: string, storage?: string | null): string | null => {
  if (!path) return null
  if (path.startsWith('http://') || path.startsWith('https://')) return path

  const token = currentToken.value
  const baseUrl = currentBaseUrl.value

  // Paths stored as rental/... crm/... static_files/... or STATIC storage → use static URL
  if (
    path.startsWith('rental/') ||
    path.startsWith('crm/') ||
    path.startsWith('static_files/') ||
    (storage && storage.toUpperCase().startsWith('STATIC'))
  ) {
    const encoded = path.split('/').map(encodeURIComponent).join('/')
    return `${baseUrl}static_files/${encoded}${token ? `?token=${token}` : ''}`
  }

  // Other cloud storage
  if (storage) {
    try {
      const url = (Helper as any).viewBlobFile(path, false, storage)
      return typeof url === 'string' ? url : null
    } catch {
      return null
    }
  }

  // Fallback: treat as static path
  const encoded = path.split('/').map(encodeURIComponent).join('/')
  return `${baseUrl}static_files/${encoded}${token ? `?token=${token}` : ''}`
}

const getFirstImageUrl = (raw: any): string | null => {
  if (!raw) return null
  if (typeof raw === 'string') return resolveImageUrl(raw)
  
  // Fast path for common object/array scenarios
  let first = null
  if (Array.isArray(raw)) {
    if (raw.length > 0) first = raw[0]
  } else if (typeof raw === 'object') {
    if ('path' in raw) return resolveImageUrl(raw.path, raw.storage ?? null)
    if ('url' in raw && raw.url) return raw.url
    const values = Object.values(raw)
    if (values.length > 0) first = values[0]
  }

  if (first) {
    if (typeof first === 'string') return resolveImageUrl(first)
    if (typeof first === 'object') {
       if ('path' in first) return resolveImageUrl(first.path, first.storage ?? null)
       if ('url' in first) return first.url
    }
  }

  return null
}

const resolveItemImage = (row: any): string | null => {
  // Compare as string to avoid number/string mismatch
  const found = itemOptions.value.find((i) => String(i.id) === String(row.item_id))
  if (!found) return null
  return getFirstImageUrl(found.images ?? found.image ?? found.image_url ?? found.photo)
}

const loadOptions = () => {
  API.get('master/items?limit=0', (status: number, data: any) => {
    if (status === 200) {
      itemOptions.value = data?.data ?? data
      if (queryItemId && (!dataModel.value.items || dataModel.value.items.length === 0)) {
        addItem(queryItemId)
      }
    }
  }, Meta.app)
}

const makeItem = () => ({
  uid: crypto.randomUUID(),
  item_id: null,
  item_code: null,
  item_name: null,
  quantity: 1,
  price_per_day: 0,
  deposit_amount: 0,
  subtotal: 0,
  max_available: null,
  has_clash: false,
  checking_availability: false,
})

const addItem = (itemId?: number | null) => {
  const item = makeItem()
  if (itemId) {
    const found = itemOptions.value.find((i) => i.id === itemId)
    if (found) {
      item.item_id = found.id
      item.item_code = resolveItemCode(found)
      item.item_name = resolveItemName(found)
      item.price_per_day = found.price_per_day ?? 0
      item.deposit_amount = found.deposit_amount ?? 0
    }
  }
  dataModel.value.items = [...(dataModel.value.items ?? []), item]
  if (itemId) {
    recalcLineItem(item)
    checkAvailability(item)
  }
}

const removeItem = (idx: number) => {
  dataModel.value.items?.splice(idx, 1)
  recalcTotals()
}

const onLineItemChange = (row: any, val: number) => {
  const found = itemOptions.value.find((i) => String(i.id) === String(val))
  if (found) {
    row.item_id       = found.id
    row.item_code     = resolveItemCode(found)
    row.item_name     = resolveItemName(found)
    row.price_per_day = found.price_per_day ?? 0
    row.deposit_amount = found.deposit_amount ?? 0
    recalcLineItem(row)
    checkAvailability(row)
  }
}

const onQuantityChange = (row: any, val: any) => {
  const quantity = Number(val)
  const newQty = Number.isFinite(quantity) && quantity > 0 ? quantity : 1
  if (Number(row.quantity) === newQty) return
  if (typeof row.max_available === 'number' && newQty > row.max_available) {
    $q.notify({ type: 'warning', message: `Maximum available stock is only ${row.max_available}` })
    row.quantity = row.max_available
    row.has_clash = row.max_available === 0
  } else {
    row.quantity = newQty
    row.has_clash = false
  }

  recalcLineItem(row)
}

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
            $q.notify({ type: 'negative', message: `Out of stock for [${row.item_code}] on selected dates.` })
            row.has_clash = true
          } else {
            $q.notify({ type: 'warning', message: `Auto-adjusted quantity for [${row.item_code}]: Remaining ${row.max_available}` })
            row.quantity = row.max_available
            row.has_clash = false
            recalcLineItem(row)
          }
        } else {
          row.has_clash = false
        }
      }
    }
  }, Meta.app)
}

const recalcLineItem = (row: any) => {
  const days = dataModel.value.duration_days ?? 1
  row.subtotal = (row.quantity ?? 0) * (row.price_per_day ?? 0) * days
  recalcTotals()
}

const recalcTotals = () => {
  const items = dataModel.value.items ?? []
  dataModel.value.subtotal = items.reduce((sum, i) => sum + (i.subtotal ?? 0), 0)
  dataModel.value.deposit_total = items.reduce((sum, i) => sum + ((i.deposit_amount ?? 0) * (i.quantity ?? 0)), 0)
  dataModel.value.grand_total = dataModel.value.subtotal + dataModel.value.deposit_total
}

const recalcDuration = () => {
  const s = dataModel.value.start_date
  const e = dataModel.value.end_date
  if (s && e) {
    const diff = Math.ceil((new Date(e).getTime() - new Date(s).getTime()) / (1000 * 60 * 60 * 24))
    dataModel.value.duration_days = diff >= 0 ? diff + 1 : 0
    // Recalculate ALL line items subtotal based on new duration
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

const formatCurrency = (val: number | null) =>
  new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(val ?? 0)

const validateSubmit = () => {
  if (!dataModel.value.start_date || !dataModel.value.end_date) {
    Helper.showNotif('Rental period is required.')
    return false
  }
  if (!dataModel.value.payment_method) {
    Helper.showNotif('Payment method is required.')
    return false
  }
  if (!dataModel.value.items || dataModel.value.items.length === 0) {
    Helper.showNotif('Please add items to rent.')
    return false
  }
  const invalidItem = dataModel.value.items.find((item: any) => !item.item_id || (item.quantity ?? 0) <= 0)
  if (invalidItem) {
    Helper.showNotif('Make sure all items are selected and the quantity is valid.')
    return false
  }
  if (dataModel.value.payment_method === 'transfer') {
    Helper.showToast('Transfer to BCA 083851071957 a.n. Nuristiana Izatul, then send the receipt to WA +62838-5107-1957.', 'info', 8000, 'top')
  }
  return true
}

const save = async () => {
  let statusapi = 600
  await API.post(Meta.apiModule || Meta.module, dataModel.value, (status: number, _data: any) => {
    statusapi = status
    if (_data?.id) dataModel.value.id = _data.id
    if (_data?.rental_code) dataModel.value.rental_code = _data.rental_code
  }, Meta.app)
  return statusapi
}

const submit = async () => {
  if (!validateSubmit()) return

  loading.value = true
  const status = await save()

  if (status === 200) {
    loading.value = false
    router.push({
      name: 'rental/user/rental-success',
      query: { 
        code: dataModel.value.rental_code ?? '',
        payment_method: dataModel.value.payment_method ?? '',
        grand_total: dataModel.value.grand_total ?? 0
      }
    })
    return
  }

  loading.value = false
}

const init = () => {
  dataModel.value = Helper.unreactive(Meta.model)
  const currentUser = auth.user || auth.getUser()
  if (currentUser) {
    dataModel.value.customer_id = currentUser.id
    dataModel.value.customer_name = currentUser.name ?? currentUser.username ?? ''
    dataModel.value.petugas_id = currentUser.id
    dataModel.value.petugas_name = currentUser.name ?? currentUser.username ?? ''
    dataModel.value.status = 'menunggu_bayar'
    
    // Cache values to avoid repeated Lookups
    currentToken.value = auth.getToken?.() ?? authStore().getToken() ?? ''
    currentBaseUrl.value = Config.apiUrl('rental')
    
    // Check if profile is complete
    API.get('me', (s: number, data: any) => {
      if (s === 200 && data) {
        if (!data.phone || !data.location || !data.profile_picture) {
          Helper.showToast('Please complete your profile details and upload your ID card first.', 'negative', 5000, 'top')
          router.push({ name: 'user-change-profile' })
          return
        }
      }
    }, 'identity')
  }
  loadOptions()
  Handler.permissions(router, 'browse', Meta, (status: boolean, data: any) => {
    Meta.permission = data
    loading.value = false
  })
}

const back = () => router.back()

onMounted(init)
</script>