import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import math
import numpy as np
from PIL import Image, ImageOps  # Added for image resizing
import graphviz

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
icon_image = Image.open("logo.png")
st.set_page_config(
    page_title="Camden Strategy Framework",
    page_icon=icon_image,
    layout="wide",
    initial_sidebar_state="collapsed", # Collapsed gives more room for the presentation
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Camden Borough Protection Strategy Presentation"
    }
)

# -----------------------------------------------------------------------------
# 2. GLOBAL STYLING & THEME
# -----------------------------------------------------------------------------

# Define a color palette for use in Python charts later
THEME = {
    "primary": "#0e1b3c",    # Camden Navy
    "accent": "#d92828",     # Alert Red
    "background": "#ffffff",
    "text": "#0E1117",
    "secondary_text": "#5d6d7e"
}

st.markdown(f"""
    <style>
    /* Import a clean, professional font */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Roboto', sans-serif;
    }}

    /* Remove top padding to maximize screen real estate for presentation */
    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}

    /* Headings */
    h1, h2, h3 {{
        color: {THEME['primary']};
        font-weight: 700;
    }}

    /* Professional Alert/Info Boxes */
    .stAlert {{
        background-color: #f8f9fa;
        border-left: 5px solid {THEME['primary']};
        border-radius: 4px;
    }}

    /* Remove Streamlit Branding for clean presentation mode */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* Custom Tab styling to look like folders */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0px 0px;
        color: {THEME['primary']};
        font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {THEME['primary']};
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. HELPER FUNCTIONS & DATA LOADING
# -----------------------------------------------------------------------------

def check_system_integrity():
    """
    Verifies that all critical assets (Data and Images) are present.
    Stops execution with a polished error message if critical data is missing.
    """
    # Required assets
    required_images = [f"{i}.png" for i in range(1, 9)] # Added 8.png for logo
    required_data = ["data.csv"]
    
    # Check Data (Critical)
    missing_data = [f for f in required_data if not os.path.exists(f)]
    if missing_data:
        st.error(f"⛔ **CRITICAL ERROR: System Data Missing**\n\nThe following core files could not be found: `{', '.join(missing_data)}`")
        st.stop()

    # Check Images (Non-critical, but warn)
    missing_images = [f for f in required_images if not os.path.exists(f)]
    if missing_images:
        st.warning(f"⚠️ **Asset Warning:** Some visual assets are missing: `{', '.join(missing_images)}`. Placeholders will be used.")

# Run integrity check immediately
check_system_integrity()

@st.cache_resource
def load_and_resize_image(image_path, size=(600, 400)):
    """
    Loads, resizes, and caches an image.
    Returns None if image is not found, preventing crashes.
    """
    if os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            # High-quality resampling for professional look
            img = ImageOps.fit(img, size, Image.Resampling.LANCZOS) 
            return img
        except Exception as e:
            st.error(f"Error loading image {image_path}: {e}")
            return None
    return None

@st.cache_data
def load_data():
    """
    Loads the dataset with error handling.
    """
    try:
        df = pd.read_csv("data.csv")
        # Optional: Convert standard date columns if they exist to datetime objects
        # if 'date' in df.columns:
        #     df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        st.error(f"⛔ **Data Load Error:** Could not read `data.csv`. \n\nError details: {e}")
        st.stop()

# Load data into session
df_incidents = load_data()


# # -----------------------------------------------------------------------------
# # 3. TITLE SLIDE - OPTIMIZED LAYOUT
# # -----------------------------------------------------------------------------

# # 1. Custom CSS for Bolder Text and Title Box
# st.markdown("""
#     <style>
#     /* --- TITLE BOX STYLING --- */
#     .header-box {
#         background-color: #0e1b3c; /* Camden Navy */
#         padding: 30px;
#         border-radius: 10px;
#         border-left: 12px solid #d92828; /* Red Accent */
#         color: white;
#         text-align: center; /* CHANGED TO CENTER */
#         box-shadow: 0px 6px 10px rgba(0,0,0,0.2);
#         /* Ensure box fills height to match logo visual weight */
#         height: 100%;
#         display: flex;
#         flex-direction: column;
#         justify-content: center;
#         align-items: center; /* Centers items horizontally in flex container */
#     }
    
#     /* Large Title Font */
#     .header-title {
#         font-size: 42px !important;
#         font-weight: 800;
#         font-family: 'Helvetica Neue', 'Arial', sans-serif;
#         margin-bottom: 10px;
#         line-height: 1.1;
#     }
    
#     /* Subtitle Font */
#     .header-subtitle {
#         font-size: 22px !important;
#         font-weight: 400;
#         color: #e0e0e0;
#         margin: 0;
#     }

#     /* --- BODY TEXT STYLING (Make it Bolder) --- */
    
#     /* Make standard paragraphs darker and heavier */
#     .stMarkdown p {
#         font-size: 18px !important;
#         font-weight: 500 !important; /* 500 is semi-bold */
#         color: #000000 !important;   /* Pure black for contrast */
#         line-height: 1.6;
#     }
    
#     /* Make bullet points darker */
#     .stMarkdown li {
#         font-size: 18px !important;
#         font-weight: 500 !important;
#         color: #000000 !important;
#     }
    
#     /* Make Headers pop */
#     h3 {
#         font-weight: 800 !important;
#         color: #0e1b3c !important;
#     }
#     h4 {
#         font-weight: 700 !important;
#         color: #d92828 !important; /* Red accent for smaller headers */
#     }
#     </style>
# """, unsafe_allow_html=True)

# # 2. Create the Layout [1, 3]
# col_logo, col_title = st.columns([1, 3], gap="medium", vertical_alignment="center")

# with col_logo:
#     # Replace "8.png" with your actual image path
#     st.image("8.png", use_container_width=True)

# with col_title:
#     st.markdown("""
#         <div class="header-box">
#             <div class="header-title">Turning Threat into Opportunity:</div>
#             <div class="header-title">A Protection Strategy for Camden</div>
#             <div class="header-subtitle">Short, Medium, and Long-Term Strategic Planning Framework</div>
#         </div>
#     """, unsafe_allow_html=True)

# st.markdown("---")
import streamlit as st

# -----------------------------------------------------------------------------
# 3. TITLE SLIDE - OPTIMIZED LAYOUT
# -----------------------------------------------------------------------------

# 1. Custom CSS for Bolder Text, Title Box, and Recipient Note
st.markdown("""
    <style>
    /* --- TITLE BOX STYLING --- */
    .header-box {
        background-color: #0e1b3c; /* Camden Navy */
        padding: 30px;
        border-radius: 10px;
        border-left: 12px solid #d92828; /* Red Accent */
        color: white;
        text-align: center;
        box-shadow: 0px 6px 10px rgba(0,0,0,0.2);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    /* Large Title Font */
    .header-title {
        font-size: 42px !important;
        font-weight: 800;
        font-family: 'Helvetica Neue', 'Arial', sans-serif;
        margin-bottom: 10px;
        line-height: 1.1;
    }
    
    /* Subtitle Font */
    .header-subtitle {
        font-size: 22px !important;
        font-weight: 400;
        color: #e0e0e0;
        margin: 0;
    }

    /* --- RECIPIENT DESIGNATION STYLING (New) --- */
    .recipient-box {
        margin-top: 20px;       /* Space between title and this note */
        padding: 15px;
        background-color: #f4f4f4; /* Very light grey for subtlety */
        border-left: 6px solid #0e1b3c; /* Matching Navy Accent */
        border-radius: 4px;
        font-family: 'Georgia', 'Times New Roman', serif; /* Serif font for formality */
        font-size: 16px;
        color: #333;
        text-align: center;
        font-style: italic;
    }

    .recipient-name {
        font-weight: 700;
        color: #0e1b3c;
        font-style: normal; /* Keep the name non-italic for emphasis */
    }

    /* --- BODY TEXT STYLING --- */
    .stMarkdown p {
        font-size: 18px !important;
        font-weight: 500 !important;
        color: #000000 !important;
        line-height: 1.6;
    }
    
    .stMarkdown li {
        font-size: 18px !important;
        font-weight: 500 !important;
        color: #000000 !important;
    }
    
    h3 {
        font-weight: 800 !important;
        color: #0e1b3c !important;
    }
    h4 {
        font-weight: 700 !important;
        color: #d92828 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Create the Layout [1, 3]
col_logo, col_title = st.columns([1, 3], gap="medium", vertical_alignment="center")

with col_logo:
    # Replace "8.png" with your actual image path
    st.image("8.png", use_container_width=True)

with col_title:
    st.markdown("""
        <div class="header-box">
            <div class="header-title">Turning Problem into Opportunity:</div>
            <div class="header-title">A Protection Strategy for Camden</div>
            <div class="header-subtitle">Short, Medium, and Long-Term Strategic Planning Framework</div>
        </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# NEW SECTION: STRATEGIC CONTEXT (Formatted Professional Text)
# -----------------------------------------------------------------------------
st.subheader("📌 Strategic Context & Rationale")

# Intro Paragraph (Full Width)
st.write(
    """
    Camden has a significant opportunity to set a positive example among London boroughs by tackling a challenge 
    that requires not only local action but also the attention of central government and the Mayor of London. 
    **Current police data consistently ranks Camden among the highest boroughs for drug-related activity**, 
    creating an urgent need for a specialist approach.
    """
)

# Split the analysis into two columns for better readability
ctx_col1, ctx_col2 = st.columns(2, gap="large")

with ctx_col1:
    st.markdown("#### The Operational Gap")
    st.write(
        """
        Despite increased police deployment and a stronger on-street presence over the past year, 
        Camden remains at the top of crime rankings. This indicates a critical disconnect:
        
        * **Effort vs. Impact:** Operational efforts have increased, but results have plateaued.
        * **Missing Framework:** Tactical enforcement has not been supported by a sufficiently robust, 
            data-driven strategic framework.
        """
    )

with ctx_col2:
    st.markdown("#### The Catalyst: Transport Hubs")
    st.write(
        """
        Research highlights that the primary driver of Camden’s persistent challenge is its proximity to 
        major international and national transport hubs:
        
        * **St Pancras International & King’s Cross Station**
        * These hubs offer seamless "in-and-out" access for individuals from across the UK and Europe.
        * This high mobility enables offenders to conduct illicit activity and return home the same day, 
            drastically increasing the complexity of local enforcement.
        """
    )

# The Proposal / Solution (Highlighted in a box)
st.success(
    "**The Proposal:** This plan aims to develop a comprehensive protection strategy—structured across "
    "**one-year, three-year, and five-year plans**—that will not only reduce drug-related activity in "
    "Camden but also create a repeatable model that other London boroughs can adopt."
)

st.caption("Please refer to the accompanying map and station-area analysis for further context.")

# # -----------------------------------------------------------------------------
# # 3. Executive Summary Content (Existing)
# # -----------------------------------------------------------------------------
# st.markdown("---")
# st.subheader("📋 Executive Summary")

# col1, col2 = st.columns(2, gap="large")

# with col1:
#     st.markdown("**The Strategic Challenge**")
#     st.write(
#         """
#         Camden faces a critical opportunity to lead London in public safety. 
#         Current data indicates that despite increased police presence, 
#         **Camden remains a top-ranking borough for drug dealing offenses.** This persistence suggests that tactical deployment alone is insufficient 
#         and a robust strategic overhaul is required.
#         """
#     )
#     # Using warning/info box for emphasis
#     st.info(
#         "**Meeting Objective:** Develop a comprehensive **1-3-5 Year Plan** "
#         "to tackle local issues and establish a blueprint for cross-borough learning."
#     )

# with col2:
#     st.markdown("**Key Driver: Transport Infrastructure**")
#     st.write(
#         """
#         Our analysis identifies a primary structural catalyst for this issue:
#         **Proximity to Major Transport Hubs.**
#         """
#     )
#     st.markdown("""
#     * 🚄 **St Pancras International**
#     * 🚆 **King's Cross Station**
#     """)
#     st.caption(
#         "These hubs facilitate rapid 'in-and-out' access for offenders from across "
#         "the UK and Europe."
#     )

# st.markdown("---")
# -----------------------------------------------------------------------------
# 4. INTERACTIVE STATION MAP (The Triangle)
# -----------------------------------------------------------------------------
st.header("📍 The Critical Transport Triangle")

# Layout: Map on the left, Details on the right
col_map, col_info = st.columns([1.2, 1])

with col_map:
    st.image("5.png", use_container_width=True, caption="Map of Key Transport Hubs")
    st.caption("👇 Select a station to view passenger statistics and details.")
    
    # Interactive selection
    station_selector = st.radio(
        "Select Location to Inspect:",
        ["St Pancras International", "Kings Cross Station", "Camden Town Station"],
        horizontal=True
    )

with col_info:
    st.markdown(f"### {station_selector}")
    
    if station_selector == "St Pancras International":
        st.image("1.png", use_container_width=True)
        st.metric(label="Yearly Usage", value="35,959,980", delta="High Volume")
        st.info("International trains: It’s the London terminal for the Eurostar, which runs high-speed trains to Paris, Brussels, Amsterdam, and other destinations in Europe.")

    elif station_selector == "Kings Cross Station":
        st.image("2.png", use_container_width=True)
        st.metric(label="Yearly Usage", value="24,483,824", delta="Major Interchange")
        st.info("Major UK rail hub: Trains from King’s Cross go mainly to the north and east of England, including: York, Newcastle, Leeds, Edinburgh (Scotland), and Other destinations along the East Coast Main Line.")

#     elif station_selector == "Camden Town Station":
#         st.image("3.png", use_container_width=True)
        
#         # Growth Chart Data
#         growth_data = pd.DataFrame({
#             "Year": ["2020", "2021", "2022", "2023"],
#             "Passengers (Millions)": [5.51, 9.12, 17.34, 18.81]
#         })
        
#         # Area Chart for Growth
#         fig_growth = px.area(
#             growth_data, 
#             x="Year", 
#             y="Passengers (Millions)", 
#             title="📈 Explosive Passenger Growth",
#             markers=True,
#             color_discrete_sequence=['#1f77b4']  # Standard Blue
#         )
#         fig_growth.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
#         st.plotly_chart(fig_growth, use_container_width=True)
#         st.info("Major UK rail hub: Trains from King’s Cross go mainly to the north and east of England, including: York, Newcastle, Leeds, Edinburgh (Scotland), and Other destinations along the East Coast Main Line.")
# st.markdown("---")
    # elif station_selector == "Camden Town Station":
    #     st.image("3.png", use_container_width=True)
        
    #     # --- CUSTOM COLORED CHART LOGIC ---
        
    #     fig_growth = go.Figure()

    #     # 1. Blue Segment (2020 to 2021)
    #     fig_growth.add_trace(go.Scatter(
    #         x=["2020", "2021"],
    #         y=[5.51, 9.12],
    #         mode='lines+markers',
    #         fill='tozeroy',  # Fills area to x-axis
    #         line=dict(color='#1f77b4', width=3), # Blue
    #         name="Recovery"
    #     ))

    #     # 2. Yellow Segment (2021 to 2022)
    #     fig_growth.add_trace(go.Scatter(
    #         x=["2021", "2022"],
    #         y=[9.12, 17.34],
    #         mode='lines+markers',
    #         fill='tozeroy',
    #         line=dict(color='#f1c40f', width=3), # Warning Yellow
    #         name="Growth"
    #     ))

    #     # 3. Red Segment (2022 to 2023)
    #     fig_growth.add_trace(go.Scatter(
    #         x=["2022", "2023"],
    #         y=[17.34, 18.81],
    #         mode='lines+markers',
    #         fill='tozeroy',
    #         line=dict(color='#d92828', width=3), # Danger Red
    #         name="High Traffic"
    #     ))

    #     # Update Layout to lock X-Axis and styling
    #     fig_growth.update_layout(
    #         title="📈 Explosive Passenger Growth",
    #         height=300,
    #         margin=dict(l=0, r=0, t=30, b=0),
    #         showlegend=False, # Hide legend to keep it clean
    #         xaxis=dict(
    #             tickmode='array', # Forces Plotly to use only the ticks we provide
    #             tickvals=["2020", "2021", "2022", "2023"], # Exact labels
    #             showgrid=False
    #         ),
    #         yaxis=dict(
    #             title="Passengers (Millions)",
    #             showgrid=True,
    #             gridcolor='#f0f0f0'
    #         )
    #     )

    #     st.plotly_chart(fig_growth, use_container_width=True)
    elif station_selector == "Camden Town Station":
        st.image("3.png", use_container_width=True)
        
        # --- CUSTOM COLORED CHART LOGIC ---
        
        fig_growth = go.Figure()

        # 1. Blue Segment (2020 to 2021)
        fig_growth.add_trace(go.Scatter(
            x=["2020", "2021"],
            y=[5.51, 9.12],
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color='#1f77b4', width=3), # Blue
            name="Recovery"
        ))

        # 2. Yellow Segment (2021 to 2022)
        fig_growth.add_trace(go.Scatter(
            x=["2021", "2022"],
            y=[9.12, 17.34],
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color='#f1c40f', width=3), # Warning Yellow
            name="Growth"
        ))

        # 3. Red Segment (2022 to 2023)
        fig_growth.add_trace(go.Scatter(
            x=["2022", "2023"],
            y=[17.34, 18.81],
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color='#d92828', width=3), # Danger Red
            name="High Traffic"
        ))

        # Update Layout: Added 'annotations' section below
        fig_growth.update_layout(
            title="📈 Explosive Passenger Growth",
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            showlegend=False,
            xaxis=dict(
                tickmode='array',
                tickvals=["2020", "2021", "2022", "2023"],
                showgrid=False
            ),
            yaxis=dict(
                title="Passengers (Millions)",
                showgrid=True,
                gridcolor='#f0f0f0'
            ),
            # --- NEW CODE STARTS HERE ---
            annotations=[
                # Blue Part Label (Anchored to 2020 value)
                dict(
                    x="2020", y=5.51,
                    text="<b>Over 5 Million</b>",
                    showarrow=True,
                    arrowhead=2,
                    ax=0, ay=-40, # Moves text up 40px
                    font=dict(color='#1f77b4') # Matches Blue line
                ),
                # Yellow Part Label (Anchored to 2021 value)
                dict(
                    x="2021", y=9.12,
                    text="<b>Over 9 Million</b>",
                    showarrow=True,
                    arrowhead=2,
                    ax=0, ay=-40,
                    font=dict(color='#f1c40f') # Matches Yellow line (darker for readability)
                ),
                                # Red Part Label (Anchored to 2023 value)
                dict(
                    x="2022", y=17.34,
                    text="<b>Over 17 Million</b>",
                    showarrow=True,
                    arrowhead=2,
                    ax=0, ay=-30,
                    font=dict(color='#d92828') # Matches Red line
                ),
            
                # Red Part Label (Anchored to 2023 value)
                dict(
                    x="2023", y=18.81,
                    text="<b>Over 18 Million</b>",
                    showarrow=True,
                    arrowhead=2,
                    ax=0, ay=-30,
                    font=dict(color='#d92828') # Matches Red line
                )
            ]
            # --- NEW CODE ENDS HERE ---
        )

        st.plotly_chart(fig_growth, use_container_width=True)
        
        st.info("According to CrystalRoof, the annual crime rate in the area around Camden Town Underground Station (Oct 2024–Sept 2025) is 1,597 crimes per 1,000 resident population. That’s very high by their scale.")

    st.markdown("---")
