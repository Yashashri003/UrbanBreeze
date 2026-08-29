import streamlit as st
import pandas as pd
import folium
import json
import os
import html
from datetime import datetime

from streamlit_folium import st_folium

from ai_chatbot import (
    ask_gemini,
    build_route_context,
)

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
       URBANBREEZE — DARK MODERN UI
       Matches the dark teal + cyan visual language.
       No red, no glow, no decorative shadows.
       ======================================================== */

    :root {
        --ub-bg: #061f26;
        --ub-bg-deep: #04191f;
        --ub-surface: #0b2f37;
        --ub-surface-2: #0e3740;
        --ub-border: #24545d;
        --ub-border-soft: #1a444d;
        --ub-text: #f4fafb;
        --ub-muted: #8eabb1;
        --ub-cyan: #20bec3;
        --ub-cyan-light: #54d4d7;
        --ub-cyan-dark: #15979c;
        --ub-green: #203c32;
        --ub-green-border: #345b4b;
    }

    /* GLOBAL */
    .stApp {
        background: var(--ub-bg-deep) !important;
        color: var(--ub-text) !important;
    }

    .main .block-container {
        max-width: 1320px;
        padding-top: 0.8rem;
        padding-bottom: 4rem;
        padding-left: 3%;
        padding-right: 3%;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    /* TEXT */
    h1, h2, h3, h4, h5, h6 {
        color: var(--ub-text) !important;
        font-weight: 750 !important;
        letter-spacing: -0.55px;
    }

    p,
    label,
    .stCaption,
    [data-testid="stCaptionContainer"] {
        color: var(--ub-muted) !important;
    }

    /* NAVBAR */
    .navbar-title {
        color: var(--ub-text);
    }

    /* Profile button — compact white icon button */
    div[data-testid="stButton"] button[key="navbar_profile"],
    div.st-key-navbar_profile button {
        width: 42px !important;
        min-width: 42px !important;
        max-width: 42px !important;
        height: 42px !important;
        min-height: 42px !important;
        max-height: 42px !important;
        padding: 0 !important;
        margin-left: auto !important;
        border-radius: 50% !important;
        background: #ffffff !important;
        border: 1px solid #dce7e8 !important;
        color: #56328a !important;
        font-size: 18px !important;
        line-height: 1 !important;
        box-shadow: none !important;
    }

    div[data-testid="stButton"] button[key="navbar_profile"]:hover,
    div.st-key-navbar_profile button:hover {
        background: #ffffff !important;
        border-color: #cfdfe1 !important;
        color: #56328a !important;
        box-shadow: none !important;
        transform: none !important;
    }

    hr {
        border-color: var(--ub-border) !important;
    }

    /* BUTTONS — SIMPLE, FLAT, PROFESSIONAL */
    .stButton > button {
        min-height: 43px !important;
        border-radius: 10px !important;
        border: 1px solid var(--ub-border) !important;
        background: var(--ub-surface) !important;
        color: var(--ub-text) !important;
        font-weight: 650 !important;
        box-shadow: none !important;
        transition: background 0.15s ease, border-color 0.15s ease;
    }

    .stButton > button:hover {
        background: var(--ub-surface-2) !important;
        border-color: var(--ub-cyan) !important;
        color: var(--ub-cyan-light) !important;
        transform: none !important;
        box-shadow: none !important;
    }

    .stButton > button[kind="primary"] {
        background: var(--ub-cyan-dark) !important;
        border: 1px solid var(--ub-cyan) !important;
        color: #ffffff !important;
        box-shadow: none !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: #117f84 !important;
        border-color: var(--ub-cyan-light) !important;
        color: #ffffff !important;
        box-shadow: none !important;
    }

    /* ROUTE SELECTOR */
    .stButton > button[aria-pressed="true"] {
        background: var(--ub-cyan-dark) !important;
        color: #ffffff !important;
        border-color: var(--ub-cyan) !important;
        box-shadow: none !important;
    }

    /* METRIC CARDS */
    div[data-testid="stMetric"] {
        background: var(--ub-surface) !important;
        border: 1px solid var(--ub-border) !important;
        border-radius: 15px !important;
        padding: 19px 18px !important;
        min-height: 120px;
        box-shadow: none !important;
    }

    div[data-testid="stMetricLabel"] {
        color: var(--ub-muted) !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        color: var(--ub-text) !important;
        font-size: 27px !important;
        font-weight: 760 !important;
    }

    div[data-testid="stMetricDelta"] {
        color: var(--ub-cyan-light) !important;
    }

    /* INPUTS */
    .stTextInput input,
    .stSelectbox div[data-baseweb="select"] {
        background: var(--ub-surface) !important;
        color: var(--ub-text) !important;
        border: 1px solid var(--ub-border) !important;
        border-radius: 10px !important;
    }

    .stTextInput input::placeholder {
        color: #75949b !important;
    }

    .stTextInput input:focus {
        border-color: var(--ub-cyan) !important;
        box-shadow: none !important;
    }

    div[data-baseweb="select"] * {
        color: var(--ub-text) !important;
    }

    /* ALERTS */
    div[data-testid="stAlert"] {
        background: var(--ub-green) !important;
        border: 1px solid var(--ub-green-border) !important;
        border-radius: 13px !important;
        color: var(--ub-text) !important;
        box-shadow: none !important;
    }

    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] span {
        color: var(--ub-text) !important;
    }

    /* PROGRESS */
    div[data-testid="stProgressBar"] > div {
        background: #12343b !important;
        border-radius: 99px !important;
    }

    div[data-testid="stProgressBar"] > div > div {
        background: var(--ub-cyan) !important;
        border-radius: 99px !important;
    }

    /* ========================================================
       WHITE ROUTE COMPARISON TABLE
       Clean website-style table, no badges/glow.
       ======================================================== */

    .ub-table-wrap {
        width: 100%;
        overflow-x: auto;
        background: #ffffff;
        border: 1px solid #d7e3e5;
        border-radius: 13px;
        box-shadow: none;
        -webkit-overflow-scrolling: touch;
    }

    .ub-route-table {
        width: 100%;
        min-width: 760px;
        border-collapse: separate;
        border-spacing: 0;
        background: #ffffff;
        color: #183f47;
        font-size: 13px;
    }

    .ub-route-table thead th {
        background: #f4f8f8;
        color: #58767c;
        padding: 13px 15px;
        text-align: left;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .35px;
        border-bottom: 1px solid #dbe6e8;
        white-space: nowrap;
    }

    .ub-route-table tbody td {
        background: #ffffff;
        color: #234851;
        padding: 14px 15px;
        border-bottom: 1px solid #e5edef;
        white-space: nowrap;
        vertical-align: middle;
    }

    .ub-route-table tbody tr:nth-child(even) td {
        background: #fbfcfc;
    }

    .ub-route-table tbody tr:last-child td {
        border-bottom: none;
    }

    .ub-route-table tbody tr:hover td {
        background: #f7fafa;
    }

    .ub-route-name {
        color: #173c44;
        font-weight: 700;
    }

    .ub-type-badge,
    .ub-score {
        display: inline;
        padding: 0;
        border: none;
        background: transparent;
        color: #32747b;
        font-weight: 650;
    }

    .ub-table-scroll-hint {
        display: none;
        color: #77939a;
        font-size: 10px;
        margin-top: 7px;
    }

    /* MAP */
    iframe {
        border-radius: 15px !important;
        border: 1px solid var(--ub-border) !important;
    }

    /* CHATBOT — RIGHT SIDE */
    div.st-key-ub_chat_toggle {
        position: fixed !important;
        right: 22px !important;
        left: auto !important;
        bottom: 22px !important;
        width: 60px !important;
        z-index: 99999 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    div.st-key-ub_chat_toggle button {
        width: 58px !important;
        height: 58px !important;
        min-width: 58px !important;
        min-height: 58px !important;
        max-width: 58px !important;
        max-height: 58px !important;
        padding: 0 !important;
        border-radius: 50% !important;
        background: var(--ub-cyan-dark) !important;
        color: #ffffff !important;
        border: 2px solid #d8f7f8 !important;
        box-shadow: none !important;
        font-size: 20px !important;
    }

    div.st-key-ub_chat_toggle button:hover {
        background: #117f84 !important;
        border-color: #ffffff !important;
        transform: none !important;
        box-shadow: none !important;
    }

    div.st-key-ub_chat_panel {
        position: fixed !important;
        right: 22px !important;
        bottom: 94px !important;
        width: 365px !important;
        max-width: calc(100vw - 30px) !important;
        max-height: calc(100vh - 120px) !important;
        z-index: 99998 !important;
        padding: 0 !important;
        overflow: hidden !important;
        background: var(--ub-bg) !important;
        border: 1px solid var(--ub-border) !important;
        border-radius: 16px !important;
        box-shadow: none !important;
    }

    div.st-key-ub_chat_header {
        background: #0d555c !important;
        padding: 13px !important;
        margin: 0 !important;
        border-radius: 15px 15px 0 0 !important;
    }

    div.st-key-ub_chat_header div[data-testid="stButton"] button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #ffffff !important;
    }

    .ub-ai-avatar {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: #dffafb;
        color: #087c83;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: 850;
        margin-right: 9px;
    }

    .ub-ai-name {
        color: #ffffff;
        font-size: 15px;
        font-weight: 750;
    }

    .ub-ai-status {
        color: rgba(255,255,255,.8);
        font-size: 11px;
        margin-top: 3px;
    }

    div.st-key-ub_chat_body {
        background: #061f26 !important;
        padding: 10px 12px !important;
        max-height: 420px !important;
        overflow-y: auto !important;
    }

    div.st-key-ub_chat_body div[data-testid="stChatMessageContent"] {
        background: var(--ub-surface) !important;
        color: var(--ub-text) !important;
        border: 1px solid var(--ub-border) !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }

    div.st-key-ub_chat_body div[data-testid="stChatMessage"] p {
        color: var(--ub-text) !important;
    }

    div.st-key-ub_chat_quick button {
        background: transparent !important;
        color: var(--ub-cyan-light) !important;
        border: 1px solid #2b747a !important;
        border-radius: 18px !important;
        box-shadow: none !important;
    }

    div.st-key-ub_chat_quick button:hover {
        background: #103d45 !important;
        color: #ffffff !important;
        border-color: var(--ub-cyan) !important;
        box-shadow: none !important;
    }

    div.st-key-ub_chat_composer {
        background: var(--ub-bg) !important;
        border-top: 1px solid var(--ub-border) !important;
        padding: 8px 10px 10px !important;
    }

    div.st-key-ub_chat_composer input {
        background: var(--ub-surface) !important;
        color: #ffffff !important;
        border: 1px solid var(--ub-border) !important;
        border-radius: 20px !important;
        box-shadow: none !important;
    }

    div.st-key-ub_chat_composer input:focus {
        border-color: var(--ub-cyan) !important;
        box-shadow: none !important;
    }

    div.st-key-ub_chat_composer div[data-testid="stButton"] button {
        width: 38px !important;
        height: 38px !important;
        min-width: 38px !important;
        min-height: 38px !important;
        padding: 0 !important;
        border-radius: 50% !important;
        background: var(--ub-cyan-dark) !important;
        color: #ffffff !important;
        border-color: var(--ub-cyan) !important;
        box-shadow: none !important;
    }

    .ub-chat-footer {
        text-align: center;
        color: #64858c;
        font-size: 9px;
        padding-top: 4px;
    }

    /* MOBILE */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 14px;
            padding-right: 14px;
            padding-top: .5rem;
            overflow-x: hidden;
        }

        h1 {
            font-size: 29px !important;
        }

        h2 {
            font-size: 23px !important;
        }

        h3 {
            font-size: 19px !important;
        }

        div[data-testid="stMetric"] {
            min-height: 100px;
            padding: 15px !important;
        }

        div[data-testid="stMetricValue"] {
            font-size: 21px !important;
        }

        .ub-route-table {
            min-width: 720px;
        }

        .ub-route-table thead th,
        .ub-route-table tbody td {
            padding: 12px 11px;
        }

        .ub-table-scroll-hint {
            display: block;
        }

        div.st-key-ub_chat_toggle {
            right: 14px !important;
            bottom: 14px !important;
        }

        div.st-key-ub_chat_panel {
            left: 10px !important;
            right: 10px !important;
            bottom: 80px !important;
            width: auto !important;
            max-width: none !important;
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
# AI CHAT STATE
# ============================================================

if "ub_chat_open" not in st.session_state:
    st.session_state.ub_chat_open = False

if "ub_chat_messages" not in st.session_state:
    st.session_state.ub_chat_messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I'm UrbanBreeze AI. "
                "Ask me about this route, its temperature, "
                "Cool Score, travel time, or why a route was recommended."
            ),
        }
    ]

