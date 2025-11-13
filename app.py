import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set Plotly's default template to dark
px.defaults.template = "plotly_dark"


# --- UPDATED FUNCTION TO INJECT CUSTOM CSS ---
def inject_custom_css():
    """
    Injects custom CSS to force a dark theme for the app,
    bypassing the .streamlit/config.toml file.
    """
    custom_css = """
    <style>
        /* Main app background */
        .main .block-container {
            background-color: #0f172a;
            color: #f1f5f9;
        }
        
        /* Main app text and headers */
        body, .stApp, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, 
        .stMarkdown, .stHeader, .stSubheader, .stTabs {
            color: #f1f5f9 !important;
        }

        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color: #1e293b;
        }

        /* Sidebar text */
        [data-testid="stSidebar"] .stMarkdown, 
        [data-testid="stSidebar"] .stSelectbox, 
        [data-testid="stSidebar"] label {
            color: #f1f5f9;
        }

        /* --- STYLES TO FIX WIDGETS AND METRICS --- */

        /* Fix Metric numbers */
        [data-testid="stMetricValue"] {
            color: #f1f5f9;
        }
        
        /* Fix Metric labels */
        [data-testid="stMetricLabel"] {
            color: #cbd5e1 !important;
        }
        .stMetric .st-bq { /* Fallback */
            color: #cbd5e1;
        }

        /* Fix Selectbox and Multiselect backgrounds */
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
            background-color: #0f172a; /* Darker background for the widget */
            border-color: #334155;
            color: #f1f5f9;
        }
        
        /* --- NEW STYLES FOR DROPDOWN MENUS --- */

        /* Fix dropdown menus (when you click on a selectbox) */
        div[data-baseweb="popover"] ul {
             background-color: #1e293b;
        }
        
        /* Fix dropdown menu item text and background */
        div[data-baseweb="popover"] ul li,
        div[data-baseweb="popover"] ul li div[role="option"] {
            color: #f1f5f9 !important;
            background-color: #1e293b !important; /* Force background of item */
        }

        /* Fix dropdown menu item hover */
        div[data-baseweb="popover"] ul li:hover {
            background-color: #334155 !important;
        }
        
        /* --- END NEW DROPDOWN STYLES --- */

        /* Fix multiselect tags (the red boxes) */
        [data-testid="stTag"] {
            background-color: #334155;
            color: #f1f5f9;
            border: none;
        }
        /* Fix the 'x' in the multiselect tag */
        [data-testid="stTag"] svg {
            fill: #f1f5f9;
        }
        
        /* Tab labels */
        .stTabs [data-baseweb="tab"] {
            color: #cbd5e1;
        }

        /* Selected tab */
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            color: #22a079;
        }
        
        /* Set background for the main app area (outside the centered block) */
        [data-testid="stAppViewContainer"] {
            background-color: #0f172a;
        }
        
        /* Ensure headers in the main container are also dark */
        [data-testid="stAppViewContainer"] h1,
        [data-testid="stAppViewContainer"] h2,
        [data-testid="stAppViewContainer"] h3 {
             color: #f1f5f9;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


# Set page configuration
st.set_page_config(
    page_title="GreenLens ESG Analytics",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CALL THE NEW CSS FUNCTION ---
inject_custom_css()


# Load and cache data
@st.cache_data
def load_data():
    # Using the provided CSV data
    data = pd.read_csv('greenlens_esg_dataset.csv')
    return data


# Load the data
df = load_data()

# App title and description
st.title("🌱 GreenLens ESG Analytics Dashboard")
st.markdown("""
Comprehensive analysis of Environmental, Social, and Governance performance metrics 
across companies, regions, and time periods.
""")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")

# Company selection
companies = df['company_name'].unique()
selected_company = st.sidebar.selectbox(
    "Select Company",
    companies,
    index=0
)

# Year selection
years = sorted(df['year'].unique(), reverse=True)
selected_years = st.sidebar.multiselect(
    "Select Years",
    years,
    default=years[:2]
)

# Region selection
regions = df['region'].unique()
selected_regions = st.sidebar.multiselect(
    "Select Regions",
    regions,
    default=regions
)

# Department selection
departments = df['department'].unique()
selected_departments = st.sidebar.multiselect(
    "Select Departments",
    departments,
    default=departments[:3]
)

# Filter data based on selections
filtered_df = df[
    (df['company_name'] == selected_company) &
    (df['year'].isin(selected_years)) &
    (df['region'].isin(selected_regions)) &
    (df['department'].isin(selected_departments))
    ]

# Main dashboard
if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your selection.")
else:
    # Key Metrics Overview
    st.header("📊 Key Performance Indicators")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        avg_esg = filtered_df['esg_score'].mean()
        st.metric("Average ESG Score", f"{avg_esg:.1f}")

    with col2:
        avg_emissions = filtered_df[['scope1_emissions_tco2e', 'scope2_emissions_tco2e']].sum(axis=1).mean()
        st.metric("Avg Scope 1+2 Emissions (tCO2e)", f"{avg_emissions:,.0f}")

    with col3:
        renewable_share = filtered_df['renewable_energy_share_pct'].mean()
        st.metric("Avg Renewable Energy %", f"{renewable_share:.1f}%")

    with col4:
        female_ratio = filtered_df['female_pct'].mean()
        st.metric("Avg Female Representation", f"{female_ratio:.1%}")

    with col5:
        total_emissions = filtered_df[
            ['scope1_emissions_tco2e', 'scope2_emissions_tco2e', 'scope3_emissions_tco2e']].sum().sum()
        st.metric("Total Emissions (tCO2e)", f"{total_emissions:,.0f}")

    # Tabs for different analysis sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Environmental",
        "👥 Social",
        "⚖️ Governance",
        "📅 Trends",
        "🔍 Detailed View"
    ])

    with tab1:
        st.subheader("Environmental Performance")

        # Calculate new metrics
        filtered_df = filtered_df.copy()
        filtered_df['energy_intensity'] = filtered_df['energy_consumption_mwh'] / filtered_df['production_output_units']
        filtered_df['carbon_intensity'] = (filtered_df['scope1_emissions_tco2e'] + filtered_df[
            'scope2_emissions_tco2e'] + filtered_df['scope3_emissions_tco2e']) / filtered_df['revenue_usd_m']
        filtered_df['waste_intensity'] = filtered_df['waste_generated_tonnes'] / filtered_df['production_output_units']
        filtered_df['water_intensity'] = filtered_df['water_withdrawal_m3'] / filtered_df['production_output_units']

        # Calculate weighted waste recycled percentage
        filtered_df['weighted_waste_recycled'] = filtered_df['waste_recycled_pct'] * filtered_df[
            'waste_generated_tonnes']

        # Calculate Green Efficiency Score
        # Normalize metrics to 0-1 scale for composite scoring
        filtered_df['norm_carbon_intensity'] = 1 - (
                filtered_df['carbon_intensity'] / filtered_df['carbon_intensity'].max())
        filtered_df['green_efficiency_score'] = (
                                                        filtered_df['norm_carbon_intensity'] * 0.4 +
                                                        filtered_df['renewable_energy_share_pct'] * 0.3 +
                                                        filtered_df['waste_recycled_pct'] * 0.3
                                                ) * 100

        # Environmental KPIs
        st.markdown("#### 🌍 Key Environmental Intensity Metrics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            avg_energy_intensity = filtered_df['energy_intensity'].mean()
            st.metric("Energy Intensity", f"{avg_energy_intensity:.2f} MWh/unit")

        with col2:
            avg_carbon_intensity = filtered_df['carbon_intensity'].mean()
            st.metric("Carbon Intensity", f"{avg_carbon_intensity:.1f} tCO₂e/MUSD")

        with col3:
            avg_waste_intensity = filtered_df['waste_intensity'].mean()
            st.metric("Waste Intensity", f"{avg_waste_intensity:.3f} tonnes/unit")

        with col4:
            avg_water_intensity = filtered_df['water_intensity'].mean()
            st.metric("Water Intensity", f"{avg_water_intensity:.1f} m³/unit")

        # Row 1: Energy & Carbon
        st.markdown("#### ⚡ Energy & Carbon Performance")
        col1, col2 = st.columns(2)

        with col1:
            # Energy Intensity Trend
            energy_intensity_trend = filtered_df.groupby('year')['energy_intensity'].mean().reset_index()
            fig = px.line(energy_intensity_trend, x='year', y='energy_intensity',
                          title="Energy Intensity Trend (MWh per Production Unit)",
                          markers=True)
            fig.update_layout(yaxis_title="MWh per Unit", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            # Average Emissions by Scope Over Time
            emissions_data = filtered_df.groupby('year')[
                ['scope1_emissions_tco2e', 'scope2_emissions_tco2e', 'scope3_emissions_tco2e']].mean().reset_index()
            fig = px.line(emissions_data, x='year',
                          y=['scope1_emissions_tco2e', 'scope2_emissions_tco2e', 'scope3_emissions_tco2e'],
                          title="Average Emissions by Scope Over Time")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Carbon Intensity Trend
            carbon_intensity_trend = filtered_df.groupby('year')['carbon_intensity'].mean().reset_index()
            fig = px.line(carbon_intensity_trend, x='year', y='carbon_intensity',
                          title="Carbon Intensity Trend (tCO₂e per MUSD Revenue)",
                          markers=True)
            fig.update_layout(yaxis_title="tCO₂e per MUSD", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            # Renewable Energy Share by Region
            renewable_by_region = filtered_df.groupby('region')['renewable_energy_share_pct'].mean().reset_index()
            fig = px.bar(renewable_by_region, x='region', y='renewable_energy_share_pct',
                         title="Renewable Energy Share by Region")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)



        # Row 2: Waste & Recycling
        st.markdown("#### ♻️ Waste & Recycling Performance")
        col1, col2 = st.columns(2)

        with col1:
            # Total Waste Recycled Over Time
            waste_recycled_trend = filtered_df.groupby('year')['waste_recycled_pct'].mean().reset_index()
            fig = px.line(waste_recycled_trend, x='year', y='waste_recycled_pct',
                          title="Total Waste Recycled (%) Over Time",
                          markers=True)
            fig.update_layout(yaxis_title="Waste Recycled (%)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            # Waste Intensity by Region
            waste_intensity_region = filtered_df.groupby('region')['waste_intensity'].mean().reset_index()
            fig = px.bar(waste_intensity_region, x='region', y='waste_intensity',
                         title="Waste Intensity by Region (Tonnes per Production Unit)")
            fig.update_layout(yaxis_title="Tonnes per Unit", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Departmental Waste Comparison
            dept_waste = filtered_df.groupby('department').agg({
                'waste_generated_tonnes': 'mean',
                'waste_recycled_pct': 'mean'
            }).reset_index()

            fig = go.Figure()
            # --- THEME UPDATE ---
            fig.update_layout(
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                title_font_color='#f1f5f9', legend_font_color='#f1f5f9',
                title="Departmental Waste Comparison",
                xaxis_title="Department",
                yaxis_title="Waste Generated (tonnes)",
                yaxis2=dict(title="Recycling Rate (%)", overlaying='y', side='right', range=[0, 100]),
                barmode='group'
            )
            fig.add_trace(go.Bar(name='Waste Generated (tonnes)', x=dept_waste['department'],
                                 y=dept_waste['waste_generated_tonnes'], yaxis='y'))
            fig.add_trace(go.Scatter(name='Recycling Rate (%)', x=dept_waste['department'],
                                     y=dept_waste['waste_recycled_pct'], yaxis='y2',
                                     mode='lines+markers', line=dict(color='red')))
            st.plotly_chart(fig, use_container_width=True)

            # Waste Generation vs Recycling Rate by Department
            waste_data = filtered_df.groupby('department')[
                ['waste_generated_tonnes', 'waste_recycled_pct']].mean().reset_index()
            fig = px.scatter(waste_data, x='waste_generated_tonnes', y='waste_recycled_pct',
                             size='waste_generated_tonnes', color='department',
                             title="Waste Generation vs Recycling Rate by Department")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        # Row 3: Water Usage
        st.markdown("#### 💧 Water Usage Performance")
        col1, col2 = st.columns(2)

        with col1:
            # Water Intensity Trend
            water_intensity_trend = filtered_df.groupby('year')['water_intensity'].mean().reset_index()
            fig = px.line(water_intensity_trend, x='year', y='water_intensity',
                          title="Water Intensity Trend (m³ per Production Unit)",
                          markers=True)
            fig.update_layout(yaxis_title="m³ per Unit", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            # Water Usage and Recycling Over Time
            water_data = filtered_df.groupby('year')[['water_withdrawal_m3', 'water_recycled_pct']].mean().reset_index()
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            # --- THEME UPDATE ---
            fig.update_layout(
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                title_font_color='#f1f5f9', legend_font_color='#f1f5f9',
                title="Water Usage and Recycling Over Time"
            )
            fig.add_trace(go.Scatter(x=water_data['year'], y=water_data['water_withdrawal_m3'],
                                     name="Water Withdrawal"), secondary_y=False)
            fig.add_trace(go.Scatter(x=water_data['year'], y=water_data['water_recycled_pct'],
                                     name="Water Recycled %"), secondary_y=True)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Regional Water Dependency
            regional_water = filtered_df.groupby('region').agg({
                'water_withdrawal_m3': 'mean',
                'water_recycled_pct': 'mean'
            }).reset_index()

            fig = px.scatter(regional_water, x='water_withdrawal_m3', y='water_recycled_pct',
                             size='water_withdrawal_m3', color='region',
                             title="Regional Water Dependency: Withdrawal vs Recycling",
                             hover_data=['region'])
            fig.update_layout(xaxis_title="Water Withdrawal (m³)", yaxis_title="Water Recycled (%)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        # Row 4: Combined Environmental Performance
        st.markdown("#### 🌱 Combined Environmental Performance")
        col1, col2 = st.columns(2)

        with col1:
            # Green Efficiency Score by Department
            green_score_dept = filtered_df.groupby('department')['green_efficiency_score'].mean().reset_index()
            fig = px.bar(green_score_dept, x='department', y='green_efficiency_score',
                         title="Departmental Environmental Rating (Green Efficiency Score)",
                         color='green_efficiency_score',
                         color_continuous_scale='Viridis')
            fig.update_layout(yaxis_title="Green Efficiency Score", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            # Departmental Environmental Performance Matrix
            dept_performance = filtered_df.groupby('department').agg({
                'carbon_intensity': 'mean',
                'renewable_energy_share_pct': 'mean',
                'waste_recycled_pct': 'mean',
                'green_efficiency_score': 'mean'
            }).reset_index()

            fig = px.scatter(dept_performance, x='carbon_intensity', y='green_efficiency_score',
                             size='renewable_energy_share_pct', color='department',
                             title="Departmental Performance: Carbon Intensity vs Green Score",
                             hover_data=['waste_recycled_pct'])
            fig.update_layout(xaxis_title="Carbon Intensity (tCO₂e/MUSD)",
                              yaxis_title="Green Efficiency Score", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Emissions Intensity vs ESG Score Correlation
            fig = px.scatter(filtered_df, x='carbon_intensity', y='esg_score',
                             color='region', size='revenue_usd_m',
                             title="Emissions Intensity vs ESG Score",
                             trendline="lowess",
                             hover_data=['department', 'year'])
            fig.update_layout(xaxis_title="Carbon Intensity (tCO₂e/MUSD)", yaxis_title="ESG Score", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            # Environmental Performance Over Time
            env_trends = filtered_df.groupby('year').agg({
                'green_efficiency_score': 'mean',
                'carbon_intensity': 'mean',
                'renewable_energy_share_pct': 'mean'
            }).reset_index()

            fig = make_subplots(specs=[[{"secondary_y": True}]])
            # --- THEME UPDATE ---
            fig.update_layout(
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                title_font_color='#f1f5f9', legend_font_color='#f1f5f9',
                title="Environmental Performance Trends Over Time"
            )
            fig.add_trace(go.Scatter(x=env_trends['year'], y=env_trends['green_efficiency_score'],
                                     name="Green Efficiency Score"), secondary_y=False)
            fig.add_trace(go.Scatter(x=env_trends['year'], y=env_trends['carbon_intensity'],
                                     name="Carbon Intensity"), secondary_y=True)
            fig.update_yaxes(title_text="Green Efficiency Score", secondary_y=False)
            fig.update_yaxes(title_text="Carbon Intensity", secondary_y=True)
            st.plotly_chart(fig, use_container_width=True)

        # Additional detailed analysis at the end
        with st.expander("📈 Detailed Environmental Analysis"):
            col1, col2 = st.columns(2)

            with col1:
                # Energy vs Carbon Correlation
                fig = px.scatter(filtered_df, x='energy_intensity', y='carbon_intensity',
                                 color='department', trendline="ols",
                                 title="Energy Intensity vs Carbon Intensity Correlation",
                                 hover_data=['region', 'year'])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Environmental Performance by Region - ALTERNATIVE CLEAN VERSION
                region_performance = filtered_df.groupby('region').agg({
                    'green_efficiency_score': 'mean',
                    'carbon_intensity': 'mean',
                    'renewable_energy_share_pct': 'mean',
                    'waste_recycled_pct': 'mean'
                }).reset_index()

                # Format the values
                region_performance['green_efficiency_score'] = region_performance['green_efficiency_score'].round(1)
                region_performance['carbon_intensity'] = region_performance['carbon_intensity'].round(1)
                region_performance['renewable_energy_share_pct'] = region_performance[
                    'renewable_energy_share_pct'].round(1)
                region_performance['waste_recycled_pct'] = region_performance['waste_recycled_pct'].round(1)

                # Create a grouped bar chart for better readability
                fig = go.Figure()
                # --- THEME UPDATE ---
                fig.update_layout(
                    template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                    title_font_color='#f1f5f9', legend_font_color='#f1f5f9',
                    title="Regional Environmental Performance Comparison",
                    xaxis_title="Region",
                    yaxis_title="Score (%)",
                    yaxis2=dict(
                        title="Carbon Intensity (tCO₂e/MUSD)",
                        overlaying='y',
                        side='right'
                    ),
                    barmode='group',
                    font=dict(size=12), # Color will be inherited from dark theme
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    hovermode='x unified'
                )

                # Add bars for each metric
                fig.add_trace(go.Bar(
                    name='Green Efficiency Score',
                    x=region_performance['region'],
                    y=region_performance['green_efficiency_score'],
                    marker_color='#2E8B57'
                ))

                fig.add_trace(go.Bar(
                    name='Renewable Energy %',
                    x=region_performance['region'],
                    y=region_performance['renewable_energy_share_pct'],
                    marker_color='#1E90FF'
                ))

                fig.add_trace(go.Bar(
                    name='Waste Recycled %',
                    x=region_performance['region'],
                    y=region_performance['waste_recycled_pct'],
                    marker_color='#FF8C00'
                ))

                # Add carbon intensity as a line (since it's on a different scale)
                fig.add_trace(go.Scatter(
                    name='Carbon Intensity (tCO₂e/MUSD)',
                    x=region_performance['region'],
                    y=region_performance['carbon_intensity'],
                    mode='lines+markers',
                    yaxis='y2',
                    line=dict(color='#FF4500', width=3),
                    marker=dict(size=8, color='#FF4500')
                ))
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Social Performance")

        # Calculate new social metrics
        filtered_df = filtered_df.copy()

        # Calculate male percentage for gender diversity charts
        filtered_df['male_pct'] = 1 - filtered_df['female_pct']

        # Calculate Social Well-Being Index
        filtered_df['social_well_being_index'] = (
                                                         (filtered_df['employee_engagement_score'] / 100) * 0.25 +
                                                         (1 - filtered_df['employee_turnover_pct']) * 0.25 +
                                                         filtered_df['pay_equity_ratio_female_to_male'] * 0.25 +
                                                         (filtered_df['avg_training_hours_per_employee'] / filtered_df[
                                                             'avg_training_hours_per_employee'].max()) * 0.25
                                                 ) * 100

        # Calculate Diversity & Inclusion Index
        filtered_df['diversity_inclusion_index'] = (
                                                           filtered_df['female_pct'] +
                                                           filtered_df['minority_pct'] +
                                                           filtered_df['board_gender_diversity_pct']
                                                   ) / 3 * 100

        # Social KPIs
        st.markdown("#### 👥 Key Social Metrics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            avg_engagement = filtered_df['employee_engagement_score'].mean()
            st.metric("Avg Engagement Score", f"{avg_engagement:.1f}")

        with col2:
            avg_turnover = filtered_df['employee_turnover_pct'].mean()
            st.metric("Avg Turnover Rate", f"{avg_turnover:.1%}")

        with col3:
            avg_pay_equity = filtered_df['pay_equity_ratio_female_to_male'].mean()
            st.metric("Avg Pay Equity Ratio", f"{avg_pay_equity:.3f}")

        with col4:
            social_index = filtered_df['social_well_being_index'].mean()
            st.metric("Social Well-Being Index", f"{social_index:.1f}")

        # Section 1: Workforce Diversity & Inclusion
        st.markdown("#### 🌈 Workforce Diversity & Inclusion")
        col1, col2 = st.columns(2)

        with col1:
            # Gender Diversity by Department
            gender_by_dept = filtered_df.groupby('department').agg({
                'female_pct': 'mean',
                'male_pct': 'mean'
            }).reset_index()

            fig = px.bar(gender_by_dept, x='department', y=['female_pct', 'male_pct'],
                         title="Gender Diversity by Department",
                         barmode='stack',
                         labels={'value': 'Percentage', 'variable': 'Gender'})
            fig.update_layout(yaxis_title="Percentage", yaxis_tickformat=".0%", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            # Diversity metrics over time
            diversity_data = filtered_df.groupby('year')[['female_pct', 'minority_pct']].mean().reset_index()
            fig = px.line(diversity_data, x='year', y=['female_pct', 'minority_pct'],
                          title="Diversity Metrics Over Time")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Minority Representation Over Time by Region
            minority_trend = filtered_df.groupby(['year', 'region'])['minority_pct'].mean().reset_index()
            fig = px.line(minority_trend, x='year', y='minority_pct', color='region',
                          title="Minority Representation Over Time by Region",
                          markers=True)
            fig.update_layout(yaxis_title="Minority Percentage", yaxis_tickformat=".1%", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            # Pay Equity Analysis by Department
            pay_equity_dept = filtered_df.groupby('department')['pay_equity_ratio_female_to_male'].mean().reset_index()
            fig = px.bar(pay_equity_dept, x='department', y='pay_equity_ratio_female_to_male',
                         title="Pay Equity Ratio by Department",
                         color='pay_equity_ratio_female_to_male',
                         color_continuous_scale='RdYlGn',
                         range_color=[0.8, 1.2])
            fig.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Ideal Equity")
            fig.update_layout(yaxis_title="Pay Equity Ratio (Female to Male)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        # Section 2: Employee Well-Being & Development
        st.markdown("#### 💼 Employee Well-Being & Development")
        col1, col2 = st.columns(2)

        with col1:
            # Average Training Hours by Department
            training_by_dept = filtered_df.groupby('department')['avg_training_hours_per_employee'].mean().reset_index()
            fig = px.bar(training_by_dept, x='department', y='avg_training_hours_per_employee',
                         title="Average Training Hours by Department",
                         color='avg_training_hours_per_employee',
                         color_continuous_scale='Blues')
            fig.update_layout(yaxis_title="Training Hours", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            # Employee Turnover Trend Over Time
            turnover_trend = filtered_df.groupby(['year', 'quarter'])['employee_turnover_pct'].mean().reset_index()
            turnover_trend['period'] = turnover_trend['year'].astype(str) + '-Q' + turnover_trend['quarter'].astype(str)
            fig = px.line(turnover_trend, x='period', y='employee_turnover_pct',
                          title="Employee Turnover Trend Over Time",
                          markers=True)
            fig.update_layout(yaxis_title="Turnover Rate", yaxis_tickformat=".1%", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Lost Time Incident Rate
            safety_trend = filtered_df.groupby('year')['lost_time_incident_rate'].mean().reset_index()
            fig = px.line(safety_trend, x='year', y='lost_time_incident_rate',
                          title="Lost Time Incident Rate (Safety Performance)",
                          markers=True)
            fig.update_layout(yaxis_title="Incident Rate", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            # Training vs Turnover vs Engagement Correlation Heatmap
            correlation_data = filtered_df[['avg_training_hours_per_employee', 'employee_turnover_pct',
                                            'employee_engagement_score', 'pay_equity_ratio_female_to_male']].corr()
            fig = px.imshow(correlation_data,
                            title="Employee Metrics Correlation Heatmap",
                            color_continuous_scale='RdBu',
                            aspect="auto")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        # Section 3: Employee Engagement & Satisfaction
        st.markdown("#### 😊 Employee Engagement & Satisfaction")
        col1, col2 = st.columns(2)

        with col1:
            # Employee Engagement Score Over Time
            # Employee engagement by department
            engagement_by_dept = filtered_df.groupby('department')['employee_engagement_score'].mean().reset_index()
            fig = px.bar(engagement_by_dept, x='department', y='employee_engagement_score',
                         title="Employee Engagement by Department")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            engagement_trend = filtered_df.groupby('year')['employee_engagement_score'].mean().reset_index()
            fig = px.line(engagement_trend, x='year', y='employee_engagement_score',
                          title="Employee Engagement Score Over Time",
                          markers=True)
            fig.update_layout(yaxis_title="Engagement Score", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            # Community Investment Impact
            community_investment = filtered_df.groupby('year')['community_investment_usd_m'].sum().reset_index()
            fig = px.area(community_investment, x='year', y='community_investment_usd_m',
                          title="Community Investment Over Time")
            fig.update_layout(yaxis_title="Community Investment (USD M)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Engagement vs Turnover Scatter Plot
            fig = px.scatter(filtered_df, x='employee_engagement_score', y='employee_turnover_pct',
                             color='region', size='headcount',
                             title="Engagement vs Employee Turnover",
                             trendline="lowess",
                             hover_data=['department', 'year'])
            fig.update_layout(xaxis_title="Employee Engagement Score",
                              yaxis_title="Turnover Rate",
                              yaxis_tickformat=".1%", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            # Training and turnover
            hr_data = filtered_df.groupby('year')[
                ['avg_training_hours_per_employee', 'employee_turnover_pct']].mean().reset_index()
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            # --- THEME UPDATE ---
            fig.update_layout(
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                title_font_color='#f1f5f9', legend_font_color='#f1f5f9',
                title="Training Hours vs Employee Turnover"
            )
            fig.add_trace(go.Scatter(x=hr_data['year'], y=hr_data['avg_training_hours_per_employee'],
                                     name="Training Hours"), secondary_y=False)
            fig.add_trace(go.Scatter(x=hr_data['year'], y=hr_data['employee_turnover_pct'],
                                     name="Turnover %"), secondary_y=True)
            st.plotly_chart(fig, use_container_width=True)

        # Section 4: Social Equity & Fairness
        st.markdown("#### ⚖️ Social Equity & Fairness")
        col1, col2 = st.columns(2)

        with col1:
            # 1. Pay Equity vs Engagement - Changed to Grouped Bar Chart
            equity_engagement = filtered_df.groupby('department').agg({
                'pay_equity_ratio_female_to_male': 'mean',
                'employee_engagement_score': 'mean'
            }).reset_index()

            fig = go.Figure()
            # --- THEME UPDATE ---
            fig.update_layout(
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                title_font_color='#f1f5f9', legend_font_color='#f1f5f9',
                title="Pay Equity vs Employee Engagement by Department",
                xaxis_title="Department",
                yaxis=dict(title="Pay Equity Ratio", side='left', range=[0.8, 1.2]),
                yaxis2=dict(title="Engagement Score", side='right', overlaying='y', range=[0, 100]),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
            )
            fig.add_trace(go.Bar(
                name='Pay Equity Ratio',
                x=equity_engagement['department'],
                y=equity_engagement['pay_equity_ratio_female_to_male'],
                yaxis='y',
                marker_color='#1f77b4'
            ))
            fig.add_trace(go.Scatter(
                name='Engagement Score',
                x=equity_engagement['department'],
                y=equity_engagement['employee_engagement_score'],
                yaxis='y2',
                mode='lines+markers',
                line=dict(color='#ff7f0e', width=3),
                marker=dict(size=8, color='#ff7f0e')
            ))
            fig.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Ideal Equity")
            st.plotly_chart(fig, use_container_width=True)

            # 2. Training Hours vs Pay Equity - Changed to Heatmap
            # Create bins for training hours
            filtered_df['training_hours_bin'] = pd.cut(
                filtered_df['avg_training_hours_per_employee'],
                bins=5,
                labels=['Very Low', 'Low', 'Medium', 'High', 'Very High']
            )

            training_equity_pivot = filtered_df.pivot_table(
                values='pay_equity_ratio_female_to_male',
                index='region',
                columns='training_hours_bin',
                aggfunc='mean'
            ).fillna(0)

            fig = px.imshow(training_equity_pivot,
                            title="Training Hours vs Pay Equity by Region",
                            color_continuous_scale='RdYlGn',
                            aspect="auto",
                            labels=dict(x="Training Hours Level", y="Region", color="Pay Equity Ratio"))
            fig.update_layout(xaxis_title="Training Hours Level", yaxis_title="Region", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # 3. Minority Representation vs Pay Equity - Changed to Enhanced Bubble Chart
            minority_equity = filtered_df.groupby('department').agg({
                'minority_pct': 'mean',
                'pay_equity_ratio_female_to_male': 'mean',
                'headcount': 'mean'
            }).reset_index()

            fig = px.scatter(minority_equity,
                             x='minority_pct',
                             y='pay_equity_ratio_female_to_male',
                             size='headcount',
                             color='department',
                             title="Minority Representation vs Pay Equity by Department",
                             hover_data=['department'],
                             size_max=60)

            # Add quadrant lines and annotations
            fig.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Ideal Equity")
            fig.add_vline(x=minority_equity['minority_pct'].median(), line_dash="dash", line_color="blue",
                          annotation_text="Median Minority %")

            # Add quadrant annotations
            fig.add_annotation(x=0.7, y=1.15, text="High Equity\nHigh Diversity", showarrow=False,
                               font=dict(color="green"))
            fig.add_annotation(x=0.7, y=0.85, text="Low Equity\nHigh Diversity", showarrow=False,
                               font=dict(color="orange"))
            fig.add_annotation(x=0.3, y=1.15, text="High Equity\nLow Diversity", showarrow=False,
                               font=dict(color="blue"))
            fig.add_annotation(x=0.3, y=0.85, text="Low Equity\nLow Diversity", showarrow=False, font=dict(color="red"))

            fig.update_layout(
                xaxis_title="Minority Percentage",
                yaxis_title="Pay Equity Ratio",
                xaxis_tickformat=".0%",
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                title_font_color='#f1f5f9',
                legend_font_color='#f1f5f9'
            )
            st.plotly_chart(fig, use_container_width=True)


            # Pay equity gauge
            pay_equity = filtered_df['pay_equity_ratio_female_to_male'].mean()
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pay_equity,
                title={'text': "Average Pay Equity Ratio (Female to Male)", 'font': {'color': '#f1f5f9'}},
                gauge={
                    'axis': {'range': [0.8, 1.2]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0.8, 0.95], 'color': "lightgray"},
                        {'range': [0.95, 1.05], 'color': "lightgreen"},
                        {'range': [1.05, 1.2], 'color': "lightgray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 1.0
                    }
                }))
            # --- THEME UPDATE ---
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        # Section 5: Composite Index Metrics
        st.markdown("#### 📊 Composite Social Metrics")
        col1, col2 = st.columns(2)

        with col1:
            # Social Well-Being Index by Department
            social_index_dept = filtered_df.groupby('department')['social_well_being_index'].mean().reset_index()
            fig = px.bar(social_index_dept, x='department', y='social_well_being_index',
                         title="Social Well-Being Index by Department",
                         color='social_well_being_index',
                         color_continuous_scale='Viridis')
            fig.update_layout(yaxis_title="Social Well-Being Index", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            # Social Well-Being Index Trend
            social_trend = filtered_df.groupby('year')['social_well_being_index'].mean().reset_index()
            fig = px.line(social_trend, x='year', y='social_well_being_index',
                          title="Social Well-Being Index Over Time",
                          markers=True)
            fig.update_layout(yaxis_title="Social Well-Being Index", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Diversity & Inclusion Index by Region
            diversity_index_region = filtered_df.groupby('region')['diversity_inclusion_index'].mean().reset_index()
            fig = px.bar(diversity_index_region, x='region', y='diversity_inclusion_index',
                         title="Diversity & Inclusion Index by Region",
                         color='diversity_inclusion_index',
                         color_continuous_scale='Plasma')
            fig.update_layout(yaxis_title="Diversity & Inclusion Index", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            # Diversity & Inclusion Index Trend
            diversity_trend = filtered_df.groupby('year')['diversity_inclusion_index'].mean().reset_index()
            fig = px.line(diversity_trend, x='year', y='diversity_inclusion_index',
                          title="Diversity & Inclusion Index Over Time",
                          markers=True)
            fig.update_layout(yaxis_title="Diversity & Inclusion Index", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        # Additional detailed analysis
        with st.expander("📈 Detailed Social Analysis"):
            col1, col2 = st.columns(2)

            with col1:
                # Regional Social Performance Comparison
                region_social = filtered_df.groupby('region').agg({
                    'social_well_being_index': 'mean',
                    'diversity_inclusion_index': 'mean',
                    'employee_engagement_score': 'mean',
                    'pay_equity_ratio_female_to_male': 'mean'
                }).reset_index()

                fig = px.scatter(region_social, x='social_well_being_index', y='diversity_inclusion_index',
                                 size='employee_engagement_score', color='region',
                                 title="Regional Social Performance: Well-Being vs Diversity",
                                 hover_data=['pay_equity_ratio_female_to_male'])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Department Performance Matrix
                dept_social = filtered_df.groupby('department').agg({
                    'social_well_being_index': 'mean',
                    'employee_turnover_pct': 'mean',
                    'avg_training_hours_per_employee': 'mean'
                }).reset_index()

                fig = px.scatter(dept_social, x='social_well_being_index', y='employee_turnover_pct',
                                 size='avg_training_hours_per_employee', color='department',
                                 title="Department Performance: Well-Being vs Turnover",
                                 trendline="lowess")
                fig.update_layout(yaxis_title="Turnover Rate", yaxis_tickformat=".1%", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
                st.plotly_chart(fig, use_container_width=True)



    with tab3:
        st.subheader("Governance Performance")

        # Calculate Governance Effectiveness Index
        filtered_df['governance_effectiveness_index'] = (
                filtered_df['independent_directors_pct'] * 0.3 +
                filtered_df['board_gender_diversity_pct'] * 0.2 +
                filtered_df['anti_corruption_training_pct'] * 0.2 +
                filtered_df['esg_policy_coverage_pct'] * 0.15 +
                filtered_df['supplier_code_of_conduct_coverage_pct'] * 0.15 +
                (1 - filtered_df['controversy_level_0_low_3_high'] / 3) * 0.1
        )

        # Governance KPIs
        st.markdown("#### 🏛️ Key Governance Metrics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            governance_index = filtered_df['governance_effectiveness_index'].mean()
            st.metric("Governance Effectiveness Index", f"{governance_index:.1f}")

        with col2:
            board_independence = filtered_df['independent_directors_pct'].mean()
            st.metric("Avg Board Independence", f"{board_independence:.1f}%")

        with col3:
            policy_coverage = filtered_df['esg_policy_coverage_pct'].mean()
            st.metric("ESG Policy Coverage", f"{policy_coverage:.1f}%")

        with col4:
            controversies = filtered_df['controversy_level_0_low_3_high'].mean()
            st.metric("Avg Controversy Level", f"{controversies:.2f}")

        # Section 1: Board & Leadership Insights
        st.markdown("#### 👑 Board & Leadership Insights")
        col1, col2 = st.columns(2)



        with col1:
            # Regional Comparison of Board Structures
            board_structures = filtered_df.groupby('region').agg({
                'board_size': 'mean',
                'independent_directors_pct': 'mean'
            }).reset_index()

            fig = go.Figure()
            # --- THEME UPDATE ---
            fig.update_layout(
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                title_font_color='#f1f5f9', legend_font_color='#f1f5f9',
                title="Regional Comparison of Board Structures",
                xaxis_title="Region",
                yaxis=dict(title="Board Size", side='left'),
                yaxis2=dict(title="Independent Directors %", side='right', overlaying='y'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
            )
            fig.add_trace(go.Bar(
                name='Avg Board Size',
                x=board_structures['region'],
                y=board_structures['board_size'],
                yaxis='y',
                marker_color='#1f77b4'
            ))
            fig.add_trace(go.Scatter(
                name='Independent Directors %',
                x=board_structures['region'],
                y=board_structures['independent_directors_pct'],
                yaxis='y2',
                mode='lines+markers',
                line=dict(color='#ff7f0e', width=3)
            ))
            st.plotly_chart(fig, use_container_width=True)


        with col2:

            # Board composition over time (existing but enhanced)
            board_data = filtered_df.groupby('year')[
                ['board_gender_diversity_pct', 'independent_directors_pct', 'board_size']].mean().reset_index()
            fig = px.line(board_data, x='year', y=['board_gender_diversity_pct', 'independent_directors_pct'],
                          title="Board Composition Over Time",
                          markers=True)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        # Section 2: Ethics, Compliance & Risk
        st.markdown("#### ⚖️ Ethics, Compliance & Risk")
        col1, col2 = st.columns(2)

        with col1:
            # Governance Risk Heatmap
            risk_data = filtered_df.groupby('region').agg({
                'data_breaches_count': 'sum',
                'whistleblower_reports': 'sum',
                'fines_penalties_usd_m': 'sum'
            }).reset_index()

            # Normalize for heatmap
            risk_normalized = risk_data.copy()
            for col in ['data_breaches_count', 'whistleblower_reports', 'fines_penalties_usd_m']:
                if risk_data[col].max() - risk_data[col].min() != 0:
                    risk_normalized[col] = (risk_data[col] - risk_data[col].min()) / (
                                risk_data[col].max() - risk_data[col].min())
                else:
                    risk_normalized[col] = 0.5 # Avoid division by zero if all values are same

            risk_normalized = risk_normalized.set_index('region')
            fig = px.imshow(risk_normalized.T,
                            title="Governance Risk Heatmap by Region",
                            color_continuous_scale='Reds',
                            aspect="auto")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            # Whistleblower Activity Over Time
            if 'whistleblower_reports' in filtered_df.columns:
                whistleblower_trend = filtered_df.groupby('year')['whistleblower_reports'].sum().reset_index()
                fig = px.line(whistleblower_trend, x='year', y='whistleblower_reports',
                              title="Whistleblower Reports Over Time",
                              markers=True)
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Data Breach Trends
            if 'data_breaches_count' in filtered_df.columns:
                breach_trend = filtered_df.groupby('year')['data_breaches_count'].sum().reset_index()
                fig = px.line(breach_trend, x='year', y='data_breaches_count',
                              title="Data Breach Trends",
                              markers=True, color_discrete_sequence=['red'])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
                st.plotly_chart(fig, use_container_width=True)

            # Fines and Penalties Tracker
            if 'fines_penalties_usd_m' in filtered_df.columns:
                fines_trend = filtered_df.groupby('year')['fines_penalties_usd_m'].sum().reset_index()
                fig = px.bar(fines_trend, x='year', y='fines_penalties_usd_m',
                             title="Fines and Penalties Over Time",
                             color='fines_penalties_usd_m',
                             color_continuous_scale='Reds')
                fig.update_layout(yaxis_title="Fines (USD M)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
                st.plotly_chart(fig, use_container_width=True)

        with col1:

            # Anti-corruption training (existing)
            anti_corruption = filtered_df.groupby('department')['anti_corruption_training_pct'].mean().reset_index()
            fig = px.bar(anti_corruption, x='department', y='anti_corruption_training_pct',
                         title="Anti-Corruption Training Completion by Department")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        # Section 3: Transparency & Reporting Features
        st.markdown("#### 📊 Transparency & Reporting Features")
        col1, col2 = st.columns(2)


        with col1:
            # Governance Compliance Scorecard
            st.markdown("##### 📋 Governance Compliance Scorecard")
            compliance_data = filtered_df.groupby('department').agg({
                'anti_corruption_training_pct': 'mean',
                'esg_policy_coverage_pct': 'mean',
                'supplier_code_of_conduct_coverage_pct': 'mean',
                'data_breaches_count': 'sum',
                'fines_penalties_usd_m': 'sum'
            }).reset_index()

            # Display as a table with formatting
            display_data = compliance_data.copy()
            display_data['anti_corruption_training_pct'] = display_data['anti_corruption_training_pct'].round(1)
            display_data['esg_policy_coverage_pct'] = display_data['esg_policy_coverage_pct'].round(1)
            display_data['supplier_code_of_conduct_coverage_pct'] = display_data[
                'supplier_code_of_conduct_coverage_pct'].round(1)
            display_data['fines_penalties_usd_m'] = display_data['fines_penalties_usd_m'].round(2)

            st.dataframe(display_data, use_container_width=True)

        with col2:

            # Benchmark Governance Score
            st.markdown("##### 🎯 Governance Benchmark")
            current_gov_index = filtered_df['governance_effectiveness_index'].mean()
            previous_year = filtered_df[filtered_df['year'] == filtered_df['year'].max() - 1]
            previous_gov_index = previous_year[
                'governance_effectiveness_index'].mean() if not previous_year.empty else current_gov_index

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Current Governance Index", f"{current_gov_index:.1f}",
                          delta=f"{(current_gov_index - previous_gov_index):.1f}")
            with col2:
                industry_benchmark = 65  # Example benchmark
                st.metric("Industry Benchmark", f"{industry_benchmark}")

        # Section 4: Performance & Accountability
        st.markdown("#### 📈 Performance & Accountability")
        col1, col2 = st.columns(2)

        with col1:
            # ESG Score vs Governance Variables Correlation
            corr_data = filtered_df[['esg_score', 'independent_directors_pct', 'board_gender_diversity_pct',
                                     'anti_corruption_training_pct', 'esg_policy_coverage_pct',
                                     'supplier_code_of_conduct_coverage_pct']].corr()

            fig = px.imshow(corr_data,
                            title="ESG Score vs Governance Variables Correlation",
                            color_continuous_scale='RdBu',
                            aspect="auto",
                            zmin=-1, zmax=1)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)



        with col2:
            # Governance Effectiveness Index Gauge
            gov_index = filtered_df['governance_effectiveness_index'].mean()
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=gov_index,
                title={'text': "Governance Effectiveness Index", 'font': {'color': '#f1f5f9'}},
                delta={'reference': previous_gov_index},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 75], 'color': "yellow"},
                        {'range': [75, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 80
                    }
                }))
            # --- THEME UPDATE ---
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        with col1:

            # Governance Index by Department
            gov_by_dept = filtered_df.groupby('department')['governance_effectiveness_index'].mean().reset_index()
            fig = px.bar(gov_by_dept, x='department', y='governance_effectiveness_index',
                         title="Governance Effectiveness by Department",
                         color='governance_effectiveness_index',
                         color_continuous_scale='Viridis')
            fig.update_layout(yaxis_title="Governance Effectiveness Index", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        # Section 5: Policy & Compliance Oversight
        st.markdown("#### 📝 Policy & Compliance Oversight")
        col1, col2 = st.columns(2)

        with col1:
            # Policy Adoption vs ESG Score
            fig = px.scatter(filtered_df,
                             x='esg_policy_coverage_pct',
                             y='esg_score',
                             color='region',
                             size='board_size',
                             title="ESG Policy Coverage vs ESG Score",
                             trendline="ols")
            fig.update_layout(xaxis_title="ESG Policy Coverage (%)", yaxis_title="ESG Score", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            # Supplier Code of Conduct Compliance
            supplier_trend = filtered_df.groupby('year')['supplier_code_of_conduct_coverage_pct'].mean().reset_index()
            fig = px.line(supplier_trend, x='year', y='supplier_code_of_conduct_coverage_pct',
                          title="Supplier Code of Conduct Coverage Over Time",
                          markers=True)
            fig.update_layout(yaxis_title="Supplier Code Coverage (%)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # ESG Policy Gap Tracker
            policy_gap = filtered_df.groupby('department')['esg_policy_coverage_pct'].mean().reset_index()
            policy_gap['meets_threshold'] = policy_gap['esg_policy_coverage_pct'] >= 70

            fig = px.bar(policy_gap, x='department', y='esg_policy_coverage_pct',
                         color='meets_threshold',
                         title="ESG Policy Gap Tracker by Department",
                         color_discrete_map={True: 'green', False: 'red'})
            fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="70% Threshold")
            fig.update_layout(yaxis_title="ESG Policy Coverage (%)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

            # Controversy levels (existing pie chart)
            controversy_data = filtered_df['controversy_level_0_low_3_high'].value_counts().reset_index()
            controversy_data.columns = ['controversy_level', 'count']
            fig = px.pie(controversy_data, values='count', names='controversy_level',
                         title="Distribution of Controversy Levels")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        # Detailed Analysis Expandable Section
        with st.expander("🔍 Detailed Governance Analysis"):
            col1, col2 = st.columns(2)

            with col1:
                # Regional Governance Performance
                regional_gov = filtered_df.groupby('region').agg({
                    'governance_effectiveness_index': 'mean',
                    'esg_score': 'mean',
                    'controversy_level_0_low_3_high': 'mean'
                }).reset_index()

                fig = px.scatter(regional_gov,
                                 x='governance_effectiveness_index',
                                 y='esg_score',
                                 size='controversy_level_0_low_3_high',
                                 color='region',
                                 title="Regional Governance vs ESG Performance",
                                 hover_data=['region'])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Department Risk Profile
                dept_risk = filtered_df.groupby('department').agg({
                    'data_breaches_count': 'sum',
                    'fines_penalties_usd_m': 'sum',
                    'whistleblower_reports': 'sum'
                }).reset_index()

                fig = px.scatter(dept_risk,
                                 x='data_breaches_count',
                                 y='fines_penalties_usd_m',
                                 size='whistleblower_reports',
                                 color='department',
                                 title="Department Risk Profile Analysis")
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
                st.plotly_chart(fig, use_container_width=True)



    with tab4:
        st.subheader("Trend Analysis")

        # ESG Score trends
        esg_trends = filtered_df.groupby(['year', 'quarter'])['esg_score'].mean().reset_index()
        esg_trends['period'] = esg_trends['year'].astype(str) + '-Q' + esg_trends['quarter'].astype(str)

        fig = px.line(esg_trends, x='period', y='esg_score',
                      title="ESG Score Trend Over Time")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            # Regional comparison
            regional_esg = filtered_df.groupby('region')['esg_score'].mean().reset_index()
            fig = px.bar(regional_esg, x='region', y='esg_score',
                         title="Average ESG Score by Region")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Department comparison
            dept_esg = filtered_df.groupby('department')['esg_score'].mean().reset_index()
            fig = px.bar(dept_esg, x='department', y='esg_score',
                         title="Average ESG Score by Department")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title_font_color='#f1f5f9', legend_font_color='#f1f5f9')
            st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.subheader("Detailed Data View")

        # Show raw data with additional metrics
        display_columns = [
            'company_name', 'region', 'department', 'year', 'quarter',
            'esg_score', 'renewable_energy_share_pct', 'scope1_emissions_tco2e',
            'female_pct', 'employee_engagement_score', 'controversy_level_0_low_3_high'
        ]

        detailed_df = filtered_df[display_columns].copy()
        detailed_df = detailed_df.sort_values(['year', 'quarter', 'department'], ascending=[False, False, True])

        st.dataframe(
            detailed_df,
            use_container_width=True,
            height=400
        )

        # Download option
        csv = detailed_df.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv,
            file_name=f"esg_data_{selected_company.replace(' ', '_')}.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown(
    "**GreenLens ESG Analytics** | Data updated regularly | "
    "For more information, contact your ESG representative."
)
