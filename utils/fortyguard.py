import hashlib
import json
import os
import time
import requests
from dotenv import load_dotenv
from config import (
    FORTYGUARD_DEMO_MODE
)

# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

FORTYGUARD_API_KEY = os.getenv("FORTYGUARD_API_KEY")

FORTYGUARD_BASE_URL = "https://api.fortyguard.com/v1"


# ============================================================
# CACHE CONFIGURATION
# ============================================================

# Cache file is stored inside:
#
# UrbanBreeze/
#     data/
#         fortyguard_cache.json

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIRECTORY = os.path.join(
    PROJECT_ROOT,
    "data"
)

CACHE_FILE = os.path.join(
    DATA_DIRECTORY,
    "fortyguard_cache.json"
)


# ============================================================
# CALIFORNIA BOUNDARY
# ============================================================

CA_WEST = -124.5
CA_SOUTH = 32.5
CA_EAST = -114.0
CA_NORTH = 42.1


# ============================================================
# CACHE FUNCTIONS
# ============================================================

def ensure_cache_directory():
    """
    Create the data directory if it doesn't exist.
    """

    os.makedirs(
        DATA_DIRECTORY,
        exist_ok=True
    )


def load_cache():
    """
    Load FortyGuard results from local cache.

    If the cache doesn't exist, return an empty dictionary.
    """

    ensure_cache_directory()

    if not os.path.exists(CACHE_FILE):
        return {}

    try:

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, dict):
                return data

            return {}

    except (
        json.JSONDecodeError,
        OSError
    ):

        return {}


def save_cache(cache):
    """
    Save FortyGuard results to local cache.
    """

    ensure_cache_directory()

    try:

        temporary_file = CACHE_FILE + ".tmp"

        with open(
            temporary_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                cache,
                file,
                indent=2
            )

        os.replace(
            temporary_file,
            CACHE_FILE
        )

    except OSError as error:

        print(
            f"Warning: Could not save "
            f"FortyGuard cache: {error}"
        )


def make_temperature_cache_key(
    latitude,
    longitude,
    date_string,
    time_string
):
    """
    Create a unique cache key based on:

        latitude
        longitude
        date
        time
    """

    raw = (
        f"{round(float(latitude), 4)}|"
        f"{round(float(longitude), 4)}|"
        f"{date_string}|"
        f"{time_string}"
    )

    return hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()


# ============================================================
# CALIFORNIA CHECK
# ============================================================

def is_california_coordinate(
    latitude,
    longitude
):
    """
    Basic California geographic check.
    """

    try:

        latitude = float(latitude)
        longitude = float(longitude)

    except (
        TypeError,
        ValueError
    ):

        return False

    return (
        CA_SOUTH <= latitude <= CA_NORTH
        and
        CA_WEST <= longitude <= CA_EAST
    )


# ============================================================
# API KEY CHECK
# ============================================================

def fortyguard_available():
    """
    Check whether the FortyGuard API key exists.
    """

    return bool(
        FORTYGUARD_API_KEY
    )


# ============================================================
# REQUEST HEADERS
# ============================================================

def get_headers():
    """
    Headers used by FortyGuard.
    """

    return {
        "api-key": FORTYGUARD_API_KEY,
        "Content-Type": "application/json"
    }


# ============================================================
# CREATE POLYGON
# ============================================================

def create_point_polygon(
    latitude,
    longitude,
    size=0.015
):
    """
    Create a small GeoJSON polygon around
    a route point.

    GeoJSON uses:

        [longitude, latitude]
    """

    latitude = float(latitude)
    longitude = float(longitude)

    west = longitude - size
    east = longitude + size

    south = latitude - size
    north = latitude + size

    return {

        "type": "FeatureCollection",

        "features": [

            {

                "type": "Feature",

                "properties": {},

                "geometry": {

                    "type": "Polygon",

                    "coordinates": [

                        [

                            [
                                west,
                                south
                            ],

                            [
                                east,
                                south
                            ],

                            [
                                east,
                                north
                            ],

                            [
                                west,
                                north
                            ],

                            [
                                west,
                                south
                            ]

                        ]

                    ]

                }

            }

        ]

    }


# ============================================================
# SUBMIT HEATMAP
# ============================================================

