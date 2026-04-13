<template>
  <q-layout view="hhh lpR fFf" class="body">
    <q-page-container>
      <s-loading v-if="loading" />
      <h-form v-else :meta="Meta" type="form" :disable-submit="disableSubmit" @submit="submit">
        <div class="row q-pa-sm">
          <f-card title="APP Config" row>
            <div class="col-12 q-pa-sm">
              <div class="row justify-between">
                <q-toggle label="login" v-model="dataModel.login" />
                <q-btn to="/login" label="LOGIN PAGE" color="primary" size="lg" />
              </div>
            </div>
            <f-input col="6" label="url" v-model="dataModel.url" required />
            <f-input col="6" label="rental" v-model="dataModel.rental" />
            <!-- <f-input col="6" label="vms" v-model="dataModel.vms" /> -->
            <f-input col="6" label="weigh" v-model="dataModel.weigh" />
            <div class="column q-pa-sm">
              <q-btn-toggle
                v-model="model"
                push
                glossy
                toggle-color="primary"
                @click="changeData()"
                :options="[
                  { label: 'local', value: 'local' },
                  { label: 'stag', value: 'stag' },
                  { label: 'prod', value: 'prod' }
                ]"
              />
            </div>
          </f-card>
        </div>
      </h-form>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Meta from './meta'
import { configStore } from 'src/stores/config'
import { Helper } from 'src/services/helper'

const loading = ref(true)
const dataModel = ref(Meta.model)
const model = ref(null)
const disableSubmit = false
const hostname = window.location.hostname

if (hostname == 'localhost') loading.value = false
else loading.value = true

const changeData = () => {
  if (model.value == 'local') {
    dataModel.value.url = 'http://localhost:8190/'
    dataModel.value.rental = 'http://localhost:8191/'
  } else if (model.value == 'stag') {
    dataModel.value.url = 'http://localhost:8190/'
    dataModel.value.rental = 'http://localhost:8191/'
  } else if (model.value == 'prod') {
    dataModel.value.url = 'http://localhost:8190/'
    dataModel.value.rental = 'http://localhost:8191/'
  }
}

const submit = () => {
  configStore().saveConfig(dataModel.value)
  Helper.showSuccess('Save Succesfully', 'Okeeee')
}
</script>
