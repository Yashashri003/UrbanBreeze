import streamlit as st
import os
import json
import hashlib
import re

from utils.ui import apply_urbanbreeze_theme


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Login | UrbanBreeze",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_urbanbreeze_theme()


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(PROJECT_ROOT, "data")

USERS_FILE = os.path.join(DATA_DIR, "users.json")


# ============================================================
# USER STORAGE
# ============================================================

def load_users():

    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(USERS_FILE):
        return []

    try:
        with open(
            USERS_FILE,
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


def save_users(users):

    os.makedirs(DATA_DIR, exist_ok=True)

    with open(
        USERS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            users,
            file,
            indent=2,
            ensure_ascii=False
        )


# ============================================================
# PASSWORD
# ============================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def verify_password(password, password_hash):

    return (
        hash_password(password)
        == password_hash
    )


# ============================================================
# EMAIL VALIDATION
# ============================================================

def valid_email(email):

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.match(
        pattern,
        email
    ) is not None


# ============================================================
# LOGIN USER
# ============================================================

def login_user(user):

    st.session_state.authenticated = True

    st.session_state.current_user_email = user.get(
        "email",
        ""
    )

    st.session_state.profile_name = user.get(
        "name",
        "Your Name"
    )

    st.session_state.profile_username = user.get(
        "username",
        "urbanbreeze_user"
    )

    st.session_state.profile_email = user.get(
        "email",
        ""
    )

    st.session_state.coolness_preference = user.get(
        "coolness_preference",
        55
    )

    st.session_state.max_extra_time = user.get(
        "max_extra_time",
        10
    )

    st.session_state.heat_priority = user.get(
        "heat_priority",
        "High"
    )

    st.session_state.default_travel_mode = user.get(
        "default_travel_mode",
        "🚶 Walk"
    )

    st.session_state.saved_home = user.get(
        "saved_home",
        ""
    )

    st.session_state.saved_work = user.get(
        "saved_work",
        ""
    )

    st.session_state.saved_other = user.get(
        "saved_other",
        ""
    )

    st.session_state.route_history = user.get(
        "route_history",
        []
    )


# ============================================================
# SESSION STATE
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "current_user_email" not in st.session_state:
    st.session_state.current_user_email = None


# ============================================================
# ALREADY LOGGED IN
# ============================================================

if st.session_state.authenticated:

    st.switch_page("app.py")


# ============================================================
# CUSTOM LOGIN CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       LOGIN PAGE BACKGROUND
       ======================================================== */

    .stApp {
        background: linear-gradient(
            180deg,
            #071A21 0%,
            #0B252D 50%,
            #0E2B34 100%
        ) !important;
    }


    /* ========================================================
       PAGE WIDTH
       ======================================================== */

    .block-container {
        max-width: 1180px !important;
        padding-top: 2.5rem !important;
        padding-bottom: 3rem !important;
    }


    /* ========================================================
       CENTER LOGIN AREA
       ======================================================== */

    .login-area {
        width: 100%;
        max-width: 520px;
        margin: 0 auto;
    }


    /* ========================================================
       WELCOME TITLE
       ======================================================== */

    .login-title {
        text-align: center;

        color: #FFFFFF !important;

        font-size: 2.8rem;

        font-weight: 750;

        letter-spacing: -0.04em;

        margin-top: 1rem;

        margin-bottom: 0.45rem;
    }


    .login-subtitle {
        text-align: center;

        color: #B8CDD1 !important;

        font-size: 1rem;

        margin-bottom: 1.8rem;
    }


    /* ========================================================
       CENTER TABS
       ======================================================== */

    div[data-testid="stTabs"] {
        width: 100% !important;

        max-width: 520px !important;

        margin: 0 auto !important;
    }


    div[data-testid="stTabs"] [role="tablist"] {
        justify-content: center !important;

        gap: 2rem !important;

        border-bottom: 1px solid #294A53 !important;
    }


    div[data-testid="stTabs"] button {
        color: #D5E5E8 !important;

        font-size: 0.95rem !important;

        font-weight: 650 !important;

        padding-left: 1rem !important;

        padding-right: 1rem !important;
    }


    div[data-testid="stTabs"]
    button[aria-selected="true"] {
        color: #39C7C2 !important;
    }


    div[data-testid="stTabs"]
    [data-baseweb="tab-highlight"] {
        background-color: #159C9C !important;

        height: 2px !important;
    }


    /* ========================================================
       LOGIN / SIGNUP CARD
       ======================================================== */

    div[data-testid="stForm"] {

        background: #112F38 !important;

        border: 1px solid #2A5059 !important;

        border-radius: 20px !important;

        padding: 2rem 2rem 1.8rem 2rem !important;

        box-shadow:
            0 10px 30px
            rgba(0, 0, 0, 0.22) !important;

        width: 100% !important;

        max-width: 520px !important;

        margin: 1.2rem auto 0 auto !important;
    }


    /* ========================================================
       CARD HEADINGS
       ======================================================== */

    div[data-testid="stForm"] h3,
    div[data-testid="stForm"] h2 {

        color: #FFFFFF !important;

        text-align: center !important;
    }


    div[data-testid="stForm"] p {

        color: #B8CDD1 !important;
    }


    /* ========================================================
       INPUT LABELS
       ======================================================== */

    div[data-testid="stForm"] .stTextInput label {

        color: #D5E5E8 !important;

        font-weight: 600 !important;
    }


    /* ========================================================
       INPUT BOXES
       ======================================================== */

    div[data-testid="stForm"] .stTextInput input {

        background: #FFFFFF !important;

        color: #172B30 !important;

        border: 1px solid #DCE9EB !important;

        border-radius: 11px !important;

        min-height: 46px !important;

        font-size: 0.95rem !important;
    }


    div[data-testid="stForm"]
    .stTextInput input::placeholder {

        color: #789096 !important;

        opacity: 1 !important;
    }


    div[data-testid="stForm"]
    .stTextInput input:focus {

        border-color: #159C9C !important;

        box-shadow:
            0 0 0 1px #159C9C !important;
    }


    /* ========================================================
       LOGIN / CREATE ACCOUNT BUTTON
       ======================================================== */

    div[data-testid="stForm"]
    button[kind="primary"] {

        width: 100% !important;

        min-height: 46px !important;

        margin-top: 0.7rem !important;

        border-radius: 11px !important;

        background: #159C9C !important;

        border: 1px solid #159C9C !important;

        color: #FFFFFF !important;

        font-size: 0.92rem !important;

        font-weight: 700 !important;

        box-shadow:
            0 7px 18px
            rgba(21, 156, 156, 0.20) !important;
    }


    div[data-testid="stForm"]
    button[kind="primary"]:hover {

        background: #118B8B !important;

        border-color: #118B8B !important;

        color: #FFFFFF !important;

        transform: translateY(-1px);
    }


    /* ========================================================
       SUCCESS / ERROR MESSAGES
       ======================================================== */

    div[data-testid="stAlert"] {

        border-radius: 10px !important;
    }


    /* ========================================================
       REMOVE EXCESS TAB CONTENT SPACE
       ======================================================== */

    div[data-testid="stTabsContent"] {

        padding-top: 0 !important;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 600px) {

        .block-container {

            padding-left: 1rem !important;

            padding-right: 1rem !important;
        }


        .login-title {

            font-size: 2.25rem;
        }


        .login-area {

            max-width: 100%;
        }


        div[data-testid="stForm"] {

            padding: 1.5rem 1.2rem !important;

            border-radius: 17px !important;
        }


        div[data-testid="stTabs"]
        [role="tablist"] {

            gap: 0.5rem !important;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CENTER PAGE
# ============================================================

st.markdown(
    '<div class="login-area">',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="login-title">'
    'Welcome to UrbanBreeze'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="login-subtitle">'
    'Cooler & smarter climate-aware journeys.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# TABS
# ============================================================

login_tab, signup_tab = st.tabs(
    [
        "🔐 Login",
        "✨ Sign Up"
    ]
)


# ============================================================
# LOGIN
# ============================================================

with login_tab:

    with st.form("login_form"):

        login_email = st.text_input(
            "Email",
            placeholder="you@example.com"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            placeholder="Your password"
        )

        login_button = st.form_submit_button(
            "LOGIN",
            type="primary",
            use_container_width=True
        )

    if login_button:

        email = login_email.strip().lower()

        if not email or not login_password:

            st.error(
                "Please enter your email and password."
            )

        else:

            users = load_users()

            user = None

            for existing_user in users:

                if (
                    existing_user
                    .get("email", "")
                    .lower()
                    == email
                ):

                    user = existing_user
                    break

            if user is None:

                st.error(
                    "No account found with this email."
                )

            elif not verify_password(
                login_password,
                user.get(
                    "password_hash",
                    ""
                )
            ):

                st.error(
                    "Incorrect password."
                )

            else:

                login_user(user)

                st.success(
                    "Login successful!"
                )

                # GO TO MAIN APP
                st.switch_page("app.py")


# ============================================================
# SIGN UP
# ============================================================

with signup_tab:

    with st.form("signup_form"):

        st.markdown(
            '<div class="login-card-title">'
            'Create Account'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="login-card-subtitle">'
            'Start your climate-aware journey with UrbanBreeze.'
            '</div>',
            unsafe_allow_html=True
        )

        signup_name = st.text_input(
            "Full Name",
            placeholder="Your name"
        )

        signup_username = st.text_input(
            "Username",
            placeholder="Choose a username"
        )

        signup_email = st.text_input(
            "Email",
            placeholder="you@example.com"
        )

        signup_password = st.text_input(
            "Password",
            type="password",
            placeholder="At least 6 characters"
        )

        signup_confirm = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password"
        )

        signup_button = st.form_submit_button(
            "CREATE ACCOUNT",
            type="primary",
            use_container_width=True
        )


    # ========================================================
    # SIGNUP PROCESS
    # ========================================================

    if signup_button:

        name = signup_name.strip()

        username = signup_username.strip()

        email = signup_email.strip().lower()


        if not name:

            st.error(
                "Please enter your name."
            )

        elif not username:

            st.error(
                "Please choose a username."
            )

        elif not valid_email(email):

            st.error(
                "Please enter a valid email address."
            )

        elif len(signup_password) < 6:

            st.error(
                "Password must contain at least 6 characters."
            )

        elif signup_password != signup_confirm:

            st.error(
                "Passwords do not match."
            )

        else:

            users = load_users()

            email_exists = any(
                user.get(
                    "email",
                    ""
                ).lower()
                == email
                for user in users
            )

            username_exists = any(
                user.get(
                    "username",
                    ""
                ).lower()
                == username.lower()
                for user in users
            )


            if email_exists:

                st.error(
                    "An account with this email already exists."
                )

            elif username_exists:

                st.error(
                    "That username is already taken."
                )

            else:

                new_user = {

                    "name": name,

                    "username": username,

                    "email": email,

                    "password_hash":
                        hash_password(
                            signup_password
                        ),

                    "coolness_preference": 55,

                    "max_extra_time": 10,

                    "heat_priority": "High",

                    "default_travel_mode":
                        "🚶 Walk",

                    "saved_home": "",

                    "saved_work": "",

                    "saved_other": "",

                    "route_history": []
                }


                users.append(new_user)

                save_users(users)

                login_user(new_user)

                st.success(
                    "Account created successfully!"
                )

                # GO TO MAIN APP
                st.switch_page("app.py")


# ============================================================
# CLOSE CENTER
# ============================================================

st.markdown(
    '</div>',
    unsafe_allow_html=True
)
