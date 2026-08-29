import streamlit as st
import pandas as pd
import folium

from streamlit_folium import st_folium

from utils.routing import get_routes

from utils.climate import (
    analyze_route_temperature,
    compare_routes,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="UrbanBreeze - Route Results",
    page_icon="🌿",
    layout="wide",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f6fbfc;
    }

    .block-container {
        padding-top: 2rem;
        padding-left: 5%;
        padding-right: 5%;
        padding-bottom: 4rem;
    }

    .route-hero {
        background: white;
        border: 1px solid #e3edef;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
    }

    .ai-box {
        background-color: #e9f7f6;
        border: 2px solid #159c9c;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 20px;
    }

    .stButton > button {
        border-radius: 12px;
        min-height: 48px;
        font-weight: 650;
    }

    iframe {
        border-radius: 18px !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# GET USER DATA FROM PLAN ROUTE
# ============================================================

start_location = st.session_state.get(
    "start_location",
    "Unknown"
)

destination = st.session_state.get(
    "destination",
    "Unknown"
)

travel_mode = st.session_state.get(
    "travel_mode",
    "🚶 Walk"
)

prefer_cooler = st.session_state.get(
    "prefer_cooler",
    True
)

start_coords = st.session_state.get(
    "start_coords"
)

destination_coords = st.session_state.get(
    "destination_coords"
)


# ============================================================
# CHECK COORDINATES
# ============================================================

if start_coords is None:

    st.error(
        "Starting point coordinates are missing."
    )

    st.info(
        "Please return to Plan Route and select "
        "a starting location."
    )

    if st.button("← Back to Plan Route"):

        st.switch_page(
            "pages/1_Plan_Route.py"
        )

    st.stop()


if destination_coords is None:

    st.error(
        "Destination coordinates are missing."
    )

    st.info(
        "Please return to Plan Route and select "
        "a destination."
    )

    if st.button("← Back to Plan Route"):

        st.switch_page(
            "pages/1_Plan_Route.py"
        )

    st.stop()


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🌿 UrbanBreeze")

st.subheader("Climate-aware route results")

st.write(
    f"**{start_location}** → **{destination}**"
)

st.caption(
    f"Travel mode: {travel_mode}"
)


# ============================================================
# CREATE A UNIQUE CACHE KEY
# ============================================================
#
# IMPORTANT:
#
# Streamlit reruns the whole page whenever a button
# is clicked.
#
# We DO NOT want every button click to call FortyGuard
# again.
#
# Therefore route/climate results are stored in
# session_state.
# ============================================================

cache_key = (
    f"{start_coords['lat']:.6f}_"
    f"{start_coords['lon']:.6f}_"
    f"{destination_coords['lat']:.6f}_"
    f"{destination_coords['lon']:.6f}_"
    f"{travel_mode}"
)


# ============================================================
# GENERATE REAL ROUTES + CLIMATE DATA
# ============================================================

if (
    "route_results_cache" not in st.session_state
    or
    st.session_state.route_results_cache.get(
        "key"
    ) != cache_key
):

    # --------------------------------------------------------
    # REAL OSRM ROUTES
    # --------------------------------------------------------

    with st.spinner(
        "🗺️ Finding real route options..."
    ):

        routes = get_routes(
            start_coords,
            destination_coords,
            travel_mode
        )


    if not routes:

        st.error(
            "Could not find a route between "
            "these locations."
        )

        if st.button(
            "← Try another route"
        ):

            st.switch_page(
                "pages/1_Plan_Route.py"
            )

        st.stop()


    # --------------------------------------------------------
    # REAL FORTYGUARD CLIMATE ANALYSIS
    # --------------------------------------------------------

    progress = st.progress(
        0,
        text="🌡️ Analyzing route temperatures..."
    )

    total_routes = len(routes)


    for index, route in enumerate(routes):

        climate_result = analyze_route_temperature(
            route,
            number_of_points=5
        )

        route["climate"] = climate_result

        progress.progress(
            (index + 1) / total_routes,
            text=(
                f"🌡️ Analyzed route "
                f"{index + 1}/{total_routes}"
            )
        )


    progress.empty()


    # --------------------------------------------------------
    # REAL ROUTE COMPARISON
    # --------------------------------------------------------

    comparison = compare_routes(
        routes,
        prefer_cooler=prefer_cooler
    )


    # --------------------------------------------------------
    # SAVE RESULTS
    # --------------------------------------------------------

    st.session_state.route_results_cache = {

        "key": cache_key,

        "routes": routes,

        "comparison": comparison
    }


# ============================================================
# LOAD CACHED RESULTS
# ============================================================

cached = st.session_state.route_results_cache

routes = cached["routes"]

comparison = cached["comparison"]


# ============================================================
# GET ROUTE TYPES
# ============================================================

fastest_route = comparison.get(
    "fastest"
)

coolest_route = comparison.get(
    "coolest"
)

ai_pick = comparison.get(
    "ai_pick"
)


# ============================================================
# SAFETY
# ============================================================

if fastest_route is None:

    st.error(
        "Unable to determine the fastest route."
    )

    st.stop()


if ai_pick is None:

    ai_pick = fastest_route


# ============================================================
# INITIAL ROUTE
# ============================================================
#
# AI Recommended is selected initially.
# ============================================================

if "selected_route_type" not in st.session_state:

    st.session_state.selected_route_type = "ai"


# ============================================================
# ROUTE SELECTOR
# ============================================================

st.markdown("---")

st.subheader(
    "Choose your route"
)

col1, col2, col3 = st.columns(3)


with col1:

    if st.button(
        "🤖 AI Recommended",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.selected_route_type
            == "ai"
            else "secondary"
        )
    ):

        st.session_state.selected_route_type = "ai"

        st.rerun()


