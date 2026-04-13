<template>
  <s-page :meta="Meta">

    <!-- Report Type Tabs -->
    <q-tabs
      v-model="activeTab"
      dense
      class="text-grey q-mb-md border-bottom"
      active-color="primary"
      indicator-color="primary"
      align="left"
      narrow-indicator
    >
      <q-tab name="transaksi" icon="receipt_long" label="Transaksi & Pendapatan" />
      <q-tab name="items" icon="inventory_2" label="Penyewaan Alat" />
      <q-tab name="denda" icon="gavel" label="Keterlambatan & Denda" />
    </q-tabs>

    <q-tab-panels v-model="activeTab" animated class="bg-transparent no-padding">
      <!-- PANEL TRANSAKSI & PENDAPATAN -->
      <q-tab-panel name="transaksi" class="no-padding">
        <!-- Filters Section -->
        <f-card title="Laporan Transaksi Rental" col="12" class="no-print q-mb-md">
          <div class="row q-col-gutter-sm items-center">
            <div class="col-12 col-md-3">
              <q-input v-model="filters.startDate" type="date" label="Tanggal Mulai" outlined dense />
            </div>
            <div class="col-12 col-md-3">
              <q-input v-model="filters.endDate" type="date" label="Tanggal Akhir" outlined dense />
            </div>
            <div class="col-12 col-md-3">
              <q-select 
                v-model="filters.status" 
                :options="Meta.statusOptions" 
                label="Status Transaksi" 
                outlined 
                dense 
                emit-value 
                map-options 
              />
            </div>
            <div class="col-12 col-md-3">
              <q-btn color="primary" label="Terapkan" icon="filter_alt" @click="fetchData" unelevated class="full-width" />
            </div>
          </div>
        </f-card>

        <s-loading v-if="loading" />
        <template v-else>
          <!-- Summary / Info Board -->
          <div class="row q-col-gutter-sm q-mb-md no-print">
            <div class="col-12 col-sm-4">
              <q-card flat bordered class="bg-grey-2">
                <q-card-section>
                  <div class="text-caption text-grey-8 uppercase">Total Transaksi</div>
                  <div class="text-h5 text-bold text-primary">{{ totalTransactions }}</div>
                </q-card-section>
              </q-card>
            </div>
            <div class="col-12 col-sm-4">
              <q-card flat bordered class="bg-grey-2">
                <q-card-section>
                  <div class="text-caption text-grey-8 uppercase">Total Pendapatan Aktual (Selesai/Aktif)</div>
                  <div class="text-h5 text-bold text-green">{{ formatCurrency(totalRevenue) }}</div>
                </q-card-section>
              </q-card>
            </div>
            <div class="col-12 col-sm-4">
              <q-card flat bordered class="bg-grey-2">
                <q-card-section>
                  <div class="text-caption text-grey-8 uppercase">Transaksi Dibatalkan</div>
                  <div class="text-h5 text-bold text-red">{{ totalCanceled }}</div>
                </q-card-section>
              </q-card>
            </div>
          </div>

          <!-- Report Table & Export -->
          <f-card col="12" class="no-print">
            <r-table
              :columns="columns"
              v-model="data"
              row-key="id"
            >
              <template v-slot:top-right>
                <q-btn color="primary" outline label="Cetak Dokumen" icon="print" @click="printPage" />
              </template>
            </r-table>
          </f-card>
        </template>
      </q-tab-panel>

      <!-- PANEL PENYEWAAN ALAT -->
      <q-tab-panel name="items" class="no-padding">
        <f-card title="Filter Laporan Penyewaan Alat" col="12" class="no-print q-mb-md">
          <div class="row q-col-gutter-sm items-center">
            <div class="col-12 col-md-3">
              <q-input v-model="filters.startDate" type="date" label="Tanggal Mulai" outlined dense />
            </div>
            <div class="col-12 col-md-3">
              <q-input v-model="filters.endDate" type="date" label="Tanggal Akhir" outlined dense />
            </div>
            <div class="col-12 col-md-4">
              <q-select 
                v-model="filters.status" 
                :options="Meta.statusOptions" 
                label="Status Transaksi" 
                outlined 
                dense 
                emit-value 
                map-options 
              />
            </div>
            <div class="col-12 col-md-2">
              <q-btn color="primary" label="Terapkan" icon="filter_alt" @click="fetchData" unelevated class="full-width" />
            </div>
          </div>
        </f-card>

        <s-loading v-if="loadingItems" />
        <template v-else>
          <div class="row q-col-gutter-sm q-mb-md no-print">
            <div class="col-12 col-md-6">
              <q-card flat bordered class="bg-blue-1 text-primary">
                <q-card-section>
                  <div class="text-caption text-uppercase">Total Item Disewa (Pcs)</div>
                  <div class="text-h5 text-bold">{{ totalItemsRented }}</div>
                </q-card-section>
              </q-card>
            </div>
            <div class="col-12 col-md-6">
              <q-card flat bordered class="bg-blue-1 text-primary">
                <q-card-section>
                  <div class="text-caption text-uppercase">Total Pendapatan Alat</div>
                  <div class="text-h5 text-bold">{{ formatCurrency(totalItemsRevenue) }}</div>
                </q-card-section>
              </q-card>
            </div>
          </div>

          <f-card col="12" class="no-print">
            <r-table
              :columns="itemColumns"
              v-model="dataItems"
              row-key="item_id"
            >
              <template v-slot:top-right>
                <q-btn color="primary" outline label="Cetak Laporan Alat" icon="print" @click="printPage" />
              </template>
            </r-table>
          </f-card>
        </template>
      </q-tab-panel>

      <!-- PANEL DENDA -->
      <q-tab-panel name="denda" class="no-padding">
        <f-card title="Filter Laporan Denda" col="12" class="no-print q-mb-md">
          <div class="row q-col-gutter-sm items-center">
            <div class="col-12 col-md-4">
              <q-input v-model="filters.startDate" type="date" label="Tanggal Mulai" outlined dense />
            </div>
            <div class="col-12 col-md-4">
              <q-input v-model="filters.endDate" type="date" label="Tanggal Akhir" outlined dense />
            </div>
            <div class="col-12 col-md-4">
              <q-btn color="primary" label="Terapkan" icon="filter_alt" @click="fetchData" unelevated class="full-width" />
            </div>
          </div>
        </f-card>

        <s-loading v-if="loadingFines" />
        <template v-else>
          <div class="row q-col-gutter-sm q-mb-md no-print">
            <div class="col-12 col-md-6">
              <q-card flat bordered class="bg-red-1 text-red-9">
                <q-card-section>
                  <div class="text-caption text-uppercase">Total Kejadian Denda</div>
                  <div class="text-h5 text-bold">{{ fineData.length }}</div>
                </q-card-section>
              </q-card>
            </div>
            <div class="col-12 col-md-6">
              <q-card flat bordered class="bg-red-1 text-red-9">
                <q-card-section>
                  <div class="text-caption text-uppercase">Total Denda Terkumpul (Terverifikasi)</div>
                  <div class="text-h5 text-bold">{{ formatCurrency(totalFines) }}</div>
                </q-card-section>
              </q-card>
            </div>
          </div>

          <f-card col="12" class="no-print">
            <r-table
              :columns="fineColumns"
              v-model="fineData"
              row-key="id"
            >
              <template v-slot:top-right>
                <q-btn color="primary" outline label="Cetak Laporan Denda" icon="print" @click="printPage" />
              </template>
            </r-table>
          </f-card>
        </template>
      </q-tab-panel>
    </q-tab-panels>

    <!-- PRINT OUT TEMPLATE (Only visible when printing) -->
    <div class="print-only print-template">
      <!-- 1. TRANSAKSI PRINT TEMPLATE -->
      <template v-if="activeTab === 'transaksi'">
        <div class="print-header row items-center justify-between">
          <div>
            <div style="font-size: 28px; line-height: 1;">
              <span class="text-weight-bold" style="font-family: 'Outfit', sans-serif; color: #1e3a8a;">RENT</span><span class="text-weight-regular text-grey-8" style="font-family: 'Outfit', sans-serif;">CAM</span>
            </div>
            <div style="font-size: 12px; letter-spacing: 1px; color: #64748b; text-transform: uppercase;">rental alat photo</div>
          </div>
          <div class="text-right">
            <h3 class="q-ma-none text-bold" style="font-size: 20px; color: #111; margin-bottom: 4px;">LAPORAN TRANSAKSI RENTAL</h3>
            <p style="font-size: 13px; color: #555; margin: 0;">Periode: {{ filters.startDate }} s/d {{ filters.endDate }}</p>
          </div>
        </div>

        <div class="print-summary row q-mb-md justify-between">
          <div class="col-4">
            <strong>Total Transaksi</strong>
            <span>{{ totalTransactions }}</span>
          </div>
          <div class="col-4 text-center">
             <strong>Pendapatan Aktual</strong>
             <span>{{ formatCurrency(totalRevenue) }}</span>
          </div>
          <div class="col-4 text-right">
            <strong>Dibatalkan</strong>
            <span>{{ totalCanceled }}</span>
          </div>
        </div>

        <table class="print-table">
          <thead>
            <tr>
              <th class="text-left">No</th>
              <th class="text-left">Kode Rental</th>
              <th class="text-left">Tanggal</th>
              <th class="text-left">Pelanggan</th>
              <th class="text-center">Durasi</th>
              <th class="text-center">Status</th>
              <th class="text-right">Grand Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in data" :key="item.id">
              <td>{{ index + 1 }}</td>
              <td>{{ item.rental_code }}</td>
              <td>{{ new Date(item.created_at).toLocaleDateString('id-ID') }}</td>
              <td>{{ item.customer_name }}</td>
              <td class="text-center">{{ item.duration_days }}</td>
              <td class="text-center">{{ getStatusLabel(item.status) }}</td>
              <td class="text-right">{{ formatCurrency(item.grand_total) }}</td>
            </tr>
            <tr v-if="!data || data.length === 0">
              <td colspan="7" class="text-center">Tidak ada transaksi pada periode ini.</td>
            </tr>
          </tbody>
        </table>
      </template>

      <!-- 2. ALAT DISEWA PRINT TEMPLATE -->
      <template v-if="activeTab === 'items'">
        <div class="print-header row items-center justify-between">
          <div>
            <div style="font-size: 28px; line-height: 1;">
              <span class="text-weight-bold" style="font-family: 'Outfit', sans-serif; color: #1e3a8a;">RENT</span><span class="text-weight-regular text-grey-8" style="font-family: 'Outfit', sans-serif;">CAM</span>
            </div>
            <div style="font-size: 12px; letter-spacing: 1px; color: #64748b; text-transform: uppercase;">rental alat photo</div>
          </div>
          <div class="text-right">
            <h3 class="q-ma-none text-bold" style="font-size: 20px; color: #111; margin-bottom: 4px;">LAPORAN PENYEWAAN ALAT</h3>
            <p style="font-size: 13px; color: #555; margin: 0;">Periode: {{ filters.startDate }} s/d {{ filters.endDate }}</p>
          </div>
        </div>

        <div class="print-summary row q-mb-md justify-between">
          <div class="col-6">
            <strong>Total QTY Disewa</strong>
            <span>{{ totalItemsRented }} Pcs</span>
          </div>
          <div class="col-6 text-right">
             <strong>Estimasi Pendapatan Alat</strong>
             <span>{{ formatCurrency(totalItemsRevenue) }}</span>
          </div>
        </div>

        <table class="print-table">
          <thead>
            <tr>
              <th class="text-left">No</th>
              <th class="text-left">Kode Alat</th>
              <th class="text-left">Nama Alat</th>
              <th class="text-center">Hit. Sewa</th>
              <th class="text-center">Total QTY</th>
              <th class="text-right">Pendapatan</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in dataItems" :key="item.item_id">
              <td>{{ index + 1 }}</td>
              <td>{{ item.item_code }}</td>
              <td>{{ item.item_name }} <small class="text-grey-7">({{ item.item_brand }})</small></td>
              <td class="text-center">{{ item.times_rented }}x</td>
              <td class="text-center">{{ item.sum_qty }}</td>
              <td class="text-right">{{ formatCurrency(item.total_revenue) }}</td>
            </tr>
            <tr v-if="!dataItems || dataItems.length === 0">
              <td colspan="6" class="text-center">Tidak ada penyewaan alat pada periode ini.</td>
            </tr>
          </tbody>
        </table>
      </template>

      <!-- 3. DENDA PRINT TEMPLATE -->
      <template v-if="activeTab === 'denda'">
        <div class="print-header row items-center justify-between">
          <div>
            <div style="font-size: 28px; line-height: 1;">
              <span class="text-weight-bold" style="font-family: 'Outfit', sans-serif; color: #1e3a8a;">RENT</span><span class="text-weight-regular text-grey-8" style="font-family: 'Outfit', sans-serif;">CAM</span>
            </div>
            <div style="font-size: 12px; letter-spacing: 1px; color: #64748b; text-transform: uppercase;">rental alat photo</div>
          </div>
          <div class="text-right">
            <h3 class="q-ma-none text-bold" style="font-size: 20px; color: #111; margin-bottom: 4px;">LAPORAN PEMBAYARAN DENDA</h3>
            <p style="font-size: 13px; color: #555; margin: 0;">Periode: {{ filters.startDate }} s/d {{ filters.endDate }}</p>
          </div>
        </div>

        <div class="print-summary row q-mb-md justify-between">
          <div class="col-6">
            <strong>Total Kejadian Denda</strong>
            <span>{{ fineData.length }}</span>
          </div>
          <div class="col-6 text-right">
             <strong>Total Denda Terverifikasi</strong>
             <span>{{ formatCurrency(totalFines) }}</span>
          </div>
        </div>

        <table class="print-table">
          <thead>
            <tr>
              <th class="text-left">No</th>
              <th class="text-left">Kode Rental</th>
              <th class="text-left">Tgl Pembayaran</th>
              <th class="text-right">Jumlah Denda</th>
              <th class="text-left">Keterangan</th>
              <th class="text-center">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in fineData" :key="item.id">
              <td>{{ index + 1 }}</td>
              <td>{{ item.rental_code }}</td>
              <td>{{ new Date(item.created_at).toLocaleDateString('id-ID') }}</td>
              <td class="text-right">{{ formatCurrency(item.amount) }}</td>
              <td>{{ item.notes || '-' }}</td>
              <td class="text-center">{{ item.status }}</td>
            </tr>
            <tr v-if="!fineData || fineData.length === 0">
              <td colspan="6" class="text-center">Tidak ada pembayaran denda pada periode ini.</td>
            </tr>
          </tbody>
        </table>
      </template>

      <!-- COMMON SIGNATURE FOOTER -->
      <div class="print-footer q-mt-lg row justify-end">
        <div class="text-center">
          <p>Dicetak pada: {{ new Date().toLocaleString('id-ID') }}</p>
          <br /><br /><br />
          <p><strong>Admin / Petugas</strong></p>
        </div>
      </div>
    </div>
  </s-page>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Meta } from './meta'
