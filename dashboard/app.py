import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Configure Streamlit page
st.set_page_config(
    page_title="L-AIPI Dataset Explorer (2000-2023)",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data function (cached)
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dev_path = os.path.join(base_dir, "data", "laipi_developing_panel_2000_2023.csv")
    glob_path = os.path.join(base_dir, "data", "laipi_global_panel_2000_2023.csv")
    rank_path = os.path.join(base_dir, "data", "laipi_country_rankings_2023.csv")
    
    dev_df = pd.read_csv(dev_path)
    glob_df = pd.read_csv(glob_path)
    rank_df = pd.read_csv(rank_path)
    return dev_df, glob_df, rank_df

try:
    dev_df, glob_df, rank_df = load_data()
except Exception as e:
    st.error(f"Error loading datasets: {e}")
    st.stop()

# Header
st.title("🌍 Longitudinal AI Preparedness Index (L-AIPI)")
st.markdown("""
**An Open Macroeconomic Panel Benchmark for 149 Developing Economies (2000–2023)**  
*Constructed by Chisom L. Ubabukoh (O.P. Jindal Global University) • Validated against IMF AIPI ($r = 0.912$)*
""")

# Sidebar Navigation and Filters
st.sidebar.header("Navigation & Filters")
dataset_choice = st.sidebar.radio("Select Dataset Scope:", ["Developing Economies Panel (N=149)", "Global Panel (N=240+)"])
active_df = dev_df if "Developing" in dataset_choice else glob_df

regions = ["All Regions"] + sorted(list(active_df["region"].dropna().unique()))
selected_region = st.sidebar.selectbox("Filter by UN Region:", regions)

if selected_region != "All Regions":
    filtered_df = active_df[active_df["region"] == selected_region]
else:
    filtered_df = active_df

countries = sorted(list(filtered_df["country_name"].dropna().unique()))
default_country = "Nigeria" if "Nigeria" in countries else countries[0]
selected_country = st.sidebar.selectbox("Select Country:", countries, index=countries.index(default_country) if default_country in countries else 0)

year_range = st.sidebar.slider("Select Year Horizon:", 2000, 2023, (2000, 2023))

# Quick Metrics for Selected Country
country_data = filtered_df[filtered_df["country_name"] == selected_country].sort_values("year")
c_start = country_data[country_data["year"] == year_range[0]]
c_end = country_data[country_data["year"] == year_range[1]]

val_start = c_start["laipi_composite"].values[0] if not c_start.empty and pd.notna(c_start["laipi_composite"].values[0]) else 0.0
val_end = c_end["laipi_composite"].values[0] if not c_end.empty and pd.notna(c_end["laipi_composite"].values[0]) else 0.0
growth = ((val_end - val_start) / max(val_start, 0.001)) * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric(f"L-AIPI ({year_range[0]})", f"{val_start:.3f}")
col2.metric(f"L-AIPI ({year_range[1]})", f"{val_end:.3f}", f"{growth:+.1f}%")
latest_rank = rank_df[rank_df["country_name"] == selected_country]["rank_laipi_2023"].values
col3.metric("Global Rank (2023)", f"#{latest_rank[0]}" if len(latest_rank) > 0 else "N/A")
imf_score = country_data["imf_aipi_2023"].dropna().values
col4.metric("Official IMF AIPI (2023)", f"{imf_score[0]:.2f}" if len(imf_score) > 0 else "N/A")

# Main Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Trajectory Explorer", 
    "🧩 Pillar Decomposition", 
    "⚡ The Capacity Paradox", 
    "🏆 Global Rankings (2023)", 
    "📥 Data Export & Citation"
])

# TAB 1: Country Trajectory Explorer
with tab1:
    st.subheader(f"AI Preparedness Trajectory: {selected_country} vs Benchmarks ({year_range[0]}–{year_range[1]})")
    
    # Calculate regional and sample averages
    reg_avg = active_df.groupby("year")["laipi_composite"].mean().reset_index()
    c_df = country_data[(country_data["year"] >= year_range[0]) & (country_data["year"] <= year_range[1])]
    
    fig_traj = go.Figure()
    fig_traj.add_trace(go.Scatter(
        x=c_df["year"], y=c_df["laipi_composite"],
        mode="lines+markers", name=f"{selected_country} (L-AIPI)",
        line=dict(color="#0d3b66", width=3.5), marker=dict(size=7)
    ))
    fig_traj.add_trace(go.Scatter(
        x=reg_avg["year"], y=reg_avg["laipi_composite"],
        mode="lines", name="Global Developing Average",
        line=dict(color="#b22222", width=2, dash="dash")
    ))
    fig_traj.update_layout(
        xaxis_title="Year", yaxis_title="Longitudinal AI Preparedness Index [0–1]",
        yaxis=dict(range=[0, 1]), hovermode="x unified",
        template="plotly_white", height=480
    )
    st.plotly_chart(fig_traj, use_container_width=True)

