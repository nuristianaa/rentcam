<template>
  <q-drawer v-if="!loading" show-if-above v-model="drawer" :mini="!drawer || (miniState && !forceBig)" :width="240" :mini-width="50" side="left" :breakpoint="823">
    <template v-slot:mini>
      <q-scroll-area class="relative-position border-right" style="height: 100%;">
        <q-list padding>
          <q-item clickable v-ripple @click="$router.push('/home')">
            <q-item-section avatar>
              <q-avatar square size="24px">
                <img src="~assets/favicon.png" />
              </q-avatar>
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="star" color="primary" />
              <q-tooltip>Favorites</q-tooltip>
            </q-item-section>
            <q-menu anchor="top right" self="top left">
              <q-list padding>
                <q-item dense clickable v-for="(v, i) in auth.$state?.user?.menu_favorites" :key="i" @click="$router.push(v.path)">
                  <q-item-section>{{ v.name }}</q-item-section>
                  <q-popup-proxy context-menu>
                    <div class="row" v-close-popup clickable @click="deleteFavorite(i)">
                      <q-btn size="12px" no-caps flat label="Delete Favorite" icon="delete" color="negative" />
                    </div>
                  </q-popup-proxy>
                </q-item>
              </q-list>
            </q-menu>
          </q-item>

          <q-item clickable v-ripple @click="miniState = false">
            <q-item-section avatar>
              <q-icon name="chevron_right" color="primary" />
              <q-tooltip>Show Menu</q-tooltip>
            </q-item-section>
          </q-item>
        </q-list>
        <!-- <div class="button-ministate fixed row items-center justify-center cursor-pointer" @click="miniState = false">
          <q-icon :name="'chevron_right'" color="white" size="20px" />
        </div> -->
      </q-scroll-area>
    </template>

    <q-scroll-area class="relative-position border-right" style="height: 100%;">
      <div id="sidebar">
        <div class="side-bar-top q-pa-md">
          <!-- BRAND -->
          <div class="row items-start q-mb-md relative-position sidebar-brand">
            <q-avatar square size="32px">
              <img src="~assets/favicon.png" />
            </q-avatar>

            <div class="q-ml-sm">
              <div class="text-weight-bold text-h5">RENTCAM</div>
              <div class="text-body2 text-grey-5" style="letter-spacing: 0.5px;">rental alat photo</div>
            </div>

            <!-- FAVORITE BADGE -->
            <q-btn
              flat
              round
              dense
              icon="star"
              size="sm"
              color="amber-5"
              class="favorite-badge"
            >
              <q-menu anchor="top right" self="top left">
                <q-item
                  dense
                  clickable
                  v-for="(v, i) in auth.$state?.user?.menu_favorites"
                  :key="i"
                  @click="$router.push(v.path)"
                >
                  <q-item-section>{{ v.name }}</q-item-section>

                  <q-popup-proxy context-menu>
                    <div class="row" v-close-popup>
                      <q-btn
                        size="12px"
                        no-caps
                        flat
                        label="Delete Favorite"
                        icon="delete"
                        color="negative"
                        @click.stop="deleteFavorite(i)"
                      />
                    </div>
                  </q-popup-proxy>
                </q-item>
              </q-menu>
            </q-btn>
          </div>

          <!-- APP / PROJECT -->
          <q-select outlined dense style="text-transform: uppercase"  v-model="app" :options="appOptions" dropdown-icon="keyboard_arrow_down" stack-label :display-value="`${app ? app : '-'}`" @update:model-value="onRefresh(app)">
          </q-select>
        </div>

        <q-separator class="q-my-sm" />

        <!-- SEARCH -->
        <div class="row items-center q-pa-md">
          <q-input dense outlined debounce="500" v-model="search" label="Search" class="col-12" @update:model-value="filterMenu">
            <template v-slot:prepend>
              <q-icon name="search" size="18px" />
            </template>
          </q-input>
        </div>

        <!-- <div clickable @click="miniState = true" style="right: -10px" class="absolute">
          <q-btn  unelevated icon="chevron_left" color="primary" class="q-px-lg">
            <q-tooltip>Hide Menu</q-tooltip>
          </q-btn>
        </div> -->

        <div v-if="!s_load && menuList" class="q-pa-xs">
          <div v-if="app == 'all'">
            <div v-for="v in Object.keys(allMenus)" :key="v">
              <q-item-label header class="no-padding q-mx-sm q-my-xs text-uppercase text-bold">{{ v }}</q-item-label>
              <SideMenuList v-model="allMenus[v]" dense />
              <q-separator />
            </div>
          </div>
          <SideMenuList v-else v-model="menuList" dense />
        </div>
      </div>
    </q-scroll-area>
  </q-drawer>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import SideMenuList from './SideMenuList.vue'