# -----------------------------------------------------------------------------
# 5. MARKET CONTEXT
# -----------------------------------------------------------------------------
st.header("🛍️ Inverness Street Market")

col_mkt_img, col_mkt_text = st.columns([1, 1])

with col_mkt_img:
    st.image("4.png", use_container_width=True, caption="Inverness Street Market")

with col_mkt_text:
    st.markdown("#### The Commerce-Crime Nexus")
    st.metric("Yearly Visitors", "14,000,000", delta="High Density Area")
    st.write("""
    According to CrystalRoof, for the postcode around Inverness Street (NW1 7HB) the estimated annual drug-crime rate is 139 per 1,000 (very high).    
    Business owners in Inverness Street (market traders, restaurants, cafés) have publicly complained that open drug dealing is “persistent” and part of a “nuisance” problem.
    """)

st.markdown("---")

# -----------------------------------------------------------------------------
# 6. EVIDENCE & POLICING CHALLENGES
# -----------------------------------------------------------------------------
import base64

# Function to load image and convert to base64 so it can be used in HTML
def get_img_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 1. Convert your image
img_str = get_img_as_base64("ju.png")

# 2. Render Header with Inline Image
st.markdown(f"""
    <h2 style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{img_str}" 
             style="width: 40px; height: 40px; margin-right: 10px; border-radius: 5px;">
        The Evidence Challenge
    </h2>
    """, unsafe_allow_html=True)

