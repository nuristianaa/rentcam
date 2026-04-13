<template>
  <q-page-sticky v-if="$q.fullscreen.isActive && exitBtnVisible" position="bottom-right" :offset="[18, 18]" style="z-index: 10000">
    <q-btn flat icon="fullscreen_exit" label="Exit Full Screen" @click="$q.fullscreen.toggle()" />
  </q-page-sticky>
  <div v-if="showDrawer && !$q.fullscreen.isActive">
    <q-header class="page-header">
      <q-toolbar class="header-toolbar">
        <q-btn flat dense round @click="toggleMenu = !toggleMenu" aria-label="Menu" icon="menu">
          <q-tooltip>Show / Hide Menu</q-tooltip>
        </q-btn>
        <q-toolbar-title class="row items-center"></q-toolbar-title>

        <div :class="`row items-center`">
          <!-- HOME -->
          <div class="q-px-xs">
            <q-btn round dense unelevated flat to="/home">
              <q-icon name="home" size="18px" class="cursor-pointer" />
              <q-tooltip>Home</q-tooltip>
            </q-btn>
          </div>

          <!-- REFRESH -->
          <div class="q-px-xs">
            <q-btn round dense unelevated flat @click="hardRefreshBrowser()">
              <q-icon name="refresh" size="18px" class="cursor-pointer" />
              <q-tooltip>Refresh</q-tooltip>
            </q-btn>
          </div>

          <!-- DARK MODE -->
          <div class="q-px-xs">
            <q-btn v-if="dark_mode == 'auto'" round dense unelevated flat @click="toggleDark(true)">
              <q-icon name="contrast" size="18px" class="cursor-pointer" />
              <q-tooltip>Color Scheme: Auto</q-tooltip>
            </q-btn>
            <q-btn v-else-if="dark_mode" round dense unelevated flat @click="toggleDark(false)">
              <q-icon name="dark_mode" size="18px" class="cursor-pointer" />
              <q-tooltip>Color Scheme: Dark</q-tooltip>
            </q-btn>
            <q-btn v-else-if="!dark_mode" round dense unelevated flat @click="toggleDark('auto')">
              <q-icon name="light_mode" size="18px" class="cursor-pointer" />
              <q-tooltip>Color Scheme: Light</q-tooltip>
            </q-btn>
          </div>

          <!-- FULL SCREEN -->
          <div class="q-px-xs">
            <q-btn round dense unelevated flat @click="$q.fullscreen.toggle()">
              <q-icon name="fullscreen" size="18px" class="cursor-pointer" />
              <q-tooltip>Full Screen</q-tooltip>
            </q-btn>
          </div>

          <!-- NOTIF -->
          <div class="q-px-xs">
            <q-btn :loading="loading" round dense unelevated flat size="sm">
              <q-icon name="o_notifications" size="18px" class="cursor-pointer" />
              <q-badge v-if="count_notif" color="red" text-color="white" floating>{{ count_notif }}</q-badge>
              <q-tooltip>Notifications</q-tooltip>
              <q-menu>
                <q-list>
                  <NotifList v-model="notif_list" @clear="clearNotif" @refreshEvent="onRefresh()" />
                </q-list>
              </q-menu>
            </q-btn>
          </div>

          <div v-if="hasToken" class="q-px-sm">
            <ProfilePopup v-model="user" @refresh-event="onRefresh(true)" />
          </div>
        </div>
      </q-toolbar>
    </q-header>
    <SidebarComp :refresh="refresh" :toggleMenu="toggleMenu" @refreshMenu="getUser" />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import SidebarComp from './SidebarComp.vue'
import ProfilePopup from './ProfilePopup.vue'
import NotifList from './NotifList.vue'
import Api from 'src/services/api'
import { Helper } from 'src/services/helper'
import { authStore } from 'src/stores/auth'
import { configStore } from 'src/stores/config'
import { Config } from 'src/services/config'
import { Screen } from 'quasar'

interface User {
  username: string | null
  name: string | null
  phone: string | null
  profile_picture: string | null
  user_type: string | null
  role: Record<string, unknown>
  menu: Record<string, unknown>
  menu_favorites: Array<any>
  table_configs: Array<any>
}

const API = new Api()
const Auth = authStore()
const Cfg = configStore()

const hasToken = ref(!!Auth.getToken())
const hasMenu = ref(Array.isArray(Auth.getMenu()) && Auth.getMenu().length > 0)
const showDrawer = ref(hasToken.value || hasMenu.value)

watch(
  () => Auth.printMode,
  (newVal) => {
    showDrawer.value = !newVal
  },
  { immediate: true } // langsung sync saat komponen mounted
)

const user = ref<User>({
  username: null,
  name: null,
  phone: null,
  profile_picture: null,
  user_type: null,
  role: { permissions: [] },
  menu: { menu_items: [] },
  menu_favorites: [],
  table_configs: []
})

