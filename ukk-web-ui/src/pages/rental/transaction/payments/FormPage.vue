<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else :meta="Meta" @submit="submit" @back="back">
      <div class="row">

        <!-- Mode BARU: tampilkan pilih rental + form input -->
        <template v-if="!isEditMode">
          <!-- Rental -->
          <f-select
            v-model="dataModel.rental_id"
            col="6"
            :label="Lang.module(Meta, 'rental_id')"
            :options="rentalOptions"
            :option-label="(v) => v.rental_code"
            option-value="id"
            required
            @update:model-value="onRentalChange"
          />

          <!-- Kode Rental (readonly) -->
          <f-input
            v-model="dataModel.rental_code"
            col="6"
            :label="Lang.module(Meta, 'rental_code')"
            readonly
          />

          <!-- Tipe Pembayaran -->
          <f-select
            v-model="dataModel.type"
            col="6"
            :label="Lang.module(Meta, 'type')"
            :options="Meta.typeOptions"
            option-label="label"
            option-value="value"
            required
          />

          <!-- Jumlah -->
          <f-number
            v-model="dataModel.amount"
            col="6"
            :label="Lang.module(Meta, 'amount')"
            prefix="Rp"
            required
          />

          <!-- Tanggal Bayar -->
          <f-date
            v-model="dataModel.paid_at"
            col="6"
            :label="Lang.module(Meta, 'paid_at')"
          />

          <!-- Nama Bank -->
          <f-input
            v-model="dataModel.bank_name"
            col="6"
            :label="Lang.module(Meta, 'bank_name')"
          />

          <!-- Nomor Rekening -->
          <f-input
            v-model="dataModel.account_number"
            col="6"
            :label="Lang.module(Meta, 'account_number')"
          />

          <!-- Catatan -->
          <f-textarea
            v-model="dataModel.notes"
            col="12"
            :label="Lang.module(Meta, 'notes')"
          />

          <!-- Toggle: Langsung Verifikasi -->
          <div class="col-12 q-mt-sm">
            <q-separator class="q-mb-md" />
            <q-toggle
              v-model="autoVerify"
              label="Langsung verifikasi setelah disimpan"
              color="positive"
              left-label
            />
          </div>

          <!-- Form verifikasi inline (muncul jika autoVerify aktif) -->
          <template v-if="autoVerify">
            <f-select
              v-model="verifyStatus"
              col="6"
              label="Status Verifikasi"
              :options="verifyOptions"
              option-label="label"
              option-value="value"
              required
            />
            <f-textarea
              v-model="verifyNotes"
              col="12"
              label="Catatan Verifikasi"
            />
          </template>
        </template>

        <!-- Mode VERIFIKASI: hanya tampilkan info + pilih status verifikasi -->
        <template v-else>
          <f-card title="Informasi Pembayaran" col="12">
            <div class="row q-col-gutter-sm">
              <div class="col-6">
                <div class="text-caption text-grey">Kode Rental</div>
                <div class="text-body2 text-bold">{{ dataModel.rental_code || '-' }}</div>
              </div>
              <div class="col-6">
                <div class="text-caption text-grey">Tipe</div>
                <div class="text-body2">{{ typeLabel(dataModel.type) }}</div>
              </div>
              <div class="col-6">
                <div class="text-caption text-grey">Jumlah</div>
                <div class="text-body2 text-bold text-positive">{{ formatCurrency(dataModel.amount) }}</div>
              </div>
              <div class="col-6">
                <div class="text-caption text-grey">Status Saat Ini</div>
                <q-badge :color="statusColor(dataModel.status)" :label="statusLabel(dataModel.status)" />
              </div>
              <div class="col-6" v-if="dataModel.bank_name">
                <div class="text-caption text-grey">Bank</div>
                <div class="text-body2">{{ dataModel.bank_name }}</div>
              </div>
              <div class="col-6" v-if="dataModel.account_number">
                <div class="text-caption text-grey">No. Rekening</div>
                <div class="text-body2">{{ dataModel.account_number }}</div>
              </div>
            </div>
          </f-card>

          <!-- Hanya tampilkan form verifikasi jika masih 'menunggu' -->
          <template v-if="dataModel.status === 'menunggu'">
            <f-select
              v-model="verifyStatus"
              col="6"
              label="Status Verifikasi"
              :options="verifyOptions"
              option-label="label"
              option-value="value"
              required
            />
            <f-textarea
              v-model="verifyNotes"
              col="12"
              label="Catatan Verifikasi"
            />
          </template>

          <div v-else class="col-12">
            <q-banner rounded class="bg-orange-1 text-orange-9">
              <template v-slot:avatar>
                <q-icon name="info" />
              </template>
              Pembayaran sudah <strong>{{ statusLabel(dataModel.status) }}</strong> — tidak dapat diubah lagi.
            </q-banner>
          </div>
        </template>

      </div>
    </h-form>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Meta } from './meta'
import type { DataModel } from './meta'
import { Lang } from 'src/services/lang'

const emit = defineEmits(['refreshEvent'])

const route  = useRoute()
const router = useRouter()
const id     = Array.isArray(route.params?.id) ? route.params.id[0] : (route.params?.id ?? null)
const API    = new Api()

const loading        = ref(true)
const dataModel      = ref<DataModel>({ ...Meta.model })
const rentalOptions  = ref<any[]>([])
const autoVerify     = ref<boolean>(false)
const verifyStatus   = ref<string>('terverifikasi')
const verifyNotes    = ref<string>('')

