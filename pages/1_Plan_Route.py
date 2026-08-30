import os
import sys

# ============================================================
# PROJECT PATH
# ============================================================

current_dir = os.path.dirname(os.path.abspath(__file__))

if current_dir not in sys.path:
    sys.path.append(current_dir)


# ============================================================
# IMPORTS
# ============================================================

import streamlit as st
import folium

from streamlit_folium import st_folium

from utils.routing import search_california_locations
from utils.ui import apply_urbanbreeze_theme, logo


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Plan Route | UrbanBreeze",
    layout="wide"
)

apply_urbanbreeze_theme()


# ============================================================
# ADDITIONAL PAGE CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       URBANBREEZE PLAN ROUTE - UI POLISH
       ======================================================== */

    .block-container {
        max-width: 1240px !important;
        padding-top: 5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-bottom: 3rem !important;
    }

    div[data-testid="stHorizontalBlock"] {
        max-width: 100% !important;
    }

    div[data-testid="stHorizontalBlock"] > div {
        min-width: 0 !important;
    }

    .stMarkdown,
    .stCaption,
    .stTextInput,
    div[data-testid="stTabs"] {
        max-width: 100% !important;
    }

    h1, h2, h3, h4, p, label, span {
        overflow-wrap: anywhere;
    }


    /* ========================================================
       ALL BUTTONS
       ======================================================== */

    div[data-testid="stButton"] button {
        border-radius: 10px !important;
        min-height: 42px !important;
        padding: 0 14px !important;

        background: #0d343b !important;
        color: #eefafa !important;

        border: 1px solid #2b555d !important;

        font-weight: 650 !important;
        line-height: 1.2 !important;

        box-shadow: none !important;

        transition:
            background 0.15s ease,
            border-color 0.15s ease,
            color 0.15s ease,
            transform 0.15s ease !important;
    }


    div[data-testid="stButton"] button:hover {
        background: #14464e !important;
        color: #ffffff !important;
        border-color: #22b7b2 !important;
    }


    /* ========================================================
       PRIMARY BUTTON
       ======================================================== */

    div[data-testid="stButton"] button[kind="primary"] {
        background: #159f9d !important;
        color: #ffffff !important;
        border-color: #159f9d !important;
        font-weight: 750 !important;
    }


    div[data-testid="stButton"] button[kind="primary"]:hover {
        background: #20b9b4 !important;
        border-color: #20b9b4 !important;
        transform: translateY(-1px) !important;
    }


    /* ========================================================
   PROFILE BUTTON
   ======================================================== */

div.st-key-plan_profile_icon button {
    width: 44px !important;
    height: 44px !important;

    min-width: 44px !important;
    max-width: 44px !important;
    min-height: 44px !important;
    max-height: 44px !important;

    padding: 0 !important;

    /* Keep the profile perfectly circular */
    border-radius: 50% !important;

    /* Same dark teal style as the navigation boxes */
    background: #0d343b !important;

    /* Light boundary around the circle */
    border: 1px solid #b9ced1 !important;

    /* Person icon */
    color: #ffffff !important;

    font-size: 18px !important;
    font-weight: 700 !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    box-shadow: none !important;
}

