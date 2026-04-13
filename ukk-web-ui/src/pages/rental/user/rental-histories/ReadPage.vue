<template>
  <div class="q-pa-md">
    <s-loading v-if="loading" />

    <template v-else>
      <q-dialog v-if="!isReviewed(selectedItem)" v-model="reviewDialog" persistent>
        <q-card style="min-width: 350px">
          <q-card-section>
            <div class="text-h6">Beri Review untuk {{ selectedItem?.item_name }}</div>
          </q-card-section>
          <q-card-section class="q-pt-none">
            <div class="q-mb-md">
              <div class="text-subtitle2 q-mb-xs">Rating</div>
              <q-rating v-model="reviewForm.rating" max="5" size="2em" color="warning" icon="star_border" icon-selected="star" />
            </div>
            <q-input v-model="reviewForm.comment" type="textarea" label="Komentar" outlined dense />
          </q-card-section>
          <q-card-actions align="right">
            <q-btn flat label="Batal" color="primary" v-close-popup />
            <q-btn flat label="Simpan Review" color="primary" @click="submitReview" />
          </q-card-actions>
        </q-card>
      </q-dialog>
      <!-- Header -->
      <div class="row items-center q-mb-md">
        <q-btn
          flat
          round
          dense
          icon="arrow_back"
          class="q-mr-sm"
          @click="back"
        />
        <div class="col">
          <div class="text-h6 text-weight-bold">Detail Booking</div>
          <div class="text-caption text-grey-6">{{ dataModel.rental_code ?? '-' }}</div>
        </div>
        <div class="col-auto">
          <q-badge
            :color="Meta.statusColor[dataModel.status ?? ''] ?? 'grey'"
            :label="resolveStatusLabel(dataModel.status)"
            class="q-py-sm q-px-md text-body2"
          />
        </div>
      </div>

      <!-- Info Booking -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="text-subtitle2 text-weight-bold q-mb-sm">
            <q-icon name="info" class="q-mr-xs" /> Informasi Booking
          </div>

          <div class="row q-col-gutter-sm">
            <div class="col-6 col-sm-3">
              <div class="text-caption text-grey-6">Kode Booking</div>
              <div class="text-body2 text-weight-medium">{{ dataModel.rental_code ?? '-' }}</div>
            </div>
            <div class="col-6 col-sm-3">
              <div class="text-caption text-grey-6">Nama Pelanggan</div>
              <div class="text-body2 text-weight-medium">{{ dataModel.customer_name ?? '-' }}</div>
            </div>
            <div class="col-6 col-sm-3">
              <div class="text-caption text-grey-6">Metode Pembayaran</div>
              <div class="text-body2 text-weight-medium">
                <q-icon
                  :name="dataModel.payment_method === 'transfer' ? 'account_balance' : 'payments'"
                  size="14px"
                  class="q-mr-xs"
                />
                {{ resolvePaymentLabel(dataModel.payment_method) }}
              </div>
            </div>
            <div class="col-6 col-sm-3">
              <div class="text-caption text-grey-6">Status</div>
              <div class="text-body2 text-weight-medium">
                <q-badge
                  :color="Meta.statusColor[dataModel.status ?? ''] ?? 'grey'"
                  :label="resolveStatusLabel(dataModel.status)"
                />
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="text-subtitle2 text-weight-bold q-mb-sm">
            <q-icon name="place" class="q-mr-xs" /> Lokasi Toko
          </div>
          <div class="text-caption q-mb-xs">
            📍 Jl. Cihampelas No. 123, Bandung, Jawa Barat
          </div>
          <div class="text-caption q-mb-sm">
            <a
              class="text-blue text-weight-bold"
              href="https://www.google.com/maps/search/?api=1&query=Jl.+Cihampelas+No.+123,+Bandung,+Jawa+Barat"
              target="_blank"
              rel="noopener noreferrer"
            >Lihat di Google Maps</a>
          </div>
          <div class="text-caption q-mb-sm">
            Kunjungi toko kami untuk mengambil alat secara langsung. Review hanya bisa dikirim setelah status transaksi selesai.
          </div>
          <q-separator class="q-my-sm" />
          <div class="q-mt-sm" style="width:100%;height:240px;overflow:hidden;border-radius:12px;">
            <iframe
              title="Preview Google Maps"
              width="100%"
              height="100%"
              frameborder="0"
              style="border:0;"
              loading="lazy"
              src="https://www.google.com/maps?q=Jl.+Cihampelas+No.+123,+Bandung,+Jawa+Barat&output=embed"
            ></iframe>
          </div>
        </q-card-section>
      </q-card>

      <!-- Info Periode -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="text-subtitle2 text-weight-bold q-mb-sm">
            <q-icon name="calendar_today" class="q-mr-xs" /> Periode Sewa
          </div>

          <div class="row q-col-gutter-sm">
            <div class="col-6 col-sm-4">
              <div class="text-caption text-grey-6">Tanggal Mulai</div>
              <div class="text-body2 text-weight-medium">{{ dataModel.start_date ?? '-' }}</div>
            </div>
            <div class="col-6 col-sm-4">
              <div class="text-caption text-grey-6">Tanggal Selesai</div>
              <div class="text-body2 text-weight-medium">{{ dataModel.end_date ?? '-' }}</div>
            </div>
            <div class="col-6 col-sm-4">
              <div class="text-caption text-grey-6">Durasi</div>
              <div class="text-body2 text-weight-medium">{{ dataModel.duration_days ?? '-' }} hari</div>
            </div>
          </div>

          <div v-if="dataModel.notes" class="q-mt-sm">
            <div class="text-caption text-grey-6">Catatan</div>
            <div class="text-body2">{{ dataModel.notes }}</div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Tabel Item -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="text-subtitle2 text-weight-bold q-mb-sm">
            <q-icon name="list_alt" class="q-mr-xs" /> Item yang Disewa
          </div>

          <q-table
            :rows="dataModel.items ?? []"
            :columns="itemColumns"
            row-key="id"
            flat
            dense
            hide-pagination
            :pagination="{ rowsPerPage: 0 }"
            no-data-label="Tidak ada item."
          >
            <template #body-cell-price_per_day="props">
              <q-td :props="props" class="text-right">
                {{ formatCurrency(props.row.price_per_day) }}
              </q-td>
            </template>
            <template #body-cell-deposit_amount="props">
              <q-td :props="props" class="text-right">
                {{ formatCurrency(props.row.deposit_amount) }}
              </q-td>
            </template>
            <template #body-cell-subtotal="props">
              <q-td :props="props" class="text-right">
                {{ formatCurrency(props.row.subtotal) }}
              </q-td>
            </template>
            <template #body-cell-action="props">
              <q-td :props="props" class="text-center">
                <div v-if="isReviewed(props.row)" class="column items-center">
                  <q-rating :model-value="getReviewForRow(props.row)?.rating ?? 0" max="5" size="1.2em" color="amber" readonly />
                  <div class="text-caption text-grey-8 ellipsis q-mb-sm" style="max-width: 150px; margin-top: 4px;" v-if="getReviewForRow(props.row)?.comment">
                    "{{ getReviewForRow(props.row)?.comment }}"
                  </div>
                  <q-btn
                    size="sm"
                    color="positive"
                    text-color="white"
                    label="Telah di-review"
                    disable
                  />
                </div>
                <q-btn
                  v-else
                  size="sm"
                  :color="dataModel.status === 'selesai' ? 'primary' : 'grey-5'"
                  :text-color="dataModel.status === 'selesai' ? 'white' : 'black'"
                  :label="dataModel.status === 'selesai' ? 'Beri Review' : 'Review akan aktif setelah selesai'"
                  :disable="dataModel.status !== 'selesai'"
                  @click="dataModel.status === 'selesai' ? openReviewDialog(props.row) : undefined"
                />
              </q-td>
            </template>

            <template #bottom-row>
              <q-tr class="bg-grey-2 text-weight-bold">
                <q-td colspan="3" class="text-right">Total</q-td>
                <q-td class="text-right">{{ formatCurrency(dataModel.deposit_total) }}</q-td>
                <q-td class="text-right">{{ formatCurrency(dataModel.subtotal) }}</q-td>
                <q-td></q-td>
              </q-tr>
            </template>
          </q-table>
        </q-card-section>
      </q-card>



      <!-- Tracking Status -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="text-subtitle2 text-weight-bold q-mb-md">
            <q-icon name="timeline" class="q-mr-xs" /> Tracking & Log Pemeriksaan
          </div>
          
          <q-timeline layout="dense" color="primary" class="q-px-sm" v-if="checkpoints.length > 0 || dataModel.status">
            <q-timeline-entry icon="shopping_cart_checkout" title="Booking Dibuat" :subtitle="dataModel.created_at ? new Date(dataModel.created_at).toLocaleString('id-ID') : '...'" />
            <q-timeline-entry v-if="dataModel.status !== 'menunggu_bayar'" icon="account_balance_wallet" title="Pembayaran Terselesaikan" color="positive" />
            
            <q-timeline-entry
              v-for="cp in checkpoints"
              :key="cp.id"
              :title="cp.type === 'OUT' ? 'Alat Diserahkan ke Penyewa' : (cp.type === 'IN' ? 'Alat Dikembalikan & Diperiksa' : cp.type)"
              :subtitle="cp.actual_at ? new Date(cp.actual_at).toLocaleString('id-ID') : '...'"
              :color="cp.type === 'OUT' ? 'info' : 'positive'"
              :icon="cp.type === 'OUT' ? 'outbox' : 'fact_check'"
            >
              <div class="text-body2 text-grey-8">Kondisi: <strong>{{ cp.condition || '-' }}</strong></div>
              <div v-if="cp.condition_notes" class="text-caption text-grey-6">Catatan: {{ cp.condition_notes }}</div>
              <div class="text-caption text-grey-6">Petugas: {{ cp.officer_name || '-' }}</div>
            </q-timeline-entry>
            
            <q-timeline-entry v-if="dataModel.status === 'selesai'" title="Selesai" subtitle="Transaksi telah ditutup" icon="check_circle" color="green" />
            <q-timeline-entry v-if="dataModel.status === 'batal'" title="Dibatalkan" subtitle="Transaksi dibatalkan" icon="cancel" color="negative" />
          </q-timeline>
          <div v-else class="text-caption text-grey-6 q-pa-md text-center">
            Belum ada log tracking.
          </div>
        </q-card-section>
      </q-card>

      <!-- Ringkasan Biaya -->
      <q-card flat bordered class="q-mb-md bg-grey-1">
        <q-card-section>
          <div class="text-subtitle2 text-weight-bold q-mb-md">
            <q-icon name="receipt_long" class="q-mr-xs" /> Rincian Pembayaran
          </div>

          <div class="column q-gutter-y-sm text-body2">
            <div class="row justify-between">
              <span class="text-grey-8">Subtotal Sewa</span>
              <span class="text-weight-medium">{{ formatCurrency(dataModel.subtotal) }}</span>
            </div>
            <div class="row justify-between">
              <span class="text-grey-8">Desposit Jaminan</span>
              <span class="text-weight-medium">{{ formatCurrency(dataModel.deposit_total) }}</span>
            </div>
            
            <q-separator class="q-my-sm" color="grey-4" />
            
            <div class="row justify-between text-subtitle1 text-weight-bold text-primary">
              <span>Grand Total</span>
              <span>{{ formatCurrency(dataModel.grand_total) }}</span>
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Info transfer -->
      <q-banner
        v-if="dataModel.payment_method === 'transfer' && dataModel.status === 'menunggu_bayar'"
        rounded
        class="bg-blue-2 text-blue-10 q-mb-md"
      >
        <template #avatar>
          <q-icon name="info" color="blue-7" size="24px" />
        </template>
        <div class="text-caption text-weight-bold q-mb-xs">Instruksi Pembayaran Transfer</div>
        <div class="text-caption q-mb-xs">
          Silakan transfer ke rekening berikut, lalu kirim bukti transfer via WhatsApp:
        </div>
        <div class="text-caption q-mb-xs">
          🏦 <b>Bank BCA</b> — No. Rek: <b>1234567890</b> a.n. <b>Admin Rental Kamera</b>
        </div>
        <div class="text-caption">
          📱 WhatsApp Admin:
          <a
            :href="`https://wa.me/6281234567890?text=Halo Admin, saya ${dataModel.customer_name ?? ''} ingin mengirim bukti transfer untuk booking ${dataModel.rental_code ?? ''}.`"
            target="_blank"
            class="text-blue-10 text-weight-bold"
          >0812-3456-7890</a>
        </div>
      </q-banner>
    </template>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { Meta } from './meta'
