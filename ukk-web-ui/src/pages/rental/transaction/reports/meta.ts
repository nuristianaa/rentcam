export const Meta = {
  app: 'rental',
  schema: 'rental',
  name: 'reports',
  title: 'Laporan Transaksi',
  module: 'transaction/reports',
  apiModule: 'transaction/rentals',

  permission: {
    browse: true,
    create: false,
    read: true,
    update: false,
    delete: false,
    restore: false
  },

  paymentMethodOptions: [
    { label: 'Semua', value: '' },
    { label: 'Transfer', value: 'transfer' },
    { label: 'COD',      value: 'cod' },
  ],

  statusOptions: [
    { label: 'Semua', value: '' },
    { label: 'Menunggu Bayar',       value: 'menunggu_bayar' },
    { label: 'Menunggu Verifikasi',  value: 'menunggu_verif' },
    { label: 'Diproses',             value: 'diproses' },
    { label: 'Aktif',                value: 'aktif' },
    { label: 'Selesai',              value: 'selesai' },
    { label: 'Dibatalkan',           value: 'dibatalkan' },
  ],

  statusColor: {
    menunggu_bayar: 'orange',
    menunggu_verif: 'blue',
    diproses:       'purple',
    aktif:          'green',
    selesai:        'teal',
    dibatalkan:     'red',
  } as Record<string, string>,
}
