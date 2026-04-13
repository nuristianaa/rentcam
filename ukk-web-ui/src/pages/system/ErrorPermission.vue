<template>
  <div class="text-center q-pa-md flex flex-center">
    <div>
      <div style="font-size: 30vh">403</div>

      <div class="text-h2" style="opacity: 0.4">Oops. You don't have permission</div>

      <div class="text-subtitle1 text-grey-6 q-mt-sm">You need one of the following permissions:</div>

      <div class="q-mt-md">
        <q-chip color="red-2" text-color="red-8" icon="lock" square>
          {{ historyState.permission }}
        </q-chip>
      </div>

      <div class="text-subtitle2 text-grey-5 q-mt-md">Please contact your administrator or log in with an account that has the correct role.</div>

      <q-btn color="primary" class="q-mt-xl" to="/" label="Go Home" no-caps />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import type { HistoryState } from 'vue-router'

const router = useRouter()
const historyState = ref<HistoryState>({
  permission: router.options.history.state?.permission
})
</script>
