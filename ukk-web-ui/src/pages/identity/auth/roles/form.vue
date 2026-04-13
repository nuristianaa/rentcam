<template>
    <div>
        <s-loading v-if="loading" />
        <q-form v-else @submit="submit">
          <header-form :meta="Meta" type="form" @back="back" :disable-submit="disableSubmit" >
          <div class="row q-pa-sm">
            <f-card row col="2">
              <div class="q-pa-sm q-mb-md text-h4">Roles</div>
              <f-input v-model="dataModel.name" label="name" required />
              <f-input v-model="dataModel.slug" label="slug" required />
            </f-card>

            <div class="col-12 col-md-10">
              <f-card row>
                <div class="q-pa-sm" style="width:100%;">
                  <q-table flat dense no-border class="no-border" style="width:100%;"
                    :rows="dataModel.permissions"
                    :columns="permission.columns"
                    row-key="name"
                    selection="multiple"
                    v-model:selected="permission.selected"
                    @selection="onSelection"
                    :rows-per-page-options="[0, 10, 20, 50]"
                    :style="'width: 100%; height: ' + ($Constant.tableHeight()-50) + 'px;'"
                  >
                    <template v-slot:top>
                      <q-input v-model="permission.search" label="Search" @keyup="filterTable" outlined dense>
                        <template v-slot:prepend>
                            <q-icon name="search" />
                        </template>
                      </q-input>
                    </template>
                    <template v-slot:header="props">
                      <q-tr :props="props">
                        <q-th>
                          <q-checkbox dense v-model="props.selected" />
                        </q-th>
                        <q-th>Name</q-th>
                        <q-th>Slug</q-th>
                        <q-th>
                          <span>Browse</span>
                          <q-checkbox dense v-model="allSelected.browse" @click="handleAllActions('browse')" />
                        </q-th>
                        <q-th>
                          <span>Read</span>
                          <q-checkbox dense v-model="allSelected.read" @click="handleAllActions('read')" />
                        </q-th>
                        <q-th>
                          <span>Create</span>
                          <q-checkbox dense v-model="allSelected.create" @click="handleAllActions('create')" />
                        </q-th>
                        <q-th>
                          <span>Update</span>
                          <q-checkbox dense v-model="allSelected.update" @click="handleAllActions('update')" />
                        </q-th>
                        <q-th>
                          <span>Delete</span>
                          <q-checkbox dense v-model="allSelected.delete" @click="handleAllActions('delete')" />
                        </q-th>
                        <q-th>
                          <span>Restore</span>
                          <q-checkbox dense v-model="allSelected.restore" @click="handleAllActions('restore')" />
                        </q-th>
                      </q-tr>
                    </template>
                    <template v-slot:body-cell-permissions="props">
                      <q-td :props="props">
                        <q-checkbox dense v-model="props.row.browse" @click="handleCheckPermission(props.row.slug, 'browse')" />
                      </q-td>
                      <q-td :props="props">
                        <q-checkbox dense v-model="props.row.read" @click="handleCheckPermission(props.row.slug, 'read')" />
                      </q-td>
                      <q-td :props="props">
                        <q-checkbox dense v-model="props.row.create" @click="handleCheckPermission(props.row.slug, 'create')" />
                      </q-td>
                      <q-td :props="props">
                        <q-checkbox dense v-model="props.row.update" @click="handleCheckPermission(props.row.slug, 'update')" />
                      </q-td>
                      <q-td :props="props">
                        <q-checkbox dense v-model="props.row.delete" @click="handleCheckPermission(props.row.slug, 'delete')" />
                      </q-td>
                      <q-td :props="props">
                        <q-checkbox dense v-model="props.row.restore" @click="handleCheckPermission(props.row.slug, 'restore')" />
                      </q-td>
                    </template>
                  </q-table>
                </div>
              </f-card>
            </div>
          </div>
          </header-form>

        </q-form>
    </div>
</template>

<script>
import Meta from './meta'