col_cctv, col_find = st.columns(2)
import base64

# Function to load image and convert to base64 so it can be used in HTML
def get_img_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 1. Convert your image
img_str = get_img_as_base64("ju.png")

# 2. Render Header with Inline Image
st.markdown(f"""
    <h2 style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{img_str}" 
             style="width: 40px; height: 40px; margin-right: 10px; border-radius: 5px;">
        The Evidence Challenge
    </h2>
    """, unsafe_allow_html=True)
# Using the resize function to ensure images match perfectly in height/aspect
img_exchange = load_and_resize_image("6.png")
img_drugs = load_and_resize_image("7.png")

with col_cctv:
    st.subheader("1. The Requirement")
    if img_exchange:
        st.image(img_exchange, use_container_width=True, caption="Hand-to-Hand Exchange")
    st.success("""
    **Actionable Evidence:**
    Police require clear footage of a **hand-to-hand exchange** (money for drugs).
    """)

with col_find:
    st.subheader("2. The Problem")
    if img_drugs:
        st.image(img_drugs, use_container_width=True, caption="Drugs Found in Bin")
    st.error("""
    **Insufficient Evidence:**
    Finding drugs in bins or on the ground is **not enough** without linking possession to a suspect.
    """)

st.markdown("---")

# -----------------------------------------------------------------------------
# 7. ECONOMIC SCALE (Imports vs Drugs)
# -----------------------------------------------------------------------------
st.header("💷 Economic Scale: Legal Imports vs. Illicit Market")

