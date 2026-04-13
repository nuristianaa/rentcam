modules = [
  {"model": "prod.wo_parents", "label": "Work Orders"},
  {"model": "prod.ba_ob_distances", "label": "BA OB Distances"},
  {"model": "prod.ob_removals", "label": "OB Removal & Distances"},
  {"model": "transaction.ba_ob_removal_distances", "label": "BA OB Removal & Distances"},
  {"model": "prod.delivery_orders", "label": "Delivery Orders"},
  {"model": "prod.delivery_order_cycles", "label": "Delivery Order Cycles"},
  {"model": "transaction.ba_haulings", "label": "BA Haulings"},
  {"model": "prod.crusher_productions", "label": "Crusher Productions"},
  {"model": "prod.barge_loadings", "label": "Barge Loadings"},
  {"model": "prod.barge_discharges", "label": "Barge Discharges"},
  {"model": "transaction.ba_coal_losses", "label": "BA Coal Losses"},
  {"model": "prod.stock_movements", "label": "Stock Movements"},
  {"model": "timesheet.activity_groups", "label": "Activity Groups"},
  {"model": "timesheet.he_activities", "label": "HE Activities"},
  {"model": "transaction.quality_result_headers", "label": "Quality Sampling & Analysis"},
  {"model": "transaction.quality_results", "label": "Quality Raw Results"},
  {"model": "transaction.quality_movements", "label": "Quality Movements"},
  {"model": "prod.fleet_volumes", "label": "Fleet Volumes"},
  {"model": "transaction.ba_ob_coal_volumes", "label": "BA OB Coal Volumes"},
  {"model": "transaction.ba_stock_surveys", "label": "BA Stock Surveys"},
  {"model": "prod.terrestrial_surveys", "label": "Terrestrial Surveys"},
  {"model": "monitoring.weathers", "label": "Weathers"},
  {"model": "monitoring.unit_histories", "label": "Unit Histories"},
  {"model": "monitoring.rainfall_histories", "label": "Rainfall Histories"},
  {"model": "monitoring.road_parameters", "label": "Road Parameters"},
  {"model": "monitoring.road_masters", "label": "Road Masters"},
  {"model": "monitoring.road_availables", "label": "Road Availables"},
  {"model": "prod.weighing_orders", "label": "Weighing Orders"},
  {"model": "prod.wo_he", "label": "Weighing Order Heavy Equipments"},
]


def trans_module(model: str) -> str:
  label = next((item.get("label", model) for item in modules if item["model"] == model), model)
  return label