import Meta from './meta'
import { authStore } from 'src/stores/auth'
import { Helper } from 'src/services/helper'
import Api from 'src/services/api'
import { Screen } from 'quasar'

// Emits
const emits = defineEmits(['refreshMenu'])

// Props
const props = defineProps<{
  refresh: number
  toggleMenu: boolean
}>()

// Reactive state
const route = useRoute()
const API = new Api()
const auth = authStore()
const drawer = ref(false)
const miniState = ref(true)
const forceBig = ref(false)
const loading = ref(false)
const search = ref('')
const app = ref<string | null>(null)
const apps = ref<Record<string, any>>({})
const allMenus = ref<Record<string, any>>({})
const allMenusTmp = ref<Record<string, any>>({})
const appOptions = ref<string[]>([])
const menuList = ref<any[]>(Meta.menus)
const menuListTmp = ref<any[]>([])
const s_load = ref(false)

if (Screen.lt.md) miniState.value = true
else miniState.value = false

// METHODS
const onRefresh = (appParam: string | null = '') => {
  const menus = Array.isArray(auth.getMenu()) ? auth.getMenu() : []

  const groupApp = menus.reduce((group: Record<string, any[]>, product) => {
    const { app } = product
    group[app] = group[app] ?? []
    group[app].push(product)
    return group
  }, {})

  apps.value = groupApp
  allMenus.value = groupApp
  allMenusTmp.value = groupApp
  appOptions.value = Object.keys(apps.value)
  appOptions.value.unshift('all')

  app.value = appParam || (route?.query?.app as string) || auth.getApp() || appOptions.value[0] || null

  if (app.value) {
    auth.setApp(app.value)
    if (app.value !== 'all') {
      menuList.value = apps.value[app.value] ?? []
      menuListTmp.value = apps.value[app.value] ?? []
    }
  } else {
    menuList.value = menus
    menuListTmp.value = menus
  }
}

const doFilter = (lists: any[], data: any[] = []) => {
  lists.forEach((e) => {
    const name = e.name.toLowerCase()
    if (name.indexOf(search.value.toLowerCase()) > -1) {
      data.push(e)
    }
    if (e.children && e.children.length > 0) {
      doFilter(e.children, data)
    }
  })
  return data
}

const filterMenu = () => {
  s_load.value = true
  if (app.value == 'all') {
    let data: Record<string, any> = {}
    if (search.value || search.value != '') {
      const keys = Object.keys(allMenusTmp.value)
      keys.forEach((key) => {
        data[key] = doFilter(allMenusTmp.value[key], [])
      })
    } else {
      data = allMenusTmp.value
    }
    allMenus.value = data
  } else {
    let data: any[] | undefined = []
    if (search.value) {
      data = doFilter(menuListTmp.value, data)
    } else {
      data = menuListTmp.value
    }
    menuList.value = data
  }

  setTimeout(() => {
    s_load.value = false
  }, 100)
}

const deleteFavorite = (index: number) => {
  const menus = auth.getFavs() || []
  menus.splice(index, 1)

  API.post(
    'me/favmenu',
    { menu_favorites: menus },
    (status: number, data: any) => {
      if (status === 200) {
        auth.setFavs(menus)
        Helper.showSuccess('Success delete menu')
      }
    },
    'main'
  )
}

// const refreshSearch = () => {
//   search.value = ""
//   menuList.value = menuListTmp.value
//   emits("refreshMenu")
// }

// const drawerClick = () => {
//   if (miniState.value) miniState.value = false
// }

// MOUNTED | WATCHERS | COMPUTED
onMounted(() => {
  onRefresh()
})

watch(
  () => props.toggleMenu,
  () => {
    drawer.value = !drawer.value
    if (drawer.value == true) miniState.value = false
  }
)

// watch(search, () => {
//   if (!search.value) {
//     menuList.value = menuListTmp.value
//     allMenus.value = allMenusTmp.value
//   }
// })

// watch(() => route.query.app, (newValue, oldValue) => {
//   const newApp = newValue as string ?? 'main'
//   if (newApp) onRefresh(newApp)
// })

// watch(() => auth.$state.app, () => { onRefresh() })
</script>


<style scoped>
.sidebar-brand {
  position: relative;
}

.favorite-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: rgba(245, 158, 11, 0.15);
  border-radius: 50%;
}
</style>