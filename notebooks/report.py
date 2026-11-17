import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import pandas as pd

    return mo, pd, plt


@app.cell
def _(mo):
    mo.md("""
    # Event Duration Report

    Distribution of event durations, loaded from the output of the DVC
    pipeline (`data/features/events.csv`).
    """)
    return


@app.cell
def _(pd):
    df = pd.read_csv("data/features/events.csv")
    df.head()
    return (df,)


@app.cell
def _(df, plt):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(df["duration_minutes"], bins=30, edgecolor="white")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Number of events")
    ax.set_title("Distribution of event durations")
    fig.tight_layout()
    ax
    return


if __name__ == "__main__":
    app.run()
