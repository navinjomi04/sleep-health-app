import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Sleep Health & Lifestyle Dashboard",
    page_icon="🌙",
    layout="wide"
)

# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("sleep_health_lifestyle_dataset-selected-columns.csv")
    return df

df = load_data()

# ----------------- SIDEBAR FILTERS -----------------
st.sidebar.header("Filter Options")

# Filter 1: Gender Multiselect
genders = st.sidebar.multiselect(
    "Select Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

# Filter 2: Occupation Selectbox
occupations = df["Occupation"].unique().tolist()
selected_occupation = st.sidebar.selectbox(
    "Select Occupation:",
    options=["All"] + occupations
)

# Filter 3: Age Slider
min_age, max_age = int(df["Age"].min()), int(df["Age"].max())
age_range = st.sidebar.slider(
    "Select Age Range:",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)

# Filter 4: BMI Category Multiselect
bmi_categories = st.sidebar.multiselect(
    "Select BMI Category:",
    options=df["BMI Category"].unique(),
    default=df["BMI Category"].unique()
)

# Apply Filters
filtered_df = df[
    (df["Gender"].isin(genders)) &
    (df["Age"].between(age_range[0], age_range[1])) &
    (df["BMI Category"].isin(bmi_categories))
]

if selected_occupation != "All":
    filtered_df = filtered_df[filtered_df["Occupation"] == selected_occupation]

# Main Header
st.title("🌙 Sleep Health & Lifestyle Analytics Dashboard")
st.markdown("Explore sleep patterns, physical activity, and stress metrics across demographics.")
st.write("---")

# ----------------- TABS NAVIGATION -----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview", 
    "📈 Data Analysis", 
    "🎨 Visualizations", 
    "💡 Insights"
])

# ----- TAB 1: OVERVIEW -----
with tab1:
    st.subheader("Key Performance Indicators (KPIs)")
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    total_records = len(filtered_df)
    avg_sleep = filtered_df["Sleep Duration (hours)"].mean() if total_records > 0 else 0
    avg_quality = filtered_df["Quality of Sleep (scale: 1-10)"].mean() if total_records > 0 else 0
    avg_activity = filtered_df["Physical Activity Level (minutes/day)"].mean() if total_records > 0 else 0
    
    kpi1.metric("Total Records", total_records)
    kpi2.metric("Avg Sleep Duration", f"{avg_sleep:.2f} hrs")
    kpi3.metric("Avg Sleep Quality", f"{avg_quality:.2f} / 10")
    kpi4.metric("Avg Daily Activity", f"{avg_activity:.1f} mins")
    
    st.write("---")
    
    with st.expander("📄 View Raw Dataset Sample"):
        st.dataframe(filtered_df, width="stretch")

# ----- TAB 2: DATA ANALYSIS -----
with tab2:
    st.subheader("Category-wise Summary & Aggregations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Occupation-wise Record Counts**")
        occ_count = filtered_df["Occupation"].value_counts().reset_index()
        occ_count.columns = ["Occupation", "Record Count"]
        st.dataframe(occ_count, width="stretch")
        
    with col2:
        st.markdown("**Average Metrics by BMI Category**")
        bmi_summary = filtered_df.groupby("BMI Category")[
            ["Sleep Duration (hours)", "Quality of Sleep (scale: 1-10)", "Stress Level (scale: 1-10)"]
        ].mean().reset_index()
        st.dataframe(bmi_summary.round(2), width="stretch")

# ----- TAB 3: VISUALIZATIONS -----
with tab3:
    st.subheader("Visual Analytics")
    
    # Bar Chart
    st.markdown("### 1. Bar Chart: Average Sleep Duration by Occupation")
    bar_data = filtered_df.groupby("Occupation")["Sleep Duration (hours)"].mean().reset_index()
    fig_bar = px.bar(
        bar_data, 
        x="Occupation", 
        y="Sleep Duration (hours)",
        color="Occupation",
        title="Average Sleep Duration across Occupations",
        text_auto=".2f"
    )
    st.plotly_chart(fig_bar, width="stretch")
    
    # Line Chart
    st.markdown("### 2. Line Chart: Trend of Sleep Quality by Age")
    line_data = filtered_df.groupby("Age")["Quality of Sleep (scale: 1-10)"].mean().reset_index()
    fig_line = px.line(
        line_data, 
        x="Age", 
        y="Quality of Sleep (scale: 1-10)",
        markers=True,
        title="Average Sleep Quality Trend Across Age Groups"
    )
    st.plotly_chart(fig_line, width="stretch")
    
    # Scatter Plot
    st.markdown("### 3. Scatter Plot: Physical Activity vs. Sleep Duration")
    fig_scatter = px.scatter(
        filtered_df,
        x="Physical Activity Level (minutes/day)",
        y="Sleep Duration (hours)",
        color="BMI Category",
        size="Quality of Sleep (scale: 1-10)",
        hover_data=["Occupation", "Age"],
        title="Physical Activity Level vs Sleep Duration categorized by BMI"
    )
    st.plotly_chart(fig_scatter, width="stretch")

# ----- TAB 4: INSIGHTS -----
with tab4:
    st.subheader("Key Analytical Insights & Findings")
    with st.container():
        st.markdown("""
        1. **Sleep vs. Physical Activity:** Higher daily physical activity generally correlates with better sleep quality scores.
        2. **Occupational Trends:** Certain professions display variations in average sleep duration, indicating workplace lifestyle impact.
        3. **BMI Impact:** Individuals in normal weight ranges show higher average sleep duration and lower stress levels compared to overweight categories.
        """)