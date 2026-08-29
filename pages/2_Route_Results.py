import streamlit as st
import pandas as pd
import folium
import json
import os
from datetime import datetime

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
    page_title="UrbanBreeze | Route Results",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# IMPORTANT:
# This is CSS only.
# No visible HTML is written into the dashboard.
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background: #062b32;
        color: #f5fbfc;
    }

    .main .block-container {
        max-width: 1280px;
        padding-top: 0.8rem;
        padding-bottom: 4rem;
        padding-left: 5%;
        padding-right: 5%;
    }

    /* Hide Streamlit default elements */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* ========================================================
       TEXT
       ======================================================== */

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        color: #f5fbfc !important;
        letter-spacing: -0.5px;
    }

    p,
    label,
    .stCaption {
        color: #b5c9cc !important;
    }

    .stMarkdown,
    .stText {
        color: #f5fbfc;
    }

    /* ========================================================
       NAVBAR
       ======================================================== */

    .navbar-title {
        font-size: 23px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
        padding-top: 9px;
    }

    .navbar-brand {
        color: #18aaa8;
    }

    .navbar-divider {
        border-bottom: 1px solid rgba(255,255,255,0.10);
        margin-top: 8px;
        margin-bottom: 28px;
    }

    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 10px;
        min-height: 43px;
        font-weight: 650;
        border: 1px solid rgba(255,255,255,0.16);
        background: #0a343b;
        color: #eefafa;
        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        border-color: #18aaa8;
        color: #ffffff;
        background: #0d4148;
    }

    /* Primary buttons */

    .stButton > button[kind="primary"] {
        background: #16a5a5;
        border-color: #16a5a5;
        color: white;
    }

    .stButton > button[kind="primary"]:hover {
        background: #13b5b2;
        border-color: #13b5b2;
    }

    /* ========================================================
       METRIC CARDS
       ======================================================== */

    div[data-testid="stMetric"] {
        background: #0a353c;
        border: 1px solid rgba(255,255,255,0.22);
        border-radius: 14px;
        padding: 20px 18px;
        min-height: 125px;
    }

    div[data-testid="stMetricLabel"] {
        color: #b9cbce !important;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 27px !important;
        font-weight: 750 !important;
    }

    /* ========================================================
       INPUTS
       ======================================================== */

    .stTextInput input,
    .stSelectbox div[data-baseweb="select"],
    .stRadio div[data-baseweb="radio"] {
        background: #092f36 !important;
        color: #ffffff !important;
    }

    .stTextInput input {
        border: 1px solid rgba(255,255,255,0.20) !important;
        border-radius: 10px !important;
    }

    /* ========================================================
       DATAFRAME
       ======================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
    }

    /* ========================================================
       MAP
       ======================================================== */

    iframe {
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
    }

    /* ========================================================
       ALERTS
       ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .main .block-container {
            padding-left: 16px;
            padding-right: 16px;
            padding-top: 0.5rem;
        }

        .navbar-title {
            font-size: 18px;
        }

        h1 {
            font-size: 30px !important;
        }

        h2 {
            font-size: 23px !important;
        }

        h3 {
            font-size: 20px !important;
        }

        div[data-testid="stMetric"] {
            padding: 15px;
            min-height: 105px;
        }

        div[data-testid="stMetricValue"] {
            font-size: 21px !important;
        }

        .stButton > button {
            min-height: 42px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# TIME FORMATTER
# ============================================================

def format_duration(minutes):

    try:
        minutes = int(
            round(
                float(minutes)
            )
        )

    except (
        TypeError,
        ValueError
    ):
        return "N/A"

    if minutes < 60:
        return f"{minutes} min"

    hours = minutes // 60
    remaining_minutes = minutes % 60

    if hours == 1:
        hour_text = "1 hr"
    else:
        hour_text = f"{hours} hrs"

    if remaining_minutes == 0:
        return hour_text

    return f"{hour_text} {remaining_minutes} min"


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "data"
)

HISTORY_FILE = os.path.join(
    DATA_DIR,
    "route_history.json"
)


# ============================================================
# ROUTE HISTORY
# ============================================================

def load_route_history():

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    if not os.path.exists(
        HISTORY_FILE
    ):
        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

    except (
        json.JSONDecodeError,
        OSError
    ):
        return []

    return []


def save_route_history(history):

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=2,
            ensure_ascii=False
        )


def save_selected_route_to_history(
    route,
    route_type,
    route_key
):

    history = load_route_history()

    climate = route.get(
        "climate",
        {}
    )

    history_item = {

        "timestamp":
            datetime.now().isoformat(
                timespec="seconds"
            ),

        "start":
            start_location,

        "destination":
            destination,

        "travel_mode":
            travel_mode,

        "route_type":
            route_type,

        "route_key":
            route_key,

        "duration_minutes":
            float(
                route.get(
                    "duration_min",
                    0
                )
            ),

        "duration":
            format_duration(
                route.get(
                    "duration_min",
                    0
                )
            ),

        "distance_km":
            float(
                route.get(
                    "distance_km",
                    0
                )
            ),

        "average_temperature":
            climate.get(
                "average_temperature"
            ),

        "minimum_temperature":
            climate.get(
                "minimum_temperature"
            ),

        "maximum_temperature":
            climate.get(
                "maximum_temperature"
            ),

        "heat_exposure":
            climate.get(
                "heat_exposure",
                "Unknown"
            ),

        "cool_score":
            climate.get(
                "cool_score"
            ),

        "ai_score":
            route.get(
                "ai_score"
            )
    }

    existing_index = None

    for index, item in enumerate(history):

        if (
            item.get("route_key")
            == route_key
        ):

            existing_index = index
            break

    if existing_index is not None:

        history[
            existing_index
        ] = history_item

    else:

        history.insert(
            0,
            history_item
        )

    save_route_history(
        history
    )


# ============================================================
# GET USER DATA
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
    "Walk"
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
# NAVBAR
# ============================================================

nav_brand, nav_plan, nav_saved, nav_history, nav_profile = (
    st.columns(
        [2.2, 1, 1, 1, 1]
    )
)


with nav_brand:

    st.markdown(
        "### 🌬️ UrbanBreeze"
    )


with nav_plan:

    if st.button(
        "Plan Route",
        use_container_width=True,
        key="nav_plan_route_btn"
    ):

        st.switch_page(
            "pages/1_Plan_Route.py"
        )


with nav_saved:

    if st.button(
        "Saved Places",
        use_container_width=True,
        key="nav_saved_places_btn"
    ):

        st.switch_page(
            "pages/3_Saved_Places.py"
        )


with nav_history:

    if st.button(
        "History",
        use_container_width=True,
        key="nav_history_btn"
    ):

        st.switch_page(
            "pages/4_Route_History.py"
        )


with nav_profile:

    if st.button(
        "◯ Profile",
        use_container_width=True,
        key="nav_profile_btn"
    ):

        st.switch_page(
            "pages/5_Profile.py"
        )


st.markdown(
    '<div class="navbar-divider"></div>',
    unsafe_allow_html=True
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

    if st.button(
        "← Back to Plan Route",
        type="primary",
        key="missing_start_back_btn"
    ):

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

    if st.button(
        "← Back to Plan Route",
        type="primary",
        key="missing_dest_back_btn"
    ):

        st.switch_page(
            "pages/1_Plan_Route.py"
        )

    st.stop()


# ============================================================
# PAGE HEADER
# ============================================================

st.title(
    "Route Results"
)

st.write(
    f"{start_location}  →  {destination}"
)

st.caption(
    f"{travel_mode}  •  Climate-aware route planning"
)


# ============================================================
# ROUTE CACHE KEY
# ============================================================

cache_key = (

    f"{start_coords['lat']:.6f}_"

    f"{start_coords['lon']:.6f}_"

    f"{destination_coords['lat']:.6f}_"

    f"{destination_coords['lon']:.6f}_"

    f"{travel_mode}"
)


# ============================================================
# GENERATE ROUTES
# ============================================================

if (
    "route_results_cache"
    not in st.session_state

    or

    st.session_state.route_results_cache.get(
        "key"
    ) != cache_key
):

    # --------------------------------------------------------
    # OSRM
    # --------------------------------------------------------

    with st.spinner(
        "Finding real route options..."
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
            "← Try another route",
            key="no_route_try_again_btn"
        ):

            st.switch_page(
                "pages/1_Plan_Route.py"
            )

        st.stop()

    # --------------------------------------------------------
    # FORTYGUARD
    # --------------------------------------------------------

    progress = st.progress(
        0,
        text="Analyzing route climate..."
    )

    total_routes = len(routes)

    for index, route in enumerate(routes):

        climate_result = (
            analyze_route_temperature(
                route,
                number_of_points=5
            )
        )

        route["climate"] = (
            climate_result
        )

        progress.progress(
            (index + 1) / total_routes,
            text=(
                f"Analyzing route "
                f"{index + 1}/{total_routes}"
            )
        )

    progress.empty()

    # --------------------------------------------------------
    # COMPARE
    # --------------------------------------------------------

    comparison = compare_routes(
        routes,
        prefer_cooler=prefer_cooler
    )

    st.session_state.route_results_cache = {

        "key":
            cache_key,

        "routes":
            routes,

        "comparison":
            comparison
    }


# ============================================================
# LOAD CACHE
# ============================================================

cached = (
    st.session_state.route_results_cache
)

routes = cached[
    "routes"
]

comparison = cached[
    "comparison"
]


# ============================================================
# ROUTE TYPES
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


if fastest_route is None:

    st.error(
        "Unable to determine the fastest route."
    )

    st.stop()


if ai_pick is None:

    ai_pick = fastest_route


# ============================================================
# DEFAULT SELECTION
# ============================================================

if (
    "selected_route_type"
    not in st.session_state
):

    st.session_state.selected_route_type = (
        "ai"
    )


# ============================================================
# ROUTE SELECTION
# ============================================================

st.markdown("## Choose your route")

route_col1, route_col2, route_col3 = (
    st.columns(3)
)


with route_col1:

    if st.button(
        "AI Recommended",
        use_container_width=True,
        type=(
            "primary"
            if
            st.session_state.selected_route_type
            == "ai"
            else
            "secondary"
        ),
        key="select_route_ai_btn"
    ):

        st.session_state.selected_route_type = (
            "ai"
        )

        st.rerun()


with route_col2:

    if st.button(
        "Fastest",
        use_container_width=True,
        type=(
            "primary"
            if
            st.session_state.selected_route_type
            == "fastest"
            else
            "secondary"
        ),
        key="select_route_fastest_btn"
    ):

        st.session_state.selected_route_type = (
            "fastest"
        )

        st.rerun()


with route_col3:

    if st.button(
        "Coolest",
        use_container_width=True,
        type=(
            "primary"
            if
            st.session_state.selected_route_type
            == "coolest"
            else
            "secondary"
        ),
        key="select_route_coolest_btn"
    ):

        st.session_state.selected_route_type = (
            "coolest"
        )

        st.rerun()


# ============================================================
# SELECT ROUTE
# ============================================================

selection = (
    st.session_state.selected_route_type
)


if selection == "fastest":

    selected_route = fastest_route

    route_title = (
        "Fastest Route"
    )

    route_description = (
        "The route with the shortest travel time."
    )

    history_route_type = "Fastest"


elif selection == "coolest":

    selected_route = coolest_route

    route_title = (
        "Coolest Route"
    )

    route_description = (
        "The route with the highest climate comfort."
    )

    history_route_type = "Coolest"


else:

    selected_route = ai_pick

    route_title = (
        "AI Recommended Route"
    )

    route_description = (
        "The best balance between travel time "
        "and climate comfort."
    )

    history_route_type = "AI Recommended"


# ============================================================
# SAVE TO HISTORY
# ============================================================

route_key = (

    f"{cache_key}_"

    f"{selection}_"

    f"{selected_route.get('route_number', 0)}"
)


save_selected_route_to_history(
    selected_route,
    history_route_type,
    route_key
)


# ============================================================
# CLIMATE DATA
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
# RECOMMENDED ROUTE
# ============================================================

st.markdown("## Recommended journey")

st.info(
    f"{route_title}\n\n"
    f"{route_description}"
)


# ============================================================
# MAIN METRICS
# ============================================================

st.markdown("### Journey overview")


m1, m2, m3, m4 = st.columns(4)


with m1:

    st.metric(
        "Travel Time",
        format_duration(
            selected_route[
                "duration_min"
            ]
        )
    )


with m2:

    st.metric(
        "Distance",
        f"{selected_route['distance_km']:.1f} km"
    )


with m3:

    if temperature is not None:

        st.metric(
            "Temperature",
            f"{temperature:.1f} °C"
        )

    else:

        st.metric(
            "Temperature",
            "N/A"
        )


with m4:

    if cool_score is not None:

        st.metric(
            "Cool Score",
            f"{cool_score}/100"
        )

    else:

        st.metric(
            "Cool Score",
            "N/A"
        )


# ============================================================
# AI SCORE
# ============================================================

if (
    selection == "ai"
    and
    ai_score is not None
):

    st.success(
        f"AI Score: {ai_score}/100"
    )


# ============================================================
# ROUTE MAP
# ============================================================

st.markdown("## Route map")

geometry = selected_route.get(
    "geometry"
)


if geometry:

    coordinates = geometry[
        "coordinates"
    ]

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

    # Start

    folium.Marker(

        [
            start_coords["lat"],
            start_coords["lon"]
        ],

        tooltip="Starting point",

        popup=start_location

    ).add_to(
        route_map
    )

    # Destination

    folium.Marker(

        [
            destination_coords["lat"],
            destination_coords["lon"]
        ],

        tooltip="Destination",

        popup=destination

    ).add_to(
        route_map
    )

    # Route

    folium.PolyLine(

        locations=route_points,

        weight=7,

        opacity=0.9,

        tooltip=route_title

    ).add_to(
        route_map
    )

    st_folium(

        route_map,

        width=None,

        height=520,

        returned_objects=[],
        key="route_results_map"
    )


else:

    st.warning(
        "Route geometry is unavailable."
    )


# ============================================================
# CLIMATE INSIGHTS
# ============================================================

st.markdown("## Climate insights")

c1, c2, c3 = st.columns(3)


with c1:

    minimum_temperature = (
        climate.get(
            "minimum_temperature"
        )
    )

    if minimum_temperature is not None:

        st.metric(
            "Minimum Temperature",
            f"{minimum_temperature:.1f} °C"
        )

    else:

        st.metric(
            "Minimum Temperature",
            "N/A"
        )


with c2:

    maximum_temperature = (
        climate.get(
            "maximum_temperature"
        )
    )

    if maximum_temperature is not None:

        st.metric(
            "Maximum Temperature",
            f"{maximum_temperature:.1f} °C"
        )

    else:

        st.metric(
            "Maximum Temperature",
            "N/A"
        )


with c3:

    st.metric(
        "Heat Exposure",
        heat_exposure
    )


# ============================================================
# ROUTE COMPARISON
# ============================================================

st.markdown("## Compare routes")

table_rows = []


for route in routes:

    route_climate = route.get(
        "climate",
        {}
    )

    route_number = route[
        "route_number"
    ]

    labels = []

    if (
        fastest_route

        and

        route_number
        ==
        fastest_route[
            "route_number"
        ]
    ):

        labels.append(
            "Fastest"
        )

    if (
        coolest_route

        and

        route_number
        ==
        coolest_route[
            "route_number"
        ]
    ):

        labels.append(
            "Coolest"
        )

    if (
        ai_pick

        and

        route_number
        ==
        ai_pick[
            "route_number"
        ]
    ):

        labels.append(
            "AI Recommended"
        )

    label = (
        " / ".join(
            labels
        )
    )

    if not label:

        label = (
            "Alternative"
        )

    average_temperature = (
        route_climate.get(
            "average_temperature"
        )
    )

    route_cool_score = (
        route_climate.get(
            "cool_score"
        )
    )

    route_ai_score = (
        route.get(
            "ai_score"
        )
    )

    table_rows.append({

        "Route":
            f"Route {route_number}",

        "Type":
            label,

        "Time":
            format_duration(
                route[
                    "duration_min"
                ]
            ),

        "Distance":
            f"{route['distance_km']:.1f} km",

        "Avg Temp":
            (
                f"{average_temperature:.1f} °C"
                if
                average_temperature
                is not None
                else
                "N/A"
            ),

        "Cool Score":
            (
                f"{route_cool_score}/100"
                if
                route_cool_score
                is not None
                else
                "N/A"
            ),

        "AI Score":
            (
                f"{route_ai_score}/100"
                if
                route_ai_score
                is not None
                else
                "N/A"
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
# ROUTE SUMMARY
# ============================================================

st.markdown("## Journey summary")

st.write(
    f"**{start_location}** → **{destination}**"
)

st.write(
    f"Travel time: **{format_duration(selected_route['duration_min'])}**"
)

st.write(
    f"Distance: **{selected_route['distance_km']:.1f} km**"
)

if temperature is not None:

    st.write(
        f"Average temperature: **{temperature:.1f} °C**"
    )

if cool_score is not None:

    st.write(
        f"Climate comfort score: **{cool_score}/100**"
    )


# ============================================================
# NAVIGATION
# ============================================================

st.markdown("### Continue")


back_col, history_col, plan_col = st.columns(3)


with back_col:

    if st.button(
        "← Plan another route",
        use_container_width=True,
        key="bottom_plan_another_route_btn"
    ):

        st.switch_page(
            "pages/1_Plan_Route.py"
        )


with history_col:

    if st.button(
        "View route history",
        use_container_width=True,
        key="bottom_view_history_btn"
    ):

        st.switch_page(
            "pages/4_Route_History.py"
        )


with plan_col:

    if st.button(
        "Saved Places",
        use_container_width=True,
        key="bottom_saved_places_btn"
    ):

        st.switch_page(
            "pages/3_Saved_Places.py"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "UrbanBreeze • Routes powered by OSRM • "
    "Climate analysis powered by FortyGuard"
)
