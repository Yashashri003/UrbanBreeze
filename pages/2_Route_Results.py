import streamlit as st
import folium

from streamlit_folium import st_folium

from utils.routing import get_routes

from utils.climate import (
    analyze_route_temperature,
    compare_routes
)


# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Route Results | UrbanBreeze",
    page_icon="🗺️",
    layout="wide"
)


# ============================================
# CSS
# ============================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f6fbfc;
    }

    .block-container {
        padding-top: 2rem;
        padding-left: 4%;
        padding-right: 4%;
        padding-bottom: 4rem;
    }

    /* Route cards */
    .route-card {
        background-color: white;
        border: 1px solid #e3edef;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 15px;
        box-shadow: 0px 4px 15px rgba(18, 63, 75, 0.05);
    }

    .ai-card {
        background-color: #e9f7f6;
        border: 2px solid #159c9c;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 15px;
        box-shadow: 0px 6px 20px rgba(21, 156, 156, 0.08);
    }

    .small-label {
        color: #71858b;
        font-size: 0.85rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================
# GET USER DATA
# ============================================

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

max_extra_time = st.session_state.get(
    "max_extra_time",
    5
)

prefer_charging = st.session_state.get(
    "prefer_charging",
    False
)


# ============================================
# GET EXACT COORDINATES
# ============================================

start_coords = st.session_state.get(
    "start_coords"
)

destination_coords = st.session_state.get(
    "destination_coords"
)


# ============================================
# CHECK START COORDINATES
# ============================================

if start_coords is None:

    st.error(
        "Starting point coordinates are missing."
    )

    st.info(
        "Please return to Plan Route and "
        "select a California starting location."
    )

    if st.button(
        "← Go back to Plan Route"
    ):
        st.switch_page(
            "pages/1_Plan_Route.py"
        )

    st.stop()


# ============================================
# CHECK DESTINATION COORDINATES
# ============================================

if destination_coords is None:

    st.error(
        "Destination coordinates are missing."
    )

    st.info(
        "Please return to Plan Route and "
        "select a California destination."
    )

    if st.button(
        "← Go back to Plan Route"
    ):
        st.switch_page(
            "pages/1_Plan_Route.py"
        )

    st.stop()


# ============================================
# NAVIGATION
# ============================================

nav1, nav2, nav3, nav4 = st.columns(
    [4, 1, 1, 1]
)

with nav1:

    st.markdown(
        "## 🌬️ UrbanBreeze"
    )

with nav2:

    if st.button(
        "Home",
        use_container_width=True
    ):
        st.switch_page(
            "app.py"
        )

with nav3:

    if st.button(
        "Plan Route",
        use_container_width=True
    ):
        st.switch_page(
            "pages/1_Plan_Route.py"
        )

with nav4:

    if st.button(
        "History",
        use_container_width=True
    ):
        st.switch_page(
            "pages/4_Route_History.py"
        )


st.divider()


# ============================================
# PAGE TITLE
# ============================================

st.title(
    "🗺️ Smart Route Results"
)

st.write(
    f"**{start_location}** → **{destination}**"
)

st.caption(
    f"Travel mode: {travel_mode}"
)


# ============================================
# CALCULATE ROUTES
# ============================================

with st.spinner(
    "Finding the best route options..."
):

    routes = get_routes(
        start_coords,
        destination_coords,
        travel_mode
    )


# ============================================
# CHECK ROUTES
# ============================================

if not routes:

    st.error(
        "We could not calculate a route "
        "between these locations."
    )

    st.info(
        "Please try another California "
        "starting point or destination."
    )

    if st.button(
        "← Try another route"
    ):
        st.switch_page(
            "pages/1_Plan_Route.py"
        )

    st.stop()


# ============================================
# BASIC ROUTE INFORMATION
# ============================================

fastest_route = min(
    routes,
    key=lambda route: route["duration_min"]
)

shortest_route = min(
    routes,
    key=lambda route: route["distance_km"]
)


# ============================================
# CLIMATE ANALYSIS
# ============================================

st.subheader(
    "🌡️ Climate analysis"
)

st.caption(
    "Analyzing temperature along your "
    "California routes using FortyGuard."
)


for index, route in enumerate(routes):

    with st.spinner(
        f"Analyzing route {index + 1}..."
    ):

        climate_result = analyze_route_temperature(
            route,
            number_of_points=5
        )

    route["climate"] = climate_result


# ============================================
# COMPARE ROUTES
# ============================================

route_comparison = compare_routes(
    routes,
    prefer_cooler=prefer_cooler
)


fastest_route = route_comparison["fastest"]

coolest_route = route_comparison["coolest"]

ai_pick = route_comparison["ai_pick"]


# ============================================
# SAFETY CHECK
# ============================================

if fastest_route is None:

    st.error(
        "Unable to determine the fastest route."
    )

    st.stop()


if ai_pick is None:

    ai_pick = fastest_route


# ============================================
# ROUTE TYPES
# ============================================

for route in routes:

    route["type"] = "Alternative"

    if (
        route["route_number"]
        == fastest_route["route_number"]
    ):

        route["type"] = "Fastest"

    elif (
        route["route_number"]
        == shortest_route["route_number"]
    ):

        route["type"] = "Shortest"


# ============================================
# CLIMATE LABELS
# ============================================

for route in routes:

    route["climate_label"] = ""

    if coolest_route:

        if (
            route["route_number"]
            == coolest_route["route_number"]
        ):

            route["climate_label"] = "🥶 Coolest"


# ============================================
# SUMMARY
# ============================================

st.subheader(
    "Your route options"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "⚡ Fastest",
        f"{fastest_route['duration_min']:.0f} min"
    )

with col2:

    st.metric(
        "📍 Shortest",
        f"{shortest_route['distance_km']:.1f} km"
    )

with col3:

    st.metric(
        "🛣️ Routes found",
        len(routes)
    )


# ============================================
# MAP
# ============================================

st.subheader(
    "🗺️ Route map"
)


# --------------------------------------------
# Calculate map center
# --------------------------------------------

center_lat = (
    start_coords["lat"]
    + destination_coords["lat"]
) / 2

center_lon = (
    start_coords["lon"]
    + destination_coords["lon"]
) / 2


# --------------------------------------------
# Create map
# --------------------------------------------

route_map = folium.Map(
    location=[
        center_lat,
        center_lon
    ],
    zoom_start=12,
    control_scale=True
)


# ============================================
# START MARKER
# ============================================

folium.Marker(
    location=[
        start_coords["lat"],
        start_coords["lon"]
    ],
    tooltip="Starting point",
    popup=start_location
).add_to(route_map)


# ============================================
# DESTINATION MARKER
# ============================================

folium.Marker(
    location=[
        destination_coords["lat"],
        destination_coords["lon"]
    ],
    tooltip="Destination",
    popup=destination
).add_to(route_map)


# ============================================
# DRAW ROUTES
# ============================================

for route in routes:

    coordinates = route["geometry"]["coordinates"]

    # Convert longitude, latitude
    # to latitude, longitude

    route_points = [
        [
            point[1],
            point[0]
        ]
        for point in coordinates
    ]


    # ----------------------------------------
    # AI route
    # ----------------------------------------

    if (
        route["route_number"]
        == ai_pick["route_number"]
    ):

        line_weight = 7
        line_opacity = 0.9
        line_color = "#159c9c"
        tooltip_text = "🤖 AI Pick"

    else:

        line_weight = 4
        line_opacity = 0.55
        line_color = "#5d7d84"
        tooltip_text = route["type"]


    # ----------------------------------------
    # Draw route
    # ----------------------------------------

    folium.PolyLine(
        locations=route_points,
        color=line_color,
        weight=line_weight,
        opacity=line_opacity,
        tooltip=tooltip_text
    ).add_to(route_map)


# ============================================
# DISPLAY MAP
# ============================================

st_folium(
    route_map,
    width=1100,
    height=550
)


# ============================================
# ROUTE CARDS
# ============================================

st.write("")

st.subheader(
    "🌡️ Route options"
)


# ============================================
# FASTEST ROUTE DATA
# ============================================

fastest_climate = fastest_route.get(
    "climate",
    {}
)

fastest_has_climate = fastest_climate.get(
    "success",
    False
)


if fastest_has_climate:

    fastest_temperature = fastest_climate.get(
        "average_temperature"
    )

    fastest_exposure = fastest_climate.get(
        "heat_exposure",
        "Unknown"
    )

    fastest_cool_score = fastest_climate.get(
        "cool_score"
    )

else:

    fastest_temperature = None
    fastest_exposure = "Unavailable"
    fastest_cool_score = None


# ============================================
# FASTEST ROUTE CARD
# ============================================

with st.container(border=True):

    st.subheader(
        "⚡ Fastest Route"
    )

    info1, info2 = st.columns(2)

    with info1:

        st.write(
            f"⏱️ **{fastest_route['duration_min']:.0f} min**"
        )

    with info2:

        st.write(
            f"📍 **{fastest_route['distance_km']:.1f} km**"
        )


    if fastest_temperature is not None:

        st.write(
            f"🌡️ Average temperature: "
            f"**{fastest_temperature:.1f}°C**"
        )

    else:

        st.write(
            "🌡️ Average temperature: "
            "**Unavailable**"
        )


    st.write(
        f"🔥 Heat exposure: "
        f"**{fastest_exposure}**"
    )


    if fastest_cool_score is not None:

        st.write(
            f"🧊 Cool Score: "
            f"**{fastest_cool_score} / 100**"
        )

    else:

        st.write(
            "🧊 Cool Score: "
            "**Unavailable**"
        )


    st.caption(
        "Best option when travel time is "
        "the main priority."
    )


# ============================================
# AI PICK DATA
# ============================================

ai_climate = ai_pick.get(
    "climate",
    {}
)

ai_has_climate = ai_climate.get(
    "success",
    False
)


if ai_has_climate:

    ai_temperature = ai_climate.get(
        "average_temperature"
    )

    ai_exposure = ai_climate.get(
        "heat_exposure",
        "Unknown"
    )

    ai_cool_score = ai_climate.get(
        "cool_score"
    )

else:

    ai_temperature = None
    ai_exposure = "Unavailable"
    ai_cool_score = None


# ============================================
# AI PICK SCORE
# ============================================

ai_score = ai_pick.get(
    "ai_score"
)


if ai_score is None:

    ai_score = ai_cool_score


# ============================================
# AI PICK CARD
# ============================================

st.write("")

with st.container(border=True):

    st.subheader(
        "🤖 AI Pick"
    )

    info1, info2 = st.columns(2)

    with info1:

        st.write(
            f"⏱️ **{ai_pick['duration_min']:.0f} min**"
        )

    with info2:

        st.write(
            f"📍 **{ai_pick['distance_km']:.1f} km**"
        )


    if ai_temperature is not None:

        st.write(
            f"🌡️ Average temperature: "
            f"**{ai_temperature:.1f}°C**"
        )

    else:

        st.write(
            "🌡️ Average temperature: "
            "**Unavailable**"
        )


    st.write(
        f"🔥 Heat exposure: "
        f"**{ai_exposure}**"
    )


    if ai_score is not None:

        st.write(
            f"🧊 AI Score: "
            f"**{ai_score} / 100**"
        )

    else:

        st.write(
            "🧊 AI Score: "
            "**Unavailable**"
        )


    st.markdown(
        "**Why this route?**"
    )

    if prefer_cooler and ai_has_climate:

        if fastest_route["route_number"] != ai_pick["route_number"]:

            time_difference = (
                ai_pick["duration_min"]
                - fastest_route["duration_min"]
            )

            time_difference = max(
                0,
                time_difference
            )

            st.write(
                f"This route balances travel time "
                f"with climate comfort. It is "
                f"approximately **{time_difference:.0f} "
                f"minutes slower** than the fastest "
                f"route while providing better "
                f"climate comfort."
            )

        else:

            st.write(
                "This route provides the best "
                "overall balance between travel "
                "time and climate comfort."
            )

    elif not prefer_cooler:

        st.write(
            "You did not prioritize cooler routes, "
            "so the recommendation favors travel "
            "time."
        )

    else:

        st.write(
            "This route was selected based on "
            "the available route information."
        )


    st.caption(
        "Climate preference weighting: "
        "70% climate + 30% travel time."
    )


# ============================================
# COOLEST ROUTE CARD
# ============================================

if coolest_route:

    if (
        coolest_route["route_number"]
        != ai_pick["route_number"]
    ):

        coolest_climate = coolest_route.get(
            "climate",
            {}
        )

        if coolest_climate.get(
            "success",
            False
        ):

            coolest_temperature = coolest_climate.get(
                "average_temperature"
            )

            coolest_exposure = coolest_climate.get(
                "heat_exposure",
                "Unknown"
            )

            coolest_score = coolest_climate.get(
                "cool_score"
            )


            st.write("")

            with st.container(border=True):

                st.subheader(
                    "🥶 Coolest Route"
                )

                info1, info2 = st.columns(2)

                with info1:

                    st.write(
                        f"⏱️ **{coolest_route['duration_min']:.0f} min**"
                    )

                with info2:

                    st.write(
                        f"📍 **{coolest_route['distance_km']:.1f} km**"
                    )


                if coolest_temperature is not None:

                    st.write(
                        f"🌡️ Average temperature: "
                        f"**{coolest_temperature:.1f}°C**"
                    )


                st.write(
                    f"🔥 Heat exposure: "
                    f"**{coolest_exposure}**"
                )


                if coolest_score is not None:

                    st.write(
                        f"🧊 Cool Score: "
                        f"**{coolest_score} / 100**"
                    )


                st.caption(
                    "This route has the highest "
                    "climate comfort score."
                )


# ============================================
# OTHER ROUTES
# ============================================

for route in routes:

    # ----------------------------------------
    # Don't duplicate AI Pick
    # ----------------------------------------

    if (
        route["route_number"]
        == ai_pick["route_number"]
    ):

        continue


    # ----------------------------------------
    # Don't duplicate Fastest
    # ----------------------------------------

    if (
        route["route_number"]
        == fastest_route["route_number"]
    ):

        continue


    # ----------------------------------------
    # Don't duplicate Coolest
    # ----------------------------------------

    if coolest_route:

        if (
            route["route_number"]
            == coolest_route["route_number"]
        ):

            continue


    # ----------------------------------------
    # Climate information
    # ----------------------------------------

    climate = route.get(
        "climate",
        {}
    )

    has_climate = climate.get(
        "success",
        False
    )


    st.write("")

    with st.container(border=True):

        st.subheader(
            "🛣️ Alternative Route"
        )

        info1, info2 = st.columns(2)

        with info1:

            st.write(
                f"⏱️ **{route['duration_min']:.0f} min**"
            )

        with info2:

            st.write(
                f"📍 **{route['distance_km']:.1f} km**"
            )


        if has_climate:

            st.write(
                f"🌡️ Average temperature: "
                f"**{climate['average_temperature']:.1f}°C**"
            )

            st.write(
                f"🔥 Heat exposure: "
                f"**{climate['heat_exposure']}**"
            )

            st.write(
                f"🧊 Cool Score: "
                f"**{climate['cool_score']} / 100**"
            )

        else:

            st.warning(
                "FortyGuard climate data is "
                "currently unavailable for this route."
            )


# ============================================
# CLIMATE COMFORT
# ============================================

st.write("")

st.subheader(
    "🌡️ Climate comfort"
)

st.caption(
    "Temperature and heat exposure calculated "
    "from FortyGuard data."
)


score1, score2, score3 = st.columns(3)


# ============================================
# FASTEST CLIMATE
# ============================================

with score1:

    with st.container(border=True):

        st.subheader(
            "⚡ Fastest"
        )

        if fastest_has_climate:

            st.metric(
                "Cool Score",
                f"{fastest_cool_score} / 100"
            )

            st.write(
                f"🌡️ "
                f"{fastest_temperature:.1f}°C average"
            )

            st.caption(
                f"Heat exposure: "
                f"{fastest_exposure}"
            )

        else:

            st.warning(
                "FortyGuard data unavailable."
            )


# ============================================
# AI CLIMATE
# ============================================

with score2:

    with st.container(border=True):

        st.subheader(
            "🤖 AI Pick"
        )

        if ai_has_climate:

            st.metric(
                "AI Score",
                f"{ai_score} / 100"
            )

            st.write(
                f"🌡️ "
                f"{ai_temperature:.1f}°C average"
            )

            st.caption(
                "Climate + travel time balance"
            )

        else:

            st.warning(
                "FortyGuard data unavailable."
            )


# ============================================
# COOLEST CLIMATE
# ============================================

with score3:

    with st.container(border=True):

        st.subheader(
            "🥶 Coolest"
        )

        if coolest_route:

            coolest_climate = coolest_route.get(
                "climate",
                {}
            )

            if coolest_climate.get(
                "success",
                False
            ):

                st.metric(
                    "Cool Score",
                    f'{coolest_climate["cool_score"]} / 100'
                )

                st.write(
                    f'🌡️ '
                    f'{coolest_climate["average_temperature"]:.1f}°C average'
                )

                st.caption(
                    f'Heat exposure: '
                    f'{coolest_climate["heat_exposure"]}'
                )

            else:

                st.warning(
                    "FortyGuard data unavailable."
                )

        else:

            st.warning(
                "No climate data available."
            )


# ============================================
# USER PREFERENCES
# ============================================

st.write("")

st.subheader(
    "Your preferences"
)

pref1, pref2, pref3 = st.columns(3)


with pref1:

    st.write(
        "🌡️ Cooler route:",
        "Yes"
        if prefer_cooler
        else "No"
    )


with pref2:

    st.write(
        "⏱️ Extra time:",
        f"{max_extra_time} min"
    )


with pref3:

    if travel_mode == "🚗 EV":

        st.write(
            "🔋 Charging:",
            "Preferred"
            if prefer_charging
            else "Not required"
        )

    else:

        st.write(
            "🚗 EV charging:",
            "Not applicable"
        )


# ============================================
# BACK BUTTON
# ============================================

st.write("")

if st.button(
    "← Change route"
):

    st.switch_page(
        "pages/1_Plan_Route.py"
    )