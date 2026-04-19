<template>
  <div class="q-pa-md">
    <s-loading v-if="loading" />

    <template v-else>
      <!-- Header -->
      <div class="row items-center q-mb-lg">
        <div class="col">
          <div class="text-h6 text-weight-bold">{{ Meta.title }}</div>
          <div class="text-caption text-grey-6">
            Showing booking history for:
            <span class="text-weight-medium text-dark">{{ currentUserName }}</span>
          </div>
        </div>
        <div class="col-auto">
          <q-btn
            unelevated
            rounded
            label="New Booking"
            color="primary"
            icon="add"
            @click="goToCreate"
          />
        </div>
      </div>

      <!-- Filter Status Chips -->
      <div class="row q-gutter-sm q-mb-lg">
        <q-chip
          clickable
          :outline="filterStatus !== null"
          color="primary"
          text-color="white"
          label="All"
          @click="filterStatus = null"
        />
        <q-chip
          v-for="opt in Meta.statusOptions"
          :key="opt.value"
          clickable
          :outline="filterStatus !== opt.value"
          :color="Meta.statusColor[opt.value]"
          text-color="white"
          :label="opt.label"
          @click="filterStatus = filterStatus === opt.value ? null : opt.value"
        />
      </div>

      <!-- Loading Skeleton -->
      <template v-if="tableLoading">
        <q-card
          v-for="n in 3"
          :key="n"
          flat
          bordered
          class="q-mb-sm"
        >
          <q-card-section>
            <q-skeleton type="text" width="40%" />
            <q-skeleton type="text" width="60%" class="q-mt-xs" />
          </q-card-section>
        </q-card>
      </template>

      <!-- Empty State -->
      <div
        v-else-if="filteredRows.length === 0"
        class="column flex-center q-py-xl text-grey-5"
      >
        <q-icon name="receipt_long" size="72px" />
        <div class="text-body1 q-mt-sm">No booking history yet.</div>
        <q-btn
          flat
          rounded
          color="primary"
          label="Start Booking Now"
          icon="add"
          class="q-mt-sm"
          @click="goToCreate"
        />
      </div>

      <!-- List Card -->
      <template v-else>
        <q-card
          v-for="row in filteredRows"
          :key="row.id"
          flat
          bordered
          class="q-mb-md cursor-pointer rental-card"
          style="border-radius: 12px; border-color: #e2e8f0;"
          @click="goToDetail(row)"
        >
          <q-card-section class="q-pa-md">
            <div class="row items-start no-wrap">

              <!-- Icon Status -->
              <q-avatar
                color="blue-2"
                text-color="blue-9"
                size="42px"
                class="q-mr-md"
              >
                <q-icon name="receipt_long" size="22px" />
              </q-avatar>

              <!-- Info Utama -->
              <div class="col">
                <div class="row items-center q-gutter-x-sm">
                  <span class="text-weight-bold">{{ row.rental_code ?? '-' }}</span>
                  <q-badge
                    :color="Meta.statusColor[row.status] ?? 'grey'"
                    :label="resolveStatusLabel(row.status)"
                    class="q-py-xs"
                  />
                </div>

                <div class="row q-gutter-x-md q-mt-xs text-caption text-grey-7">
                  <span>
                    <q-icon name="calendar_today" size="12px" class="q-mr-xs" />
                    {{ row.start_date ?? '-' }} → {{ row.end_date ?? '-' }}
                  </span>
                  <span>
                    <q-icon name="timelapse" size="12px" class="q-mr-xs" />
                    {{ row.duration_days ?? '-' }} days
                  </span>
                  <span>
                    <q-icon name="payments" size="12px" class="q-mr-xs" />
                    {{ resolvePaymentLabel(row.payment_method) }}
                  </span>
                </div>

                <div v-if="row.notes" class="text-caption text-grey-5 q-mt-xs ellipsis">
                  <q-icon name="notes" size="12px" class="q-mr-xs" />{{ row.notes }}
                </div>
              </div>

              <!-- Total -->
              <div class="col-auto text-right">
                <div class="text-weight-bold text-primary">
                  {{ formatCurrency(row.grand_total) }}
                </div>
                <div class="text-caption text-grey-5">Total</div>
              </div>

            </div>
          </q-card-section>
        </q-card>
      </template>

    </template>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Handler } from 'src/services/handler'
import { authStore } from 'src/stores/auth'
import { Meta } from './meta'

const router = useRouter()
const API = new Api()
const auth = authStore()

// ─── State ────────────────────────────────────────────────────────────────────
const loading      = ref(true)
const tableLoading = ref(false)
const rows         = ref<any[]>([])
const filterStatus = ref<string | null>(null)

// ─── Current User ─────────────────────────────────────────────────────────────
const currentUser     = auth.user || auth.getUser()
const currentUserId   = currentUser?.id ?? null
const currentUserName = currentUser?.name ?? currentUser?.username ?? '-'

// ─── Filter ───────────────────────────────────────────────────────────────────
const filteredRows = computed(() => {
  if (!filterStatus.value) return rows.value
  return rows.value.filter((r) => r.status === filterStatus.value)
})

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

// ─── Fetch Data ───────────────────────────────────────────────────────────────
const loadData = () => {
  if (!currentUserId) {
    rows.value = []
    return
  }

  tableLoading.value = true

  // GET transaction/rentals?where=customer_email:{email} atau fallback ke customer_id jika email tidak tersedia
  const filterQuery = currentUser?.email
    ? `where=customer_email:${encodeURIComponent(currentUser.email)}`
    : `where=customer_id:${currentUserId}`

  API.get(
    `${Meta.apiModule}?${filterQuery}`,
    (status: number, data: any) => {
      rows.value = status === 200 ? (data?.data ?? data ?? []) : []
      tableLoading.value = false
    },
    Meta.app
  )
}

// ─── Navigation ───────────────────────────────────────────────────────────────
const goToCreate = () => router.push({ name: 'user/rental/create' })

const goToDetail = (row: any) =>
  router.push({ name: 'user/rental/read', params: { id: row.id } })

// ─── Init ─────────────────────────────────────────────────────────────────────
onMounted(() => {
  Handler.permissions(router, 'browse', Meta, (_status: boolean, data: any) => {
    Meta.permission = data
    loadData()
    loading.value = false
  })
})
</script>

<style scoped>
.rental-card {
  transition: box-shadow 0.2s, transform 0.15s;
}
.rental-card:hover {
  box-shadow: 0 4px 16px rgba(25, 118, 210, 0.15);
  transform: translateY(-1px);
}
</style>