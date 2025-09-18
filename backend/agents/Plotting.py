import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def style_time_axis(ax):
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M"))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right", fontsize=8)
    ax.grid(True, linestyle="--", alpha=0.5)


def plotGraphs(csv_file):
    """
    Reads a CSV file and plots time series for salinity and/or temperature
    against time. Returns matplotlib figure(s) for Streamlit.
    """
    if not os.path.exists(csv_file):
        print(f"❌ File not found: {csv_file}")
        return []

    try:
        df = pd.read_csv(csv_file)

        if "time" not in df.columns:
            print("⚠️ 'time' column not found in CSV.")
            return []

        # Convert time column to datetime
        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        df = df.dropna(subset=["time"])  # drop invalid times

        figures = []

        # Plot salinity if exists
        if "salinity" in df.columns:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(df["time"], df["salinity"], label="Salinity", color="blue")
            ax.set_title("Salinity vs Time")
            ax.set_xlabel("Time")
            ax.set_ylabel("Salinity")
            ax.legend()
            style_time_axis(ax)
            figures.append(fig)

        # Plot temperature if exists
        if "temperature" in df.columns:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(df["time"], df["temperature"], label="Temperature", color="red")
            ax.set_title("Temperature vs Time")
            ax.set_xlabel("Time")
            ax.set_ylabel("Temperature")
            ax.legend()
            style_time_axis(ax)
            figures.append(fig)

        return figures

    except Exception as e:
        print(f"⚠️ Error while plotting: {e}")
        return []


# Example usage without Streamlit:
if __name__ == "__main__":
    figures = plotGraphs("dataExtracted.csv")
    for fig in figures:
        plt.show(fig)
