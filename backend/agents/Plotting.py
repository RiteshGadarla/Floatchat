import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

ALLOWED_VISUALIZATIONS = [
    "Bar Chart", "Line Chart", "Histogram", "Scatter Plot",
    "Pie Chart", "Box Plot", "Area Chart", "Heatmap"
]

def style_time_axis(ax):
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M"))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right", fontsize=8)
    ax.grid(True, linestyle="--", alpha=0.5)

def plotGraphs(csv_file, visualizations_info):
    """
    Generate figures based on visualization instructions (JSON).
    """
    if not os.path.exists(csv_file):
        print(f"❌ File not found: {csv_file}")
        return []

    try:
        print("visualizations_info in plotting: ", visualizations_info)
        df = pd.read_csv(csv_file)
        figures = []

        # Convert time column if exists
        if "time" in df.columns:
            df["time"] = pd.to_datetime(df["time"], errors="coerce")
            df = df.dropna(subset=["time"])

        for viz in visualizations_info:
            vtype = viz.get("type")
            cols = viz.get("columns", [])

            if vtype not in ALLOWED_VISUALIZATIONS:
                print(f"⚠️ Unsupported visualization type: {vtype}")
                continue
            print(df.columns)
            if any(col not in df.columns for col in cols):
                continue

            fig, ax = plt.subplots(figsize=(8, 4))

            if vtype == "Line Chart":
                x = df[cols[0]] if df[cols[0]].dtype.kind in 'iufc' else df.get("time", df.index)
                y = df[cols[1]] if len(cols) > 1 else df[cols[0]]
                ax.plot(x, y, label=cols[1] if len(cols) > 1 else cols[0])
                ax.set_xlabel(cols[0] if len(cols) > 1 else "Time")
                ax.set_ylabel(cols[1] if len(cols) > 1 else cols[0])
                ax.set_title(f"{y.name} vs {x.name}")
                ax.legend()
                if x.name == "time":
                    style_time_axis(ax)

            elif vtype == "Bar Chart":
                ax.bar(df[cols[0]], df[cols[1]] if len(cols) > 1 else df[cols[0]], color='skyblue')
                ax.set_xlabel(cols[0])
                ax.set_ylabel(cols[1] if len(cols) > 1 else cols[0])
                ax.set_title(f"Bar Chart: {', '.join(cols)}")

            elif vtype == "Scatter Plot":
                x = df[cols[0]]
                y = df[cols[1]] if len(cols) > 1 else df[cols[0]]
                ax.scatter(x, y, alpha=0.7)
                ax.set_xlabel(cols[0])
                ax.set_ylabel(cols[1] if len(cols) > 1 else cols[0])
                ax.set_title(f"Scatter Plot: {cols[1]} vs {cols[0]}" if len(cols) > 1 else f"{cols[0]} Scatter")

            elif vtype == "Histogram":
                for col in cols:
                    ax.hist(df[col].dropna(), bins=20, alpha=0.7, label=col)
                ax.set_title(f"Histogram: {', '.join(cols)}")
                ax.set_xlabel("Value")
                ax.set_ylabel("Frequency")
                ax.legend()

            elif vtype == "Box Plot":
                sns.boxplot(data=df[cols], ax=ax)
                ax.set_title(f"Box Plot: {', '.join(cols)}")

            elif vtype == "Area Chart":
                df[cols].plot.area(ax=ax)
                ax.set_title(f"Area Chart: {', '.join(cols)}")

            elif vtype == "Pie Chart":
                if len(cols) != 1:
                    continue
                ax.pie(df[cols[0]].value_counts(), labels=df[cols[0]].value_counts().index, autopct='%1.1f%%')
                ax.set_title(f"Pie Chart: {cols[0]}")

            elif vtype == "Heatmap":
                sns.heatmap(df[cols].corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
                ax.set_title(f"Heatmap: {', '.join(cols)}")

            figures.append(fig)

        if not figures:
            print("⚠️ No valid visualizations generated.")

        return figures

    except Exception as e:
        print(f"⚠️ Error while plotting: {e}")
        return []
