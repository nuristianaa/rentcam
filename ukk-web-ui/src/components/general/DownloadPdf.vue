<template>
  <slot name="button">
    <q-btn label="Download PDF" @click="downloadPdf" color="primary"  />
  </slot>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Dialog } from 'quasar'
import Api from 'src/services/api'
import { Helper } from 'src/services/helper'

interface Props {
  model: any
  meta: any
}

const props = defineProps<Props>()

const API = new Api()

// simulate PDF API request
const downloadPdf = () => {
  Helper.loadingOverlay(true)

  const status = props.model?.approval_status
  const files = props.model?.approval_files ?? []
  const fileType = status === 'Approve' ? 'signed' : 'unsigned'
  const fileUrl = files.find((r: any) => r.type === fileType)?.url ?? ''
  const filename = props.meta?.title ?? 'document'

  Helper.loadingOverlay(false)

  if (!fileUrl) {
    Helper.showNotif('PDF tidak ditemukan.')
    return
  }

  const blobUrl = Helper.viewBlobFile(fileUrl)

  Dialog.create({
    html: true,
    fullWidth: true,
    fullHeight: true,
    cancel: true,
    ok: 'Download',
    message: `
      <div style="display:flex; flex-direction:column; height:82vh; width:100%;">
        <iframe src="${blobUrl}" style="flex:1; border:none;"></iframe>
      </div>
    `
  }).onOk(() => {
    const link = document.createElement('a')
    link.href = blobUrl
    link.download = `${filename}.pdf`
    link.click()
  })
}
</script>
