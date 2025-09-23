import re
from typing import Optional, Tuple, List
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from database.postgres import run_query


def _parse_latlon_ranges(sql: str) -> Optional[Tuple[float, float, float, float]]:
    """Return (lat_min, lat_max, lon_min, lon_max) if found, else None."""
    lat_pat = r"latitude\s+BETWEEN\s*([+-]?\d+(?:\.\d+)?)\s+AND\s*([+-]?\d+(?:\.\d+)?)"
    lon_pat = r"longitude\s+BETWEEN\s*([+-]?\d+(?:\.\d+)?)\s+AND\s*([+-]?\d+(?:\.\d+)?)"

    lat_m = re.search(lat_pat, sql, flags=re.IGNORECASE)
    lon_m = re.search(lon_pat, sql, flags=re.IGNORECASE)

    if not lat_m or not lon_m:
        return None

    lat_min, lat_max = map(float, lat_m.groups())
    lon_min, lon_max = map(float, lon_m.groups())

    # normalize
    if lat_min > lat_max:
        lat_min, lat_max = lat_max, lat_min
    if lon_min > lon_max:
        lon_min, lon_max = lon_max, lon_min

    return lat_min, lat_max, lon_min, lon_max


def _extract_table_and_where(sql: str) -> Tuple[Optional[str], str]:
    """Extract first table after FROM (simple heuristic) and the WHERE clause body (if any)."""
    from_m = re.search(r"FROM\s+([^\s;]+)", sql, flags=re.IGNORECASE)
    table = from_m.group(1) if from_m else None

    where_m = re.search(r"WHERE\s+(.*?)(?:GROUP\s+BY|ORDER\s+BY|LIMIT\b|;|$)",
                        sql, flags=re.IGNORECASE | re.DOTALL)
    where_clause = where_m.group(1).strip() if where_m else ""
    return table, where_clause


def _clean_leftover_where(where_clause: str) -> List[str]:
    """
    Remove latitude/longitude BETWEEN clauses from the WHERE text and
    return a list of remaining conditions split by AND.
    NOTE: This preserves simple AND-separated conditions. Complex boolean logic (OR, nested parentheses)
    may not be reconstructed perfectly.
    """
    if not where_clause:
        return []

    # remove latitude/longitude between patterns
    without_box = re.sub(
        r"latitude\s+BETWEEN\s*[+-]?\d+(?:\.\d+)?\s+AND\s*[+-]?\d+(?:\.\d+)?",
        "",
        where_clause, flags=re.IGNORECASE)
    without_box = re.sub(
        r"longitude\s+BETWEEN\s*[+-]?\d+(?:\.\d+)?\s+AND\s*[+-]?\d+(?:\.\d+)?",
        "",
        without_box, flags=re.IGNORECASE)

    # split on AND and keep non-empty parts (trim whitespace)
    parts = [p.strip() for p in re.split(r"\bAND\b", without_box, flags=re.IGNORECASE) if p.strip()]

    # remove stray leading/trailing AND/OR tokens if any
    cleaned = []
    for p in parts:
        p = re.sub(r"(^\s*AND\s+)|(\s+AND\s*$)", "", p, flags=re.IGNORECASE).strip()
        if p:
            cleaned.append(p)
    return cleaned


def generateMap(
        original_sql: str,
        padding: float = 1.0
) -> str:
    """
    Generate a Folium map from SQL and return HTML as a string.
    """
    # 1) parse ranges
    ranges = _parse_latlon_ranges(original_sql)
    if not ranges:
        raise ValueError("No latitude/longitude BETWEEN ... AND ... clauses found in provided SQL.")
    lat_min, lat_max, lon_min, lon_max = ranges

    # 2) extract table & leftover conditions
    table_name, where_clause = _extract_table_and_where(original_sql)
    leftover_conditions = _clean_leftover_where(where_clause)

    # build final WHERE
    where_parts = [
        f"latitude BETWEEN {lat_min} AND {lat_max}",
        f"longitude BETWEEN {lon_min} AND {lon_max}"
    ]
    if leftover_conditions:
        where_parts.extend(leftover_conditions)
    final_where = " AND ".join(where_parts)

    # build SELECT
    select_cols = "time, latitude, longitude, depth, temperature, salinity"
    final_query = f"SELECT {select_cols} FROM {table_name} WHERE {final_where};"

    # run query
    result = run_query(final_query, return_columns=True)
    if isinstance(result, str) and result.startswith("PostgreSQL Error"):
        raise RuntimeError(result)
    rows, columns = result
    df = pd.DataFrame(rows, columns=columns)
    df["latitude"] = df["latitude"].astype(float)
    df["longitude"] = df["longitude"].astype(float)

    if df.empty:
        # fallback: empty map centered on lat/lon box
        center_lat = (lat_min + lat_max) / 2
        center_lon = (lon_min + lon_max) / 2
        m = folium.Map(location=[center_lat, center_lon], zoom_start=6)
        return m._repr_html_()

    # compute bounds of points with padding
    min_lat = df["latitude"].min() - padding
    max_lat = df["latitude"].max() + padding
    min_lon = df["longitude"].min() - padding
    max_lon = df["longitude"].max() + padding

    # center map at mean
    center_lat = df["latitude"].mean()
    center_lon = df["longitude"].mean()

    m = folium.Map(location=[center_lat, center_lon])
    cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        lat = float(row["latitude"])
        lon = float(row["longitude"])
        popup_html = (
            f"time: {row.get('time')}<br>"
            f"depth: {row.get('depth')}<br>"
            f"temperature: {row.get('temperature')}<br>"
            f"salinity: {row.get('salinity')}"
        )
        folium.Marker(location=[lat, lon], popup=popup_html).add_to(cluster)

    # fit map to bounds
    m.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])

    # return HTML string instead of saving file
    return m._repr_html_()


# =========================
# Example usage (drop into your module)
# =========================
if __name__ == "__main__":
    example_sql = """
                  SELECT *
                  FROM floatchat.argo_data
                  WHERE
                    AND latitude BETWEEN 8
                    AND 30
                    AND longitude BETWEEN 50
                    AND 75
                    AND depth = 10;

                  """

    generateMap(example_sql)
