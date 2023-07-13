from django.shortcuts import render
from .forms import MainForm
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Heatmap
import pandas as pd
import os
from django.templatetags.static import static
import csv
from datetime import datetime


def main(request):
    if request.method == "POST":
        form = MainForm(request.POST)
    else:
        form = MainForm()

    with open("analysis/data/data.csv") as file:
        df = pd.read_csv(file)
        print(df["BC6"].describe())
        df["DateTime"] = pd.to_datetime(df['DateTime'], format="%Y-%m-%d %H:%M:%S")
        reduced_df = pd.DataFrame()
        time_slots = pd.date_range(start=df['DateTime'].min(), end=df['DateTime'].max(), freq='H')


        for i in range(len(time_slots) - 1):
            start_time = time_slots[i]
            end_time = time_slots[i + 1]

            # Get the data within the time slot
            chunk = df[(df['DateTime'] >= start_time) & (df['DateTime'] < end_time)]

            # Check if the chunk has data
            if not chunk.empty:
                # Calculate the mean of the chunk
                mean_row = chunk["BC6"].mean()
                mean_df = pd.DataFrame({
                    "DateTime":start_time,
                    "BC6":mean_row
                }, index=[1])

                # Append the mean row to the reduced DataFrame
                reduced_df = pd.concat([reduced_df, mean_df], ignore_index=True)
        print(f"{reduced_df.head()=}")
        df = reduced_df
        # df = df.dropna(subset=['DateTime'])
        # print(df['DateTime'].dtype)
        # # df = df.set_index('DateTime')
        # df = df.resample('H', on="DateTime").median().reset_index()
        # df["BC6"] /= 60*60
        # df = df.dropna(subset=['DateTime'])
        # df = df.resample('6H', on='DateTime').mean().reset_index()
        # df["DateTime"] = datetime.fromtimestamp((df["DateTime"].to_timestamp())%60)
        # df.set_index("DateTime", inplace=True)
        # df.index = df.index.astype(int) // 10**9
        # df.index  = df.index.resa
        # df.index = pd.to_datetime(df.index, unit="s")
        # df.reset_index(inplace=True)

        date_low = (
            df["DateTime"].min()
            if ("date_low" not in form.fields or form["date_low"].value() is None)
            else form["date_low"].value()
        )
        date_high = (
            df["DateTime"].max()
            if ("date_high" not in form.fields or form["date_high"].value() is None)
            else form["date_high"].value()
        )

        print(date_low, date_high)

        df["Date"] = df["DateTime"].apply(lambda s: s.date())
        df["Time"] = df["DateTime"].apply(lambda s: s.time())

        print(df.head())

        heatmap = go.Heatmap(
            x=df["Date"],
            y=df["Time"],
            z=df["BC6"],
        )

        layout = go.Layout(
            title="BC6 yearly data",
            xaxis=dict(title="Date"),
            yaxis=dict(title="Time"),
            height=800,
            width=1000
        )

        heatmap_figure = go.Figure(data=[heatmap], layout=layout)

        plot_div = heatmap_figure.to_html(
            full_html=False,
            include_plotlyjs=False,
        )
        # plot_div = plot(
        #     [
        #         # Scatter(
        #         #     x=x_data,
        #         #     y=y_data,
        #         #     mode="markers",
        #         #     name="test",
        #         #     opacity=0.8,
        #         #     marker_color="green",
        #         # )
        #         Heatmap(
        #             x=df["Date"],
        #             y=df["Time"],
        #             z=df["BC6"],
        #         )
        #     ],
        # )
    return render(request, "index.html", context={"plot_div": plot_div, "form": form})
    # return render(
    #     request=request,
    #     template_name="details.html",
    #     context={"form": form},
    # )