with col2:

    if st.button(
        "⚡ Fastest",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.selected_route_type
            == "fastest"
            else "secondary"
        )
    ):

        st.session_state.selected_route_type = "fastest"

        st.rerun()


with col3:

    if st.button(
        "🥶 Coolest",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.selected_route_type
            == "coolest"
            else "secondary"
        )
    ):

        st.session_state.selected_route_type = "coolest"

        st.rerun()


# ============================================================
# SELECT ROUTE
# ============================================================

selection = st.session_state.selected_route_type


if selection == "fastest":

    selected_route = fastest_route

    route_title = "⚡ Fastest Route"

    route_description = (
        "The route with the shortest travel time."
    )


elif selection == "coolest":

    selected_route = coolest_route

    route_title = "🥶 Coolest Route"

    route_description = (
        "The route with the highest climate comfort score."
    )


else:

    selected_route = ai_pick

    route_title = "🤖 AI Recommended Route"

    route_description = (
        "The best balance between travel time "
        "and climate comfort."
    )


# ============================================================
# SELECTED ROUTE DATA
# ============================================================

climate = selected_route.get(
    "climate",
    {}
)

temperature = climate.get(
    "average_temperature"
)

cool_score = climate.get(
    "cool_score"
)

heat_exposure = climate.get(
    "heat_exposure",
    "Unknown"
)

ai_score = selected_route.get(
    "ai_score"
)


# ============================================================
# SELECTED ROUTE HERO
# ============================================================

