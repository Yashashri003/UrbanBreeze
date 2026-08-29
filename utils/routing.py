import math
import requests


# ============================================================
# NOMINATIM SETTINGS
# ============================================================

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

HEADERS = {
    "User-Agent": "UrbanBreeze-Hackathon/1.0"
}


# ============================================================
# OSRM SETTINGS
# ============================================================

OSRM_SERVERS = {
    "car":  ("https://routing.openstreetmap.de/routed-car", "driving"),
    "bike": ("https://routing.openstreetmap.de/routed-bike", "bike"),
    "foot": ("https://routing.openstreetmap.de/routed-foot", "foot"),
}


# ============================================================
# SEARCH CALIFORNIA LOCATIONS
# ============================================================

def search_california_locations(query):
    """
    Search for addresses, streets, cities and landmarks
    in California.

    Returns a list of matching locations.
    """

    if not query or len(query.strip()) < 3:
        return []

    search_query = f"{query}, California, USA"

    params = {
        "q": search_query,
        "format": "jsonv2",
        "limit": 5,
        "addressdetails": 1,
        "countrycodes": "us",

        # California approximate bounding box:
        # west, south, east, north
        "viewbox": "-124.5,32.5,-114.0,42.1",
        "bounded": 1
    }

    try:
        response = requests.get(
            NOMINATIM_URL,
            params=params,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        results = response.json()

        locations = []

        for result in results:

            address = result.get("address", {})

            state = address.get("state", "")

            if state.lower() != "california":
                continue

            locations.append({
                "display_name": result.get(
                    "display_name",
                    query
                ),

                "lat": float(result["lat"]),
                "lon": float(result["lon"]),

                "address": address,

                "osm_type": result.get("osm_type"),
                "osm_id": result.get("osm_id")
            })

        return locations

    except requests.RequestException as error:

        print("Location search error:", error)

        return []


# ============================================================
# GEOCODE LOCATION
# ============================================================

def geocode_location(location):
    """
    Convert a location name into coordinates.
    """

    results = search_california_locations(location)

    if not results:
        return None

    result = results[0]

    return {
        "lat": result["lat"],
        "lon": result["lon"],
        "name": result["display_name"]
    }


# ============================================================
# DETERMINE OSRM PROFILE
# ============================================================

def get_osrm_profile(travel_mode):
    mode = travel_mode.lower()
    if "walk" in mode or "foot" in mode:
        return "foot"
    if "bike" in mode or "cycle" in mode or "cyclist" in mode:
        return "bike"
    return "car"


# ============================================================
# GEOMETRY HELPERS
# ============================================================

def _sample_geometry(coordinates, count=7):
    """
    Reduce a route geometry to a small number of
    representative points for similarity checking.
    """

    if not coordinates:
        return []

    if len(coordinates) <= count:
        return coordinates

    return [
        coordinates[
            round(
                i * (len(coordinates) - 1)
                / (count - 1)
            )
        ]
        for i in range(count)
    ]


def routes_are_too_similar(route_a, route_b):
    """
    Determine whether two routes are effectively
    the same route.

    Both travel statistics and geometry are checked.
    """

    distance_a = route_a.get("distance_km", 0)
    distance_b = route_b.get("distance_km", 0)

    duration_a = route_a.get("duration_min", 0)
    duration_b = route_b.get("duration_min", 0)

    # --------------------------------------------------------
    # Distance/time similarity
    # --------------------------------------------------------

    if distance_a and duration_a:

        distance_difference = (
            abs(distance_a - distance_b)
            / distance_a
        )

        duration_difference = (
            abs(duration_a - duration_b)
            / duration_a
        )

        if (
            distance_difference < 0.015
            and
            duration_difference < 0.02
        ):
            return True

    # --------------------------------------------------------
    # Geometry similarity
    # --------------------------------------------------------

    coords_a = route_a.get(
        "geometry",
        {}
    ).get(
        "coordinates",
        []
    )

    coords_b = route_b.get(
        "geometry",
        {}
    ).get(
        "coordinates",
        []
    )

    if not coords_a or not coords_b:
        return False

    a = _sample_geometry(coords_a)
    b = _sample_geometry(coords_b)

    if len(a) != len(b):
        return False

    total_km = 0.0

    for p1, p2 in zip(a, b):

        lon1, lat1 = p1
        lon2, lat2 = p2

        total_km += math.hypot(
            (lon1 - lon2) * 85.0,
            (lat1 - lat2) * 111.0
        )

    average_difference = (
        total_km / len(a)
    )

    return average_difference < 0.15


# ============================================================
# PROCESS OSRM ROUTE
# ============================================================

def process_osrm_route(
    route,
    route_number,
    strategy="osrm"
):
    """
    Convert raw OSRM route data into the common
    UrbanBreeze route format.
    """

    return {
        "route_number": route_number,

        "distance_km": round(
            route.get("distance", 0)
            / 1000.0,
            2
        ),

        "duration_min": round(
            route.get("duration", 0)
            / 60.0,
            1
        ),

        "geometry": route.get("geometry"),

        "steps": route.get(
            "legs",
            []
        ),

        "strategy": strategy,

        # Filled later by climate/scoring code.
        "climate": None,
        "climate_score": None,
        "ai_score": None,
        "route_label": None,
    }


# ============================================================
# LOW-LEVEL OSRM REQUEST
# ============================================================

def _request_osrm_route(profile, coordinates, alternatives=True):
    base_url, path_profile = OSRM_SERVERS[profile]

    url = f"{base_url}/route/v1/{path_profile}/{coordinates}"

    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "true",
        "alternatives": "true" if alternatives else "false"
    }

    response = requests.get(url, params=params, timeout=25)
    response.raise_for_status()
    data = response.json()

    if data.get("code") != "Ok":
        return []

    return data.get("routes", [])


