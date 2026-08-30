import streamlit as st
from utils.ui import apply_urbanbreeze_theme, section_title
from utils.ui import (
    apply_urbanbreeze_theme,
    section_title,
)

# ============================================================
# AUTHENTICATION GATE
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.switch_page("pages/0_Login.py")
# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="UrbanBreeze",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_urbanbreeze_theme()

# ============================================
# NAVIGATION BAR
# ============================================

nav1, nav2, nav3, nav4, nav5 = st.columns(
    [5, 1.15, 1.35, 1.0, 0.7],
    gap="small"
)

with nav1:
    st.markdown(
        '<div class="logo">🌬️ UrbanBreeze</div>',
        unsafe_allow_html=True
    )

with nav2:
    if st.button("Home", use_container_width=True):
        st.switch_page("app.py")

with nav3:
    if st.button("Saved Places", use_container_width=True):
        st.switch_page("pages/3_Saved_Places.py")

with nav4:
    if st.button("History", use_container_width=True):
        st.switch_page("pages/4_Route_History.py")

with nav5:
    if st.button("👤", use_container_width=True):
        st.switch_page("pages/5_Profile.py")

st.divider()


# ============================================
# HERO SECTION
# ============================================

# ============================================
# HERO SECTION
# ============================================

st.title("Cooler & Smarter")

st.header("Climate-aware journeys.")

st.write(
    "UrbanBreeze helps you find routes that consider "
    "temperature, heat exposure, travel mode and "
    "your personal preferences."
)


# ============================================
# PLAN ROUTE BUTTON
# ============================================

button_col1, button_col2 = st.columns([1, 4])

with button_col1:

    if st.button(
        "PLAN A SMART ROUTE", type="primary", use_container_width=True
    ):
        st.switch_page("pages/1_Plan_Route.py")


st.write("")
st.write("")



# ============================================
# FEATURES
# ============================================

st.caption(
    "Environmental and travel factors used to make your journey more comfortable."
)

feature1, feature2, feature3, feature4 = st.columns(4)


with feature1:

    st.markdown("### 🌡️")
    st.markdown("**Temperature**")
    st.caption(
        "Understand environmental conditions "
        "along your journey."
    )


with feature2:

    st.markdown("### 🔥")
    st.markdown("**Heat Exposure**")
    st.caption(
        "Compare routes based on predicted "
        "heat exposure."
    )


with feature3:

    st.markdown("### 🤖")
    st.markdown("**AI Pick**")
    st.caption(
        "Get an explanation of why a route "
        "is recommended."
    )


with feature4:

    st.markdown("### 🔋")
    st.markdown("**EV Friendly**")
    st.caption(
        "Consider charging availability "
        "when planning EV journeys."
    )
# ============================================
# FOOTER
# ============================================

st.markdown(
    """
    <div class="footer">
        UrbanBreeze · Cooler, smarter, climate-aware journeys.
    </div>
    """,
    unsafe_allow_html=True
)
