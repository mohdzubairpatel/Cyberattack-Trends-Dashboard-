import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import io
import datetime
from contextlib import contextmanager

# ---- Page Config ----
st.set_page_config(page_title="CyberAttack Trend Dashboard", layout="wide")

# ---- PAGE NAVIGATION ----
if "page" not in st.session_state:
    st.session_state.page = "Overview Dashboard"

page = st.sidebar.selectbox("🌐 Go to Page", [
    "Overview Dashboard",
    "📊 Animated Trend Explorer",
    "📄 Export Reports"
], index=["Overview Dashboard", "📊 Animated Trend Explorer", "📄 Export Reports"].index(st.session_state.page))

st.session_state.page = page

# ---- Load Data ----
df = pd.read_csv("data/cyberattacks_by_year.csv")
df_attacks = pd.read_csv("data/Global_Cybersecurity_Threats_2015-2024.csv")

# ---- Clean Data ----
df_attacks['Country'] = df_attacks['Country'].astype(str).str.strip().str.title()
df_attacks['Attack Type'] = df_attacks['Attack Type'].astype(str).str.strip().str.title()
df_attacks['Target Industry'] = df_attacks['Target Industry'].astype(str).str.strip().str.title()
df_attacks['Year'] = pd.to_numeric(df_attacks['Year'], errors='coerce')
df_attacks['Incident Resolution Time (in Hours)'] = pd.to_numeric(df_attacks['Incident Resolution Time (in Hours)'], errors='coerce')
df_attacks['Financial Loss (in Million $)'] = pd.to_numeric(df_attacks['Financial Loss (in Million $)'], errors='coerce')

