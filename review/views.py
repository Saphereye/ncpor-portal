from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from proposals.models import Details
import pandas as pd


@login_required
def revision(request):
    output = [
        i for i in list(Details.objects.filter(email=request.user.email).values())
    ]
    output = pd.DataFrame(output)
    output = output[["title_of_proposal", "key_words", "proposal_number"]]
    output.index += 1
    heads = ["Sr. No"] + list(output.columns)
    output = list(output.itertuples(index=True))
    return render(
        request=request,
        template_name="revision.html",
        context={
            "output": output,
            "heads": heads,
        },
    )
