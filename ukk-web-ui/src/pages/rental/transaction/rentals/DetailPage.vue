<template>
  <div>
    <s-loading v-if="loading" />
    <h-detail v-else :meta="Meta" :model="dataModel" @back="back">

      <!-- ─── Action Buttons ───────────────────────────────────── -->
      <template #buttons>
        <div class="row q-gutter-xs q-mb-sm">

          <!-- Update Status -->
          <q-btn
            v-if="allowedNextStatuses.length"
            label="Ubah Status"
            icon="swap_horiz"
            color="primary"
            unelevated
            size="sm"
            @click="openStatusDialog"
          />

          <!-- Checkout -->
          <q-btn
            v-if="dataModel.status === 'diproses' && !checkoutDone"
            label="Checkout"
            icon="logout"
            color="purple"
            unelevated
            size="sm"
            @click="openCheckpointDialog('checkout')"
          />

          <!-- Checkin -->
          <q-btn
            v-if="dataModel.status === 'aktif' && !checkinDone"
            label="Checkin"
            icon="login"
            color="teal"
            unelevated
            size="sm"
            @click="openCheckpointDialog('checkin')"
          />

          <!-- Generate Invoice (manual, admin only) -->
          <q-btn
            label="Generate Invoice"
            icon="receipt_long"
            color="green-8"
            unelevated
            size="sm"
            :loading="loadingInvoice"
            :disable="!canGenerateInvoiceEnabled"
            @click="generateInvoice"
          />
          <q-tooltip v-if="!canGenerateInvoiceEnabled">
            {{ canGenerateInvoiceTooltip }}
          </q-tooltip>

          <!-- Lihat Profil Customer -->
          <q-btn
            v-if="dataModel.customer_id"
            label="Profil Customer"
            icon="person_search"
            color="blue-grey"
            unelevated
            size="sm"
            @click="openCustomerProfile"
          />
        </div>
      </template>

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
                <q-td colspan="3" class="text-right">Total</q-td>
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
          <div class="q-mt-sm text-caption text-grey-6">
            {{ verifiedPayment ? `Pembayaran terverifikasi ditemukan: ${formatCurrency(verifiedPayment.amount)} (${verifiedPayment.payment_method ?? 'tanpa metode'})` : 'Tidak ada pembayaran terverifikasi untuk rental ini.' }}
          </div>
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

    <!-- ─────────────────────────────────────────────────────────
         Dialog: Update Status
    ─────────────────────────────────────────────────────────── -->
    <q-dialog v-model="statusDialog.show" persistent>
      <q-card style="min-width: 360px">
        <q-card-section class="bg-primary text-white">
          <div class="text-h6">Ubah Status Rental</div>
        </q-card-section>
        <q-card-section class="q-col-gutter-sm">
          <q-select
            v-model="statusDialog.status"
            label="Status Baru"
            :options="allowedNextStatuses"
            option-label="label"
            option-value="value"
            emit-value
            map-options
            outlined
            dense
          />
          <q-input
            v-model="statusDialog.notes"
            label="Catatan"
            type="textarea"
            rows="3"
            outlined
            dense
            class="q-mt-sm"
          />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Batal" @click="statusDialog.show = false" />
          <q-btn
            unelevated
            color="primary"
            label="Simpan"
            :loading="statusDialog.loading"
            :disable="!statusDialog.status"
            @click="submitStatus"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- ─────────────────────────────────────────────────────────
         Dialog: PDF Preview Invoice
    ─────────────────────────────────────────────────────────── -->
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
            <div v-if="pdfLoading">
              Memuat preview invoice...
            </div>
            <div v-else>
              Tidak ada preview saat ini. Tutup dan coba lagi.
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- ─────────────────────────────────────────────────────────
         Dialog: Checkout / Checkin
    ─────────────────────────────────────────────────────────── -->
    <q-dialog v-model="checkpointDialog.show" persistent>
      <q-card style="min-width: 420px">
        <q-card-section :class="checkpointDialog.type === 'checkout' ? 'bg-purple text-white' : 'bg-teal text-white'">
          <div class="text-h6 row items-center q-gutter-xs">
            <q-icon :name="checkpointDialog.type === 'checkout' ? 'logout' : 'login'" />
            {{ checkpointDialog.type === 'checkout' ? 'Checkout — Serahkan Alat' : 'Checkin — Terima Alat Kembali' }}
          </div>
        </q-card-section>
        <q-card-section class="q-col-gutter-sm">

          <!-- Kondisi alat -->
          <q-select
            v-model="checkpointDialog.condition"
            label="Kondisi Alat"
            :options="conditionOptions"
            option-label="label"
            option-value="value"
            emit-value
            map-options
            outlined
            dense
          />
          <q-input
            v-if="checkpointDialog.condition && checkpointDialog.condition !== 'baik'"
            v-model="checkpointDialog.condition_notes"
            label="Keterangan Kondisi"
            type="textarea"
            rows="2"
            outlined
            dense
            class="q-mt-xs"
          />

          <!-- Checklist -->
          <div class="q-mt-sm">
            <div class="text-caption text-grey-7 q-mb-xs">Checklist</div>
            <div v-for="(cl, ci) in checkpointDialog.checklist" :key="ci" class="row items-center q-gutter-xs q-mb-xs">
              <q-checkbox v-model="cl.ok" size="sm" />
              <q-input v-model="cl.label" dense borderless placeholder="Label" class="col" />
              <q-input
                v-if="!cl.ok"
                v-model="cl.note"
                dense borderless
                placeholder="Catatan"
                class="col"
              />
              <q-btn flat round dense icon="close" color="negative" size="xs" @click="removeChecklist(ci)" />
            </div>
            <q-btn flat size="xs" icon="add" color="primary" label="Tambah item checklist" @click="addChecklist" />
          </div>

          <!-- Catatan -->
          <q-input
            v-model="checkpointDialog.notes"
            label="Catatan"
            type="textarea"
            rows="2"
            outlined
            dense
            class="q-mt-sm"
          />

        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Batal" @click="checkpointDialog.show = false" />
          <q-btn
            unelevated
            :color="checkpointDialog.type === 'checkout' ? 'purple' : 'teal'"
            :label="checkpointDialog.type === 'checkout' ? 'Serahkan Alat' : 'Terima Alat'"
            :loading="checkpointDialog.loading"
            @click="submitCheckpoint"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

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

        <q-card-section v-if="customerProfileDialog.loading" class="text-center q-py-lg">
          <q-spinner color="primary" size="40px" />
        </q-card-section>

        <template v-else>
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
              rounded dense
              class="bg-amber-1 text-amber-10 q-mt-sm"
            >
              <template #avatar><q-icon name="warning" color="amber-8" /></template>
              Profil customer <strong>belum lengkap</strong>. Pastikan nama, no. HP, alamat, dan foto KTP sudah terisi.
            </q-banner>
            <q-banner v-else rounded dense class="bg-green-1 text-green-9 q-mt-sm">
              <template #avatar><q-icon name="check_circle" color="green-7" /></template>
              Profil customer sudah lengkap dan siap rental.
            </q-banner>
          </q-card-section>
        </template>
      </q-card>
    </q-dialog>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, defineComponent, h } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Api from 'src/services/api'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Meta } from './meta'
