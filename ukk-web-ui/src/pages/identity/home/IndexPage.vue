<template>
  <div>
    <div class="my-background">
      <div class="row q-mx-md">
        <div class="col-12 q-mt-xl q-pt-xl">
          <div class="row" style="height: 72.5vh">
            <div class="col-12">
              <div class="q-ml-xl q-pl-xl">
                <div class="text-left">
                  <h1 class="typewriter text-weight-bolder" style="font-size: 4em; color: white">{{ line1 }}</h1>
                  <h1 class="typewriter" style="font-size: 4em; color: white; font-weight: 300">{{ line2 }}</h1>
                  <p style="color: white; line-height: 25px">RENTAL APP | Uji Kompetensi Keahlian</p>
                </div>
              </div>
            </div>
            <div v-if="!HaveAttendance" class="row justify-center q-ml-xl">
              <div class="col-12">
                <q-card class="q-pa-lg text-center q-ml-xl" style="border-radius: 16px">
                  <q-icon name="how_to_reg" size="48px" color="primary" />
                  <div class="text-h4 q-mt-md q-mb-lg">Silahkan absen terlebih dahulu dengan memilih opsi kehadiran</div>
                  <!-- <f-select v-model="dataModel.status" :label="Lang.module(Meta, 'status')" required :options="Constant.hris.transaction.attendance.status" /> -->
                   <div class="row justify-center gap">
                    <q-btn
                      color="primary"
                      class="q-mr-md"
                      label="Present"
                      size="lg"
                      unelevated
                      @click="handleAbsen('PRESENT')"
                    />
                    <q-btn
                      color="warning"
                      class="q-mr-md"
                      label="Sick"
                      size="lg"
                      unelevated
                      @click="openSickForm"
                    />
                    <q-btn
                      color="negative"
                      label="Leave"
                      size="lg"
                      unelevated
                      @click="openLeaveForm"
                    />
                   </div>
                </q-card>
              </div>
            </div>
            <div v-else>
              <div v-if="dataModel[0].status != 'PRESENT'" class="row justify-center q-ml-xl">
                <div class="col-12">
                  <q-card class="q-pa-lg text-center q-ml-xl" style="border-radius: 16px">
                    <q-icon name="how_to_reg" size="48px" color="primary" />
                    <div class="text-h4 q-mt-md q-mb-lg">Anda Sudah Absen Hari ini</div>
                  </q-card>
                </div>
              </div>
              <div v-else>
                <div v-if="!isAfter17" class="row justify-center q-ml-xl">
                  <div class="col-12">
                    <q-card class="q-pa-lg text-center q-ml-xl" style="border-radius: 16px">
                      <q-icon name="how_to_reg" size="48px" color="primary" />
                      <div class="text-h4 q-mt-md q-mb-lg">Anda Sudah Absen Hari ini, Silahkan Absen Lagi Saat Jam Keluar</div>
                    </q-card>
                  </div>
                </div>
                <div v-else class="row justify-center q-ml-xl">
                  <div v-if="!dataModel[0].clock_out">
                    <div class="col-12">
                      <q-card class="q-pa-lg text-center q-ml-xl" style="border-radius: 16px">
                        <q-icon name="how_to_reg" size="48px" color="primary" />
                        <div class="text-h4 q-mt-md q-mb-lg">Silahkan absen keluar</div>
                        <div class="row justify-center gap">
                          <q-btn
                            color="primary"
                            class="q-mr-md"
                            label="Check Out"
                            size="lg"
                            unelevated
                            @click="handleAbsen('PRESENT')"
                          />
                        </div>
                      </q-card>
                    </div>
                  </div>
                  <div v-else>
                    <div class="col-12">
                      <q-card class="q-pa-lg text-center q-ml-xl" style="border-radius: 16px">
                        <q-icon name="how_to_reg" size="48px" color="primary" />
                        <div class="text-h4 q-mt-md q-mb-lg">Anda Sudah Absen Hari ini</div>
                      </q-card>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <q-dialog v-model="showSickDialog" persistent>
              <q-card style="min-width: 400px; border-radius: 16px">
                <q-card-section class="row items-center q-pb-none">
                  <q-icon name="event_busy" size="28px" color="warning" class="q-mr-sm" />
                  <span class="text-h6">Alasan Sakit</span>
                  <q-space />
                  <q-btn icon="close" flat round dense v-close-popup />
                </q-card-section>

                <q-card-section>
                  <q-input
                    v-model="sickReason"
                    label="Tulis alasan..."
                    type="textarea"
                    outlined
                    autogrow
                    autofocus
                    rows="3"
                  />
                </q-card-section>

                <q-card-actions align="right" class="q-pa-md">
                  <q-btn flat label="Batal" v-close-popup />
                  <q-btn
                    color="green"
                    label="Kirim"
                    unelevated
                    @click="submitSick"
                  />
                </q-card-actions>
              </q-card>
            </q-dialog>
            <q-dialog v-model="showLeaveDialog" persistent>
              <q-card style="min-width: 400px; border-radius: 16px">
                <q-card-section class="row items-center q-pb-none">
                  <q-icon name="event_busy" size="28px" color="negative" class="q-mr-sm" />
                  <span class="text-h6">Alasan Tidak Hadir</span>
                  <q-space />
                  <q-btn icon="close" flat round dense v-close-popup />
                </q-card-section>

                <q-card-section>
                  <q-input
                    v-model="leaveReason"
                    label="Tulis alasan..."
                    type="textarea"
                    outlined
                    autogrow
                    autofocus
                    rows="3"
                  />
                </q-card-section>

                <q-card-actions align="right" class="q-pa-md">
                  <q-btn flat label="Batal" v-close-popup />
                  <q-btn
                    color="green"
                    label="Kirim"
                    unelevated
                    @click="submitLeave"
                  />
                </q-card-actions>
              </q-card>
            </q-dialog>
          </div>
        </div>
      </div>
    </div>

    <q-dialog v-model="showDetail">
      <q-card v-if="dataModel" position="right">
        <s-loading v-if="loading" />
        <div v-else class="row q-pa-lg">
          <div style="width: 100%">
            <div class="row justify-between">
              <div class="title q-pt-sm">{{ dataModel?.title }}</div>
              <q-icon v-if="dataModel?.icon" size="md" :color="dataModel?.color" text-color="white" :name="dataModel?.icon" />
            </div>
            <q-separator class="q-my-md" color="primary" />
            <div class="row q-my-md">
              <div class="col" v-html="dataModel?.description" />
            </div>
            <q-btn v-if="dataModel?.path" class="q-my-md" color="primary" icon="open_in_new" label="View" @click="toLink(dataModel.path)" />
          </div>
        </div>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import Api from 'src/services/api'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { authStore } from 'src/stores/auth'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Constant } from 'src/services/constant'
