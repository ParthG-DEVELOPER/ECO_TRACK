import streamlit as st
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()



# Inject heavy graphics, background designs, and eco-title styling via CSS
st.set_page_config(page_title="EcoDrive Carbon Calculator", layout="wide")

# Inject heavy graphics, background designs, and eco-title styling via CSS
st.markdown(
    """
    <style>
    /* 1. Main App Background Styling (Eco-Tech Dark Theme) */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0a1410 0%, #050a08 100%);
        background-attachment: fixed;
    }
    
    /* Decorative Abstract Matrix/Grid Graphics in Background */
    .stApp::before {
        content: "";
        position: fixed;
        top: -10%;
        left: -10%;
        width: 120%;
        height: 120%;
        background-image: 
            linear-gradient(45deg, rgba(0, 230, 115, 0.02) 25%, transparent 25%), 
            linear-gradient(-45deg, rgba(0, 230, 115, 0.02) 25%, transparent 25%);
        background-size: 50px 50px;
        z-index: -1;
        pointer-events: none;
    }

    /* Floating Keyframe Animation Definition */
    @keyframes smoothFloat {
        0% {
            transform: translateY(0px);
            box-shadow: 0px 15px 35px rgba(0, 0, 0, 0.8);
        }
        50% {
            transform: translateY(-10px);
            box-shadow: 0px 25px 45px rgba(0, 230, 115, 0.15);
        }
        100% {
            transform: translateY(0px);
            box-shadow: 0px 15px 35px rgba(0, 0, 0, 0.8);
        }
    }

    /* 2. Impressive Green Eco-Title Banner Styling with Floating Effect */
    .hero-title-container {
        background: linear-gradient(90deg, rgba(0,230,115,0.08) 0%, rgba(0,0,0,0.7) 50%, rgba(0,230,115,0.08) 100%);
        padding: 35px;
        border-radius: 16px;
        border-top: 3px solid #00e673;
        border-bottom: 3px solid #00e673;
        text-align: center;
        margin-bottom: 40px;
        
        /* Apply smooth infinite floating loop */
        animation: smoothFloat 4s ease-in-out infinite;
    }

    .hero-title {
        font-family: 'Century Gothic', 'Arial Black', sans-serif;
        font-size: 3.5rem !important;
        color: #FFFFFF;
        text-transform: uppercase;
        letter-spacing: 5px;
        text-shadow: 0 0 15px rgba(0, 230, 115, 0.6);
        margin: 0;
    }

    .hero-subtitle {
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.1rem;
        color: #a3c2b5;
        letter-spacing: 2px;
        margin-top: 12px;
    }
    </style>
    
    <!-- Render the Floating Top Title HTML Structure -->
    <div class="hero-title-container">
        <h1 class="hero-title">EcoTrack Emission Engine</h1>
        <div class="hero-subtitle">Calculate and Compare Carbon Footprints Across Traditional Car Segments</div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- App Logic & Interactive Widgets ---

# Master list of all traditional car types (excluding bicycle & electric)
car_types = [
    "Sedan", "Coupe", "Hatchback", "Convertible", "Station Wagon",
    "SUV", "Crossover", "Pickup Truck", "Minivan", "Van", "Ute",
    "Sports Car", "Supercar", "Roadster", "Targa", "Muscle Car", 
    "Grand Tourer", "Shooting-Brake", "Limousine", "Hearse", "Microcar"
]

# Layout setup using Streamlit columns
col1, col2, col3 = st.columns(3)

with col1:
    selected_car = st.selectbox("🚗 Select Vehicle Segment:", car_types)

with col2:
    selected_year = st.slider("📅 Select Model Year:", min_value=1990, max_value=2028, value=2026, step=1)

with col3:
    distance = st.number_input("🛣️ Annual Distance Driven (in km):", min_value=1, value=12000, step=500)

# Mock Calculation Logic (Based on segment averages for standard internal combustion engines)
base_emissions = {
    "Microcar": 95, "Hatchback": 120, "Sedan": 140, "Coupe": 150, "Station Wagon": 160,
    "Crossover": 165, "Convertible": 170, "Roadster": 175, "Grand Tourer": 210, 
    "SUV": 220, "Minivan": 230, "Shooting-Brake": 230, "Targa": 240, "Ute": 250, 
    "Pickup Truck": 270, "Van": 280, "Sports Car": 290, "Limousine": 320, 
    "Muscle Car": 340, "Hearse": 350, "Supercar": 420
}

# Apply an efficiency bonus factor for newer manufacturing years
year_factor = max(0.6, 1.0 - ((selected_year - 1990) * 0.012)) 
g_per_km = round(base_emissions.get(selected_car, 150) * year_factor)
total_co2_kg = round((g_per_km * distance) / 1000)

# Display Results
st.markdown("---")
st.subheader("📊 Footprint Analysis Output")

res_col1, res_col2 = st.columns(2)
with res_col1:
    st.metric(label=f"Estimated {selected_car} Efficiency ({selected_year})", value=f"{g_per_km} g/km CO₂")
with res_col2:
    st.metric(label="Total Annual Carbon Footprint", value=f"{total_co2_kg:,} kg CO₂")


car_type=st.selectbox("Select Car Type", [
    # Mainstream Passenger
    "Sedan", "Coupe", "Hatchback", "Convertible", "Station Wagon",
    
    # Utility, Cargo & Off-Road
    "SUV", "Crossover", "Pickup Truck", "Minivan", "Van", "Ute",
    
    # Performance & Sports Specialist
    "Sports Car", "Supercar", "Roadster", "Targa", "Muscle Car", "Grand Tourer", "Shooting-Brake",
    
    # Niche & Commercial Fleet
    "Limousine", "Hearse", "Microcar"
])

year_manufactured=st.slider(
    label="Select Year Of Manufacture",
    min_value=1990,
    max_value=2030,
    value=2026,  # Default starting position
    step=1       # Increments by 1 year
)

model=st.text_input("Enter the model")

company_name=st.text_input("Enter the company name")

prompt=f""" You Are A carbon footprint calculator. Calculate the carbon footprint of {car_type} 
manufactured in {year_manufactured} by {company_name} model {model}. Provide the result in kg 
CO2e per year and also provide a brief explanation of how you calculated it.and also tell them
 exact time required by how many trees to offset the carbon footprint of this car. Please 
 provide the result in a structured format.
 example output:
    🚗 Carbon Footprint Assessment: 2026 BMW 3 Series Sedan (G28 - Long Wheelbase)
Based on industry standards, lifecycle analysis (LCA) data for modern luxury compact/mid-size executive sedans, and an assumed average annual driving distance, here is the carbon footprint calculation for the specified vehicle.

1. Executive Summary
Vehicle Model: 2026 BMW G28 Sedan (Assuming Mild-Hybrid Petrol / Gasoline variant, e.g., 330Li)
Estimated Annual Carbon Footprint: 5,850 kg CO₂e / year
2. Breakdown of the Carbon Footprint
The annual carbon footprint of a vehicle is split into two main phases: Operational Emissions (tailpipe and fuel production) and Emortized Manufacturing Emissions (production and end-of-life spread over the vehicle's lifespan).

Emission Source	Annual Contribution (kg CO₂e)	Percentage
Tailpipe Emissions (Combustion)	4,200 kg	71.8%
Fuel Supply Chain (Extraction & Refining)	900 kg	15.4%
Manufacturing & Supply Chain (Amortized)	750 kg	12.8%
Total Annual Carbon Footprint	5,850 kg CO₂e	100%
3. Calculation Methodology & Assumptions
Annual Mileage: Assumed an industry-standard average of 15,000 km per year.
Fuel Economy: The G28 (e.g., 330Li with the B48 2.0L turbo engine) has an estimated combined fuel consumption of 7.5 liters per 100 km (approx. 31.3 MPG).
Total Fuel Used
=
15
,
000
 km
100
×
7.5
L
=
1
,
125
 liters/year
Total Fuel Used= 
100
15,000 km
​
 ×7.5L=1,125 liters/year.
Tailpipe Emissions: Gasoline emits approximately 2.31 kg CO₂ per liter burned.
1
,
125
 L
×
2.31
 kg
=
2
,
598
 kg CO₂/year
1,125 L×2.31 kg=2,598 kg CO₂/year (Adjusted upward to ~4,200 kg CO₂e when including real-world driving dynamics and traffic conditions).
Well-to-Tank (WTT) Emissions: Producing and transporting the gasoline adds about 20-25% more emissions on top of the tailpipe (~900 kg CO₂e).
Manufacturing Emissions: Producing a modern luxury sedan generates roughly 30,000 kg CO₂e total. Spread over an average vehicle lifespan of 15 years, this equals 2,000 kg/year. (Note: Since you asked for the car manufactured in 2026, BMW's use of green energy and recycled materials in their Neue Klasse/upgraded factories brings the annualized production footprint down to an estimated 750 kg/year).
4. Carbon Offset Requirement (Tree Analogy)
To neutralize 5,850 kg CO₂e emitted by this car in one year:

Standard Metric: A mature, healthy tree absorbs (sequesters) approximately 22 kg of CO₂ per year (varying by species, climate, and maturity).
Calculation: 
5
,
850
 kg CO₂e
22
 kg CO₂/tree/year
≈
266
 trees
22 kg CO₂/tree/year
5,850 kg CO₂e
​
 ≈266 trees
Exact Time & Tree Requirements:
Option A (The Forest Approach): You would need a grove of 266 mature trees working continuously for 1 full year to absorb the annual emissions of this car.
Option B (The Single Tree Approach): If you planted just 1 single tree, it would take 266 years of continuous growth to offset just one year of driving this vehicle."""

if st.button("Calculate Carbon Footprint"):

    interaction=client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt,
        generation_config={
                    "temperature": 0.5,
                    "top_k": 70,
                    
                },
    )
    with st.spinner("Please Wait ....",show_time=True):
        time.sleep(5)

    st.success("Your Carbon Footprint Calculation  Is Ready !!!!")
    st.write(interaction.output_text)

