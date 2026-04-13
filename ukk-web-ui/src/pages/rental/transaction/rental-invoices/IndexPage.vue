<template>
  <div>
    <s-page :meta="Meta">
      <s-loading v-if="loading" />
      <s-table
        v-else
        :meta="Meta"
        :refresh="refresh"
      >
      </s-table>
    </s-page>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Handler } from 'src/services/handler'
import { Meta } from './meta'

const router = useRouter()
const loading = ref(true)
const refresh = ref(0)

const init = () => {
  Handler.permissions(router, 'browse', Meta, (status, data) => {
    Meta.permission = data
    if (status) loading.value = false
  })
}

onMounted(init)
</script>
