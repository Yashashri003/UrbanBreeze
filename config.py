import os

from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# FORTYGUARD
# ============================================================

FORTYGUARD_API_KEY = os.getenv(
    "FORTYGUARD_API_KEY"
)


# ============================================================
# FORTYGUARD DEVELOPMENT MODE
# ============================================================

# True  = use cached/demo climate data
# False = use real FortyGuard API
#
# KEEP THIS TRUE while developing so that
# you don't unnecessarily consume API credits.

FORTYGUARD_DEMO_MODE = True


# ============================================================
# ROUTE SETTINGS
# ============================================================

# Number of climate sampling points
# per route.

CLIMATE_SAMPLE_POINTS = 5


# ============================================================
# APPLICATION SETTINGS
# ============================================================

APP_NAME = "UrbanBreeze"

APP_VERSION = "1.0.0"