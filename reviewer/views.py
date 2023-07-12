from django.shortcuts import render, redirect
import authentication.models
from django.contrib.auth.decorators import login_required
from .models import RequestToReview
from proposals.models import Details
import pandas as pd
from .forms import DeclineForm


def pending(request, proposal_number: str = ""):
    try:
        proposals = [
            row
            for row in RequestToReview.objects.filter(
                email=request.user.email, rejected=False
            ).values()
        ]
    except:
        proposals = None

    # try:
    description = [
        row for row in Details.objects.filter(proposal_number=proposal_number).values()
    ]
    for index in range(len(description)):
        description[index] = [
            (i, j) for (i, j) in description[index].items() if j not in [None, ""]
        ]

    return render(
        request=request,
        template_name="pending.html",
        context={
            "proposal_number": proposal_number,
            "description": description,
            "proposals": proposals,
        },
    )


def agree(request, proposal_number: str = ""):
    return render(
        request=request,
        template_name="agree.html",
        context={},
    )


def decline(request, proposal_number: str = ""):
    # Todo need to do something with the received email
    decline_form = DeclineForm()
    if request.method == "POST":
        decline_form = DeclineForm(request.POST)
        if decline_form.is_valid():
            from reviewer.models import RequestToReview

            RequestToReview.objects.filter(
                proposal_number=proposal_number, email=request.user.email
            ).update(rejected=True)
            return redirect("/proposals/home")
    return render(
        request=request,
        template_name="decline.html",
        context={"decline_form": decline_form},
    )
