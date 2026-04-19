<template>
  <div class="success-page q-pa-lg">
    <q-card class="q-pa-xl bg-white shadow-2">
      <div class="row items-center q-gutter-sm q-mb-lg">
        <q-icon name="check_circle" size="42px" color="positive" />
        <div>
          <div class="text-h5 text-weight-bold">Booking Successful</div>
          <div class="text-subtitle2 text-grey-7">Please visit the store with the following requirements.</div>
        </div>
      </div>

      <q-separator class="q-my-md" />

      <div class="q-mb-md">
        <div class="text-subtitle1 text-weight-bold q-mb-sm">What to bring</div>
        <ul class="success-list">
          <li>ID Card / Driving License / Official ID</li>
          <li v-if="paymentMethod === 'transfer'">Proof of payment transfer amounting to {{ formatIdr(grandTotal) }}</li>
          <li v-else>Cash / payment on the spot (COD)</li>
          <li>Deposit according to store policy</li>
          <li>Booking number: <strong>{{ bookingCode || '-' }}</strong></li>
        </ul>
      </div>

      <div v-if="paymentMethod === 'transfer'" class="q-mb-md">
        <div class="text-subtitle1 text-weight-bold q-mb-sm">Transfer Payment Instructions</div>
        <q-banner rounded class="bg-blue-1 text-blue-9 q-pa-md">
          <div class="row items-center q-gutter-md">
            <q-icon name="account_balance" size="lg" color="blue-7" />
            <div class="col">
              <div class="text-subtitle2 text-weight-bold" style="font-size: 1.1rem;">BCA Bank - 1234567890</div>
              <div class="text-caption text-weight-medium" style="font-size: 0.9rem;">a.n. Camera Rental Admin</div>
              <div class="text-weight-bold q-mt-xs text-blue-10" style="font-size: 1.2rem;">Total Amount: {{ formatIdr(grandTotal) }}</div>
            </div>
          </div>
        </q-banner>
      </div>

      <div class="q-mb-md">
        <div class="text-subtitle1 text-weight-bold q-mb-sm">Store Location</div>
        <div class="success-location q-pa-md bg-grey-1 rounded-borders">
          <div class="text-body1 text-weight-bold">Jl. Cihampelas No. 123, Bandung, West Java</div>
          <div class="text-caption text-grey-7 q-mt-xs">Open every Monday–Saturday, 08.00–20.00 WIB.</div>
          <q-btn class="q-mt-md" dense unelevated color="primary" label="Open Google Maps" href="https://www.google.com/maps/search/?api=1&query=Jl.+Cihampelas+No.+123,+Bandung,+Jawa+Barat" target="_blank" />
        </div>
      </div>

      <div class="q-mb-md">
        <div class="text-subtitle1 text-weight-bold q-mb-sm">Admin Contact</div>
        <q-banner rounded class="bg-green-1 text-green-9 q-pa-md">
          <div class="row items-center q-gutter-md">
            <q-icon name="chat" size="lg" color="green-7" />
            <div class="col">
              <div class="text-subtitle2 text-weight-bold" style="font-size: 1.1rem;">WhatsApp: 0838-5107-1957</div>
              <div class="text-caption text-weight-medium" style="font-size: 0.9rem;">Send payment proof or ask about your rental.</div>
            </div>
            <div class="col-auto">
              <q-btn
                unelevated
                color="green-7"
                icon="send"
                label="Send Receipt Now"
                :href="waLink"
                target="_blank"
                no-caps
              />
            </div>
          </div>
        </q-banner>
      </div>

      <div class="row justify-end q-gutter-sm">
        <q-btn label="View Booking History" color="primary" unelevated @click="goHistory" />
        <q-btn label="Back to Home" flat @click="goHome" />
      </div>
    </q-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Api from 'src/services/api'

const API = new Api()

const route = useRoute()
const router = useRouter()
const bookingCode = computed(() => String(route.query.code ?? route.query.rental_code ?? ''))
const paymentMethod = ref(String(route.query.payment_method ?? ''))
const grandTotal = ref(Number(route.query.grand_total ?? 0))

const formatIdr = (val: number) => {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(val)
}

const waLink = computed(() => {
  let text = `Hello Admin, I want to send payment confirmation for booking number: ${bookingCode.value}`
  if (paymentMethod.value === 'transfer') {
    text += ` amounting to ${formatIdr(grandTotal.value)}`
  }
  return `https://wa.me/6283851071957?text=${encodeURIComponent(text)}`
})

const goHistory = () => router.push({ name: 'rental/user/rental-histories' })
const goHome = () => router.push({ name: 'rental/user' })

onMounted(() => {
  if (!grandTotal.value && bookingCode.value) {
    API.get(`transaction/rentals?search=${bookingCode.value}`, (status: number, data: any) => {
      if (status === 200) {
        const rows = data?.data ?? data
        const found = Array.isArray(rows) 
          ? rows.find((r: any) => r.rental_code === bookingCode.value)
          : null
        if (found) {
          paymentMethod.value = found.payment_method
          grandTotal.value = found.grand_total
        }
      }
    }, 'rental')
  }

  const script = document.createElement('script')
  script.src = 'https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js'
  script.onload = () => {
    const w = window as any
    if (w.confetti) {
      w.confetti({
        particleCount: 150,
        spread: 70,
        origin: { y: 0.6 }
      })
    }
  }
  document.head.appendChild(script)
})
</script>

<style scoped>
.success-page {
  max-width: 760px;
  margin: 0 auto;
}
.success-list {
  padding-left: 16px;
  margin: 0;
  list-style: disc;
}
.success-list li {
  margin-bottom: 0.75rem;
}
.success-location {
  border: 1px solid rgba(0,0,0,.08);
}
</style>
