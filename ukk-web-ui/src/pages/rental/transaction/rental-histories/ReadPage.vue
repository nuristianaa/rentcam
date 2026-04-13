<template>
  <div>
    <s-loading v-if="loading" />
    <h-detail v-else :meta="Meta" :model="dataModel" @back="back">

      <div class="row q-pa-sm q-col-gutter-sm">

        <!-- ─── Info Utama ───────────────────────────────────── -->
        <f-card title="Detail Rental" col="6">
          <!-- Status badge -->
          <div class="q-mb-sm">
            <q-badge
              :color="statusColor(dataModel.status)"
              :label="statusLabel(dataModel.status)"
              class="text-body2 q-pa-xs"
            />
          </div>
          <s-list v-for="(item, i) in viewList" :key="i" :data="item" />
        </f-card>

        <f-card title="Log" col="6">
          <log-info :data="dataModel" />
        </f-card>

        <!-- ─── Item Rental ──────────────────────────────────── -->
        <f-card title="Item Rental" col="12">
          <q-table
            :rows="dataModel.items ?? []"
            :columns="itemColumns"
            row-key="id"
            flat
            bordered
            dense
            hide-pagination
            :pagination="{ rowsPerPage: 0 }"
          >
            <!-- Kolom Gambar -->
            <template #body-cell-image="props">
              <q-td :props="props" class="text-center" style="width: 70px;">
                <q-img
                  v-if="resolveItemImage(props.row)"
                  :src="resolveItemImage(props.row)"
                  ratio="1"
                  fit="cover"
                  style="width: 50px; height: 50px; border-radius: 4px; border: 1px solid #ddd;"
                  spinner-color="primary"
                >
                  <template #error>
                    <div class="absolute-full flex flex-center bg-grey-3 text-grey-6 text-caption" style="font-size: 10px;">N/A</div>
                  </template>
                </q-img>
                <div
                  v-else
                  class="flex flex-center bg-grey-2 rounded-borders text-grey-5 mx-auto"
                  style="width: 50px; height: 50px; border: 1px solid #e0e0e0; border-radius: 4px;"
                >
                  <q-icon name="image_not_supported" size="20px" />
                </div>
              </q-td>
            </template>

            <template #body-cell-price_per_day="props">
              <q-td :props="props" class="text-right">{{ formatCurrency(props.row.price_per_day) }}</q-td>
            </template>
            <template #body-cell-deposit_amount="props">
              <q-td :props="props" class="text-right">{{ formatCurrency(props.row.deposit_amount) }}</q-td>
            </template>
            <template #body-cell-subtotal="props">
              <q-td :props="props" class="text-right">{{ formatCurrency(props.row.subtotal) }}</q-td>
            </template>
            <template #bottom-row>
              <q-tr class="bg-grey-2 text-weight-bold">
                <q-td colspan="4" class="text-right">Total</q-td>
                <q-td class="text-right">{{ formatCurrency(dataModel.deposit_total) }}</q-td>
                <q-td class="text-right">{{ formatCurrency(dataModel.subtotal) }}</q-td>
              </q-tr>
            </template>
          </q-table>
        </f-card>

        <!-- ─── Checkpoint ───────────────────────────────────── -->
        <f-card title="Checkpoint" col="12">
          <div class="row q-col-gutter-sm">

            <!-- Checkout -->
            <div class="col-12 col-md-6">
              <q-card flat bordered>
                <q-card-section class="bg-purple-1 q-py-sm">
                  <div class="row items-center q-gutter-xs">
                    <q-icon name="logout" color="purple" />
                    <span class="text-subtitle2 text-purple">Checkout</span>
                    <q-badge v-if="checkoutDone" color="purple" label="Selesai" class="q-ml-auto" />
                    <q-badge v-else color="grey" label="Belum" class="q-ml-auto" />
                  </div>
                </q-card-section>
                <q-card-section v-if="checkoutData">
                  <div class="q-gutter-xs">
                    <checkpoint-detail :data="checkoutData" />
                  </div>
                </q-card-section>
                <q-card-section v-else class="text-grey-5 text-caption">
                  Belum ada data checkout.
                </q-card-section>
              </q-card>
            </div>

            <!-- Checkin -->
            <div class="col-12 col-md-6">
              <q-card flat bordered>
                <q-card-section class="bg-teal-1 q-py-sm">
                  <div class="row items-center q-gutter-xs">
                    <q-icon name="login" color="teal" />
                    <span class="text-subtitle2 text-teal">Checkin</span>
                    <q-badge v-if="checkinDone" color="teal" label="Selesai" class="q-ml-auto" />
                    <q-badge v-else color="grey" label="Belum" class="q-ml-auto" />
                  </div>
                </q-card-section>
                <q-card-section v-if="checkinData">
                  <checkpoint-detail :data="checkinData" />
                </q-card-section>
                <q-card-section v-else class="text-grey-5 text-caption">
                  Belum ada data checkin.
                </q-card-section>
              </q-card>
            </div>

          </div>
        </f-card>

        <!-- ─── Pembayaran ─────────────────────────────────────── -->
        <f-card title="Pembayaran" col="12">
          <q-table
            :rows="dataModel.payments ?? []"
            :columns="paymentColumns"
            row-key="id"
            flat
            bordered
            dense
            hide-pagination
            :pagination="{ rowsPerPage: 0 }"
          >
            <template #body-cell-amount="props">
              <q-td :props="props" class="text-right">{{ formatCurrency(props.row.amount) }}</q-td>
            </template>
            <template #body-cell-paid_at="props">
              <q-td :props="props">{{ formatDatetime(props.row.paid_at) }}</q-td>
            </template>
            <template #body-cell-created_at="props">
              <q-td :props="props">{{ formatDatetime(props.row.created_at) }}</q-td>
            </template>
            <template #no-data>
              <div class="text-grey-5 text-caption q-pa-sm">Belum ada pembayaran.</div>
            </template>
          </q-table>
        </f-card>

        <!-- ─── Invoice ──────────────────────────────────────── -->
        <f-card title="Invoice" col="12">
          <q-table
             :rows="dataModel.invoices ?? []"
             :columns="invoiceColumns"
             row-key="id"
             flat
             bordered
             dense
             hide-pagination
             :pagination="{ rowsPerPage: 0 }"
           >
             <template #body-cell-grand_total="props">
               <q-td :props="props" class="text-right">{{ formatCurrency(props.row.grand_total) }}</q-td>
             </template>
             <template #body-cell-pdf_status="props">
               <q-td :props="props">
                 <q-badge
                   :color="pdfStatusColor(props.row.pdf_status)"
                   :label="pdfStatusLabel(props.row.pdf_status)"
                 />
               </q-td>
             </template>
             <template #body-cell-pdf_url="props">
               <q-td :props="props" class="text-center">
                 <div class="row no-wrap justify-center q-gutter-xs">
                   <q-btn
                     flat dense round
                     icon="visibility"
                     color="primary"
                     size="sm"
                     @click="openPdfPreview(props.row)"
                   >
                     <q-tooltip>Preview PDF</q-tooltip>
                   </q-btn>
                   <q-btn
                     flat dense round
                     icon="download"
                     color="red-7"
                     size="sm"
                     @click="downloadPdf(props.row)"
                   >
                     <q-tooltip>Download PDF</q-tooltip>
                   </q-btn>
                 </div>
               </q-td>
             </template>
             <template #no-data>
               <div class="text-grey-5 text-caption q-pa-sm">Belum ada invoice.</div>
             </template>
           </q-table>
        </f-card>

        <!-- ─── Riwayat Status ───────────────────────────────── -->
        <f-card title="Riwayat Status" col="12">
          <q-timeline color="primary" layout="dense">
            <q-timeline-entry
              v-for="(h, i) in dataModel.histories ?? []"
              :key="i"
              :subtitle="formatDatetime(h.created_at)"
              :color="statusColor(h.new_status)"
              :icon="historyIcon(h.event)"
            >
              <template #title>
                <span v-if="h.old_status" class="text-grey-6 text-caption">
                  {{ statusLabel(h.old_status) }} →
                </span>
                <q-badge
                  :color="statusColor(h.new_status)"
                  :label="statusLabel(h.new_status) || h.event"
                  class="q-ml-xs"
                />
                <span class="text-caption text-grey-6 q-ml-sm">[{{ h.event }}]</span>
              </template>
              <div class="text-caption text-grey-7">
                <q-icon name="person" size="12px" class="q-mr-xs" />
                {{ h.actor || '—' }}
              </div>
              <div v-if="h.notes" class="text-caption q-mt-xs">{{ h.notes }}</div>
            </q-timeline-entry>
            <div v-if="!dataModel.histories?.length" class="text-grey-5 text-caption q-pa-sm">
              Belum ada riwayat.
            </div>
          </q-timeline>
        </f-card>

      </div>
    </h-detail>
  </div>

    <!-- ─── Dialog: PDF Preview Invoice ──────────────────────── -->
    <q-dialog v-model="pdfPreviewDialog.show" @hide="closePdfPreview">
      <q-card class="column no-wrap" style="width: 860px; max-width: 96vw;">
        <q-card-section class="row items-center bg-red-8 text-white q-py-sm">
          <q-icon name="picture_as_pdf" class="q-mr-sm" />
          <span class="text-subtitle1 text-weight-medium">{{ pdfPreviewDialog.title }}</span>
          <q-space />
          <q-btn flat dense round icon="open_in_new" color="white" @click="openPdfInNewTab" v-if="pdfPreviewDialog.url" />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>
        <q-card-section class="q-pa-none">
          <iframe
            v-if="pdfPreviewDialog.show && pdfPreviewDialog.url"
            :src="pdfPreviewDialog.url"
            style="width: 100%; height: 80vh; border: none; display: block;"
            title="Preview Invoice"
          />
          <div v-else class="text-center q-pa-lg text-grey-6">
            Memuat preview invoice...
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, defineComponent, h } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Api from 'src/services/api'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Config } from 'src/services/config'
import { authStore } from 'src/stores/auth'
import { Meta } from './meta'

