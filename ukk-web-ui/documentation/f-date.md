## Example
<f-date yearMonth v-model="dataModel.dateym" label="date ym" />
{{ dataModel.dateYm }} | 2024-01-01
<f-date range v-model="dataModel.range" label="date range" />
{{ dataModel.range }} | 2024-01-01 to  | 2024-12-31
<f-date dateTime v-model="dataModel.dateTime" label="date dateTime" />
{{ dataModel.dateTime }} | 2024-01-01 23:59:59
<f-date dateTime millis v-model="dataModel.millis" label="date millis" />
{{ dataModel.millis }} | 1723400636987

## PROPS
  - dateTime  -> bool, format datetime | YYYY-MM-DD HH:ii:ss
  - time      -> bool, format time | HH:ii
  - range     -> bool, format range date | YYYY-MM-DD to YYYY-MM-DD
  - millis    -> bool, format datetime atau range date menjadi millis |
                  > YYYY-MM-DD HH:ii:ss -> timemillis(int)
                  > YYYY-MM-DD to YYYY-MM-DD -> timemillis to timemillis
  - yearMonth -> bool, MMMM YYYY -> YYYY-MM-DD
  - noRules   -> bool, force tanpa rules

## EMITS
  - updateEvent -> trigger saat update data
  - updateRange -> trigger saat update data range, value = {from: '', to: ''}