import { Lang } from 'src/services/lang'
import { Meta } from './meta'
import type { DataModel } from './meta'

const line1 = ref('')
const line2 = ref('')

const route = useRoute()
const API = new Api()
const loading = ref(true)
const dataModel = ref<DataModel>(Meta.model)
const showDetail = ref(false)
const Auth = authStore()
const refresh = ref(0)
const HaveAttendance = ref(false)
const isAfter17 = ref(false)
const showLeaveDialog = ref(false)
const showSickDialog = ref(false)
const leaveReason = ref('')
const sickReason = ref('')

function typeWriter(text: string, target: typeof line1, speed = 200) {
  let index = 0

  function type() {
    if (index < text.length) {
      target.value += text.charAt(index)
      index++
      setTimeout(type, speed)
    }
  }

  type()
}

const openLeaveForm = () => {
  leaveReason.value = ''
  showLeaveDialog.value = true
}

const openSickForm = () => {
  sickReason.value = ''
  showSickDialog.value = true
}

const submitLeave = async () => {
  if (!leaveReason.value.trim()) {
    Helper.showNotif('Alasan tidak boleh kosong')
    return
  }
  showLeaveDialog.value = false
  await handleAbsen('LEAVE')
}
const submitSick = async () => {
  if (!sickReason.value.trim()) {
    Helper.showNotif('Alasan tidak boleh kosong')
    return
  }
  showSickDialog.value = false
  await handleAbsen('SICK')
}

const checkTime = () => {
  const now = new Date()
  const hour = now.getHours()
  const minute = now.getMinutes()
  const totalMinutes = hour * 60 + minute

  const startMinutes = 7 * 60 + 30   // 07:30
  const endMinutes = 17 * 60    // 17:00
  if (totalMinutes >= endMinutes || totalMinutes < startMinutes)
  isAfter17.value = true
}

const onRefresh = () => {
  refresh.value += 1
}

