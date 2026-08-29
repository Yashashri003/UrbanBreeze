import streamlit as st
from utils.ui import apply_urbanbreeze_theme, section_title
from utils.ui import (
    apply_urbanbreeze_theme,
    section_title,
)


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

nav1, nav2, nav3, nav4, nav5 = st.columns([3, 1, 1, 1, 1])

with nav1:
    st.markdown('<div class="logo">🌬️ UrbanBreeze</div>', unsafe_allow_html=True)

with nav2:
    if st.button("Home"):
        st.switch_page("app.py")

with nav3:
    if st.button("Plan Route"):
        st.switch_page("pages/1_Plan_Route.py")

with nav4:
    st.button("Saved Places")

with nav5:
    st.button("History")


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
# CURRENT CONDITIONS CARDS
# ============================================

# ============================================
# CURRENT CONDITIONS CARDS
# ============================================

st.subheader("Your climate dashboard")
st.caption("A quick overview of your climate-aware travel preferences.")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("### 🌤️ Current Temperature")

        st.markdown(
            "<h2 style='color:#159c9c;'>-- °C</h2>",
            unsafe_allow_html=True
        )

        st.caption("Location data will appear here")

with col2:
    with st.container(border=True):
        st.markdown("### 🧊 Cool Score")

        st.markdown(
            "<h2 style='color:#159c9c;'>-- / 100</h2>",
            unsafe_allow_html=True
        )

        st.caption("Your climate comfort score")

with col3:
    with st.container(border=True):
        st.markdown("### 🚶 Preferred Travel Mode")

        st.markdown(
            "<h2 style='color:#159c9c;'>Walk</h2>",
            unsafe_allow_html=True
        )

        st.caption("Change this in your preferences")

# ============================================
# FEATURES
# ============================================

st.subheader("What UrbanBreeze considers")
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