# ============================================================
# DETOUR WAYPOINT
# ============================================================

def _build_detour_waypoint(
    start_lat,
    start_lon,
    destination_lat,
    destination_lon,
    side,
    strength
):
    """
    Build a controlled waypoint to one side of the
    direct start → destination direction.

    OSRM then calculates a REAL road route through
    this waypoint.

    This does NOT draw a fake route.
    """

    mid_lat = (
        start_lat
        + destination_lat
    ) / 2.0

    mid_lon = (
        start_lon
        + destination_lon
    ) / 2.0

    dx = (
        destination_lon
        - start_lon
    )

    dy = (
        destination_lat
        - start_lat
    )

    length = math.hypot(
        dx,
        dy
    )

    if length < 0.0001:
        return (
            mid_lat,
            mid_lon
        )

    # --------------------------------------------------------
    # Perpendicular direction
    # --------------------------------------------------------

    perpendicular_x = (
        -dy / length
    )

    perpendicular_y = (
        dx / length
    )

    # --------------------------------------------------------
    # Estimate direct distance
    # --------------------------------------------------------

    direct_distance_km = math.hypot(
        dx * 85.0,
        dy * 111.0
    )

    # --------------------------------------------------------
    # Adaptive detour size
    # --------------------------------------------------------

    adaptive_strength = min(
        strength,
        max(
            0.008,
            direct_distance_km / 2500.0
        )
    )

    waypoint_lon = (
        mid_lon
        +
        side
        * perpendicular_x
        * adaptive_strength
    )

    waypoint_lat = (
        mid_lat
        +
        side
        * perpendicular_y
        * adaptive_strength
    )

    return (
        waypoint_lat,
        waypoint_lon
    )


# ============================================================
# ADD UNIQUE ROUTE
# ============================================================

def _add_unique_route(
    routes,
    raw_route,
    strategy
):
    """
    Process a raw OSRM route and add it only if
    it is genuinely different from existing routes.
    """

    processed = process_osrm_route(
        raw_route,
        len(routes) + 1,
        strategy
    )

    if not processed.get("geometry"):
        return False

    for existing in routes:

        if routes_are_too_similar(
            processed,
            existing
        ):
            return False

    routes.append(processed)

    return True


# ============================================================
# BUILD WAYPOINT ROUTE
# ============================================================

def _try_waypoint_route(
    routes,
    profile,
    start_lat,
    start_lon,
    destination_lat,
    destination_lon,
    side,
    strength,
    strategy
):
    """
    Try to generate one additional REAL road route
    through a waypoint.
    """

    waypoint_lat, waypoint_lon = (
        _build_detour_waypoint(
            start_lat,
            start_lon,
            destination_lat,
            destination_lon,
            side,
            strength
        )
    )

    coordinates = (
        f"{start_lon},{start_lat};"
        f"{waypoint_lon},{waypoint_lat};"
        f"{destination_lon},{destination_lat}"
    )

    try:

        raw_routes = _request_osrm_route(
            profile,
            coordinates,
            alternatives=False
        )

        for raw_route in raw_routes:

            if _add_unique_route(
                routes,
                raw_route,
                strategy
            ):
                return True

    except requests.RequestException as error:

        print(
            f"OSRM {strategy} error:",
            error
        )

    return False


