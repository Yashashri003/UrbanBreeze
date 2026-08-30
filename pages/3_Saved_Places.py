import streamlit as st
import json
import os
import folium

from streamlit_folium import st_folium
from utils.routing import search_california_locations


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Saved Places | UrbanBreeze",
    page_icon="📍",
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

SAVED_PLACES_FILE = os.path.join(
    DATA_DIR,
    "saved_places.json"
)


# ============================================================
# DARK URBANBREEZE UI
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background-color: #07191f;
        color: #ffffff;
    }

    .block-container {
        max-width: 1240px;
        padding-top: 5rem;
        padding-bottom: 3rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    * {
        box-sizing: border-box;
    }


    /* ========================================================
       NAVBAR
       ======================================================== */

    .ub-navbar {
        width: 100%;
        min-height: 62px;

        display: flex;
        align-items: center;

        border-bottom: 1px solid #24434b;

        margin-bottom: 28px;
    }

    .brand {
        font-size: 21px;
        font-weight: 750;
        color: #ffffff;
        white-space: nowrap;
    }

    .brand-mark {
        color: #21c7c2;
        font-size: 22px;
        margin-right: 5px;
    }


    /* ========================================================
       NAVIGATION LINKS
       ======================================================== */

    .nav-link {
        color: #d8e7e9 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        text-decoration: none !important;
        white-space: nowrap !important;
    }

    .nav-link:hover {
        color: #21c7c2 !important;
    }


    /* ========================================================
       HEADINGS
       ======================================================== */

    h1 {
        color: #ffffff !important;
        font-weight: 750 !important;
        letter-spacing: -1px;
    }

    h2,
    h3,
    h4 {
        color: #ffffff !important;
    }

    p,
    label,
    .stMarkdown {
        color: #e3eef0;
    }

    .stCaption,
    [data-testid="stCaptionContainer"] {
        color: #9eb4ba !important;
    }


    /* ========================================================
       HERO ICON
       ======================================================== */

    .hero-icon-box {
        width: 58px;
        height: 58px;

        background-color: #10343c;

        border: 1px solid #1d5b63;

        border-radius: 15px;

        display: flex;
        align-items: center;
        justify-content: center;

        color: #21c7c2;

        font-size: 28px;
        font-weight: 400;

        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.20);
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    .stTextInput input {
        background-color: #10262d !important;
        color: #ffffff !important;

        border-radius: 10px !important;
        border: 1px solid #31515a !important;

        min-height: 42px;
    }

    .stTextInput input::placeholder {
        color: #829ba2 !important;
    }

    .stTextInput input:focus {
        border-color: #21c7c2 !important;

        box-shadow:
            0 0 0 3px rgba(33, 199, 194, 0.14) !important;
    }


    /* ========================================================
       SELECTBOX
       ======================================================== */

    div[data-baseweb="select"] > div {
        background-color: #10262d !important;
        border-color: #31515a !important;
        color: #ffffff !important;
    }

    div[data-baseweb="select"] span {
        color: #ffffff !important;
    }


    /* ========================================================
       RADIO BUTTONS
       ======================================================== */

    div[data-testid="stRadio"] label {
        color: #dcebed !important;
    }

    div[data-testid="stRadio"] label p {
        color: #dcebed !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 10px !important;

        min-height: 42px;

        font-weight: 600;

        white-space: nowrap;

        background-color: #12343c !important;
        color: #ffffff !important;

        border: 1px solid #31545d !important;

        transition: 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);

        background-color: #17464f !important;

        border-color: #21c7c2 !important;

        color: #ffffff !important;
    }


    /* ========================================================
       PRIMARY BUTTONS
       ======================================================== */

    .stButton > button[kind="primary"] {
        background-color: #159b9b !important;
        border-color: #159b9b !important;
        color: #ffffff !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #20b8b3 !important;
        border-color: #20b8b3 !important;
        color: #ffffff !important;
    }


    /* ========================================================
       USE IN ROUTE BUTTON
       ======================================================== */

    div[class*="st-key-use_wrap"] .stButton > button {
        background-color: #159b9b !important;
        border-color: #159b9b !important;
        color: #ffffff !important;
    }

    div[class*="st-key-use_wrap"] .stButton > button:hover {
        background-color: #20b8b3 !important;
        border-color: #20b8b3 !important;
    }


    /* ========================================================
       DELETE BUTTON
       ======================================================== */

    div[class*="st-key-delete_wrap"] .stButton > button {
        width: 44px !important;
        min-width: 44px !important;
        max-width: 44px !important;

        height: 44px !important;
        min-height: 44px !important;

        padding: 0 !important;

        border-radius: 10px !important;

        background-color: #10262d !important;

        border: 1px solid #31515a !important;

        color: #a9bcc1 !important;

        font-size: 22px !important;
        font-weight: 400 !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div[class*="st-key-delete_wrap"] .stButton > button:hover {
        background-color: #3a2022 !important;
        border-color: #a85d5d !important;
        color: #ff8d8d !important;
    }


    /* ========================================================
       ACTION ROW
       ======================================================== */

    div[class*="st-key-actions_row"] {
        width: 100%;
    }

    div[class*="st-key-actions_row"]
    > div[data-testid="stHorizontalBlock"] {

        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;

        gap: 8px !important;

        width: 100% !important;
    }

    div[class*="st-key-actions_row"]
    > div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"]:first-child {

        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    div[class*="st-key-actions_row"]
    > div[data-testid="stHorizontalBlock"]
    > div[data-testid="column"]:last-child {

        flex: 0 0 44px !important;
        width: 44px !important;
        min-width: 44px !important;
    }


    /* ========================================================
       CARDS / CONTAINERS
       ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {

        background-color: #0d252c !important;

        border-radius: 16px !important;

        border: 1px solid #294951 !important;

        box-shadow:
            0 5px 20px rgba(0, 0, 0, 0.18);
    }


    /* ========================================================
       PLACE ICON
       ======================================================== */

    .place-icon {
        width: 48px;
        height: 48px;

        background-color: #103a42;

        border: 1px solid #205c64;

        border-radius: 13px;

        display: flex;
        align-items: center;
        justify-content: center;

        color: #21c7c2;

        font-size: 21px;

        margin-bottom: 12px;
    }


    /* ========================================================
       PLACE NAME
       ======================================================== */

    .place-name {
        color: #ffffff;

        font-size: 18px;

        font-weight: 700;

        line-height: 1.3;

        margin-bottom: 5px;

        word-break: break-word;
    }


    /* ========================================================
       PLACE ADDRESS
       ======================================================== */

    .place-address {
        color: #9eb4ba;

        font-size: 13px;

        line-height: 1.5;

        min-height: 40px;

        word-break: break-word;
    }


    /* ========================================================
       CATEGORY PILL
       ======================================================== */

    .category-pill {
        display: inline-block;

        margin-top: 9px;

        padding: 4px 10px;

        border-radius: 20px;

        background-color: #123e45;

        border: 1px solid #1c666b;

        color: #67d9d4;

        font-size: 11px;

        font-weight: 700;
    }


    /* ========================================================
       CONFIRM DELETE
       ======================================================== */

    .confirm-text {
        font-size: 13px;

        color: #ffaaaa;

        background-color: #382326;

        border: 1px solid #704447;

        border-radius: 10px;

        padding: 9px 11px;

        margin-bottom: 8px;
    }


    /* ========================================================
       TIP
       ======================================================== */

    .tip-box {
        background-color: #0d3036;

        border: 1px solid #20565b;

        border-radius: 14px;

        padding: 15px 18px;

        color: #b7cccf;

        font-size: 13px;

        margin-top: 28px;
    }

    .tip-box strong {
        color: #ffffff;
    }


    /* ========================================================
       SUCCESS / INFO / WARNING
       ======================================================== */

    div[data-testid="stAlert"] {
        background-color: #102d34 !important;
        border: 1px solid #28535b !important;
        color: #e8f5f6 !important;
    }

    div[data-testid="stAlert"] p {
        color: #e8f5f6 !important;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border-color: #29464e !important;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 700px) {

        .block-container {
            padding-left: 14px !important;
            padding-right: 14px !important;
            padding-top: 0.3rem !important;
        }

        .brand {
            font-size: 18px;
        }

        .brand-mark {
            font-size: 20px;
        }

        .hero-icon-box {
            width: 50px;
            height: 50px;
            font-size: 24px;
        }

        div[data-testid="stHorizontalBlock"]:has(.place-card-row) {
            flex-wrap: nowrap !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.place-card-row)
        > div[data-testid="column"] {

            flex: 1 1 0 !important;
            min-width: 0 !important;
        }

        .place-name {
            font-size: 16px;
        }

        .place-address {
            font-size: 12px;
        }

        div[class*="st-key-actions_row"]
        > div[data-testid="stHorizontalBlock"] {

            flex-direction: row !important;
            flex-wrap: nowrap !important;
        }

        div[class*="st-key-actions_row"]
        > div[data-testid="stHorizontalBlock"]
        > div[data-testid="column"]:last-child {

            flex: 0 0 44px !important;
            width: 44px !important;
            min-width: 44px !important;
        }

        div[class*="st-key-delete_wrap"] .stButton > button {

            width: 44px !important;
            min-width: 44px !important;
            max-width: 44px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# STORAGE
# ============================================================

def load_saved_places():

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    if not os.path.exists(
        SAVED_PLACES_FILE
    ):
        return []

    try:

        with open(
            SAVED_PLACES_FILE,
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
        pass

    return []


def save_saved_places(places):

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    with open(
        SAVED_PLACES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            places,
            file,
            indent=2,
            ensure_ascii=False
        )


def add_saved_place(place):

    places = load_saved_places()

    for existing in places:

        if (
            existing.get("name", "")
            .strip()
            .lower()
            ==
            place["name"]
            .strip()
            .lower()
        ):

            return False

    places.append(place)

    save_saved_places(
        places
    )

    return True


def delete_saved_place(name):

    places = load_saved_places()

    places = [
        place
        for place in places
        if place.get("name") != name
    ]

    save_saved_places(
        places
    )


# ============================================================
# RESET NEW PLACE
# ============================================================

def start_new_place():

    st.session_state.selected_lat = None
    st.session_state.selected_lon = None
    st.session_state.selected_address = ""

    st.session_state.search_results = []

    st.session_state.form_reset_counter += 1


# ============================================================
# SESSION STATE
# ============================================================

if "selected_lat" not in st.session_state:
    st.session_state.selected_lat = None

if "selected_lon" not in st.session_state:
    st.session_state.selected_lon = None

if "selected_address" not in st.session_state:
    st.session_state.selected_address = ""

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "form_reset_counter" not in st.session_state:
    st.session_state.form_reset_counter = 0


# ============================================================
# TOP NAVBAR
# ============================================================

nav_brand, nav_plan, nav_saved, nav_history, nav_profile = st.columns(
    [2.6, 1.15, 1.35, 0.9, 0.65],
    gap="small"
)


with nav_brand:

    st.markdown(
        """
        <div class="brand">
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



# ============================================================
# PAGE HEADER
# ============================================================

hero_col, hero_button = st.columns(
    [5, 1]
)

with hero_col:

    st.title(
        "Saved Places"
    )

    st.caption(
        "Save your favourite locations and access them "
        "quickly when planning your next route."
    )


with hero_button:

    st.write("")

    if st.button(
        "+  Add New Place",
        type="primary",
        use_container_width=True
    ):

        start_new_place()

        st.rerun()


# ============================================================
# ADD PLACE
# ============================================================

st.markdown("### Add a new place")

st.caption(
    "Search for a location or drop a pin directly on the map."
)


# ============================================================
# NAME + CATEGORY
# ============================================================

name_col, category_col = st.columns(
    [3, 1]
)


with name_col:

    place_name = st.text_input(
        "Place name",
        placeholder="Home, College, Office...",
        key=f"place_name_{st.session_state.form_reset_counter}"
    )


with category_col:

    category = st.selectbox(
        "Category",
        [
            "Home",
            "Education",
            "Work",
            "Shopping",
            "Other"
        ]
    )


# ============================================================
# LOCATION METHOD
# ============================================================

method = st.radio(
    "Choose location method",
    [
        "Search location",
        "Pin on map"
    ],
    horizontal=True
)


# ============================================================
# SEARCH LOCATION
# ============================================================

if method == "Search location":

    search_col, button_col = st.columns(
        [6, 1]
    )

    with search_col:

        search_query = st.text_input(
            "Search",
            placeholder=(
                "Search places, addresses or landmarks in California..."
            ),
            label_visibility="collapsed",
            key=f"search_query_{st.session_state.form_reset_counter}"
        )

    with button_col:

        search_clicked = st.button(
            "Search",
            type="primary",
            use_container_width=True
        )

    if search_clicked:

        if len(
            search_query.strip()
        ) < 3:

            st.warning(
                "Enter at least 3 characters."
            )

        else:

            with st.spinner(
                "Finding your location..."
            ):

                try:

                    results = search_california_locations(
                        search_query
                    )

                except Exception as error:

                    st.error(
                        f"Location search failed: {error}"
                    )

                    results = []

            st.session_state.search_results = (
                results or []
            )


    results = st.session_state.search_results


    # ========================================================
    # SEARCH RESULTS
    # ========================================================

    if results:

        location_names = [
            result["display_name"]
            for result in results
        ]

        selected_location = st.selectbox(
            "Select location",
            location_names
        )

        selected_index = location_names.index(
            selected_location
        )

        selected_result = results[
            selected_index
        ]

        st.session_state.selected_lat = float(
            selected_result["lat"]
        )

        st.session_state.selected_lon = float(
            selected_result["lon"]
        )

        st.session_state.selected_address = (
            selected_result["display_name"]
        )


        # ====================================================
        # MAP
        # ====================================================

        selected_map = folium.Map(
            location=[
                selected_result["lat"],
                selected_result["lon"]
            ],
            zoom_start=15,
            control_scale=True
        )

        folium.Marker(
            [
                selected_result["lat"],
                selected_result["lon"]
            ],
            tooltip="Selected location"
        ).add_to(
            selected_map
        )

        st_folium(
            selected_map,
            width="100%",
            height=420,
            returned_objects=[]
        )


# ============================================================
# PIN ON MAP
# ============================================================

else:

    st.info(
        "Click anywhere on the map to choose your location."
    )

    map_lat = (
        st.session_state.selected_lat
        if st.session_state.selected_lat is not None
        else 37.7749
    )

    map_lon = (
        st.session_state.selected_lon
        if st.session_state.selected_lon is not None
        else -122.4194
    )

    pin_map = folium.Map(
        location=[
            map_lat,
            map_lon
        ],
        zoom_start=11,
        control_scale=True
    )

    if (
        st.session_state.selected_lat is not None
        and st.session_state.selected_lon is not None
    ):

        folium.Marker(
            [
                st.session_state.selected_lat,
                st.session_state.selected_lon
            ],
            tooltip="Selected location"
        ).add_to(
            pin_map
        )

    map_data = st_folium(
        pin_map,
        width="100%",
        height=430,
        returned_objects=[
            "last_clicked"
        ]
    )


    # ========================================================
    # MAP CLICK
    # ========================================================

    if map_data:

        clicked = map_data.get(
            "last_clicked"
        )

        if clicked:

            lat = clicked.get(
                "lat"
            )

            lon = clicked.get(
                "lng"
            )

            if (
                lat is not None
                and lon is not None
            ):

                st.session_state.selected_lat = float(
                    lat
                )

                st.session_state.selected_lon = float(
                    lon
                )

                st.session_state.selected_address = (
                    "Pinned location"
                )

                st.rerun()


# ============================================================
# SELECTED LOCATION
# ============================================================

if (
    st.session_state.selected_lat is not None
    and st.session_state.selected_lon is not None
):

    st.success(
        "Location selected"
    )

    st.caption(
        st.session_state.selected_address
    )


# ============================================================
# SAVE PLACE
# ============================================================

if (
    st.session_state.selected_lat is not None
    and st.session_state.selected_lon is not None
):

    if st.button(
        "Save place",
        type="primary",
        use_container_width=True
    ):

        if not place_name.strip():

            st.warning(
                "Please enter a name for this place."
            )

        else:

            new_place = {

                "name":
                    place_name.strip(),

                "display_name":
                    st.session_state.selected_address,

                "lat":
                    float(
                        st.session_state.selected_lat
                    ),

                "lon":
                    float(
                        st.session_state.selected_lon
                    ),

                "category":
                    category
            }

            if add_saved_place(
                new_place
            ):

                st.success(
                    f"{place_name} saved successfully."
                )

                st.session_state.selected_lat = None
                st.session_state.selected_lon = None
                st.session_state.selected_address = ""
                st.session_state.search_results = []

                st.session_state.form_reset_counter += 1

                st.rerun()

            else:

                st.warning(
                    "A place with this name already exists."
                )


# ============================================================
# YOUR PLACES
# ============================================================

st.markdown("---")

places = load_saved_places()


header_col, search_col = st.columns(
    [3, 2]
)


with header_col:

    st.markdown(
        f"### Your Places · {len(places)}"
    )

    st.caption(
        "Your frequently used destinations, ready when you are."
    )


with search_col:

    place_filter = st.text_input(
        "Search saved places",
        placeholder="Search your places...",
        label_visibility="collapsed"
    )


# ============================================================
# FILTER
# ============================================================

if place_filter:

    filtered_places = [

        place

        for place in places

        if (
            place_filter.lower()
            in place.get(
                "name",
                ""
            ).lower()
        )

        or (

            place_filter.lower()
            in place.get(
                "display_name",
                ""
            ).lower()
        )
    ]

else:

    filtered_places = places


# ============================================================
# EMPTY STATE
# ============================================================

if not filtered_places:

    with st.container(
        border=True
    ):

        st.markdown(
            "### No saved places yet"
        )

        st.caption(
            "Add Home, College, Office or another place "
            "you visit often."
        )


# ============================================================
# SAVED PLACE CARDS
# ============================================================

else:

    # TWO CARDS PER ROW
    for start in range(
        0,
        len(filtered_places),
        2
    ):

        row_places = filtered_places[
            start:start + 2
        ]

        columns = st.columns(
            len(row_places),
            gap="medium"
        )

        for index, (column, place) in enumerate(
            zip(
                columns,
                row_places
            )
        ):

            with column:

                # Hidden marker used by mobile CSS
                st.markdown(
                    '<span class="place-card-row"></span>',
                    unsafe_allow_html=True
                )

                with st.container(
                    border=True
                ):

                    place_key = (
                        f"{start}_{index}_"
                        f"{place.get('name', '')}"
                    )

                    confirm_state_key = (
                        f"confirm_delete_{place_key}"
                    )

                    if confirm_state_key not in st.session_state:

                        st.session_state[
                            confirm_state_key
                        ] = False


                    # ====================================================
                    # PLACE ICON
                    # ====================================================

                    category_icons = {

                        "Home": "⌂",

                        "Education": "◇",

                        "Work": "▣",

                        "Shopping": "□",

                        "Other": "●"
                    }

                    icon = category_icons.get(
                        place.get(
                            "category",
                            "Other"
                        ),
                        "●"
                    )

                    st.markdown(
                        f"""
                        <div class="place-icon">
                            {icon}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    # ====================================================
                    # PLACE NAME
                    # ====================================================

                    st.markdown(
                        f"""
                        <div class="place-name">
                            {place.get("name", "Unnamed")}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    # ====================================================
                    # ADDRESS
                    # ====================================================

                    st.markdown(
                        f"""
                        <div class="place-address">
                            {place.get(
                                "display_name",
                                "Saved location"
                            )}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    # ====================================================
                    # CATEGORY
                    # ====================================================

                    st.markdown(
                        f"""
                        <span class="category-pill">
                            {place.get("category", "Other")}
                        </span>
                        """,
                        unsafe_allow_html=True
                    )

                    st.write("")


                    # ====================================================
                    # DELETE CONFIRMATION
                    # ====================================================

                    with st.container(
                        key=f"actions_row_{place_key}"
                    ):

                        if st.session_state[
                            confirm_state_key
                        ]:

                            st.markdown(
                                f"""
                                <div class="confirm-text">
                                    Delete "{place.get("name", "this place")}"?
                                    This cannot be undone.
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            yes_col, no_col = st.columns(
                                [1, 1],
                                gap="small"
                            )

                            with yes_col:

                                if st.button(
                                    "Delete",
                                    key=f"yes_{place_key}",
                                    use_container_width=True
                                ):

                                    delete_saved_place(
                                        place.get("name")
                                    )

                                    st.session_state[
                                        confirm_state_key
                                    ] = False

                                    st.rerun()

                            with no_col:

                                if st.button(
                                    "Cancel",
                                    key=f"no_{place_key}",
                                    use_container_width=True
                                ):

                                    st.session_state[
                                        confirm_state_key
                                    ] = False

                                    st.rerun()

                        else:

                            # =================================================
                            # USE + DELETE
                            # =================================================

                            use_col, delete_col = st.columns(
                                [1, 0.18],
                                gap="small"
                            )


                            # -------------------------------------------------
                            # USE IN ROUTE
                            # -------------------------------------------------

                            with use_col:

                                with st.container(
                                    key=f"use_wrap_{place_key}"
                                ):

                                    if st.button(
                                        "Use in Route",
                                        key=f"use_{place_key}",
                                        use_container_width=True
                                    ):

                                        st.session_state[
                                            "saved_route_place"
                                        ] = place

                                        st.session_state[
                                            "saved_place_name"
                                        ] = place.get(
                                            "name",
                                            ""
                                        )

                                        st.session_state[
                                            "saved_place_address"
                                        ] = place.get(
                                            "display_name",
                                            ""
                                        )

                                        st.session_state[
                                            "saved_place_lat"
                                        ] = place.get(
                                            "lat"
                                        )

                                        st.session_state[
                                            "saved_place_lon"
                                        ] = place.get(
                                            "lon"
                                        )

                                        st.switch_page(
                                            "pages/1_Plan_Route.py"
                                        )


                            # -------------------------------------------------
                            # DELETE
                            # -------------------------------------------------

                            with delete_col:

                                with st.container(
                                    key=f"delete_wrap_{place_key}"
                                ):

                                    if st.button(
                                        "×",
                                        key=f"delete_{place_key}",
                                        help="Delete this saved place"
                                    ):

                                        st.session_state[
                                            confirm_state_key
                                        ] = True

                                        st.rerun()


# ============================================================
# TIP
# ============================================================

st.markdown(
    """
    <div class="tip-box">
        <strong>Tip:</strong>
        Save places you visit often to plan routes faster
        and get better climate-aware recommendations.
    </div>
    """,
    unsafe_allow_html=True
)