import Api from 'src/services/api'
import { Helper } from 'src/services/helper'
import { format } from 'quasar'

const { capitalize } = format
const loading = ref(false)
const loadingItems = ref(false)
const activeTab = ref('transaksi')
const data = ref<any[]>([])
const dataItems = ref<any[]>([])

const now = new Date()
const firstDay = new Date(now.getFullYear(), now.getMonth(), 1).toISOString().split('T')[0]
const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0).toISOString().split('T')[0]

const filters = ref({
  startDate: firstDay,
  endDate: lastDay,
  status: ''
})

const columns = [
  { name: 'rental_code', align: 'left', label: 'Kode Rental', field: 'rental_code' },
  { name: 'created_at', align: 'left', label: 'Tanggal', field: 'created_at', formatter: 'date' },
  { name: 'customer_name', align: 'left', label: 'Pelanggan', field: 'customer_name' },
  { name: 'duration_days', align: 'center', label: 'Durasi (Hari)', field: 'duration_days' },
  { name: 'status', align: 'center', label: 'Status', field: 'status', formatter: 'badge' },
  { name: 'grand_total', align: 'right', label: 'Total', field: 'grand_total', formatter: 'float' }
] as any

const itemColumns = [
  { name: 'item_code', align: 'left', label: 'Kode Alat', field: 'item_code', sortable: true },
  { name: 'item_name', align: 'left', label: 'Nama Alat', field: 'item_name', sortable: true },
  { name: 'item_brand', align: 'left', label: 'Merk', field: 'item_brand', sortable: true },
  { name: 'times_rented', align: 'center', label: 'Hit. Sewa (Kali)', field: 'times_rented', sortable: true },
  { name: 'sum_qty', align: 'center', label: 'Total QTY Disewa', field: 'sum_qty', sortable: true },
  { name: 'total_revenue', align: 'right', label: 'Pendapatan', field: 'total_revenue', formatter: 'float', sortable: true }
] as any

