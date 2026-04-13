<template>
  <div>
    <s-page :meta="Meta">
      <s-loading v-if="loading" />
      <s-table
        v-else
        :meta="Meta"
        :refresh="refresh"
        @add="add"
        @edit="edit"
        @detail="detail"
      >
        <!-- Tombol toggle visible per baris -->
        <template v-slot:body-action="props">
          <q-btn
            v-if="Meta.permission.update"
            class="bg-soft"
            dense round flat
            :color="props.props.row.is_visible ? 'negative' : 'positive'"
            :icon="props.props.row.is_visible ? 'visibility_off' : 'visibility'"
            @click="toggleVisible(props.props.row)"
          >
            <q-tooltip>{{ props.props.row.is_visible ? 'Sembunyikan' : 'Tampilkan' }}</q-tooltip>
          </q-btn>
        </template>
      </s-table>
    </s-page>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import Api from 'src/services/api'
import { Meta } from './meta'

const router  = useRouter()
const route   = useRoute()
const loading = ref(true)
const refresh = ref(0)
const API     = new Api()

const init = () => {
  Handler.permissions(router, 'browse', Meta, (status, data) => {
    Meta.permission = data
    if (status) loading.value = false
  })
}

const add = () => {
  router.push({
    name: `add-${Meta.module}`,
    query: route.query
  })
}

const edit = (data: any) => {
  router.push({
    name: `edit-${Meta.module}`,
    params: { id: data.id },
    query: route.query
  })
}

const detail = (data: any) => {
  router.push({
    name: `view-${Meta.module}`,
    params: { id: data.id },
    query: route.query
  })
}

const toggleVisible = (row: any) => {
  const payload = { is_visible: !row.is_visible }
  API.put(`${Meta.module}/${row.id}/toggle-visible`, payload, (status: number) => {
    if (status === 200) {
      Helper.showSuccess(
        payload.is_visible ? 'Ulasan berhasil ditampilkan.' : 'Ulasan berhasil disembunyikan.'
      )
      refresh.value++
    }
  }, Meta.app)
}

onMounted(init)
</script>