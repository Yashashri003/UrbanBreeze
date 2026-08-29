import streamlit as st


# ============================================================
# URBANBREEZE DESIGN SYSTEM
# ============================================================

def apply_urbanbreeze_theme():

    st.markdown(
        """
        <style>

        /* ==================================================
           GLOBAL PAGE
           ================================================== */

        .stApp {
            background:
                linear-gradient(
                    180deg,
                    #F8FCFC 0%,
                    #F3F9F9 100%
                );

            color: #173F49;
        }


        .block-container {
            max-width: 1180px;

            padding-top: 1rem;
            padding-bottom: 3rem;

            padding-left: 2rem;
            padding-right: 2rem;
        }


        /* Hide Streamlit menu */
        #MainMenu {
            visibility: hidden;
        }


        /* Hide footer */
        footer {
            visibility: hidden;
        }


        /* ==================================================
           TYPOGRAPHY
           ================================================== */

        html,
        body,
        [class*="css"] {
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }


        h1,
        h2,
        h3,
        h4 {
            color: #123F4B !important;
        }


        h1 {
            font-size: 2.8rem !important;
            line-height: 1.1 !important;
            font-weight: 750 !important;
            letter-spacing: -0.04em !important;
        }


        h2 {
            font-size: 1.75rem !important;
            line-height: 1.2 !important;
            font-weight: 720 !important;
            letter-spacing: -0.025em !important;
        }


        h3 {
            font-size: 1.05rem !important;
            line-height: 1.3 !important;
            font-weight: 700 !important;
        }


        p {
            color: #637B82;
        }


        /* ==================================================
           NAVIGATION
           ================================================== */

        .ub-navbar {
            display: flex;

            align-items: center;

            justify-content: space-between;

            min-height: 62px;

            padding: 0.25rem 0;
        }


        .ub-logo {
            display: flex;

            align-items: center;

            gap: 0.55rem;

            color: #123F4B;

            font-size: 1.35rem;

            font-weight: 750;

            letter-spacing: -0.035em;

            white-space: nowrap;
        }


        .ub-logo-mark {
            width: 34px;

            height: 34px;

            display: flex;

            align-items: center;

            justify-content: center;

            background: #E5F6F5;

            border-radius: 11px;

            font-size: 1.05rem;
        }


        /* ==================================================
           HERO
           ================================================== */

        .ub-hero {
            padding-top: 3.8rem;

            padding-bottom: 3.4rem;
        }


        .ub-eyebrow {
            display: inline-block;

            color: #118B8B;

            background: #E7F7F6;

            border-radius: 999px;

            padding: 0.42rem 0.8rem;

            font-size: 0.72rem;

            font-weight: 750;

            letter-spacing: 0.11em;

            text-transform: uppercase;

            margin-bottom: 1.1rem;
        }


        .ub-hero-title {
            max-width: 780px;

            color: #123F4B;

            font-size: 4rem;

            line-height: 1.02;

            font-weight: 780;

            letter-spacing: -0.055em;

            margin: 0;
        }


        .ub-hero-title span {
            color: #159C9C;
        }


        .ub-hero-description {
            max-width: 690px;

            margin-top: 1.35rem;

            color: #657D83;

            font-size: 1.05rem;

            line-height: 1.7;
        }


        .ub-hero-note {
            margin-top: 1rem;

            color: #82979C;

            font-size: 0.82rem;
        }


        /* ==================================================
           SECTION
           ================================================== */

        .ub-section {
            margin-top: 2.6rem;

            margin-bottom: 1.2rem;
        }


        .ub-section-title {
            color: #123F4B;

            font-size: 1.55rem;

            font-weight: 730;

            letter-spacing: -0.025em;
        }


        .ub-section-caption {
            color: #789097;

            font-size: 0.88rem;

            margin-top: 0.3rem;
        }


        /* ==================================================
           CARDS
           ================================================== */

        .ub-card {
            background: #FFFFFF;

            border: 1px solid #E0EBED;

            border-radius: 20px;

            padding: 1.35rem;

            min-height: 170px;

            box-shadow:
                0 8px 28px
                rgba(18, 63, 75, 0.045);

            transition:
                transform 0.18s ease,
                box-shadow 0.18s ease,
                border-color 0.18s ease;
        }


        .ub-card:hover {
            transform: translateY(-3px);

            border-color: #B9DCDD;

            box-shadow:
                0 14px 34px
                rgba(18, 63, 75, 0.08);
        }


        .ub-card-icon {
            width: 44px;

            height: 44px;

            display: flex;

            align-items: center;

            justify-content: center;

            background: #E9F7F6;

            border-radius: 13px;

            font-size: 1.25rem;

            margin-bottom: 1rem;
        }


        .ub-card-title {
            color: #173F49;

            font-size: 1rem;

            font-weight: 700;

            margin-bottom: 0.45rem;
        }


        .ub-card-text {
            color: #71878D;

            font-size: 0.88rem;

            line-height: 1.6;
        }


        /* ==================================================
           DASHBOARD CARDS
           ================================================== */

        [data-testid="stVerticalBlockBorderWrapper"] {
            background: #FFFFFF !important;

            border: 1px solid #E0EBED !important;

            border-radius: 20px !important;

            box-shadow:
                0 8px 28px
                rgba(18, 63, 75, 0.045) !important;
        }


        /* ==================================================
           METRICS
           ================================================== */

        [data-testid="stMetric"] {
            background: transparent !important;

            border: none !important;

            padding: 0.2rem 0 !important;

            box-shadow: none !important;
        }


        [data-testid="stMetricLabel"] {
            color: #71878D !important;

            font-size: 0.78rem !important;
        }


        [data-testid="stMetricValue"] {
            color: #159C9C !important;

            font-size: 1.65rem !important;

            font-weight: 720 !important;
        }


        /* ==================================================
           BUTTONS
           ================================================== */

        .stButton > button {
            min-height: 43px;

            padding:
                0.55rem 1.1rem;

            border-radius: 12px;

            border: 1px solid #DCE9EB;

            background: #FFFFFF;

            color: #234F59;

            font-size: 0.88rem;

            font-weight: 650;

            transition:
                all 0.18s ease;
        }


        .stButton > button:hover {
            border-color: #159C9C;

            color: #118B8B;

            transform: translateY(-1px);

            box-shadow:
                0 5px 16px
                rgba(21, 156, 156, 0.1);
        }


        .stButton > button[kind="primary"] {
            background: #159C9C;

            border-color: #159C9C;

            color: #FFFFFF;

            min-height: 48px;

            padding:
                0.65rem 1.35rem;

            font-size: 0.92rem;

            box-shadow:
                0 7px 18px
                rgba(21, 156, 156, 0.2);
        }


        .stButton > button[kind="primary"]:hover {
            background: #118B8B;

            border-color: #118B8B;

            color: #FFFFFF;
        }


        /* ==================================================
           INPUTS
           ================================================== */

        .stTextInput input {
            min-height: 45px !important;

            border-radius: 12px !important;

            border-color: #DCE9EB !important;

            background: #FFFFFF !important;
        }


        .stTextInput input:focus {
            border-color: #159C9C !important;

            box-shadow:
                0 0 0 1px #159C9C !important;
        }


        .stTextInput label,
        .stSelectbox label,
        .stRadio label,
        .stCheckbox label,
        .stSlider label {
            color: #365962 !important;

            font-weight: 600 !important;
        }


        /* ==================================================
           DIVIDERS
           ================================================== */

        hr {
            border-color: #E1ECEE !important;

            margin-top: 1rem !important;

            margin-bottom: 1rem !important;
        }


        /* ==================================================
           MAP
           ================================================== */

        iframe {
            border-radius: 18px !important;
        }


        /* ==================================================
           FOOTER
           ================================================== */

        .ub-footer {
            text-align: center;

            padding-top: 2rem;

            padding-bottom: 0.5rem;

            color: #8AA0A6;

            font-size: 0.78rem;
        }


        /* ==================================================
           MOBILE
           ================================================== */

        @media (max-width: 768px) {

            .block-container {
                padding-left: 1rem;

                padding-right: 1rem;
            }


            .ub-hero {
                padding-top: 2.5rem;

                padding-bottom: 2.2rem;
            }


            .ub-hero-title {
                font-size: 2.7rem;
            }


            h1 {
                font-size: 2.4rem !important;
            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# LOGO
# ============================================================

def logo():

    st.markdown(
        """
        <div class="ub-logo">

            <div class="ub-logo-mark">
                🌬️
            </div>

            <div>
                UrbanBreeze
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SECTION TITLE
# ============================================================

def section_title(
    title,
    caption=None
):

    st.markdown(
        f"""
        <div class="ub-section">

            <div class="ub-section-title">
                {title}
            </div>

            {
                f'<div class="ub-section-caption">{caption}</div>'
                if caption
                else ""
            }

        </div>
        """,
        unsafe_allow_html=True
    )