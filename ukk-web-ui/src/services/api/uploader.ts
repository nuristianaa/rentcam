import Api from 'src/services/api'
const API = new Api()

export const storeFile = async (url: any, id: any, code: any, files: any, deletedIds: any, app: any = 'rental') => {
  const model = new FormData()
  if (id) model.append('id', String(id))
  if (code) model.append('code', String(code))

  files.value.forEach((item: { attachmentId: string; file: string | Blob; tempId: string; colSize: any, remark: any, maxHeight: any }) => {
    // ===============================
    // CASE 1: Existing but replaced
    // ===============================
    if (item.attachmentId && item.file instanceof File) {
      if (!item.tempId) {
        item.tempId = 'temp_' + Math.random().toString(36).slice(2, 10)
      }

      model.append('order[]', `new:${item.tempId}`)
      model.append(`file_${item.tempId}`, item.file)

      // 💡 Kirim colSize
      if (item.colSize != null) {
        model.append(`colSize_${item.tempId}`, String(item.colSize))
      }
      if (item.remark != null) {
        model.append(`remark_${item.tempId}`, item.remark)
      }
      
      if (item.maxHeight != null) {
        model.append(`maxHeight_${item.tempId}`, String(item.maxHeight))
      }

      model.append('delete_ids[]', item.attachmentId)
      return
    }

    // ===============================
    // CASE 2: Existing untouched
    // ===============================
    if (item.attachmentId && !item.file) {
      model.append('order[]', `attachment:${item.attachmentId}`)

      // 💡 Kirim colSize untuk attachment existing
      if (item.colSize != null) {
        model.append(`colSize_${item.attachmentId}`, String(item.colSize))
      }
      if (item.remark != null) {
        model.append(`remark_${item.attachmentId}`, item.remark)
      }
      
      if (item.maxHeight != null) {
        model.append(`maxHeight_${item.attachmentId}`, String(item.maxHeight))
      }
      return
    }

    // ===============================
    // CASE 3: Truly new
    // ===============================
    if (item.tempId && item.file instanceof File) {
      model.append('order[]', `new:${item.tempId}`)
      model.append(`file_${item.tempId}`, item.file)

      // 💡 Kirim colSize untuk file baru
      if (item.colSize != null) {
        model.append(`colSize_${item.tempId}`, String(item.colSize))
      }
      if (item.remark != null) {
        model.append(`remark_${item.tempId}`, item.remark)
      }
      
      if (item.maxHeight != null) {
        model.append(`maxHeight_${item.tempId}`, String(item.maxHeight))
      }
      return
    }
  })

  // Unique delete ids
  const uniqueDeletes = Array.from(new Set(deletedIds.value))
  uniqueDeletes.forEach((id) => model.append('delete_ids[]', String(id)))

  let status = 200
  await API.post(
    url,
    model,
    (s: number) => (status = s),
    app,
    true
  )

  if (status === 200) {
    deletedIds.value = []
  }

  return status
}