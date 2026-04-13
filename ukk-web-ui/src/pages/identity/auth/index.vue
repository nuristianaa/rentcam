<template>
    <q-layout view="hHh lpR fFf"> <!-- Full-screen layout -->
      <!-- Main Layout -->
      <q-page-container>
        <q-page class="login-page">
          <div class="login-container">
            <q-form class="q-gutter-md" @submit.prevent="login">
              <q-card flat class="q-pa-md shadow-1 justify-center">
                <h3><strong>Login</strong></h3>
                <q-input stack-label dense outlined lazy-rules
                  icon="person"
                  label="Username"
                  v-model="dataModel.username"
                  placeholder="username"
                  :rules="[(val) => $Helper.validateRequired(val) || '']"
                >
                  <template v-slot:prepend>
                    <q-icon name="person" />
                  </template>
                </q-input>
                <q-input stack-label dense outlined lazy-rules
                  icon="lock"
                  :label="$Lang.login.password"
                  v-model="dataModel.password"
                  :type="isPwd ? 'password' : 'text'"
                  placeholder="**********"
                  :rules="[(val) => $Helper.validateRequired(val) || '']"
                >
                  <template v-slot:append>
                    <q-icon
                      :name="isPwd ? 'visibility_off' : 'visibility'"
                      class="cursor-pointer"
                      @click="isPwd = !isPwd"
                    />
                  </template>
                  <template v-slot:prepend>
                    <q-icon name="lock" />
                  </template>
                </q-input>
  
                <!-- Remember & Forgot Password  -->
                <div class="row q-pb-sm justify-between">
                  <q-toggle v-model="dataModel.remember_me" checked-icon="check" :label="$Lang.remember_me" />
                </div>
  
                <!-- Submit Button -->
                <q-btn type="submit" color="primary" class="btn-bmb full-width capital" label="Login" size="md"  :loading="loading" >
                  <template v-slot:loading>
                    <q-spinner-puff />
                  </template>
                </q-btn>
  
                <!-- Register Button -->
                <!-- <div v-if="$Config.signup()" class="row q-mt-md justify-center items-end">
                  <q-btn class="text-weight-regular" no-caps dense flat :label="$Lang.signUpLabel" />
                  <q-btn to="/signup" no-caps dense flat color="primary" :label="$Lang.signupButton" />
                </div> -->
  
                <q-card-section class="text-center q-pa-none q-my-md">
                  <div class="text-grey-6 q-pa-none">{{ $Config.appName() }} V-{{ $Config.version() }}</div>
                  <div class="text-grey-6 q-pa-none">{{ $Config.copyright() }}</div>
                </q-card-section>
              </q-card>
            </q-form>
          </div>
        </q-page>
      </q-page-container>
    </q-layout>
  </template>
  
  <script>
  export default {
    name: 'LoginPage',
    data () {
      return {
        API: this.$Api,
        dataModel: {
            username: '',
            password: '',
            remember_me: false,
        },
        isPwd: true,
        loading: false
      }
    },
    methods: {
      login () {
        this.disableSubmit = true
        this.loading = true
        this.API.post('token', this.dataModel, (status, data) => {
          this.loading = false
          if (status === 200) {
            this.$Config.credentials(data)
            this.disableSubmit = false
            this.auth()
          }
        })
      },
      auth (path = 'controller') {
        const query = this.$route.query
        if(query && query.app != null && query.redirect == 1) {
          const q = Object.keys(query).map(function(key) {
            if(key !== 'token') return `${key}=${encodeURIComponent(query[key])}`
          }).join('&');

          const token = this.$Config.getLdb('token') || this.$Config.getSdb('token')
          const app = Object.keys(query).find((key) => key == 'app')
          const url = this.$Config.appUrl(app)

          setTimeout(() => {
            window.location.replace(`${url}/login?${q}&token=${token}`)
          }, 500)
        }
        else if (path && !query) this.$router.push({ name: path })
        else {
          setTimeout(() => {
            window.location.assign('/')
          }, 500)
        }
      },
    }
  }
  </script>
  
  <style scoped>
  .login-page {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f5f5f5;
  }
  
  .login-container {
    max-width: 400px;
    width: 100%;
  }
  
  .full-width {
    width: 100%;
  }
  </style>
  