import os
import sys

# Get the directory of the current file and add it to python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Now your original imports will work flawlessly
import streamlit as st
import folium
from streamlit_folium import st_folium
from utils.routing import search_california_locations


# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Plan Route | UrbanBreeze",
    page_icon="🗺️",
    layout="wide"
)


# ============================================
# CSS
# ============================================

st.markdown("""
<style>

.stApp {
    background-color: #f6fbfc;
}

.block-container {
    padding-top: 2rem;
    padding-left: 5%;
    padding-right: 5%;
}


/* Navigation */

.logo {
    color: #123f4b;
    font-size: 25px;
    font-weight: 700;
}


/* Page title */

.page-heading {
    color: #123f4b;
    font-size: 42px;
    font-weight: 700;
    margin-top: 25px;
}

.page-description {
    color: #71858b;
    font-size: 17px;
    margin-bottom: 25px;
}


/* Location boxes */

.location-box {
    background-color: white;
    border: 1px solid #e3edef;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 15px rgba(18, 63, 75, 0.05);
}


/* Selected location */

.selected-location {
    background-color: #e9f7f6;
    border-radius: 12px;
    padding: 12px;
    color: #286168;
    margin-top: 10px;
}


/* Map heading */

.map-title {
    color: #123f4b;
    font-size: 22px;
    font-weight: 650;
}

</style>
""", unsafe_allow_html=True)


# ============================================
# NAVIGATION
# ============================================

nav1, nav2, nav3, nav4 = st.columns(
    [4, 1, 1, 1]
)


with nav1:

    st.markdown(
        '<div class="logo">🌬️ UrbanBreeze</div>',
        unsafe_allow_html=True
    )


with nav2:

    if st.button("Home"):

        st.switch_page("app.py")


with nav3:

    st.write("Plan Route")


with nav4:

    st.write("History")


st.divider()


# ============================================
# PAGE TITLE
# ============================================

