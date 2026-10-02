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
    "car": ("https://routing.openstreetmap.de/routed-car", "driving"),
    "bike": ("https://routing.openstreetmap.de/routed-bike", "bike"),
    "foot": ("https://routing.openstreetmap.de/routed-foot", "foot"),
}


# ============================================================
# GLOBAL LOCATION SEARCH
# ============================================================

def search_locations(query):
    """Search globally for cities, areas, streets and landmarks."""

    if not query or len(query.strip()) < 3:
        return []

    params = {
        "q": query.strip(),
        "format": "jsonv2",
        "limit": 5,
        "addressdetails": 1,
    }

    try:
        response = requests.get(
            NOMINATIM_URL,
            params=params,
            headers=HEADERS,
            timeout=10,
        )

        response.raise_for_status()

        results = response.json()
        locations = []

        for result in results:
            try:
                lat = float(result["lat"])
                lon = float(result["lon"])
            except (KeyError, TypeError, ValueError):
                continue

            locations.append({
                "display_name": result.get(
                    "display_name",
                    query.strip()
                ),
                "lat": lat,
                "lon": lon,
                "address": result.get("address", {}),
                "osm_type": result.get("osm_type"),
                "osm_id": result.get("osm_id"),
            })

        return locations

    except requests.RequestException as error:
        print("Location search error:", error)
        return []


# Backward-compatible function name
def search_california_locations(query):
    return search_locations(query)


# ============================================================
# GEOCODE LOCATION
# ============================================================

def geocode_location(location):
    """Convert a location name into coordinates."""

    results = search_locations(location)

    if not results:
        return None

    result = results[0]

    return {
        "lat": result["lat"],
        "lon": result["lon"],
        "name": result["display_name"],
    }


# ============================================================
# OSRM PROFILE
# ============================================================

def get_osrm_profile(travel_mode):
    mode = str(travel_mode).lower()

    if "walk" in mode or "foot" in mode:
        return "foot"

    if "bike" in mode or "cycle" in mode or "cyclist" in mode:
        return "bike"

    return "car"


# ============================================================
# GEOMETRY HELPERS
# ============================================================

