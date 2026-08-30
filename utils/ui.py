import streamlit as st
import textwrap
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
    background: linear-gradient(
        180deg,
        #071A21 0%,
        #0B252D 50%,
        #0E2B34 100%
    );

    color: #FFFFFF;
}


        .block-container {
    max-width: 1180px;

    padding-top: 5rem;
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
    color: #FFFFFF !important;
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
    color: #D5E5E8 !important;
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

            color: #FFFFFF;

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
    color: #FFFFFF !important;
}

.ub-section-caption {
    color: #B8CDD1 !important;
}


        /* ==================================================
           CARDS
           ================================================== */

        .ub-card {
    background: #112F38;

    border: 1px solid #2A5059;

    border-radius: 20px;

    padding: 1.35rem;

    min-height: 170px;

    box-shadow:
        0 8px 28px
        rgba(0, 0, 0, 0.22);

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease,
        border-color 0.18s ease;
}


        .ub-card:hover {
    transform: translateY(-3px);

    border-color: #159C9C;

    box-shadow:
        0 14px 34px
        rgba(21, 156, 156, 0.15);
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
            color: #FFFFFF;

            font-size: 1rem;

            font-weight: 700;

            margin-bottom: 0.45rem;
        }


        .ub-card-text {
            color: #C1D3D7;

            font-size: 0.88rem;

            line-height: 1.6;
        }
        /* ============================================
               TOP NAVIGATION
               ============================================ */
        
            div[data-testid="stHorizontalBlock"] .stButton > button {
                white-space: nowrap;
            }
        
        /* Profile icon button */
        div[data-testid="stHorizontalBlock"] .stButton > button {
            min-width: 42px;
        }
        
        /* Make the last navigation button round */
        div[data-testid="stHorizontalBlock"] > div:last-child .stButton > button {
            width: 42px !important;
            height: 42px !important;
            min-width: 42px !important;
            min-height: 42px !important;
        
            padding: 0 !important;
        
            border-radius: 50% !important;
        
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        
            font-size: 18px !important;
        }

        /* ==================================================
           DASHBOARD CARDS
           ================================================== */

        [data-testid="stVerticalBlockBorderWrapper"] {
    background: #112F38 !important;

    border: 1px solid #2A5059 !important;

    border-radius: 20px !important;

    box-shadow:
        0 8px 28px
        rgba(0, 0, 0, 0.22) !important;
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
    color: #B8CDD1 !important;

    font-size: 0.78rem !important;
}

[data-testid="stMetricValue"] {
    color: #39C7C2 !important;

    font-size: 1.65rem !important;

    font-weight: 720 !important;
}

        /* ==================================================
           BUTTONS
           ================================================== */

        .stButton > button {
    min-height: 43px;

    padding: 0.55rem 1.1rem;

    border-radius: 12px;

    border: 1px solid #315A63;

    background: #112F38;

    color: #FFFFFF;

    font-size: 0.88rem;

    font-weight: 650;

    transition: all 0.18s ease;
}


        .stButton > button:hover {
    border-color: #159C9C;

    color: #FFFFFF;

    background: #173C46;

    transform: translateY(-1px);

    box-shadow:
        0 5px 16px
        rgba(21, 156, 156, 0.18);
}


        .stButton > button[kind="primary"] {
    background: #159C9C;

    border-color: #159C9C;

    color: #FFFFFF;

    min-height: 48px;

    padding: 0.65rem 1.35rem;

    font-size: 0.92rem;

    box-shadow:
        0 7px 18px
        rgba(21, 156, 156, 0.25);
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
    border-color: #294A53 !important;

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
            <div class="ub-logo-mark">🌬️</div>
            <div> UrbanBreeze</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SECTION TITLE
# ============================================================

# ============================================================
# SECTION TITLE
# ============================================================

def section_title(title, caption=None):

    html = f"""
    <div class="ub-section">
        <div class="ub-section-title">{title}</div>
    """

    if caption:
        html += f"""
        <div class="ub-section-caption">{caption}</div>
        """

    html += """
    </div>
    """

    st.markdown(
        html,
        unsafe_allow_html=True
    )
    
