<template>
  <div>
    <s-page :meta="Meta">
      <s-loading v-if="loading" />
      <s-table
        v-else
        :meta="Meta"
        :refresh="refresh"
        @detail="detail"
      >
        <template v-slot:top-buttons>
           <q-btn v-if="Meta.permission.read" class="bg-primary text-white q-mr-sm" dense flat @click="$router.push('/rental/transaction/reports')" icon="print" label="Laporan Transaksi" />
        </template>
      </s-table>
    </s-page>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Meta } from './meta'

const router = useRouter()
const route = useRoute()
const loading = ref(true)
const refresh = ref(0)

const init = () => {
  Handler.permissions(router, 'browse', Meta, (status, data) => {
    Meta.permission = data
    if (status) loading.value = false
  })
}

const detail = (data: any) => {
  router.push({
    name: `view-transaction/rentals`,
    params: { id: data.id },
    query: route.query
  })
}

onMounted(init)
</script>
