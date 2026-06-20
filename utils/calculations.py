# GreenMind AI - Calculations & Math Models

# Global constants for calculations
GRID_CO2_FACTOR = 0.85  # kg CO2 per kWh of grid electricity
CARBON_OFFSET_TREE_YEAR = 22.0  # kg CO2 absorbed by one mature tree in a year
COST_PER_KWH = 8.0     # Average electricity tariff (INR/currency units per kWh)
COST_PER_LITER_WATER = 0.15 # Average water supply cost (INR/currency units per liter)
BASE_STUDENTS = 2000    # Default campus size

# Baseline operational parameters (Before optimizations)
BASELINE = {
    "electricity_kwh": 600000.0,      # Annual grid electricity usage (kWh) -> ~300 kWh/student/year
    "water_liters": 98550000.0,       # Annual water consumption (liters) -> 135 LPCD for 2000 students
    "waste_tons": 100.0,              # Annual solid waste generated (metric tons) -> 50 kg/student/year
    "recycling_rate": 20.0,           # Percentage of waste recycled/composted (%)
    "solar_capacity": 0.0             # Installed solar panels capacity (kW)
}

def calculate_score(electricity_kwh, water_liters, waste_tons, recycling_rate, students=BASE_STUDENTS):
    """
    Calculates sustainability scores out of 100 for individual areas and overall.
    Returns a dict of scores.
    """
    # 1. Energy Score (Goal: <= 200 kWh per student/year. Penalty above that up to 400 kWh)
    kwh_per_student = electricity_kwh / students
    if kwh_per_student <= 200:
        energy_score = 100.0
    elif kwh_per_student >= 400:
        energy_score = 10.0
    else:
        energy_score = 100.0 - ((kwh_per_student - 200) / (400 - 200) * 90.0)
        
    # 2. Water Score (Goal: <= 80 LPCD (Liters Per Capita Day). Penalty up to 150 LPCD)
    # Annual water divided by students / 365
    lpcd = water_liters / students / 365.0
    if lpcd <= 75:
        water_score = 100.0
    elif lpcd >= 150:
        water_score = 15.0
    else:
        water_score = 100.0 - ((lpcd - 75) / (150 - 75) * 85.0)
        
    # 3. Waste Score (Composed of 60% recycling rate and 40% waste minimisation (Goal <= 40 kg/student/year))
    waste_per_student_kg = (waste_tons * 1000) / students
    if waste_per_student_kg <= 30:
        minimisation_score = 100.0
    elif waste_per_student_kg >= 70:
        minimisation_score = 20.0
    else:
        minimisation_score = 100.0 - ((waste_per_student_kg - 30) / (70 - 30) * 80.0)
        
    waste_score = (0.6 * recycling_rate) + (0.4 * minimisation_score)
    waste_score = max(0.0, min(100.0, waste_score))
    
    # 4. Carbon Footprint Score
    # Total CO2 = grid electricity * GRID_CO2_FACTOR
    co2_tons = (electricity_kwh * GRID_CO2_FACTOR) / 1000.0
    co2_per_student_kg = (co2_tons * 1000) / students
    # Goal: <= 150 kg CO2 per student/year. Penalty up to 350 kg CO2/student/year
    if co2_per_student_kg <= 150:
        carbon_score = 100.0
    elif co2_per_student_kg >= 350:
        carbon_score = 10.0
    else:
        carbon_score = 100.0 - ((co2_per_student_kg - 150) / (350 - 150) * 90.0)
        
    # Overall Score (Weighted Average)
    overall_score = (0.3 * energy_score) + (0.25 * water_score) + (0.2 * waste_score) + (0.25 * carbon_score)
    
    return {
        "energy": round(energy_score, 1),
        "water": round(water_score, 1),
        "waste": round(waste_score, 1),
        "carbon": round(carbon_score, 1),
        "overall": round(overall_score, 1)
    }

def get_grade(score):
    """Returns a letter grade from A+ to F based on score."""
    if score >= 90: return "A+"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    if score >= 50: return "D"
    return "F"

