"""
Parcl Real Estate – Buyer Segmentation & Investment Profiling Dashboard
Production-ready Streamlit application
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram, linkage
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# -----------------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Parcl | Buyer Segmentation Intelligence",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f766e 100%);
        padding: 1.8rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 1.9rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        margin: 0.4rem 0 0 0;
        opacity: 0.85;
        font-size: 0.95rem;
    }
    
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    
    .segment-card {
        background: #f8fafc;
        border-left: 4px solid #0f766e;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
    }
    
    div[data-testid="stSidebar"] {
        background: #f1f5f9;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #ecfdf5 0%, #f0fdfa 100%);
        border: 1px solid #99f6e4;
        border-radius: 10px;
        padding: 1rem 1.3rem;
        margin: 0.8rem 0;
        color: #134e4a !important;
    }
    
    .insight-box b {
        color: #0f766e !important;
    }
    
    /* Force readable text in dark mode / Streamlit theme overrides */
    .insight-box, .insight-box * {
        color: #134e4a !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING & FEATURE ENGINEERING
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner="Loading and preparing data...")
def load_and_prepare_data():
    import os
    base = os.path.dirname(os.path.abspath(__file__))
    clients = pd.read_csv(os.path.join(base, "clients.csv"))
    props = pd.read_csv(os.path.join(base, "properties.csv"))

    # --- Clean clients ---
    clients = clients.drop_duplicates(subset=["client_id"])
    clients["loan_applied"] = clients["loan_applied"].map({"Yes": 1, "No": 0})
    clients["client_type"] = clients["client_type"].replace({"Company": "Corporate"})

    # Parse date of birth → age
    def parse_dob(x):
        for fmt in ("%m-%d-%Y", "%m/%d/%Y", "%Y-%m-%d", "%d-%m-%Y"):
            try:
                return datetime.strptime(str(x).strip(), fmt)
            except Exception:
                continue
        return pd.NaT

    clients["dob"] = clients["date_of_birth"].apply(parse_dob)
    clients["age"] = ((datetime(2026, 1, 1) - clients["dob"]).dt.days / 365.25).round(0)
    clients["age"] = clients["age"].fillna(clients["age"].median()).astype(int)

    # --- Clean properties ---
    props["sale_price_clean"] = (
        props["sale_price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .replace("nan", np.nan)
    )
    props["sale_price_clean"] = pd.to_numeric(props["sale_price_clean"], errors="coerce")

    # Aggregate property features per client
    sold = props[props["listing_status"] == "Sold"].copy()
    agg = sold.groupby("client_ref").agg(
        total_purchases=("listing_id", "count"),
        total_spend=("sale_price_clean", "sum"),
        avg_unit_price=("sale_price_clean", "mean"),
        avg_floor_area=("floor_area_sqft", "mean"),
        apartment_count=("unit_category", lambda x: (x == "Apartment").sum()),
        office_count=("unit_category", lambda x: (x == "Office").sum()),
    ).reset_index()
    agg.rename(columns={"client_ref": "client_id"}, inplace=True)

    # Merge
    df = clients.merge(agg, on="client_id", how="left")
    for col in ["total_purchases", "total_spend", "avg_unit_price", "avg_floor_area",
                "apartment_count", "office_count"]:
        df[col] = df[col].fillna(0)

    df["spend_per_purchase"] = np.where(
        df["total_purchases"] > 0,
        df["total_spend"] / df["total_purchases"],
        0
    )

    return df, props

@st.cache_data(show_spinner="Running clustering pipeline...")
def run_clustering(df):
    # Features for clustering
    cat_cols = ["client_type", "gender", "country", "region",
                "acquisition_purpose", "referral_channel"]
    num_cols = ["age", "satisfaction_score", "loan_applied",
                "total_purchases", "total_spend", "avg_unit_price",
                "avg_floor_area", "apartment_count", "office_count"]

    # Encode categoricals
    df_enc = df.copy()
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df_enc[col + "_enc"] = le.fit_transform(df_enc[col].astype(str))
        encoders[col] = le

    feature_cols = [c + "_enc" for c in cat_cols] + num_cols
    X = df_enc[feature_cols].values

    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Elbow & Silhouette for k=2..8
    inertias = []
    silhouettes = []
    K_range = range(2, 9)
    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=20)
        labels = km.fit_predict(X_scaled)
        inertias.append(km.inertia_)
        silhouettes.append(silhouette_score(X_scaled, labels))

    # Final KMeans k=4
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=30)
    df_enc["cluster"] = kmeans.fit_predict(X_scaled)

    # Hierarchical (for validation)
    hier = AgglomerativeClustering(n_clusters=4, linkage="ward")
    df_enc["cluster_hier"] = hier.fit_predict(X_scaled)

    # PCA for 2D projection
    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(X_scaled)
    df_enc["pca1"] = coords[:, 0]
    df_enc["pca2"] = coords[:, 1]

    # Map clusters to business names based on characteristics
    cluster_profiles = df_enc.groupby("cluster").agg({
        "acquisition_purpose": lambda x: (x == "Investment").mean(),
        "loan_applied": "mean",
        "age": "mean",
        "total_spend": "mean",
        "client_type": lambda x: (x == "Corporate").mean(),
        "satisfaction_score": "mean",
        "avg_unit_price": "mean",
    })

    # Heuristic mapping
    mapping = {}
    remaining = set(range(4))

    # Global Investors: high investment purpose + high spend
    inv_score = cluster_profiles["acquisition_purpose"] * cluster_profiles["total_spend"]
    c = inv_score.idxmax()
    mapping[c] = "Global Investors"
    remaining.discard(c)

    # First-Time Buyers: younger + high loan
    ft_score = (1 / (cluster_profiles["age"] + 1)) * cluster_profiles["loan_applied"]
    c = ft_score[list(remaining)].idxmax()
    mapping[c] = "First-Time Buyers"
    remaining.discard(c)

    # Corporate Buyers: high corporate share
    corp_score = cluster_profiles["client_type"]
    c = corp_score[list(remaining)].idxmax()
    mapping[c] = "Corporate Buyers"
    remaining.discard(c)

    # Luxury Investors: remaining (high satisfaction / price)
    mapping[list(remaining)[0]] = "Luxury Investors"

    df_enc["segment"] = df_enc["cluster"].map(mapping)

    # Colors
    segment_colors = {
        "Global Investors": "#0f766e",
        "First-Time Buyers": "#2563eb",
        "Corporate Buyers": "#7c3aed",
        "Luxury Investors": "#d97706",
    }

    return (
        df_enc,
        inertias,
        silhouettes,
        list(K_range),
        segment_colors,
        kmeans,
        scaler,
        feature_cols,
        pca,
    )

# -----------------------------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------------------------
df_raw, props_raw = load_and_prepare_data()
(
    df,
    inertias,
    silhouettes,
    k_range,
    SEGMENT_COLORS,
    kmeans_model,
    scaler,
    feature_cols,
    pca_model,
) = run_clustering(df_raw)

# -----------------------------------------------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------------------------------------------
st.sidebar.markdown("### 🔍 Filters")
st.sidebar.markdown("---")

countries = sorted(df["country"].unique())
regions = sorted(df["region"].unique())
purposes = sorted(df["acquisition_purpose"].unique())
client_types = sorted(df["client_type"].unique())
segments = sorted(df["segment"].unique())

sel_country = st.sidebar.multiselect("Country", countries, default=countries)
sel_region = st.sidebar.multiselect("Region", regions, default=regions)
sel_purpose = st.sidebar.multiselect("Acquisition Purpose", purposes, default=purposes)
sel_ctype = st.sidebar.multiselect("Client Type", client_types, default=client_types)
sel_segment = st.sidebar.multiselect("Segment", segments, default=segments)

# Apply filters
mask = (
    df["country"].isin(sel_country)
    & df["region"].isin(sel_region)
    & df["acquisition_purpose"].isin(sel_purpose)
    & df["client_type"].isin(sel_ctype)
    & df["segment"].isin(sel_segment)
)
fdf = df[mask].copy()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Showing {len(fdf):,} of {len(df):,} clients**")
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="font-size:0.8rem;color:#64748b;">
    Built for Parcl Market Intelligence<br>
    Clustering: K-Means (k=4) + Hierarchical validation
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="main-header">
        <h1>🏢 Parcl Buyer Segmentation & Investment Profiling</h1>
        <p>AI-driven customer intelligence • Discover hidden buyer segments • Optimize marketing & targeting</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "👥 Segment Insights",
    "📈 Investor Behavior",
    "🌍 Geographic Analysis",
    "🔬 Model Diagnostics",
    "📋 Data Explorer",
])

# =============================================================================
# TAB 1 – OVERVIEW
# =============================================================================
with tab1:
    st.subheader("Buyer Segmentation Overview")

    # KPI row
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Clients", f"{len(fdf):,}")
    c2.metric("Segments", fdf["segment"].nunique())
    c3.metric("Avg Satisfaction", f"{fdf['satisfaction_score'].mean():.2f}/5")
    c4.metric("Investment Buyers", f"{(fdf['acquisition_purpose']=='Investment').mean()*100:.1f}%")
    c5.metric("Loan Dependent", f"{fdf['loan_applied'].mean()*100:.1f}%")

    st.markdown("---")

    col_left, col_right = st.columns([1.1, 1])

    with col_left:
        # Cluster distribution pie
        seg_counts = fdf["segment"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Count"]
        fig_pie = px.pie(
            seg_counts,
            names="Segment",
            values="Count",
            color="Segment",
            color_discrete_map=SEGMENT_COLORS,
            hole=0.45,
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie.update_layout(
            title="Segment Distribution",
            margin=dict(t=40, b=20, l=20, r=20),
            height=380,
            showlegend=False,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        # PCA scatter
        fig_pca = px.scatter(
            fdf,
            x="pca1",
            y="pca2",
            color="segment",
            color_discrete_map=SEGMENT_COLORS,
            hover_data=["client_id", "age", "country", "total_spend"],
            opacity=0.7,
        )
        fig_pca.update_layout(
            title="Cluster Separation (PCA Projection)",
            xaxis_title="Principal Component 1",
            yaxis_title="Principal Component 2",
            margin=dict(t=40, b=20, l=20, r=20),
            height=380,
            legend_title="Segment",
        )
        st.plotly_chart(fig_pca, use_container_width=True)

    # Quick segment cards
    st.markdown("#### Segment Snapshots")
    cols = st.columns(4)
    for i, seg in enumerate(["Global Investors", "First-Time Buyers", "Corporate Buyers", "Luxury Investors"]):
        if seg not in fdf["segment"].values:
            continue
        sdf = fdf[fdf["segment"] == seg]
        with cols[i]:
            color = SEGMENT_COLORS.get(seg, "#64748b")
            st.markdown(
                f"""
                <div style="background:#f8fafc;border-left:5px solid {color};border-radius:8px;padding:1rem;">
                    <div style="font-weight:600;color:{color};font-size:0.95rem;">{seg}</div>
                    <div style="font-size:1.6rem;font-weight:700;margin:0.3rem 0;">{len(sdf):,}</div>
                    <div style="font-size:0.8rem;color:#64748b;">
                        Avg Age: {sdf['age'].mean():.0f}<br>
                        Investment: {(sdf['acquisition_purpose']=='Investment').mean()*100:.0f}%<br>
                        Loan Rate: {sdf['loan_applied'].mean()*100:.0f}%
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# =============================================================================
# TAB 2 – SEGMENT INSIGHTS
# =============================================================================
with tab2:
    st.subheader("Deep Segment Insights")

    selected_seg = st.selectbox(
        "Select Segment to Analyze",
        options=sorted(fdf["segment"].unique()),
        key="seg_select",
    )
    sdf = fdf[fdf["segment"] == selected_seg]
    color = SEGMENT_COLORS.get(selected_seg, "#0f766e")

    # KPIs
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Clients", f"{len(sdf):,}")
    k2.metric("Avg Age", f"{sdf['age'].mean():.1f}")
    k3.metric("Avg Satisfaction", f"{sdf['satisfaction_score'].mean():.2f}")
    k4.metric("Total Spend", f"${sdf['total_spend'].sum():,.0f}")
    k5.metric("Avg Unit Price", f"${sdf['avg_unit_price'].mean():,.0f}")

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        # Purpose breakdown
        purpose_df = sdf["acquisition_purpose"].value_counts().reset_index()
        purpose_df.columns = ["Purpose", "Count"]
        fig = px.bar(
            purpose_df,
            x="Purpose",
            y="Count",
            color_discrete_sequence=[color],
            text="Count",
        )
        fig.update_layout(title="Acquisition Purpose", height=320, margin=dict(t=40))
        st.plotly_chart(fig, use_container_width=True)

        # Client type
        ct_df = sdf["client_type"].value_counts().reset_index()
        ct_df.columns = ["Type", "Count"]
        fig = px.pie(ct_df, names="Type", values="Count", hole=0.4,
                     color_discrete_sequence=[color, "#94a3b8"])
        fig.update_layout(title="Client Type Mix", height=320, margin=dict(t=40))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Loan
        loan_df = sdf["loan_applied"].map({1: "Yes", 0: "No"}).value_counts().reset_index()
        loan_df.columns = ["Loan Applied", "Count"]
        fig = px.bar(loan_df, x="Loan Applied", y="Count",
                     color_discrete_sequence=[color], text="Count")
        fig.update_layout(title="Financing Behavior", height=320, margin=dict(t=40))
        st.plotly_chart(fig, use_container_width=True)

        # Referral channel
        ref_df = sdf["referral_channel"].value_counts().reset_index()
        ref_df.columns = ["Channel", "Count"]
        fig = px.bar(ref_df, x="Channel", y="Count",
                     color_discrete_sequence=[color], text="Count")
        fig.update_layout(title="Referral Channel", height=320, margin=dict(t=40))
        st.plotly_chart(fig, use_container_width=True)

    # Demographic profile
    st.markdown("#### Demographic & Behavioral Profile")
    p1, p2, p3 = st.columns(3)
    with p1:
        fig = px.histogram(sdf, x="age", nbins=20, color_discrete_sequence=[color])
        fig.update_layout(title="Age Distribution", height=280, margin=dict(t=40))
        st.plotly_chart(fig, use_container_width=True)
    with p2:
        fig = px.histogram(sdf, x="satisfaction_score", nbins=5,
                           color_discrete_sequence=[color])
        fig.update_layout(title="Satisfaction Score", height=280, margin=dict(t=40))
        st.plotly_chart(fig, use_container_width=True)
    with p3:
        fig = px.histogram(sdf, x="total_purchases", nbins=10,
                           color_discrete_sequence=[color])
        fig.update_layout(title="Purchases per Client", height=280, margin=dict(t=40))
        st.plotly_chart(fig, use_container_width=True)

    # Descriptive stats table
    st.markdown("#### Descriptive Statistics")
    stats = sdf[["age", "satisfaction_score", "total_purchases", "total_spend",
                 "avg_unit_price", "avg_floor_area", "loan_applied"]].describe().T
    stats = stats[["count", "mean", "std", "min", "25%", "50%", "75%", "max"]].round(2)
    st.dataframe(stats, use_container_width=True)