# Initialize session state for the reveal button if not present
if 'reveal_drug_market' not in st.session_state:
    st.session_state['reveal_drug_market'] = False

# Base Data (Legal Commodities)
import_data = [
    {"Commodity": "Mineral Fuels", "Value": 8.7, "Type": "Legal"},
    {"Commodity": "Mechanical Appliances", "Value": 6.4, "Type": "Legal"},
    {"Commodity": "Electronic Equipment", "Value": 5.3, "Type": "Legal"},
    {"Commodity": "Precious Metals", "Value": 4.2, "Type": "Legal"},
    {"Commodity": "Motor Vehicles", "Value": 4.1, "Type": "Legal"},
    {"Commodity": "Pharmaceuticals", "Value": 2.0, "Type": "Legal"}, # Shortened name for better vertical fit
    {"Commodity": "Other Products", "Value": 1.6, "Type": "Legal"},
    {"Commodity": "Plastics", "Value": 1.5, "Type": "Legal"},
    {"Commodity": "Measuring Devices", "Value": 1.3, "Type": "Legal"},
    {"Commodity": "Knitwear", "Value": 1.3, "Type": "Legal"}
]

df_imports = pd.DataFrame(import_data)

# 1. Handle Reveal Logic
if st.session_state['reveal_drug_market']:
    # Add Illicit Drugs to DataFrame
    new_row = pd.DataFrame([{"Commodity": "Illicit Drugs", "Value": 9.4, "Type": "Illegal"}])
    df_imports = pd.concat([df_imports, new_row], ignore_index=True)

