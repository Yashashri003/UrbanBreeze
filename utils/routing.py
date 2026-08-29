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

OSRM_BASE_URL = (
    "https://router.project-osrm.org"
)


# ============================================================
# SEARCH CALIFORNIA LOCATIONS
# ============================================================

def search_california_locations(query):
    """
    Search for addresses, streets, cities and
    landmarks in California.

    Returns a list of matching locations.
    """

    if not query or len(query.strip()) < 3:
        return []


    search_query = (
        f"{query}, California, USA"
    )


    params = {

        "q": search_query,

        "format": "jsonv2",

        "limit": 5,

        "addressdetails": 1,

        "countrycodes": "us",

        # California approximate bounding box
        #
        # west, south, east, north
        "viewbox": (
            "-124.5,32.5,"
            "-114.0,42.1"
        ),

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

            address = result.get(
                "address",
                {}
            )


            # ----------------------------------------
            # Make sure result is California
            # ----------------------------------------

            state = address.get(
                "state",
                ""
            )


            if state.lower() != "california":

                continue


            # ----------------------------------------
            # Store location
            # ----------------------------------------

            locations.append({

                "display_name":
                    result.get(
                        "display_name",
                        query
                    ),

                "lat":
                    float(result["lat"]),

                "lon":
                    float(result["lon"]),

                "address":
                    address,

                "osm_type":
                    result.get(
                        "osm_type"
                    ),

                "osm_id":
                    result.get(
                        "osm_id"
                    )
            })


        return locations


    except requests.RequestException as error:

        print(
            "Location search error:",
            error
        )

        return []


# ============================================================
# GEOCODE LOCATION
# ============================================================

def geocode_location(location):
    """
    Convert a location name into coordinates.
    """

    results = search_california_locations(
        location
    )


    if not results:

        return None


    result = results[0]


    return {

        "lat":
            result["lat"],

        "lon":
            result["lon"],

        "name":
            result["display_name"]
    }



# ============================================================
# DETERMINE OSRM PROFILE
# ============================================================

def get_osrm_profile(travel_mode):
    """
    The public OSRM demo server is primarily configured for car
    routing. Walking/cycling/EV profiles need a backend that
    actually provides those profiles.
    """
    return "car"


# ============================================================
# GEOMETRY HELPERS
# ============================================================

def _sample_geometry(coordinates, count=7):
    if not coordinates:
        return []

    if len(coordinates) <= count:
        return coordinates

    return [
        coordinates[
            round(i * (len(coordinates) - 1) / (count - 1))
        ]
        for i in range(count)
    ]


def routes_are_too_similar(route_a, route_b):
    """
    Reject routes that are effectively the same route.
    Geometry is checked in addition to time/distance.
    """

    distance_a = route_a.get("distance_km", 0)
    distance_b = route_b.get("distance_km", 0)
    duration_a = route_a.get("duration_min", 0)
    duration_b = route_b.get("duration_min", 0)

    if distance_a and duration_a:
        distance_difference = abs(distance_a - distance_b) / distance_a
        duration_difference = abs(duration_a - duration_b) / duration_a

        if distance_difference < 0.015 and duration_difference < 0.02:
            return True

    coords_a = route_a.get("geometry", {}).get("coordinates", [])
    coords_b = route_b.get("geometry", {}).get("coordinates", [])

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

    return (total_km / len(a)) < 0.15


# ============================================================
# PROCESS OSRM ROUTE
# ============================================================

def process_osrm_route(route, route_number, strategy="osrm"):
    return {
        "route_number": route_number,
        "distance_km": round(route.get("distance", 0) / 1000.0, 2),
        "duration_min": round(route.get("duration", 0) / 60.0, 1),
        "geometry": route.get("geometry"),
        "steps": route.get("legs", []),
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
    url = (
        f"{OSRM_BASE_URL}/route/v1/{profile}/{coordinates}"
    )

    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "true",
        "alternatives": "true" if alternatives else "false",
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
    strength=0.035
):
    """
    Create a moderate waypoint to the left/right of the direct
    route. OSRM then calculates a real road route through it.

    This gives UrbanBreeze genuine alternative geometries instead
    of drawing fake/duplicated lines.
    """

    mid_lat = (start_lat + destination_lat) / 2.0
    mid_lon = (start_lon + destination_lon) / 2.0

    dx = destination_lon - start_lon
    dy = destination_lat - start_lat
    length = math.hypot(dx, dy)

    if length < 0.0001:
        return mid_lat, mid_lon

    # Perpendicular direction.
    perpendicular_x = -dy / length
    perpendicular_y = dx / length

    # Scale the offset down for short trips.
    direct_distance_km = math.hypot(
        dx * 85.0,
        dy * 111.0
    )

    adaptive_strength = min(
        strength,
        max(0.008, direct_distance_km / 2500.0)
    )

    waypoint_lon = (
        mid_lon
        + side * perpendicular_x * adaptive_strength
    )

    waypoint_lat = (
        mid_lat
        + side * perpendicular_y * adaptive_strength
    )

    return waypoint_lat, waypoint_lon


# ============================================================
# ADD UNIQUE ROUTE
# ============================================================

def _add_unique_route(routes, raw_route, strategy):
    processed = process_osrm_route(
        raw_route,
        len(routes) + 1,
        strategy
    )

    if not processed.get("geometry"):
        return False

    for existing in routes:
        if routes_are_too_similar(processed, existing):
            return False

    routes.append(processed)
    return True


# ============================================================
# GET MULTIPLE ROUTES
# ============================================================

def get_routes(
    start,
    destination,
    travel_mode="🚶 Walk"
):
    """
    Generate up to 3 real route candidates.

    Candidate sources:
      1. Normal OSRM route + OSRM alternatives.
      2. Real OSRM route through a left-side waypoint.
      3. Real OSRM route through a right-side waypoint.

    If OSRM cannot produce 3 genuinely different routes, the
    function returns the number it can actually produce rather
    than inventing route geometries.

    This function does NOT decide Fastest/Coolest/AI Pick.
    Climate scoring does that after route generation.
    """

    profile = get_osrm_profile(travel_mode)

    start_lon = float(start["lon"])
    start_lat = float(start["lat"])
    destination_lon = float(destination["lon"])
    destination_lat = float(destination["lat"])

    direct_coordinates = (
        f"{start_lon},{start_lat};"
        f"{destination_lon},{destination_lat}"
    )

    print("\n" + "=" * 60)
    print("URBANBREEZE ROUTE GENERATION")
    print("=" * 60)
    print("Travel mode:", travel_mode)
    print("OSRM profile:", profile)
    print("Requesting up to 3 real route candidates...")
    print("=" * 60)

    routes = []

    # --------------------------------------------------------
    # 1. Normal route + OSRM alternatives
    # --------------------------------------------------------

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
        print("OSRM direct request error:", error)

    # --------------------------------------------------------
    # 2. Left detour candidate
    # --------------------------------------------------------

    if len(routes) < 3:

        waypoint_lat, waypoint_lon = _build_detour_waypoint(
            start_lat,
            start_lon,
            destination_lat,
            destination_lon,
            side=-1,
            strength=0.035
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
                    "detour_left"
                ):
                    break

        except requests.RequestException as error:
            print("OSRM left-detour error:", error)

    # --------------------------------------------------------
    # 3. Right detour candidate
    # --------------------------------------------------------

    if len(routes) < 3:

        waypoint_lat, waypoint_lon = _build_detour_waypoint(
            start_lat,
            start_lon,
            destination_lat,
            destination_lon,
            side=1,
            strength=0.035
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
                    "detour_right"
                ):
                    break

        except requests.RequestException as error:
            print("OSRM right-detour error:", error)

    # --------------------------------------------------------
    # Stronger detours only if needed
    # --------------------------------------------------------

    if len(routes) < 3:

        for side, strategy in [
            (-1, "wide_detour_left"),
            (1, "wide_detour_right")
        ]:

            if len(routes) >= 3:
                break

            waypoint_lat, waypoint_lon = _build_detour_waypoint(
                start_lat,
                start_lon,
                destination_lat,
                destination_lon,
                side=side,
                strength=0.055
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
                        break

            except requests.RequestException as error:
                print(
                    f"OSRM {strategy} error:",
                    error
                )

    # --------------------------------------------------------
    # Sort by travel time
    # --------------------------------------------------------

    routes.sort(
        key=lambda route: route["duration_min"]
    )

    for index, route in enumerate(routes):
        route["route_number"] = index + 1

    # This is only a candidate label. The final dashboard labels
    # should be assigned after climate analysis.
    if routes:
        routes[0]["route_label"] = "Fastest Candidate"

    # --------------------------------------------------------
    # Debug
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print(
        f"URBANBREEZE FOUND {len(routes)} "
        "UNIQUE ROUTE CANDIDATE(S)"
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