def _sample_geometry(coordinates, count=12):
    """Sample a route geometry at evenly spaced positions."""

    if not coordinates:
        return []

    if len(coordinates) <= count:
        return coordinates

    if count <= 1:
        return [coordinates[len(coordinates) // 2]]

    return [
        coordinates[
            round(
                i * (len(coordinates) - 1)
                / (count - 1)
            )
        ]
        for i in range(count)
    ]


def _average_geometry_difference(route_a, route_b):
    """
    Approximate average separation between two route geometries.

    Routes are sampled at the same normalized positions.
    """

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
        return float("inf")

    a = _sample_geometry(coords_a, 12)
    b = _sample_geometry(coords_b, 12)

    count = min(len(a), len(b))

    if count == 0:
        return float("inf")

    total_km = 0.0

    for p1, p2 in zip(a[:count], b[:count]):

        lon1, lat1 = p1
        lon2, lat2 = p2

        total_km += math.hypot(
            (lon1 - lon2) * 85.0,
            (lat1 - lat2) * 111.0
        )

    return total_km / count


def routes_are_too_similar(route_a, route_b):
    """
    Reject routes that are effectively duplicates.

    Uses both:
        - travel statistics
        - route geometry
    """

    distance_a = route_a.get(
        "distance_km",
        0
    )

    distance_b = route_b.get(
        "distance_km",
        0
    )

    duration_a = route_a.get(
        "duration_min",
        0
    )

    duration_b = route_b.get(
        "duration_min",
        0
    )

    # --------------------------------------------------------
    # Distance/time similarity
    # --------------------------------------------------------

    if distance_a > 0 and duration_a > 0:

        distance_difference = (
            abs(distance_a - distance_b)
            / distance_a
        )

        duration_difference = (
            abs(duration_a - duration_b)
            / duration_a
        )

        if (
            distance_difference < 0.01
            and
            duration_difference < 0.015
        ):
            return True

    # --------------------------------------------------------
    # Geometry similarity
    # --------------------------------------------------------

    average_difference = _average_geometry_difference(
        route_a,
        route_b
    )

    # Less than approximately 300 m average separation
    # is considered the same corridor.
    return average_difference < 0.30


# ============================================================
# PROCESS OSRM ROUTE
# ============================================================

def process_osrm_route(
    route,
    route_number,
    strategy="osrm"
):

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

        "geometry": route.get(
            "geometry"
        ),

        "steps": route.get(
            "legs",
            []
        ),

        "strategy": strategy,

        "climate": None,
        "climate_score": None,
        "ai_score": None,
        "route_label": None,
    }


# ============================================================
# LOW-LEVEL OSRM REQUEST
# ============================================================

def _request_osrm_route(
    profile,
    coordinates,
    alternatives=True
):

    base_url, path_profile = OSRM_SERVERS[
        profile
    ]

    url = (
        f"{base_url}/route/v1/"
        f"{path_profile}/{coordinates}"
    )

    params = {

        "overview": "full",

        "geometries": "geojson",

        "steps": "true",

        "alternatives":
            "true"
            if alternatives
            else "false",
    }

    response = requests.get(
        url,
        params=params,
        timeout=25
    )

    response.raise_for_status()

    data = response.json()

    if data.get("code") != "Ok":
        return []

    return data.get(
        "routes",
        []
    )


# ============================================================
# WAYPOINT GENERATION
# ============================================================

def _build_detour_waypoint(
    start_lat,
    start_lon,
    destination_lat,
    destination_lon,
    side,
    fraction=0.50,
    strength=0.035
):
    """
    Create a waypoint left/right of the direct route.

    fraction:
        Position of waypoint along the journey.

    strength:
        How far the waypoint is pushed sideways.
    """

    # --------------------------------------------------------
    # Position along direct route
    # --------------------------------------------------------

    lat = (
        start_lat
        +
        (
            destination_lat
            - start_lat
        )
        * fraction
    )

    lon = (
        start_lon
        +
        (
            destination_lon
            - start_lon
        )
        * fraction
    )

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
        return lat, lon

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
        lon
        +
        side
        * perpendicular_x
        * adaptive_strength
    )

    waypoint_lat = (
        lat
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

    processed = process_osrm_route(
        raw_route,
        len(routes) + 1,
        strategy
    )

    if not processed.get(
        "geometry"
    ):
        return False

    for existing in routes:

        if routes_are_too_similar(
            processed,
            existing
        ):
            return False

    routes.append(
        processed
    )

    return True


# ============================================================
# WAYPOINT ROUTE
# ============================================================

def _try_waypoint_route(
    routes,
    profile,
    start_lat,
    start_lon,
    destination_lat,
    destination_lon,
    side,
    fraction,
    strength,
    strategy
):

    waypoint_lat, waypoint_lon = (
        _build_detour_waypoint(
            start_lat,
            start_lon,
            destination_lat,
            destination_lon,
            side,
            fraction,
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
    Generate up to 3 genuinely different
    real-road routes.

    We intentionally generate more candidates
    than we need and keep only routes that are
    geometrically different.
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

    print(
        "\n" + "=" * 60
    )

    print(
        "URBANBREEZE ROUTE GENERATION"
    )

    print(
        "=" * 60
    )

    print(
        "Travel mode:",
        travel_mode
    )

    print(
        "OSRM profile:",
        profile
    )

    print(
        "Searching for distinct route corridors..."
    )

    print(
        "=" * 60
    )

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
    # 2. DIFFERENT CORRIDOR CANDIDATES
    # ========================================================

    # Instead of always creating a detour around
    # one midpoint, we try several positions.

    waypoint_candidates = [

        # fraction, side, strength, strategy

        (
            0.35,
            -1,
            0.045,
            "detour_left_35"
        ),

        (
            0.35,
            1,
            0.045,
            "detour_right_35"
        ),

        (
            0.50,
            -1,
            0.055,
            "detour_left_50"
        ),

        (
            0.50,
            1,
            0.055,
            "detour_right_50"
        ),

        (
            0.65,
            -1,
            0.045,
            "detour_left_65"
        ),

        (
            0.65,
            1,
            0.045,
            "detour_right_65"
        ),

        (
            0.50,
            -1,
            0.075,
            "wide_left_50"
        ),

        (
            0.50,
            1,
            0.075,
            "wide_right_50"
        ),
    ]

    for (
        fraction,
        side,
        strength,
        strategy
    ) in waypoint_candidates:

        if len(routes) >= 3:
            break

        _try_waypoint_route(

            routes,

            profile,

            start_lat,
            start_lon,

            destination_lat,
            destination_lon,

            side=side,

            fraction=fraction,

            strength=strength,

            strategy=strategy
        )

    # ========================================================
    # SORT BY TIME
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

    print(
        "\n" + "=" * 60
    )

    print(
        f"URBANBREEZE FOUND "
        f"{len(routes)} "
        f"UNIQUE ROUTE CANDIDATE(S)"
    )

    print(
        "=" * 60
    )

    for route in routes:

        print(
            f"Route "
            f"{route['route_number']}: "
            f"{route['duration_min']} min | "
            f"{route['distance_km']} km | "
            f"{route['strategy']}"
        )

    # --------------------------------------------------------
    # Show actual route separation in terminal
    # --------------------------------------------------------

    for i in range(
        len(routes)
    ):

        for j in range(
            i + 1,
            len(routes)
        ):

            difference = (
                _average_geometry_difference(
                    routes[i],
                    routes[j]
                )
            )

            print(
                f"Route "
                f"{routes[i]['route_number']} "
                f"↔ "
                f"Route "
                f"{routes[j]['route_number']}: "
                f"{difference:.2f} km "
                f"average separation"
            )

    print(
        "=" * 60
    )

    return routes