# 2. Sort by Value Descending (Highest on Left)
df_imports = df_imports.sort_values("Value", ascending=False)

# Define Colors
colors = {"Legal": "#1f77b4", "Illegal": "#DC3912"}

# 3. Build Chart (Vertical)
# Note: We swapped x and y. x is now Commodity, y is Value.
fig_imports = px.bar(
    df_imports,
    x="Commodity", 
    y="Value", 
    color="Type", 
    color_discrete_map=colors, 
    text="Value",
    title="<b>Top UK Commodities vs. Illicit Drugs Market (£ Billions)</b>",
)

# 4. Apply Styling (Thicker, Bolder, Larger)
fig_imports.update_layout(
    showlegend=False, 
    height=600, # Increased height for vertical breathing room
    bargap=0.15, # <--- This makes columns THICKER by reducing the gap between them
    
    # Global Font Settings
    font=dict(
        family="Arial, sans-serif",
        size=14,  # Base font size increased
        color="black"
    ),
    
    # X-Axis Styling (The Categories)
    xaxis=dict(
        title=None,
        tickfont=dict(
            size=14, 
            family="Arial Black" # Bold font for labels
        ),
        tickangle=-45 # Angle labels to prevent overlapping
    ),
    
    # Y-Axis Styling (The Numbers)
    yaxis=dict(
        title=dict(text="<b>Value (£ Billions)</b>", font=dict(size=16)),
        tickfont=dict(size=14),
        showgrid=True,
        gridcolor='lightgray'
    )
)