# ============================================================
# GET MULTIPLE ROUTES
# ============================================================

def get_routes(
    start,
    destination,
    travel_mode="🚶 Walk"
):
    """
    Generate real route candidates between the
    same start and destination.

    Candidate generation order:

        1. Normal OSRM route
        2. OSRM alternative routes
        3. Moderate left-side route
        4. Moderate right-side route
        5. Wider left-side route
        6. Wider right-side route

    The function returns up to 3 genuinely different
    routes.

    IMPORTANT:
        This function does NOT decide:
            - Fastest
            - Coolest
            - AI Recommended

        Those decisions belong to climate/scoring code.
    """

    profile = get_osrm_profile(
        travel_mode
    )

    start_lon = float(
        start["lon"]
    )

    start_lat = float(
        start["lat"]
    )

    destination_lon = float(
        destination["lon"]
    )

    destination_lat = float(
        destination["lat"]
    )

    direct_coordinates = (
        f"{start_lon},{start_lat};"
        f"{destination_lon},{destination_lat}"
    )

    print("\n" + "=" * 60)
    print(
        "URBANBREEZE ROUTE GENERATION"
    )
    print("=" * 60)

    print(
        "Travel mode:",
        travel_mode
    )

    print(
        "OSRM profile:",
        profile
    )

    print(
        "Generating up to 3 "
        "genuinely different routes..."
    )

    print("=" * 60)

    routes = []

    # ========================================================
    # 1. NORMAL ROUTE + OSRM ALTERNATIVES
    # ========================================================

    try:

        raw_routes = _request_osrm_route(
            profile,
            direct_coordinates,
            alternatives=True
        )

        for raw_route in raw_routes:

            _add_unique_route(
                routes,
                raw_route,
                "osrm_alternative"
            )

            if len(routes) >= 3:
                break

    except requests.RequestException as error:

        print(
            "OSRM direct request error:",
            error
        )

    # ========================================================
    # 2. MODERATE LEFT DETOUR
    # ========================================================

    if len(routes) < 3:

        _try_waypoint_route(
            routes,
            profile,
            start_lat,
            start_lon,
            destination_lat,
            destination_lon,
            side=-1,
            strength=0.025,
            strategy="detour_left"
        )

    # ========================================================
    # 3. MODERATE RIGHT DETOUR
    # ========================================================

    if len(routes) < 3:

        _try_waypoint_route(
            routes,
            profile,
            start_lat,
            start_lon,
            destination_lat,
            destination_lon,
            side=1,
            strength=0.025,
            strategy="detour_right"
        )

    # ========================================================
    # 4. WIDER LEFT DETOUR
    # ========================================================

    if len(routes) < 3:

        _try_waypoint_route(
            routes,
            profile,
            start_lat,
            start_lon,
            destination_lat,
            destination_lon,
            side=-1,
            strength=0.045,
            strategy="wide_detour_left"
        )

    # ========================================================
    # 5. WIDER RIGHT DETOUR
    # ========================================================

    if len(routes) < 3:

        _try_waypoint_route(
            routes,
            profile,
            start_lat,
            start_lon,
            destination_lat,
            destination_lon,
            side=1,
            strength=0.045,
            strategy="wide_detour_right"
        )

    # ========================================================
    # SORT BY TRAVEL TIME
    # ========================================================

    routes.sort(
        key=lambda route:
        route["duration_min"]
    )

    # ========================================================
    # REASSIGN ROUTE NUMBERS
    # ========================================================

    for index, route in enumerate(
        routes
    ):

        route["route_number"] = (
            index + 1
        )

    # ========================================================
    # DEBUG INFORMATION
    # ========================================================

    print("\n" + "=" * 60)

    print(
        f"URBANBREEZE FOUND "
        f"{len(routes)} "
        f"UNIQUE ROUTE CANDIDATE(S)"
    )

    print("=" * 60)

    for route in routes:

        print(
            f"Route {route['route_number']}: "
            f"{route['duration_min']} min | "
            f"{route['distance_km']} km | "
            f"{route['strategy']}"
        )

    print("=" * 60)

    return routes