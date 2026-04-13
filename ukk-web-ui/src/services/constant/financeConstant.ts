export default {
  finance: {
    master: {
      chart_of_accounts:{
        account_type: ["ASSET", "LIABILITY", "EQUITY", "REVENUE", "EXPENSE"]
      },
      cost_centers:{
        type: ["PROJECT", "DEPARTMENT"]
      },
    },
    plan: {
     
    },
    transaction: {
      journal_entries: {
        trx_code: [
          'SALES_INVOICE',
          'MANUAL',
        ],
        status: [
          {name: 'DRAFT', id: 'DRAFT'},
          {name: 'POSTED', id: 'POSTED'},
          {name: 'REVERSED', id: 'REVERSED'},
        ],
      },
      billing_managements: {
        term_type: [
          'DP',
          'PROGRESS',
          'RETENTION',
        ],
        status: [
          'DRAFT',
          'SENT',
          'PARTIAL_PAID',
          'PAID',
          'OVERDUE',
          'WRITE_OFF',
        ],
      },
    }
  }
}