def simulate_scenario(elec_reduction_pct, solar_kw, water_reduction_pct, waste_recycling_rate, students=BASE_STUDENTS):
    """
    Computes operational metrics and savings based on user inputs.
    Returns baseline vs optimized results.
    """
    # 1. Base carbon and costs
    base_co2 = (BASELINE["electricity_kwh"] * GRID_CO2_FACTOR) / 1000.0
    base_cost_elec = BASELINE["electricity_kwh"] * COST_PER_KWH
    base_cost_water = BASELINE["water_liters"] * COST_PER_LITER_WATER
    base_cost = base_cost_elec + base_cost_water
    
    # 2. Optimized Electricity Calculation
    # Solar generation: 1 kWp installed yields ~4 kWh/day -> 4 * 365 = 1460 kWh/year
    solar_generation = solar_kw * 4.0 * 365.0
    reduced_grid_elec = BASELINE["electricity_kwh"] * (1 - elec_reduction_pct / 100.0)
    
    # Total grid electricity net footprint (can be negative if solar generation exceeds usage)
    opt_grid_elec = reduced_grid_elec - solar_generation
    opt_co2 = (opt_grid_elec * GRID_CO2_FACTOR) / 1000.0
    
    # Electricity savings cost (considering net metering credits for excess generation)
    opt_cost_elec = opt_grid_elec * COST_PER_KWH
    if reduced_grid_elec < solar_generation:
        # Excess fed to grid, credited at 50% retail tariff
        excess = solar_generation - reduced_grid_elec
        opt_cost_elec -= excess * (COST_PER_KWH * 0.5)
        
    # 3. Optimized Water Calculation
    opt_water = BASELINE["water_liters"] * (1 - water_reduction_pct / 100.0)
    opt_cost_water = opt_water * COST_PER_LITER_WATER
    
    # 4. Waste & Recycling
    # Waste generation stays same, but recycling changes waste score
    
    # 5. Summary metrics
    opt_cost = opt_cost_elec + opt_cost_water
    
    financial_savings = base_cost - opt_cost
    co2_saved_tons = base_co2 - opt_co2
    water_saved_liters = BASELINE["water_liters"] - opt_water
    trees_equivalent = (co2_saved_tons * 1000.0) / CARBON_OFFSET_TREE_YEAR
    
    # Scores
    base_scores = calculate_score(
        BASELINE["electricity_kwh"],
        BASELINE["water_liters"],
        BASELINE["waste_tons"],
        BASELINE["recycling_rate"],
        students
    )
    
    opt_scores = calculate_score(
        opt_grid_elec,
        opt_water,
        BASELINE["waste_tons"],
        waste_recycling_rate,
        students
    )
    
    # SDG Mapping indicator strengths based on actions
    sdg_impact = {
        "SDG 6 (Water)": min(100.0, water_reduction_pct * 3.0),
        "SDG 7 (Energy)": min(100.0, (elec_reduction_pct + (solar_kw / 5.0)) * 2.0),
        "SDG 11 (Communities)": min(100.0, (elec_reduction_pct + water_reduction_pct + (waste_recycling_rate - BASELINE["recycling_rate"])) * 1.5),
        "SDG 12 (Consumption)": min(100.0, waste_recycling_rate),
        "SDG 13 (Climate)": min(100.0, (co2_saved_tons / max(1.0, base_co2)) * 100.0)
    }
    
    return {
        "baseline": {
            "electricity_kwh": BASELINE["electricity_kwh"],
            "water_liters": BASELINE["water_liters"],
            "waste_tons": BASELINE["waste_tons"],
            "recycling_rate": BASELINE["recycling_rate"],
            "co2_tons": round(base_co2, 2),
            "cost": round(base_cost, 2),
            "scores": base_scores,
            "lpcd": round(BASELINE["water_liters"] / students / 365.0, 1),
            "kwh_per_student": round(BASELINE["electricity_kwh"] / students, 1)
        },
        "optimized": {
            "electricity_kwh": round(opt_grid_elec, 1),
            "water_liters": round(opt_water, 1),
            "waste_tons": BASELINE["waste_tons"],
            "recycling_rate": waste_recycling_rate,
            "co2_tons": round(opt_co2, 2),
            "cost": round(opt_cost, 2),
            "scores": opt_scores,
            "lpcd": round(opt_water / students / 365.0, 1),
            "kwh_per_student": round(opt_grid_elec / students, 1)
        },
        "savings": {
            "financial": round(financial_savings, 2),
            "co2_tons": round(co2_saved_tons, 2),
            "water_liters": round(water_saved_liters, 1),
            "trees": round(trees_equivalent, 0)
        },
        "sdg_impact": sdg_impact
    }
