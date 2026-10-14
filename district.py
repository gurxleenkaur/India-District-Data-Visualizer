
import json
import re
import html

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="India District Explorer",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #0b1020;
    --glass: rgba(255,255,255,0.075);
    --border: rgba(255,255,255,0.14);
    --text: #f1f5ff;
    --muted: #a7b3cf;
    --cyan: #68e1fd;
    --purple: #b69cff;
    --pink: #ff9ecb;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 5%, rgba(80, 90, 255, .22), transparent 32%),
        radial-gradient(ellipse at 92% 18%, rgba(0, 220, 200, .14), transparent 30%),
        radial-gradient(ellipse at 60% 95%, rgba(200, 80, 255, .14), transparent 35%),
        #0b1020;
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

header[data-testid="stHeader"] {
    background: rgba(11,16,32,.45);
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

h1, h2, h3 {
    font-family: 'Outfit', sans-serif !important;
    color: #f5f7ff !important;
}

p, label, [data-testid="stMarkdownContainer"] {
    color: #e0e7ff;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 35px 36px;
    border: 1px solid rgba(255,255,255,.18);
    border-radius: 30px;
    background: linear-gradient(
        125deg,
        rgba(108,99,255,.23),
        rgba(60,210,220,.10),
        rgba(255,135,190,.12)
    );
    box-shadow: 0 20px 55px rgba(0,0,0,.25),
                inset 0 1px 1px rgba(255,255,255,.18);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    margin-bottom: 25px;
}

.hero:after {
    content: "";
    position: absolute;
    width: 210px;
    height: 210px;
    right: -65px;
    top: -95px;
    border-radius: 48% 52% 63% 37%;
    background: linear-gradient(135deg, #78e8ff66, #b69cff44);
    filter: blur(4px);
}

.eyebrow {
    text-transform: uppercase;
    letter-spacing: 3px;
    color: #85e9ff;
    font-size: 11px;
    font-weight: 700;
}

.hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(30px, 4vw, 48px);
    font-weight: 800;
    line-height: 1.12;
    margin: 10px 0;
    color: #ffffff;
}

.hero-description {
    color: #c2cce4;
    font-size: 15px;
    max-width: 650px;
}

.glass-card {
    border: 1px solid var(--border);
    background: linear-gradient(
        145deg,
        rgba(255,255,255,.10),
        rgba(255,255,255,.035)
    );
    border-radius: 23px;
    padding: 23px;
    box-shadow: 0 12px 35px rgba(0,0,0,.18),
                inset 0 1px 0 rgba(255,255,255,.11);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
}

.kpi-card {
    border-radius: 23px;
    padding: 21px;
    min-height: 142px;
    background: linear-gradient(145deg, #222c47, #141c31);
    border: 1px solid rgba(255,255,255,.10);
    box-shadow: 8px 8px 18px rgba(0,0,0,.22),
                -4px -4px 14px rgba(255,255,255,.035),
                inset 1px 1px 1px rgba(255,255,255,.07);
    transition: transform .25s ease, border-color .25s ease;
}

.kpi-card:hover {
    transform: translateY(-4px);
    border-color: rgba(104,225,253,.45);
}

.kpi-label {
    color: #aab7d5;
    font-size: 12px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.kpi-value {
    color: #ffffff;
    font-family: 'Outfit', sans-serif;
    font-size: clamp(23px, 2.5vw, 32px);
    font-weight: 700;
    margin-top: 10px;
    overflow-wrap: anywhere;
}

.kpi-note {
    font-size: 12px;
    color: #80e5dc;
    margin-top: 5px;
}

.section-label {
    color: #80e5ff;
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: 700;
    text-transform: uppercase;
}

div[data-testid="stPlotlyChart"] {
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 22px;
    padding: 7px;
    background: rgba(255,255,255,.035);
}

div[data-testid="stSelectbox"] > div > div,
div[data-testid="stTextInput"] > div > div {
    background: rgba(255,255,255,.07);
    border: 1px solid rgba(255,255,255,.15);
    border-radius: 13px;
}

div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141b30, #101526);
    border-right: 1px solid rgba(255,255,255,.10);
}

div[data-testid="stSidebar"] * {
    color: #e8edff;
}

.stButton > button,
.stDownloadButton > button {
    border: 1px solid rgba(255,255,255,.20);
    border-radius: 13px;
    color: #ffffff;
    background: linear-gradient(110deg, #6d65f7, #398edb);
    font-weight: 600;
    transition: .2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #9feeff;
    transform: translateY(-2px);
}

div[data-testid="stAlert"] {
    border-radius: 15px;
}

hr {
    border-color: rgba(255,255,255,.12);
}

.footer {
    text-align: center;
    color: #8190b0;
    font-size: 12px;
    padding: 25px 0 5px;
}
</style>
""", unsafe_allow_html=True)


def normalize_name(value):
    """Normalize names to improve joins between census and GeoJSON."""
    value = str(value).strip().casefold()
    return re.sub(r"\s+", " ", value)


def get_center(feature):
    """Approximate center from polygon coordinates."""
    geometry = feature["geometry"]
    coords = geometry["coordinates"]

    if geometry["type"] == "Polygon":
        points = [pt for ring in coords for pt in ring]
    elif geometry["type"] == "MultiPolygon":
        points = [
            pt
            for polygon in coords
            for ring in polygon
            for pt in ring
        ]
    else:
        return {"lat": 22.5, "lon": 80.0}

    if not points:
        return {"lat": 22.5, "lon": 80.0}

    return {
        "lat": sum(pt[1] for pt in points) / len(points),
        "lon": sum(pt[0] for pt in points) / len(points)
    }


def format_number(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:,.0f}"


def make_kpi(label, value, note, accent):
    return f"""
    <div class="kpi-card" style="border-top:3px solid {accent}">
        <div class="kpi-label">{html.escape(str(label))}</div>
        <div class="kpi-value">{html.escape(str(value))}</div>
        <div class="kpi-note">{html.escape(str(note))}</div>
    </div>
    """


def style_chart(fig, height=None):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#e8edff"),
        margin=dict(l=12, r=12, t=40, b=12),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe5ff")
        ),
        colorway=["#68e1fd", "#b69cff", "#ff9ecb", "#80e5b4"],
    )
    if height:
        fig.update_layout(height=height)
    return fig

@st.cache_data
def load_geojson():
    with open("dist[1].geojson", "r", encoding="utf-8") as file:
        return json.load(file)


@st.cache_data
def load_census():
    df = pd.read_csv("census.csv")
    df.columns = df.columns.str.strip()

    required = {"State name", "District name", "Male", "Female"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            "Missing census.csv columns: " + ", ".join(sorted(missing))
        )

    df["State name"] = df["State name"].fillna("").astype(str).str.strip()
    df["District name"] = df["District name"].fillna("").astype(str).str.strip()

    for col in ["Male", "Female"]:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", "", regex=False),
            errors="coerce"
        )

    df["_state_key"] = df["State name"].map(normalize_name)
    df["_district_key"] = df["District name"].map(normalize_name)

    df = df.groupby(
        ["_state_key", "_district_key"],
        as_index=False
    ).agg({
        "State name": "first",
        "District name": "first",
        "Male": "sum",
        "Female": "sum"
    })

    return df


try:
    geojson_data = load_geojson()
    census_df = load_census()
except Exception as error:
    st.error(f"Could not load application data: {error}")
    st.stop()


st.markdown("""
<div class="hero">
    <div class="eyebrow">INDIA • GEOSPATIAL ANALYTICS</div>
    <div class="hero-title">India District Explorer 🇮🇳</div>
    <div class="hero-description">
        Explore India's administrative districts, compare population
        statistics, and discover regional insights through an interactive
        geospatial dashboard.
    </div>
</div>
""", unsafe_allow_html=True)


st.sidebar.markdown("## ✦ Explore India")
st.sidebar.caption("Customize your map and insights.")

features = geojson_data.get("features", [])

states = sorted({
    f.get("properties", {}).get("st_nm", "")
    for f in features
    if f.get("properties", {}).get("st_nm")
})

if not states:
    st.error("No state names were found in the GeoJSON file.")
    st.stop()

if "selected_state" not in st.session_state:
    st.session_state.selected_state = (
        "Andaman and Nicobar Islands"
        if "Andaman and Nicobar Islands" in states
        else states[0]
    )

if st.session_state.selected_state not in states:
    st.session_state.selected_state = states[0]

selected_state = st.sidebar.selectbox(
    "Select state / UT",
    states,
    key="selected_state"
)

state_features = [
    f for f in features
    if f.get("properties", {}).get("st_nm") == selected_state
]

districts = sorted({
    f.get("properties", {}).get("district", "")
    for f in state_features
    if f.get("properties", {}).get("district")
})

if not districts:
    st.warning("No districts found for this state in the GeoJSON.")
    st.stop()

selected_district = st.sidebar.selectbox(
    "Select district",
    districts
)

search_text = st.sidebar.text_input(
    "🔎 Find a district",
    placeholder="Type a district name..."
).strip()

if search_text:
    matches = [
        district for district in districts
        if search_text.casefold() in district.casefold()
    ]

    if matches:
        st.sidebar.caption("Matching districts")
        chosen_match = st.sidebar.selectbox(
            "Choose a search result",
            matches,
            key="search_result"
        )

        if chosen_match != selected_district:
            selected_district = chosen_match
    else:
        st.sidebar.info("No matching district found.")

st.sidebar.divider()
st.sidebar.markdown("### About this dashboard")
st.sidebar.caption(
    "Maps are based on your GeoJSON boundaries. Population figures "
    "come from your census.csv file."
)
st.sidebar.caption("Use the charts and hover over map regions for details.")



df_state = pd.DataFrame({
    "district": [
        f["properties"]["district"] for f in state_features
    ]
})

df_state["_district_key"] = df_state["district"].map(normalize_name)
df_state["_state_key"] = normalize_name(selected_state)

merged_state = df_state.merge(
    census_df[
        ["_state_key", "_district_key", "Male", "Female"]
    ],
    on=["_state_key", "_district_key"],
    how="left"
)

merged_state["Total Population"] = (
    merged_state["Male"] + merged_state["Female"]
)

merged_state["Total Population"] = merged_state[
    "Total Population"
].fillna(0)


merged_state["Population data available"] = (
    merged_state["Male"].notna() & merged_state["Female"].notna()
)

state_geojson = {
    "type": "FeatureCollection",
    "features": state_features
}

selected_key = normalize_name(selected_district)

selected_rows = merged_state[
    merged_state["_district_key"] == selected_key
]

male = selected_rows["Male"].iloc[0] if not selected_rows.empty else None
female = selected_rows["Female"].iloc[0] if not selected_rows.empty else None

if male is not None and female is not None and pd.notna(male) and pd.notna(female):
    district_total = male + female
else:
    district_total = None

known_total = merged_state.loc[
    merged_state["Population data available"],
    "Total Population"
].sum()

known_male = merged_state["Male"].sum(min_count=1)
known_female = merged_state["Female"].sum(min_count=1)

data_coverage = int(
    merged_state["Population data available"].sum()
)


st.markdown('<div class="section-label">01 / QUICK OVERVIEW</div>',
            unsafe_allow_html=True)
st.markdown("### At a glance")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        make_kpi("State / UT", selected_state, "Currently exploring", "#68e1fd"),
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        make_kpi("Districts", len(districts), "Mapped administrative areas", "#b69cff"),
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        make_kpi(
            "Selected population",
            format_number(district_total) if district_total is not None else "N/A",
            selected_district,
            "#ff9ecb"
        ),
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        make_kpi(
            "Data coverage",
            f"{data_coverage}/{len(districts)}",
            "Districts with both population values",
            "#80e5b4"
        ),
        unsafe_allow_html=True
    )

st.caption(
    "Population totals include only districts with available male and female "
    "figures. These are the totals in your supplied dataset, not necessarily "
    "current population estimates."
)


st.markdown('<div class="section-label">02 / GEOGRAPHY</div>',
            unsafe_allow_html=True)
st.markdown("### Explore the map")

map_mode = st.radio(
    "Map coloring",
    ["Uniform color", "Total population"],
    horizontal=True
)

map_color = (
    "Total Population"
    if map_mode == "Total population"
    else None
)

left, right = st.columns([1.25, 1])

with left:
    st.markdown("#### 🗺️ State / UT view")

    center = get_center(state_features[0])

    if map_color:
        map_df = merged_state.copy()
        map_df.loc[
            ~map_df["Population data available"],
            "Total Population"
        ] = None
        map_color_scale = "Viridis"
    else:
        map_df = merged_state.copy()
        map_df["Map color"] = "District"
        map_color = "Map color"
        map_color_scale = ["#4689f5", "#4689f5"]

    fig_state = px.choropleth_map(
        map_df,
        geojson=state_geojson,
        locations="district",
        featureidkey="properties.district",
        color=map_color,
        hover_name="district",
        hover_data={
            "Male": ":,.0f",
            "Female": ":,.0f",
            "Total Population": ":,.0f",
            "Population data available": True,
            "Map color": False
        } if not map_mode == "Total population" else {
            "Male": ":,.0f",
            "Female": ":,.0f",
            "Total Population": ":,.0f",
            "Population data available": True
        },
        color_continuous_scale=map_color_scale,
        map_style="carto-darkmatter",
        center=center,
        zoom=4.3,
        opacity=0.78,
        height=510
    )

    fig_state.update_layout(
        margin=dict(l=0, r=0, t=5, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#e8edff"
    )
    fig_state.update_coloraxes(showscale=(map_mode == "Total population"))
    st.plotly_chart(fig_state, use_container_width=True)

with right:
    st.markdown(f"#### 📍 {selected_district}")

    district_feature = [
        f for f in state_features
        if normalize_name(f["properties"]["district"]) == selected_key
    ]

    if district_feature:
        district_geojson = {
            "type": "FeatureCollection",
            "features": district_feature
        }

        district_map_df = pd.DataFrame({
            "district": [selected_district],
            "Population": [
                district_total if district_total is not None else 0
            ],
            "Male": [male],
            "Female": [female]
        })

        fig_district = px.choropleth_map(
            district_map_df,
            geojson=district_geojson,
            locations="district",
            featureidkey="properties.district",
            color="Population",
            hover_name="district",
            hover_data={
                "Male": ":,.0f",
                "Female": ":,.0f",
                "Population": ":,.0f"
            },
            color_continuous_scale=["#f39c12", "#ff72b6"],
            map_style="carto-darkmatter",
            center=get_center(district_feature[0]),
            zoom=6.7,
            opacity=0.85,
            height=510
        )

        fig_district.update_layout(
            margin=dict(l=0, r=0, t=5, b=0),
            paper_bgcolor="rgba(0,0,0,0)"
        )
        fig_district.update_coloraxes(showscale=False)
        st.plotly_chart(fig_district, use_container_width=True)

        if district_total is None:
            st.warning("Population information is unavailable for this district.")
    else:
        st.warning("District boundary not found.")



st.markdown('<div class="section-label">03 / DATA INSIGHTS</div>',
            unsafe_allow_html=True)
st.markdown("### Population analytics")

chart1, chart2 = st.columns(2)

with chart1:
    st.markdown("#### Male vs female population")

    gender_df = pd.DataFrame({
        "Category": ["Male", "Female"],
        "Population": [male, female]
    })

    gender_df = gender_df.dropna(subset=["Population"])

    if not gender_df.empty and gender_df["Population"].sum() > 0:
        fig_gender = px.pie(
            gender_df,
            names="Category",
            values="Population",
            hole=0.68,
            color="Category",
            color_discrete_map={
                "Male": "#68e1fd",
                "Female": "#ff9ecb"
            }
        )
        fig_gender.update_traces(
            textposition="inside",
            textinfo="percent",
            marker=dict(line=dict(color="#11182b", width=3))
        )
        fig_gender.update_layout(
            annotations=[dict(
                text="GENDER<br>SHARE",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=13, color="#e8edff")
            )]
        )
        st.plotly_chart(style_chart(fig_gender, 350), use_container_width=True)
    else:
        st.info("No population data available for the selected district.")

with chart2:
    st.markdown("#### District population comparison")

    comparison_df = merged_state[
        merged_state["Population data available"]
    ].copy()

    comparison_df = comparison_df.sort_values(
        "Total Population", ascending=False
    ).head(10)

    if not comparison_df.empty:
        fig_bar = px.bar(
            comparison_df.sort_values("Total Population"),
            x="Total Population",
            y="district",
            orientation="h",
            labels={
                "Total Population": "Population",
                "district": "District"
            },
            color="Total Population",
            color_continuous_scale=["#7567ff", "#68e1fd"]
        )
        fig_bar.update_layout(showlegend=False)
        fig_bar.update_coloraxes(showscale=False)
        st.plotly_chart(style_chart(fig_bar, 350), use_container_width=True)
    else:
        st.info("No district population data available for comparison.")


st.markdown('<div class="section-label">04 / DATA EXPLORER</div>',
            unsafe_allow_html=True)
st.markdown("### District data")

show_all = st.checkbox("Show all districts in this state", value=True)

display_df = merged_state[
    [
        "district",
        "Male",
        "Female",
        "Total Population",
        "Population data available"
    ]
].copy()

display_df = display_df.rename(columns={
    "district": "District",
    "Male": "Male Population",
    "Female": "Female Population",
    "Total Population": "Total Population",
    "Population data available": "Data Available"
})

if not show_all:
    display_df = display_df[
        display_df["District"].map(normalize_name) == selected_key
    ]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Male Population": st.column_config.NumberColumn(format="%d"),
        "Female Population": st.column_config.NumberColumn(format="%d"),
        "Total Population": st.column_config.NumberColumn(format="%d"),
        "Data Available": st.column_config.CheckboxColumn()
    }
)

download_csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download district data as CSV",
    data=download_csv,
    file_name=f"{selected_state.replace(' ', '_')}_district_data.csv",
    mime="text/csv",
    use_container_width=False
)


st.markdown("""
<div class="footer">
    INDIA DISTRICT EXPLORER · GEOSPATIAL DATA & ANALYTICS<br>
    Built with Streamlit · Plotly · Pandas
</div>
""", unsafe_allow_html=True)
