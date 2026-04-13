<template>
  <q-input :disable="disabled" :readonly="readonly" class="form-xs" v-model="dataModel" outlined dense @keyup.enter="submit" @blur="submit" :class="dataModel ? ($q.dark.isActive ? 'bg-yellow-9' : 'bg-yellow-1') : ''" :input-class="readonly && dataModel ? 'text-yellow-1' : ''">
    <template v-slot:append>
      <q-icon name="filter_list" round size="15px" class="clickable" clickable>
        <q-menu>
          <div class="q-pa-md" :style="col.datetime ? 'width: 700px;' : 'width: 320px;'">
            <q-form @submit="submitAdv" class="row q-gutter-y-sm">
              <div class="col-12 text-bold">
                Advanced filter
                <q-chip size="xs" label="reset" color="deep-orange" class="text-white clickable" clickable @click="resetFilter" />
              </div>
              <div class="col-12">
                <div class="row q-gutter-sm">
                  <q-btn dense no-caps unelevated class="q-px-sm" v-for="(v, i) in options" :key="i" size="sm" :color="prepend == v.value ? 'primary' : 'grey-3'" :text-color="prepend == v.value ? 'white' : 'dark'" :label="v.label" @click="prepend = v.value" />
                </div>
              </div>

              <!-- FILTERS -->
              <div class="col-12 row">
                <!-- BETWEEN -->
                <div v-if="prepend.indexOf('between') > -1" class="col-12">
                  <!-- BETWEEN DATETIME -->
                  <div v-if="col.datetime" class="row">
                    <q-input class="form-sm col-5" outlined dense v-model="range.from" mask="####-##-## ##:##:##" placeholder="YYYY-MM-DD HH:ii:ss">
                      <template v-slot:append>
                        <PopupDate v-model="range.from" />
                      </template>
                    </q-input>
                    <span class="col-2 text-center q-pt-xs">to</span>
                    <q-input class="form-sm col-5" outlined dense v-model="range.to" mask="####-##-## ##:##:##" placeholder="YYYY-MM-DD HH:ii:ss">
                      <!-- <template v-slot:append>
                        <PopupDate type="range" v-model="range.to"/>
                      </template> -->
                    </q-input>
                    <div class="col-6 row justify-center q-pa-sm">
                      <q-date flat minimal today-btn v-model="range.from" mask="YYYY-MM-DD HH:mm:ss" />
                      <q-time flat minimal with-seconds now-btn v-model="range.from" mask="YYYY-MM-DD HH:mm:ss" />
                    </div>
                    <div class="col-6 row justify-center q-pa-sm">
                      <q-date flat minimal today-btn v-model="range.to" mask="YYYY-MM-DD HH:mm:ss" />
                      <q-time flat minimal with-seconds now-btn v-model="range.to" mask="YYYY-MM-DD HH:mm:ss" />
                    </div>
                  </div>
                  <!-- BETWEEN DATE -->
                  <q-date flat range minimal v-else-if="col.is_date" v-model="range" mask="YYYY-MM-DD" />
                  <!-- BETWEEN NUMBER -->
                  <div v-else class="row">
                    <q-input class="form-sm col-5" outlined dense v-model="range.from" />
                    <span class="col-2 text-center q-pt-xs">to</span>
                    <q-input class="form-sm col-5" outlined dense v-model="range.to" />
                  </div>
                </div>

                <!-- TEXT INPUT -->
                <div v-else-if="prepend.indexOf('null') == -1" class="col-12">
                  <div v-if="col.datetime" class="col-12">
                    <q-input class="form-sm" outlined dense v-model="dataDate" mask="####-##-## ##:##:##" placeholder="YYYY-MM-DD HH:ii:ss">
                      <!-- <template v-slot:append>
                        <q-btn flat dense icon="calendar_month" size="xs" @click="showDate = !showDate"/>
                      </template> -->
                    </q-input>
                    <div class="row justify-center q-pa-sm">
                      <q-date flat minimal today-btn v-model="dataDate" mask="YYYY-MM-DD HH:mm:ss" />
                      <q-time flat minimal with-seconds now-btn v-model="dataDate" mask="YYYY-MM-DD HH:mm:ss" />
                    </div>
                  </div>
                  <div v-else-if="col.is_date" class="col-12">
                    <q-input class="form-sm" outlined dense v-model="dataDate" mask="####-##-##" placeholder="YYYY-MM-DD" />
                    <q-date flat today-btn minimal style="max-width: 50px" v-model="dataDate" mask="YYYY-MM-DD" />
                  </div>
                  <q-input v-else class="form-sm" outlined dense v-model="inputvalue" />
                </div>
              </div>

              <div class="col-12 q-py-xs">
                <q-btn class="full-width" label="submit" type="submit" color="positive" size="sm" v-close-popup></q-btn>
              </div>
            </q-form>
          </div>
        </q-menu>
      </q-icon>
    </template>
  </q-input>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import PopupDate from './HTPopupDate.vue'

