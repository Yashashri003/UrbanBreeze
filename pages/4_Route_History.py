import streamlit as st
import json
import os


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Route History | UrbanBreeze",
    page_icon="↺",
    layout="wide"
)


# ============================================================
# PATHS
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
# MODERN UI
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background-color: #071a20 !important;
        color: #ffffff !important;
    }

    .block-container {
        max-width: 1240px;
        padding-top: 0.5rem;
        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ========================================================
       ALL TEXT
       ======================================================== */

    body {
        color: #ffffff !important;
    }

    p {
        color: #d7e7ea !important;
    }

    h1,
    h2,
    h3,
    h4 {
        color: #ffffff !important;
    }

    [data-testid="stCaptionContainer"] {
        color: #91aeb5 !important;
    }

    [data-testid="stMarkdownContainer"] {
        color: #ffffff;
    }


    /* ========================================================
       NAVBAR
       ======================================================== */

    .brand-text {
        font-size: 22px;
        font-weight: 750;
        color: #ffffff !important;
        padding-top: 8px;
    }

    .brand-mark {
        color: #2dd4bf !important;
        font-size: 25px;
    }

    .nav-line {
        border-bottom: 1px solid #23434b;
        margin-top: 8px;
        margin-bottom: 30px;
    }


    /* NAVIGATION LINKS */

    [data-testid="stPageLink-NavLink"] {
        color: #d7e7ea !important;
        font-weight: 600 !important;
    }

    [data-testid="stPageLink-NavLink"]:hover {
        color: #2dd4bf !important;
    }


    /* ========================================================
       HISTORY HEADER
       ======================================================== */

    .history-icon-box {
        width: 62px;
        height: 62px;
        border-radius: 16px;

        background-color: #0d3339;

        color: #2dd4bf;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 30px;

        border: 1px solid #22535a;

        box-shadow:
            0 5px 18px rgba(0, 0, 0, 0.25);
    }


    .muted-text {
        color: #91aeb5;
        font-size: 14px;
    }


    /* ========================================================
       SEARCH INPUT
       ======================================================== */

    .stTextInput input {
        background-color: #0d272e !important;
        color: #ffffff !important;

        border: 1px solid #28505a !important;
        border-radius: 10px !important;

        min-height: 42px;
    }

    .stTextInput input::placeholder {
        color: #78939a !important;
    }

    .stTextInput input:focus {
        border-color: #2dd4bf !important;

        box-shadow:
            0 0 0 3px rgba(45, 212, 191, 0.12) !important;
    }


    /* ========================================================
       SELECT BOX
       ======================================================== */

    div[data-baseweb="select"] > div {
        background-color: #0d272e !important;

        border: 1px solid #28505a !important;

        border-radius: 10px !important;

        color: #ffffff !important;
    }

    div[data-baseweb="select"] span {
        color: #ffffff !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        background-color: #12343b !important;

        color: #ffffff !important;

        border: 1px solid #28545c !important;

        border-radius: 10px !important;

        min-height: 42px;

        font-weight: 600;

        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        background-color: #18464e !important;

        border-color: #2dd4bf !important;

        color: #ffffff !important;

        transform: translateY(-1px);
    }


    /* ========================================================
       PRIMARY BUTTONS
       ======================================================== */

    .stButton > button[kind="primary"] {
        background-color: #149b9b !important;

        border-color: #149b9b !important;

        color: #ffffff !important;

        font-weight: 700;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #0f8585 !important;

        border-color: #2dd4bf !important;

        color: #ffffff !important;
    }


    /* ========================================================
       HISTORY CARDS
       ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #0b252c !important;

        border: 1px solid #24474f !important;

        border-radius: 16px !important;

        box-shadow:
            0 5px 18px rgba(0, 0, 0, 0.22);
    }


    /* ========================================================
       FASTEST PILL
       ======================================================== */

    .fastest-pill {
        background-color: #3a2d16;

        color: #f5c66d;

        padding: 5px 10px;

        border-radius: 20px;

        font-size: 12px;

        font-weight: 700;

        border: 1px solid #5b451f;
    }


    /* ========================================================
       AI RECOMMENDED PILL
       ======================================================== */

    .ai-pill {
        background-color: #103b3b;

        color: #54ddd0;

        padding: 5px 10px;

        border-radius: 20px;

        font-size: 12px;

        font-weight: 700;

        border: 1px solid #1e6262;
    }


    /* ========================================================
       COOLEST PILL
       ======================================================== */

    .coolest-pill {
        background-color: #172746;

        color: #9eb5ff;

        padding: 5px 10px;

        border-radius: 20px;

        font-size: 12px;

        font-weight: 700;

        border: 1px solid #2a4370;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border-color: #23434b !important;
    }


    /* ========================================================
       INFO BOX
       ======================================================== */

    div[data-testid="stAlert"] {
        background-color: #0d3035 !important;

        border: 1px solid #22545a !important;

        color: #d7eeee !important;

        border-radius: 12px !important;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 700px) {

        .block-container {
            padding-left: 14px !important;
            padding-right: 14px !important;
        }

        .brand-text {
            font-size: 17px;
        }

        .brand-mark {
            font-size: 20px;
        }

        .history-icon-box {
            width: 52px;
            height: 52px;
            font-size: 24px;
        }

        .stButton > button {
            min-height: 42px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HISTORY STORAGE
# ============================================================

def load_history():

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


def save_history(history):

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


def delete_history_item(index):

    history = load_history()

    if 0 <= index < len(history):

        history.pop(index)

        save_history(
            history
        )


def clear_history():

    save_history([])


# ============================================================
# NAVBAR
# ============================================================

nav_brand, nav_plan, nav_saved, nav_history, nav_profile = st.columns(
    [3, 1.2, 1.4, 1.1, 1]
)


with nav_brand:

    st.markdown(
        """
        <div class="brand-text">
            <span class="brand-mark">✦</span>
            UrbanBreeze
        </div>
        """,
        unsafe_allow_html=True
    )


with nav_plan:

    st.page_link(
        "pages/1_Plan_Route.py",
        label="Plan Route"
    )


with nav_saved:

    st.page_link(
        "pages/3_Saved_Places.py",
        label="Saved Places"
    )


with nav_history:

    st.page_link(
        "pages/4_Route_History.py",
        label="History"
    )


with nav_profile:

    st.page_link(
        "pages/5_Profile.py",
        label="Profile"
    )


st.markdown(
    '<div class="nav-line"></div>',
    unsafe_allow_html=True
)


# ============================================================
# PAGE HEADER
# ============================================================

header_icon, header_text = st.columns(
    [0.6, 6]
)


with header_icon:

    st.markdown(
        '<div class="history-icon-box">↺</div>',
        unsafe_allow_html=True
    )


with header_text:

    st.title(
        "Route History"
    )

    st.caption(
        "View your previous routes and quickly plan them again."
    )


# ============================================================
# LOAD HISTORY
# ============================================================

history = load_history()


# ============================================================
# SEARCH + FILTER
# ============================================================

search_col, filter_col = st.columns(
    [3, 1.3]
)


with search_col:

    search_history = st.text_input(
        "Search history",
        placeholder="Search places or routes...",
        label_visibility="collapsed"
    )


with filter_col:

    route_filter = st.selectbox(
        "Route type",
        [
            "All routes",
            "Fastest",
            "AI Recommended",
            "Coolest"
        ],
        label_visibility="collapsed"
    )


# ============================================================
# FILTER HISTORY
# ============================================================

filtered_history = []


for index, item in enumerate(history):

    start = str(
        item.get(
            "start",
            item.get(
                "origin",
                "Starting point"
            )
        )
    )

    destination = str(
        item.get(
            "destination",
            item.get(
                "end",
                "Destination"
            )
        )
    )

    route_type = str(
        item.get(
            "route_type",
            item.get(
                "type",
                item.get(
                    "label",
                    "AI Recommended"
                )
            )
        )
    )

    searchable_text = (
        start
        + " "
        + destination
        + " "
        + route_type
    ).lower()


    if search_history:

        if search_history.lower() not in searchable_text:
            continue


    route_type_lower = route_type.lower()


    if route_filter == "Fastest":

        if "fast" not in route_type_lower:
            continue


    elif route_filter == "AI Recommended":

        if (
            "ai" not in route_type_lower
            and "recommend" not in route_type_lower
        ):
            continue


    elif route_filter == "Coolest":

        if "cool" not in route_type_lower:
            continue


    filtered_history.append(
        (
            index,
            item
        )
    )


# ============================================================
# SECTION HEADER
# ============================================================

header_left, header_right = st.columns(
    [3, 1]
)


with header_left:

    st.subheader(
        f"Previous routes · {len(history)}"
    )

    st.caption(
        "Your recent climate-aware route searches."
    )


with header_right:

    if history:

        if st.button(
            "Clear History",
            use_container_width=True
        ):

            clear_history()

            st.rerun()


# ============================================================
# EMPTY HISTORY
# ============================================================

if not history:

    with st.container(
        border=True
    ):

        st.markdown(
            "### No route history yet"
        )

        st.caption(
            "Routes you plan will appear here automatically."
        )

        if st.button(
            "Plan a route",
            type="primary"
        ):

            st.switch_page(
                "pages/1_Plan_Route.py"
            )


# ============================================================
# NO SEARCH RESULTS
# ============================================================

elif not filtered_history:

    with st.container(
        border=True
    ):

        st.markdown(
            "### No matching routes"
        )

        st.caption(
            "Try changing your search or route filter."
        )


# ============================================================
# ROUTE HISTORY CARDS
# ============================================================

else:

    for original_index, item in filtered_history:

        # ----------------------------------------------------
        # Basic information
        # ----------------------------------------------------

        start = item.get(
            "start",
            item.get(
                "origin",
                "Starting point"
            )
        )

        destination = item.get(
            "destination",
            item.get(
                "end",
                "Destination"
            )
        )

        route_type = item.get(
            "route_type",
            item.get(
                "type",
                item.get(
                    "label",
                    "AI Recommended"
                )
            )
        )

        duration = item.get(
            "duration",
            item.get(
                "duration_minutes",
                "--"
            )
        )

        distance = item.get(
            "distance",
            item.get(
                "distance_km",
                "--"
            )
        )

        temperature = item.get(
            "average_temperature",
            item.get(
                "temperature",
                "--"
            )
        )

        cool_score = item.get(
            "cool_score",
            item.get(
                "climate_score",
                "--"
            )
        )

        travel_mode = item.get(
            "travel_mode",
            item.get(
                "mode",
                ""
            )
        )

        date = item.get(
            "date",
            item.get(
                "timestamp",
                item.get(
                    "created_at",
                    ""
                )
            )
        )


        # ----------------------------------------------------
        # Determine route label
        # ----------------------------------------------------

        route_lower = str(
            route_type
        ).lower()


        if "fast" in route_lower:

            route_label = "Fastest"

            pill_class = "fastest-pill"


        elif "cool" in route_lower:

            route_label = "Coolest"

            pill_class = "coolest-pill"


        else:

            route_label = "AI Recommended"

            pill_class = "ai-pill"


        # ----------------------------------------------------
        # Card
        # ----------------------------------------------------

        with st.container(
            border=True
        ):

            top_left, top_right = st.columns(
                [5, 1]
            )


            with top_left:

                st.markdown(
                    f'<span class="{pill_class}">'
                    f'{route_label}'
                    f'</span>',
                    unsafe_allow_html=True
                )


            with top_right:

                if st.button(
                    "Delete",
                    key=f"delete_history_{original_index}",
                    use_container_width=True
                ):

                    delete_history_item(
                        original_index
                    )

                    st.rerun()


            st.markdown(
                f"### {start} → {destination}"
            )


            route_details = []


            if travel_mode:

                route_details.append(
                    str(travel_mode)
                )


            if date:

                route_details.append(
                    str(date)
                )


            if route_details:

                st.caption(
                    " · ".join(route_details)
                )


            # ------------------------------------------------
            # STATS
            # ------------------------------------------------

            stat1, stat2, stat3, stat4 = st.columns(
                4
            )


            with stat1:

                st.caption(
                    "Duration"
                )

                if duration != "--":

                    st.write(
                        f"**{duration} min**"
                    )

                else:

                    st.write(
                        "**—**"
                    )


            with stat2:

                st.caption(
                    "Distance"
                )

                if distance != "--":

                    st.write(
                        f"**{distance} km**"
                    )

                else:

                    st.write(
                        "**—**"
                    )


            with stat3:

                st.caption(
                    "Temperature"
                )

                if temperature != "--":

                    st.write(
                        f"**{temperature}°C**"
                    )

                else:

                    st.write(
                        "**—**"
                    )


            with stat4:

                st.caption(
                    "Cool Score"
                )

                if cool_score != "--":

                    st.write(
                        f"**{cool_score}/100**"
                    )

                else:

                    st.write(
                        "**—**"
                    )


            # ------------------------------------------------
            # USE AGAIN
            # ------------------------------------------------

            if st.button(
                "Use this route again",
                key=f"reuse_history_{original_index}",
                use_container_width=True
            ):

                st.session_state[
                    "history_route"
                ] = item

                st.switch_page(
                    "pages/1_Plan_Route.py"
                )


# ============================================================
# TIP
# ============================================================

st.info(
    "Tip: Your route history makes it easy to revisit "
    "previous journeys and compare climate-aware choices."
)
