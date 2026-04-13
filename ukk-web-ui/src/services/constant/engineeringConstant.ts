export default {
  engineering: {

    master: {
      wms_service_catalog: {
        hierarcy_level: [
          'ATOMIC',
          'GENERAL',
        ],
        project_phase: [
          'PRE_SALES',
          'PRE_PROJECT',
          'EXE',
          'POST',
        ],
        category_type: [
          'PHYSICAL',
          'DIGITAL',
        ],
        complexity_level: [
          'HIGH',
          'MEDIUM',
          'LOW',
        ],
        type_of_cost: [
          'DIRECT_LABOR',
          'FREELANCE',
          'SUB_CONTRACTOR',
        ],
      },
      wms_library: {
        sct_unit: [
          'ManDay',
          'ManHour',
        ],
      },
      wms_components: {
        component_type: [
          'EQUIPMENT',
          'TOOL',
          'MANPOWER',
        ],
      },
      procur_validity_rules: {

      },
      tools: {
        type: [
          'OWNED',
          'RENTED',
          'PROCURED',
        ],
        category: [
          'SAFETY',
          'SUPPORTING',
          'OTHER',
        ],

      },
      items: {
        category: [
          'MAIN_EQUIPMENT',
          'SUPPORTING_EQUIPMENT',
          'INSTALLATION_MATERIAL',
          'CONSUMABLES',
        ],
        level: [
          'HIGH',
          'MEDIUM',
          'LOW',
        ],

      },

      item_vendor_prices: {

      },

    },
    transaction: {
      estimation_labors: {
        type_of_cost: [
          'DIRECT_LABOR',
          'FREELANCE',
          'SUB_CONTRACTOR',
        ],
      },
      estimation_equipments: {
        item_category: [
          'MAIN',
          'SUPPORTING',
          'INSTALLATION_MATERIAL',
          'CONSUMABLES',
        ],
      },
      estimation_preliminary: {
        tool_type: [
          'SUPPORTING',
          'SAFETY',
          'OTHERS',
        ],
      },
      travel_accomodation: {
      },
      request_ce: {
        priority: [
          'NORMAL',
          'HIGH',
          'URGENT',
        ],
        status: [
          'UNSIGNED',
          'TODO',
          'PROGRESS',
          'REVISION',
          'DONE',
          'READY'
        ],
      },
      estimations: {
        location_zone: [
          'INNER_CITY',
          'OUTER_CITY',
          'REMOTE',
        ],

        project_category: [
          'Gajah',
          'Rusa',
          'Unicorn',
          'Sapi Perah',
        ],

      },
    }

  }
}
