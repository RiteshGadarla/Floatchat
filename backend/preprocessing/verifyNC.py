import xarray as xr

# Open the NetCDF file
file_name = input("Enter the nc files path: ")
ds = xr.open_dataset(file_name)

# Display general info about the dataset
print(ds)

# List all variables
print("Variables:", list(ds.data_vars))