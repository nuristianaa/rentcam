<template>
  <div>
    <s-loading v-if="loading" />
    <h-form v-else @submit="submit" :meta="Meta" :modal="dataModel" @back="back">
      <div class="row">
        <div class="col-12 q-pa-sm">
          <div class="form-title">General Info</div>
        </div>
        <f-input col="6" v-model="dataModel.name" :label="Lang.module(Meta, 'Name')" required />
        <f-input col="6" v-model="dataModel.username" :label="Lang.module(Meta, 'Username')" required />
        <f-input col="6" v-model="dataModel.email" :label="Lang.module(Meta, 'Email')" required />
        <f-input col="6" v-model="dataModel.phone" label="Mobile Phone" inputClass="text-right" />
        <f-input col="6" v-model="dataModel.title" :label="Lang.module(Meta, 'Title')" />

        <template v-if="dataModel.user_type != 'contact'">
          <div class="col-12 q-pa-sm">
            <div class="form-title">Other Info</div>
          </div>
          <f-select col="6" v-model="dataModel.role_ids" label="Role" api="auth/roles" must-fill multiple />

          <f-select col="6" v-model="dataModel.menu_id" label="Menu" api="auth/master-menus" />
          <f-select col="6" v-model="dataModel.additional_permissions" :label="Lang.module(Meta, 'Additional Permissions')" multiple api="auth/users?const_list=additional_permissions" option-value="code" :option-label="(o: any) => (o ? o?.label : o)" />
          <f-toggle col="4" v-model="dataModel.is_active" :label="Lang.module(Meta, 'Status')" active-mode />
        </template>
      </div>
    </h-form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Api from 'src/services/api'
import { Handler } from 'src/services/handler'
import { Helper } from 'src/services/helper'
import { Lang } from 'src/services/lang'
import type { DataModel, Company } from './meta'
import { Meta } from './meta'

const props = defineProps<{ props?: { id?: string | number } }>()
const emit = defineEmits(['refreshEvent'])

const router = useRouter()
const API = new Api()

const loading = ref(true)
const dataModel = ref<DataModel>(Meta.model)
const avatar = ref<any>(null)

const opt = ref<any>({
  companies: [],
  vendors: [],
  user_type: []
})

// METHODS
const init = () => {
  dataModel.value = Helper.unreactive(Meta.model)
  if ((Meta as any).tab != 'all') dataModel.value.user_type = (Meta as any).tab

  const action = props.props?.id ? 'update' : 'create'
  Handler.permissions(router, action, Meta, (status: boolean, data: any) => {
    Meta.permission = data
    if (status) {
      if (props.props?.id) getData(props.props?.id)
      else onRefresh()
    }
  })
}

const onRefresh = () => {
  loading.value = false
}

const getData = (id: string | number) => {
  loading.value = true
  const endpoint = `${Meta.module}/${id}`
  API.get(endpoint, (status: number, data: any) => {
    loading.value = false
    if (status === 200) {
      if (data.additional_permissions) data.additional_permissions = data.additional_permissions.split(',')
      if (data.roles) data.role_ids = data.roles.map((role: any) => role.id)
      dataModel.value = data
    }
  })
}

function mail2username(mail: any) {
  if (typeof mail !== 'string') return ''

  const atIndex = mail.indexOf('@')
  if (atIndex === -1) {
    return mail // tidak ada '@', return semua
  }
  return mail.substring(0, atIndex)
}

const submit = async () => {
  if (validateSubmit()) {
    loading.value = true

    let status = 600
    // Handle File
    if (dataModel.value.id) status = await update()
    else status = await save()
    if (avatar.value) status = await uploadAvatar(dataModel.value)

    if (status === 200) {
      Helper.showSuccess('Data has been successfully saved.')
      back()
    }
    loading.value = false
  }
}

const validateSubmit = () => {
  dataModel.value.companies = dataModel.value.companies?.toString() || null
  dataModel.value.vendors = dataModel.value.vendors?.toString() || null
  dataModel.value.additional_permissions = dataModel.value.additional_permissions?.toString() || null
  // dataModel.value.notifications = dataModel.value.notifications?.toString() || null
  if (dataModel.value.user_type == 'contact') {
    dataModel.value.username = dataModel.value.email
  }

  let msg = ''

  const d = dataModel.value
  if (!d.name) msg += 'Name is required. '
  if (!d.email) msg += 'Email is required. '
  if (d.email && !d.email.includes('@')) msg += 'Email is not valid. '
  // if (!d.phone) msg += 'Phone is required. '

  if (msg === '') {
    if (!d.username && d.email) {
      d.username = mail2username(d.email)
    }
    return true
  } else {
    Helper.showNotif(msg)
    return false
  }
}

const save = async () => {
  let statusapi = 600
  await API.post(Meta.module, dataModel.value, (status: number, data: any) => {
    statusapi = status
    dataModel.value.id = data.id
  })
  return statusapi
}

const update = async () => {
  let statusapi = 600
  await API.put(`${Meta.module}/${dataModel.value.id}`, dataModel.value, (status: number, _data: any) => {
    statusapi = status
  })
  return statusapi
}

const uploadAvatar = async (data: any) => {
  /* CHECK & UPLOAD AVATAR */
  let statusapi = 200
  if (avatar.value && data.id) {
    const dataModel = new FormData()
    dataModel.append('_method', 'PUT')
    dataModel.append('file', avatar.value)
    await API.post(`${Meta.module}/${data.id}`, dataModel, (status: number, _data: any) => {
      statusapi = status
    })
  }
  return statusapi
}

const back = () => {
  emit('refreshEvent')
}

const onChangeUserType = () => {
  dataModel.value.vendors = null
  dataModel.value.companies = null
}



// MOUNTED | COMPUTED | WATHERS
onMounted(() => {
  init()
})
</script>