# TAB 2: Pillar Decomposition
with tab2:
    st.subheader(f"Pillar Evolution for {selected_country}")
    st.markdown("Decomposition across **Digital Infrastructure ($DI$)**, **Human Capital ($HC$)**, and **Innovation & Technology ($\text{INN}$)**:")
    
    c_pillars = c_df[["year", "pillar_digital_infra", "pillar_human_capital", "pillar_innovation"]].melt(
        id_vars="year", var_name="Pillar", value_name="Score"
    )
    pillar_names = {
        "pillar_digital_infra": "Digital Infrastructure (DI)",
        "pillar_human_capital": "Human Capital (HC)",
        "pillar_innovation": "Innovation & Tech Capability (INN)"
    }
    c_pillars["Pillar"] = c_pillars["Pillar"].map(pillar_names)
    
    fig_pil = px.line(
        c_pillars, x="year", y="Score", color="Pillar",
        color_discrete_sequence=["#1f77b4", "#2ca02c", "#ff7f0e"],
        markers=True, template="plotly_white", height=450
    )
    fig_pil.update_layout(yaxis=dict(range=[0, 1]), hovermode="x unified")
    st.plotly_chart(fig_pil, use_container_width=True)

# TAB 3: Capacity Paradox Visualizer
with tab3:
    st.subheader("The AI Adaptation Capacity Paradox")
    st.markdown("""
    Economies facing the greatest climate vulnerability display the largest theoretical marginal buffering returns ($\beta = +0.7714$), 
    yet their low baseline preparedness (mean index $= 0.142$) prevents them from realizing actual protection.
    """)
    
    # Scatter plot: 2023 L-AIPI vs Temperature Anomaly
    dev_2023 = dev_df[dev_df["year"] == 2023].dropna(subset=["laipi_composite", "temp_anomaly_c"])
    fig_paradox = px.scatter(
        dev_2023, x="laipi_composite", y="temp_anomaly_c",
        hover_name="country_name", color="region", size="agri_val_add_worker",
        labels={
            "laipi_composite": "Longitudinal AI Preparedness Index (2023)",
            "temp_anomaly_c": "Temperature Anomaly (°C)",
            "region": "UN Region",
            "agri_val_add_worker": "Agri Output / Worker"
        },
        template="plotly_white", height=500
    )
    fig_paradox.add_vline(x=0.421, line_dash="dash", line_color="red", annotation_text="Zero-Crossing Buffer Threshold (0.421)")
    st.plotly_chart(fig_paradox, use_container_width=True)

# TAB 4: Global Rankings
with tab4:
    st.subheader("Cross-Country AI Preparedness Rankings (2023)")
    st.dataframe(
        rank_df.style.format({
            "laipi_composite": "{:.3f}",
            "pillar_digital_infra": "{:.3f}",
            "pillar_human_capital": "{:.3f}",
            "pillar_innovation": "{:.3f}",
            "imf_aipi_2023": "{:.2f}"
        }),
        height=500, use_container_width=True
    )

# TAB 5: Data Export & Citation
with tab5:
    st.subheader("Download Standardized Datasets")
    st.markdown("Download ready-to-merge research data in standard formats:")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button(
            label="📥 Download Filtered Country Slice (CSV)",
            data=c_df.to_csv(index=False).encode('utf-8'),
            file_name=f"laipi_{selected_country.lower().replace(' ', '_')}_{year_range[0]}_{year_range[1]}.csv",
            mime="text/csv"
        )
    with col_d2:
        st.download_button(
            label="📥 Download Full Developing Panel (CSV, 3,512 obs)",
            data=dev_df.to_csv(index=False).encode('utf-8'),
            file_name="laipi_developing_panel_2000_2023.csv",
            mime="text/csv"
        )
    
    st.divider()
    st.subheader("How to Cite L-AIPI")
    st.code("""
@article{ubabukoh2026laipi,
  author    = {Ubabukoh, Chisom L.},
  title     = {The AI Adaptation Capacity Paradox: Longitudinal AI Preparedness and Agricultural Climate Resilience in Developing Economies},
  journal   = {Information Technology for Development},
  year      = {2026},
  note      = {Under review}
}
""", language="bibtex")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Open Access:** Distributed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).")
