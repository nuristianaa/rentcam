<template>
  <div>
    <q-page class="window-height window-width row standard-font">
      <div class="row col-md-12 col-12">
        <div class="bg-white window-height window-width" :ratio="16 / 9">
          <div class="shadow-1 fit flex items-stretch justify-evenly overflow-auto">
            <div class="col-md-5 col-12">
              <div class="row fit col-12">
                <div class="fit row items-center justify-center col-12">
                  <q-form class="q-gutter-md" @submit.prevent="onSubmit" style="text-align: center; width: 100%">
                    <q-img v-if="!$q.screen.gt.sm" src="~assets/image.png" width="300px" class="q-mr-md" />
                    <q-img v-if="$q.screen.gt.sm" src="~assets/image.png" width="300px" class="q-mr-md" style="margin-right: 50px" />

                    <div class="q-pa-md q-ma-md justify-center text-white full-width">
                      <div class="q-pb-sm column q-gutter-y-none q-mb-lg">
                        <div style="font-size: 2.6rem">
                          <strong>RENT - UKK</strong>
                        </div>
                      </div>

                      <div>
                        <!-- Username & Email row -->
                        <div class="row q-col-gutter-sm q-mb-md">
                          <div class="col-12 col-md-6">
                            <q-input
                              filled
                              v-model="form.username"
                              label="Username"
                              :rules="[val => !!val || 'Wajib diisi']"
                            >
                              <template v-slot:prepend>
                                <q-icon name="person" />
                              </template>
                            </q-input>
                          </div>
                          <div class="col-12 col-md-6">
                            <q-input
                              filled
                              v-model="form.email"
                              label="Email"
                              type="email"
                              :rules="[val => !!val || 'Wajib diisi']"
                            >
                              <template v-slot:prepend>
                                <q-icon name="email" />
                              </template>
                            </q-input>
                          </div>
                        </div>

                        <!-- Full Name -->
                        <q-input
                          filled
                          v-model="form.name"
                          label="Nama Lengkap"
                          class="q-mb-md"
                          :rules="[val => !!val || 'Nama wajib diisi']"
                        >
                          <template v-slot:prepend>
                            <q-icon name="badge" />
                          </template>
                        </q-input>

                        <!-- Password -->
                        <q-input
                          filled
                          v-model="form.password"
                          :type="isPwd ? 'password' : 'text'"
                          label="Password"
                          class="q-mb-md"
                          :rules="[val => val && val.length >= 8 || 'Min. 8 karakter']"
                        >
                          <template v-slot:prepend>
                            <q-icon name="lock" />
                          </template>
                          <template v-slot:append>
                            <q-icon :name="isPwd ? 'visibility_off' : 'visibility'" class="cursor-pointer" @click="isPwd = !isPwd" />
                          </template>
                        </q-input>

                        <!-- WhatsApp -->
                        <q-input
                          filled
                          v-model="form.phone"
                          label="Nomor WhatsApp"
                          type="tel"
                          class="q-mb-md"
                        >
                          <template v-slot:prepend>
                            <q-icon name="phone" />
                          </template>
                        </q-input>

                        <!-- Already have account & back to login -->
                        <div class="row q-pb-sm justify-between items-center">
                          <span class="text-caption text-grey-6">Already have an account?</span>
                          <q-btn flat label="Login di sini" color="primary" class="text-capitalize" to="/login" />
                        </div>

                        <!-- Submit Button -->
                        <q-btn
                          class="q-py-sm full-width capital"
                          type="submit"
                          color="primary"
                          label="Register Now"
                          size="md"
                          style="border-radius: 100px"
                          :loading="loading"
                          :disable="!(form.username && form.email && form.name && form.password)"
                        >
                          <template v-slot:loading>
                            <q-spinner-puff />
                          </template>
                        </q-btn>
                      </div>
                    </div>

                    <div class="text-center q-pa-md q-pt-lg">
                      <div class="text-grey-6 q-pa-none">&copy; {{ new Date().getFullYear() }} RENTCAM · All Rights Reserved</div>
                    </div>
                  </q-form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </q-page>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import Api from 'src/services/api'
import { authStore } from 'src/stores/auth'

const $q = useQuasar()
const router = useRouter()
const Auth = authStore()
const loading = ref(false)
const isPwd = ref(true)
const form = ref({
  username: '',
  email: '',
  name: '',
  password: '',
  phone: ''
})

function onSubmit() {
  loading.value = true
  const payload = {
    ...form.value,
    role_ids: [3] // default user
  }
  
  new Api().post('auth/users/public', payload, (status: number, data: any, msg: string) => {
    if (status === 200) {
      autoLogin()
    } else {
      loading.value = false
      $q.notify({ 
        type: 'negative', 
        message: msg || 'Registration failed, please try again.',
        position: 'top'
      })
    }
  }, 'identity')
}

function autoLogin() {
  const params = new URLSearchParams()
  params.append('username', form.value.username)
  params.append('password', form.value.password)
  
  new Api().post('token', params, (status: number, data: any) => {
    if (status === 200) {
      Auth.setTokenInfo(data)
      // Fetch user info
      new Api().get('me', (mStatus: number, mData: any) => {
        loading.value = false
        if (mStatus === 200) {
          Auth.setUser(mData)
          $q.notify({
            type: 'positive',
            message: 'Registration Successful! Welcome to RentCam.',
            icon: 'verified',
            timeout: 2000
          })
          void router.push('/rental/user')
        } else {
          void router.push('/login')
        }
      })
    } else {
      loading.value = false
      void router.push('/login')
    }
  })
}
</script>

<style scoped>
.info-notice {
  background: rgba(25, 118, 210, 0.07);
  border: 1px solid rgba(25, 118, 210, 0.18);
  padding: 12px 16px;
  border-radius: 12px;
}
</style>