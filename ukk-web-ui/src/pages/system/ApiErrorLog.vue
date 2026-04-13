<template>
  <div>
    <s-loading v-if="loading" />
    <q-table v-else flat dense bordered :rows="logs" :columns="columns" title="Error Logs" :rows-per-page-options="[25, 100, 0]" v-model:pagination="pagination">
      <template v-slot:body-cell-actions="props">
        <q-td>
          <div class="row q-gutter-sm">
            <q-btn icon="visibility" color="secondary" round dense @click="viewLog(props.row.app, props.row.name)" />
          </div>
        </q-td>
      </template>
    </q-table>
    <q-dialog v-model="showDialog" maximized>
      <q-card style="height: 100%; width: 100%">
        <q-bar>
          <div class="text-subtitle1">{{ selectedLog }}</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup />
        </q-bar>

        <q-card-section class="log-viewer" style="overflow-y: auto; height: calc(100% - 40px)">
          <pre v-html="logContent"></pre>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Api from 'src/services/api'

const API = new Api()
const loading = ref(true)
const logs = ref<{ app: string; name: string }[]>([])
const selectedLog = ref<string | null>(null)
const logContent = ref<string>('')
const showDialog = ref(false)

const columns: any = [
  { sortable: true, name: 'app', label: 'App', field: 'app', align: 'left' },
  { sortable: true, name: 'name', label: 'Log File', field: 'name', align: 'left' },
  { sortable: true, name: 'actions', label: 'Actions', field: 'actions', align: 'center' }
]

const pagination = ref({
  sortBy: 'name',
  descending: true,
  page: 1,
  rowsPerPage: 25
})

const fetchLogs = async () => {
  loading.value = true
  const apps = ['identity', 'crm', 'engineering', 'finance', 'hris', 'procurement', 'project_management']
  for (let i = 0; i < apps.length; i++) {
    const app = apps[i]
    if (app) {
      await API.get(
        'api-error-logs',
        (status: number, data: any) => {
          if (status === 200 && data) {
            data.forEach((el: string) => {
              logs.value.push({ app: app, name: el })
            })
          }
        },
        app
      )
    }
  }
  loading.value = false
}

const viewLog = async (app: string, filename: string) => {
  await API.get(
    `api-error-logs/${filename}`,
    (status: number, data: any) => {
      if (status === 200) {
        selectedLog.value = `${app} | ${filename}`
        logContent.value = data.replace(/ERROR/g, '<span class="error">ERROR</span>').replace(/WARN/g, '<span class="warn">WARN</span>').replace(/INFO/g, '<span class="info">INFO</span>')
        showDialog.value = true
      }
    },
    app
  )
}

// const downloadLog = async (app: string, filename: string) => {
//   try {
//     let apidata: any = null
//     await API.get(`api-error-logs/${filename}`, (status: number, _data: any, _message: any, response: any) => {
//       if (status === 200) apidata = response
//     }, app, 'blob')

//     const url = window.URL.createObjectURL(new Blob([apidata.data]))
//     const link = document.createElement('a')
//     link.href = url
//     link.setAttribute('download', filename)
//     document.body.appendChild(link)
//     link.click()
//     link.remove()
//   } catch (err) {
//     console.log(err)
//   }
// }

onMounted(() => {
  void fetchLogs()
})
</script>

<style scoped>
.log-viewer {
  background-color: #1e1e1e; /* dark background */
  color: #d4d4d4; /* light text */
  font-family: 'Fira Code', monospace; /* clean monospace font */
  font-size: 13px;
  line-height: 1.5;
  padding: 12px;
  border-radius: 8px;
  white-space: pre-wrap;
  word-break: break-word;
  overflow-x: auto;
}

/* Optional: highlight error/warning/info lines */
.log-viewer .error {
  background-color: #ff6b6b;
  font-weight: bold;
}
.log-viewer .warn {
  color: #f1c40f;
}
.log-viewer .info {
  color: #4db6ac;
}
</style>
