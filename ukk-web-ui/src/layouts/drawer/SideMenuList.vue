<template>
  <div>
    <template v-for="(menuItem, index) in modelValue">
      <q-expansion-item v-if="menuItem.children && menuItem.children.length !== 0" dense class="side-menu-item" :key="'ii' + index" :label="menuItem.name" :icon="menuIcon(menuItem.icon)" :header-inset-level="inset" :default-opened="checkOpen(menuItem.children, menuItem)">
        <template v-slot:header>
          <div class="q-py-xs" style="width: 100%">
            <q-icon class="q-pr-sm icon-menu-list" dense size="xs" :name="menuIcon(menuItem.icon)" />
            <span>{{ menuItem.name }}</span>
          </div>
        </template>
        <!-- SUBMENUS -->
        <side-menu-list :modelValue="menuItem.children" :inset-level="inset + 0.2" sub />
      </q-expansion-item>

      <q-expansion-item v-else dense @click="actionMenu(menuItem)" :key="'iii' + index" :class="sub + ' side-menu-item ' + isActive(menuItem.path) + ' ic-' + menuIcon(menuItem.icon)" :label="menuItem.name" :icon="menuIcon(menuItem.icon)" :header-inset-level="inset" expand-icon="none">
        <template v-slot:header>
          <div class="q-py-xs" style="width: 100%">
            <q-icon class="q-pb-xs q-pr-xs icon-menu-list" dense size="xs" :name="menuIcon(menuItem.icon)" />
            <span>{{ menuItem.name }}</span>

            <q-popup-proxy context-menu>
              <div class="row" v-close-popup clickable @click="setFavorite(menuItem)">
                <q-btn size="11px" no-caps flat label="Set Favorite" icon-right="star" color="primary" />
              </div>
            </q-popup-proxy>
          </div>
        </template>
      </q-expansion-item>
    </template>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { Helper } from 'src/services/helper'
import { authStore } from 'src/stores/auth'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

interface MenuItem {
  name: string
  path?: string
  icon?: string | null
  children?: MenuItem[]
}

const props = defineProps<{
  modelValue: MenuItem[]
  insetLevel?: number
  sub?: boolean
}>()

const API = new Api()
const router = useRouter()
const auth = authStore()

const inset = computed(() => props.insetLevel ?? 0)

const menuIcon = (icon: string | null | undefined): string => {
  return icon && icon.trim() !== '' ? icon : 'noise_control_off'
}

const actionMenu = (menu: MenuItem) => {
  if (!menu.children || menu.children.length === 0) {
    if (menu.path && menu.path.indexOf('https://') > -1) window.open(menu.path, '_blank')
    else router.push(menu.path || '/')
  }
}

const checkOpen = (subMenu: MenuItem[], current: MenuItem): boolean => {
  const route = router.currentRoute.value.path
  if (route === current.path) return true
  return subMenu.some((item) => item.path === route)
}

const isActive = (current: string | undefined): string => {
  if (!current) return ''
  let path = router.currentRoute.value.path
  const indexRight = path.indexOf('/form/')
  if (indexRight > -1) path = path.substring(0, indexRight)
  return current === path ? 'active-menu' : ''
}

const openNew = (path: string | undefined): string => {
  if (!path) return ''
  const origin = window.location.origin
  const hash = window.location.hash.includes('#')
  return hash ? `${origin}/#${path}` : `${origin}${path}`
}

const setFavorite = (menuItem: MenuItem) => {
  const favorites: MenuItem[] = auth.getFavs() || []
  if (favorites.some((fav: MenuItem) => fav.path === menuItem.path)) {
    Helper.showNotif('Favorite menu already exists')
    return
  }
  favorites.push(menuItem)
  API.post(
    'me/favmenu',
    { menu_favorites: favorites },
    (status: number, data: any) => {
      if (status === 200) {
        auth.setFavs(favorites)
        Helper.showSuccess('Menu added to favorites')
      }
    },
    'main'
  )
}
</script>