const dark_mode = ref<'auto' | boolean>('auto')
const notif_list = ref([])
const count_notif = ref<number | null>(null)
const loading = ref(false)
const refresh = ref(0)
const toggleMenu = ref(false)
const company_code = ref<string | null>(null)
const vendor_code = ref<string | null>(null)
const companyOpt = Auth.getCompanies() as any[]
const vendorOpt = Auth.getVendors() as any[]

let ws: WebSocket | null = null
const wsConnected = ref(false)
const wsTopic = 'notification' // contoh topic, bisa dinamis per user

const toggleDark = (value: 'auto' | boolean) => {
  dark_mode.value = value
  Cfg?.setDarkMode(value)
  refresh.value++
}

const updateCompany = () => {
  if (company_code.value) Auth?.setCompany(company_code.value)
  setTimeout(() => window.location.reload(), 300)
}

const updateVendor = () => {
  if (vendor_code.value) Auth?.setVendor(vendor_code.value)
  setTimeout(() => window.location.reload(), 300)
}

const getUser = async () => {
  if (!hasToken.value) return
  if (API && Config) {
    await API.get(
      'me',
      (status: number, data: User) => {
        if (status === 200) {
          user.value = data
          Auth?.setUser(data)
          refresh.value++
        }
      },
      Config.app()
    )
  }
}

const getNotif = async () => {
  notif_list.value = []
  const endpoint = 'me/notifications?where=is_read:false'
  if (API && Config) {
    await API.get(
      endpoint,
      (status: number, data: { unread: number; items: never[] }) => {
        loading.value = false
        if (status === 200) {
          count_notif.value = data.unread
          notif_list.value = data.items || []
        }
      },
      'identity'
    )
  }
}

const clearNotif = () => {
  if (API && Config) {
    API.get(
      'me/notifications?clear=true',
      (status: number) => {
        if (status === 200) {
          notif_list.value = []
          count_notif.value = 0
        }
      },
      'identity'
    )
  }
}

const onRefresh = async (hard = false) => {
  if (!hasToken.value) return
  loading.value = true
  user.value = Auth?.getUser()
  company_code.value = Auth?.getCompanyCode() || null
  if (user.value.user_type == 'vendor') vendor_code.value = Auth?.getVendorCode() || null
  dark_mode.value = Cfg?.getDarkMode() || false

  if (hard || !user.value.username) await getUser()
  else await getNotif()
}

const hardRefreshBrowser = async () => {
  await onRefresh(true)
  // Attempt to clear all cookies
  document.cookie.split(';').forEach((cookie) => {
    const eqPos = cookie.indexOf('=')
    const name = eqPos > -1 ? cookie.slice(0, eqPos) : cookie
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/`
  })
  window.location.reload()
}

const exitBtnVisible = ref(false)
const threshold = 200 // distance from top-right corner in px

function onMove(e: MouseEvent) {
  // const nearTop = e.clientY < threshold
  const nearBottom = e.clientY > window.innerHeight - threshold
  const nearRight = e.clientX > window.innerWidth - threshold
  exitBtnVisible.value = nearBottom && nearRight && !!document.fullscreenElement
}

const swMessageHandler = (event: MessageEvent) => {
  const data = event.data
  if (!data?.type) return
  switch (data.type) {
    case 'NEW_NOTIFICATION': {
      const msg = data.payload
      Helper.showToast(msg.title ?? msg.body, 'primary', 15000, 'bottom', msg.body)
      getNotif()
      break
    }
  }
}

const connectWS = () => {
  if (!hasToken.value || !user.value.username) return

  const userId = user.value.id // atau user id numerik dari backend
  const wsUrl = `ws://localhost:8190/ws?user_id=${userId}&topic=${wsTopic}`

  ws = new WebSocket(wsUrl)

  ws.onopen = () => {
    console.log('WebSocket connected')
    wsConnected.value = true
  }

  ws.onmessage = (event: MessageEvent) => {
    const data = JSON.parse(event.data)
    console.log('WS message received', data)

    if (data.type === wsTopic) {
      // tampilkan toast atau update notif list
      Helper.showToast(data.message, 'primary', 10000, 'bottom', data.message)
      getNotif() // update notif list dari API
    }
  }

  ws.onclose = () => {
    console.log('WebSocket disconnected')
    wsConnected.value = false
    // reconnect otomatis setelah 5 detik
    setTimeout(connectWS, 5000)
  }

  ws.onerror = (err) => {
    console.error('WebSocket error', err)
    ws?.close()
  }
}

onMounted(() => {
  if (hasToken.value) {
    onRefresh()
    connectWS()
  }
  if (Screen.lt.md) exitBtnVisible.value = true
  else window.addEventListener('mousemove', onMove)

  navigator.serviceWorker.addEventListener('message', swMessageHandler)
})
onBeforeUnmount(() => {
  window.removeEventListener('mousemove', onMove)
  navigator.serviceWorker.removeEventListener('message', swMessageHandler)
})
</script>