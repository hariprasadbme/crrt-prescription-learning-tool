"""Simplified flow-based calculations for an educational CRRT prototype."""
def calculate_crrt(modality, weight_kg, dialysate_ml_hr=0, pre_replacement_ml_hr=0,
                   post_replacement_ml_hr=0, net_uf_ml_hr=0, blood_flow_ml_min=0,
                   hematocrit_percent=0, uptime_percent=100, period_hours=24):
    if modality not in {"CVVH", "CVVHD", "CVVHDF"}:
        raise ValueError("Select CVVH, CVVHD, or CVVHDF.")
    if weight_kg <= 0:
        raise ValueError("Weight must be greater than zero.")
    values = [dialysate_ml_hr, pre_replacement_ml_hr, post_replacement_ml_hr, net_uf_ml_hr, blood_flow_ml_min]
    if any(v < 0 for v in values):
        raise ValueError("Flow values cannot be negative.")
    if not 0 <= hematocrit_percent < 100:
        raise ValueError("Haematocrit must be at least 0 and less than 100.")
    if not 0 <= uptime_percent <= 100:
        raise ValueError("Uptime must be between 0 and 100.")
    if period_hours <= 0:
        raise ValueError("Period must be greater than zero.")
    if modality == "CVVH" and dialysate_ml_hr:
        raise ValueError("Dialysate flow must be zero for CVVH.")
    if modality == "CVVHD" and (pre_replacement_ml_hr or post_replacement_ml_hr):
        raise ValueError("Replacement flows must be zero for CVVHD.")
    replacement = pre_replacement_ml_hr + post_replacement_ml_hr
    effluent = dialysate_ml_hr + replacement + net_uf_ml_hr
    dose = effluent / weight_kg
    plasma_water = blood_flow_ml_min * 60 * (1 - hematocrit_percent / 100)
    if pre_replacement_ml_hr > 0:
        predilution_factor = plasma_water / (plasma_water + pre_replacement_ml_hr) if plasma_water + pre_replacement_ml_hr else 1.0
        predilution_applied = True
    else:
        predilution_factor, predilution_applied = 1.0, False
    uptime_fraction = uptime_percent / 100
    return {
        "modality": modality, "weight_kg": weight_kg,
        "dialysate_ml_hr": dialysate_ml_hr, "pre_replacement_ml_hr": pre_replacement_ml_hr,
        "post_replacement_ml_hr": post_replacement_ml_hr, "replacement_total_ml_hr": replacement,
        "net_uf_ml_hr": net_uf_ml_hr, "blood_flow_ml_min": blood_flow_ml_min,
        "hematocrit_percent": hematocrit_percent, "plasma_water_flow_ml_hr": plasma_water,
        "effluent_ml_hr": effluent, "unadjusted_dose_ml_kg_hr": dose,
        "predilution_factor": predilution_factor, "predilution_applied": predilution_applied,
        "predilution_adjusted_dose_ml_kg_hr": dose * predilution_factor,
        "uptime_percent": uptime_percent, "uptime_adjusted_dose_ml_kg_hr": dose * uptime_fraction,
        "period_hours": period_hours, "estimated_running_hours": period_hours * uptime_fraction,
        "estimated_effluent_volume_ml": effluent * period_hours * uptime_fraction,
    }
