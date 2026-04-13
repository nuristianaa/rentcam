<template >
    <div>
      <s-drawer @refresh-event="onRefresh"/>
  
      <s-loading v-if="loading" />
      <header-form v-else :meta="Meta" type="detail" @back="back" :model="dataModel" >
        <div class="row q-pa-sm">
  
        <f-card title="Detail" col="6">
          <s-list v-for="(value, index) in viewList" :key="index" :data="value" />
        </f-card>
  
        <f-card title="Log Info" col="6">
          <log-info :data="dataModel" />
        </f-card>
      </div>
  
      </header-form>
    </div>
  </template>
  
  <script>
  import Meta from './meta'
  export default {
    name: Meta.page.view,
    data () {
      return {
        Meta,
        API: this.$Api,
        dataModel: Meta.model,
        viewList: null,
        loading: true,
      }
    },
  
    mounted () {
      this.$Handler.permissions(this, 'read', Meta, (status, data) => {
        this.Meta.permission = data 
        const id = this.$route.params.id
        if (id) this.getData(id)
        else this.loading = false
      })
    },
  
    methods: {
      onRefresh () {
        //
      },

      getData(id) {
        this.loading = true
        const endpoint = this.Meta.module + '/' + id
        this.API.get(endpoint, (status, data, message, response) => {
          this.loading = false
          if (status === 200) {
            this.dataModel = data
            const {id, role_id, Menus, ...viewlist} = data
            viewlist.role = data.role.name
            viewlist.activated_at = this.$Helper.readDate(data.activated_at, true)
            this.viewList = this.$Handler.viewList(viewlist, this)
          }
        })
      },
  
      back () {
        this.$router.push({ name: this.Meta.route_ui, query: this.$route.query })
      },
  
    }
  }
  </script>
  