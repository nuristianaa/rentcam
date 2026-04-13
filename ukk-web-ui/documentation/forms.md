## Example
<f-input col="3" v-model="dataModel.value" label="Value" className="text-xs" styles="font-color: red;" placeholder="Please input at least 1 character" readonly :rules="v => customValidation(v)" bottomhints="custom hints" hintcolor="blue" prefix="Rp" />

## PROPS
  - col         -> grid column saat page max width 1-12
  - className   -> custom class
  - styles      -> custom style
  - label       -> label
  - v-model     -> value model
  - placeholder -> placeholder
  - readonly    -> readonly
  - rules       -> rules tambahan
  - required    -> nilai harus diisi
  - bottomhints -> tambahkan text di bawah form
  - hintcolor   -> warna bottomhints
  - prefix      -> tambahkan awalan form
