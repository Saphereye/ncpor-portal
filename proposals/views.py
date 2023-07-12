from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import DetailsForm, FilesForm
from .models import Details, Files, IncompleteProposals
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from hashlib import shake_256
from django.db.models import Subquery
from datetime import datetime
import requests
import json
import authentication.models
import reviewer.models


@login_required
def home(request):
    # entries_in_revisers = Revisers.objects.all().values("proposal_number")
    # result = Details.objects.exclude(proposal_number=Subquery(entries_in_revisers))
    # print(result.values())
    # print(authentication.models.CustomUser.objects.filter(email=request.user.email).values()[0]["id"])
    is_pi = False
    is_verifier = False
    is_coordinator = False
    try:
        user = authentication.models.Details.objects.filter(
            email=request.user.email
        ).values()[0]
        print(user)
        is_pi = user["is_pi"]
        is_verifier = user["is_verifier"]
        is_coordinator = user["is_coordinator"]
    except:
        pass

    return render(
        request=request,
        template_name="home.html",
        context={
            "incomplete": IncompleteProposals.objects.filter(
                email=request.user.email
            ).count(),
            "all": Details.objects.filter(email=request.user.email).count(),
            "is_pi": is_pi,
            "is_verifier": is_verifier,
            "is_coordinator": is_coordinator,
            "total_proposals": Details.objects.all().count(),
            "num_of_pending": reviewer.models.RequestToReview.objects.filter(
                email=request.user.email
            ).count(),
            "num_of_agreed": reviewer.models.RequestToReview.objects.filter(
                email=request.user.email, accepted=True
            ).count(),
        },
    )


@login_required
def submit(request):
    request.session["completing"] = False
    return redirect("/proposals/submit/details")


@login_required
def submit_details(request, title: str = ""):
    if title != "":
        title = title.replace("_", " ")
    details_form = DetailsForm()
    if request.method == "POST":
        if title != "":
            details_form = DetailsForm(
                request.POST,
                instance=get_object_or_404(Details, title_of_proposal=title),
            )
        else:
            details_form = DetailsForm(request.POST)
        if details_form.is_valid():
            details = details_form.save(commit=False)
            title = details.title_of_proposal
            IncompleteProposals.objects.get_or_create(
                email=request.user.email, title=title
            )
            details.email = request.user.email
            details.proposal_number = shake_256(
                (str(details) + str(datetime.now())).encode()
            ).hexdigest(6)
            details.save()
            messages.success(request, "Details saved successful.")
            return redirect(f"/proposals/submit/files/{title.replace(' ', '_')}/")
        messages.error(request, "Details not saved. Invalid information.")

    # print(Details.objects.filter(title_of_proposal=request.session["title"]).values()[0])
    if title != "":
        query_set = Details.objects.filter(title_of_proposal=title).values()

        if len(query_set) > 0:
            details_form = DetailsForm(
                initial=Details.objects.filter(title_of_proposal=title).values()[0]
            )

    return render(
        request=request,
        template_name="submit.html",
        context={
            "details_form": details_form,
            "step": 1,
            "title": title if title != "" else None,
        },
    )


@login_required
def submit_files(request, title: str = ""):
    if title != "":
        title = title.replace("_", " ")
    files_form = FilesForm()
    if request.method == "POST":
        try:
            query = Files.objects.get(title_of_proposal=title)
            if title != "" and query:
                files_form = FilesForm(
                    request.POST,
                    instance=query,
                )
        except Files.DoesNotExist:
            files_form = FilesForm(request.POST, request.FILES)
        print(f"{request.FILES=}")

        if files_form.is_valid():
            files = files_form.save(commit=False)
            files.title_of_proposal = title
            files.email = request.user.email
            # files.cover_letter = request.FILES["cover_letter"]

            # print(files, request.FILES, request.FILES["cover_letter"])
            IncompleteProposals.objects.get_or_create(
                email=request.user.email, title=title
            )
            files.save()
            messages.success(request, "Files saved successful.")
            return redirect(f"/proposals/submit/summary/{title.replace(' ', '_')}/")
        messages.error(request, "Files not saved. Invalid information.")

    if title != "" and len(Files.objects.filter(title_of_proposal=title).values()) > 0:
        # proposal_id =
        # print(
        #     Details.objects.filter(title_of_proposal=title).values()[
        #         0
        #     ]["title_of_proposal"],
        # )
        # session_title = Details.objects.filter(
        #     title_of_proposal=title
        # ).values()[0]["title_of_proposal"]
        files_form = FilesForm(
            initial=Files.objects.filter(title_of_proposal=title).values()[0]
        )

    return render(
        request=request,
        template_name="submit.html",
        context={
            "files_form": files_form,
            "step": 2,
            "title": title if title != "" else None,
        },
    )


@login_required
def submit_summary(request, title: str = ""):
    if title != "":
        title = title.replace("_", " ")
    if request.method == "POST":
        try:
            proposal = IncompleteProposals.objects.get(
                email=request.user.email, title=title
            )
            proposal.delete()
            return redirect("/proposals/submit/finish")
        except IncompleteProposals.DoesNotExist:
            pass
    if title != "":
        details = Details.objects.filter(title_of_proposal=title).values()
        files = Files.objects.filter(title_of_proposal=title).values()
    else:
        details = None
        files = None
    print(details, files)
    # print(details[0].items(), [i for i in details])
    return render(
        request=request,
        template_name="submit.html",
        context={
            "step": 3,
            "details": [
                (i.replace("_", " ").capitalize(), j)
                for (i, j) in details[0].items()
                if i not in ["id", "email"] and j is not None and j != ""
            ]
            if details
            else None,
            "title": request.session["title"]
            if "title" in request.session
            else "No Title",
            "files": [
                (i.replace("_", " ").capitalize(), "No" if j == "" else "Yes")
                for (i, j) in files[0].items()
                if i not in ["id", "title_of_proposal", "email"]
            ]
            if files
            else None,
        },
    )


@login_required
def submit_finish(request, title: str = ""):
    if (
        "details_done" in request.session
        and "files_done" in request.session
        and request.session["details_done"] is True
        and request.session["files_done"] is True
    ):
        try:
            proposals = IncompleteProposals.objects.get(email=request.user.email)
            proposals.delete()
        except IncompleteProposals.DoesNotExist:
            proposals = None
    return render(
        request=request,
        template_name="submit.html",
        context={"step": 4},
    )


@login_required
def incomplete_proposals(request):
    try:
        proposals = IncompleteProposals.objects.filter(email=request.user.email)
        proposals = [
            (index + 1, i["title"], i["title"].replace(" ", "_"))
            for index, i in enumerate(proposals.values())
        ]
        print(proposals)
    except IncompleteProposals.DoesNotExist:
        proposals = None
    return render(
        request=request,
        template_name="incomplete.html",
        context={"proposals": proposals},
    )


@login_required
def all(request):
    details = [
        i for i in list(Details.objects.filter(email=request.user.email).values())
    ]
    output = []
    for index, i in enumerate(details):
        try:
            files = Files.objects.get(
                email=request.user.email, title_of_proposal=i["title_of_proposal"]
            )
            files = model_to_dict(files)
            temp = {"id": index + 1}
            temp.update(i)
            temp.update(files)
            output.append(
                [
                    (
                        " ".join((i.replace("_", " ").capitalize()).split()[:3]),
                        j if j != "" else "No",
                    )
                    for i, j in temp.items()
                    if i not in ["email"]
                ]
            )
        except Files.DoesNotExist:
            pass
    print(output)
    return render(
        request=request,
        template_name="all.html",
        context={"output": output, "heads": output[0]},
    )