const fineColumns = [
  { name: 'rental_code', align: 'left', label: 'Kode Rental', field: 'rental_code' },
  { name: 'created_at', align: 'left', label: 'Tgl Pembayaran Denda', field: 'created_at', formatter: 'date' },
  { name: 'amount', align: 'right', label: 'Jumlah Denda', field: 'amount', formatter: 'float', classes: 'text-bold text-red' },
  { name: 'bank_name', align: 'left', label: 'Bank', field: 'bank_name' },
  { name: 'account_number', align: 'left', label: 'No. Rekening', field: 'account_number' },
  { name: 'notes', align: 'left', label: 'Keterangan', field: 'notes' },
  { name: 'status', align: 'center', label: 'Status', field: 'status', formatter: 'badge' },
] as any

const api = new Api()

const totalTransactions = computed(() => data.value.length)
const totalRevenue = computed(() => {
  return data.value
    .filter(d => ['selesai', 'aktif'].includes(d.status))
    .reduce((sum, item) => sum + (Number(item.grand_total) || 0), 0)
})
const totalCanceled = computed(() => {
  return data.value.filter(d => d.status === 'dibatalkan').length
})

const totalItemsRented = computed(() => {
  return dataItems.value.reduce((sum, item) => sum + (Number(item.sum_qty) || 0), 0)
})