export default {
  name: Meta.page.form,
  data () {
    return {
      Meta,
      API: this.$Api,
      loading: true,
      dataModel: null,
      disableSubmit: false,
      permission: {
        columns: [
          // { name: 'id', required: true, label: 'id', field: 'id', align: 'center', sortable: true },
          { name: 'name', label: 'Name', field: 'name', align: 'center', sortable: true },
          { name: 'slug', label: 'Slug', field: 'slug', align: 'center', sortable: true },
          { name: 'permissions', label: 'Permissions', field: 'current_allow', align: 'center', sortable: true }
        ],
        data: [],
        dataTmp: [],
        selected: [],
        search: null
      },
      allSelected: {
        browse: false,
        read: false,
        create: false,
        update: false,
        delete: false,
        restore: false,
      },
    }
  },

  created () {
    this.dataModel = this.$Helper.unReactive(this.Meta.model)
    
    const action = this.$Handler.formMode(this)
    this.$Handler.permissions(this, action.mode, Meta, (status, data) => {
      this.Meta.permission = data
      if (status) {
        if (action.mode === 'update' && action.params.id !== undefined) this.getData(action.params.id)
        else this.getPermissionsData(); this.loading = false;
      }
    })
    
  },

  methods: {
    onRefresh () {
      //
    },

    getData(id) {
      this.loading = true
      const endpoint = this.Meta.module + '/' + id
        this.API.get(endpoint, (status, data) => {
          this.loading = false
          if (status === 200) {
            this.dataModel = data
            this.dataModel.permissions = data.permissions?data.permissions:[]
            this.getPermissionsData(); 
          }
        })
    },

    getPermissionsData () {
      this.loading = true
      const endpoint = 'auth/permissions'
      endpoint += `?limit=0`
      this.API.get(endpoint, (status, data) => {
        this.loading = false
        if (status === 200) {
          const action = this.$Handler.formMode(this)
          if ((action.mode === 'create' && action.params.id === undefined) || this.dataModel.permissions.length == 0) {
            data.forEach((val) => {
              let permission = {
                ...val,
                browse: false,
                read: false,
                create: false,
                update: false,
                delete: false,
                restore: false,
              }
              if(action.mode === 'update'){
                permission = {
                  ...permission,
                  parent_id: null
                }
              }
              this.dataModel.permissions.push(permission)
              this.permission.dataTmp.push(permission)
            })
          } else {
            for (let i = 0; i < data.length; i++) {
              const val = data[i];
              const permission = this.dataModel.permissions.find((perm) => perm.id == val.id)
              if(!permission) {
                const perm = {
                  ...val,
                  browse: false,
                  read: false,
                  create: false,
                  update: false,
                  delete: false,
                  restore: false,
                  parent_id: null,
                }
                this.dataModel.permissions.push(perm)
                this.permission.dataTmp.push(perm)
              }
            }
          }
        }
      })
    },

    submit () {
      this.dataModel = this.$Handler.clearRequest(this.dataModel)
      if (this.validateSubmit()) {
        this.disableSubmit = true
        if (this.dataModel.id !== null) this.update()
        else this.save()
      }
    },

    validateSubmit () {
      return true
    },

    save () {
      this.$Helper.loadingOverlay(true, 'Saving..')
      this.API.post(this.Meta.module, this.dataModel, (status, data, message) => {
        this.$Helper.loadingOverlay(false)
        if (status === 200) {
          this.$Helper.showSuccess('Save Succesfully', message)
          this.back()
        } else this.disableSubmit = false
      })
    },

    update () {
      this.$Helper.loadingOverlay(true, 'Saving..')
      this.API.put(this.Meta.module + '/' + this.dataModel.id, this.dataModel, (status, data, message) => {
        this.$Helper.loadingOverlay(false)
        if (status === 200) {
          this.$Helper.showSuccess('Update Succesfully', message)
          this.back()
        } else this.disableSubmit = false
      })
    },

    back () {
      console.log('test');
      this.$router.push({ name: this.Meta.route_ui, query: this.$route.query })
    },

    handleAllActions(action) {
      this.dataModel.permissions = this.dataModel.permissions.map((val) => {
        return {
          ...val,
          [action]: this.allSelected[action]
        }
      })
    },

    filterTable() {
      const needle = this.permission.search.toLowerCase()
      const data = this.permission.dataTmp
      const filtered = []
      if(needle !== '') {
        data.forEach(el => {
          if (el.name && el.name.toLowerCase().indexOf(needle) !== -1)
            filtered.push(el)
        })
        const uniqueFiltered = Array.from(new Set(filtered.map(a => a.name)))
          .map(name => {
            return filtered.find(a => a.name === name)
          })
        this.dataModel.permissions = uniqueFiltered
      } else {
        const uniqueData = Array.from(new Set(this.permission.dataTmp.map(a => a.name)))
          .map(name => {
            return this.permission.dataTmp.find(a => a.name === name)
          })
        this.dataModel.permissions = uniqueData
      }
    },

    onSelection ({ rows, added }) {
      if(added) {
        rows[0].browse = true
        rows[0].read = true
        rows[0].create = true
        rows[0].update = true
        rows[0].delete = true
        rows[0].restore = true
      } else {
        rows[0].browse = false
        rows[0].read = false
        rows[0].create = false
        rows[0].update = false
        rows[0].delete = false
        rows[0].restore = false
      }
    }

  }
}
</script>
