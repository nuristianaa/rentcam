<template>
  <div class="fm-wrapper">
    <q-btn dense flat color="grey-6"  size="16px" icon="settings_suggest" class="fm-btn-settings" @click="showModal = true" />
    <InputFormula v-model="finalFormula" :tokens="tokens" :validation-errors="getErrorFinalFormula" />

    <q-dialog v-model="showModal">
      <q-card style="width: 80vw; max-width: 90vw">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6">Close icon</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-card-section style="max-height: 50vh" class="scroll">
          <q-markup-table class="fm-table" flat bordered dense>
            <thead>
              <tr>
                <th class="fm-table__col fm-table__col--header" width="25%">Reference</th>
                <th class="fm-table__col fm-table__col--header">Value / Formula</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="field in fields" :key="field.referenceName">
                <tr v-if="field.referenceName !== '_result_'">
                  <td class="fm-table__col fm-table__col--input">
                    <b class="fm-var-name">{{ field.referenceName }}</b>
                  </td>
                  <td class="fm-table__col fm-table__col--input">
                    <template v-if="field.type === 'formula'">
                      <InputFormula @blur="emiters" v-model="field.formula" :tokens="extendedTokensByRefs[field.referenceName]?.tokens" :validation-errors="extendedTokensByRefs[field.referenceName]?.validationErrors" />
                      <div class="fm-result-viewer">Result : {{ getResult(field.referenceName) }}</div>
                    </template>
                    <span class="text-bold text-blue-10" v-else>{{ Helper.formatNumberAuto(field.formula) }}</span>
                  </td>
                </tr>
              </template>
            </tbody>
          </q-markup-table>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- <json-viewer label="extendedTokensByRefs" :data="extendedTokensByRefs" /> -->
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { evaluateTokenNodes, getExtendedTokens, type ExtendedFormulaEntry } from 'src/services/formula-parser'
import InputFormula from 'src/components/form/InputFormula.vue'
import { Helper } from 'src/services/helper'

const props = defineProps<{
  modelValue: string | number | null | undefined
  formula: string | number | null | undefined
  cleanFields?: boolean
  sources?: SourceItem[]
  references?: ReferenceItem[]
}>()

const emit = defineEmits(['update:model-value', 'change'])

type ReferenceItem = {
  referenceName: string
  formula?: string | number | null | undefined
}

type SourceItem = {
  key: string
  refCol: string
  value?: string | number | null | undefined
}

const finalFormula = ref(props.formula)
const showModal = ref(false)
const items = ref<Record<string, string | number | null | undefined>[]>([])
const fields = ref<Record<string, string | number | null | undefined>[]>([])

const supportedRefs = computed(() => {
  if (!items.value.length) return []
  return Object.keys(items.value?.[0] ?? {})
})

const formulasByRefs = computed(() =>
  fields.value.reduce((out: Record<string, string>, field) => {
    if (field.referenceName) {
      out[field.referenceName] = field.formula ?? ''
    }
    return out
  }, {})
)

const extendedTokens = computed(() => getExtendedTokens(formulasByRefs.value, supportedRefs.value))

const extendedTokensByRefs = computed(() =>
  Object.values(extendedTokens.value).reduce((out: Record<string, ExtendedFormulaEntry>, entry) => {
    out[entry.referenceNameOrig] = entry
    return out
  }, {})
)

const extendedTokensOrdered = computed(() => Object.values(extendedTokens.value).sort((a, b) => a.order - b.order))

const extendedItems = computed(() =>
  items.value.map((item) => {
    const extendedItem: Record<string, string> = {}
    Object.entries(item).forEach(([key, value]) => {
      extendedItem[key] = (value === 0 ? 0 : value || '').toString()
    })
    extendedTokensOrdered.value.forEach((entry) => {
      extendedItem[entry.referenceNameOrig] = evaluateTokenNodes(entry.tokenNodes, (prop: string) => (extendedItem[prop] || '').toString())
    })
    return extendedItem
  })
)

const result = computed(() => {
  return getResult()
})

const tokens = computed(() => {
  return getResultRaw('tokens')
})

