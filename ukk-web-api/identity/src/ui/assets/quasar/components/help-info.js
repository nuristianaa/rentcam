

const HelpInfo = {
  template: `
  <q-icon name="help_outline" size="16px" class="q-ml-sm cursor-pointer">
    <q-popup-proxy>
      <q-banner class="bg-grey-2 text-dark q-pa-sm" style="max-width: 350px">
        <div class="text-body2">
          <slot></slot>
        </div>
      </q-banner>
    </q-popup-proxy>
  </q-icon>
  `,
  props: {
    label: "color",
  },
  data() {
    return {
      model: null
    }
  },
  computed: {
    //
  },
  methods: {
  },
  mounted() {

  },
}
