<template>
  <div class="row">
    <div class="col-12 q-pb-sm text-bold text-grey-8">
      {{ label }}
    </div>
    <div v-if="data" class="col-12" v-html="jsonViewer(data)"></div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  data?: any
  label?: string
}

const props = defineProps<Props>()

function jsonViewer(json: any, collapsible = false): string {
  json = JSON.parse(JSON.stringify(json))

  const TEMPLATES = {
    item: `
      <div class="json__item">
        <div class="json__key">%KEY%</div>
        <div class="json__value json__value--%TYPE%">%VALUE%</div>
      </div>`,
    itemCollapsible: `
      <label class="json__item json__item--collapsible">
        <input type="checkbox" class="json__toggle" />
        <div class="json__key">%KEY%</div>
        <div class="json__value json__value--type-%TYPE%">%VALUE%</div>
        %CHILDREN%
      </label>`,
    itemCollapsibleOpen: `
      <label class="json__item json__item--collapsible">
        <input type="checkbox" checked class="json__toggle" />
        <div class="json__key">%KEY%</div>
        <div class="json__value json__value--type-%TYPE%">%VALUE%</div>
        %CHILDREN%
      </label>`
  }

  function createItem(key: string, value: string, type: string): string {
    let element = TEMPLATES.item.replace('%KEY%', key)
    if (type === 'string') {
      element = element.replace('%VALUE%', `"${value}"`)
    } else {
      element = element.replace('%VALUE%', String(value))
    }
    element = element.replace('%TYPE%', type)
    return element
  }

  function createCollapsibleItem(key: string, typeLabel: string, type: string, children: string): string {
    const tpl = collapsible ? 'itemCollapsibleOpen' : 'itemCollapsible'
    let element = TEMPLATES[tpl].replace('%KEY%', key)
    element = element.replace('%VALUE%', typeLabel)
    element = element.replace('%TYPE%', type)
    element = element.replace('%CHILDREN%', children)
    return element
  }

  function handleChildren(key: string, value: any, type: string): string {
    let html = ''

    if (Array.isArray(value)) {
      for (let i = 0; i < value.length; i++) {
        html += handleItem(String(i), value[i])
      }
      return createCollapsibleItem(key, `[Array(${value.length})]`, 'array', html)
    } else {
      for (const item in value) {
        html += handleItem(item, value[item])
      }
      return createCollapsibleItem(key, '{Object}', 'object', html)
    }
  }

  function handleItem(key: string, value: any): string {
    if (value === null) {
      return createItem(key, 'null', 'null')
    }

    if (Array.isArray(value)) {
      return handleChildren(key, value, 'array')
    }

    if (typeof value === 'object') {
      return handleChildren(key, value, 'object')
    }

    return createItem(key, value, typeof value)
  }

  function parseObject(obj: Record<string, any>): string {
    let result = '<div class="json">'
    for (const item in obj) {
      result += handleItem(item, obj[item])
    }
    result += '</div>'
    return result
  }

  return parseObject(json)
}
</script>