function getResult(key: string = '_result_') {
  let res = null

  extendedItems.value.map((item: any) => {
    // const key = '_result_'
    if (extendedTokensByRefs.value[key]?.validationErrors?.length) res = null
    else res = item[key] || null
  })

  return res
}

function getResultRaw(selector: string) {
  const result = extendedTokensByRefs.value?._result_
  if (!result) return null

  return result[selector] ?? null
}

function toFormulaObject(list: ReferenceItem[] = [], sources: SourceItem[] = []) {
  const referencePart = Object.fromEntries(
    list.map((ref) => {
      const key = ref.referenceName || '__missing_key__'

      // cari source yg sama key-nya
      const source = sources.find((s) => s.key === ref.referenceName)

      const value = ref.formula !== null && ref.formula !== undefined ? ref.formula : (source?.value ?? null)

      return [key, value]
    })
  )

  // ambil source yang belum ada di reference
  const sourceExtras = Object.fromEntries(sources.filter((s) => !list.some((ref) => ref.referenceName === s.key)).map((s) => [s.key, s.value ?? null]))

  // gabungkan semuanya + result
  return {
    ...referencePart,
    ...sourceExtras,
    _result_: finalFormula.value ?? ''
  }
}

function buildFields() {
  if (!props.references) return []

  const references = props.references
  const sources = props.sources ?? []

  // hasil dari reference
  const refsPart = references.map((ref) => {
    const source = sources.find((s) => s.key === ref.referenceName)

    const val = ref.formula !== null && ref.formula !== undefined ? ref.formula : (source?.value ?? '')
    return {
      referenceName: ref.referenceName,
      refCol: null,
      formula: '' + val + '', // convert to string
      type: source ? 'default' : 'formula'
    }
  })

  // cari source yang tidak punya pasangan reference
  const sourceExtras = sources
    .filter((src) => !references.some((ref) => ref.referenceName === src.key))
    .map((src) => ({
      referenceName: src.key,
      refCol: src.refCol, // default label jika tidak ada di reference
      formula: `${src.value ?? ''}`,
      type: 'default'
    }))

  return [
    ...sourceExtras,
    ...refsPart,
    {
      referenceName: '_result_',
      refCol: 'Result',
      formula: finalFormula.value ?? '',
      type: 'result'
    }
  ]
}

function prepare() {
  const item = toFormulaObject(props.references ?? [], props.sources ?? [])
  items.value.push(item)

  fields.value = buildFields()
}

function bindFinalFormula(v: string) {
  if (!fields.value.length) return false

  // cari row dengan key "_result_"
  const target = fields.value.find((f) => f.referenceName === '_result_')
  if (target) {
    target.formula = v
  }
}

const getErrorFinalFormula = computed(() => {
  if (!extendedTokens.value._result_) return []

  const target = extendedTokens.value._result_
  if (target) {
    return target.validationErrors
  } else return []
})

function extractRefAndFormula(obj: Record<string, any>) {
  const result: Record<string, { referenceName: string; formula: string }> = {}

  for (const key in obj) {
    if (obj[key]) {
      result[key] = {
        referenceName: obj[key].referenceName,
        formula: obj[key].formula
      }
    }
  }

  return result
}

const emiters = () => {
  // console.log('emit(update:modelValue)', result.value)
  emit('update:model-value', result.value)

  let raw = extendedTokensByRefs.value
  if (props.cleanFields) {
    raw = extractRefAndFormula(raw)
  }

  emit('change', result.value, getErrorFinalFormula.value?.map((error) => error.errorType).join(', '), getErrorFinalFormula.value, raw)
}

watch(
  () => props.references,
  () => {
    prepare()
  },
  { immediate: true }
)

watch(
  () => result.value,
  () => {
    emit('update:model-value', result.value)
  },
  { immediate: true }
)

watch(
  () => props.formula,
  (v: any) => {
    bindFinalFormula(v)
  },
  { immediate: true }
)

watch(
  () => finalFormula.value,
  (v: any) => {
    bindFinalFormula(v)
    emiters()
  },
  { immediate: true }
)
</script>