if "ub_chat_interaction_id" not in st.session_state:
    st.session_state.ub_chat_interaction_id = None


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
        key="navbar_plan_route",
        use_container_width=True
    ):

        st.switch_page(
            "pages/1_Plan_Route.py"
        )


with nav_saved:

    if st.button(
        "Saved Places",
        key="navbar_saved_places",
        use_container_width=True
    ):

        st.switch_page(
            "pages/3_Saved_Places.py"
        )


with nav_history:

    if st.button(
        "History",
        key="navbar_history",
        use_container_width=True
    ):

        st.switch_page(
            "pages/4_Route_History.py"
        )


with nav_profile:

    if st.button(
        "♟",
        key="navbar_profile",
        use_container_width=True
    ):

        st.switch_page(
            "pages/5_Profile.py"
        )


st.divider()


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
        key="missing_start_back",
        type="primary"
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
        key="missing_destination_back",
        type="primary"
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
            key="try_another_route"
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
        key="select_ai_route",
        use_container_width=True,
        type=(
            "primary"
            if
            st.session_state.selected_route_type
            == "ai"
            else
            "secondary"
        )
    ):

        st.session_state.selected_route_type = (
            "ai"
        )

        st.rerun()


with route_col2:

    if st.button(
        "Fastest",
        key="select_fastest_route",
        use_container_width=True,
        type=(
            "primary"
            if
            st.session_state.selected_route_type
            == "fastest"
            else
            "secondary"
        )
    ):

        st.session_state.selected_route_type = (
            "fastest"
        )

        st.rerun()


