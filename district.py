
import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Load files
with open("dist[1].geojson", "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

census_df = pd.read_csv("census.csv")
census_df.columns = census_df.columns.str.strip()

# Validate required columns
required_columns = {"State name", "District name", "Male", "Female"}
missing_columns = required_columns - set(census_df.columns)

if missing_columns:
    st.error(f"Missing columns in census.csv: {', '.join(sorted(missing_columns))}")
    st.stop()

# Clean names for reliable matching
census_df["State name"] = census_df["State name"].astype(str).str.strip()
census_df["District name"] = census_df["District name"].astype(str).str.strip()

# Calculate approximate map center
def get_center(feature):
    coords = feature["geometry"]["coordinates"]

    if feature["geometry"]["type"] == "Polygon":
        flat = [pt for ring in coords for pt in ring]
    elif feature["geometry"]["type"] == "MultiPolygon":
        flat = [
            pt
            for polygon in coords
            for ring in polygon
            for pt in ring
        ]
    else:
        return {"lat": 22.5, "lon": 80.0}

    if not flat:
        return {"lat": 22.5, "lon": 80.0}

    lats = [pt[1] for pt in flat]
    lons = [pt[0] for pt in flat]

    return {
        "lat": sum(lats) / len(lats),
        "lon": sum(lons) / len(lons)
    }


# App title
st.title("📍 Indian District Map")

states = sorted({
    f["properties"]["st_nm"]
    for f in geojson_data["features"]
})

col1, col2 = st.columns(2)

with col1:
    selected_state = st.selectbox("Select State", states)

state_features = [
    f for f in geojson_data["features"]
    if f["properties"]["st_nm"] == selected_state
]

districts = sorted({
    f["properties"]["district"]
    for f in state_features
})

with col2:
    selected_district = st.selectbox("Select District", districts)

# Prepare state GeoJSON
state_geojson = {
    "type": "FeatureCollection",
    "features": state_features
}

df_state = pd.DataFrame({
    "district": [f["properties"]["district"] for f in state_features],
    "state": [selected_state] * len(state_features),
    "metric": [1] * len(state_features)
})

# Merge on BOTH state and district
census_for_merge = census_df.rename(columns={
    "State name": "state",
    "District name": "district",
    "Male": "Male Population",
    "Female": "Female Population"
})

merged_state = df_state.merge(
    census_for_merge[
        ["state", "district", "Male Population", "Female Population"]
    ],
    on=["state", "district"],
    how="left"
)

# Display maps
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"🗺️ State Map: {selected_state}")

    center = get_center(state_features[0])

    fig_state = px.choropleth_map(
        merged_state,
        geojson=state_geojson,
        locations="district",
        featureidkey="properties.district",
        color="metric",
        hover_data={
            "Male Population": True,
            "Female Population": True,
            "metric": False
        },
        color_continuous_scale=["#3498DB", "#3498DB"],
        range_color=(0, 2),
        map_style="carto-positron",
        center=center,
        zoom=5,
        opacity=0.6,
        height=500
    )

    fig_state.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    fig_state.update_coloraxes(showscale=False)
    st.plotly_chart(fig_state, use_container_width=True)

with col2:
    st.subheader(f"📌 District Map: {selected_district}")

    district_feature = [
        f for f in state_features
        if f["properties"]["district"] == selected_district
    ]

    if district_feature:
        district_geojson = {
            "type": "FeatureCollection",
            "features": district_feature
        }

        center_district = get_center(district_feature[0])

        pop_row = census_df[
            (census_df["State name"].str.casefold() ==
             selected_state.strip().casefold()) &
            (census_df["District name"].str.casefold() ==
             selected_district.strip().casefold())
        ]

        if not pop_row.empty:
            male = pop_row.iloc[0]["Male"]
            female = pop_row.iloc[0]["Female"]
        else:
            male = None
            female = None
            st.warning(
                "Population data was not found for this district."
            )

        df_district = pd.DataFrame({
            "district": [selected_district],
            "value": [1],
            "Male Population": [male],
            "Female Population": [female]
        })

        fig_district = px.choropleth_map(
            df_district,
            geojson=district_geojson,
            locations="district",
            featureidkey="properties.district",
            color="value",
            hover_data={
                "Male Population": True,
                "Female Population": True,
                "value": False
            },
            color_continuous_scale=["#F39C12", "#F39C12"],
            range_color=(0, 2),
            map_style="carto-positron",
            center=center_district,
            zoom=7,
            opacity=0.8,
            height=400
        )

        fig_district.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )
        fig_district.update_coloraxes(showscale=False)
        st.plotly_chart(
            fig_district,
            use_container_width=True
        )
    else:
        st.warning("District not found in GeoJSON.")
