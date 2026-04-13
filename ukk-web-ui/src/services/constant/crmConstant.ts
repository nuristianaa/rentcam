export default {
  crm: {
    master: {
      
    },
    plan: {
     
    },
    transaction: {
      pricing_items: {
        category: [
          { id: "MAIN_EQUIPMENT", name: 'MAIN EQUIPMENT' },
          { id: "SUPPORTING_EQUIPMENT", name: 'SUPPORTING EQUIPMENT' },
          { id: "INSTALLATION_MATERIAL", name: 'INSTALLATION MATERIAL' },
          { id: "CONSUMABLES", name: 'CONSUMABLES' }
        ],
      },
      pricing_services: {
        category: [
          { id: "DIRECT_LABOR", name: 'DIRECT LABOR' },
          { id: "FREELANCE", name: 'FREELANCE' },
          { id: "SUB_CONTRACTOR", name: 'SUB CONTRACTOR' },
        ],
      },
      project_plan: {
        stage: [
          // { id: "MY_FARM", name: "MY FARM" },
          { id: "LEADS", name: "LEADS" },
          { id: "QUALIFIED", name: "QUALIFIED" },
          { id: "SURVEY_ASSESMENT", name: "SURVEY ASSESMENT" },
          { id: "SOLUTION_DESIGN", name: "SOLUTION DESIGN" },
          { id: "QUOTATION", name: "QUOTATION" },
          { id: "NEGOTIATION", name: "NEGOTIATION" },
          { id: "WON", name: "WON" },
          // { id: "LOST", name: "LOST" }
        ],
        stage_default: [
          // { id: "MY_FARM", name: "MY FARM" },
          { id: "LEADS", name: "LEADS" },
          { id: "QUALIFIED", name: "QUALIFIED" },
          { id: "SURVEY_ASSESMENT", name: "SURVEY ASSESMENT" },
          { id: "SOLUTION_DESIGN", name: "SOLUTION DESIGN" },
          { id: "QUOTATION", name: "QUOTATION" },
          { id: "NEGOTIATION", name: "NEGOTIATION" },
          { id: "WON", name: "WON" },
          { id: "LOST", name: "LOST" }
        ]
      },
      quotations: {
        status: [
          'DRAFT',
          'PROGRESS_APPROVE',
          'APPROVE',
          'SENT',
          'CANCEL',
        ],

      },
      commercial_checks:{
        status: [
          'NEW',
          'CUSTOMER',
        ],
      }
    }
  }
}
