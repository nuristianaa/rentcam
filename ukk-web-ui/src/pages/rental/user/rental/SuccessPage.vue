<template>
  <div class="success-page q-pa-lg">
    <q-card class="q-pa-xl bg-white shadow-2">
      <div class="row items-center q-gutter-sm q-mb-lg">
        <q-icon name="check_circle" size="42px" color="positive" />
        <div>
          <div class="text-h5 text-weight-bold">Booking Berhasil</div>
          <div class="text-subtitle2 text-grey-7">Silakan datang ke toko dengan persyaratan berikut.</div>
        </div>
      </div>

      <q-separator class="q-my-md" />

      <div class="q-mb-md">
        <div class="text-subtitle1 text-weight-bold q-mb-sm">Apa yang harus dibawa</div>
        <ul class="success-list">
          <li>KTP / SIM / identitas resmi</li>
          <li>Bukti transfer atau bukti pembayaran</li>
          <li>Deposit sesuai ketentuan toko</li>
          <li>Nomor booking: <strong>{{ bookingCode || '-' }}</strong></li>
        </ul>
      </div>

      <div class="q-mb-md">
        <div class="text-subtitle1 text-weight-bold q-mb-sm">Lokasi toko</div>
        <div class="success-location q-pa-md bg-grey-1 rounded-borders">
          <div class="text-body1 text-weight-bold">Jl. Cihampelas No. 123, Bandung, Jawa Barat</div>
          <div class="text-caption text-grey-7 q-mt-xs">Buka setiap Senin–Sabtu, 08.00–20.00 WIB.</div>
          <q-btn class="q-mt-md" dense unelevated color="primary" label="Buka Google Maps" href="https://www.google.com/maps/search/?api=1&query=Jl.+Cihampelas+No.+123,+Bandung,+Jawa+Barat" target="_blank" />
        </div>
      </div>

      <div class="row justify-end q-gutter-sm">
        <q-btn label="Lihat Riwayat Booking" color="primary" unelevated @click="goHistory" />
        <q-btn label="Kembali ke Home" flat @click="goHome" />
      </div>
    </q-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const bookingCode = computed(() => String(route.query.code ?? route.query.rental_code ?? ''))

const goHistory = () => router.push({ name: 'rental/user/rental-histories' })
const goHome = () => router.push({ name: 'rental/user' })
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
