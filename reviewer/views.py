from django.shortcuts import render
import authentication.models
from django.contrib.auth.decorators import login_required
from .models import RequestToReview
from proposals.models import Details
import pandas as pd

def pending(request, proposal_number: str = ""):
    try:
        proposals = [row for row in RequestToReview.objects.filter(email=request.user.email).values()]
    except:
        proposals = None
    
    # try:
    description = [row for row in Details.objects.filter(proposal_number=proposal_number).values()]
    for index in range(len(description)):
        description[index] = [(i, j) for (i, j) in  description[index].items() if j not in [None, ""]]
    # except:
    #     description = None
    print(description)
    
    return render(
        request=request,
        template_name="pending.html",
        context={
            "proposal_number": proposal_number,
            "description": description,
            "proposals": proposals
        },
    )