# ---- Context Manager for Sections ----
@contextmanager
def with_bordered_section(title):
    st.markdown(f"""
    <div style="border: 1px solid #ccc; border-radius: 10px; padding: 20px; margin-bottom: 30px;">
    <h4 style='margin-top:0;'>{title}</h4>
    """, unsafe_allow_html=True)
    with st.container():
        yield
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Page Routing ----
if page == "Overview Dashboard":
    # ---- Header Section with Border and Background ----
    st.markdown("""
<div style="
    background-color: #e2ecf8;
    border: 2px solid #cbd5e0;
    padding: 25px;
    border-radius: 10px;
    margin-bottom: 25px;
    color: #222222;  /* Ensures dark readable text */
">
    <h1 style='margin-bottom: 10px; color: #1a202c;'>🛡️ CyberAttack Trend Dashboard</h1>
    <p style='font-size: 16px; color: #2d3748;'>
        Analyze global cyber threats, financial impacts, and industry vulnerabilities with forecasting features.
    </p>
    <div style="
        background-color: #fff3cd;
        color: #856404;
        padding: 12px;
        border: 1px solid #ffeeba;
        border-radius: 6px;
        font-size: 15px;
        margin-top: 15px;
    ">
        ⚠️ <strong>Disclaimer:</strong> This dashboard is built on a sample dataset and does not reflect all global cyberattack incidents.
    </div>
</div>
""", unsafe_allow_html=True)



    # Sidebar filters
    year_range = st.sidebar.slider("Select Year Range", int(df_attacks['Year'].min()), int(df_attacks['Year'].max()), (2015, 2024))
    selected_countries = st.sidebar.multiselect("Select Countries", df_attacks['Country'].unique(), default=df_attacks['Country'].unique())
    selected_attacks = st.sidebar.multiselect("Select Attack Types", df_attacks['Attack Type'].unique(), default=df_attacks['Attack Type'].unique())

    filtered_df = df_attacks[
        (df_attacks['Year'] >= year_range[0]) &
        (df_attacks['Year'] <= year_range[1]) &
        (df_attacks['Country'].isin(selected_countries)) &
        (df_attacks['Attack Type'].isin(selected_attacks))
    ]

    df['Total_Attacks'] = df['Total_Attacks'].astype(int)
    df_sorted = df.sort_values("Year")
    df_sorted["YoY Change"] = df_sorted["Total_Attacks"].diff()
    spike_year = df_sorted.loc[df_sorted["YoY Change"].idxmax(), "Year"] if not df_sorted["YoY Change"].isna().all() else "N/A"

    # --- KPI Section ---
    with with_bordered_section("💡 Key Cyber Threat Metrics"):
        common_attack = filtered_df['Attack Type'].mode()[0] if not filtered_df.empty else "N/A"
        loss_by_country = filtered_df.groupby('Country')['Financial Loss (in Million $)'].sum()
        top_loss_country = loss_by_country.idxmax() if not loss_by_country.empty else "N/A"
        top_loss_value = loss_by_country.max() if not loss_by_country.empty else 0

        st.markdown("""
            <style>
            .kpi-container {{
                display: flex;
                gap: 20px;
                justify-content: space-between;
                flex-wrap: wrap;
            }}
            .kpi-card {{
                flex: 1;
                min-width: 250px;
                background: linear-gradient(to right, #1e3c72, #2a5298);
                color: white;
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }}
            .kpi-icon {{
                font-size: 28px;
                margin-bottom: 5px;
            }}
            .kpi-title {{
                font-size: 14px;
                font-weight: 600;
                margin-bottom: 5px;
            }}
            .kpi-value {{
                font-size: 20px;
                font-weight: bold;
            }}
            .kpi-sub {{
                font-size: 12px;
                color: #e0e0e0;
            }}
            </style>

            <div class="kpi-container">
                <div class="kpi-card">
                    <div class="kpi-icon">🔥</div>
                    <div class="kpi-title">Most Frequent Attack Type</div>
                    <div class="kpi-value">{}</div>
                    <div class="kpi-sub">Based on selection</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-icon">💸</div>
                    <div class="kpi-title">Country with Highest Loss</div>
                    <div class="kpi-value">${:,.0f}M</div>
                    <div class="kpi-sub">{}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-icon">📈</div>
                    <div class="kpi-title">Year with Sharpest Rise</div>
                    <div class="kpi-value">{}</div>
                    <div class="kpi-sub">Max year-on-year growth</div>
                </div>
            </div>
        """.format(common_attack, top_loss_value, top_loss_country, spike_year), unsafe_allow_html=True)

    # Divider
    st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)

    with with_bordered_section("📈 Yearly Trend of Cyberattacks"):
        fig1 = px.line(df, x="Year", y="Total_Attacks", markers=True, title="Annual Cyberattack Trend")
        st.plotly_chart(fig1, use_container_width=True)

    st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)

    with with_bordered_section("🔮 Projected Cyberattacks (Next 5 Years)"):
        forecast = pd.read_csv("data/forecast_attacks.csv")
        forecast['ds'] = pd.to_datetime(forecast['ds'])
        
        fig2 = px.line(forecast, x='ds', y='yhat', title='Predicted Total Attacks (2025–2029)', markers=True,
                    labels={'ds': 'Year', 'yhat': 'Predicted Attacks'})

        fig2.add_scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines',
                        name='Upper Bound', line=dict(dash='dot', color='green'))
        fig2.add_scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines',
                        name='Lower Bound', line=dict(dash='dot', color='red'))

        fig2.update_traces(hovertemplate='Year: %{x|%Y}<br>Attacks: %{y}')
        fig2.update_layout(xaxis_title="Year", yaxis_title="Predicted Attacks")
        st.plotly_chart(fig2, use_container_width=True)


    st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)

    with with_bordered_section("🧨 Top Cyberattack Types"):
        top_attacks = filtered_df['Attack Type'].value_counts().nlargest(10).reset_index()
        top_attacks.columns = ['Attack Type', 'Count']
        fig3 = px.pie(
            top_attacks,
            names='Attack Type',
            values='Count',
            title='Top Cyberattack Types',
            hole=0.5,  # Makes it a donut
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        st.plotly_chart(fig3, use_container_width=True)


    with with_bordered_section("🌍 Most Affected Countries"):
        country_attack_counts = filtered_df['Country'].value_counts().nlargest(20).reset_index()
        country_attack_counts.columns = ['Country', 'Incidents']
        fig4 = px.choropleth(
            country_attack_counts,
            locations='Country',
            locationmode='country names',
            color='Incidents',
            title='Geographic Spread of Cyberattacks',
            color_continuous_scale='Tealgrn'  # Changed here
        )
        st.plotly_chart(fig4, use_container_width=True)



    st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)

    with with_bordered_section("💰 Total Financial Loss by Country"):
        loss_by_country = filtered_df.groupby('Country')['Financial Loss (in Million $)'].sum().nlargest(15).reset_index()
        loss_by_country['Financial Loss (in Million $)'] = loss_by_country['Financial Loss (in Million $)'].round().astype(int)
        fig5 = px.treemap(
            loss_by_country,
            path=['Country'],
            values='Financial Loss (in Million $)',
            title='Top Countries by Financial Loss from Cyberattacks'
        )
        st.plotly_chart(fig5, use_container_width=True)


    with with_bordered_section("🏭 Most Targeted Industries"):
        top_industries = filtered_df['Target Industry'].value_counts().nlargest(10).reset_index()
        top_industries.columns = ['Industry', 'Attack Count']
        fig6 = px.bar(top_industries, x='Industry', y='Attack Count', color='Industry', text_auto=True)
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)

    with with_bordered_section("📋 Sample Incident Descriptions"):
        display_df = filtered_df[['Year', 'Country', 'Attack Type', 'Target Industry']].copy()
        display_df['Year'] = display_df['Year'].astype(int).astype(str).str.replace(',', '')
        st.dataframe(display_df.head(20))


    st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)

    with with_bordered_section("🎛️ Drill-Down: Explore by Country"):
        selected_drill = st.selectbox("Choose a country to explore", df_attacks['Country'].unique())
        country_view = df_attacks[df_attacks['Country'] == selected_drill]
        fig7 = px.pie(country_view, names='Target Industry', title=f'Targeted Industries in {selected_drill}')
        st.plotly_chart(fig7, use_container_width=True)


