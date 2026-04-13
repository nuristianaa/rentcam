<template>
  <div class="flex flex-center">
    <q-card style="width: 800px; max-width: 80vw">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">Reset Password</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>
      <q-form @submit.prevent="submit">
        <q-card-section class="q-pt-md">
          <q-input v-model="email" type="email" label="email *" lazy-rules :rules="[(val) => validate.validateRequired(val) || 'Please type your email']" />
          <q-card-actions align="right">
            <div class="row q-mt-xs">
              <q-btn type="submit" class="q-pl-md text-capitalize -borders" label="Ok" color="primary" />
            </div>
          </q-card-actions>
        </q-card-section>
      </q-form>
    </q-card>
  </div>
</template>
<script setup lang="ts">
import validate from 'src/services/helper/validate'
import { ref } from 'vue'

const emits = defineEmits(['resetPassword'])
const email = ref(null)
const submit = () => {
  emits('resetPassword', email.value)
}
</script>
