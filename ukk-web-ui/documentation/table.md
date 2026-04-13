## METADATA
```bash
const Meta = {
  schema: 'auth',
  name: 'Users',
  title: 'Users',
  module: 'auth/users',
  route_ui: 'auth/users',
  ## TABS: variable table() dikosongkan jika tampilan column2nya benar2 sama
  tabs: [
    { name: 'notifications',
      label: 'unread',
      icon: 'mark_chat_unread',
      api: 'me/notifications?where=is_read:false'
    },
    { name: 'all-notifications',
      label: 'all',
      icon: 'mark_chat_read',
      api: 'me/notifications?',
      table: (H, C, L) => {
        const meta = { schema: 'auth', name: 'user_notifications' }
        return [
          { name: 'action', label: '#', field: 'id', align: 'center', style: 'width: 20px' },
          { name: 'type', label: L.module(meta, 'type'), field: 'type', align: 'center' }
        ]
      }
    }
  ],
  tab: 'notifications',
  ## CUSTOM TABLE untuk handle table di .vue
  custom_table: null,

  ## TABLE
  - is_date: true     -> date YYYY-MM-DD
  - datetime: true    -> datetime YYYY-MM-DD HH:ii:ss
  - millis: true      -> timemillis integer
  - colHide: true     -> default hide column, default false
  - filterHide: true  -> column di disable filter datanya, default false
  - sortable: false   -> sorting, default true
  - api: {url: 'auth/roles?limit=0', key: 'id', label: 'name'} -> select opt filter data
  - opt: C.xxx      -> select options saat filter
  - formatter:
    - float         -> 100.20
    - integer       -> 100
    - date          -> YYYY-MM-DD
    - time          -> HH:ii:ss
    - datetime      -> YYYY-MM-DD HH:ii:ss
    - millis        -> int to YYYY-MM-DD HH:ii:ss

  table: (H, C, L) => {
    const meta = { schema: 'auth', name: 'Users' };
    return [
      { config: true, sortBy: 'date', ascending: false },
      { align: 'left', name: 'action', label: '#', field: 'id', style: 'width: 20px', },
      { align: 'left', name: 'name', label: L.module(meta, 'name'), field: 'name' },
      { align: 'left', name: 'role_id', label: L.module(meta, 'role'),
        field: v => v.role?.name,
        api: {url: 'auth/roles?limit=0', key: 'id', label: 'name'}
      },
      { align: 'left', name: 'menu_id', label: L.module(meta, 'menu'),
        field: v => v.menu?.name,
        api: {url: 'auth/master-menus?limit=0', key: 'id', label: 'name'}
      },
      { align: 'left', name: 'birthday', label: L.module(meta, 'birthday'),
        field: 'birthday', is_date: true
      },
      { align: 'left', name: 'hours', label: L.module(meta, 'hours'),
        field: 'hours', is_date: true, datetime: true, millis: true
      },
      { align: 'left', name: 'custom', label: L.module(meta, 'birthday'),
        field: 'custom', colHide: true, filterHide: true, sortable: false
      }
    ];
  },
};
```
## TABLE COMPONENT
# props & emits
```bash
meta        -> Metadata
refresh     -> refresh data ke table
epCustom    -> endpoint custom, ex: locations?table=true
epQuery     -> query tambahan, ex: where=field1:oke&where=field2:oke
row-key     -> custom row key
wrap-cells  -> bool, cell jadi multiline
@add        -> trigger saat add button di klik
@edit       -> trigger saat edit button di klik
@detail     -> trigger saat detail button di klik
@selected   -> trigger saat select table
@getTab     -> trigger saat pindah tab
@getItems   -> trigger saat data items di load
```

<s-table
  :meta="Meta"
  :refresh="refresh"
  :epQuery="custom_query"
  @add="add"
  @edit="edit"
  @detail="detail"
  @onRefresh="onRefresh"
>
  <!-- CHANGE TOP TITLE -->
  <template v-slot:top-title>
    <h1>Custom Title</h1>
  </template>
  <!-- ADD TOP BUTTONS -->
  <template v-slot:top-buttons>
    <q-btn label="Custom Top Button"/>
  </template>

  <!-- CHANGE HEADER VALUE / LABEL -->
  <template v-slot:header-name>
    <span class="bg-yellow-3">
      name
      <q-tooltip>Custom Slot</q-tooltip>
    </span>
  </template>
  <!-- CHANGE ACTION COLUMN -->
  <template v-slot:body-action="props">
    <q-btn dense round flat color="secondary" @click="changePass(props.props.row)" icon="lock">
      <q-tooltip>Reset Password</q-tooltip>
    </q-btn>
  </template>
  <!-- CHANGE SINGLE BODY VALUE -->
  <template v-slot:body-cell-name="props">
    {{ props.props.value }}
  </template>
</s-table>