import { Config } from 'src/services/config'
import { authStore } from 'src/stores/auth'

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

const loading = ref(true)
const dataModel = ref<any>({})
const viewList = ref<{ label: string; value: any }[]>([])
const loadingInvoice = ref(false)
const pdfLoading = ref(false)

// ─── Customer Profile Dialog ────────────────────────────────
const customerProfileDialog = ref({
  show:     false,
  loading:  false,
  data:     null as any,
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
  customerProfileDialog.value = { show: true, loading: true, data: null, initials: '-' }
  API.get(`auth/users/${customerId}`, (status: number, data: any) => {
    const u = data?.data ?? data
    customerProfileDialog.value.loading = false
    if (status === 200) {
      customerProfileDialog.value.data     = u
      customerProfileDialog.value.initials = (u?.name ?? '?').charAt(0).toUpperCase()
    }
  }, 'identity')
}

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
  return new Promise((resolve) => {
    API.get(
      `transaction/rental-invoices/${invoiceId}/${endpoint}`,
      (_status: number, _data: any, _message: string, response: any) => {
        if (!response || !response.data) {
          resolve(null)
          return
        }
        resolve(response.data)
      },
      Meta.app,
      'blob'
    )
  })
}

const openPdfPreview = async (invoice: any) => {
  pdfPreviewDialog.value = { show: true, url: '', title: invoice.invoice_code ?? 'Invoice' }
  pdfLoading.value = true
  const blob = await fetchPdfBlob(invoice.id, 'preview-pdf')
  pdfLoading.value = false

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

// ─── Computed: allowed status transitions ────────────────────
const allowedNextStatuses = computed(() =>
  Meta.statusFlowOptions[dataModel.value.status ?? ''] ?? []
)

// ─── Table columns ───────────────────────────────────────────
const itemColumns = [
  { name: 'item_name',      label: 'Item',       field: 'item_name',      align: 'left'  as const },
  { name: 'quantity',       label: 'Qty',        field: 'quantity',       align: 'right' as const },
  { name: 'price_per_day',  label: 'Harga/Hari', field: 'price_per_day',  align: 'right' as const },
  { name: 'deposit_amount', label: 'Deposit',    field: 'deposit_amount', align: 'right' as const },
  { name: 'subtotal',       label: 'Subtotal',   field: 'subtotal',       align: 'right' as const },
]

const paymentColumns = [
  { name: 'rental_code',    label: 'Kode Rental',     field: 'rental_code',    align: 'left'   as const },
  { name: 'type',           label: 'Tipe',            field: 'type',           align: 'left'   as const },
  { name: 'status',         label: 'Status',          field: 'status',         align: 'left'   as const },
  { name: 'amount',         label: 'Jumlah',          field: 'amount',         align: 'right'  as const },
  { name: 'payment_method', label: 'Metode',          field: 'payment_method', align: 'left'   as const },
  { name: 'bank_name',      label: 'Bank',            field: 'bank_name',      align: 'left'   as const },
  { name: 'account_number', label: 'No. Rekening',    field: 'account_number', align: 'left'   as const },
  { name: 'verified_by_name', label: 'Diverifikasi Oleh', field: 'verified_by_name', align: 'left' as const },
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

const verifiedPayment = computed(() => {
  const payments = dataModel.value.payments ?? []
  return payments.find((p: any) => {
    const status = (p.status ?? '').toString().toLowerCase()
    return status === 'terverifikasi' || status === 'verified' || !!p.verified_at
  }) ?? null
})

const hasInvoice = computed(() => (dataModel.value.invoices ?? []).length > 0)
const latestInvoice = computed(() => (dataModel.value.invoices ?? [])[0] ?? null)

const canGenerateInvoice = computed(() => true)
const canGenerateInvoiceEnabled = computed(() => !!verifiedPayment.value && !hasInvoice.value)
const canGenerateInvoiceTooltip = computed(() => {
  if (hasInvoice.value) return 'Invoice sudah dibuat. Gunakan tombol preview untuk melihat invoice.'
  return 'Butuh pembayaran terverifikasi untuk membuat invoice.'
})

// ─── Dialogs ─────────────────────────────────────────────────
const statusDialog = ref({
  show: false,
  status: null as string | null,
  notes: null as string | null,
  loading: false,
})

const conditionOptions = [
  { label: 'Baik',         value: 'baik' },
  { label: 'Cacat Ringan', value: 'cacat_ringan' },
  { label: 'Rusak',        value: 'rusak' },
  { label: 'Hilang',       value: 'hilang' },
]

const checkpointDialog = ref({
  show:             false,
  type:             'checkout' as 'checkout' | 'checkin',
  condition:        null as string | null,
  condition_notes:  null as string | null,
  checklist:        [] as { label: string; ok: boolean; note: string }[],
  notes:            null as string | null,
  loading:          false,
})

const openStatusDialog = () => {
  statusDialog.value = { show: true, status: null, notes: null, loading: false }
}

const openCheckpointDialog = (type: 'checkout' | 'checkin') => {
  checkpointDialog.value = {
    show: true, type,
    condition: null, condition_notes: null,
    checklist: [], notes: null, loading: false,
  }
}

const addChecklist = () => {
  checkpointDialog.value.checklist.push({ label: '', ok: true, note: '' })
}
const removeChecklist = (i: number) => {
  checkpointDialog.value.checklist.splice(i, 1)
}

// ─── Format helpers ──────────────────────────────────────────
const formatCurrency = (val: number | null) =>
  new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(val ?? 0)

const formatDatetime = (val: string | null) =>
  val ? new Date(val).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' }) : '—'

// ─── API Actions ─────────────────────────────────────────────
const submitStatus = () => {
  if (!statusDialog.value.status) return
  statusDialog.value.loading = true
  API.put(`${Meta.module}/${id}/status`, {
    status:  statusDialog.value.status,
    notes:   statusDialog.value.notes,
  }, (status: number) => {
    statusDialog.value.loading = false
    if (status === 200) {
      statusDialog.value.show = false
      Helper.showSuccess('Status berhasil diubah.')
      getData(id)
    }
  }, Meta.app)
}

const submitCheckpoint = () => {
  const d = checkpointDialog.value
  d.loading = true
  const endpoint = `${Meta.module}/${id}/${d.type}`
  API.post(endpoint, {
    condition:       d.condition,
    condition_notes: d.condition_notes,
    checklist:       d.checklist.length ? d.checklist : null,
    notes:           d.notes,
  }, (status: number) => {
    d.loading = false
    if (status === 200) {
      d.show = false
      Helper.showSuccess(`${d.type === 'checkout' ? 'Checkout' : 'Checkin'} berhasil.`)
      getData(id)
    }
  }, Meta.app)
}

const generateInvoice = () => {
  if (!verifiedPayment.value) {
    Helper.showError('Belum ada pembayaran yang terverifikasi untuk rental ini.')
    return
  }

  loadingInvoice.value = true
  API.post(
    `transaction/rental-invoices/generate-from-payment/${verifiedPayment.value.id}`,
    {},
    (status: number) => {
      loadingInvoice.value = false
      if (status === 200) {
        Helper.showSuccess('Invoice berhasil dibuat.')
        getData(id)
      }
    },
    Meta.app
  )
}

// ─── Init & Load ─────────────────────────────────────────────
const loadInvoices = (rentalId: string) => {
  API.get(`transaction/rental-invoices/by-rental/${rentalId}`, (status: number, data: any) => {
    if (status === 200) {
      const invoices = data?.data ?? data ?? []
      dataModel.value = { ...dataModel.value, invoices: Array.isArray(invoices) ? invoices : [] }
    }
  }, Meta.app)
}

const getData = (id?: string | number) => {
  if (!id) return (loading.value = false)

  API.get(`${Meta.module}/${id}`, (status: number, data: any) => {
    if (status === 200) {
      const payload = data?.data ?? data ?? {}
      dataModel.value = { ...payload }
      const config = {
        exclude: [
          'id', 'images', 'items', 'histories', 'checkpoints', 'invoices', 'payments',
          'created_by', 'updated_by', 'deleted_by',
          'created_at', 'updated_at', 'deleted_at',
        ],
        numbers: ['duration_days'],
        moneys:  ['subtotal', 'deposit_total', 'grand_total'],
        date:    ['start_date', 'end_date'],
        dateTime: [],
      }
      viewList.value = Handler.viewList(dataModel.value, config)
      // Load invoices terpisah karena tidak di-return oleh endpoint detail rental
      if (payload.id) loadInvoices(String(payload.id))
    }
    loading.value = false
  }, Meta.app)
}

const back = () => { router.back() }

onMounted(() => {
  dataModel.value = Helper.unreactive(Meta.model)
  Handler.permissions(router, 'read', Meta, (status) => {
    if (status) getData(id)
    else loading.value = false
  })
})
</script>