st.markdown(
    f"""
    <div class="ai-box">

    <h2>{route_title}</h2>

    <p>{route_description}</p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# METRICS
# ============================================================

m1, m2, m3, m4 = st.columns(4)


with m1:

    st.metric(
        "⏱️ Travel Time",
        f"{selected_route['duration_min']:.0f} min"
    )


with m2:

    st.metric(
        "📏 Distance",
        f"{selected_route['distance_km']:.1f} km"
    )


with m3:

    if temperature is not None:

        st.metric(
            "🌡️ Avg Temperature",
            f"{temperature:.1f} °C"
        )

    else:

        st.metric(
            "🌡️ Avg Temperature",
            "N/A"
        )


with m4:

    if cool_score is not None:

        st.metric(
            "🥶 Cool Score",
            f"{cool_score}/100"
        )

    else:

        st.metric(
            "🥶 Cool Score",
            "N/A"
        )


# ============================================================
# AI SCORE
# ============================================================

if selection == "ai" and ai_score is not None:

    st.info(
        f"🤖 **AI Score: {ai_score}/100**  "
        f"— climate comfort + travel time"
    )


# ============================================================
# MAP
# ============================================================

st.subheader(
    "🗺️ Selected Route"
)


geometry = selected_route.get(
    "geometry"
)


if geometry:

    coordinates = geometry["coordinates"]


    route_points = [
        [
            point[1],
            point[0]
        ]
        for point in coordinates
    ]


    center_lat = (
        start_coords["lat"]
        +
        destination_coords["lat"]
    ) / 2


    center_lon = (
        start_coords["lon"]
        +
        destination_coords["lon"]
    ) / 2


    route_map = folium.Map(
        location=[
            center_lat,
            center_lon
        ],
        zoom_start=13,
        control_scale=True
    )


    # --------------------------------------------------------
    # START
    # --------------------------------------------------------

    folium.Marker(
        [
            start_coords["lat"],
            start_coords["lon"]
        ],
        tooltip="Starting point",
        popup=start_location
    ).add_to(route_map)


    # --------------------------------------------------------
    # DESTINATION
    # --------------------------------------------------------

    folium.Marker(
        [
            destination_coords["lat"],
            destination_coords["lon"]
        ],
        tooltip="Destination",
        popup=destination
    ).add_to(route_map)


    # --------------------------------------------------------
    # SELECTED ROUTE
    # --------------------------------------------------------

    folium.PolyLine(
        locations=route_points,
        weight=8,
        opacity=0.9,
        tooltip=route_title
    ).add_to(route_map)


    st_folium(
        route_map,
        width=None,
        height=550
    )


else:

    st.warning(
        "Route geometry is unavailable."
    )


# ============================================================
# CLIMATE INFORMATION
# ============================================================

st.subheader(
    "🌡️ Climate information"
)


c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "Minimum",
        (
            f"{climate['minimum_temperature']:.1f} °C"
            if climate.get("minimum_temperature")
            is not None
            else "N/A"
        )
    )


with c2:

    st.metric(
        "Maximum",
        (
            f"{climate['maximum_temperature']:.1f} °C"
            if climate.get("maximum_temperature")
            is not None
            else "N/A"
        )
    )


with c3:

    st.metric(
        "Heat Exposure",
        heat_exposure
    )


# ============================================================
# ROUTE COMPARISON TABLE
# ============================================================

st.subheader(
    "📊 Compare Routes"
)


table_rows = []


for route in routes:

    route_climate = route.get(
        "climate",
        {}
    )


    route_number = route["route_number"]


    # --------------------------------------------------------
    # Determine label
    # --------------------------------------------------------

    labels = []


    if (
        fastest_route
        and
        route_number
        ==
        fastest_route["route_number"]
    ):

        labels.append(
            "⚡ Fastest"
        )


    if (
        coolest_route
        and
        route_number
        ==
        coolest_route["route_number"]
    ):

        labels.append(
            "🥶 Coolest"
        )


    if (
        ai_pick
        and
        route_number
        ==
        ai_pick["route_number"]
    ):

        labels.append(
            "🤖 AI Recommended"
        )


    label = " / ".join(labels)


    table_rows.append({

        "Route":
            f"Route {route_number}",

        "Type":
            label or "Alternative",

        "Time":
            f"{route['duration_min']:.0f} min",

        "Distance":
            f"{route['distance_km']:.1f} km",

        "Avg Temp":
            (
                f"{route_climate['average_temperature']:.1f} °C"
                if route_climate.get(
                    "average_temperature"
                ) is not None
                else "N/A"
            ),

        "Cool Score":
            (
                f"{route_climate['cool_score']}/100"
                if route_climate.get(
                    "cool_score"
                ) is not None
                else "N/A"
            ),

        "AI Score":
            (
                f"{route.get('ai_score')}/100"
                if route.get("ai_score")
                is not None
                else "N/A"
            )
    })


comparison_df = pd.DataFrame(
    table_rows
)


st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "UrbanBreeze • Routes powered by OSRM • "
    "Climate analysis powered by FortyGuard"
)