

<template>
	<q-page class="window-height window-width row standard-font">
		<div class="row col-md-12 col-12 flex flex-center items-center justify-center" style="min-height:100vh;">
			<div class="bg-white window-height window-width flex flex-center items-center justify-center" style="width:100vw;">
				<div class="shadow-1 flex items-center justify-center" style="width:100vw;min-height:100vh;">
					<div class="col-md-4 col-12 flex flex-center items-center justify-center" style="margin:auto;max-width:420px;width:100vw;">
						<q-form class="q-gutter-md" @submit.prevent="onSubmit" style="text-align: center;width:100%;">
							<q-img src="~assets/image.png" width="300px" class="q-mr-md q-mb-md" style="margin:auto;" />
							<div class="q-pa-md q-ma-md justify-center text-white full-width">
								<div class="q-pb-sm column q-gutter-y-none q-mb-lg">
									<div style="font-size: 2.6rem">
										<strong>RENT - UKK</strong>
									</div>
								</div>
								<q-input filled v-model="form.username" label="Username" class="q-mb-md" :rules="[val => !!val || 'Username wajib diisi']">
									<template v-slot:prepend>
										<q-icon name="person" />
									</template>
								</q-input>
								<q-input filled v-model="form.email" label="Email" type="email" class="q-mb-md" :rules="[val => !!val || 'Email wajib diisi']">
									<template v-slot:prepend>
										<q-icon name="email" />
									</template>
								</q-input>
								<q-input filled v-model="form.name" label="Nama Lengkap" class="q-mb-md" :rules="[val => !!val || 'Nama wajib diisi']">
									<template v-slot:prepend>
										<q-icon name="badge" />
									</template>
								</q-input>
								<q-input filled v-model="form.password" :type="isPwd ? 'password' : 'text'" label="Password" class="q-mb-md" :rules="[val => val && val.length >= 8 || 'Min 8 karakter']">
									<template v-slot:prepend>
										<q-icon name="lock" />
									</template>
									<template v-slot:append>
										<q-icon :name="isPwd ? 'visibility_off' : 'visibility'" class="cursor-pointer" @click="isPwd = !isPwd" />
									</template>
								</q-input>
								<q-input filled v-model="form.phone" label="No. HP" type="tel" class="q-mb-md">
									<template v-slot:prepend>
										<q-icon name="phone" />
									</template>
								</q-input>
								<q-btn class="q-py-sm full-width capital" type="submit" color="primary" label="Daftar" size="md" style="border-radius: 100px" :loading="loading"/>
							</div>
							<div class="text-center q-pa-md q-pt-lg">
								<div class="text-black-6 q-pa-none">{{ new Date().getFullYear() }} rent-ukk | All Rights Reserved.</div>
							</div>
							<div class="text-caption text-center q-mt-sm">
								Sudah punya akun? <router-link to="/login">Login</router-link>
							</div>
						</q-form>
					</div>
				</div>
			</div>
		</div>
	</q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import Api from 'src/services/api'

const $q = useQuasar()
const router = useRouter()
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
		loading.value = false
		if (status === 200) {
			$q.notify({
				type: 'positive',
				message: 'Registrasi berhasil! Silakan login.',
				timeout: 1200,
				onDismiss: () => { void router.push('/login') }
			})
		} else {
			$q.notify({ type: 'negative', message: msg || 'Registrasi gagal' })
			form.value = { username: '', email: '', name: '', password: '', phone: '' }
		}
	}, 'identity')
}
</script>

<style scoped>
.full-width { width: 100%; }
</style>
