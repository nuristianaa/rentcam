<template>
    <div>
        <s-loading v-if="loading" />
        <q-form v-else @submit.prevent="submit">
            <header-form :meta="Meta" type="form" @back="back" :disable-submit="disableSubmit">
                <div class="row q-pa-sm">
                    <f-card :title="Meta.name" row>
                        <f-input col="6" label="Name" v-model="dataModel.name" required/>
                        <f-input col="6" label="Slug" v-model="dataModel.slug" required/>
                    </f-card>
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
    }
  },

  created () {
    this.dataModel = this.$Helper.unReactive(this.Meta.model)
    
    const action = this.$Handler.formMode(this)
    this.$Handler.permissions(this, action.mode, Meta, (status, data) => {
      this.Meta.permission = data
      if (status) {
        if (action.mode === 'update' && action.params.id !== undefined) this.getData(action.params.id)
        else this.loading = false;
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
  }
}
</script>
