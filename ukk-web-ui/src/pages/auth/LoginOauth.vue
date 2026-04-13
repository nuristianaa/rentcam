<template>
  <q-page class="window-height window-width items-center justify-center">
    <div>Redirecting...</div>
    <!-- {{ dataQuery }} -->
  </q-page>
</template>
<script setup lang="ts">
// import { onMounted, ref, getCurrentInstance } from 'vue'
// import { useRoute, useRouter } from 'vue-router'
// import Api from 'src/services/api'
// import { authStore } from 'src/stores/auth'
// import { msal } from 'src/services/auth/msalInstance'

// const { proxy } = getCurrentInstance()!;
// const route = useRoute()
// const dataQuery = ref(<any>{})
// const API = new Api()
// const Auth = authStore()
// const router = useRouter()

// onMounted(async () => {
//   const queryParams = route.query
//   // If you want to extract specific ones:
//   const code = queryParams.code
//   const state = queryParams.state
//   // console.log('code:', code)
//   // console.log('state:', state)
//   dataQuery.value = queryParams
//   try {
//     const result = await msal.handleRedirectPromise();
//     if (result) {
//       msal.setActiveAccount(result.account);
//       const token = result.accessToken
//       API.post('ms-oauth', { oauth: token }, (status: number, data: { access_token: any; token_expire: any; }) => {
//         if (status === 200) {
//           if (data.access_token) Auth.setToken(data.access_token)
//           if (data.token_expire) Auth.setData('token_expire', data.token_expire)
//           API.get('me', (status: number, data: any) => {
//             if (status === 200) {
//               Auth.setUser(data)
//               auth()
//             }
//           })
//         }
//       })
//     }
//   } catch (err) {
//     console.error(err);
//   }
// });

// const auth = (path = 'controller') => {
//   if (path) router.push({ name: path })
//   else {
//     setTimeout(() => {
//       window.location.assign('/dashboard')
//     }, 500)
//   }
// }
</script>