# =============================================================================
# TAB 3 – INVESTOR BEHAVIOR
# =============================================================================
with tab3:
    st.subheader("Investor Behavior Dashboard")

    # Comparison across segments
    st.markdown("#### Cross-Segment Comparison")

    comp = fdf.groupby("segment").agg(
        clients=("client_id", "count"),
        avg_age=("age", "mean"),
        investment_pct=("acquisition_purpose", lambda x: (x == "Investment").mean() * 100),
        loan_pct=("loan_applied", "mean"),
        avg_satisfaction=("satisfaction_score", "mean"),
        avg_spend=("total_spend", "mean"),
        avg_purchases=("total_purchases", "mean"),
        avg_unit_price=("avg_unit_price", "mean"),
        corporate_pct=("client_type", lambda x: (x == "Corporate").mean() * 100),
    ).reset_index()

    # Radar-style multi metrics
    m1, m2 = st.columns(2)

    with m1:
        fig = px.bar(
            comp,
            x="segment",
            y="avg_spend",
            color="segment",
            color_discrete_map=SEGMENT_COLORS,
            text=comp["avg_spend"].apply(lambda x: f"${x:,.0f}"),
        )
        fig.update_layout(
            title="Average Total Spend by Segment",
            showlegend=False,
            height=360,
            xaxis_title="",
            yaxis_title="Avg Spend ($)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with m2:
        fig = px.bar(
            comp,
            x="segment",
            y="avg_unit_price",
            color="segment",
            color_discrete_map=SEGMENT_COLORS,
            text=comp["avg_unit_price"].apply(lambda x: f"${x:,.0f}"),
        )
        fig.update_layout(
            title="Average Unit Price by Segment",
            showlegend=False,
            height=360,
            xaxis_title="",
            yaxis_title="Avg Unit Price ($)",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Investment vs Loan behavior
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(
            comp,
            x="segment",
            y="investment_pct",
            color="segment",
            color_discrete_map=SEGMENT_COLORS,
            text=comp["investment_pct"].apply(lambda x: f"{x:.0f}%"),
        )
        fig.update_layout(
            title="% Investment Purpose",
            showlegend=False,
            height=340,
            xaxis_title="",
            yaxis_title="%",
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.bar(
            comp,
            x="segment",
            y="loan_pct",
            color="segment",
            color_discrete_map=SEGMENT_COLORS,
            text=comp["loan_pct"].apply(lambda x: f"{x*100:.0f}%"),
        )
        fig.update_layout(
            title="% Using Loan Financing",
            showlegend=False,
            height=340,
            xaxis_title="",
            yaxis_title="Loan Rate",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Spend vs Age scatter
    st.markdown("#### Spend vs Age by Segment")
    fig = px.scatter(
        fdf,
        x="age",
        y="total_spend",
        color="segment",
        color_discrete_map=SEGMENT_COLORS,
        size="total_purchases",
        hover_data=["client_id", "country", "acquisition_purpose"],
        opacity=0.65,
    )
    fig.update_layout(
        height=420,
        xaxis_title="Age",
        yaxis_title="Total Spend ($)",
        legend_title="Segment",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Comparison table
    st.markdown("#### Segment Comparison Table")
    display_comp = comp.copy()
    display_comp["avg_age"] = display_comp["avg_age"].round(1)
    display_comp["investment_pct"] = display_comp["investment_pct"].round(1)
    display_comp["loan_pct"] = (display_comp["loan_pct"] * 100).round(1)
    display_comp["avg_satisfaction"] = display_comp["avg_satisfaction"].round(2)
    display_comp["avg_spend"] = display_comp["avg_spend"].round(0)
    display_comp["avg_purchases"] = display_comp["avg_purchases"].round(2)
    display_comp["avg_unit_price"] = display_comp["avg_unit_price"].round(0)
    display_comp["corporate_pct"] = display_comp["corporate_pct"].round(1)
    display_comp.columns = [
        "Segment", "Clients", "Avg Age", "Investment %", "Loan %",
        "Avg Satisfaction", "Avg Spend", "Avg Purchases", "Avg Unit Price", "Corporate %"
    ]
    st.dataframe(display_comp, use_container_width=True, hide_index=True)

# =============================================================================
# TAB 4 – GEOGRAPHIC ANALYSIS
# =============================================================================
with tab4:
    st.subheader("Geographic Buyer Analysis")

    # Country distribution by segment
    st.markdown("#### Buyer Segments by Country")
    country_seg = (
        fdf.groupby(["country", "segment"])
        .size()
        .reset_index(name="count")
    )
    fig = px.bar(
        country_seg,
        x="country",
        y="count",
        color="segment",
        color_discrete_map=SEGMENT_COLORS,
        barmode="stack",
    )
    fig.update_layout(
        height=400,
        xaxis_title="Country",
        yaxis_title="Number of Clients",
        legend_title="Segment",
        xaxis={"categoryorder": "total descending"},
    )
    st.plotly_chart(fig, use_container_width=True)

    # Region analysis
    st.markdown("#### Regional Distribution")
    c1, c2 = st.columns(2)

    with c1:
        region_counts = fdf["region"].value_counts().head(12).reset_index()
        region_counts.columns = ["Region", "Clients"]
        fig = px.bar(
            region_counts,
            x="Clients",
            y="Region",
            orientation="h",
            color_discrete_sequence=["#0f766e"],
        )
        fig.update_layout(
            title="Top Regions by Client Count",
            height=400,
            yaxis={"categoryorder": "total ascending"},
            margin=dict(l=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        region_seg = (
            fdf.groupby(["region", "segment"])
            .size()
            .reset_index(name="count")
        )
        top_regions = fdf["region"].value_counts().head(8).index.tolist()
        region_seg = region_seg[region_seg["region"].isin(top_regions)]
        fig = px.bar(
            region_seg,
            x="region",
            y="count",
            color="segment",
            color_discrete_map=SEGMENT_COLORS,
            barmode="group",
        )
        fig.update_layout(
            title="Segment Mix in Top Regions",
            height=400,
            xaxis_title="",
            yaxis_title="Clients",
            legend_title="Segment",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Heatmap: Region × Segment
    st.markdown("#### Region × Segment Heatmap")
    pivot = pd.crosstab(fdf["region"], fdf["segment"])
    # Keep top regions
    pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).head(15).index]
    fig = px.imshow(
        pivot,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Teal",
    )
    fig.update_layout(height=450, xaxis_title="Segment", yaxis_title="Region")
    st.plotly_chart(fig, use_container_width=True)

    # Country level spend
    st.markdown("#### Average Spend by Country & Segment")
    spend_geo = (
        fdf.groupby(["country", "segment"])["total_spend"]
        .mean()
        .reset_index()
    )
    fig = px.bar(
        spend_geo,
        x="country",
        y="total_spend",
        color="segment",
        color_discrete_map=SEGMENT_COLORS,
        barmode="group",
    )
    fig.update_layout(
        height=400,
        xaxis_title="Country",
        yaxis_title="Avg Total Spend ($)",
        legend_title="Segment",
        xaxis={"categoryorder": "total descending"},
    )
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# TAB 5 – MODEL DIAGNOSTICS
# =============================================================================
with tab5:
    st.subheader("Model Diagnostics & Validation")

    st.markdown(
        """
        <div class="insight-box">
        <b>Methodology Summary</b><br>
        • Features: client demographics, acquisition purpose, financing, referral channel + 
        aggregated property behavior (purchases, spend, unit price, floor area)<br>
        • Encoding: Label Encoding for categoricals<br>
        • Scaling: StandardScaler<br>
        • Algorithms: K-Means (primary) + Agglomerative Hierarchical (validation)<br>
        • Optimal k selected via Elbow Method + Silhouette Score
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        # Elbow
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(k_range),
            y=inertias,
            mode="lines+markers",
            marker=dict(size=10, color="#0f766e"),
            line=dict(width=2.5, color="#0f766e"),
        ))
        fig.add_vline(x=4, line_dash="dash", line_color="#d97706",
                      annotation_text="Selected k=4")
        fig.update_layout(
            title="Elbow Method – Inertia vs k",
            xaxis_title="Number of Clusters (k)",
            yaxis_title="Inertia",
            height=360,
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Silhouette
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(k_range),
            y=silhouettes,
            mode="lines+markers",
            marker=dict(size=10, color="#2563eb"),
            line=dict(width=2.5, color="#2563eb"),
        ))
        fig.add_vline(x=4, line_dash="dash", line_color="#d97706",
                      annotation_text="Selected k=4")
        fig.update_layout(
            title="Silhouette Score vs k",
            xaxis_title="Number of Clusters (k)",
            yaxis_title="Silhouette Score",
            height=360,
        )
        st.plotly_chart(fig, use_container_width=True)

    # Agreement between KMeans and Hierarchical
    st.markdown("#### K-Means vs Hierarchical Agreement")
    agreement = (df["cluster"] == df["cluster_hier"]).mean() * 100
    st.metric("Label Agreement Rate", f"{agreement:.1f}%")

    conf = pd.crosstab(df["cluster"], df["cluster_hier"],
                       rownames=["K-Means"], colnames=["Hierarchical"])
    fig = px.imshow(conf, text_auto=True, aspect="auto",
                    color_continuous_scale="Blues")
    fig.update_layout(title="Cluster Assignment Crosstab", height=350)
    st.plotly_chart(fig, use_container_width=True)

    # Feature importance proxy (cluster center variance)
    st.markdown("#### Feature Importance (Cluster Separation Strength)")
    centers = kmeans_model.cluster_centers_
    feature_var = centers.var(axis=0)
    imp_df = pd.DataFrame({
        "Feature": feature_cols,
        "Separation Strength": feature_var,
    }).sort_values("Separation Strength", ascending=True)

    # Clean names
    imp_df["Feature"] = (
        imp_df["Feature"]
        .str.replace("_enc", "")
        .str.replace("_", " ")
        .str.title()
    )

    fig = px.bar(
        imp_df,
        x="Separation Strength",
        y="Feature",
        orientation="h",
        color_discrete_sequence=["#0f766e"],
    )
    fig.update_layout(height=480, margin=dict(l=10))
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# TAB 6 – DATA EXPLORER
# =============================================================================
with tab6:
    st.subheader("Data Explorer")

    st.markdown("#### Filtered Client Data")
    show_cols = [
        "client_id", "client_type", "gender", "age", "country", "region",
        "acquisition_purpose", "loan_applied", "referral_channel",
        "satisfaction_score", "total_purchases", "total_spend",
        "avg_unit_price", "segment",
    ]
    st.dataframe(
        fdf[show_cols].sort_values("total_spend", ascending=False),
        use_container_width=True,
        height=420,
    )

    st.markdown("#### Download Filtered Data")
    csv = fdf[show_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="parcl_buyer_segments_filtered.csv",
        mime="text/csv",
    )

    st.markdown("---")
    st.markdown("#### Segment Definitions (Business Mapping)")
    st.markdown(
        """
        | Segment | Typical Profile |
        |---------|-----------------|
        | **Global Investors** | High investment-purpose share, elevated total spend, international footprint |
        | **First-Time Buyers** | Younger age profile, high loan dependency, primarily personal-use (Home) purchases |
        | **Corporate Buyers** | Elevated share of Corporate client type, multi-unit purchasing patterns |
        | **Luxury Investors** | Higher average unit prices / satisfaction, lower loan reliance, premium positioning |
        """
    )

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center;color:#94a3b8;font-size:0.8rem;padding:0.5rem 0 1rem 0;">
        Parcl Market Intelligence Platform • Buyer Segmentation Engine v1.0<br>
        Data Science Pipeline: Cleaning → Encoding → Scaling → K-Means / Hierarchical Clustering → Interpretation
    </div>
    """,
    unsafe_allow_html=True,
)