const getData = () => {
    loading.value = true
    const endpoint = `${Meta.module}?where=username:${Auth.user.username}&where=date:${Helper.today()}&like=deleted_at:null`
    API.get(endpoint, (status: number, data: any) => {
      loading.value = false
      if (status === 200) {
        if (data.length === 0){
          HaveAttendance.value = false
        } else {
          HaveAttendance.value = true
          dataModel.value = data
          console.log(dataModel.value)
          onRefresh()
        }
      }
    }, Meta.app)
  }

const handleAbsen = async (type : string) => {
  if (validateSubmit()) {
    loading.value = true
    // Store execution
    let status = 600
    status = await save(type)
    // Action after store
    if (status === 200) {
      Helper.showSuccess('Data has been successfully saved.')
      onRefresh()
      getData()
    }
    loading.value = false
  }
}

const validateSubmit = () => {
  
  const msg = '' // change const to let if any validations
  // Validations
  // example: if (dataModel.value.app == null) msg += 'App cannot be null'
  // Execution
  if (msg === '') return true
  else {
    Helper.showNotif(msg)
    return false
  }
}

const save = async (type: string) => {
  let statusapi = 600
  if (!HaveAttendance.value){
    dataModel.value.date = Helper.today()
    dataModel.value.clock_in = Helper.now()
    dataModel.value.status = type
    dataModel.value.remark = type === 'LEAVE' ? leaveReason.value : null
    dataModel.value.employee_id = Auth.user.employee_id
    dataModel.value.nik = Auth.user.employee_nik
    dataModel.value.username = Auth.user.username
    await API.post(Meta.module, dataModel.value, (status: number, _data: any) => {
      statusapi = status
    }, Meta.app)
  } else {
    dataModel.value[0].clock_out = Helper.now()
    await API.put(`${Meta.module}/${dataModel.value[0].id}`, dataModel.value[0], (status: number, _data: any) => {
      statusapi = status
    }, Meta.app)
  }
  
  return statusapi
}


// EVENT NOTIF HANDLER
const init = () => {
  if (route.params?.notif_id) {
    readNotif(route.params?.notif_id)
  }
  getData()
  checkTime()
}

const readNotif = (notif_id: any) => {
  loading.value = true
  dataModel.value = null

  // Mock API call, replace with actual API logic
  void API.get(
    `auth/notifications/${notif_id}`,
    (status: number, data: Notification) => {
      if (status === 200) dataModel.value = data
      loading.value = false
      showDetail.value = true
    },
    'main'
  )
}

function toLink(path: string) {
  const link = document.createElement('a')
  link.href = path
  link.click()
}

const getGpsLocation = () => {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject('Geolocation is not supported by this browser.')
      return
    }
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const coords = [position.coords.latitude, position.coords.longitude]
        resolve(coords)
      },
      (error) => {
        reject(error.message)
      }
    )
  })
}

onMounted(() => {
  init()

  setTimeout(() => {
    typeWriter('UKK', line1, 100)
    setTimeout(() => {
      typeWriter('Rental Alat Photo Planning', line2, 100)
    }, 1050)
  }, 750)
})

</script>

<style scoped>
.typewriter {
  white-space: pre-line;
  animation: blink 0.7s infinite;
}

@keyframes blink {
  0%,
  100% {
    border-color: transparent;
  }
  50% {
    border-color: #00ffcc;
  }
}

.content {
  flex: 1;
  display: flex;
  overflow: auto;
}

.box {
  display: flex;
  min-height: min-content;
}

.card-active:hover {
  transition: 0.3s ease;
  transform: scale(1.02);
}

.card-active #card-img {
  height: 300px !important;
}

body.ts .bg-amber {
  background-color: #e23b3b !important;
}

.my-background {
  background-color: #001744;
  background-size: cover; /* Adjust as needed: cover, contain, auto, etc. */
  background-position: center; /* Optional: adjust positioning */
  background-repeat: no-repeat; /* Optional: prevent repeating */
  height: 95vh;
}

.q-card.my-card {
  background-color: rgba(255, 255, 255, 0.1); /* Semi-transparent white background */
  border: 1px solid rgba(255, 255, 255, 0.3); /* Semi-transparent border */
  backdrop-filter: blur(10px); /* Blur effect for content behind the card */
  -webkit-backdrop-filter: blur(10px); /* For Safari compatibility */
  color: white;
}

@media screen and (max-width: 800px) {
  .mobile-card {
    margin-top: 20px !important;
  }
}
</style>