// Mode edit = verifikasi (ID ada), mode create = input baru
const isEditMode = computed(() => !!id)

const verifyOptions = [
  { label: 'Terverifikasi ✓', value: 'terverifikasi' },
  { label: 'Ditolak ✗',       value: 'ditolak' },
]

// ─── Helpers ───────────────────────────────────────────────────

const typeLabel = (type: string | null) =>
  Meta.typeOptions.find((o) => o.value === type)?.label ?? type ?? '-'

const statusLabel = (status: string | null) =>
  Meta.statusOptions.find((o) => o.value === status)?.label ?? status ?? '-'

const statusColor = (status: string | null) => {
  if (status === 'terverifikasi') return 'positive'
  if (status === 'ditolak')       return 'negative'
  return 'warning'
}

const formatCurrency = (val: number | null) => {
  if (val == null) return '-'
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(val)
}

// ─── Data loading ───────────────────────────────────────────────

const loadRentals = () => {
  API.get('transaction/rentals?limit=0', (status: number, data: any) => {
    if (status === 200) {
      const raw = data?.data?.data ?? data?.data ?? data
      rentalOptions.value = Array.isArray(raw) ? raw : []
    }
  }, Meta.app)
}

const onRentalChange = (val: string) => {
  const found = rentalOptions.value.find((r) => r.id === val)
  if (found) dataModel.value.rental_code = found.rental_code ?? null
}

const today = new Date().toISOString().slice(0, 10)

const init = () => {
  // Reset model, tapi pertahankan paid_at = hari ini untuk create mode
  dataModel.value = { ...Meta.model, paid_at: today }
  autoVerify.value   = false
  verifyStatus.value = 'terverifikasi'
  verifyNotes.value  = ''
  loadRentals()  // selalu load — dibutuhkan untuk lookup rental_code saat edit
  const action = id ? 'update' : 'create'
  Handler.permissions(router, action, Meta, (status: boolean, perms: any) => {
    Meta.permission = perms
    if (status) {
      if (id) {
        getData(id)
      } else {
        loading.value = false
      }
    } else {
      loading.value = false
    }
  })
}

const getData = (targetId: string | number) => {
  API.get(`${Meta.module}/${targetId}`, (status: number, res: any) => {
    if (status === 200) {
      const payload = res?.data ?? res ?? {}
      Object.keys(Meta.model).forEach((key) => {
        (dataModel.value as any)[key] = payload[key] ?? (Meta.model as any)[key]
      })
      // rental_code mungkin tidak ikut di response get_id (tidak ada join)
      // → cari dari rentalOptions yang sudah di-load, atau tunggu load selesai
      const resolveRentalCode = () => {
        if (payload.rental_code) {
          dataModel.value.rental_code = payload.rental_code
        } else if (payload.rental_id) {
          const found = rentalOptions.value.find((r) => r.id === payload.rental_id)
          if (found) {
            dataModel.value.rental_code = found.rental_code ?? null
          } else {
            // rentalOptions belum selesai load — coba lagi setelah 500ms
            setTimeout(resolveRentalCode, 500)
          }
        }
      }
      resolveRentalCode()
      dataModel.value.verified_by_name = payload.verified_by_name ?? null
    }
    loading.value = false
  }, Meta.app)
}

// ─── Save / Verify ─────────────────────────────────────────────

const save = (): Promise<number> => {
  // Hapus field UI-only sebelum kirim
  const payload: any = { ...dataModel.value }
  delete payload.rental_code
  delete payload.verified_by_name

  // Jika autoVerify aktif: kirim status langsung di payload create
  // Backend store() sudah handle verified_by, verified_at, invoice, & sync rental otomatis
  if (autoVerify.value) {
    payload.status = verifyStatus.value
    if (verifyNotes.value) payload.notes = verifyNotes.value
  } else {
    // Hapus status agar backend pakai default 'menunggu'
    delete payload.status
  }

  return new Promise((resolve) => {
    API.post(Meta.module, payload, (status: number, res: any) => {
      const newId = res?.data?.id ?? res?.data?.data?.id ?? null
      if (newId) dataModel.value.id = newId
      resolve(status)
    }, Meta.app)
  })
}

const verify = (targetId?: string | null): Promise<number> => {
  const id = targetId ?? dataModel.value.id
  if (!id) return Promise.resolve(600)
  if (!verifyStatus.value) {
    Helper.showError('Pilih status verifikasi terlebih dahulu.')
    return Promise.resolve(600)
  }

  return new Promise((resolve) => {
    API.put(
      `${Meta.module}/${id}/verify`,
      { status: verifyStatus.value, notes: verifyNotes.value || null },
      (status: number) => resolve(status),
      Meta.app
    )
  })
}

const submit = async () => {
  loading.value = true

  if (isEditMode.value) {
    const statusapi = await verify()
    if (statusapi === 200) {
      Helper.showSuccess('Verifikasi berhasil.')
      back()
    }
  } else {
    const saveStatus = await save()
    if (saveStatus === 200) {
      Helper.showSuccess(
        autoVerify.value
          ? 'Pembayaran disimpan dan langsung diverifikasi.'
          : 'Pembayaran berhasil disimpan.'
      )
      back()
    }
  }

  loading.value = false
}

const back = () => {
  emit('refreshEvent')
  router.back()
}

onMounted(init)
</script>