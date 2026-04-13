def calculate_ua(working_hours: float, standby: float):
  divider = working_hours + standby
  return (working_hours / divider) * 100 if divider > 0 else 0


def calculate_pa(working_hours: float, standby: float, breakdown: float):
  divider = working_hours + standby + breakdown
  return ((working_hours + standby) / divider) * 100 if divider > 0 else 0
