import streamlit as st


# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="UrbanBreeze",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================
# CUSTOM CSS
# ============================================

st.markdown(
    """
<style>

    /* -------------------------------
       MAIN PAGE
    ------------------------------- */

    .stApp {
        background-color: #f6fbfc;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-left: 5%;
        padding-right: 5%;
        padding-bottom: 3rem;
    }


    /* -------------------------------
       NAVIGATION
    ------------------------------- */

    .logo {
        font-size: 25px;
        font-weight: 700;
        color: #123f4b;
    }

    .nav-text {
        font-size: 15px;
        color: #567078;
        text-align: center;
        padding-top: 8px;
    }


    /* -------------------------------
       HERO SECTION
    ------------------------------- */

    .hero {
        padding-top: 55px;
        padding-bottom: 35px;
    }

    .hero-title {
        font-size: 52px;
        line-height: 1.1;
        font-weight: 750;
        color: #123f4b;
        margin-bottom: 18px;
    }

    .hero-title span {
        color: #159c9c;
    }

    .hero-description {
        font-size: 19px;
        line-height: 1.6;
        color: #61757c;
        max-width: 700px;
        margin-bottom: 25px;
    }


    /* -------------------------------
   DASHBOARD CARDS
------------------------------- */

.dashboard-card {
    background-color: white;
    border: 1px solid #e3edef;
    border-radius: 20px;
    padding: 25px;
    min-height: 175px;
    box-shadow: 0px 5px 18px rgba(18, 63, 75, 0.05);
}

    /* -------------------------------
       SECTION TITLE
    ------------------------------- */

    .section-title {
        font-size: 27px;
        font-weight: 700;
        color: #163f4b;
        margin-top: 35px;
        margin-bottom: 18px;
    }


    /* -------------------------------
       BUTTON
    ------------------------------- */

    .stButton > button {
        border-radius: 12px;
        min-height: 45px;
        font-weight: 600;
    }


    /* -------------------------------
       FOOTER
    ------------------------------- */

    .footer {
        text-align: center;
        color: #8a9ca1;
        font-size: 13px;
        padding-top: 35px;
    }

</style>
""",
    unsafe_allow_html=True,
)


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

st.title("Cooler, smarter,")

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
        "🌡️  PLAN A SMART ROUTE", type="primary", use_container_width=True
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

st.markdown(
    '<div class="section-title">Your climate dashboard</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)


# --------------------------------------------
# CARD 1
# --------------------------------------------

with col1:

    st.markdown("### 🌤️ Current Temperature")

    st.markdown(
        "<h2 style='color:#159c9c;'>-- °C</h2>",
        unsafe_allow_html=True
    )

    st.caption("Location data will appear here")


# --------------------------------------------
# CARD 2
# --------------------------------------------

with col2:

    st.markdown("### 🧊 Cool Score")

    st.markdown(
        "<h2 style='color:#159c9c;'>-- / 100</h2>",
        unsafe_allow_html=True
    )

    st.caption("Your climate comfort score")


# --------------------------------------------
# CARD 3
# --------------------------------------------

with col3:

    st.markdown("### 🚶 Preferred Travel Mode")

    st.markdown(
        "<h2 style='color:#159c9c;'>Walk</h2>",
        unsafe_allow_html=True
    )

    st.caption("Change this in your preferences")



# ============================================
# FEATURES
# ============================================

st.markdown(
    '<div class="section-title">What UrbanBreeze considers</div>',
    unsafe_allow_html=True
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