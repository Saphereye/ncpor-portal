from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from proposals.models import Details
import pandas as pd
from .models import Revisers


@login_required
def revision(request, proposal_number: str = None):
    description = description_head = None
    if proposal_number != None:
        description = Details.objects.filter(proposal_number=proposal_number).values()[
            0
        ]
        description_head = description["proposal_number"]
        description = [(i, j) for (i, j) in description.items() if j not in [None, ""]]
        print(description)

    output = list(Details.objects.filter(email=request.user.email).values())
    output = pd.DataFrame(output)
    output = output[["title_of_proposal", "key_words", "proposal_number"]]
    output = output[~output["proposal_number"].isin(Revisers.objects.values_list("proposal_number", flat=True))]
    output.index += 1
    heads = ["Sr. No"] + list(output.columns)
    output = list(output.itertuples(index=True))
    return render(
        request=request,
        template_name="revision.html",
        context={
            "output": output,
            "heads": heads,
            "description": description,
            "description_head": description_head,
        },
    )


@login_required
def agree(request, proposal_number: str = None):
    Revisers.objects.create(
        reviser_email=request.user.email, proposal_number=proposal_number
    )
    return render(
        request=request,
        template_name="agree.html",
        context={"proposal_number": proposal_number},
    )