const totalItemsRevenue = computed(() => {
  return dataItems.value.reduce((sum, item) => sum + (Number(item.total_revenue) || 0), 0)
})

const loadingFines = ref(false)
const fineData = ref<any[]>([])

const totalFines = computed(() =>
  fineData.value
    .filter(d => d.status === 'terverifikasi')
    .reduce((sum, item) => sum + (Number(item.amount) || 0), 0)
)

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(value || 0)
}

const getStatusLabel = (status: string) => {
  const opt = Meta.statusOptions.find(o => o.value === status)
  return opt ? opt.label : capitalize(status)
}

const fetchData = () => {
  loading.value = true
  loadingItems.value = true
  
  const queries = []
  queries.push(`limit=0`)
  
  if (filters.value.startDate && filters.value.endDate) {
    queries.push(`between=created_at:${filters.value.startDate} to ${filters.value.endDate} 23:59:59`)
  }
  if (filters.value.status) {
    queries.push(`where=status:${filters.value.status}`)
  }

  const qs = queries.join('&')
  
  // Fetch Transactions
  api.get(`${Meta.apiModule}?${qs}`, (status: number, responseData: any) => {
    if (status === 200) {
      data.value = Array.isArray(responseData) ? responseData : (responseData.items || [])
    }
    loading.value = false
  })
  
  // Fetch Rental Items for Aggregation
  let itemQs = queries.filter(q => !q.startsWith('where=status:')).join('&')
  if (filters.value.status) {
    itemQs += `&where=rental_status:${filters.value.status}`
  }
  
  api.get(`transaction/rental-items?${itemQs}`, (status: number, responseData: any) => {
    if (status === 200) {
      const rawItems = Array.isArray(responseData) ? responseData : (responseData.items || [])
      const acc: Record<string, any> = {}
      
      // Group by item_id
      rawItems.forEach((r: any) => {
        const id = r.item_id
        if (!acc[id]) {
          acc[id] = { 
            item_id: id,
            item_code: r.item_code || '-',
            item_name: r.item_name || 'Tidak Diketahui',
            item_brand: r.item_brand || '-',
            times_rented: 0,
            sum_qty: 0,
            total_revenue: 0
          }
        }
        acc[id].times_rented += 1
        acc[id].sum_qty += (r.quantity || 1)
        acc[id].total_revenue += (r.subtotal || 0)
      })
      
      dataItems.value = Object.values(acc).sort((a, b) => b.total_revenue - a.total_revenue)
    }
    loadingItems.value = false
  })
  // Fetch Fines (pembayaran denda nyata)
  loadingFines.value = true
  const fineQs = [
    'limit=0',
    'where=type:denda',
    ...(filters.value.startDate && filters.value.endDate
      ? [`between=created_at:${filters.value.startDate} to ${filters.value.endDate} 23:59:59`]
      : [])
  ].join('&')
  api.get(`transaction/payments?${fineQs}`, (status: number, responseData: any) => {
    if (status === 200) {
      fineData.value = Array.isArray(responseData) ? responseData : (responseData.items || [])
    }
    loadingFines.value = false
  })
}

