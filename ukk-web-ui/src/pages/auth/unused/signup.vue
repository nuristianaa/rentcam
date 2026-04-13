<template>Unused</template>

<!-- <template>
  <q-page class="window-height window-width row standard-font col-12">
    <div v-if="$Config.signup()" class="row col-lg-6 col-12">
      <div class="row fit col-12">
        <q-card class="shadow-1 fit row items-center justify-center col-12">
          <q-form class="q-gutter-md" @submit.prevent="submit">
            <div class="col-12 text-center text-h4 text-weight-bold">
              Sign Up
            </div>
            <div class="col-12 text-center text-grey">
              Enter your personal information
            </div>
            <q-card-section class="q-pt-md q-pb-none justify-center">
              <q-input stack-label dense outlined
                :label="$Lang.login.name"
                v-model="dataModel.name"
                lazy-rules :rules="[(val) => $Helper.validateRequired(val) || '']"
              />
              <q-input stack-label dense outlined
                :label="$Lang.login.email"
                v-model="dataModel.email"
                type="email"
                placeholder="mail@website.com"
                lazy-rules :rules="[(val) => $Helper.validateRequired(val) || '']"
              />
              <q-input stack-label dense outlined
                :label="$Lang.login.mobile"
                v-model="dataModel.mobile"
                lazy-rules :rules="[(val) => (val !== ' ') || '']"
              />
              <q-input stack-label dense outlined
                :label="$Lang.login.password"
                v-model="dataModel.password"
                :type="isPwd ? 'password' : 'text'"
                placeholder="**********"
                lazy-rules
                :rules="[(val) => $Helper.validateRequired(val) || '']"
              >
                <template v-slot:append>
                  <q-icon :name="isPwd ? 'visibility_off' : 'visibility'" class="cursor-pointer" @click="isPwd = !isPwd" />
                </template>
              </q-input>
              <q-input stack-label dense outlined
                :label="$Lang.login.retype_password"
                v-model="dataModel.retype_password"
                :type="isRetypePwd ? 'password' : 'text'"
                placeholder="**********"
                lazy-rules :rules="[(val) => $Helper.validateRequired(val) || '']"
              >
                <template v-slot:append>
                  <q-icon :name="isRetypePwd ? 'visibility_off' : 'visibility'" class="cursor-pointer" @click="isRetypePwd = !isRetypePwd" />
                </template>
              </q-input>

              <q-btn type="submit" class="full-width" color="primary" :label="$Lang.signupButton" size="md" :loading="loading" unelevated />
              <div class="row q-mt-md justify-center items-end">
                <q-btn class="text-weight-regular" no-caps dense flat :label="$Lang.loginLabel" />
                <q-btn to="/login" no-caps dense flat color="primary" :label="$Lang.loginButton" />
              </div>
            </q-card-section>
            <q-card-section class="text-center q-pa-none">
              <div class="text-grey-6 q-pa-none">{{ appName }} V-{{ version }}</div>
              <div class="text-grey-6 q-pa-none">&copy; 2022</div>
            </q-card-section>
          </q-form>
        </q-card>
      </div>
    </div>
    <div class="row col-lg-6 col-12" v-if="$q.screen.gt.md">
      <div class="row fit col-12">
        <q-img spinner-color="white" class="z-top" src="~/assets/background.png" />
      </div>
    </div>
  </q-page>
</template>
<script>
import Api from '../../services/Api/index'

export default {
  name: 'AuthSignup',
  data() {
    return {
      API: new Api(this.$router),
      loading: false,
      dataModel: {
        name: '',
        email: '',
        mobile: '',
        password: '',
        retype_password: '',
      },
      isPwd: true,
      isRetypePwd: true,
      disableSubmit: false,
      appName: this.$Config.appName(),
      version: this.$Config.version(),
      version_be: null
    };
  },

  methods: {

    submit () {
      if (this.dataModel.password === this.dataModel.retype_password) {
        this.disableSubmit = true
        this.loading = true
        this.API.cache = false
        this.API.post('user/signup', this.dataModel, (status, data, message, response, full) => {
          this.loading = false;
          console.log({ status, data, message, response, full })
          if (status === 200) {
            this.$Helper.showAlert('Success', this.$Lang.login.activationAlert, true)
            this.$router.push({ name: 'login' })
          }
        })
      } else {
        this.$Helper.showAlert('Error', 'Password does not match')
      }
    }

  }
}
</script>
-->
