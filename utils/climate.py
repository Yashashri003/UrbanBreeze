from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.fortyguard import (
    get_temperature,
    is_california_coordinate
)


# ============================================================
# ROUTE SAMPLING
# ============================================================

def sample_route_points(
    geometry,
    number_of_points=5
):
    """
    Select evenly distributed points from an OSRM route.

    OSRM format:
        [longitude, latitude]

    Returned format:
        {
            "lat": latitude,
            "lon": longitude
        }
    """

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

        lon = float(point[0])
        lat = float(point[1])

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

        for i in range(
            number_of_points
        ):

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


        # ----------------------------------------------------
        # California safety check
        # ----------------------------------------------------

        if not is_california_coordinate(
            lat,
            lon
        ):
            continue


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
# SINGLE POINT FORTYGUARD ANALYSIS
# ============================================================

def analyze_temperature_point(
    index,
    point
):
    """
    Analyze one route point using FortyGuard.

    This function is intentionally separated from
    analyze_route_temperature() so multiple points
    can be processed concurrently.
    """

    latitude = point["lat"]
    longitude = point["lon"]


    # --------------------------------------------------------
    # California check
    # --------------------------------------------------------

    if not is_california_coordinate(
        latitude,
        longitude
    ):

        return {
            "index": index,
            "lat": latitude,
            "lon": longitude,
            "success": False,
            "error": (
                "Coordinate is outside "
                "California."
            )
        }


    # --------------------------------------------------------
    # FortyGuard
    # --------------------------------------------------------

    try:

        print(
            f"\n🌡️ FortyGuard point {index + 1}"
            f" started:"
        )

        print(
            f"   Latitude: {latitude}"
        )

        print(
            f"   Longitude: {longitude}"
        )


        result = get_temperature(
            latitude,
            longitude
        )


        print(
            f"🌡️ FortyGuard point {index + 1}"
            f" finished."
        )


    except Exception as error:

        print(
            f"\nFORTYGUARD ERROR "
            f"(point {index + 1})"
        )

        print(
            f"Error: {repr(error)}"
        )


        return {
            "index": index,
            "lat": latitude,
            "lon": longitude,
            "success": False,
            "error": str(error)
        }


    # --------------------------------------------------------
    # FortyGuard failure
    # --------------------------------------------------------

    if not result.get(
        "success",
        False
    ):

        return {
            "index": index,
            "lat": latitude,
            "lon": longitude,
            "success": False,
            "error":
                result.get(
                    "error",
                    "FortyGuard request failed."
                )
        }


    # --------------------------------------------------------
    # Extract temperature
    # --------------------------------------------------------

    temperature = clean_temperature(
        result.get(
            "temperature"
        )
    )


    minimum = clean_temperature(
        result.get(
            "minimum"
        )
    )


    maximum = clean_temperature(
        result.get(
            "maximum"
        )
    )


    # --------------------------------------------------------
    # Build result
    # --------------------------------------------------------

    return {
        "index": index,
        "lat": latitude,
        "lon": longitude,
        "success": True,
        "temperature": temperature,
        "minimum": minimum,
        "maximum": maximum,
        "activity_id":
            result.get(
                "activity_id"
            )
    }


# ============================================================
# ROUTE TEMPERATURE ANALYSIS
# ============================================================

def analyze_route_temperature(
    route,
    number_of_points=5
):
    """
    Analyze temperature along a route.

    Five points are sampled by default.

    IMPORTANT:
    The five FortyGuard requests are processed
    concurrently instead of sequentially.

    The FortyGuard cache is still respected inside
    get_temperature(), so cached points do not
    create new API requests.
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
                "No valid California points "
                "were found on this route."
        }


    print("\n")
    print("=" * 60)
    print(
        f"CLIMATE ANALYSIS "
        f"→ {len(points)} POINTS"
    )
    print("=" * 60)

    print(
        "FortyGuard requests will run "
        "concurrently."
    )

    print("=" * 60)


    # ========================================================
    # RESULTS
    # ========================================================

    temperatures = []

    point_results = []


    # ========================================================
    # PARALLEL FORTYGUARD REQUESTS
    # ========================================================

    # We keep the number of workers equal to the
    # number of sampled points, but never more than 5.
    #
    # This means:
    #
    # OLD:
    #
    # Point 1 → wait
    # Point 2 → wait
    # Point 3 → wait
    # Point 4 → wait
    # Point 5 → wait
    #
    # NEW:
    #
    # Point 1 ─┐
    # Point 2 ─┤
    # Point 3 ─┼→ FortyGuard concurrently
    # Point 4 ─┤
    # Point 5 ─┘

    max_workers = min(
        len(points),
        5
    )


    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        future_to_index = {}


        for index, point in enumerate(
            points
        ):

            future = executor.submit(
                analyze_temperature_point,
                index,
                point
            )

            future_to_index[
                future
            ] = index


        # ----------------------------------------------------
        # Collect completed requests
        # ----------------------------------------------------

        completed_results = []


        for future in as_completed(
            future_to_index
        ):

            index = future_to_index[
                future
            ]


            try:

                result = future.result()

            except Exception as error:

                point = points[index]

                result = {
                    "index": index,
                    "lat": point["lat"],
                    "lon": point["lon"],
                    "success": False,
                    "error": str(error)
                }


            completed_results.append(
                result
            )


    # ========================================================
    # RESTORE ROUTE ORDER
    # ========================================================

    completed_results.sort(
        key=lambda item:
            item["index"]
    )


    # ========================================================
    # PROCESS RESULTS
    # ========================================================

    for result in completed_results:

        point_results.append(
            result
        )


        if result.get(
            "success",
            False
        ):

            temperature = clean_temperature(
                result.get(
                    "temperature"
                )
            )


            if temperature is not None:

                temperatures.append(
                    temperature
                )


    # ========================================================
    # CHECK RESULTS
    # ========================================================

    if not temperatures:

        return {
            "success": False,

            "error":
                "FortyGuard returned no usable "
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

        "heat_exposure":
            heat_exposure,

        "cool_score":
            cool_score,

        "sample_count":
            len(temperatures),

        "points":
            point_results
    }


    print("\n")
    print("=" * 60)
    print("CLIMATE ANALYSIS COMPLETE")
    print("=" * 60)

    print(
        f"Average: "
        f"{final_result['average_temperature']}°C"
    )

    print(
        f"Minimum: "
        f"{final_result['minimum_temperature']}°C"
    )

    print(
        f"Maximum: "
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
            route["duration_min"]
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
            route["climate"]["cool_score"]
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
            ["cool_score"]
        )


        route_time = (
            route["duration_min"]
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