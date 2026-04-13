<template>
  <q-page class="window-height window-width row justify-center items-center">
    <div class="column">
      <div class="row">
        <h5 class="text-h3 q-my-md">Create New Password</h5>
      </div>
      <div class="row">
        <q-card square bordered class="q-pa-lg shadow-1">
          <q-form class="q-gutter-md" @submit.prevent="submit">
            <q-card-section class="q-pt-md q-pb-none justify-center">
              <q-input stack-label dense outlined label="Password" v-model="dataModel.password" :type="isPwd ? 'password' : 'text'" placeholder="**********" lazy-rules :rules="[(val) => validate.validateRequired(val) || '']">
                <template v-slot:append>
                  <q-icon :name="isPwd ? 'visibility_off' : 'visibility'" class="cursor-pointer" @click="isPwd = !isPwd" />
                </template>
              </q-input>
              <q-input stack-label dense outlined label="Re-type Password" v-model="dataModel.retype_password" :type="isRetypePwd ? 'password' : 'text'" placeholder="**********" lazy-rules :rules="[(val) => validate.validateRequired(val) || '']">
                <template v-slot:append>
                  <q-icon :name="isRetypePwd ? 'visibility_off' : 'visibility'" class="cursor-pointer" @click="isRetypePwd = !isRetypePwd" />
                </template>
              </q-input>

              <!-- Submit Button -->
              <q-btn type="submit" class="full-width" color="primary" label="Submit" size="md" :loading="loading" unelevated />
            </q-card-section>
            <q-card-section class="text-center q-pa-none">
              <div class="text-grey-6 q-pa-none">{{ appName }} V-{{ version }}</div>
            </q-card-section>
          </q-form>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { Config } from 'src/services/config'
import { Helper } from 'src/services/helper'
import validate from 'src/services/helper/validate'
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const API = new Api()
const route = useRoute()
const router = useRouter()
const loading = false
const dataModel = ref({
  password: '',
  retype_password: '',
  token: route.query.token ? route.query.token : null
})
const isPwd = ref(true)
const isRetypePwd = ref(true)
const appName = Config.appName()
const version = Config.version()

const init = () => {
  if (route.query.msg) {
    const msg = route.query.msg as string
    Helper.showNotif(msg)
  }
}
const submit = () => {
  if (dataModel.value.password === dataModel.value.retype_password) {
    Helper.loadingOverlay()
    const ep = 'user/forgot-password'
    API.post(ep, dataModel, (status: number, _data: any, message: any) => {
      Helper.loadingOverlay(false)
      if (status === 200) {
        Helper.showAlert('Success', message, true)
        router.push({ name: 'login' })
      } else Helper.showAlert('Error', message)
    })
  } else {
    Helper.showAlert('Error', 'Password does not match')
  }
}

onMounted(init)
</script>
