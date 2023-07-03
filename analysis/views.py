from django.shortcuts import render
from .forms import MainForm
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import Scatter
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
        df["DateTime"] = df["DateTime"].apply(
            lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        )
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

        df = df[(df["DateTime"] > date_low) & (df["DateTime"] < date_high)]
        x_data = df["DateTime"]
        y_data = df["BC6"]
        plot_div = plot(
            [
                Scatter(
                    x=x_data,
                    y=y_data,
                    mode="markers",
                    name="test",
                    opacity=0.8,
                    marker_color="green",
                )
            ],
            output_type="div",
            include_plotlyjs=False,
            show_link=False,
            link_text=""
        )
    return render(request, "index.html", context={"plot_div": plot_div, "form": form})
    # return render(
    #     request=request,
    #     template_name="details.html",
    #     context={"form": form},
    # )
