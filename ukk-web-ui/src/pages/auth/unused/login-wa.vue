<!-- <template>
  <div>
    <q-form class="q-gutter-md" @submit.prevent="submit">
      <q-card flat class="q-pa-xl q-ma-xl shadow-1 justify-center">
        <h3><strong>Login By Whatsapp</strong></h3>
        <div v-if="step == 1">
          <q-input stack-label dense outlined lazy-rules
            label="Your Phone Number"
            v-model="dataModel.mobile"
            placeholder="6281177772222"
            :rules="[(val) => $Helper.validateRequired(val) || null]"
            mask="#############"
            type="number"
          >
            <template v-slot:prepend>
              <q-icon name="phone" />
            </template>
          </q-input>
          <q-btn class="full-width capital" type="submit" color="primary" label="Submit" size="md" :loading="loading" />
          <q-btn class="q-my-sm full-width capital" @click="$emit('update:modelValue', false)" color="dark" label="Back" size="md" />
        </div>
        <div v-else>
          <InputOtp v-model="dataModel.otp" @complete="submit" />
          <div class="q-my-sm text-center text-h5">{{ timekeeper }}</div>
          <q-btn v-if="resend" class="q-my-xs full-width capital" @click="first()" color="info" label="Resend" size="md" />
          <q-btn class="q-my-xs full-width capital" type="submit" color="primary" label="Submit" size="md" :loading="loading" />
          <q-btn class="q-my-xs full-width capital" @click="step = 1" color="dark" label="Back" size="md" />
        </div>
      </q-card>
    </q-form>
  </div>
</template>
<script>
import Api from '../../services/Api/index'
import InputOtp from './input-otp.vue'

export default {
  name: 'AuthLoginWa',
  props: ['modelValue'],
  emits: ['update:modelValue'],
  components: { InputOtp },
  data() {
    return {
      API: new Api(this.$router),
      loading: false,
      dataModel: {
        mobile: null,
        whatsapp: true,
        otp: null
      },
      step: 1,
      resend: false,
      dataOtp: null,
      timekeeper: null,
      otpArr: [],
      otp: null
    }
  },
  created() {
    //
  },
  methods: {
    submit () {
      if (this.step == 1) this.first()
      if (this.step == 2) this.login()
    },
    first () {
      if (this.dataModel.mobile) {
        const m = this.dataModel.mobile
        if (this.dataModel.mobile.indexOf('0') == 0) this.dataModel.mobile = '62' + m.substring(1, m.length)
        // this.$Helper.showNotif(this.dataModel.mobile)
        this.dataModel.otp = null
        this.loading = true
        this.API.post('user/login', this.dataModel, (status, data, message) => {
          this.loading = false
          if (status === 200) {
            this.$Helper.showSuccess('', message)
            this.step = 2
            this.dataOtp = data
            this.countdown()
          }
        })
      } else this.$Helper.showAlert('Please insert valid mobile number')
    },
    login () {
      this.disableSubmit = true
      this.loading = true
      this.API.post('user/login', this.dataModel, (status, data) => {
        this.loading = false
        if (status === 200) {
          this.$Config.credentials(data)
          this.disableSubmit = false
          this.auth()
        }
      })
    },
    auth (path = 'controller') {
      // this.$Config.init(true, 'login sucess')
      if (path) this.$router.push({ name: path })
      else {
        setTimeout(() => {
          window.location.assign('/dashboard')
        }, 500)
      }
    },
    countdown () {
      const t = Date.parse(new Date(this.dataOtp.expired)) - Date.parse(new Date());
      if (t >= 0){
        const second  = Math.floor(t / 1000 % 60)
        const minute  = Math.floor(t / 1000 / 60 % 60)
        this.timekeeper = `${minute}:${second}`
      } else {
        this.resend = true
      }
      setTimeout(() => {
        this.countdown()
      }, 1000)
    }
  }
}
</script> -->