import type { DataModel } from './meta'

const route  = useRoute()
const router = useRouter()
const API    = new Api()
const $q     = useQuasar()

// ─── State ────────────────────────────────────────────────────────────────────
const loading   = ref(true)
const dataModel = ref<DataModel>({ ...Meta.model })
const reviews = ref<any[]>([])
const checkpoints = ref<any[]>([])
const reviewDialog = ref(false)
const selectedItem = ref<any>(null)
const reviewForm = ref({ rating: 5, comment: '' })

// ─── Columns ──────────────────────────────────────────────────────────────────
const itemColumns = [
  { name: 'item_name',     label: 'Nama Item',  field: 'item_name',     align: 'left' as const },
  { name: 'quantity',      label: 'Qty',        field: 'quantity',      align: 'center' as const },
  { name: 'price_per_day', label: 'Harga/Hari', field: 'price_per_day', align: 'right' as const },
  { name: 'deposit_amount',label: 'Deposit',    field: 'deposit_amount',align: 'right' as const },
  { name: 'subtotal',      label: 'Subtotal',   field: 'subtotal',      align: 'right' as const },
  { name: 'action',        label: 'Aksi',       field: 'action',        align: 'center' as const },
]

// ─── Helpers ──────────────────────────────────────────────────────────────────
const resolveStatusLabel = (val: string | null) =>
  Meta.statusOptions.find((o) => o.value === val)?.label ?? val ?? '-'