// ─── Inline helper component: CheckpointDetail ──────────────
const CheckpointDetail = defineComponent({
  props: { data: Object },
  setup(props) {
    const fmt = (v: string | null) => v
      ? new Date(v).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
      : '—'

    const condLabel: Record<string, string> = {
      baik: 'Baik', cacat_ringan: 'Cacat Ringan', rusak: 'Rusak', hilang: 'Hilang',
    }
    const condColor: Record<string, string> = {
      baik: 'positive', cacat_ringan: 'warning', rusak: 'negative', hilang: 'red-9',
    }

    return () => {
      const d = props.data as any
      if (!d) return null
      return h('div', { class: 'q-gutter-xs' }, [
        h('div', { class: 'text-caption text-grey-7' }, [
          h('span', { class: 'text-weight-medium' }, 'Waktu: '),
          fmt(d.actual_at),
        ]),
        d.condition
          ? h('div', { class: 'q-mt-xs' }, [
              h('span', { class: 'text-caption text-grey-7 text-weight-medium' }, 'Kondisi: '),
              h('q-badge', { color: condColor[d.condition] ?? 'grey', label: condLabel[d.condition] ?? d.condition }),
            ])
          : null,
        d.condition_notes
          ? h('div', { class: 'text-caption q-mt-xs' }, [
              h('span', { class: 'text-weight-medium' }, 'Ket. Kondisi: '),
              d.condition_notes,
            ])
          : null,
        d.officer_name
          ? h('div', { class: 'text-caption q-mt-xs' }, [
              h('span', { class: 'text-weight-medium' }, 'Petugas: '),
              d.officer_name,
            ])
          : null,
        d.notes
          ? h('div', { class: 'text-caption q-mt-xs' }, [
              h('span', { class: 'text-weight-medium' }, 'Catatan: '),
              d.notes,
            ])
          : null,
        d.checklist?.length
          ? h('div', { class: 'q-mt-sm' }, [
              h('div', { class: 'text-caption text-weight-medium text-grey-7' }, 'Checklist:'),
              ...(d.checklist as any[]).map(cl =>
                h('div', { class: 'row items-center q-gutter-xs q-mt-xs' }, [
                  h('q-icon', {
                    name: cl.ok ? 'check_circle' : 'cancel',
                    color: cl.ok ? 'positive' : 'negative',
                    size: '14px',
                  }),
                  h('span', { class: 'text-caption' }, cl.label ?? ''),
                  cl.note ? h('span', { class: 'text-caption text-grey-6' }, `(${cl.note})`) : null,
                ])
              ),
            ])
          : null,
      ])
    }
  },
})

