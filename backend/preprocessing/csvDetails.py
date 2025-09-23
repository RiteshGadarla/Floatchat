import pandas as pd

# === Load CSV ===
file_path = input("Enter CSV file path: ")
df = pd.read_csv(file_path)

# === Convert time column to datetime if exists ===
if 'time' in df.columns:
    df['time'] = pd.to_datetime(df['time'], errors='coerce')  # Invalid dates become NaT

# === Basic Info ===
print("=== Basic Info ===")
print(f"Number of rows: {df.shape[0]}")
print(f"Number of columns: {df.shape[1]}")
print(f"Column names: {list(df.columns)}")
print("\nNumber of nulls in each column:")
print(df.isnull().sum())

# === Min and Max Values ===
print("\n=== Min and Max Values ===")
for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_datetime64_any_dtype(df[col]):
        print(f"{col} -> Min: {df[col].min()}, Max: {df[col].max()}")
    else:
        print(f"{col} -> Non-numeric/categorical column")
