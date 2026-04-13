<template>
  <div>
    <s-loading v-if="initLoad" />
    <q-page v-else class="window-height window-width row standard-font">
      <div class="row col-md-12 col-12">
        <!-- <q-img spinner-color="white" src="~assets/background-home.png" :fit="backgroundImageFit" class="window-height window-width" :ratio="16 / 9"> -->
          <div class="bg-white window-height window-width" :ratio="16 / 9">
            <div class="shadow-1 fit flex items-stretch justify-evenly overflow-auto">
              <div class="col-md-4 col-12">
                <div class="row fit col-12">
                  <div class="fit row items-center justify-center col-12">
                    <q-form class="q-gutter-md" @submit.prevent="login" style="text-align: center">
                      <q-img v-if="!$q.screen.gt.sm" src="~assets/image.png" width="300px" class="q-mr-md" />
                      <q-img v-if="$q.screen.gt.sm" src="~assets/image.png" width="300px" class="q-mr-md" style="margin-right: 50px" />
                      <div class="q-pa-md q-ma-md justify-center text-white full-width">
                        <div class="q-pb-sm column q-gutter-y-none q-mb-lg">
                          <div style="font-size: 2.6rem">
                            <strong>RENT - UKK</strong>
                          </div>
                        </div>
  
                        <div>
                          <q-input filled v-model="dataModel.email" placeholder="email/username" class="q-mb-md">
                            <template v-slot:prepend>
                              <q-icon name="person" />
                            </template>
                          </q-input>
  
                          <q-input stack-label filled v-model="dataModel.password" :type="isPwd ? 'password' : 'text'" placeholder="**********">
                            <template v-slot:prepend>
                              <q-icon name="lock" />
                            </template>
                            <template v-slot:append>
                              <q-icon :name="isPwd ? 'visibility_off' : 'visibility'" class="cursor-pointer" @click="isPwd = !isPwd" />
                            </template>
                          </q-input>
  
                          <!-- Remember & Forgot Password  -->
                          <div class="row q-pb-sm justify-between items-center">
                            <q-btn flat label="forgot password" color="white" class="text-capitalize" @click="forgotPassword" />
                            <q-btn flat label="Register" color="primary" class="text-capitalize" to="/signup" />
                          </div>

                          <!-- Submit Button -->
                          <q-btn class="q-py-sm full-width capital" type="submit" color="primary" label="Sign In" size="md" style="border-radius: 100px" :loading="loading" :disable="!(dataModel.email && dataModel.password)">
                            <template v-slot:loading>
                              <q-spinner-puff />
                            </template>
                          </q-btn>
                        </div>
                      </div>
                      <div class="text-center q-pa-md q-pt-lg">
                        <div v-if="$q.screen.gt.sm" class="text-black-6 q-pa-none">{{ Config.ukkCopyright() }}</div>
                        <div v-if="!$q.screen.gt.sm" class="text-black-6 q-pa-none" style="color: white">{{ Config.ukkCopyright() }}</div>
                      </div>
                    </q-form>
                  </div>
                </div>
              </div>
              <!-- <div class="col-md-8 col-12 flex column items-center justify-center" v-if="$q.screen.gt.sm">
                
              </div> -->
            </div>
          </div>
        <!-- </q-img> -->
      </div>
      <!-- <div class="row col-md-8 col-12" v-if="$q.screen.gt.sm">
        <div class="row fit col-12">
          <q-img spinner-color="white" src="~assets/bg-login.jpg" img-class="no-object-fit" :ratio="100 / 20" />
        </div>
      </div> -->
      <!-- Forgot Pass Dialog -->
      <q-dialog v-model="resetPwdDialog">
        <ForgotPassword @reset-password="resetPassword" />
      </q-dialog>
      <!-- Forgot Pass Dialog -->
    </q-page>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import ForgotPassword from './ForgotPassword.vue'
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Helper } from 'src/services/helper'
import { Config } from 'src/services/config'
import { authStore } from 'src/stores/auth'
import { useQuasar } from 'quasar'
import { subscribePush } from 'src/services/api/push-notif'

const API = new Api()
const Auth = authStore()
const route = useRoute()
const router = useRouter()
const loading = ref(false)
const initLoad = ref(true)
const dataModel = ref({
  email: '',
  password: '',
  firebase_token: null,
  remember_me: false
})
const isPwd = ref(true)
const disableSubmit = ref(false)
const resetPwdDialog = ref(false)
const $q = useQuasar()

const isUserRole = (user: any) => {
  if (!user) return false
  
  // Check dari menu.name
  if (user.menu?.name === 'user') return true
  
  // Check dari roles array
  if (Array.isArray(user.roles)) {
    return user.roles.some((role: any) => role.name?.toLowerCase() === 'user')
  }
  
  return false
}