// ─── Setup ──────────────────────────────────────────────────
const route = useRoute()
const router = useRouter()
const id = Array.isArray(route.params?.id) ? route.params.id[0] : (route.params?.id ?? null)
const API = new Api()
const auth = authStore()

const loading = ref(true)
const dataModel = ref<any>({})
const viewList = ref<{ label: string; value: any }[]>([])

// ─── PDF Preview Dialog ──────────────────────────────────────
const pdfPreviewDialog = ref({ show: false, url: '', title: '' })
const pdfObjectUrl = ref<string | null>(null)

const closePdfPreview = () => {
  if (pdfObjectUrl.value) {
    URL.revokeObjectURL(pdfObjectUrl.value)
    pdfObjectUrl.value = null
  }
  pdfPreviewDialog.value.show = false
}

const fetchPdfBlob = async (invoiceId: string, endpoint: 'preview-pdf' | 'download-pdf'): Promise<Blob | null> => {
  try {
    const store   = authStore()
    const token   = store.token
    const baseUrl = (Config.api_url || (process.env.API_URL as string) || '').replace(/\/$/, '')
    const url     = baseUrl
      ? `${baseUrl}/v1/transaction/rental-invoices/${invoiceId}/${endpoint}`
      : `/v1/transaction/rental-invoices/${invoiceId}/${endpoint}`
    const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } })
    if (!res.ok) return null
    return await res.blob()
  } catch {
    return null
  }
}