def request_temperature(
    latitude,
    longitude,
    date_string,
    time_string
):
    """
    Submit a FortyGuard heatmap request.

    IMPORTANT:
    This function makes an actual API request.
    """

    if not fortyguard_available():

        return {
            "success": False,
            "error": (
                "FortyGuard API key is missing."
            )
        }


    if not is_california_coordinate(
        latitude,
        longitude
    ):

        return {
            "success": False,
            "error": (
                "Location is outside "
                "California."
            )
        }


    polygon = create_point_polygon(
        latitude,
        longitude
    )


    payload = {

        "polygon_aoi": polygon,

        "date_time": {

            "start_date": date_string,

            "start_time": time_string,

            "filter_type": 1

        },

        "granularity": 100,

        "analytic_type": "tcm"

    }


    url = (
        f"{FORTYGUARD_BASE_URL}"
        "/heatmap"
    )


    print("\n")
    print("=" * 60)
    print("FORTYGUARD API REQUEST")
    print("=" * 60)

    print(
        "Location:",
        latitude,
        longitude
    )

    print(
        "Date:",
        date_string
    )

    print(
        "Time:",
        time_string
    )

    print(
        "NOTE: This request consumes "
        "FortyGuard API usage."
    )

    print("=" * 60)


    try:

        response = requests.post(

            url,

            headers=get_headers(),

            json=payload,

            timeout=30

        )


    except requests.RequestException as error:

        return {

            "success": False,

            "error": (
                f"FortyGuard request failed: "
                f"{error}"
            )

        }


    if response.status_code != 200:

        return {

            "success": False,

            "error": (
                f"FortyGuard returned "
                f"{response.status_code}: "
                f"{response.text}"
            )

        }


    try:

        data = response.json()

    except ValueError:

        return {

            "success": False,

            "error": (
                "FortyGuard returned "
                "invalid JSON."
            )

        }


    activity_id = (
        data
        .get("data", {})
        .get("activity_id")
    )


    if not activity_id:

        return {

            "success": False,

            "error": (
                "FortyGuard did not return "
                "an activity ID."
            )

        }


    print(
        "Activity ID:",
        activity_id
    )

    print("=" * 60)


    return {

        "success": True,

        "activity_id": activity_id

    }


# ============================================================
# CHECK ACTIVITY STATUS
# ============================================================

def get_activity_status(
    activity_id
):
    """
    Check the status of a FortyGuard activity.

    IMPORTANT:
    Polling is required after submitting a heatmap.
    """

    url = (
        f"{FORTYGUARD_BASE_URL}"
        f"/status/{activity_id}"
    )


    try:

        response = requests.get(

            url,

            headers=get_headers(),

            timeout=30

        )

    except requests.RequestException as error:

        return {

            "success": False,

            "error": str(error)

        }


    if response.status_code != 200:

        return {

            "success": False,

            "error": (
                f"FortyGuard status "
                f"{response.status_code}: "
                f"{response.text}"
            )

        }


    try:

        response_data = response.json()

    except ValueError:

        return {

            "success": False,

            "error": (
                "FortyGuard status "
                "returned invalid JSON."
            )

        }


    return {

        "success": True,

        "data": response_data

    }


# ============================================================
# WAIT FOR RESULT
# ============================================================

def wait_for_temperature(
    activity_id,
    max_attempts=12,
    wait_seconds=5
):
    """
    Poll FortyGuard until the heatmap completes.

    Maximum default waiting time:

        12 × 5 seconds
        = approximately 60 seconds
    """

    for attempt in range(
        max_attempts
    ):

        status_response = (
            get_activity_status(
                activity_id
            )
        )


        if not status_response[
            "success"
        ]:

            return {

                "success": False,

                "error":
                    status_response[
                        "error"
                    ]

            }


        response_data = (
            status_response["data"]
        )


        data = response_data.get(
            "data",
            response_data
        )


        status = data.get(
            "status"
        )


        print(
            f"FortyGuard status "
            f"{attempt + 1}/{max_attempts}: "
            f"{status}"
        )


        # ----------------------------------------------------
        # COMPLETED
        # ----------------------------------------------------

        if status == "Completed":

            result = data.get(
                "result",
                {}
            )


            return {

                "success": True,

                "result": result

            }


        # ----------------------------------------------------
        # FAILED
        # ----------------------------------------------------

        if status == "Failed":

            return {

                "success": False,

                "error": (
                    "FortyGuard heatmap "
                    "processing failed."
                )

            }


        # ----------------------------------------------------
        # STILL PROCESSING
        # ----------------------------------------------------

        if attempt < max_attempts - 1:

            time.sleep(
                wait_seconds
            )


    return {

        "success": False,

        "error": (
            "FortyGuard request timed out "
            "while waiting for completion."
        )

    }


# ============================================================
# DEMO CLIMATE DATA
# ============================================================

