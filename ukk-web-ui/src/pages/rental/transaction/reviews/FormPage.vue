<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else :meta="Meta" @submit="submit" @back="back">
      <div class="row">

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

        <!-- Item -->
        <f-select
          v-model="dataModel.item_id"
          col="6"
          :label="Lang.module(Meta, 'item_id')"
          :options="itemOptions"
          :option-label="(v) => v.name"
          option-value="id"
          required
        />

        <!-- Rating -->
        <f-select
          v-model="dataModel.rating"
          col="6"
          :label="Lang.module(Meta, 'rating')"
          :options="Meta.ratingOptions"
          :option-label="(v) => v.label"
          option-value="value"
          required
        />

        <!-- Komentar -->
        <f-textarea
          v-model="dataModel.comment"
          col="12"
          :label="Lang.module(Meta, 'comment')"
        />

      </div>
    </h-form>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, onMounted } from 'vue'
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

const loading      = ref(true)
const dataModel    = ref<DataModel>({ ...Meta.model })
const rentalOptions = ref<any[]>([])
const itemOptions  = ref<any[]>([])

const loadRentals = () => {
  API.get('transaction/rentals', (status: number, data: any) => {
    if (status === 200) rentalOptions.value = data?.data ?? data
  }, Meta.app)
}

const loadItems = () => {
  API.get('master/items', (status: number, data: any) => {
    if (status === 200) itemOptions.value = data?.data ?? data
  }, Meta.app)
}

const onRentalChange = (val: string) => {
  const found = rentalOptions.value.find((r) => r.id === val)
  if (found) dataModel.value.rental_code = found.rental_code
}

const init = () => {
  dataModel.value = Helper.unreactive(Meta.model)
  loadRentals()
  loadItems()
  const action = id ? 'update' : 'create'
  Handler.permissions(router, action, Meta, (status: boolean, data: any) => {
    Meta.permission = data
    if (status) {
      if (id) getData(id)
      else loading.value = false
    } else {
      loading.value = false
    }
  })
}

const getData = (id: string | number) => {
  API.get(`${Meta.module}/${id}`, (status: number, data: any) => {
    if (status === 200) dataModel.value = data
    loading.value = false
  }, Meta.app)
}

const save = async () => {
  let statusapi = 600
  await API.post(Meta.module, dataModel.value, (status: number, _data: any) => {
    statusapi = status
    dataModel.value.id = _data.id
  }, Meta.app)
  return statusapi
}

const update = async () => {
  let statusapi = 600
  await API.put(`${Meta.module}/${dataModel.value.id}`, dataModel.value, (status: number, _data: any) => {
    statusapi = status
  }, Meta.app)
  return statusapi
}

const submit = async () => {
  loading.value = true

  const status = dataModel.value.id ? await update() : await save()

  if (status === 200) {
    Helper.showSuccess('Data berhasil disimpan.')
    back()
  }

  loading.value = false
}

const back = () => {
  emit('refreshEvent')
  router.back()
}

onMounted(init)
</script>