# GreenMind AI - Sample PDF Generator

import os
import sys
import subprocess

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing package: {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure reportlab is installed
install_and_import("reportlab")

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor

def create_pdf(filename, title, content_paragraphs):
    os.makedirs("sample_data", exist_ok=True)
    filepath = os.path.join("sample_data", filename)
    
    # Setup document
    doc = SimpleDocTemplate(filepath, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        textColor=HexColor('#059669'), # Emerald
        spaceAfter=15
    )
    
    section_style = ParagraphStyle(
        'DocSection',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=HexColor('#1e293b'), # Slate 800
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10.5,
        textColor=HexColor('#334155'), # Slate 700
        leading=15,
        spaceAfter=10
    )
    
    story = []
    
    # Add title
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 10))
    
    for item in content_paragraphs:
        if item.startswith("SECTION:"):
            section_title = item.replace("SECTION:", "").strip()
            story.append(Paragraph(section_title, section_style))
        else:
            story.append(Paragraph(item, body_style))
            
    doc.build(story)
    print(f"Successfully generated sample PDF at: {filepath}")

# 1. Sample Energy Audit Contents
energy_content = [
    "SECTION: EXECUTIVE SUMMARY",
    "This report documents the annual energy consumption and comprehensive utility audit for the Academic and Residential blocks of the main university campus for the fiscal year 2025. The campus serves approximately 2,000 students and 300 staff members. The audit was conducted to identify saving opportunities, assess renewable energy integration, and map operations to UN SDG 7 (Clean Energy) and SDG 13 (Climate Action).",
    "SECTION: 1. KEY CONSUMPTION DATA",
    "Total annual grid electricity consumption was evaluated at 520,000 kWh, with peak demand of 115 kW occurring during the summer months of April and May. The average monthly utility expenditure stands at INR 3,46,000, totaling INR 41,52,000 annually. Currently, the campus has 0 kW of installed on-site renewable energy, leaving it 100% dependent on the carbon-intensive local thermal power grid.",
    "SECTION: 2. IDENTIFIED INEFFICIENCIES & ISSUES",
    "1. HVAC System Setpoints: The air conditioning units in the main computer engineering labs and administrative server rooms are set at 18 degrees Celsius (64 degrees Fahrenheit) continuously. They run 24 hours a day, including weekends when student labs are closed.",
    "2. Obsolete Lighting Infrastructure: Over 800 standard T8 fluorescent tubes (40W each) remain in service in the hostel corridors and library reading rooms. These units are active throughout the night.",
    "3. Canteen Ventilation: Kitchen exhaust systems and industrial ventilation fans are left running at full power overnight when the canteens are completely closed.",
    "SECTION: 3. RECOMMENDATIONS & SDG MAPPING",
    "- Retrofit all 800 fluorescent tubes with 18W energy-efficient LED tubes. This is expected to save 38,500 kWh annually.",
    "- Reset all classroom and lab thermostat setpoints to a standardized 24 degrees Celsius. Enforce automatic shutdown policies via smart plugs after 6 PM.",
    "- Feasibility Study: Install a 100 kWp rooftop solar photovoltaic array on the Academic Block roof. This will generate approximately 146,000 kWh of clean power annually, reducing grid dependency by 28% and directly advancing SDG 7 target 7.2.",
    "- Implementing these actions will offset approximately 44 metric tons of CO2 equivalent emissions annually, supporting SDG 13 (Climate Action)."
]

# 2. Sample Water Audit Contents
water_content = [
    "SECTION: EXECUTIVE SUMMARY",
    "This water conservation audit report outlines water intake, consumption intensity, and leakage identification across the residential hostels, dining blocks, and laboratories. The main goal is to improve water stewardship, lower municipal water bills, and establish alignment with UN SDG 6 (Clean Water and Sanitation).",
    "SECTION: 1. KEY FOOTPRINT METRICS",
    "Total annual campus water consumption stands at 9,85,50,000 liters (98.55 million liters). For a population of 2,000 residential students, this represents an average water usage intensity of 135 liters per capita per day (LPCD). The annual cost of raw water extraction and municipal sanitation supply charges totals INR 1,47,82,500.",
    "SECTION: 2. IDENTIFIED INEFFICIENCIES & LEAKS",
    "1. High Faucet Flow Rates: Faucets in the hostel restrooms deliver water at an average rate of 15 liters per minute. None are equipped with aerators or auto-cutoff mechanisms.",
    "2. Overhead Tank Overflows: The main storage tanks suffer from faulty float valves. Four major overflow instances were reported this quarter, resulting in an estimated loss of 12,000 liters of potable water per day.",
    "3. Underground Leakage: Pressure tests reveal a constant pressure drop between the main pump house and the sports field. An underground line fracture is suspected, causing a loss of about 15,000 liters daily.",
    "SECTION: 3. ACTION PLAN & SDG CORRESPONDENCE",
    "- Install 2.5 GPM low-flow aerators on all 350 public faucets. This simple retrofitting will cut tap water consumption by 50%.",
    "- Replace all faulty mechanical float valves in the overhead reservoirs with electronic level controllers to eliminate overflow waste completely.",
    "- Locate and repair the underground line fracture. Implementing sub-meters at each hostel block will help isolate future underground leaks.",
    "- Restore and connect the rainwater harvesting sumps to the recharge wells. Roof runoff potential on campus is estimated at 4.2 million liters annually.",
    "- Accomplishing these water efficiency goals will save 24.6 million liters of water annually, improving the score and directly meeting SDG 6 indicators."
]

if __name__ == "__main__":
    create_pdf("sample_energy_audit.pdf", "Campus Energy Audit Report 2025", energy_content)
    create_pdf("sample_water_consumption.pdf", "Campus Water & Leak Audit Report 2025", water_content)
