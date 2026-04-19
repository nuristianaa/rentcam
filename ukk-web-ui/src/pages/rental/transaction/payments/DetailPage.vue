<template>
  <div>
    <s-loading v-if="loading" />
    <h-detail v-else :meta="Meta" :model="dataModel" @back="back">

      <!-- Tombol aksi di header -->
      <template #actions>
        <q-btn
          v-if="dataModel.status === 'menunggu' && Meta.permission.update"
          label="Verify"
          icon="verified"
          color="positive"
          unelevated
          @click="openVerifyDialog"
        />
      </template>

      <div class="row q-pa-sm">

        <!-- Info utama -->
        <f-card title="Payment Detail" col="6">
          <s-list
            v-for="(item, i) in viewList"
            :key="i"
            :data="item"
          />
        </f-card>

        <!-- Status badge + log -->
        <f-card title="Status & Log" col="6">
          <div class="q-mb-md">
            <div class="text-caption text-grey q-mb-xs">Status</div>
            <q-badge
              :color="statusColor(dataModel.status)"
              :label="statusLabel(dataModel.status)"
              class="text-subtitle2 q-pa-sm"
            />
          </div>
          <div v-if="dataModel.verified_by_name" class="q-mb-sm">
            <div class="text-caption text-grey">Verified by</div>
            <div class="text-body2">{{ dataModel.verified_by_name }}</div>
          </div>
          <div v-if="dataModel.verified_at" class="q-mb-sm">
            <div class="text-caption text-grey">Verify time</div>
            <div class="text-body2">{{ formatDate(dataModel.verified_at) }}</div>
          </div>
          <q-separator class="q-my-md" />
          <log-info :data="dataModel" />
        </f-card>

      </div>
    </h-detail>

    <!-- Dialog Verifikasi -->
    <q-dialog v-model="verifyDialog" persistent>
      <q-card style="min-width: 400px">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Verify Payment</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section>
          <div class="text-body2 q-mb-md">
            Rental: <strong>{{ dataModel.rental_code }}</strong> —
            Amount: <strong>{{ formatCurrency(dataModel.amount) }}</strong>
          </div>

          <q-option-group
            v-model="verifyStatus"
            :options="verifyOptions"
            color="primary"
            inline
            class="q-mb-md"
          />

          <q-input
            v-model="verifyNotes"
            label="Notes (optional)"
            type="textarea"
            outlined
            autogrow
            rows="3"
          />
        </q-card-section>

        <q-card-actions align="right" class="q-px-md q-pb-md">
          <q-btn flat label="Cancel" v-close-popup />
          <q-btn
            :label="verifyStatus === 'terverifikasi' ? 'Verify ✓' : 'Reject ✗'"
            :color="verifyStatus === 'terverifikasi' ? 'positive' : 'negative'"
            unelevated
            :loading="verifyLoading"
            @click="submitVerify"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Api from 'src/services/api'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Meta } from './meta'
import type { DataModel } from './meta'

const route  = useRoute()
const router = useRouter()
const id     = Array.isArray(route.params?.id) ? route.params.id[0] : (route.params?.id ?? null)
const API    = new Api()

const loading      = ref(true)
const verifyDialog  = ref(false)
const verifyLoading = ref(false)
const verifyStatus  = ref<'terverifikasi' | 'ditolak'>('terverifikasi')
const verifyNotes   = ref('')

const dataModel = ref<DataModel>({ ...Meta.model })
const viewList  = ref<{ label: string; value: any }[]>([])

const verifyOptions = [
  { label: 'Verified', value: 'terverifikasi' },
  { label: 'Rejected',       value: 'ditolak' },
]

// ─── Helpers ───────────────────────────────────────────────────

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

const formatDate = (val: string | null) => {
  if (!val) return '-'
  return new Date(val).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
}

// ─── Data ──────────────────────────────────────────────────────

const init = () => {
  dataModel.value = { ...Meta.model }
  Handler.permissions(router, 'read', Meta, (status: boolean) => {
    if (status) getData(id)
    else loading.value = false
  })
}

const getData = (targetId?: string | number | null) => {
  if (!targetId) return (loading.value = false)

  API.get(`${Meta.module}/${targetId}`, (status: number, res: any) => {
    if (status === 200) {
      const payload = res?.data ?? res ?? {}
      // Assign field-by-field untuk menghindari reaktif loop di QTd
      Object.keys(Meta.model).forEach((key) => {
        (dataModel.value as any)[key] = payload[key] ?? null
      })
      dataModel.value.rental_code      = payload.rental_code ?? null
      dataModel.value.verified_by_name = payload.verified_by_name ?? null

      viewList.value = buildViewList(dataModel.value)
    }
    loading.value = false
  }, Meta.app)
}

const buildViewList = (data: DataModel) => {
  return [
    { label: 'Rental Code',   value: data.rental_code },
    { label: 'Type',          value: Meta.typeOptions.find((o) => o.value === data.type)?.label ?? data.type },
    { label: 'Amount',        value: formatCurrency(data.amount) },
    { label: 'Method',        value: data.payment_method ?? '-' },
    { label: 'Bank',          value: data.bank_name ?? '-' },
    { label: 'Account No.',  value: data.account_number ?? '-' },
    { label: 'Payment Date',     value: formatDate(data.paid_at) },
    { label: 'Notes',       value: data.notes ?? '-' },
  ].filter((item) => item.value && item.value !== '-')
}

// ─── Verify ────────────────────────────────────────────────────

const openVerifyDialog = () => {
  verifyStatus.value = 'terverifikasi'
  verifyNotes.value  = ''
  verifyDialog.value = true
}

const submitVerify = () => {
  if (!dataModel.value.id) return
  verifyLoading.value = true

  API.put(
    `${Meta.module}/${dataModel.value.id}/verify`,
    { status: verifyStatus.value, notes: verifyNotes.value || null },
    (status: number) => {
      verifyLoading.value = false
      if (status === 200) {
        verifyDialog.value = false
        Helper.showSuccess(
          verifyStatus.value === 'terverifikasi'
            ? 'Payment verified successfully. Invoice will be generated automatically.'
            : 'Payment rejected.'
        )
        getData(id) // refresh tanpa full reload
      }
    },
    Meta.app
  )
}

const back = () => router.back()

onMounted(init)
</script>