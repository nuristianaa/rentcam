<template>
  <q-layout view="lHh Lpr lFf">
    <q-header class="text-primary user-header glass-header">
      <q-toolbar class="header-toolbar q-px-lg user-toolbar">
        <q-toolbar-title class="user-brand-title">
          <router-link class="user-brand row items-center no-wrap" to="/rental/user">
            <div class="user-brand-text user-brand-text-only">
              <div class="brand-title">
                <span class="text-primary">RENT</span><span class="text-secondary" style="color: #64748b;">CAM</span>
              </div>
              <div class="brand-subtitle">rental alat photo</div>
            </div>
          </router-link>
        </q-toolbar-title>

        <!-- Desktop Menu -->
        <div class="gt-sm row items-center user-nav-links">
          <q-btn
            v-for="item in topMenuItems"
            :key="item.path"
            flat
            dense
            rounded
            no-caps
            :to="item.path"
            :label="item.name"
            class="user-nav-link"
            :class="{ 'user-nav-active': isActive(item) }"
          />
        </div>

        <q-space />

        <div class="row items-center q-gutter-sm user-header-actions">
          <ProfilePopup v-if="isLoggedIn" :modelValue="user" />
          <q-btn
            v-else
            unelevated
            rounded
            color="primary"
            icon="login"
            label="Masuk"
            to="/login"
            class="login-btn q-px-md gt-xs"
          />
          
          <!-- Mobile Menu Toggle -->
          <q-btn
            flat
            round
            dense
            icon="menu"
            class="lt-md text-primary"
            @click="mobileMenuOpen = !mobileMenuOpen"
          />
        </div>
      </q-toolbar>
    </q-header>

    <!-- Mobile Drawer -->
    <q-drawer
      v-model="mobileMenuOpen"
      side="right"
      overlay
      behavior="mobile"
      elevated
      class="bg-white drawer-mobile"
    >
      <div class="q-pa-md flex column q-gutter-y-md full-height">
        <div class="row items-center justify-between q-mt-xs q-mb-md">
          <div class="user-brand-text user-brand-text-only">
            <div class="brand-title text-h6" style="font-size: 1.2rem;">RENTCAM</div>
            <div class="brand-subtitle" style="font-size: 0.75rem;">rental alat photo</div>
          </div>
          <q-btn flat round dense icon="close" @click="mobileMenuOpen = false" color="grey-8" />
        </div>

        <q-separator class="q-mb-sm" />

        <div class="column q-gutter-y-xs flex-1">
          <q-btn
            v-for="item in topMenuItems"
            :key="item.path"
            flat
            no-caps
            align="left"
            :to="item.path"
            class="mobile-nav-link full-width"
            :class="{ 'mobile-nav-active': isActive(item) }"
            @click="mobileMenuOpen = false"
          >
            <div class="row items-center full-width">
              <span class="text-weight-bold" style="text-transform: uppercase; font-size: 0.9rem;">{{ item.name }}</span>
              <q-space />
              <q-icon name="chevron_right" size="1.2em" :color="isActive(item) ? 'primary' : 'grey-5'" />
            </div>
          </q-btn>
        </div>
        
        <q-space />
        
        <div class="q-mt-auto q-pb-md" v-if="!isLoggedIn">
           <q-btn
             unelevated
             color="primary"
             class="full-width rounded-borders"
             label="Masuk"
             icon="login"
             to="/login"
             size="md"
             @click="mobileMenuOpen = false"
           />
        </div>
      </div>
    </q-drawer>

    <q-page-container class="bg-grey-1">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { authStore } from 'src/stores/auth'
import ProfilePopup from 'src/layouts/drawer/ProfilePopup.vue'

const auth = authStore()
const route = useRoute()
const mobileMenuOpen = ref(false)

const topMenuItems = computed(() => {
  const menus = (auth.getMenu() || []).filter((item: any) => item.path && !item.children)
  
  const hasHowTo = menus.some((m: any) => m.path === '/rental/user/how-to')
  const hasContact = menus.some((m: any) => m.path === '/rental/user/contact')

  if (!hasHowTo) {
    const faqIndex = menus.findIndex((m: any) => m.path === '/rental/user/faq')
    const howToItem = { name: 'Cara Sewa', path: '/rental/user/how-to' }
    if (faqIndex !== -1) menus.splice(faqIndex, 0, howToItem)
    else menus.push(howToItem)
  }

  if (!hasContact) {
    menus.push({ name: 'Kontak', path: '/rental/user/contact' })
  }

  return menus
})
const user = computed(() => auth.user)
const isLoggedIn = computed(() => !!auth.getToken())

onMounted(() => {
  auth.getUser()
})

const isActive = (item: any) => {
  if (!item?.path) return false

  const currentPath = route.path.replace(/\/+$/, '')
  const itemPath = item.path.replace(/\/+$/, '')

  if (currentPath === itemPath) return true
  if (itemPath === '/rental/user') return false
  return currentPath.startsWith(itemPath + '/')
}
</script>

<style scoped>
/* Glassmorphism Header Effects */
.glass-header {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  box-shadow: 0 4px 20px -10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.user-header {
  min-height: 80px;
}
.user-toolbar {
  min-height: 80px;
  gap: 0.75rem;
  align-items: center;
}

@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;800;900&display=swap');

/* User Brand Enhancements */
.user-brand-title {
  min-width: auto;
}
.user-brand {
  display: inline-flex;
  align-items: center;
  gap: 0.65rem;
  text-decoration: none;
  transition: transform 0.2s ease, opacity 0.2s ease;
}
.user-brand:hover {
  transform: translateY(-1px);
  opacity: 0.9;
}
.user-brand-text {
  display: flex;
  flex-direction: column;
  gap: 0px;
}
.user-brand-text-only {
  display: flex;
  flex-direction: column;
  gap: 0;
}
.brand-title {
  font-family: 'Outfit', sans-serif;
  font-size: 1.55rem;
  font-weight: 800;
  letter-spacing: -0.01em;
  line-height: 1;
}
.brand-subtitle {
  font-family: 'Outfit', sans-serif;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.16em;
  color: #8fa0b9;
  line-height: 1.1;
  text-transform: uppercase;
}

/* Menu desktop - KEPT UNCHANGED AS REQUESTED */
.user-nav-links {
  flex: 1 1 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  overflow-x: auto;
  white-space: nowrap;
}
.user-nav-links::-webkit-scrollbar {
  display: none;
}
.user-nav-link {
  min-width: 100px;
  max-width: 180px;
  justify-content: center;
  text-transform: uppercase;
  font-weight: 600;
  color: var(--q-primary);
}
.user-nav-link .q-btn__content {
  padding: 0 12px;
}
.user-nav-active {
  color: var(--q-primary);
  border-bottom: 2px solid currentColor;
}
/* END MENU UNCHANGED */

.user-header-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  white-space: nowrap;
}

/* Mobile Drawer/Menu Styles */
.mobile-nav-link {
  border-radius: 12px;
  padding: 12px 16px;
  color: #475569;
  transition: all 0.2s ease;
  margin-bottom: 4px;
}
.mobile-nav-active {
  background: rgba(33, 150, 243, 0.08); /* Fallback generic blue if primary differs */
  color: var(--q-primary) !important;
}

@media (max-width: 900px) {
  /* Using standard Quasar lt-md for hiding instead */
}
</style>
