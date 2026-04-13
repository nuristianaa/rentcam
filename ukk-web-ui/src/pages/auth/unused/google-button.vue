<!-- <template>
  <div class="text-center">
    <div class="q-pa-md">{{$Lang.sign_in_with}}</div>
    <q-btn no-caps size="md" @click="handleClickSignIn" :disabled="!Vue3GoogleOauth.isInit" :loading="loading"
      style="color: #444; border-radius: 5px; border: thin solid #888; padding-top: 0px;"
    >
      <img src="~assets/logo/google.png" style="height:25px; width:25px">
      <span class="buttonText">Google</span>
    </q-btn>

  </div>
  </template>

  <script>
  import { inject, toRefs } from 'vue';
  import Api from '../../services/Api/index'

  export default {
    name: 'google-button',
    props: [
      'remember',
      'firebase'
    ],
    data(){
      return {
        API: new Api(this.$router),
        loading: false
      }
    },

    methods: {
      async handleClickSignIn(){
        this.$Helper.loadingOverlay()
        try {
          const googleUser = await this.$gAuth.signIn();
          console.log(googleUser)
          if (!googleUser) return null
          else this.loginWithGoogle(googleUser)
        } catch (error) {
          this.$Helper.loadingOverlay(false)
          console.error(error);
          return null
        }
      },

      loginWithGoogle (googleUser) {
        let extract = Object.values(googleUser)
        let name = null
        let email = null
        let picture = null
        extract.forEach(element => {
          if (element) {
            let profiles = Object.values(element)
            if (profiles.length > 0 && profiles.length < 8) {
              console.log(profiles)
              profiles.forEach(profile => {
                let el = null
                if (profile) el = profile.toString()
                /* EMAIL */
                if (el) {
                  if (this.$Helper.strMatch(el, '@')) {
                    email = el
                    const split = el.split('@')
                    if (split[0] !== undefined) name = split[0]
                  }
                  /* NAME */
                  if (this.$Helper.strMatch(el, ' ')) name = el
                  /* PICTURE */
                  if (this.$Helper.strMatch(el, 'http')) {
                    if (!this.$Helper.strMatch(el, 'openid')) picture = el
                  }
                  if (this.$Helper.strMatch(el, 'content')) picture = el
                }
              })
            }
          }
        })
        if (email) {
          const dataModel = {
            name: name,
            email: email,
            picture: picture,
            firebase_token: this.firebase,
            type: 'google',
            remember_me: this.remember
          }
          this.login(dataModel)
        }
        console.log('goo', extract);
      },

      login (dataModel) {
        console.log('profile', dataModel)
        this.loading = true
        this.API.cache = false
        this.API.post('user/login/google', dataModel, (status, data, message, response, full) => {
          // console.log({ status, data, message, response, full });
          this.loading = false
          this.$Helper.loadingOverlay(false)
          if (status === 200) {
            this.$Config.credentials(data);
            this.auth();
          }
        })
      },

      auth (path = null) {
        this.$Config.init(true, 'login sucess')
        if (path) this.$router.push({ name: path })
        else {
          setTimeout(() => {
            window.location.assign('/')
          }, 500)
        }
      },

    },
    setup(props) {
      const { isSignIn } = toRefs(props);
      const Vue3GoogleOauth = inject('Vue3GoogleOauth');

      const handleClickLogin = () => {};
      return {
        Vue3GoogleOauth,
        handleClickLogin,
        isSignIn,
      };
    },
  }

  /*
    async handleClickGetAuthCode(){
      try {
        this.user = googleUser.getBasicProfile().getEmail();
        const authCode = await this.$gAuth.getAuthCode();
        console.log("authCode:", authCode, "gAuth:", this.$gAuth);
      } catch(error) {
        //on fail do something
        console.error(error);
        return null;
      }
    },

    async handleClickSignOut() {
      try {
        await this.$gAuth.signOut();
        console.log("isAuthorized", this.Vue3GoogleOauth.isAuthorized);
        this.user = "";
      } catch (error) {
        console.error(error);
      }
    },

    handleClickDisconnect() {
      window.location.href = `https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=${window.location.href}`;
    },


  */
  </script>

  <style>
  button:disabled {
    background: #fff;
    color: #ddd;
    cursor: not-allowed;
  }
  .customBtn {
    height: 40px;
    /* width: 190px; */
    /* display: inline-block; */
    background: white;
    color: #444;
    border-radius: 5px;
    border: thin solid #888;
    box-shadow: 1px 1px 1px grey;
    /* white-space: nowrap; */
  }
  .customBtn:hover {
    cursor: pointer;
  }
  span.label {
    font-family: serif;
    font-weight: normal;
  }
  span.buttonText {
    display: inline-block;
    vertical-align: middle;
    padding-left: 15px;
    padding-right: 35px;
    font-size: 14px;
    font-weight: bold;
    /* Use the Roboto font that is loaded in the <head> */
    font-family: "Roboto", sans-serif;
  }
  </style>
   -->