const getRedirectPath = (user: any) => {
  return isUserRole(user) ? '/rental/user' : '/home'
}

const init = () => {
  // Dark.set('auto')
  if (Auth.getToken()) {
    const user = Auth.getUser()
    router.push(getRedirectPath(user))
  } else {
    Auth.clearData()
    initLoad.value = false
    if (route.query.email) dataModel.value.email = route.query.email as string
    if (route.query.msg) Helper.showNotif(route.query.msg as string)
  }
}

const login = () => {
  disableSubmit.value = true
  loading.value = true
  const params = new URLSearchParams()
  params.append('username', dataModel.value.email)
  params.append('password', dataModel.value.password)
  params.append('remember_me', dataModel.value.remember_me.toString())
  API.post('token', params, (status: number, data: any) => {
    if (status === 200) auth(data)
    else {
      disableSubmit.value = false
      loading.value = false
    }
  })
}

const auth = (data: any) => {
  if (data) Auth.setTokenInfo(data)
  API.get('me', (status: number, data: any) => {
    if (status === 200) {
      if (isUserRole(data)) {
        if (Array.isArray(data.menu)) {
          data.menu = { menu_items: data.menu }
        } else {
          data.menu = data.menu || {}
        }
        const userMenuItems = Array.isArray(data.menu.menu_items) ? data.menu.menu_items : []
        if (userMenuItems.length === 0) {
          data.menu.menu_items = [
            { app: 'rental', name: 'Beranda', slug: 'rental/user', path: '/rental/user', icon: 'home' },
            { app: 'rental', name: 'Alat Foto', slug: 'rental/user/items', path: '/rental/user/items', icon: 'photo_camera' },
            { app: 'rental', name: 'Cara Sewa', slug: 'rental/user/how-to', path: '/rental/user/how-to', icon: 'menu_book' },
            { app: 'rental', name: 'Kontak', slug: 'rental/user/contact', path: '/rental/user/contact', icon: 'contacts' },
            { app: 'rental', name: 'Booking', slug: 'rental/user/rental', path: '/rental/user/rental', icon: 'shopping_cart' },
            { app: 'rental', name: 'FAQ', slug: 'rental/user/faq', path: '/rental/user/faq', icon: 'help' },
            { app: 'rental', name: 'About', slug: 'rental/user/about', path: '/rental/user/about', icon: 'info' }
          ]
        }
        data.menu_favorites = Array.isArray(data.menu_favorites) && data.menu_favorites.length > 0
          ? data.menu_favorites
          : [{ app: 'rental', name: 'Alat Foto', slug: 'rental/user/items', path: '/rental/user/items', icon: 'photo_camera' }]
      }
      Auth.setUser(data)
      void router.push(getRedirectPath(data))
      void subscribePush(data.username, data.id)
    } else {
      disableSubmit.value = false
      loading.value = false
    }
  })
}

const forgotPassword = () => {
  resetPwdDialog.value = true
}

const resetPassword = (email: string) => {
  Helper.loadingOverlay()
  API.get(`forgot-password?email=${email}`, (status: number, data: { message: string }) => {
    Helper.loadingOverlay(false)
    resetPwdDialog.value = false
    if (status === 200) {
      Helper.showSuccess(data?.message ?? 'Please check your inbox, reset password only valid for 5 minutes.')
    }
  })
}

const backgroundImageFit = computed<'fill' | 'contain'>(() => ($q.screen.gt.sm ? 'fill' : 'contain'))

onMounted(init)
</script>

<style>
.bg-login-small {
  position: absolute;
  opacity: 1;
  /* z-index: -1; */
  /* background-color: #fff; */
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-position: right;
  background-size: cover;
  height: 100% !important;
  min-height: 100vh;
}

.circle {
  height: 70px;
  width: 70px;
  background-color: #ffe394;
  border-radius: 50%;
  display: inline-block;
}

.modules {
  font-style: normal;
  font-weight: 500;
  font-size: 12px;
  line-height: 20px;

  text-align: center;
  letter-spacing: 0.05em;
}

.no-object-fit {
  object-fit: fill !important;
}

.glass-card {
  background: rgba(255, 255, 255, 0.39);
  backdrop-filter: blur(50px);
  -webkit-backdrop-filter: blur(50px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.5),
    inset 0 -1px 0 rgba(255, 255, 255, 0.1),
    inset 0 0 0px 0px rgba(255, 255, 255, 0);
  position: relative;
  overflow: hidden;
}

.glass-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent);
}

.glass-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 1px;
  height: 100%;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.8), transparent, rgba(255, 255, 255, 0.3));
}
</style>