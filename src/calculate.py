import pandas
import matplotlib.pyplot

from .config import PROCESSED_DIR


def average_load(data: pandas.DataFrame):
    return data["Actual Load"].mean()


def peak_load(data: pandas.DataFrame):
    return data["Actual Load"].max()


def plot(data: pandas.DataFrame):
    n = len(data)

    daily_chunks = [data.iloc[i:7] for i in range(7)]

    daily_averages = [average_load(chunk) for chunk in daily_chunks]

    matplotlib.pyplot.figure(figsize=(10, 8))
    matplotlib.pyplot.plot(range(1, 8), daily_averages)
    matplotlib.pyplot.title("Daily Average Over Last 7 Days")
    matplotlib.pyplot.xlabel("Day")
    matplotlib.pyplot.ylabel("Average Load")
    matplotlib.pyplot.grid(True)

    matplotlib.pyplot.savefig(f"{PROCESSED_DIR}/plot.png")
    matplotlib.pyplot.close()
