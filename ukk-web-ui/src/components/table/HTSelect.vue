<template>
  <q-input readonly class="form-xs" v-model="dataModel" outlined dense @keyup.enter="submit" @blur="submit" :class="dataModel ? 'bg-yellow-1' : ''" :input-class="dataModel ? 'text-yellow-1' : ''">
    <template v-slot:append>
      <q-icon name="filter_list" round size="15px" class="clickable" clickable></q-icon>
      <q-menu>
        <q-form @submit="submit" class="row q-pa-md">
          <div class="col-12 q-py-sm">
            <q-btn class="q-my-xs full-width" label="submit" type="submit" color="primary" size="xs" v-close-popup />
            <q-btn class="q-my-xs full-width" label="reset" color="deep-orange" size="xs" @click="init()" />
          </div>
          <div class="col-12" style="max-height: 50vh; overflow: auto">
            <div class="col-12 q-pb-sm">
              <div class="row q-gutter-md">
                <q-btn dense no-caps unelevated class="q-px-sm" v-for="(v, i) in optNull" :key="i" size="sm" :color="dataNull == v.value ? 'primary' : 'grey-3'" :text-color="dataNull == v.value ? 'white' : 'dark'" :label="v.label" @click="dataNull = v.value" />
              </div>
            </div>
            <div v-if="dataNull == ''">
              <div class="col-12" v-for="(v, i) in options" :key="i">
                <q-checkbox dense size="sm" v-model="dataSelect" :val="v?.id ?? v" :label="v?.name ?? v" />
              </div>
            </div>
          </div>
        </q-form>
      </q-menu>
    </template>
  </q-input>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { onMounted, ref, watch } from 'vue'

const props = defineProps<{
  modelValue: string | null
  col: any
  refresh: number
}>()
const emit = defineEmits(['update:modelValue'])

const API = new Api()
const dataSelect = ref<string[]>([])
const dataModel = ref<string>('')
const options = ref<Array<{ id: string; name: string }>>([])
const dataNull = ref<string>('')
const optNull = ref([
  { value: '', label: 'Choose' },
  { value: 'null', label: 'Is empty' },
  { value: 'notnull', label: 'Is not empty' }
])

// METHODS
const init = () => {
  dataSelect.value = []
  dataNull.value = ''
  dataModel.value = ''
  if (props.col.opt) options.value = props.col.opt
  else if (props.col.api) getFromApi(props.col.api)
  else if (props.col.formatter === 'boolean') getBooleanOpts()
}

const getFromApi = (api: { url: string; key?: string; label?: string }) => {
  const { url, key = 'id', label = 'name' } = api
  if (url) {
    API.get(url, (status: number, data: any) => {
      if (status === 200) {
        const optionsList = data?.items ?? data
        optionsList.forEach((e: any) => {
          options.value.push({ id: e[key], name: e[label] })
        })
      }
    })
  }
}

const getBooleanOpts = () => {
  options.value = [
    { id: 'True', name: 'True' },
    { id: 'False', name: 'False' }
  ]
}

const submit = () => {
  let model = null
  if (dataNull.value != '') model = dataNull.value
  else if (dataSelect.value.length > 0) {
    dataModel.value = dataSelect.value.toString()
    model = `in:${dataModel.value}`
  }
  emit('update:modelValue', model)
}

// MOUNTED | WATCHERS
onMounted(() => {
  init()
})
watch(() => props.refresh, init)
</script>