# 5. Update Bar Text (The numbers on top of bars)
fig_imports.update_traces(
    texttemplate='<b>£%{text}B</b>', # <b> tag makes it bold
    textposition='outside',
    textfont=dict(
        size=18, # Significantly larger
        family="Arial Black"
    ),
    cliponaxis=False # Ensures top labels don't get cut off
)

# Render Chart
st.plotly_chart(fig_imports, use_container_width=True)

# Render Button
col_btn, col_space = st.columns([1, 4])
with col_btn:
    if not st.session_state['reveal_drug_market']:
        if st.button("⚠️ Reveal Illicit Market Scale"):
            st.session_state['reveal_drug_market'] = True
            st.rerun()
    else:
        if st.button("Reset Chart"):
            st.session_state['reveal_drug_market'] = False
            st.rerun()
url = "https://www.independent.co.uk/news/uk/crime/russia-war-money-laundering-uk-operation-destabilise-keremet-b2869448.html"

st.markdown(f"""
    <a href="{url}" target="_blank" style="text-decoration: none;">
        <div style="
            padding: 20px;
            background-color: #fdfdfd;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            border-left: 10px solid #d92828; /* Matching your Red Accent */
            box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        ">
            <div style="
                color: #555; 
                font-size: 12px; 
                font-weight: 600; 
                text-transform: uppercase; 
                letter-spacing: 1px; 
                margin-bottom: 8px;
            ">
                📰 Related Intelligence / Media Report
            </div>
            <div style="
                color: #0e1b3c; /* Matching your Camden Navy */
                font-size: 20px; 
                font-weight: 700; 
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                line-height: 1.4;
                margin-bottom: 10px;
            ">
                How billion-dollar money laundering network in UK ‘bought bank to fund Russian war effort’
            </div>
            <div style="
                color: #d92828; 
                font-size: 14px; 
                font-weight: 600;
            ">
                Read full article on The Independent &rarr;
            </div>
        </div>
    </a>
""", unsafe_allow_html=True)
st.markdown("---")

# -----------------------------------------------------------------------------
# 8. ADVANCED INCIDENT ANALYSIS
# -----------------------------------------------------------------------------
st.header("📊 Incidents by Location and Type (Top 20 Locations)")

