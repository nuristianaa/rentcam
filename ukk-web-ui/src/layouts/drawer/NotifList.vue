<template>
  <div class="pt">
    <q-item-label class="row q-px-md justify-between">
      <div class="q-my-sm q-mr-sm text-info">Notifications</div>
      <q-btn flat dense no-caps label="View All" icon-right="open_in_new" @click="toPageNotif" />
      <q-btn flat dense no-caps color="negative" label="Clear All" icon-right="delete" @click="clear" />
    </q-item-label>
    <hr />
    <q-list>
      <div v-for="(notif, index) in modelValue" :key="`${index}-notif`">
        <q-item clickable v-ripple @click="readNotif(notif)">
          <q-item-section>
            <q-item-label class="text-primary text-bold">{{ notif.title }}</q-item-label>
            <q-item-label caption lines="2">
              <div v-html="notif.description"></div>
            </q-item-label>
          </q-item-section>
          <q-item-section side top>
            <q-item-label caption>{{ Helper.readDate(notif.created_at) }}</q-item-label>
            <q-icon :color="notif.color ?? 'secondary'" :icon="notif.icon ?? 'star'" />
          </q-item-section>
        </q-item>
        <q-separator />
      </div>
    </q-list>

    <!-- DIALOG DETAIL -->
    <q-dialog v-model="showDetail" @hide="emitRefreshEvent">
      <q-card position="right">
        <s-loading v-if="loading" />
        <div v-else class="row q-pa-lg">
          <div style="width: 100%">
            <div class="row justify-between">
              <div class="title q-pt-sm">{{ dataModel?.title }}</div>
              <q-icon v-if="dataModel?.icon" size="md" :color="dataModel?.color" text-color="white" :name="dataModel?.icon" />
            </div>
            <q-separator class="q-my-md" color="primary" />
            <div class="row q-my-md">
              <div class="col" v-html="dataModel?.description" />
            </div>
            <q-btn v-if="dataModel?.path" class="q-my-md" color="primary" icon="open_in_new" label="View" @click="toLink(dataModel.path)" />
            <log-info :data="dataModel" />
          </div>
        </div>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { Helper } from 'src/services/helper'
import { ref } from 'vue'

interface Notification {
  id?: string | number
  _id?: string | number
  title: string
  description: string
  created_at: string
  color?: string
  icon?: string
  path?: string
}

const props = defineProps<{
  modelValue: Notification[]
}>()

const emit = defineEmits(['refreshEvent', 'clear'])

const API = new Api()
const loading = ref(true)
const dataModel = ref<Notification | null>(null)
const showDetail = ref(false)

function readNotif(notif: Notification) {
  const id = notif.id || notif._id
  loading.value = true
  dataModel.value = null

  // Mock API call, replace with actual API logic
  API.get(`auth/notifications/${id}`, (status: number, data: Notification) => {
    if (status === 200) {
      dataModel.value = data
    }
    loading.value = false
    showDetail.value = true
  })
}

function toLink(path: string) {
  const link = document.createElement('a')
  link.href = path
  link.click()
}

function toPageNotif() {
  const link = document.createElement('a')
  link.href = '/notifications'
  link.click()
}

function clear() {
  emit('clear')
}

function emitRefreshEvent() {
  emit('refreshEvent')
}
</script>

<style scoped>
.pt {
  padding-top: 16px;
}
</style>
