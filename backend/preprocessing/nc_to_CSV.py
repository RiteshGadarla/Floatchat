import os
import glob
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime, timedelta
from netCDF4 import Dataset

# === Config ===
NC_DIR = input("Enter the directory where NC data is located: ")
if not os.path.exists(NC_DIR):
    raise FileNotFoundError(f"NC data directory {NC_DIR} not found")

OUTPUT_CSV = "data.csv"


def juld_to_datetime(val):
    """Convert JULD to 'YYYY-MM-DD HH:MM:SS' (auto-detect unit)."""
    if val is None or np.isnan(val):
        return None
    base = datetime(1950, 1, 1)
    v = float(val)

    try:
        if v > 1e15:  # microseconds
            dt = base + timedelta(microseconds=v)
        elif v > 1e12:  # milliseconds
            dt = base + timedelta(milliseconds=v)
        elif v > 1e9:  # seconds
            dt = base + timedelta(seconds=v)
        else:  # days
            dt = base + timedelta(days=v)
    except Exception:
        return None

    return dt.strftime("%Y-%m-%d %H:%M:%S")


def safe_float(val):
    """Convert netCDF MaskedArray element to float, or np.nan if masked."""
    if hasattr(val, "mask") and val.mask:
        return np.nan
    return float(val)


def assign_depth_bin(pres_val, step=10, tol=1):
    """
    Assign pressure value to nearest depth bin (0, 10, 20, ...)
    if within tolerance (±tol). Returns None if outside tolerance.
    """
    if pres_val is None:
        return None
    bin_val = round(pres_val / step) * step  # nearest multiple of step
    if abs(pres_val - bin_val) <= tol:
        return bin_val
    return None


# Remove old CSV if exists
if os.path.exists(OUTPUT_CSV):
    os.remove(OUTPUT_CSV)

# Find all .nc files
nc_files = glob.glob(os.path.join(NC_DIR, "**", "*.nc"), recursive=True)
print(f"📂 Found {len(nc_files)} NetCDF files")

with tqdm(total=len(nc_files), desc="Processing files", unit="file") as pbar:
    for nc_file in nc_files:
        try:
            ds = Dataset(nc_file, "r")

            n_prof = len(ds.dimensions.get("N_PROF", [0]))
            n_levels = len(ds.dimensions.get("N_LEVELS", [0]))

            rows = []
            for p in range(n_prof):
                juld_val = juld_to_datetime(ds.variables["JULD"][p]) if "JULD" in ds.variables else None
                lat_val = float(ds.variables["LATITUDE"][p]) if "LATITUDE" in ds.variables else None
                lon_val = float(ds.variables["LONGITUDE"][p]) if "LONGITUDE" in ds.variables else None

                for l in range(n_levels):
                    pres_val = ds.variables["PRES"][p, l] if "PRES" in ds.variables else np.nan
                    temp_val = ds.variables["TEMP"][p, l] if "TEMP" in ds.variables else np.nan
                    psal_val = ds.variables["PSAL"][p, l] if "PSAL" in ds.variables else np.nan

                    if np.isnan(pres_val) and np.isnan(temp_val) and np.isnan(psal_val):
                        continue

                    # Round values
                    lat_val_r = round(safe_float(lat_val), 5) if lat_val is not None else None
                    lon_val_r = round(safe_float(lon_val), 5) if lon_val is not None else None
                    pres_val_r = round(safe_float(pres_val), 5) if not np.isnan(safe_float(pres_val)) else None
                    temp_val_r = round(safe_float(temp_val), 5) if not np.isnan(safe_float(temp_val)) else None
                    psal_val_r = round(safe_float(psal_val), 5) if not np.isnan(safe_float(psal_val)) else None

                    # Assign depth bin
                    depth_bin = assign_depth_bin(pres_val_r)

                    if depth_bin is not None:
                        rows.append({
                            "time": juld_val,
                            "latitude": lat_val_r,
                            "longitude": lon_val_r,
                            "depth": depth_bin,  # ✅ depth instead of pressure
                            "temperature": temp_val_r,
                            "salinity": psal_val_r,
                        })

            ds.close()

            # Append to CSV
            if rows:
                df = pd.DataFrame(rows, columns=["time", "latitude", "longitude", "depth", "temperature", "salinity"])
                df.to_csv(OUTPUT_CSV, mode="a", header=not os.path.exists(OUTPUT_CSV), index=False)

        except Exception as e:
            tqdm.write(f"❌ Error processing {os.path.basename(nc_file)}: {e}")

        pbar.update(1)

print(f"\n🎉 Finished! Data saved to {OUTPUT_CSV}")