const openPdfPreview = async (invoice: any) => {
  pdfPreviewDialog.value = { show: true, url: '', title: invoice.invoice_code ?? 'Invoice' }
  const blob = await fetchPdfBlob(invoice.id, 'preview-pdf')
  if (!blob) {
    Helper.showError('Gagal membuka preview invoice.')
    pdfPreviewDialog.value.show = false
    return
  }
  if (pdfObjectUrl.value) URL.revokeObjectURL(pdfObjectUrl.value)
  const url = URL.createObjectURL(blob)
  pdfObjectUrl.value = url
  pdfPreviewDialog.value.url = url
}

const openPdfInNewTab = () => {
  if (!pdfPreviewDialog.value.url) return
  window.open(pdfPreviewDialog.value.url, '_blank')
}

const downloadPdf = async (invoice: any) => {
  const blob = await fetchPdfBlob(invoice.id, 'download-pdf')
  if (!blob) {
    Helper.showError('Gagal mengunduh invoice.')
    return
  }
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${invoice.invoice_code ?? 'invoice'}.pdf`
  a.click()
  URL.revokeObjectURL(url)
}

// ─── Status helpers ──────────────────────────────────────────
const STATUS_COLOR: Record<string, string> = {
  menunggu_bayar: 'orange', menunggu_verif: 'blue',
  diproses: 'purple', aktif: 'green', selesai: 'teal', dibatalkan: 'red',
}
const STATUS_LABEL: Record<string, string> = {
  menunggu_bayar: 'Menunggu Bayar', menunggu_verif: 'Menunggu Verifikasi',
  diproses: 'Diproses', aktif: 'Aktif', selesai: 'Selesai', dibatalkan: 'Dibatalkan',
}
const statusColor = (val: string | null) => STATUS_COLOR[val ?? ''] ?? 'grey'
const statusLabel = (val: string | null) => STATUS_LABEL[val ?? ''] ?? (val || '—')

const historyIcon = (event: string) => {
  const map: Record<string, string> = {
    status_changed: 'swap_horiz',
    checkout:       'logout',
    checkin:        'login',
    invoice_generated: 'receipt_long',
  }
  return map[event] ?? 'fiber_manual_record'
}

const pdfStatusColor = (s: string) =>
  ({ pending: 'orange', generated: 'positive', failed: 'negative' }[s] ?? 'grey')
const pdfStatusLabel = (s: string) =>
  ({ pending: 'Pending', generated: 'Selesai', failed: 'Gagal' }[s] ?? s)

// ─── Computed: checkpoint state ──────────────────────────────
const checkoutData = computed(() =>
  (dataModel.value.checkpoints ?? []).find((c: any) => c.type === 'checkout') ?? null
)
const checkinData = computed(() =>
  (dataModel.value.checkpoints ?? []).find((c: any) => c.type === 'checkin') ?? null
)
const checkoutDone = computed(() => !!checkoutData.value)
const checkinDone  = computed(() => !!checkinData.value)

// ─── Format helpers ──────────────────────────────────────────
const formatCurrency = (val: number | null) =>
  new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(val ?? 0)

const formatDatetime = (val: string | null) =>
  val ? new Date(val).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' }) : '—'

// Image helper function for items
const resolveImageUrl = (path: string, storage?: string | null): string | null => {
  if (!path) return null
  if (path.startsWith('http://') || path.startsWith('https://')) return path

  const token = auth.getToken?.() ?? auth.getToken()
  const baseUrl = Config.apiUrl('rental')

  if (
    path.startsWith('rental/') ||
    path.startsWith('crm/') ||
    path.startsWith('static_files/') ||
    (storage && storage.toUpperCase().startsWith('STATIC'))
  ) {
    const encoded = path.split('/').map(encodeURIComponent).join('/')
    return `${baseUrl}static_files/${encoded}${token ? `?token=${token}` : ''}`
  }

  if (storage) {
    try {
      const url = (Helper as any).viewBlobFile(path, false, storage)
      return typeof url === 'string' ? url : null
    } catch {
      return null
    }
  }

  const encoded = path.split('/').map(encodeURIComponent).join('/')
  return `${baseUrl}static_files/${encoded}${token ? `?token=${token}` : ''}`
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
    if ('url' in raw && raw.url) return raw.url
    return getFirstImageUrl(Object.values(raw))
  }
  return null
}

const resolveItemImage = (row: any): string | null => {
  const rawData = row.item?.images ?? row.item?.image ?? row.item?.image_url ?? row.item?.photo ?? row.images ?? row.image_url
  return getFirstImageUrl(rawData)
}

// ─── Table columns ───────────────────────────────────────────
const itemColumns = [
  { name: 'image',          label: 'Foto',       field: 'image',          align: 'center' as const, style: 'width: 70px' },
  { name: 'item_name',      label: 'Item',       field: 'item_name',      align: 'left'  as const },
  { name: 'quantity',       label: 'Qty',        field: 'quantity',       align: 'right' as const },
  { name: 'price_per_day',  label: 'Harga/Hari', field: 'price_per_day',  align: 'right' as const },
  { name: 'deposit_amount', label: 'Deposit',    field: 'deposit_amount', align: 'right' as const },
  { name: 'subtotal',       label: 'Subtotal',   field: 'subtotal',       align: 'right' as const },
]

const paymentColumns = [
  { name: 'type',           label: 'Tipe',            field: 'type',           align: 'left'   as const },
  { name: 'status',         label: 'Status',          field: 'status',         align: 'left'   as const },
  { name: 'amount',         label: 'Jumlah',          field: 'amount',         align: 'right'  as const },
  { name: 'payment_method', label: 'Metode',          field: 'payment_method', align: 'left'   as const },
  { name: 'bank_name',      label: 'Bank',            field: 'bank_name',      align: 'left'   as const },
  { name: 'account_number', label: 'No. Rekening',    field: 'account_number', align: 'left'   as const },
  { name: 'paid_at',        label: 'Tgl Bayar',       field: 'paid_at',        align: 'left'   as const },
  { name: 'created_at',     label: 'Dibuat',          field: 'created_at',     align: 'left'   as const },
]

const invoiceColumns = [
  { name: 'invoice_code',   label: 'Kode Invoice', field: 'invoice_code',  align: 'left'   as const },
  { name: 'type',           label: 'Tipe',         field: 'type',          align: 'left'   as const },
  { name: 'grand_total',    label: 'Total',        field: 'grand_total',   align: 'right'  as const },
  { name: 'payment_method', label: 'Metode',       field: 'payment_method',align: 'left'   as const },
  { name: 'pdf_status',     label: 'Status PDF',   field: 'pdf_status',    align: 'left'   as const },
  { name: 'pdf_url',        label: 'Aksi PDF',     field: 'pdf_url',       align: 'center' as const },
]

// ─── Init & Load ─────────────────────────────────────────────
const loadInvoices = (rentalId: string) => {
  API.get(`transaction/rental-invoices/by-rental/${rentalId}`, (status: number, data: any) => {
    if (status === 200) {
      const invoices = data?.data ?? data ?? []
      dataModel.value = { ...dataModel.value, invoices: Array.isArray(invoices) ? invoices : [] }
    }
  })
}

const getData = (id?: string | number) => {
  if (!id) return (loading.value = false)

  API.get(`${Meta.apiModule ?? Meta.module}/${id}`, (status: number, data: any) => {
    if (status === 200) {
      const payload = data?.data ?? data ?? {}
      
      // Standarisasi items format
      payload.items = payload.items ?? payload.rental_items ?? payload.details ?? payload.line_items ?? payload.rentalItems ?? []
      payload.items = payload.items.map((item: any) => ({
        ...item,
        item_name: item.item_name ?? item.item?.name ?? item.item?.item_name ?? item.name ?? '-',
      }))

      dataModel.value = { ...payload }
      const config = {
        exclude: [
          'id', 'images', 'items', 'histories', 'checkpoints', 'invoices',
          'created_by', 'updated_by', 'deleted_by',
          'created_at', 'updated_at', 'deleted_at',
        ],
        numbers: ['duration_days'],
        moneys:  ['subtotal', 'deposit_total', 'grand_total'],
        date:    ['start_date', 'end_date'],
        dateTime: [],
      }
      viewList.value = Handler.viewList(dataModel.value, config)
      if (payload.id) loadInvoices(String(payload.id))
    }
    loading.value = false
  })
}

const back = () => { router.back() }

onMounted(() => {
  dataModel.value = Helper.unreactive(Meta.model)
  // Untuk read, kita cukup cek permission read
  Handler.permissions(router, 'read', Meta, (status) => {
    if (status) getData(id)
    else loading.value = false
  })
})
</script>