// src/pages/detail-registry.ts
import SalesPersonDetail from 'src/pages/crm/master/sales-person/DetailPage.vue'
import QuotationDetail from 'src/pages/crm/transaction/quotations/DetailPage.vue'
import OvertimeDetail from 'src/pages/hris/transaction/overtime/DetailPage.vue'
import PurchaseRequestDetail from 'src/pages/procurement/transaction/purchase-requests/DetailPage.vue'
import RequestEngDetail from 'src/pages/crm/transaction/request-engineering/DetailPage.vue'
import PayableDetai from './finance/transaction/payables/DetailPage.vue'
import CommercialCheckDetail from 'src/pages/crm/transaction/commercial-checks/DetailPage.vue'

export const detailRegistry = {
  'crm.master.sales-person': {
    component: SalesPersonDetail,
    props: ({ model }) => ({
        props: {
            id: model?.module_id
        }
    })
  },
  'crm.transaction.request-engineer': {
    component: RequestEngDetail,
    props: ({ model }) => ({
        props: {
            id: model?.module_id
        }
    })
  },
  'hris.transaction.overtime': {
    component: OvertimeDetail,
    props: ({ model }) => ({
        data: {
            id: model?.module_id
        }
    })
  },
  'procurement.transaction.purchase-requests': {
    component: PurchaseRequestDetail,
    props: ({ model }) => ({
        props: {
            id: model?.module_id
        }
    })
  },
  'crm.transaction.quotations': {
    component: QuotationDetail,
    props: ({ model }) => ({
        data: {
            id: model?.module_id,
        }
    })
  },
  'finance.transaction.payables': {
    component: PayableDetai,
    props: ({ model }) => ({
        data: {
            id: model?.module_id,
        }
    })
  },
  'crm.transaction.commercial-checks': {
    component: CommercialCheckDetail,
    props: ({ model }) => ({
        data: {
            id: model?.module_id,
        }
    })
  }
}