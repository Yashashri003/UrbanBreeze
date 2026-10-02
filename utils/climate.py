import requests


# ============================================================
# OPEN-METEO CONFIGURATION
# ============================================================

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# Number of route points used for climate analysis
DEFAULT_SAMPLE_POINTS = 5

# Request timeout in seconds
REQUEST_TIMEOUT = 15


# ============================================================
# ROUTE SAMPLING
# ============================================================

def sample_route_points(
    geometry,
    number_of_points=DEFAULT_SAMPLE_POINTS
):
    """
    Select evenly distributed points from an OSRM route.

    OSRM geometry format:
        [longitude, latitude]

    Returned format:
        {
            "lat": latitude,
            "lon": longitude
        }
    """

    if not geometry:
        return []

    coordinates = geometry.get(
        "coordinates",
        []
    )

    if not coordinates:
        return []

    # --------------------------------------------------------
    # Clean duplicate points
    # --------------------------------------------------------

    cleaned = []

    previous = None

    for point in coordinates:

        if len(point) < 2:
            continue

        try:
            lon = float(point[0])
            lat = float(point[1])
        except (TypeError, ValueError):
            continue

        current = (
            round(lat, 6),
            round(lon, 6)
        )

        if current == previous:
            continue

        cleaned.append(
            [lon, lat]
        )

        previous = current

    if not cleaned:
        return []

    # --------------------------------------------------------
    # Select evenly spaced points
    # --------------------------------------------------------

    number_of_points = max(
        1,
        int(number_of_points)
    )

    if len(cleaned) <= number_of_points:

        selected = cleaned

    elif number_of_points == 1:

        selected = [
            cleaned[
                len(cleaned) // 2
            ]
        ]

    else:

        selected = []

        for i in range(number_of_points):

            position = (
                i
                * (len(cleaned) - 1)
                / (number_of_points - 1)
            )

            index = round(position)

            selected.append(
                cleaned[index]
            )

    # --------------------------------------------------------
    # Convert to latitude/longitude
    # --------------------------------------------------------

    points = []

    for point in selected:

        lon = float(point[0])
        lat = float(point[1])

        points.append(
            {
                "lat": lat,
                "lon": lon
            }
        )

    return points


# ============================================================
# TEMPERATURE CONVERSION
# ============================================================

def clean_temperature(value):

    if value is None:
        return None

    try:
        return float(value)

    except (
        TypeError,
        ValueError
    ):
        return None


# ============================================================
# OPEN-METEO WEATHER REQUEST
# ============================================================

