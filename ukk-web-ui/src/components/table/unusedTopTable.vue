<template>Unused</template>
<!-- <template>
  <div v-if="meta" style="width: 100%;">
    <div class="row justify-end q-mt-sm">
      <div class="column">
        <div class="title">{{ meta.title }}</div>
        <div v-if="meta.tabs" class="q-gutter-x-md column items-start">
          <q-btn-dropdown v-if="$q.screen.lt.sm" flat dense size="10px" color="info" :label="meta.tab">
            <q-btn v-for="v in meta.tabs" :key="v.name" :label="v.label" :icon="v.icon"
              flat dense size="10px" class="row"
              :color="meta.tab == v.name ? 'positive' : 'grey'"
              @click="$emit('updateTab', v.name)"
            />
          </q-btn-dropdown>
          <q-btn-group v-else flat>
            <q-btn v-for="v in meta.tabs" :key="v.name" :label="v.label" :icon="v.icon"
              flat dense size="11px" class="q-pr-sm"
              :color="meta.tab == v.name ? 'positive' : 'grey'"
              @click="$emit('updateTab', v.name)"
            />
          </q-btn-group>
        </div>
      </div>
      <slot />

      <q-space />

      <div class="q-gutter-sm q-pb-sm">
        <q-btn v-if="meta.permission.delete && datatable.selected.length !== 0"
          :color="trash ? 'green' : 'negative'"
          :icon="trash ? 'refresh' : 'delete'"
          :label="trash ? 'Re-Activate' : 'Delete'"
          @click="deleteSelected"
        />
        <q-btn v-if="!trash && meta.permission.create && !meta.hide_add"
          color="primary" icon="add" :label="meta.label_add ?? 'Add'" @click="$emit('addEvent')"
        />
        <slot name="buttons" />
        <q-btn @click="onRefresh(false)" dense flat size="sm" color="primary" icon="refresh" >
          <q-tooltip>Refresh</q-tooltip>
        </q-btn>
        <q-chip @click="onRefresh(true)" dense clickable size="sm" color="deep-orange" text-color="white" icon-right="restart_alt" style="margin-top: 12px;">
          Reset filter
        </q-chip>
        <q-btn dense flat color="primary" icon="archive" @click="exportTable">
          <q-tooltip>Export to CSV or XlS</q-tooltip>
        </q-btn>
        <q-btn dense flat color="primary" icon="settings" @click="modal.show = !modal.show">
          <q-tooltip>Advance Settings</q-tooltip>
        </q-btn>
        <q-btn v-if="meta.permission.restore && !trash && !meta.hide_trash"
          dense flat color="negative" icon="recycling" @click="updateTrash(true)"
        >
          <q-tooltip>Trash</q-tooltip>
        </q-btn>
        <q-btn v-if="trash" dense flat color="grey-6" icon="chevron_left" @click="updateTrash(false)">
          <q-tooltip>Back</q-tooltip>
        </q-btn>
      </div>
    </div>

    <q-drawer v-model="modal.show" bordered side="right" :width="300" class="">
      <div class="row justify-between q-pa-md">
        <div class="text-bold">Settings</div>
        <div>
          <q-btn dense flat no-caps color="negative" icon="cancel" size="sm" @click="modal.show = false" />
          <q-btn dense flat no-caps color="positive" icon-right="save" label="Apply" size="sm" @click="saveTemplate()" />
        </div>
      </div>

      <div class="row q-pa-sm q-gutter-sm">
        <q-btn label="Default" dense outline no-caps color="info" icon="refresh" size="sm" @click="resetTemplate()" />
        <q-btn-group  v-for="v,i in templates" :key="i" size="xs">
          <q-btn dense  size="xs" :color="v.apply ? 'primary' : 'grey-3'" :text-color="v.apply ? 'white' : 'dark'" icon="check" @click="chooseTemplate(v,i)"/>
          <q-btn dense no-caps class="q-px-sm"  size="sm" :color="v.apply ? 'primary' : 'grey-3'" :text-color="v.apply ? 'white' : 'dark'" :label="v.name">
            <q-popup-edit v-model="v.name" auto-save v-slot="scope">
              <q-input class="form-xs" v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
            </q-popup-edit>
          </q-btn>
          <q-btn no-caps dense  size="xs" :color="v.apply ? 'primary' : 'grey-3'" :text-color="v.apply ? 'white' : 'dark'" icon="delete" @click="deleteTemplate(i)"/>
        </q-btn-group>
        <q-btn label="Save as new" dense outline no-caps color="info" icon="add" size="sm" @click="addTemplate(cols.applied)" />
      </div>
      <q-separator />
      <q-linear-progress v-if="loading" />
      <q-scroll-area v-else visible :style="'width: 100%; height: ' + ($q.screen.height - 220) + 'px;'">
        <VueDraggable class="" tag="div" :list="cols.applied" :group="{ name: 'g1' }" item-key="name" >
          <template #item="{ element }">
            <q-list bordered separator dense>
              <q-item v-if="element" clickable v-ripple>
                <q-toggle size="sm" dense v-model="element.show" color="green" class="q-mr-sm" />
                <q-item-section>{{ element?.label ?? element?.name }} </q-item-section>
                <q-item-section side><q-icon size="sm" name="swap_vertical_circle" /></q-item-section>
              </q-item>
            </q-list>
          </template>
        </VueDraggable>
      </q-scroll-area>
    </q-drawer>
  </div>