with route_col3:

    if st.button(
        "Coolest",
        key="select_coolest_route",
        use_container_width=True,
        type=(
            "primary"
            if
            st.session_state.selected_route_type
            == "coolest"
            else
            "secondary"
        )
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

        returned_objects=[]
    )


else:

    st.warning(
        "Route geometry is unavailable."
    )


# ============================================================
# START JOURNEY
# ============================================================

st.markdown("### Journey")

if "journey_started" not in st.session_state:
    st.session_state.journey_started = False

journey_col1, journey_col2 = st.columns([2, 1])

with journey_col1:
    if st.button(
        "Start Journey",
        key="start_journey",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.journey_started = True
        st.session_state.navigation_route = selected_route
        st.rerun()

with journey_col2:
    if st.session_state.get("journey_started"):
        if st.button(
            "End Journey",
            key="end_journey",
            use_container_width=True,
        ):
            st.session_state.journey_started = False
            st.session_state.pop(
                "navigation_route",
                None,
            )
            st.rerun()


if st.session_state.get("journey_started"):
    st.success(
        "Journey started. Follow the selected route on the map."
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

# Build a responsive custom table so the visual styling is consistent
# across Streamlit versions and matches the UrbanBreeze dark-teal UI.
table_html = """
<div class="ub-table-wrap">
<table class="ub-route-table">
<thead>
<tr>
    <th>Route</th>
    <th>Type</th>
    <th>Time</th>
    <th>Distance</th>
    <th>Avg Temp</th>
    <th>Cool Score</th>
    <th>AI Score</th>
</tr>
</thead>
<tbody>
"""

for row in table_rows:
    route_name = html.escape(str(row["Route"]))
    route_type = html.escape(str(row["Type"]))
    time_value = html.escape(str(row["Time"]))
    distance_value = html.escape(str(row["Distance"]))
    temp_value = html.escape(str(row["Avg Temp"]))
    cool_value = html.escape(str(row["Cool Score"]))
    ai_value = html.escape(str(row["AI Score"]))

    table_html += f"""
<tr>
    <td><span class="ub-route-name">{route_name}</span></td>
    <td><span class="ub-type-badge">{route_type}</span></td>
    <td>{time_value}</td>
    <td>{distance_value}</td>
    <td>{temp_value}</td>
    <td><span class="ub-score">{cool_value}</span></td>
    <td><span class="ub-score">{ai_value}</span></td>
</tr>
"""

table_html += """
</tbody>
</table>
</div>
<div class="ub-table-scroll-hint">Swipe horizontally to view the full table →</div>
"""

st.markdown(
    table_html,
    unsafe_allow_html=True,
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
# URBANBREEZE AI CHATBOT
# ============================================================

# Floating launcher
with st.container(key="ub_chat_toggle"):
    if st.button(
        "✦",
        key="ub_open_chat",
        help="Open UrbanBreeze AI",
    ):
        st.session_state.ub_chat_open = (
            not st.session_state.ub_chat_open
        )
        st.rerun()


if st.session_state.ub_chat_open:

    route_context = build_route_context(
        start_location=start_location,
        destination=destination,
        travel_mode=travel_mode,
        selected_route=selected_route,
        route_title=route_title,
        routes=routes,
    )

    with st.container(key="ub_chat_panel"):

        # -----------------------------
        # Header
        # -----------------------------
        with st.container(key="ub_chat_header"):

            header_left, header_menu, header_close = st.columns(
                [7, 1, 1],
                gap="small",
            )

            with header_left:
                st.markdown(
                    """
                    <div style="display:flex;align-items:center;">
                        <div class="ub-ai-avatar">UB</div>
                        <div>
                            <div class="ub-ai-name">UrbanBreeze AI</div>
                            <div class="ub-ai-status">
                                Climate & route assistant
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with header_menu:
                if st.button(
                    "⋮",
                    key="ub_chat_menu",
                    help="Clear conversation",
                ):
                    st.session_state.ub_chat_messages = [
                        {
                            "role": "assistant",
                            "content": (
                                "Hi! I'm your UrbanBreeze AI assistant. "
                                "I can help you understand your route, "
                                "temperature, travel time and Cool Score."
                            ),
                        }
                    ]
                    st.session_state.ub_chat_interaction_id = None
                    st.rerun()

            with header_close:
                if st.button(
                    "×",
                    key="ub_close_chat",
                    help="Close chatbot",
                ):
                    st.session_state.ub_chat_open = False
                    st.rerun()

        # -----------------------------
        # Conversation
        # -----------------------------
        with st.container(key="ub_chat_body"):

            for message in st.session_state.ub_chat_messages[-8:]:

                # Streamlit avatars must be an image, emoji, or a supported
                # avatar value. Text such as "UB" is NOT a valid avatar.
                # Emoji avatars keep the interface compact and reliable.
                avatar = (
                    "🤖"
                    if message["role"] == "assistant"
                    else "👤"
                )

                with st.chat_message(
                    message["role"],
                    avatar=avatar,
                ):
                    st.write(message["content"])

            # Quick replies appear near the beginning of the chat.
            if len(st.session_state.ub_chat_messages) <= 1:

                st.markdown(
                    '<div class="ub-quick-title">Quick questions</div>',
                    unsafe_allow_html=True,
                )

                with st.container(key="ub_chat_quick"):

                    quick_1, quick_2 = st.columns(2)
                    quick_3, quick_4 = st.columns(2)

                    quick_questions = [
                        "Which route is coolest?",
                        "Why was this route recommended?",
                        "What is the route temperature?",
                        "How long is this journey?",
                    ]

                    with quick_1:
                        q1 = st.button(
                            quick_questions[0],
                            key="ub_quick_0",
                            use_container_width=True,
                        )

                    with quick_2:
                        q2 = st.button(
                            quick_questions[1],
                            key="ub_quick_1",
                            use_container_width=True,
                        )

                    with quick_3:
                        q3 = st.button(
                            quick_questions[2],
                            key="ub_quick_2",
                            use_container_width=True,
                        )

                    with quick_4:
                        q4 = st.button(
                            quick_questions[3],
                            key="ub_quick_3",
                            use_container_width=True,
                        )

                selected_quick = None

                if q1:
                    selected_quick = quick_questions[0]
                elif q2:
                    selected_quick = quick_questions[1]
                elif q3:
                    selected_quick = quick_questions[2]
                elif q4:
                    selected_quick = quick_questions[3]

                if selected_quick:
                    st.session_state.ub_chat_input = selected_quick
                    st.rerun()

        # -----------------------------
        # Composer
        # -----------------------------
        with st.container(key="ub_chat_composer"):

            if "ub_chat_input" not in st.session_state:
                st.session_state.ub_chat_input = ""

            input_col, send_col = st.columns(
                [7, 1],
                gap="small",
            )

            with input_col:
                user_question = st.text_input(
                    "Ask UrbanBreeze AI",
                    key="ub_chat_input",
                    label_visibility="collapsed",
                    placeholder="Ask about your route...",
                )

            with send_col:
                send_chat = st.button(
                    "➤",
                    key="ub_send_chat",
                    help="Send",
                )

            st.markdown(
                '<div class="ub-chat-footer">UrbanBreeze AI</div>',
                unsafe_allow_html=True,
            )

        # -----------------------------
        # Send message
        # -----------------------------
        if send_chat and user_question.strip():

            question = user_question.strip()

            st.session_state.ub_chat_messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            try:

                with st.spinner(
                    "UrbanBreeze AI is thinking..."
                ):

                    answer, interaction_id = ask_gemini(
                        message=question,
                        route_context=route_context,
                        previous_interaction_id=(
                            st.session_state.ub_chat_interaction_id
                        ),
                    )

                st.session_state.ub_chat_messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

                st.session_state.ub_chat_interaction_id = (
                    interaction_id
                )

            except Exception:

                st.session_state.ub_chat_messages.append(
                    {
                        "role": "assistant",
                        "content": (
                            "I couldn't connect to the AI service right now. "
                            "Please check your Gemini API key and connection."
                        ),
                    }
                )

            st.session_state.ub_chat_input = ""
            st.rerun()


# ============================================================
# NAVIGATION
# ============================================================

st.markdown("### Continue")


back_col, history_col, plan_col = st.columns(3)


with back_col:

    if st.button(
        "← Plan another route",
        key="bottom_plan_another_route",
        use_container_width=True
    ):

        st.switch_page(
            "pages/1_Plan_Route.py"
        )


with history_col:

    if st.button(
        "View route history",
        key="bottom_view_history",
        use_container_width=True
    ):

        st.switch_page(
            "pages/4_Route_History.py"
        )


with plan_col:

    if st.button(
        "Saved Places",
        key="bottom_saved_places",
        use_container_width=True
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
