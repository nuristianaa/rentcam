

const CardWeather = {
  template: `
  <div>
    <div class="widget-weather col-12 q-pa-sm q-mt-md rounded-corner" :style="styleBg">
    
      <div class="col-12 row q-pa-sm">
        <div class="col-3">
          <img v-if="img" :src="img" width="32px" />
        </div>
        <div class="col-9 text-h5 text-bold text-right">
          {{ title }}
        </div>

        <div class="col-12 q-pt-md row">
          <table class="widget-weather_table" :style="styleTable">
            <thead>
              <th :style="styleColor"></th>
              <th :style="styleColor">
                PLAN
                <q-tooltip>{{ data.plan_tooltip }}</q-tooltip>
              </th>
              <th v-if="!hideActual" :style="styleColor">ACTUAL<q-tooltip>{{ data.actual_tooltip }}</q-tooltip></th>
              <th v-if="!hideFreq" :style="styleColor">FREQ<q-tooltip>ACTUAL</q-tooltip></th>
            </thead>
            <tbody>
              <tr v-for="key in keys" :key="key">
                <td class="text-center" :style="styleColor">{{ key.toUpperCase() }}</td>
                <td class="text-center" :style="styleColor">{{ data.plan ? data.plan[key].toFixed(2) : 0 }}</td>
                <td v-if="!hideActual" class="text-center" :style="styleColor">{{ data.actual ? data.actual[key].toFixed(2) : 0 }}</td>
                <td v-if="!hideFreq" class="text-center" :style="styleColor">{{ data.freq ? data.freq[key] : 0 }}</td>
              </tr>
            </tbody>
          </table>
          <slot></slot>
          <div class="text-h5 q-py-sm" v-if="subTitle"> {{ subTitle }} </div>
        </div>
      </div>
    </div>
    </div>
  `,
  props: {
    title: { type: String, required: true },
    subTitle: { type: String | null, default: null },
    img: { type: String, default: null },
    bgColor: { type: String, default: '#D6EFFC' },
    color: { type: String, default: '#000' },
    data: { type: Object, required: true },
    hideActual: { type: Boolean, default: false },
    hideFreq: { type: Boolean, default: false },
  },
  computed: {
    keys() {
      return Object.keys(this.data.plan) // hasil: ["daily","mtd","ytd"]
    },
    styleBg() {
      let res = `background-color: ${this.bgColor}`
      return res
    },
    styleColor() {
      let res = `color: ${this.color}; border-color: ${this.color};`
      return res
    },
    styleTable() {
      let res = `width: 100%; ${this.styleColor};`
      return res
    }
  }
}
