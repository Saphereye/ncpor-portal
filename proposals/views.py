from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import DetailsForm, FilesForm
from .models import Details, Files, IncompleteProposals
from django.shortcuts import get_object_or_404


@login_required
def home(request):
    return render(
        request=request,
        template_name="home.html",
        context={
            "incomplete": IncompleteProposals.objects.filter(
                email=request.user.email
            ).count()
        },
    )


@login_required
def submit(request):
    request.session["completing"] = False
    return redirect("/proposals/submit/details")


@login_required
def submit_details(request, title: str = ""):
    details_form = DetailsForm()
    if request.method == "POST":
        if title != "":
            details_form = DetailsForm(
                request.POST,
                instance=get_object_or_404(
                    Details, title_of_proposal=title
                ),
            )
        else:
            details_form = DetailsForm(request.POST)
        if details_form.is_valid():
            IncompleteProposals.objects.get_or_create(
                email=request.user.email, title=title
            )
            details_form.save()
            messages.success(request, "Details saved successful.")
            return redirect(f"/proposals/submit/files/{title}/")
        messages.error(request, "Details not saved. Invalid information.")

    # print(Details.objects.filter(title_of_proposal=request.session["title"]).values()[0])
    if title != "":
        query_set = Details.objects.filter(
            title_of_proposal=title
        ).values()

        if len(query_set) > 0:
            details_form = DetailsForm(
                initial=Details.objects.filter(
                    title_of_proposal=title
                ).values()[0]
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
    files_form = FilesForm()
    if request.method == "POST":
        query = Files.objects.filter(title_of_proposal=title)
        print(query)
        if title != "" and len(query) > 0:
            files_form = FilesForm(
                request.POST,
                instance=query,
            )
        else:
            files_form = FilesForm(request.POST)
        # files_form = FilesForm(request.POST)

        if files_form.is_valid():
            files_form.save(commit=False)
            files_form.title_of_proposal = title
            IncompleteProposals.objects.get_or_create(
                email=request.user.email, title=title
            )
            files_form.save()
            messages.success(request, "Files saved successful.")
            return redirect(f"/proposals/submit/summary/{title}/")
        messages.error(request, "Files not saved. Invalid information.")

    if (
        title != ""
        and len(
            Files.objects.filter(title_of_proposal=title).values()
        )
        > 0
    ):
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
            initial=Files.objects.filter(
                title_of_proposal=title
            ).values()[0]
        )
    else:
        files_form = FilesForm()
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
        details = Details.objects.filter(
            title_of_proposal=title
        ).values()
    else:
        details = None
    # print(details[0].items(), [i for i in details])
    return render(
        request=request,
        template_name="submit.html",
        context={
            "step": 3,
            "details": [
                (i.replace("_", " ").capitalize(), j)
                for (i, j) in details[0].items()
                if i not in ["id"]
            ]
            if details
            else None,
            "title": request.session["title"]
            if "title" in request.session
            else "No Title",
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
            (index + 1, i["title"], i["title"].replace(" ", "_").lower())
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
