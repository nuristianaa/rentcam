export default {
  project_management: {
    transaction: {
      projects: {
        roleOptions: [
          'PM',
          'ADMIN',
          'FPE',
          'LEAD_TECH',
          'DEV_LEAD',
          'ENGINEER'
        ],
        typeMethodOptions: [
          'PO_VENDOR',
          'INTERNAL_RESOURCE',
          'CASH_EXPANSE'
        ],
        typeResourceOptions: [
          'MATERIAL',
          'LABOR',
          'TOOL',
          'PRELIM'
        ],
      },
      work_orders: {
        status: [
          'DRAFT', 
          'ASSIGNED', 
          'IN_PROGRESS', 
          'COMPLETED', 
          'VERIFIED'
        ]
      },

    }

  }
}