if not df_incidents.empty:
    # 1. Calculate Totals to find the ACTUAL Top 20
    # Sort Ascending so .tail(20) grabs the largest values
    location_totals = df_incidents.groupby("Location")["Count"].sum().sort_values(ascending=True)
    
    # 2. Get Top 20 Locations
    top_locations = location_totals.tail(20).index.tolist()
    
    # 3. Filter main dataframe
    df_filtered = df_incidents[df_incidents["Location"].isin(top_locations)]
    
    # 4. Custom Color Map (Kept as requested)
    custom_colors = {
        "Drug Users/Dealers": "#DC3912",  # Red
        "Youths": "#FF9900",              # Orange
        "Noise": "#3366CC",               # Blue
        "Rough Sleeper": "#109618",       # Green
        "Smoking": "#990099",             # Purple
        "Loitering": "#0099C6",           # Teal
        "Public Indecency": "#DD4477",    # Pink
        "Intruder": "#AAAA11",            # Olive
        "Drinking/Drunk": "#66AA00"       # Light Green
    }

    # 5. Create Chart
    fig_advanced = px.bar(
        df_filtered,
        x="Count",
        y="Location",
        color="Category",
        orientation='h',
        text="Count", # This adds the number inside the bar
        title=f"<b>Total Incidents: {df_incidents['Count'].sum()}</b>", # Bold Title
        color_discrete_map=custom_colors,
        # Ensure the largest bars are at the top visual position
        category_orders={"Location": top_locations} 
    )

    # 6. Advanced Styling
    fig_advanced.update_layout(
        height=800, # Taller to accommodate thicker bars
        bargap=0.15, # <--- This makes the columns/bars THICKER (closer to 0 is thicker)
        barmode='stack', # Ensures bars collapse when items are removed via legend
        
        # Legend Styling
        legend_title_text="<b>Incident Type</b>",
        legend=dict(
            yanchor="top", 
            y=1, 
            xanchor="left", 
            x=1.01,
            font=dict(size=14)
        ),
        
        # Global Font
        font=dict(family="Arial", size=14, color="black"),
        
        # X-Axis (Numbers)
        xaxis=dict(
            title="<b>Number of Incidents</b>",
            tickfont=dict(size=14, family="Arial Black"),
            showgrid=True, 
            gridcolor='lightgray'
        ),
        
        # Y-Axis (Locations)
        yaxis=dict(
            title=None, # Remove "Location" label as it's obvious
            tickfont=dict(
                size=15, 
                family="Arial Black" # Very bold labels for readability
            )
        )
    )
    
    # 7. Style the numbers inside the bars
    fig_advanced.update_traces(
        texttemplate='%{text}', 
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial Black",
            size=14,
            color="white" # White text on colored bars for contrast
        )
    )
    
    st.plotly_chart(fig_advanced, use_container_width=True)
else:
    st.warning("No data available for analysis.")

st.write("Escalating drug-related costs for the council and rising crime rates have become a serious concern. Reports show a significant increase in resident complaints about various forms of anti-social behaviour across Camden.")
st.markdown("---")

# -----------------------------------------------------------------------------
# 9. THE VICIOUS CYCLE (INTERACTIVE & ENHANCED)
# -----------------------------------------------------------------------------


st.header("🔄 The Cycle of Supply & Local Impact")

# 1. Layout: Equal columns (1:1) and Vertically Centered
col_diagram, col_text = st.columns([1, 1], gap="large", vertical_alignment="center")

with col_diagram:
    # Initialize Graphviz
    dot = graphviz.Digraph(comment='Drug Market Cycle')
    
    # --- COMPACT GRAPH STYLING ---
    # rankdir='LR' (Left-to-Right) often fits presentations better than Top-Bottom
    # newrank='true' helps align nodes better
    dot.attr(rankdir='TB', newrank='true') 
    dot.attr(splines='curved') # Curved lines look cleaner and take less space
    dot.attr(nodesep='0.3')    # Reduce space between nodes width-wise
    dot.attr(ranksep='0.4')    # Reduce space between levels height-wise
    dot.attr(bgcolor='transparent')
    
    # Node Style (Smaller and sharper)
    dot.attr('node', shape='box', style='filled, rounded', 
             fillcolor='#0e1b3c', # Camden Navy
             fontcolor='white', 
             fontname='Arial', 
             fontsize='10',       # Smaller font
             margin='0.1,0.1',    # Tighter margins inside boxes
             height='0.4')

    # --- NODES ---
    # Using shorter labels to keep boxes small
    dot.node('A', '1. Providers')
    dot.node('B', '2. Distributors')
    dot.node('C', '3. The Market\n(Hub)')
    dot.node('D', '4. Buyers')
    dot.node('E', '5. Reinforcement')

    # Impact Node (Red)
    dot.attr('node', fillcolor='#d92828', fontcolor='white')
    dot.node('Impact', 'SOCIAL IMPACT:\nRough Sleepers,\nbeggars, thieves, \nand those involved \nin violent crime')

    # Cost Node (Yellow)
    dot.attr('node', fillcolor='#ffcc00', fontcolor='black')
    dot.node('Cost', '£ Council Costs\n& Crime Rates')

    # --- EDGES ---
    dot.attr('edge', color='#555555', arrowsize='0.6', penwidth='1.2')
    
    # Main Cycle
    dot.edge('A', 'B')
    dot.edge('B', 'C')
    dot.edge('C', 'D')
    dot.edge('D', 'E')
    dot.edge('E', 'A')

    # Consequences (Dotted)
    dot.attr('edge', style='dashed', color='#d92828')
    dot.edge('D', 'Impact')
    dot.edge('E', 'Cost')
    dot.edge('Impact', 'Cost')
    # Render with a specific height/width constraint via Streamlit
    st.graphviz_chart(dot, use_container_width=True)

