from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import proposals.models
from django.forms.models import model_to_dict
from .forms import AssignedForm
import authentication.models
from django.db.models import Subquery, OuterRef
import reviewer.models


@login_required
def all(request):
    details = [i for i in list(proposals.models.Details.objects.exclude(
    proposal_number__in=Subquery(reviewer.models.RequestToReview.objects.values('proposal_number'))
).values())]
    print(f"{details=}")
    output = []
    for index, i in enumerate(details):
        temp = {"id": index + 1}
        temp.update(i)
        try:
            files = proposals.models.Files.objects.get(
                email=request.user.email, title_of_proposal=i["title_of_proposal"]
            )
            files = model_to_dict(files)
            temp.update(files)
        except proposals.models.Files.DoesNotExist:
            pass
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
    print(f"{output=}")
    return render(
        request=request,
        template_name="all_proposals.html",
        context={"output": output, "heads": output[0]},
    )


def assign(request, proposal_number: str = ""):
    if proposal_number == "":
        form = AssignedForm()
    else:
        form = AssignedForm(
            initial={
                "proposal_number": proposal_number,
            }
        )
    if request.method == "POST":
        form = AssignedForm(request.POST)
        if form.is_valid():
            # Put in request to reviewer table
            from reviewer.models import RequestToReview

            for i in range(1, 6):
                if request.POST[f"reviewer_{i}_email"] != 'None':
                    # This might get inneficient for large numbers, but as they say
                    # "Premature optimization is the root of all evil."
                    RequestToReview.objects.update_or_create(
                        proposal_number=proposal_number
                        if proposal_number != ""
                        else request.POST["proposal_number"],
                        email=request.POST[f"reviewer_{i}_email"],
                    )
            return redirect("/proposals/home")
    return render(
        request=request,
        template_name="assign.html",
        context={"proposal_number": proposal_number, "form": form},
    )