</template>

<script>
import { exportFile } from 'quasar'
import VueDraggable from 'vuedraggable';
import * as XLSX from 'xlsx'

function wrapCsvValue(val, formatFn) {
  let formatted = formatFn !== void 0 ? formatFn(val) : val;
  formatted = formatted === void 0 || formatted === null ? '' : String(formatted);
  formatted = formatted
    .split('"')
    .join('""')
    .split('\n')
    .join('\\n')
    .split('\r')
    .join('\\r');
  /**
   * Excel accepts \n and \r in strings, but some other CSV parsers do not
   * Uncomment the next two lines to escape new lines
   */
  return `"${formatted}"`;
}

export default {
  name: 'TopTable',
  components: { VueDraggable },
  props: [
    'meta',
    'modelValue',
    'trash',
    'tableConfigs'
  ],
  emits: [
    'updateTab',
    'update:modelValue',
    'update:trash',
    'update:meta',
    'refreshEvent',
    'addEvent',
  ],
  data() {
    return {
      API: this.$Api,
      datatable: this.modelValue,
      loading: false,
      modal: {
        show: false,
      },
      csvdelimiter: ';',
      templates: [],
      cols: {
        all: [],
        applied: []
      }
    };
  },

  created() {
    this.init()
  },

  watch: {
    tableConfigs() { this.init() },
    modelValue() { this.datatable = this.modelValue }
  },

  methods: {
    init() {
      this.cols.all = []
      this.cols.applied = []
      for (let i = 0; i < this.modelValue.columns.length; i++) {
        const el = this.modelValue.columns[i]
        const row = {show: true, name: el.name, label: el.label}
        if (el.colHide) row.show = false
        this.cols.all.push(row)
        this.cols.applied.push(row)
      }

      const configs = this.tableConfigs
      if (configs && configs.length > 0) {
        for (let i = 0; i < configs.length; i++) {
          const e = configs[i]
          if (e.app == this.meta.app && e.module == this.meta.module) {
            this.templates = e.templates ?? []
            for (let ii = 0; ii < this.templates.length; ii++) {
              const el = this.templates[ii]
              if (el.apply) this.chooseTemplate(el, ii)
            }
          }
        }
      }
    },
    onRefresh(reset = false) {
      if (reset) {
        const config = this.datatable?.config
        this.datatable.search = null
        if (config) {
          this.datatable.pagination.sortBy = config.sortBy
          this.datatable.pagination.descending = !config.ascending
        } else {
          this.datatable.pagination.sortBy = 'id'
          this.datatable.pagination.descending = true
        }
      }
      this.$emit('update:modelValue', this.datatable)
      this.$emit('refreshEvent')
    },
    updateTrash(val) {
      this.$emit('update:trash', val)
      this.onRefresh(true)
    },
    resetTemplate() {
      this.cols.applied = []
      this.templates = this.templates.map(p => { return {...p, apply: false}})
      for (let i = 0; i < this.cols.all.length; i++) {
        const col = this.cols.all[i]
        col.show = true
        this.cols.applied.push(col)
      }
    },
    addTemplate(cols) {
      const list = []
      for (let i = 0; i < cols.length; i++) {
        const e = cols[i]
        if (e.show) list.push(e.name)
      }
      const template = {apply: true, name: 'new', value: list}
      const i = this.templates.length
      this.templates.push(template)
      this.chooseTemplate(template, i)
    },
    deleteTemplate(i) {
      this.templates.splice(i, 1)
    },
    chooseTemplate(template, i) {
      // this.loading = true
      this.templates = this.templates.map(p => { return {...p, apply: false}})
      this.templates[i].apply = true
      const choosen = template.value
      const cols = []
      if (choosen && choosen.length > -1) {
        for (let i = 0; i < choosen.length; i++) {
          const c = choosen[i];
          const col = this.cols.all.find((e) => e?.name == c)
          if (col) {
            col.show = true
            cols.push(col)
          }
        }
      }
      const others = this.cols.all.filter(e => !choosen.includes(e.name));
      for (let i = 0; i < others.length; i++) {
        const col = others[i]
        col.show = false
        cols.push(col)
      }
      this.cols.applied = cols
      // setTimeout(() => {this.loading = false}, 300)
    },
    saveTemplate() {
      this.loading = true
      const meta = this.meta
      const update = []
      for (let i = 0; i < this.cols.applied.length; i++) {
        const e = this.cols.applied[i]
        if (e.show) update.push(e.name)
      }
      const templates = this.templates.map(e => {
        if (e.apply == true) {
          return { ...e, value: update }
        }
        return e
      })
      // const configs = this.tableConfigs
      let insert = true
      // const findcfg = this.tableConfigs.find((e) => e.app == meta.app && e.module == meta.module)
      const configs = this.tableConfigs.map(e => {
        if (e.app == meta.app && e.module == meta.module) {
          insert = false
          return { ...e, templates: templates }
        }
        return e
      })
      // if (findcfg) {
      // }
      if (insert) configs.push({app: meta.app, module: meta.module, templates: templates})
      // if (configs && configs.length > 0) {
      //   for (let i = 0; i < configs.length; i++) {
      //     const e = configs[i]
      //     if (e.app == this.meta.app && e.module == this.meta.module) {
      //       e.templates = this.templates
      //       saves.push(e)
      //     }
      //   }
      // }
      this.API.put('me/update', {table_configs: configs}, (status, data) => {
        if (status === 200) {
          this.$SAuth.setUser(data)
          setTimeout(() => {window.location.reload()}, 300)
        }
      }, 'user')
    },

    // Export Table
    exportTable() {
      this.$q.dialog({
        title: 'Please select format that you want',
        options: {
          type: 'radio',
          items: [
            { label: 'Csv', value: 'csv'  },
            { label: 'Excel', value: 'xls'  }
          ]
        },
        cancel: true,
        ok: {
          label: 'Execute'
        }
      }).onOk(data => {
        if(data === 'csv') this.exportCsv()
        else if(data === 'xls') this.exportExcel()
      })
    },
    exportExcel() {
      const tempArr = []
      this.modelValue.data.forEach((x, xIndex) => {
        const tempData = {}
        this.modelValue.columns.forEach((y) => {
          const label = y.label
          const field = typeof y.field === 'function' ? y.name : y.field
          tempData[label] = this.modelValue.data[xIndex][field]
          if (typeof tempData[label] === 'object') tempData[label] = JSON.stringify(tempData[label])
          if (typeof y.field === 'function') tempData[label] = y.field(x)
          if (Array.isArray(tempData[label])) tempData[label] = JSON.stringify(tempData[label])
          if (y.formatter) {
            const val = this.modelValue.data[xIndex][field]
            if (y.formatter == 'float') tempData[label] = val ? parseFloat(val) : 0
            else if (y.formatter == 'integer') tempData[label] = val ? parseInt(val) : 0
            else if (y.formatter == 'date') tempData[label] = this.$Helper.toDate(val, 'YYYY-MM-DD')
            else if (y.formatter == 'time') tempData[label] = this.$Helper.toDate(val, 'HH:mm:ss')
            else if (y.formatter == 'datetime') tempData[label] = this.$Helper.toDate(val, 'YYYY-MM-DD HH:mm:ss')
            else if (y.formatter == 'millis') tempData[label] = this.$Helper.toDate(val, 'YYYY-MM-DD HH:mm:ss')
          }
        })
        tempArr.push(tempData)
      })
      // console.log(tempArr)
      // console.log(this.modelValue.columns)
      // console.log(this.modelValue.data)
      const data = XLSX.utils.json_to_sheet(tempArr)
      const wb = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(wb, data, 'data')
      XLSX.writeFile(wb, `${this.meta.name}-table-export.xlsx`)
    },
    exportCsv() {
      const delimiter = this.csvdelimiter;
      const content = [
        this.modelValue.columns
          .map((col) => wrapCsvValue(col.label))
          .join(delimiter),
      ]
        .concat(
          this.modelValue.data.map(
            (row) =>
              this.modelValue.columns
                .map((col) =>
                wrapCsvValue(
                    typeof col.field === 'function'
                      ? col.field(row)
                      : row[col.field === void 0 ? col.name : col.field],
                    col.format
                  )
                )
                .join(delimiter) // delimiter
          )
        )
        .join('\r\n');
      const status = exportFile(
        this.meta.name + '-table-export.csv',
        content,
        'text/csv'
      );
      if (status !== true) {
        this.$q.notify({
          message: 'Browser denied file download...',
          color: 'negative',
          icon: 'warning',
        });
      }
    },

    // Delete or Restore Selected Data
    deleteSelected() {
      const type = !this.trash ? 'delete' : 'restore';
      this.$q.dialog({
        title: `${type} ${this.datatable.selected.length} data selected`,
        message:
          'Are you sure want to ' + type + ' data ' + this.meta.name + ' ?',
        persistent: true,
        ok: type,
        cancel: 'Cancel',
      })
      .onOk(() => {
        this.deleteDataSelected(type)
      })
      .onCancel(() => {
        // action
      })
      .onDismiss(() => {
        // action
      })
    },
    async deleteDataSelected(type) {
      const app = this.meta?.app ?? ''
      this.$Helper.loadingOverlay()
      const ids = []
      for (const row of this.datatable.selected) {
        ids.push(row.id)
      }
      if (this.meta.laravel) {
        for (let i = 0; i < ids.length; i++) {
          const id = ids[i];
          let ep = ''
          if (type === 'delete') {
            ep = `${this.meta.module}/${id}`
            await this.$Api.delete(ep, {}, (status, data, message) => {
              this.$Helper.showToast(message);
            }, app)
          }
          else {
            ep = `${this.meta.module}/${id}/restore`
            await this.$Api.put(ep, {}, (status, data, message) => {
              this.$Helper.showToast(message);
            }, app)
          }
        }
      } else {
        let ep = ''
        if (type === 'delete') ep = `${this.meta.module}/delete`
        else ep = `${this.meta.module}/restore`
        const request = {
          id: ids
        }
        await this.$Api.delete(ep, request, (status, data, message) => {
          this.$Helper.showToast(message);
        }, app)
      }
      this.datatable.selected = []
      this.$Helper.loadingOverlay(false)
      this.onRefresh()
    }
  }
}
</script> -->