elif page == "📊 Animated Trend Explorer":
    with with_bordered_section("📊 Cyberattack Trends Over Time"):
        df_anim = df_attacks.copy()
        fig = px.scatter(
            df_anim,
            x="Country",
            y="Financial Loss (in Million $)",
            animation_frame="Year",
            size="Financial Loss (in Million $)",
            color="Attack Type",
            hover_name="Target Industry",
            size_max=60,
            height=600
        )

        # Improve Y-axis formatting
        fig.update_layout(
            title="Year-wise Cyberattack Impact by Country",
            xaxis_title="Country",
            yaxis_title="Financial Loss (in Million $)",
        )
        fig.update_yaxes(tickprefix="$", showgrid=True)

        st.plotly_chart(fig, use_container_width=True)

        if st.button("🔙 Back to Dashboard"):
            st.session_state.page = "Overview Dashboard"
            st.rerun()


elif page == "📄 Export Reports":
    with with_bordered_section("📄 Export Options"):
        year_range = st.slider("Select Year Range for Export", int(df_attacks['Year'].min()), int(df_attacks['Year'].max()), (2015, 2024))
        df_export = df_attacks[(df_attacks['Year'] >= year_range[0]) & (df_attacks['Year'] <= year_range[1])]

        st.download_button("Download Filtered Dataset (CSV)", df_export.to_csv(index=False), file_name="filtered_cyberattacks.csv")

        if st.button("Export Summary to PDF"):
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "CyberAttack Summary Report", ln=True, align='C')

            pdf.set_font("Arial", '', 12)
            pdf.ln(10)
            pdf.cell(0, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, "Sample Incident Records:", ln=True)
            pdf.set_font("Arial", '', 10)
            for i, row in df_export.head(20).iterrows():
                pdf.cell(0, 8, f"{row['Year']} | {row['Country']} | {row['Attack Type']} | {row['Target Industry']}", ln=True)

            st.download_button(
                label="Download PDF",
                data=pdf.output(dest='S').encode('latin1'),
                file_name="cyber_summary.pdf",
                mime='application/pdf'
            )

        if st.button("🔙 Back to Dashboard"):
            st.session_state.page = "Overview Dashboard"
            st.rerun()

# ---- Footer ----
st.markdown("---")
st.markdown("<center><small>Created by Mohammed Zubair | Data Analytics & Cybersecurity</small></center>", unsafe_allow_html=True)

# ---- Background Style ----
st.markdown("""
<style>
    .main {
        background-color: #f9f9f9;
        background-image: linear-gradient(to right, #f8f9fa, #f1f3f5);
    }
</style>
""", unsafe_allow_html=True)
