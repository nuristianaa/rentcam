export const Meta = {
  schema: 'public',
  name: 'DocumentHistories',
  title: 'Document Histories',
  module: 'document-histories',
  columns: <any>[
    { name: 'template_name', label: 'Template Name', field: 'template_name', align: 'left' },
    { name: 'username', label: 'Username', field: 'username', align: 'left' },
    {
      name: 'created_at',
      label: 'Downloaded At',
      field: 'created_at',
      align: 'left'
    }
  ]
}

export default Meta