const resolvePaymentLabel = (val: string | null) =>
  Meta.paymentMethodOptions.find((o) => o.value === val)?.label ?? val ?? '-'

const formatCurrency = (val: number | null) =>
  new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(val ?? 0)

const isReviewed = (row: any) => {
  const targetId = row?.item_id || row?.id
  if (!targetId) return false
  return reviews.value.some(r => String(r.item_id) === String(targetId))
}

const getReviewForRow = (row: any) => {
  const targetId = row?.item_id || row?.id
  if (!targetId) return null
  return reviews.value.find(r => String(r.item_id) === String(targetId))
}



const openReviewDialog = (row: any) => {
  if (isReviewed(row)) {
    return
  }
  selectedItem.value = row
  reviewForm.value = { rating: 5, comment: '' }
  reviewDialog.value = true
}

const submitReview = () => {
  if (!selectedItem.value) return
  const payload = {
    rental_id: dataModel.value.id,
    item_id: selectedItem.value.item_id || selectedItem.value.id,
    rating: reviewForm.value.rating,
    comment: reviewForm.value.comment,
  }
  API.post(`transaction/reviews`, payload, (status: number, data: any) => {
    if (status === 200 || status === 201) {
      $q.notify({ type: 'positive', message: 'Review berhasil disimpan' })
      reviewDialog.value = false
      loadData()
    } else {
      $q.notify({ type: 'negative', message: data?.message || 'Gagal menyimpan review' })
    }
  }, Meta.app)
}