def get_demo_temperature(
    latitude,
    longitude,
    date_string="2024-07-15",
    time_string="14:00"
):
    """
    Return deterministic demo climate data.

    This mode makes ZERO FortyGuard API requests.
    The same coordinates always return the same
    temperature, so route comparisons remain stable.
    """

    # Build a deterministic number from the coordinates.
    # No API call and no global random state are used.
    seed_text = (
        f"{round(float(latitude), 4)}|"
        f"{round(float(longitude), 4)}"
    )

    seed = sum(
        (index + 1) * ord(character)
        for index, character in enumerate(seed_text)
    )

    # Keep the result in a realistic California range.
    temperature = 17.0 + (seed % 1200) / 100.0

    minimum = temperature - (1.0 + (seed % 200) / 100.0)
    maximum = temperature + (1.0 + ((seed // 7) % 200) / 100.0)

    return {
        "success": True,
        "temperature": round(temperature, 2),
        "minimum": round(minimum, 2),
        "maximum": round(maximum, 2),
        "activity_id": "DEMO",
        "date": date_string,
        "time": time_string,
        "latitude": float(latitude),
        "longitude": float(longitude),
        "source": "UrbanBreeze Demo Climate Data",
        "api_called": False
    }


# ============================================================
# GET TEMPERATURE
# ============================================================

def get_temperature(
    latitude,
    longitude,
    date_string="2024-07-15",
    time_string="14:00"
):
    """
    Get temperature for a location.

    CACHE-FIRST DESIGN:

        1. Check local cache
        2. If found -> return cached result
        3. If not found -> call FortyGuard
        4. Save result
        5. Return result

    This prevents repeated API calls for
    the same location/date/time.

    DEMO MODE:
        If FORTYGUARD_DEMO_MODE is True, this function
        returns deterministic local demo data and does
        not contact FortyGuard at all.
    """

    latitude = float(latitude)
    longitude = float(longitude)


    # ========================================================
    # DEMO MODE — NO API REQUEST
    # ========================================================

    if FORTYGUARD_DEMO_MODE:

        print("\n")
        print("=" * 60)
        print("FORTYGUARD DEMO MODE")
        print("=" * 60)

        print(
            "Using local demo climate data."
        )

        print(
            "NO FORTYGUARD API REQUEST MADE."
        )

        print(
            "Location:",
            latitude,
            longitude
        )

        print("=" * 60)

        return get_demo_temperature(
            latitude,
            longitude,
            date_string,
            time_string
        )


    # ========================================================
    # CREATE CACHE KEY
    # ========================================================

    cache_key = make_temperature_cache_key(

        latitude,

        longitude,

        date_string,

        time_string

    )


    # ========================================================
    # CHECK CACHE FIRST
    # ========================================================

    cache = load_cache()


    if cache_key in cache:

        cached_result = cache[
            cache_key
        ]


        print("\n")
        print("=" * 60)
        print("FORTYGUARD CACHE HIT")
        print("=" * 60)

        print(
            "Location:",
            latitude,
            longitude
        )

        print(
            "Date:",
            date_string
        )

        print(
            "Time:",
            time_string
        )

        print(
            "Using saved temperature."
        )

        print(
            "NO API REQUEST MADE."
        )

        print("=" * 60)


        return cached_result


    # ========================================================
    # CACHE MISS
    # ========================================================

    print("\n")
    print("=" * 60)
    print("FORTYGUARD CACHE MISS")
    print("=" * 60)

    print(
        "No saved result found."
    )

    print(
        "FortyGuard API will be called."
    )

    print("=" * 60)


    # ========================================================
    # SUBMIT API REQUEST
    # ========================================================

    submission = request_temperature(

        latitude,

        longitude,

        date_string,

        time_string

    )


    if not submission[
        "success"
    ]:

        return submission


    activity_id = (
        submission[
            "activity_id"
        ]
    )


    # ========================================================
    # WAIT FOR COMPLETION
    # ========================================================

    result = wait_for_temperature(

        activity_id

    )


    if not result[
        "success"
    ]:

        return result


    result_data = result[
        "result"
    ]


    # ========================================================
    # EXTRACT STATS
    # ========================================================

    stats = result_data.get(

        "stats_data",

        {}

    )


    temperature_stats = stats.get(

        "temperature_stats",

        {}

    )


    mean_temperature = (
        temperature_stats.get(
            "mean"
        )
    )


    minimum_temperature = (
        temperature_stats.get(
            "minimum"
        )
    )


    maximum_temperature = (
        temperature_stats.get(
            "maximum"
        )
    )


    # ========================================================
    # VALIDATE RESULT
    # ========================================================

    if mean_temperature is None:

        return {

            "success": False,

            "error": (
                "FortyGuard completed "
                "successfully, but no "
                "temperature mean was found."
            ),

            "raw_stats": stats,

            "activity_id": activity_id

        }


    # ========================================================
    # BUILD RESULT
    # ========================================================

    final_result = {

        "success": True,

        "temperature": float(
            mean_temperature
        ),

        "minimum": (
            float(
                minimum_temperature
            )
            if minimum_temperature is not None
            else None
        ),

        "maximum": (
            float(
                maximum_temperature
            )
            if maximum_temperature is not None
            else None
        ),

        "activity_id":
            activity_id,

        "date":
            date_string,

        "time":
            time_string,

        "latitude":
            latitude,

        "longitude":
            longitude

    }


    # ========================================================
    # SAVE TO CACHE
    # ========================================================

    cache[cache_key] = final_result

    save_cache(
        cache
    )


    print("\n")
    print("=" * 60)
    print("FORTYGUARD RESULT SAVED TO CACHE")
    print("=" * 60)

    print(
        json.dumps(
            final_result,
            indent=2
        )
    )

    print(
        "\nFuture requests for the "
        "same location/date/time "
        "will NOT call FortyGuard."
    )

    print("=" * 60)


    return final_result


# ============================================================
# END OF FILE
# ============================================================