/* Keep the person white when hovering */
div.st-key-plan_profile_icon button:hover {
    background: #0d343b !important;
    color: #ffffff !important;

    border-color: #dcebed !important;

    transform: none !important;
}


    /* ========================================================
       SWITCH LOCATION BUTTON
       ======================================================== */

    div.st-key-switch_location_container {
        width: 100% !important;
        min-height: 112px !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;

        padding-top: 30px !important;
    }


    /* Button wrapper */

    div.st-key-switch_location_container div[data-testid="stButton"] {
        width: 56px !important;
        min-width: 56px !important;

        margin: 0 auto !important;
    }


    /* ========================================================
       ARROW BOX
       ======================================================== */

    div.st-key-switch_location_container button {
        width: 56px !important;
        height: 44px !important;

        min-width: 56px !important;
        max-width: 56px !important;

        min-height: 44px !important;
        max-height: 44px !important;

        padding: 0 !important;
        margin: 0 auto !important;

        /* UrbanBreeze teal */
        background: #159f9d !important;

        /* DARK / BLACK ARROW */
        color: #07191d !important;

        border: 1px solid #22b7b2 !important;

        border-radius: 10px !important;

        font-size: 29px !important;
        font-weight: 900 !important;

        line-height: 1 !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;

        opacity: 1 !important;

        box-shadow:
            0 4px 12px rgba(0, 0, 0, 0.22) !important;

        transition:
            background 0.15s ease,
            border-color 0.15s ease,
            transform 0.15s ease !important;
    }


    /* Actual arrow/text */

    div.st-key-switch_location_container button p,
    div.st-key-switch_location_container button span {
        color: #07191d !important;
        font-weight: 900 !important;
        opacity: 1 !important;
    }


    /* Hover */

    div.st-key-switch_location_container button:hover {
        background: #20b9b4 !important;
        border-color: #5edbd6 !important;

        color: #000000 !important;

        transform: translateY(-1px) !important;
    }


    div.st-key-switch_location_container button:hover p,
    div.st-key-switch_location_container button:hover span {
        color: #000000 !important;
    }


    /* Click */

    div.st-key-switch_location_container button:active {
        transform: translateY(0) scale(0.96) !important;
    }


    /* ========================================================
       TABS
       ======================================================== */

    div[data-testid="stTabs"] button {
        color: #b9ced1 !important;
        font-weight: 600 !important;
    }


    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #ffffff !important;
    }


    div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        background-color: #16a6a3 !important;
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    .stTextInput input {
        background: #ffffff !important;
        color: #15343a !important;

        border: 1px solid #b9ced1 !important;
        border-radius: 10px !important;
    }


    .stTextInput input::placeholder {
        color: #789197 !important;
    }


    .stTextInput input:focus {
        border-color: #16a6a3 !important;

        box-shadow:
            0 0 0 2px rgba(22,166,163,0.15) !important;
    }


    div[data-baseweb="select"] > div {
        background: #ffffff !important;
        color: #15343a !important;
        border-color: #b9ced1 !important;
    }


    /* ========================================================
       FORM CONTROLS
       ======================================================== */

    div[data-testid="stRadio"] label,
    div[data-testid="stCheckbox"] label {
        color: #dcebed !important;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 900px) {

        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

    }


    @media (max-width: 700px) {

        .block-container {
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-top: 0.65rem !important;
        }


        div.st-key-switch_location_container {
            min-height: 96px !important;
            padding-top: 18px !important;
        }


        div.st-key-switch_location_container div[data-testid="stButton"] {
            width: 50px !important;
            min-width: 50px !important;
        }


        div.st-key-switch_location_container button {
            width: 50px !important;
            height: 40px !important;

            min-width: 50px !important;
            max-width: 50px !important;

            min-height: 40px !important;
            max-height: 40px !important;

            font-size: 25px !important;
        }


        div[data-testid="stButton"] button {
            min-height: 40px !important;

            padding-left: 8px !important;
            padding-right: 8px !important;

            font-size: 12px !important;
        }


        div.st-key-plan_profile_icon button {
            width: 40px !important;
            height: 40px !important;

            min-width: 40px !important;
            max-width: 40px !important;

            min-height: 40px !important;
            max-height: 40px !important;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "start_result" not in st.session_state:
    st.session_state.start_result = None

if "destination_result" not in st.session_state:
    st.session_state.destination_result = None

if "start_location" not in st.session_state:
    st.session_state.start_location = ""

if "destination" not in st.session_state:
    st.session_state.destination = ""

if "start_coords" not in st.session_state:
    st.session_state.start_coords = None

if "destination_coords" not in st.session_state:
    st.session_state.destination_coords = None

if "travel_mode" not in st.session_state:
    st.session_state.travel_mode = "EV"

if "prefer_cooler" not in st.session_state:
    st.session_state.prefer_cooler = True

if "max_extra_time" not in st.session_state:
    st.session_state.max_extra_time = 5

if "prefer_charging" not in st.session_state:
    st.session_state.prefer_charging = False

if "route_form_version" not in st.session_state:
    st.session_state.route_form_version = 0

if "loaded_route_initial_texts" not in st.session_state:
    st.session_state.loaded_route_initial_texts = {}


# ============================================================
# LOAD ROUTE FROM HISTORY / SAVED PLACE
# ============================================================

def load_route_from_previous_page():

    route_data = None

    possible_route_keys = [
        "route_to_replan",
        "replay_route",
        "history_route",
        "route_history_item",
        "selected_history_route",
        "use_route_again"
    ]

    for key in possible_route_keys:

        if key in st.session_state:

            value = st.session_state.get(key)

            if isinstance(value, dict):

                route_data = value

                del st.session_state[key]

                break


    # ========================================================
    # FULL ROUTE REPLAY
    # ========================================================

    if route_data:

        start_name = (
            route_data.get("start_location")
            or route_data.get("start")
            or route_data.get("origin")
            or route_data.get("from")
        )

        destination_name = (
            route_data.get("destination")
            or route_data.get("destination_location")
            or route_data.get("end")
            or route_data.get("to")
        )

        start_coords = (
            route_data.get("start_coords")
            or route_data.get("origin_coords")
        )

        destination_coords = (
            route_data.get("destination_coords")
            or route_data.get("end_coords")
        )


        # ----------------------------------------------------
        # LOAD START
        # ----------------------------------------------------

        if start_name:

            st.session_state.start_location = str(
                start_name
            )

            if isinstance(start_coords, dict):

                lat = start_coords.get("lat")
                lon = start_coords.get("lon")

                if lat is not None and lon is not None:

                    st.session_state.start_result = {
                        "display_name": str(start_name),
                        "lat": float(lat),
                        "lon": float(lon),
                        "address": {}
                    }


        # ----------------------------------------------------
        # LOAD DESTINATION
        # ----------------------------------------------------

        if destination_name:

            st.session_state.destination = str(
                destination_name
            )

            if isinstance(destination_coords, dict):

                lat = destination_coords.get("lat")
                lon = destination_coords.get("lon")

                if lat is not None and lon is not None:

                    st.session_state.destination_result = {
                        "display_name": str(destination_name),
                        "lat": float(lat),
                        "lon": float(lon),
                        "address": {}
                    }


        st.session_state.loaded_route_initial_texts = {
            "start_map": str(start_name or ""),
            "destination_map": str(destination_name or "")
        }


        # ----------------------------------------------------
        # TRAVEL MODE
        # ----------------------------------------------------

        saved_mode = route_data.get(
            "travel_mode"
        )

        if saved_mode:
            st.session_state.travel_mode = saved_mode


        # ----------------------------------------------------
        # PREFER COOLER
        # ----------------------------------------------------

        if "prefer_cooler" in route_data:

            st.session_state.prefer_cooler = bool(
                route_data["prefer_cooler"]
            )


        # ----------------------------------------------------
        # MAX EXTRA TIME
        # ----------------------------------------------------

        if "max_extra_time" in route_data:

            try:

                st.session_state.max_extra_time = int(
                    route_data["max_extra_time"]
                )

            except (
                TypeError,
                ValueError
            ):

                st.session_state.max_extra_time = 5


        # ----------------------------------------------------
        # PREFER CHARGING
        # ----------------------------------------------------

        if "prefer_charging" in route_data:

            st.session_state.prefer_charging = bool(
                route_data["prefer_charging"]
            )


        return True


    # ========================================================
    # SAVED PLACE
    # ========================================================

    saved_place = None

    if "saved_route_place" in st.session_state:

        value = st.session_state.get(
            "saved_route_place"
        )

        if isinstance(value, dict):

            saved_place = value

            del st.session_state[
                "saved_route_place"
            ]


    if saved_place:

        name = (
            saved_place.get("display_name")
            or saved_place.get("name")
            or "Saved place"
        )

        lat = saved_place.get("lat")
        lon = saved_place.get("lon")


        st.session_state.destination = str(
            name
        )


        if lat is not None and lon is not None:

            st.session_state.destination_result = {
                "display_name": str(name),
                "lat": float(lat),
                "lon": float(lon),
                "address": {}
            }

            st.session_state.loaded_route_initial_texts = {
                "start_map":
                    st.session_state.get(
                        "start_location",
                        ""
                    ),

                "destination_map":
                    str(name)
            }


        return True


    return False


# ============================================================
# LOAD PREVIOUS ROUTE
# ============================================================

route_loaded = load_route_from_previous_page()


# ============================================================
# NAVIGATION
# ============================================================

nav_logo, nav_plan, nav_saved, nav_history, nav_profile = st.columns(
    [4.5, 1.2, 1.2, 1.1, 0.7]
)


with nav_logo:

    logo()


with nav_plan:

    if st.button(
        "Plan Route",
        key="nav_plan_route",
        use_container_width=True
    ):

        st.switch_page(
            "pages/1_Plan_Route.py"
        )


with nav_saved:

    if st.button(
        "Saved Places",
        key="nav_saved_places",
        use_container_width=True
    ):

        st.switch_page(
            "pages/3_Saved_Places.py"
        )


with nav_history:

    if st.button(
        "History",
        key="nav_history",
        use_container_width=True
    ):

        st.switch_page(
            "pages/4_Route_History.py"
        )


with nav_profile:

    if st.button(
        "👤",
        key="plan_profile_icon",
        help="View profile",
        use_container_width=True
    ):

        st.switch_page(
            "pages/5_Profile.py"
        )


st.divider()


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    "### CLIMATE-AWARE ROUTING"
)

st.title(
    "Plan your smart route."
)

st.caption(
    "Search for an address, city or street in California, "
    "or pin your location directly on the map."
)


# ============================================================
# ROUTE LOADED MESSAGE
# ============================================================

if route_loaded:

    st.success(
        "Your previous route has been loaded. "
        "You can edit the locations before planning."
    )


# ============================================================
# LOCATION PICKER
# ============================================================

def location_picker(
    label,
    icon,
    session_key,
    location_text_key,
    map_key
):

    st.subheader(
        f"{icon} {label}"
    )


    widget_version = st.session_state.get(
        "route_form_version",
        0
    )

    widget_key = (
        f"{map_key}_{widget_version}"
    )


    # ========================================================
    # CURRENT LOCATION
    # ========================================================

    current = st.session_state.get(
        session_key
    )


    # ========================================================
    # SEARCH / MAP TABS
    # ========================================================

    tab_search, tab_map = st.tabs(
        [
            "Search",
            "Pick on map"
        ]
    )


    # ========================================================
    # SEARCH
    # ========================================================

    with tab_search:

        current_text = st.session_state.get(
            location_text_key,
            ""
        )


        query = st.text_input(
            f"Search {label.lower()}",
            value=current_text,
            placeholder="Street, address, city, ZIP code...",
            key=f"{widget_key}_search",
            label_visibility="collapsed"
        )


        st.session_state[
            location_text_key
        ] = query


        current_is_valid = (
            isinstance(current, dict)
            and current.get("lat") is not None
            and current.get("lon") is not None
        )


        initial_loaded_text = (
            st.session_state.get(
                "loaded_route_initial_texts",
                {}
            ).get(map_key)
        )


        loaded_location = (
            current_is_valid
            and initial_loaded_text is not None
            and query.strip()
            == str(initial_loaded_text).strip()
        )


        if loaded_location:

            results = None

        elif len(query.strip()) >= 3:

            with st.spinner(
                "Searching California..."
            ):

                results = search_california_locations(
                    query
                )

        else:

            results = None


        if results:

            options = [
                result["display_name"]
                for result in results
            ]


            selected_index = 0


            if current:

                current_name = current.get(
                    "display_name",
                    ""
                )

                if current_name in options:

                    selected_index = options.index(
                        current_name
                    )


            selected = st.selectbox(
                f"Select your {label.lower()}",
                options,
                index=selected_index,
                key=f"{widget_key}_selection",
                label_visibility="collapsed"
            )


            selected_result = next(
                (
                    result
                    for result in results
                    if result["display_name"] == selected
                ),
                None
            )


            if selected_result:

                st.session_state[
                    session_key
                ] = selected_result


                st.session_state[
                    location_text_key
                ] = selected_result[
                    "display_name"
                ]


                st.session_state.setdefault(
                    "loaded_route_initial_texts",
                    {}
                ).pop(
                    map_key,
                    None
                )


        elif (
            not loaded_location
            and len(query.strip()) >= 3
        ):

            st.warning(
                "No California locations found. "
                "Try a more specific search."
            )


    # ========================================================
    # MAP
    # ========================================================

    with tab_map:

        st.caption(
            f"Click anywhere on the map to set your "
            f"{label.lower()}."
        )


        if current:

            map_location = [
                current["lat"],
                current["lon"]
            ]

            zoom = 13

        else:

            map_location = [
                36.7783,
                -119.4179
            ]

            zoom = 6


        m = folium.Map(
            location=map_location,
            zoom_start=zoom,
            control_scale=True
        )


        if current:

            folium.Marker(
                location=[
                    current["lat"],
                    current["lon"]
                ],
                tooltip=(
                    f"Selected "
                    f"{label.lower()}"
                ),
                popup=label
            ).add_to(m)


        map_data = st_folium(
            m,
            width=None,
            height=350,
            use_container_width=True,
            key=widget_key
        )


        clicked = (
            map_data.get("last_clicked")
            if map_data
            else None
        )


        if clicked:

            lat = clicked.get("lat")
            lon = clicked.get("lng")


            if lat is not None and lon is not None:

                pinned_name = (
                    f"Pinned {label.lower()}"
                )


                st.session_state[
                    session_key
                ] = {
                    "display_name": pinned_name,
                    "lat": lat,
                    "lon": lon,
                    "address": {}
                }


                st.session_state[
                    location_text_key
                ] = pinned_name


                st.session_state.setdefault(
                    "loaded_route_initial_texts",
                    {}
                ).pop(
                    map_key,
                    None
                )


                st.rerun()


    # ========================================================
    # CONFIRMATION
    # ========================================================

    current = st.session_state.get(
        session_key
    )


    if current:

        st.success(
            f"{current['display_name']}  •  "
            f"{current['lat']:.5f}, "
            f"{current['lon']:.5f}"
        )


# ============================================================
# SWITCH LOCATIONS
# ============================================================

def switch_locations():

    old_start_result = st.session_state.get(
        "start_result"
    )

    old_destination_result = st.session_state.get(
        "destination_result"
    )


    old_start_location = st.session_state.get(
        "start_location",
        ""
    )

    old_destination = st.session_state.get(
        "destination",
        ""
    )


    # --------------------------------------------------------
    # Swap result objects
    # --------------------------------------------------------

    st.session_state.start_result = (
        old_destination_result
    )

    st.session_state.destination_result = (
        old_start_result
    )


    # --------------------------------------------------------
    # Swap displayed text
    # --------------------------------------------------------

    st.session_state.start_location = (
        old_destination
    )

    st.session_state.destination = (
        old_start_location
    )


    # --------------------------------------------------------
    # Swap coordinates
    # --------------------------------------------------------

    old_start_coords = st.session_state.get(
        "start_coords"
    )

    old_destination_coords = st.session_state.get(
        "destination_coords"
    )


    st.session_state.start_coords = (
        old_destination_coords
    )

    st.session_state.destination_coords = (
        old_start_coords
    )


    # --------------------------------------------------------
    # Prevent unnecessary geocoding
    # --------------------------------------------------------

    st.session_state.loaded_route_initial_texts = {
        "start_map": old_destination,
        "destination_map": old_start_location
    }


    # --------------------------------------------------------
    # Refresh location widgets
    # --------------------------------------------------------

    st.session_state.route_form_version = (
        st.session_state.get(
            "route_form_version",
            0
        ) + 1
    )


# ============================================================
# START / DESTINATION
# ============================================================

st.markdown(
    "### Route locations"
)


# ============================================================
# THREE COLUMN LAYOUT
# ============================================================

col_start, col_switch, col_dest = st.columns(
    [1, 0.18, 1],
    gap="small"
)


# ============================================================
# STARTING POINT
# ============================================================

with col_start:

    location_picker(
        "Starting point",
        "📍",
        "start_result",
        "start_location",
        "start_map"
    )


# ============================================================
# SWITCH BUTTON
# ============================================================

with col_switch:

    with st.container(
        key="switch_location_container"
    ):

        if st.button(
            "⇄",
            key="switch_locations",
            type="secondary"
        ):

            switch_locations()

            st.rerun()


# ============================================================
# DESTINATION
# ============================================================

with col_dest:

    location_picker(
        "Destination",
        "🎯",
        "destination_result",
        "destination",
        "destination_map"
    )


# ============================================================
# TRAVEL MODE & PREFERENCES
# ============================================================

st.subheader(
    "Travel & preferences"
)


pref_col1, pref_col2 = st.columns(
    2
)


# ============================================================
# TRAVEL MODE
# ============================================================

with pref_col1:

    travel_modes = [
        "Walk",
        "Cycle",
        "EV"
    ]


    current_mode = st.session_state.get(
        "travel_mode",
        "EV"
    )


    if current_mode not in travel_modes:

        current_mode = "EV"


    mode_index = travel_modes.index(
        current_mode
    )


    travel_mode = st.radio(
        "How are you travelling?",
        travel_modes,
        index=mode_index,
        horizontal=True,
        key="travel_mode_selector"
    )


    st.session_state.travel_mode = (
        travel_mode
    )


    prefer_charging = False


    if travel_mode == "EV":

        prefer_charging = st.checkbox(
            "Prefer routes with charging stations",
            value=st.session_state.get(
                "prefer_charging",
                False
            ),
            key="prefer_charging_checkbox"
        )


# ============================================================
# CLIMATE PREFERENCES
# ============================================================

with pref_col2:

    prefer_cooler = st.checkbox(
        "Prefer a cooler route",
        value=st.session_state.get(
            "prefer_cooler",
            True
        ),
        key="prefer_cooler_checkbox"
    )


    max_extra_time = st.slider(
        "Maximum additional travel time (minutes)",
        min_value=0,
        max_value=30,
        value=st.session_state.get(
            "max_extra_time",
            5
        ),
        step=1,
        key="max_extra_time_slider"
    )


# ============================================================
# FIND ROUTES
# ============================================================

st.write("")


find_routes = st.button(
    "FIND SMART ROUTES",
    type="primary",
    use_container_width=True,
    key="find_smart_routes"
)


# ============================================================
# PROCESS ROUTE
# ============================================================

if find_routes:

    start_result = st.session_state.get(
        "start_result"
    )


    destination_result = st.session_state.get(
        "destination_result"
    )


    # ========================================================
    # VALIDATION
    # ========================================================

    if start_result is None:

        st.error(
            "Please search for or pin your starting point."
        )

        st.stop()


    if destination_result is None:

        st.error(
            "Please search for or pin your destination."
        )

        st.stop()


    # ========================================================
    # SAVE LOCATION INFORMATION
    # ========================================================

    st.session_state[
        "start_location"
    ] = start_result[
        "display_name"
    ]


    st.session_state[
        "destination"
    ] = destination_result[
        "display_name"
    ]


    st.session_state[
        "start_coords"
    ] = {

        "lat":
            start_result["lat"],

        "lon":
            start_result["lon"],

        "name":
            start_result["display_name"]
    }


    st.session_state[
        "destination_coords"
    ] = {

        "lat":
            destination_result["lat"],

        "lon":
            destination_result["lon"],

        "name":
            destination_result["display_name"]
    }


    # ========================================================
    # SAVE TRAVEL SETTINGS
    # ========================================================

    st.session_state[
        "travel_mode"
    ] = travel_mode


    st.session_state[
        "prefer_cooler"
    ] = prefer_cooler


    st.session_state[
        "max_extra_time"
    ] = max_extra_time


    st.session_state[
        "prefer_charging"
    ] = prefer_charging


    # ========================================================
    # GO TO ROUTE RESULTS
    # ========================================================

    st.switch_page(
        "pages/2_Route_Results.py"
    )
