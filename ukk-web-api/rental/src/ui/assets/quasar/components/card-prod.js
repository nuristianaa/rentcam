// 1️⃣ Inject CSS ke <head>
(function(){
  const style = `
  .card-prod_icon {
    padding: 20px 20px 0 15px; 
    color: #fff;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    text-align: center;
    font-weight: bold;
    font-size: 15px;
  }
  .card-prod_detail {
    width: 100%;
    font-weight: bold;
  }
  .card-prod_detail tr td {
    text-align: right;
    vertical-align: middle;
  }
  .text-val {
    font-size:12.5pt;
  }
  .value-area {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 80px; /* sesuaikan lebar */
  }
`;
  const styleEl = document.createElement('style');
  styleEl.textContent = style;
  document.head.appendChild(styleEl);
})();

// 2️⃣ Definisi komponen Vue
const CardProd = {
  template: `
    <div>
      <q-card class="row card-prod q-pa-sm">
        <div class="col-4 q-pa-xs">
          <div class="card-prod_icon" :class="iconClass">
            <template v-if="$slots.icon">
              <slot name="icon"></slot>
            </template>
            <template v-else> {{ iconText }} </template>
          </div>
        </div>
        <div class="col-8">
         <template v-if="$slots.content">
            <slot name="content"></slot>
          </template>
        <table v-else class="card-prod_detail">
          <tbody >
            <tr>
              <td>
                <q-badge color="grey-4" class="text-grey-8 text-bold" style="font-size: 10px;">
                  {{ badge }}
                </q-badge>
              </td>
            </tr>
            <tr>
              <td class="value-area">
                <span class="text-grey-8 q-pr-sm">{{planLabel}}</span>
                <span class="text-val text-bold">{{ plan }}</span>
              </td>
            </tr>
            <tr v-if="!hideActual">
              <td class="value-area">
                <span class="text-grey-8 q-pr-sm">{{actualLabel}}</span>
                <span class="text-val text-bold">{{ actual }}</span>
              </td>
            </tr>
            <tr v-if="!hideOther">
              <td class="value-area">
                <span class="text-grey-8 q-pr-sm">{{otherLabel}}</span>
                <span class="text-val text-bold">{{ other }}</span>
              </td>
            </tr>
          </tbody>
        </table>
        </div>
      </q-card>
    </div>
  `,
  props: {
    iconText: { type: String, default: 'YTD' },
    iconClass: { type: String, default: 'bg-blue-9' },
    badge: { type: String, default: 'TRA' },
    planLabel: { type: String, default: 'PLAN' },
    actualLabel: { type: String, default: 'ACTUAL' },
    otherLabel: { type: String, default: 'OTHER' },
    plan: { type: [String, Number], default: 0 },
    actual: { type: [String, Number], default: 0 },
    other: { type: [String, Number], default: 0 },
    hideActual: { type: Boolean, default: false },
    hideOther: { type: Boolean, default: false }
  }
}
