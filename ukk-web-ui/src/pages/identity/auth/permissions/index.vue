<template>
    <div>
        <q-page class="q-pa-md">
            <header-page :Meta="Meta"></header-page>
            <x-table
                :meta="Meta"
                :refresh="refresh"
                :epQuery="custom_query"
                @add="add"
                @edit="edit"
                @detail="detail"
                @selected="selected"
            >
                <template v-slot:body-cell-updated_at="props">
                    <log-info table :data="props.props.row" />
                </template>
            </x-table>
        </q-page>
    </div>
</template>

<script>
import Meta from './meta'
export default{
    name: Meta.page.index,
    data() {
        return {
            Meta,
            refresh: 0,
            API: this.$Api,
            table: null,
            is_trash: false,
            custom_query: '',
            dataModel: null
        }
    },
    created(){
        this.table = this.$Handler.table(
            this.Meta.table(this.$Helper, this.$Constant)
        )
        this.$Handler.permissions(this, 'browse', Meta, (status, data) => {
            this.Meta.permission = data
        })
    },
    methods:{
        add() {
            this.$router.push({ name: 'add' + this.Meta.route_ui })
        },

        edit(data) {
            this.$router.push({
                name: 'edit' + this.Meta.route_ui,
                params: data
            })
        },

        detail(data) {
            this.$router.push({
                name: 'view' + this.Meta.route_ui,
                params: data
            })
        },
    }
}

</script>