const props = defineProps<{
  modelValue: string | null
  col: any
  refresh: number
}>()
const emit = defineEmits(['update:modelValue'])

const dataModel = ref('')
const prepend = ref('null')
const inputvalue = ref('')
const dataDate = ref('')
const range = ref({ from: '', to: '' })

const slug = ref('')
slug.value = `s${props.col.name}`

const disabled = ref(false)
const readonly = ref(false)
const showDate = ref(false)
if (props.col.name === 'action' || props.col.filterHide) disabled.value = true
if (props.col.is_date || ['float', 'integer'].includes(props.col.formatter)) readonly.value = true

const options = ref<Array<{ value: string; label: string }>>([])
const optNull = [
  { value: 'null', label: 'Is empty' },
  { value: 'notnull', label: 'Is not empty' }
]
options.value =
  props.col.is_date || ['float', 'integer'].includes(props.col.formatter)
    ? [
        ...optNull,
        { value: 'gt:', label: 'Greater than' },
        { value: 'gte:', label: 'Greater than or equal to' },
        { value: 'lt:', label: 'Less than' },
        { value: 'lte:', label: 'Less than or equal to' },
        { value: 'is:', label: 'Is equal to' },
        { value: 'isnot:', label: 'Is not equal to' },
        { value: 'between:', label: 'Is between' },
        { value: 'notbetween:', label: 'Is not between' }
      ]
    : [...optNull, { value: 'notlike:', label: 'Text does not contain' }, { value: 'start:', label: 'Text starts with' }, { value: 'end:', label: 'Text ends with' }, { value: 'is:', label: 'Text is exactly' }, { value: 'isnot:', label: 'Text is exactly not' }, { value: 'in:', label: 'Multiple exact (comma separated)' }]

// METHODS
const reset = () => {
  prepend.value = 'null'
  inputvalue.value = ''
  range.value.from = ''
  range.value.to = ''
  dataModel.value = ''
}

const resetFilter = () => {
  reset()
  submit()
}

const submitAdv = () => {
  let exec = true
  if (prepend.value.includes('null')) inputvalue.value = ''

  if (['float', 'integer'].includes(props.col.formatter)) {
    const isNumberValid = (!inputvalue.value || !isNaN(Number(inputvalue.value))) && (!range.value.from || !isNaN(Number(range.value.from))) && (!range.value.to || !isNaN(Number(range.value.to)))

    if (!prepend.value) {
      exec = false
      alert('Please select command first!')
    } else if (!isNumberValid) {
      exec = false
      alert('Please input number only!')
    }
  }

  if (exec) {
    let val = ''
    if (prepend.value.includes('between') && range.value.from && range.value.to) {
      if (props.col.millis && range.value.to) {
        range.value.from = new Date(range.value.from).getTime().toString()
        range.value.to = new Date(range.value.to).getTime().toString()
      }
      val = `${range.value.from} to ${range.value.to}`
    } else {
      if (props.col.millis && dataDate.value) {
        inputvalue.value = new Date(dataDate.value).getTime().toString()
      } else if (props.col.datetime || props.col.is_date) {
        inputvalue.value = dataDate.value
      }
      val = inputvalue.value
    }
    dataModel.value = `${prepend.value}${val}`
    submit()
  }
}

const submit = () => {
  emit('update:modelValue', dataModel.value)
}

watch(() => props.refresh, reset)
</script>

<style lang="scss">
.header-label {
  border-color: #f8f8f8;
}
.header-form {
  .q-field__control {
    min-height: 10px !important;
    height: 10px !important;
  }
  .q-select__dropdown-icon {
    visibility: hidden !important;
  }
  .q-field__input,
  .q-field__native {
    font-weight: 600;
    font-size: 5px !important;
  }
}
</style>
