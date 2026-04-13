export default {
  procurement: {
    master: {
        vendors:{
                categories: ['MATERIAL_SUPPLIER', 'SUBCON', 'FREELANCER']
            }
        },
        transaction: {
            good_receipts: {
                status: [
                'DRAFT',
                'COMPLETED',
                ],
            },
            goods_receipt_items: {
            },
            delivery_orders: {
                status: [
                'DRAFT',
                'ISSUED',
                'COMPLETED',
                ],
            },
            delivery_order_items: {
            },
        }
    },
}