const printPage = () => {
  window.print()
}

onMounted(() => {
  fetchData()
})
</script>

<style>
/* Hide by default on screen */
.print-only {
  display: none !important;
}

@media print {
  @page {
    size: A4 portrait;
    margin: 1.5cm;
  }

  body * {
    visibility: hidden;
  }
  
  #q-app, .q-layout, .q-page-container, .q-page, .q-pa-md {
    position: static !important;
    overflow: visible !important;
    min-height: auto !important;
    height: auto !important;
    padding: 0 !important;
    margin: 0 !important;
  }
  
  .q-card {
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
  }

  .print-only, .print-only * {
    visibility: visible;
  }
  
  .print-only {
    display: block !important;
    position: relative !important;
    width: 100% !important;
    color: #333 !important;
    font-family: 'Roboto', -apple-system, sans-serif !important;
  }

  .print-header {
    border-bottom: 2px solid #222;
    padding-bottom: 15px;
    margin-bottom: 20px;
  }
  
  .print-header h3 {
    font-size: 24px;
    font-weight: bold;
    color: #111;
    margin: 0 0 5px 0;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  
  .print-header p {
    font-size: 14px;
    color: #555;
    margin: 0;
  }

  .print-summary {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
    background-color: #f8f9fa;
    padding: 15px;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .print-summary div {
    font-size: 14px;
  }
  
  .print-summary strong {
    display: block;
    font-size: 12px;
    color: #666;
    text-transform: uppercase;
    margin-bottom: 4px;
  }
  
  .print-summary span {
    font-size: 18px;
    font-weight: bold;
    color: #000;
  }

  .print-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    font-size: 13px;
  }

  .print-table th, .print-table td {
    border: 1px solid #ddd;
    padding: 12px 10px;
    color: #333 !important;
  }

  .print-table th {
    background-color: #f1f5f9 !important;
    font-weight: bold;
    text-transform: uppercase;
    font-size: 12px;
    letter-spacing: 0.5px;
    color: #1e293b !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .print-table tr:nth-child(even) td {
    background-color: #fafbfc !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .print-table td.text-center, .print-table th.text-center { text-align: center; }
  .print-table td.text-right, .print-table th.text-right { text-align: right; }
  .print-table td.text-left, .print-table th.text-left { text-align: left; }

  .print-footer {
    margin-top: 40px;
    display: flex;
    justify-content: flex-end;
  }

  .print-footer-box {
    width: 250px;
    text-align: center;
  }
  
  .print-footer-box p {
    margin: 5px 0;
    font-size: 14px;
  }

  .print-signature {
    min-height: 80px;
  }

  .no-print {
    display: none !important;
  }
}
</style>