st.markdown(
    '<div class="page-heading">'
    'Plan your smart route'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="page-description">

    Search for an address, city or street in California,
    or simply pin your location directly on the map.

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================
# INITIALIZE SESSION STATE
# ============================================

if "start_result" not in st.session_state:

    st.session_state["start_result"] = None


if "destination_result" not in st.session_state:

    st.session_state["destination_result"] = None


# ============================================
# STARTING LOCATION
# ============================================

st.markdown(
    '<div class="location-box">',
    unsafe_allow_html=True
)

st.subheader("📍 Starting point")


start_method = st.radio(
    "How do you want to select your starting point?",
    [
        "🔎 Search",
        "📍 Pick on map"
    ],
    horizontal=True,
    key="start_method"
)


# ============================================
# START — SEARCH
# ============================================

if start_method == "🔎 Search":

    start_search = st.text_input(
        "Search starting location",
        placeholder=(
            "Street, address, city, ZIP code..."
        ),
        key="start_search"
    )


    if len(start_search.strip()) >= 3:

        with st.spinner(
            "Searching California..."
        ):

            start_results = (
                search_california_locations(
                    start_search
                )
            )


        if start_results:

            start_options = [
                result["display_name"]
                for result in start_results
            ]


            selected_start = st.selectbox(
                "Select your starting location",
                start_options,
                key="start_selection"
            )


            selected_start_result = next(
                result
                for result in start_results
                if result["display_name"]
                == selected_start
            )


            st.session_state[
                "start_result"
            ] = selected_start_result


            st.success(
                "Starting location selected."
            )


        else:

            st.warning(
                "No California locations found. "
                "Try a more specific search."
            )


# ============================================
# START — MAP
# ============================================

else:

    st.write(
        "Click anywhere on the California map "
        "to choose your starting point."
    )


    # California approximate center

    start_map = folium.Map(
        location=[
            36.7783,
            -119.4179
        ],
        zoom_start=6
    )


    # Add California marker if already selected

    if st.session_state["start_result"]:

        result = st.session_state[
            "start_result"
        ]

        folium.Marker(
            location=[
                result["lat"],
                result["lon"]
            ],
            tooltip="Selected starting point",
            popup="Starting point"
        ).add_to(start_map)


    start_map_data = st_folium(
        start_map,
        width=900,
        height=400,
        key="start_map"
    )


    # Detect click

    if start_map_data:

        clicked = start_map_data.get(
            "last_clicked"
        )


        if clicked:

            st.session_state[
                "start_result"
            ] = {

                "display_name":
                    "Pinned starting point",

                "lat":
                    clicked["lat"],

                "lon":
                    clicked["lng"],

                "address": {}
            }


            st.success(
                "Starting point pinned on the map."
            )


# ============================================
# DISPLAY START LOCATION
# ============================================

if st.session_state["start_result"]:

    result = st.session_state[
        "start_result"
    ]

    st.markdown(
        f"""
        <div class="selected-location">

        <b>📍 Starting point selected</b>

        <br><br>

        {result["display_name"]}

        <br>

        Coordinates:
        {result["lat"]:.5f},
        {result["lon"]:.5f}

        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("</div>", unsafe_allow_html=True)


# ============================================
# DESTINATION
# ============================================

st.markdown(
    '<div class="location-box">',
    unsafe_allow_html=True
)

st.subheader("🎯 Destination")


destination_method = st.radio(
    "How do you want to select your destination?",
    [
        "🔎 Search",
        "📍 Pick on map"
    ],
    horizontal=True,
    key="destination_method"
)


# ============================================
# DESTINATION — SEARCH
# ============================================

if destination_method == "🔎 Search":

    destination_search = st.text_input(
        "Search destination",
        placeholder=(
            "Street, address, city, ZIP code..."
        ),
        key="destination_search"
    )


    if len(destination_search.strip()) >= 3:

        with st.spinner(
            "Searching California..."
        ):

            destination_results = (
                search_california_locations(
                    destination_search
                )
            )


        if destination_results:

            destination_options = [
                result["display_name"]
                for result in destination_results
            ]


            selected_destination = st.selectbox(
                "Select your destination",
                destination_options,
                key="destination_selection"
            )


            selected_destination_result = next(
                result
                for result in destination_results
                if result["display_name"]
                == selected_destination
            )


            st.session_state[
                "destination_result"
            ] = selected_destination_result


            st.success(
                "Destination selected."
            )


        else:

            st.warning(
                "No California locations found. "
                "Try a more specific search."
            )


# ============================================
# DESTINATION — MAP
# ============================================

else:

    st.write(
        "Click anywhere on the California map "
        "to choose your destination."
    )


    destination_map = folium.Map(
        location=[
            36.7783,
            -119.4179
        ],
        zoom_start=6
    )


    # Add destination marker

    if st.session_state[
        "destination_result"
    ]:

        result = st.session_state[
            "destination_result"
        ]

        folium.Marker(
            location=[
                result["lat"],
                result["lon"]
            ],
            tooltip="Selected destination",
            popup="Destination"
        ).add_to(destination_map)


    destination_map_data = st_folium(
        destination_map,
        width=900,
        height=400,
        key="destination_map"
    )


    # Detect click

    if destination_map_data:

        clicked = destination_map_data.get(
            "last_clicked"
        )


        if clicked:

            st.session_state[
                "destination_result"
            ] = {

                "display_name":
                    "Pinned destination",

                "lat":
                    clicked["lat"],

                "lon":
                    clicked["lng"],

                "address": {}
            }


            st.success(
                "Destination pinned on the map."
            )


# ============================================
# DISPLAY DESTINATION
# ============================================

if st.session_state[
    "destination_result"
]:

    result = st.session_state[
        "destination_result"
    ]

    st.markdown(
        f"""
        <div class="selected-location">

        <b>🎯 Destination selected</b>

        <br><br>

        {result["display_name"]}

        <br>

        Coordinates:
        {result["lat"]:.5f},
        {result["lon"]:.5f}

        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("</div>", unsafe_allow_html=True)


# ============================================
# TRAVEL MODE
# ============================================

st.subheader("🚗 How are you travelling?")

travel_mode = st.radio(
    "Travel mode",
    [
        "🚶 Walk",
        "🚲 Cycle",
        "🚗 EV"
    ],
    horizontal=True,
    label_visibility="collapsed"
)


# ============================================
# ROUTE PREFERENCES
# ============================================

st.subheader("🌡️ Route preferences")


prefer_cooler = st.checkbox(
    "Prefer a cooler route",
    value=True
)


max_extra_time = st.slider(
    "Maximum additional travel time",
    min_value=0,
    max_value=30,
    value=5,
    step=1
)


st.caption(
    f"Maximum extra time: "
    f"{max_extra_time} minutes"
)


# ============================================
# EV CHARGING
# ============================================

prefer_charging = False


if travel_mode == "🚗 EV":

    prefer_charging = st.checkbox(
        "🔋 Prefer routes with charging stations"
    )


# ============================================
# FIND ROUTES
# ============================================

st.write("")


find_routes = st.button(
    "🌡️ FIND SMART ROUTES",
    type="primary",
    use_container_width=True
)


# ============================================
# BUTTON LOGIC
# ============================================

if find_routes:

    start_result = st.session_state[
        "start_result"
    ]

    destination_result = st.session_state[
        "destination_result"
    ]


    # -----------------------------------------
    # Check start
    # -----------------------------------------

    if start_result is None:

        st.error(
            "Please search for or pin your "
            "starting point."
        )

        st.stop()


    # -----------------------------------------
    # Check destination
    # -----------------------------------------

    if destination_result is None:

        st.error(
            "Please search for or pin your "
            "destination."
        )

        st.stop()


    # -----------------------------------------
    # Store locations
    # -----------------------------------------

    st.session_state[
        "start_location"
    ] = start_result["display_name"]


    st.session_state[
        "destination"
    ] = destination_result["display_name"]


    # -----------------------------------------
    # Store exact coordinates
    # -----------------------------------------

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


    # -----------------------------------------
    # Store preferences
    # -----------------------------------------

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


    # -----------------------------------------
    # Move to results
    # -----------------------------------------

    st.switch_page(
        "pages/2_Route_Results.py"
    )