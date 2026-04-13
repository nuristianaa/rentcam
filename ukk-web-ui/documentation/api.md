```bash
API.get
  schema/tablename?
    &like=column:null                     -> filter data yang null
    &like=column:notnull                  -> filter data yang not null
    &like=column:value                    -> string contains
    &notlike=column:value                 -> string not contains
    &start=column:value                   -> string contains in start 'val%'
    &end=column:value                     -> string contains in end '%val'
    &where=column:value                   -> exact value
    &isnot=column:value                   -> value is not
    &in_=column:value1,value2             -> in
    &between=column:value1 to value2      -> value between
    &notbetween=column:value1 to value2   -> value not between
    &gt=column:value                      -> value greater than (>)
    &gte=column:value                     -> value greater than equal (>=)
    &lt=column:value                      -> value less than (<)
    &lte=column:value                     -> value less than equal (<=)

    &order=column:asc/desc                -> ordering value
    &table=true                           -> pagination (data = {total: 100, items: []})
    &page=1                               -> pagination
    &limit=1                              -> data limit, default 10, 0 = all

Jika ada 2 atau lebih operator query yang sama, misalkan 2 kali like atau 2 kali wheren, maka query dipakai berulang. Contoh:
  auth/users?
    &where=role_name:superuser
    &like=name:john
    &like=username:alex
    &gte=birthday:2001-01-01

# API CALL
this.API.get(endpoint, (status, data, message) => {execution}, app = '')
this.API.post(endpoint, {body request}, (status, data, message) => {execution}, app = '', isMultipart = false)
this.API.put(endpoint, {body request}, (status, data, message) => {execution}, app = '', isMultipart = false)
this.API.delete(endpoint, {body request}, (status, data, message) => {execution}, app = '')

variable app sudah otomatis melihat url UI, jika /fms/, maka default fms, jika /crm/, maka default crm, dst