with col_text:
    # --- TEXT CONTENT ---
    # This box is designed to visually balance the graph size
    st.markdown("""
    <style>
    .cycle-box {
        background-color: #f8f9fa; /* Very light grey background */
        border-radius: 8px;
        padding: 25px;
        border-left: 8px solid #0e1b3c; /* Camden Navy Accent */
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); /* Subtle shadow for depth */
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .cycle-text {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 16px;
        line-height: 1.6;
        color: #2c3e50;
        text-align: justify;
    }
    .highlight-red {
        font-weight: 600;
        color: #d92828;
    }
    .highlight-navy {
        font-weight: 700;
        color: #0e1b3c;
    }
    </style>

    <div class="cycle-box">
        <div class="cycle-text">
            <span class="highlight-navy">Drug providers</span> supply drugs to distributors, who then sell them in the market. 
            This market can attract individuals such as 
            <span class="highlight-red">rough sleepers, beggars, thieves, and those involved in violent crime</span>, 
            all seeking money to purchase drugs.
            <br><br>
            This situation places a significant <b>financial burden on the council</b>, as they must address these issues 
            and manage the negative impact on the Borough's reputation. Additionally, the growth of drug dealing in this market 
            exacerbates problems, leading to increased costs and challenges for both residents and local businesses.
        </div>
    </div>
""", unsafe_allow_html=True)


# st.header("🔄 The Cycle of Supply & Local Impact")

# # 1. Render the Static Diagram
# diagram_width = 500 

# # 1. Render the Static Diagram
# # We use 'width' instead of 'use_container_width' to control the size
# st.image("9.png", width=diagram_width)
# # 2. Professional Description Box
# st.markdown("""
#     <style>
#     .cycle-box {
#         background-color: #f8f9fa; /* Very light grey background */
#         border-radius: 8px;
#         padding: 25px;
#         border-left: 8px solid #0e1b3c; /* Camden Navy Accent */
#         box-shadow: 0 4px 6px rgba(0,0,0,0.05); /* Subtle shadow for depth */
#         margin-top: 20px;
#         margin-bottom: 20px;
#     }
#     .cycle-text {
#         font-family: 'Helvetica Neue', Arial, sans-serif;
#         font-size: 16px;
#         line-height: 1.6;
#         color: #2c3e50;
#         text-align: justify;
#     }
#     .highlight-red {
#         font-weight: 600;
#         color: #d92828;
#     }
#     .highlight-navy {
#         font-weight: 700;
#         color: #0e1b3c;
#     }
#     </style>

#     <div class="cycle-box">
#         <div class="cycle-text">
#             <span class="highlight-navy">Drug providers</span> supply drugs to distributors, who then sell them in the market. 
#             This market can attract individuals such as 
#             <span class="highlight-red">rough sleepers, beggars, thieves, and those involved in violent crime</span>, 
#             all seeking money to purchase drugs.
#             <br><br>
#             This situation places a significant <b>financial burden on the council</b>, as they must address these issues 
#             and manage the negative impact on the Borough's reputation. Additionally, the growth of drug dealing in this market 
#             exacerbates problems, leading to increased costs and challenges for both residents and local businesses.
#         </div>
#     </div>
# """, unsafe_allow_html=True)
# st.markdown("---")


# -----------------------------------------------------------------------------
# REFERENCES & DATA SOURCES BOX
# -----------------------------------------------------------------------------

st.markdown("""
<style>
.ref-box {
    background-color: #f8f9fa;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 25px;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    margin-top: 20px;
}
.ref-header {
    color: #0e1b3c;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 15px;
    border-bottom: 2px solid #d92828;
    padding-bottom: 8px;
    display: flex;
    align-items: center;
}
.ref-section-title {
    color: #0e1b3c;
    font-size: 14px;
    font-weight: 700;
    margin-top: 12px;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.ref-text {
    color: #444;
    font-size: 14px;
    line-height: 1.5;
    margin-bottom: 8px;
}
.ref-link {
    color: #d92828;
    font-weight: 600;
    text-decoration: none;
    border-bottom: 1px dotted #d92828;
    transition: all 0.2s;
}
.ref-link:hover {
    color: #0e1b3c;
    border-bottom: 1px solid #0e1b3c;
}
</style>

<div class="ref-box">
    <div class="ref-header">📚 Data Sources & Evidence Base</div>
    <div class="ref-section-title">📄 Source Document</div>
    <div class="ref-text">
        • <a href="https://lbcamden-my.sharepoint.com/personal/sam_niaraeis_camden_gov_uk/_layouts/15/doc.aspx?sourcedoc={466af313-4082-4097-b9d9-04a473c1d542}&action=edit" target="_blank" class="ref-link">Crime & Safety around Camden Town Station</a>
    </div>
</div>
""", unsafe_allow_html=True)
