<template>
  <div>
    <s-loading v-if="loading" />
    <h-detail v-else :meta="Meta" :modal="dataModel" @back="back" @edit="edit">

      <!-- Tombol Toggle Visible -->
      <template #actions>
        <q-btn
          v-if="Meta.permission.update"
          :label="dataModel.is_visible ? 'Sembunyikan' : 'Tampilkan'"
          :color="dataModel.is_visible ? 'negative' : 'positive'"
          :icon="dataModel.is_visible ? 'visibility_off' : 'visibility'"
          unelevated
          @click="confirmToggleVisible"
        />
      </template>

      <div class="row">
        <div class="col-12 q-pa-sm">
          <div class="form-title">Detail Ulasan</div>
        </div>
        <d-input col="6"  :value="dataModel.rental_code"   label="No. Order Rental" />
        <d-input col="6"  :value="dataModel.item_name"     label="Item" />
        <d-input col="6"  :value="dataModel.customer_name" label="Pelanggan" />
        <d-input col="6"  :value="dataModel.rating ? `${dataModel.rating} / 5` : '-'" label="Rating" />
        <d-input col="6"  :value="dataModel.is_visible ? 'Ditampilkan' : 'Disembunyikan'" label="Status Tampil" />
        <d-input col="12" :value="dataModel.comment"       label="Komentar" />
      </div>
    </h-detail>

    <!-- Dialog konfirmasi toggle visible -->
    <q-dialog v-model="dialogVisible">
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">
            {{ dataModel.is_visible ? 'Sembunyikan Ulasan?' : 'Tampilkan Ulasan?' }}
          </div>
        </q-card-section>
        <q-card-section class="text-body2 text-grey-7">
          Ulasan akan {{ dataModel.is_visible ? 'disembunyikan dari publik' : 'ditampilkan kembali ke publik' }}.
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Batal" v-close-popup />
          <q-btn
            :label="dataModel.is_visible ? 'Sembunyikan' : 'Tampilkan'"
            :color="dataModel.is_visible ? 'negative' : 'positive'"
            unelevated
            @click="toggleVisible"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Api from 'src/services/api'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import type { DataModel } from './meta'
import { Meta } from './meta'

const props = defineProps<{ props?: { id?: string | number } }>()
const emit  = defineEmits(['refreshEvent', 'editEvent'])

const router = useRouter()
const API    = new Api()

const loading       = ref(true)
const dataModel     = ref<DataModel>(Meta.model)
const dialogVisible = ref(false)

const init = () => {
  Handler.permissions(router, 'read', Meta, (status: boolean, data: any) => {
    Meta.permission = data
    if (status && props.props?.id) getData(props.props.id)
  })
}

const getData = (id: string | number) => {
  loading.value = true
  API.get(`${Meta.module}/${id}`, (status: number, data: any) => {
    loading.value = false
    if (status === 200) dataModel.value = data
  })
}

const confirmToggleVisible = () => {
  dialogVisible.value = true
}

const toggleVisible = () => {
  const payload = { is_visible: !dataModel.value.is_visible }
  API.put(`${Meta.module}/${dataModel.value.id}/toggle-visible`, payload, (status: number) => {
    if (status === 200) {
      Helper.showSuccess(
        payload.is_visible ? 'Ulasan berhasil ditampilkan.' : 'Ulasan berhasil disembunyikan.'
      )
      dialogVisible.value = false
      getData(dataModel.value.id!)
    }
  })
}

const back = () => emit('refreshEvent')
const edit = () => emit('editEvent', { id: dataModel.value.id })

onMounted(() => init())
</script>