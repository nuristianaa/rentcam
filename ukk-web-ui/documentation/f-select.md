## Example
<f-select v-model="dataModel.select1" :options="['satu', 'dua']" />
{{ dataModel.select1 }} | satu
<f-select v-model="dataModel.select2" :options="[{id: 1, name: 'satu'}, {id: 2, name: 'dua'}]" />
{{ dataModel.select2 }} | 1

<f-select v-model="dataModel.select3" api="auth/users?where=role_code:admin" mustfill />
{{ dataModel.select3 }} | 2
<f-select v-model="dataModel.select3" api="master/trucks" app="fms" optionValue="code" :optionLabel="v => v.code + ' ' + v.name" />
{{ dataModel.select3 }} | CK_001

<f-select v-model="dataModel.select4" :options="[{id: 1, name: 'satu'}, {id: 2, name: 'dua'}], {id: 3, name: 'tiga'}]" raw multiple/>
{{ dataModel.select4 }} | [{id: 1, name: 'satu'}, {id: 2, name: 'dua'}]

## PROPS
  options      -> list option
  optionValue  -> primary key / value dari option yg dipilih
  optionLabel  -> label option
  multiple     -> flag multiple
  raw          -> return data raw (semua field masuk)
  mustFill     -> clearable false
  api          -> url get api (di component sudah include limit=0)
  app          -> app api

## EMITS
  - updateEvent -> trigger saat update data
