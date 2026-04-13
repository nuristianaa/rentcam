<template>
  <q-layout view="lHh LpR fFf">
    <DrawerComponent />
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import DrawerComponent from './drawer/DrawerComponent.vue'
import { authStore } from 'src/stores/auth'
import { subscribePush } from 'src/services/api/push-notif'
import { Dialog } from 'quasar'

const Auth = authStore()


const init = async () => {
  const hasSub = await checkSubscription()
  console.log('hassub', hasSub)

  if (!hasSub) {
    // Show custom modal asking for permission
    Dialog.create({
      title: 'Enable Notifications',
      message: 'To receive updates, please enable push notifications.',
      cancel: true,
      persistent: true,
      ok: {
        label: 'Allow Notifications',
        color: 'primary',
      },
    }).onOk(() => {
      void subscribePush(Auth.user?.username || '', Auth.user?.id)
    })
  }
}

const checkSubscription = async () => {
  const registration = await navigator.serviceWorker.ready
  const sub = await registration.pushManager.getSubscription()
  return !!sub
}

onMounted(async () => {
  if (Auth.getToken()) {
    await init()
  }
})

</script>