const loadCheckpoints = (rentalId: string) => {
  if (!rentalId) return
  API.get(`transaction/rental-checkpoints/by-rental/${rentalId}`, (status: number, data: any) => {
    if (status === 200) {
      checkpoints.value = data?.data || []
    }
  }, Meta.app)
}

// ─── Fetch Data ───────────────────────────────────────────────────────────────
const loadData = () => {
  const rawId = route.params.id
  const id = Array.isArray(rawId) ? rawId[0] : rawId
  if (!id) {
    loading.value = false
    return
  }

  // GET transaction/rentals/{id}
  API.get(
    `${Meta.apiModule}/${id}`,
    (status: number, data: any) => {
      if (status === 200) {
        const raw = data?.data ?? data

        // Normalize items — coba semua kemungkinan key dari backend
        raw.items =
          raw.items ??
          raw.rental_items ??
          raw.details ??
          raw.line_items ??
          raw.rentalItems ??
          []

        // Normalize customer_name — bisa flat string atau nested object
        raw.customer_name =
          raw.customer_name ??
          raw.customer?.name ??
          raw.customer?.username ??
          null

        // Normalize petugas_name
        raw.petugas_name =
          raw.petugas_name ??
          raw.petugas?.name ??
          raw.petugas?.username ??
          null

        // Normalize item_name di setiap baris item
        raw.items = raw.items.map((item: any) => ({
          ...item,
          item_name:
            item.item_name ??
            item.item?.name ??
            item.item?.item_name ??
            item.name ??
            '-',
        }))

        dataModel.value = raw
        reviews.value = raw.reviews ?? []
        if (raw.id) {
          loadCheckpoints(raw.id)
        }
      }
      loading.value = false
    },
    Meta.app
  )
}

// ─── Navigation ───────────────────────────────────────────────────────────────
const back = () => router.back()

// ─── Init ─────────────────────────────────────────────────────────────────────
onMounted(loadData)
</script>