def get_open_meteo_temperatures(points):
    """
    Get current weather for multiple route points
    using a SINGLE Open-Meteo API request.

    Open-Meteo supports multiple coordinates in one request,
    so 5 sampled route points do not require 5 API calls.

    Returns:
        List of dictionaries containing:
            lat
            lon
            temperature
            apparent_temperature
            humidity
            success
    """

    if not points:
        return []

    # --------------------------------------------------------
    # Build coordinate lists
    # --------------------------------------------------------

    latitudes = ",".join(
        str(point["lat"])
        for point in points
    )

    longitudes = ",".join(
        str(point["lon"])
        for point in points
    )

    params = {
        "latitude": latitudes,
        "longitude": longitudes,
        "current": (
            "temperature_2m,"
            "apparent_temperature,"
            "relative_humidity_2m"
        ),
        "timezone": "auto"
    }

    try:

        response = requests.get(
            OPEN_METEO_URL,
            params=params,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as error:

        print(
            f"\nOPEN-METEO ERROR: {error}"
        )

        return [
            {
                "lat": point["lat"],
                "lon": point["lon"],
                "success": False,
                "error": str(error)
            }
            for point in points
        ]

    except ValueError as error:

        print(
            f"\nOPEN-METEO JSON ERROR: {error}"
        )

        return [
            {
                "lat": point["lat"],
                "lon": point["lon"],
                "success": False,
                "error": "Invalid JSON response."
            }
            for point in points
        ]

    # --------------------------------------------------------
    # Open-Meteo returns a list when multiple coordinates
    # are requested.
    # --------------------------------------------------------

    if not isinstance(data, list):

        data = [data]

    results = []

    for index, point in enumerate(points):

        if index >= len(data):

            results.append(
                {
                    "lat": point["lat"],
                    "lon": point["lon"],
                    "success": False,
                    "error": "Missing Open-Meteo result."
                }
            )

            continue

        location_data = data[index]

        current = location_data.get(
            "current",
            {}
        )

        temperature = clean_temperature(
            current.get(
                "temperature_2m"
            )
        )

        apparent_temperature = clean_temperature(
            current.get(
                "apparent_temperature"
            )
        )

        humidity = current.get(
            "relative_humidity_2m"
        )

        if temperature is None:

            results.append(
                {
                    "lat": point["lat"],
                    "lon": point["lon"],
                    "success": False,
                    "error":
                        "Temperature was not returned."
                }
            )

            continue

        results.append(
            {
                "lat": point["lat"],
                "lon": point["lon"],
                "success": True,

                "temperature":
                    temperature,

                "apparent_temperature":
                    apparent_temperature,

                "humidity":
                    humidity
            }
        )

    return results


# ============================================================
# SINGLE POINT ANALYSIS
# ============================================================

def analyze_temperature_point(
    index,
    point
):
    """
    Compatibility helper.

    This function performs a single Open-Meteo request.

    The main route analysis below uses the batch function
    instead, because that requires only one API request.
    """

    results = get_open_meteo_temperatures(
        [point]
    )

    if not results:

        return {
            "index": index,
            "lat": point["lat"],
            "lon": point["lon"],
            "success": False,
            "error":
                "No Open-Meteo result."
        }

    result = results[0]

    result["index"] = index

    return result


# ============================================================
# ROUTE TEMPERATURE ANALYSIS
# ============================================================

def analyze_route_temperature(
    route,
    number_of_points=DEFAULT_SAMPLE_POINTS
):
    """
    Analyze temperature along a route.

    The route is sampled at evenly distributed points.

    IMPORTANT:
    All sampled points are sent to Open-Meteo in ONE request.

    This avoids making five separate API requests for
    a five-point route.
    """

    geometry = route.get(
        "geometry"
    )

    if not geometry:

        return {
            "success": False,
            "error":
                "Route geometry is missing."
        }

    # ========================================================
    # SAMPLE ROUTE
    # ========================================================

    points = sample_route_points(
        geometry,
        number_of_points
    )

    if not points:

        return {
            "success": False,
            "error":
                "No valid route points were found."
        }

    print("\n")
    print("=" * 60)
    print(
        f"CLIMATE ANALYSIS → "
        f"{len(points)} POINTS"
    )
    print("=" * 60)

    print(
        "Using Open-Meteo..."
    )

    print(
        "One request will be used for "
        "all sampled points."
    )

    print("=" * 60)

    # ========================================================
    # GET WEATHER
    # ========================================================

    point_results = get_open_meteo_temperatures(
        points
    )

    # Add index so route order is preserved
    for index, result in enumerate(
        point_results
    ):

        result["index"] = index

    # ========================================================
    # PROCESS RESULTS
    # ========================================================

    temperatures = []

    apparent_temperatures = []

    successful_results = []

    for result in point_results:

        if result.get(
            "success",
            False
        ):

            temperature = clean_temperature(
                result.get(
                    "temperature"
                )
            )

            apparent_temperature = clean_temperature(
                result.get(
                    "apparent_temperature"
                )
            )

            if temperature is not None:

                temperatures.append(
                    temperature
                )

                successful_results.append(
                    result
                )

            if apparent_temperature is not None:

                apparent_temperatures.append(
                    apparent_temperature
                )

    # ========================================================
    # CHECK RESULTS
    # ========================================================

    if not temperatures:

        return {
            "success": False,

            "error":
                "Open-Meteo returned no usable "
                "temperature values.",

            "points":
                point_results
        }

    # ========================================================
    # ROUTE STATISTICS
    # ========================================================

    average_temperature = (
        sum(temperatures)
        / len(temperatures)
    )

    minimum_temperature = min(
        temperatures
    )

    maximum_temperature = max(
        temperatures
    )

    # ========================================================
    # APPARENT TEMPERATURE
    # ========================================================

    if apparent_temperatures:

        average_apparent_temperature = (
            sum(apparent_temperatures)
            / len(apparent_temperatures)
        )

    else:

        average_apparent_temperature = None

    # ========================================================
    # HEAT EXPOSURE
    # ========================================================

    heat_exposure = calculate_heat_exposure(
        average_temperature
    )

    # ========================================================
    # COOL SCORE
    # ========================================================

    cool_score = calculate_cool_score(
        average_temperature
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    final_result = {

        "success": True,

        "average_temperature":
            round(
                average_temperature,
                2
            ),

        "minimum_temperature":
            round(
                minimum_temperature,
                2
            ),

        "maximum_temperature":
            round(
                maximum_temperature,
                2
            ),

        "average_apparent_temperature":
            (
                round(
                    average_apparent_temperature,
                    2
                )
                if average_apparent_temperature
                is not None
                else None
            ),

        "heat_exposure":
            heat_exposure,

        "cool_score":
            cool_score,

        "sample_count":
            len(temperatures),

        "points":
            point_results
    }

    # ========================================================
    # LOG
    # ========================================================

    print("\n")
    print("=" * 60)
    print("CLIMATE ANALYSIS COMPLETE")
    print("=" * 60)

    print(
        f"Average temperature: "
        f"{final_result['average_temperature']}°C"
    )

    print(
        f"Minimum temperature: "
        f"{final_result['minimum_temperature']}°C"
    )

    print(
        f"Maximum temperature: "
        f"{final_result['maximum_temperature']}°C"
    )

    print(
        f"Heat exposure: "
        f"{heat_exposure}"
    )

    print(
        f"Cool Score: "
        f"{cool_score}/100"
    )

    print(
        f"Successful points: "
        f"{len(temperatures)}/{len(points)}"
    )

    print("=" * 60)

    return final_result


# ============================================================
# HEAT EXPOSURE
# ============================================================

def calculate_heat_exposure(
    temperature_celsius
):

    if temperature_celsius is None:
        return "Unknown"

    if temperature_celsius < 20:
        return "Low"

    if temperature_celsius < 25:
        return "Moderate"

    if temperature_celsius < 30:
        return "High"

    return "Very High"


# ============================================================
# COOL SCORE
# ============================================================

def calculate_cool_score(
    temperature_celsius
):

    if temperature_celsius is None:
        return 0

    # --------------------------------------------------------
    # Excellent temperature
    # --------------------------------------------------------

    if temperature_celsius <= 18:
        return 100

    # --------------------------------------------------------
    # Very hot
    # --------------------------------------------------------

    if temperature_celsius >= 40:
        return 0

    # --------------------------------------------------------
    # Linear score
    # --------------------------------------------------------

    score = (
        100
        -
        (
            temperature_celsius - 18
        )
        *
        (
            100 / 22
        )
    )

    score = max(
        0,
        min(
            100,
            score
        )
    )

    return round(
        score
    )


# ============================================================
# ROUTE COMPARISON
# ============================================================

def compare_routes(
    routes,
    prefer_cooler=True
):
    """
    Compare routes using travel time
    and climate comfort.

    AI weighting:

        70% climate
        30% travel time
    """

    if not routes:

        return {
            "fastest": None,
            "coolest": None,
            "ai_pick": None
        }

    # ========================================================
    # FASTEST
    # ========================================================

    fastest = min(
        routes,
        key=lambda route:
            route.get(
                "duration_min",
                float("inf")
            )
    )

    # ========================================================
    # ROUTES WITH CLIMATE DATA
    # ========================================================

    valid_routes = []

    for route in routes:

        climate = route.get(
            "climate",
            {}
        )

        if climate.get(
            "success",
            False
        ):

            valid_routes.append(
                route
            )

    # ========================================================
    # NO CLIMATE DATA
    # ========================================================

    if not valid_routes:

        return {
            "fastest": fastest,
            "coolest": None,
            "ai_pick": fastest
        }

    # ========================================================
    # COOLEST
    # ========================================================

    coolest = max(
        valid_routes,
        key=lambda route:
            route["climate"].get(
                "cool_score",
                0
            )
    )

    # ========================================================
    # AI PICK
    # ========================================================

    if not prefer_cooler:

        for route in valid_routes:

            route["ai_score"] = 100

        ai_pick = fastest

        return {
            "fastest": fastest,
            "coolest": coolest,
            "ai_pick": ai_pick
        }

    # --------------------------------------------------------
    # Fastest valid route time
    # --------------------------------------------------------

    fastest_time = min(
        route["duration_min"]
        for route in valid_routes
    )

    # --------------------------------------------------------
    # Calculate combined score
    # --------------------------------------------------------

    for route in valid_routes:

        climate_score = (
            route["climate"]
            .get(
                "cool_score",
                0
            )
        )

        route_time = (
            route.get(
                "duration_min",
                0
            )
        )

        if route_time <= 0:

            time_score = 100

        else:

            time_score = (
                fastest_time
                / route_time
            ) * 100

        # ----------------------------------------------------
        # AI weighting
        # ----------------------------------------------------
        #
        # Climate = 70%
        # Time    = 30%
        #

        ai_score = (
            climate_score * 0.70
            +
            time_score * 0.30
        )

        route["ai_score"] = round(
            ai_score
        )

    # ========================================================
    # SELECT HIGHEST SCORE
    # ========================================================

    ai_pick = max(
        valid_routes,
        key=lambda route:
            route.get(
                "ai_score",
                0
            )
    )

    # ========================================================
    # RETURN
    # ========================================================

    return {
        "fastest": fastest,
        "coolest": coolest,
        "ai_pick": ai_pick
    }
