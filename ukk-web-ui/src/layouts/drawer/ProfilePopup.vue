<template>
  <div v-if="modelValue" class="row items-center cursor-pointer q-gutter-x-sm" style="transition: all 0.2s;">
    <div class="gt-xs text-right q-pr-xs">
      <div class="text-weight-bold text-primary" style="font-size: 0.9rem; line-height: 1.1;">{{ modelValue.name }}</div>
      <div class="text-caption" style="color: #64748b; font-size: 0.75rem;">{{ modelValue.email }}</div>
    </div>
    
    <q-avatar size="42px" color="primary" text-color="white" class="text-weight-bolder shadow-1" style="font-size: 20px;">
      {{ modelValue.name ? modelValue.name.charAt(0).toUpperCase() : 'U' }}
      
      <q-menu anchor="bottom right" self="top right" :offset="[0, 8]">
        <div class="row no-wrap q-pa-md">
          <div class="column q-gutter-y-sm">
            <div class="text-h6 q-mb-md" style="min-width: 120px">Settings</div>
            <q-btn @click="changeProfile" no-wrap dense  push size="sm" color="primary" icon="person" label="Profile" class="full-width" />
            <q-btn @click="changePassword" no-wrap dense  push size="sm" color="primary" icon="key" label="Password" class="full-width" />
            <!-- MENU MANAGE FOR VENDOR USER -->
            <q-btn v-if="modelValue.user_type == 'vendor'" @click="manageUser()" no-wrap dense  push size="sm" color="primary" icon="manage_accounts" label="Manage User" class="full-width" />
          </div>

          <q-separator vertical inset class="q-mx-lg" />

          <div class="column items-center">
            <q-avatar size="80px" color="primary" text-color="white" class="text-h3 text-weight-bolder q-mb-sm shadow-2">
              {{ modelValue.name ? modelValue.name.charAt(0).toUpperCase() : 'U' }}
            </q-avatar>

            <q-item-section class="text-center">
              <q-item-label class="text-weight-bold">{{ modelValue.name }}</q-item-label>
              <q-item-label class="text-overline">{{ modelValue.email }}</q-item-label>
              <q-item-label>
                <q-chip size="sm">
                  <q-avatar icon="check" :color="Constant.colors(modelValue.role_id)" text-color="white" />
                  {{ modelValue.title }}
                </q-chip>
              </q-item-label>
            </q-item-section>
            <q-btn @click="logout" color="negative" label="Logout" push size="sm" v-close-popup />
          </div>
        </div>
      </q-menu>
    </q-avatar>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { Config } from 'src/services/config'
import { Constant } from 'src/services/constant'
import { useRouter } from 'vue-router'
import Api from 'src/services/api'
import { Helper } from 'src/services/helper'

const props = defineProps<{
  modelValue: any
}>()
const API = new Api()
const router = useRouter()

const isUserRole = () => {
  const mv = props.modelValue
  if (!mv) return false
  const currentPath = router.currentRoute.value.path
  return mv.user_type === 'user' || 
         mv.role_code?.toLowerCase() === 'user' || 
         mv.role?.code?.toLowerCase() === 'user' || 
         mv.role_id === 3 || 
         currentPath.startsWith('/rental/user')
}

const changeProfile = () => {
  if (isUserRole()) {
    router.push({ name: 'user-change-profile', params: props.modelValue })
  } else {
    router.push({ name: 'change-profile', params: props.modelValue })
  }
}

const manageUser = () => {
  router.push({ name: 'auth/users-vendor' })
}

const changePassword = () => {
  if (isUserRole()) {
    router.push({ name: 'user-change-password', params: props.modelValue })
  } else {
    router.push({ name: 'change-password', params: props.modelValue })
  }
}

const logout = () => {
  Config.logout()
}

onMounted(() => {
  
})

// const clearCache = async (cache = false) => {
//   location.reload()
//   window.location.href = window.location.href.replace(/#.*$/, '')
// }
</script>
