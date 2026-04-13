<template>
  <slot name="button">
    <q-btn label="Download PDF" @click="generatePdf" color="primary"  />
  </slot>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Dialog } from 'quasar'
import Api from 'src/services/api'
import { Helper } from 'src/services/helper'

interface Props {
  modelValue: {
    app: string
    path: string
    filename: string
    template?: string
    format?: string
    landscape?: false
    attachement_landscape?: false
  }
}

const props = defineProps<Props>()

const API = new Api()
const pdfDialog = ref(false)
const pdfBlobUrl = ref('')

// simulate PDF API request
const generatePdf = () => {
  Helper.loadingOverlay(true)
  API.post(
    'generate-pdf',
    props.modelValue,
    (status: number, _data: any, _message: any, response: any) => {
      Helper.loadingOverlay(false)
      if (status === 200) {
        const blob = new Blob([response.data], { type: 'application/pdf' })
        const blobUrl = URL.createObjectURL(blob)

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
        })
          .onOk(() => {
            const filename = props.modelValue.filename ?? 'docs'
            const link = document.createElement('a')
            link.href = blobUrl
            link.download = `${filename}.pdf`
            link.click()
          })
          .onCancel(() => {
            // console.log('Cancel')
          })
          .onDismiss(() => {
            // console.log('I am triggered on both OK and Cancel')
          })
        // // Show in iframe dialog
        // Dialog.create({
        //   message: `
        //     <div style="display: flex; flex-direction: column; height: 85vh; width: 100%; padding: 0; margin: 0;">
        //       <iframe src="${blobUrl}" style="flex: 1; width: 100%; height: 100%; border: none; margin: 0; padding: 0;"></iframe>
        //     </div>
        //   `,
        //   html: true,
        //   fullWidth: true,
        //   fullHeight: true,
        //   ok: 'Close'
        // });
      }
    },
    'main',
    false,
    'blob'
  )
}
</script>
