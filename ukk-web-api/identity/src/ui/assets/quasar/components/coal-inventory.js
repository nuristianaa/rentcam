
const CoalInventory = {
  template: `
    <div class="col-12 row items-center justify-between q-pa-sm ">
      <table class="bordered-light">
        <tr v-for="row in rows" :key="'row-' + row">
          <template v-for="col in cols" :key="'col-' + col">
            <template v-if="!isCellCovered(row, col)">
              <td
                :rowspan="getCellItem(row, col, 'row_to') - getCellItem(row, col, 'row_from') + 1"
                :colspan="getCellItem(row, col, 'col_to') - getCellItem(row, col, 'col_from') + 1"
              >
                <div class="row items-center justify-between no-wrap q-pa-xs">
                  <div class="q-py-sm q-mx-xs q-px-sm" :style="styleCard(getCellItem(row, col, 'type'))">

                    <!-- Title -->
                    <div v-if="['exposed', 'stock'].includes(getCellItem(row, col, 'type'))"
                        class="title text-h3 text-center q-pa-sm text-weight-bold">

                      <slot name="title-top" :weatherAdm="getCellItem(row, col, 'weather_adm')" ></slot>

                      {{ getCellItem(row, col, 'title') }}
                    </div>

                    <!-- Images -->
                    <div class="flex justify-center">
                      <img v-if="['exposed'].includes(getCellItem(row, col, 'type'))" :src="getCellItem(row, col, 'image') || getImg('pit')" width="170" />
                      <img v-else-if="['stock'].includes(getCellItem(row, col, 'type'))" :src="getCellItem(row, col, 'image') || getImg('stock')" width="170" />
                      <img v-else-if="['otr'].includes(getCellItem(row, col, 'type'))" :src="getCellItem(row, col, 'image') || getImg('truck')" width="120" />
                    </div>

                    <!-- Dashed line for OTR -->
                    <div class="flex justify-center">
                      <div v-if="['otr'].includes(getCellItem(row, col, 'type'))" class="dashed-line"></div>
                    </div>

                    <!-- Value -->
                    <div class="flex justify-center q-mt-sm text-h4" v-if="['otr'].includes(getCellItem(row, col, 'type'))">
                      <span>{{ formatNumber(getCellItem(row, col, 'value')) }}</span>
                    </div>

                    <!-- Subtitle -->
                    <div class="flex justify-center q-mt-sm text-h4 text-uppercase" v-if="['otr'].includes(getCellItem(row, col, 'type'))">
                      <span>({{ getCellItem(row, col, 'subtitle') }})</span>
                    </div>

                    <div v-if="getCellItem(row, col, 'type') != 'otr'" class="flex justify-center q-mt-sm">
                      <div v-if="['exposed'].includes(getCellItem(row, col, 'type'))" >
                        <table style="border-collapse: collapse; width: 100%;">
                          <tbody>
                            <tr v-for="(d, i) in getCellItem(row, col, 'detail')" :key="'detail-' + i" class="text-h4">

                              <td class="text-right">{{ formatNumber(d.total, 3) }}</td>
                              <td class="text-left">
                                ({{ d.label }}{{ d.date ? ', ' + new Date(d.date).toLocaleDateString('id-ID', { day: '2-digit', month: 'short', year: 'numeric' }) : '' }})
                              </td>
                            </tr>
                            <tr>
                              <td class="text-right text-h4">{{ formatNumber(getCellItem(row, col, 'value'), 3) }}</td>
                              <td class="text-left text-h4">(Total {{ getCellItem(row, col, 'subtitle') }})</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                      <div v-else>
                        <table style="border-collapse: collapse; width: 100%;">
                          <tbody>
                            <tr v-for="(d, i) in getCellItem(row, col, 'detail')" :key="'detail-' + i">
                              <td class="text-right text-h4" style="min-width:75%">{{ formatNumber(d.total, 3) }}</td>
                              <td class="text-left text-h4" style="min-width:25%">({{ d.label }})</td>
                            </tr>
                            <tr>
                              <td class="text-right text-h4" style="min-width:75%">{{ formatNumber(getCellItem(row, col, 'value'), 3) }}</td>
                              <td class="text-left text-h4" style="min-width:25%">(STOCK)</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>

                  </div>
                </div>
              </td>
            </template>
          </template>
        </tr>
      </table>
    </div>
  `,
  props: {
    rows: { type: Array, required: true },
    cols: { type: Array, required: true },
    result: { type: Array, required: true }, // seperti example.result
    mainPath: { type: String, required: true }, // seperti example.result
  },
  data() {
    return {
      img: { // combine with mainPath
        pit: '/ui/images/pit.png',
        coal: '/ui/images/coal.png',
        truck: '/ui/images/truck.png',
        port: '/ui/images/port.png',
      }
      
      //
      }
  },
  methods: {
    getImg(type) {
      const path = this.mainPath
      let res = null
      if (this.img[type] && path) res = `${path}${this.img[type]}`
      return res
    },
    getCellItem(row, col, field = null) {
      const data = this.result.find(item => row === item.row_from && col === item.col_from)
      if (field && data) return data[field]
      return data
    },
    isCellCovered(row, col) {
      return this.result.some((item) =>
        row >= (item.row_from ?? 0) &&
        row <= (item.row_to ?? 0) &&
        col >= (item.col_from ?? 0) &&
        col <= (item.col_to ?? 0) &&
        !(row === item.row_from && col === item.col_from)
      )
    },
    styleCard(type) {
      if (!type) return 'display: none;'
      let color = '#ffff'
      if (type === 'pit') color = '#f77272'
      if (type === 'inventory') color = '#545454'
      if (type === 'barging') color = '#2196f3'
      return `width:100%; `
    },
    formatNumber(val, precision = 2) {
      if (val == null || isNaN(val)) return '-'
      return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: precision,
        maximumFractionDigits: precision,
      }).format(val)
    }
  }
}
