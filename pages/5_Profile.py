import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="UrbanBreeze - Profile",
    page_icon="👤",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "profile_name": "Your Name",
    "profile_username": "urbanbreeze_user",
    "profile_email": "you@example.com",

    "coolness_preference": 55,
    "max_extra_time": 10,
    "heat_priority": "High",
    "default_travel_mode": "🚶 Walk",

    "saved_home": "",
    "saved_work": "",
    "saved_other": "",

    "profile_photo": None,
    "show_edit_profile": False,
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       MAIN PAGE
       ======================================================== */

    .stApp {
        background-color: #061f24;
    }

      

    .block-container {
        max-width: 1150px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
        padding-left: 5%;
        padding-right: 5%;
    }


    /* ========================================================
       TEXT
       ======================================================== */

    h1, h2, h3 {
        color: #f5ffff !important;
    }

    p {
        color: #e2f0f1;
    }

    .page-subtitle {
        color: #9eb9bd !important;
        font-size: 16px;
        margin-top: -10px;
        margin-bottom: 28px;
    }


    /* ========================================================
       PROFILE INFORMATION
       ======================================================== */

    .profile-name {
        color: #ffffff !important;
        font-size: 30px;
        font-weight: 700;
        margin-top: 8px;
    }

    .profile-username {
        color: #65c6c5 !important;
        font-size: 16px;
        margin-top: 5px;
    }

    .profile-email {
        color: #a9c1c5 !important;
        font-size: 15px;
        margin-top: 6px;
    }


    /* ========================================================
       AVATAR
       ======================================================== */

    .avatar {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        background-color: #159c9c;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
    }


    /* ========================================================
       STREAMLIT BORDERED CONTAINERS
       ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #092b31 !important;
        border: 1px solid #31555b !important;
        border-radius: 18px !important;
        padding: 12px !important;
    }


    /* ========================================================
       SECTION TEXT
       ======================================================== */

    .section-title {
        color: #ffffff !important;
        font-size: 19px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .section-description {
        color: #98b2b6 !important;
        font-size: 14px;
        margin-bottom: 18px;
    }


    /* ========================================================
       INPUT LABELS
       ======================================================== */

    .stTextInput label,
    .stSelectbox label,
    .stSlider label,
    .stFileUploader label {
        color: #e5f2f3 !important;
        font-weight: 600 !important;
    }


    /* ========================================================
       TEXT INPUTS
       ======================================================== */

    .stTextInput input {
        background-color: #ffffff !important;
        color: #111111 !important;
        border: 1px solid #8aa5aa !important;
        border-radius: 10px !important;
        font-size: 15px !important;
    }

    .stTextInput input::placeholder {
        color: #555555 !important;
        opacity: 1 !important;
    }

    .stTextInput input:focus {
        color: #111111 !important;
        background-color: #ffffff !important;
        border-color: #159c9c !important;
    }


    /* ========================================================
       SELECT BOXES
       ======================================================== */

    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #111111 !important;
        border: 1px solid #8aa5aa !important;
        border-radius: 10px !important;
    }

    .stSelectbox div[data-baseweb="select"] span {
        color: #111111 !important;
    }

    .stSelectbox input {
        color: #111111 !important;
    }

    .stSelectbox svg {
        fill: #333333 !important;
    }


    /* ========================================================
       SLIDERS
       ======================================================== */

    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"] {
        color: #9eb8bc !important;
    }

    .stSlider [data-testid="stThumbValue"] {
        color: #ffffff !important;
    }

    .stSlider div {
        color: #e5f2f3;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {
        background-color: #ffffff !important;
        border: 1px dashed #8aa5aa !important;
        border-radius: 12px !important;
        padding: 10px !important;
    }

    [data-testid="stFileUploader"] section {
        background-color: transparent !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: #ffffff !important;
        border: 1px dashed #8aa5aa !important;
        border-radius: 12px !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #333333 !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] div {
        color: #333333 !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] span {
        color: #555555 !important;
    }

    [data-testid="stFileUploader"] small {
        color: #555555 !important;
    }


        /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 11px !important;
        min-height: 45px !important;
        font-weight: 650 !important;
        background-color: #159c9c !important;
        color: #ffffff !important;
        border: 1px solid #159c9c !important;
    }

    .stButton > button p {
        color: #ffffff !important;
    }

    .stButton > button span {
        color: #ffffff !important;
    }

    .stButton > button:hover {
        background-color: #0f8585 !important;
        color: #ffffff !important;
        border-color: #0f8585 !important;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {
        background-color: #061f24 !important;
    }

    [data-testid="stSidebar"] * {
        color: #e2f0f1 !important;
    }

    [data-testid="stSidebarNav"] a {
        color: #e2f0f1 !important;
        background-color: transparent !important;
    }

    [data-testid="stSidebarNav"] a span {
        color: #e2f0f1 !important;
    }

    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: #159c9c !important;
        border-radius: 8px !important;
    }

    [data-testid="stSidebarNav"] a[aria-current="page"] span {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* ========================================================
       SAVED PLACE TEXT
       ======================================================== */

    .place-title {
        color: #ffffff !important;
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .place-description {
        color: #94afb3 !important;
        font-size: 13px;
        margin-bottom: 14px;
    }


    /* ========================================================
       RECENT ROUTES
       ======================================================== */

    .route-title {
        color: #ffffff !important;
        font-size: 17px;
        font-weight: 700;
    }

    .route-info {
        color: #a9c1c5 !important;
        font-size: 14px;
    }

    .empty-title {
        color: #ffffff !important;
        font-size: 17px;
        font-weight: 650;
        margin-bottom: 5px;
    }

    .empty-description {
        color: #94afb3 !important;
        font-size: 14px;
    }


    /* ========================================================
       ACCOUNT
       ======================================================== */

    .account-description {
        color: #94afb3 !important;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("👤 Profile")

st.markdown(
    '<div class="page-subtitle">'
    "Manage your UrbanBreeze account and climate-aware travel preferences."
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# PROFILE SECTION
# ============================================================

profile_col1, profile_col2 = st.columns([1, 4])


with profile_col1:

    if st.session_state.profile_photo is not None:

        st.image(
            st.session_state.profile_photo,
            width=90
        )

    else:

        st.markdown(
            '<div class="avatar">👤</div>',
            unsafe_allow_html=True
        )


with profile_col2:

    st.markdown(
        f"""
        <div class="profile-name">
            {st.session_state.profile_name}
        </div>

        <div class="profile-username">
            @{st.session_state.profile_username}
        </div>

        <div class="profile-email">
            {st.session_state.profile_email}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PROFILE PHOTO
# ============================================================

with st.expander("📷 Change profile photo"):

    uploaded_photo = st.file_uploader(
        "Upload a profile photo",
        type=["png", "jpg", "jpeg"],
        help="Choose a JPG or PNG image."
    )

    if uploaded_photo is not None:

        st.session_state.profile_photo = uploaded_photo

        st.success("Profile photo selected.")

        st.rerun()


# ============================================================
# EDIT PROFILE
# ============================================================

if st.button(
    "✏️ Edit Profile",
    use_container_width=True
):

    st.session_state.show_edit_profile = (
        not st.session_state.show_edit_profile
    )


if st.session_state.show_edit_profile:

    with st.container(border=True):

        st.markdown("### ✏️ Edit Profile")

        with st.form("edit_profile_form"):

            name = st.text_input(
                "Name",
                value=st.session_state.profile_name
            )

            username = st.text_input(
                "Username",
                value=st.session_state.profile_username
            )

            email = st.text_input(
                "Email",
                value=st.session_state.profile_email
            )

            save = st.form_submit_button(
                "💾 Save Changes",
                use_container_width=True
            )

            if save:

                st.session_state.profile_name = name
                st.session_state.profile_username = username
                st.session_state.profile_email = email

                st.session_state.show_edit_profile = False

                st.success(
                    "Profile updated successfully."
                )

                st.rerun()


# ============================================================
# CLIMATE & ROUTE PREFERENCES
# ============================================================

st.markdown("## 🌡️ Climate & Route Preferences")


climate_col, route_col = st.columns(2)


# ============================================================
# CLIMATE COMFORT
# ============================================================

with climate_col:

    with st.container(border=True):

        st.markdown(
            '<div class="section-title">'
            "🌡️ Climate Comfort"
            "</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-description">'
            "Tell UrbanBreeze how strongly you prefer cooler routes."
            "</div>",
            unsafe_allow_html=True
        )

        coolness = st.slider(
            "Coolness Preference",
            min_value=0,
            max_value=100,
            value=st.session_state.coolness_preference,
            key="profile_coolness"
        )

        st.session_state.coolness_preference = coolness

        st.write(
            f"**Current preference: {coolness}/100**"
        )

        st.caption(
            "Higher preference = stronger priority for cooler routes."
        )

        max_time = st.slider(
            "Maximum Extra Travel Time",
            min_value=0,
            max_value=30,
            value=st.session_state.max_extra_time,
            step=5,
            key="profile_extra_time"
        )

        st.session_state.max_extra_time = max_time

        st.caption(
            f"Allow up to {max_time} additional minutes "
            "for a cooler route."
        )

        heat_priority = st.selectbox(
            "Heat Priority",
            ["Low", "Medium", "High"],
            index=[
                "Low",
                "Medium",
                "High"
            ].index(
                st.session_state.heat_priority
            ),
            key="profile_heat_priority"
        )

        st.session_state.heat_priority = heat_priority


# ============================================================
# ROUTE PREFERENCES
# ============================================================

with route_col:

    with st.container(border=True):

        st.markdown(
            '<div class="section-title">'
            "🗺️ Route Preferences"
            "</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-description">'
            "Choose how UrbanBreeze should plan your journeys."
            "</div>",
            unsafe_allow_html=True
        )

        travel_mode = st.selectbox(
            "Default Travel Mode",
            [
                "🚶 Walk",
                "🚴 Cycle",
                "🚗 EV"
            ],
            index=[
                "🚶 Walk",
                "🚴 Cycle",
                "🚗 EV"
            ].index(
                st.session_state.default_travel_mode
            ),
            key="profile_travel_mode"
        )

        st.session_state.default_travel_mode = travel_mode

        st.write(
            f"**Default travel mode:** {travel_mode}"
        )


# ============================================================
# SAVED PLACES
# ============================================================

st.markdown("## 📍 Saved Places")


place1, place2, place3 = st.columns(3)


# -------------------------
# HOME
# -------------------------

with place1:

    with st.container(border=True):

        st.markdown(
            '<div class="place-title">🏠 Home</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="place-description">'
            "Your saved home location"
            "</div>",
            unsafe_allow_html=True
        )

        home = st.text_input(
            "Home",
            placeholder="Enter your home",
            value=st.session_state.saved_home,
            key="home_input"
        )

        st.session_state.saved_home = home


# -------------------------
# WORK
# -------------------------

with place2:

    with st.container(border=True):

        st.markdown(
            '<div class="place-title">💼 Work</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="place-description">'
            "Your saved work location"
            "</div>",
            unsafe_allow_html=True
        )

        work = st.text_input(
            "Work",
            placeholder="Enter your workplace",
            value=st.session_state.saved_work,
            key="work_input"
        )

        st.session_state.saved_work = work


# -------------------------
# OTHER
# -------------------------

with place3:

    with st.container(border=True):

        st.markdown(
            '<div class="place-title">⭐ Other</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="place-description">'
            "Another frequently used place"
            "</div>",
            unsafe_allow_html=True
        )

        other = st.text_input(
            "Other",
            placeholder="Enter another place",
            value=st.session_state.saved_other,
            key="other_input"
        )

        st.session_state.saved_other = other


# ============================================================
# RECENT ROUTES
# ============================================================

st.markdown("## 🕘 Recent Routes")


route_history = st.session_state.get(
    "route_history",
    []
)


if route_history:

    for route in route_history[:3]:

        start = route.get(
            "start",
            "Unknown"
        )

        destination = route.get(
            "destination",
            "Unknown"
        )

        mode = route.get(
            "travel_mode",
            "Travel"
        )

        route_type = route.get(
            "route_type",
            "Route"
        )

        with st.container(border=True):

            st.markdown(
                f"""
                <div class="route-title">
                    🗺️ {route_type}
                </div>

                <div class="route-info">
                    {start} → {destination}
                </div>

                <div class="route-info">
                    Travel mode: {mode}
                </div>
                """,
                unsafe_allow_html=True
            )

else:

    with st.container(border=True):

        st.markdown(
            """
            <div class="empty-title">
                No recent routes yet
            </div>

            <div class="empty-description">
                Your recently planned climate-aware journeys
                will appear here.
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ACCOUNT
# ============================================================

st.markdown("## ⚙️ Account")


account_col1, account_col2 = st.columns(2)


# -------------------------
# PREFERENCES
# -------------------------

with account_col1:

    with st.container(border=True):

        st.markdown(
            '<div class="section-title">'
            "⚙️ Preferences"
            "</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="account-description">'
            "Manage your climate and route preferences."
            "</div>",
            unsafe_allow_html=True
        )

        if st.button(
            "Open Preferences",
            use_container_width=True
        ):

            st.info(
                "Your climate and route preferences "
                "are available above."
            )


# -------------------------
# SIGN OUT
# -------------------------

with account_col2:

    with st.container(border=True):

        st.markdown(
            '<div class="section-title">'
            "🚪 Sign Out"
            "</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="account-description">'
            "Sign out of your UrbanBreeze account."
            "</div>",
            unsafe_allow_html=True
        )

        if st.button(
            "Sign Out",
            use_container_width=True
        ):

            st.session_state.signed_out = True

            st.success(
                "You have been signed out."
            )
