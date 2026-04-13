<template>
  <div>
    <s-loading />
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { useRouter } from 'vue-router'
import { authStore } from 'src/stores/auth'
import { onMounted } from 'vue'

const API = new Api()
const Auth = authStore()
const router = useRouter()

const init = () => {
  if (Auth.getToken()) router.push('/home')
  else {
    router.push('/login')
  }
}

onMounted(() => {
  init()
})
</script>
