from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from formtools.wizard.views import SessionWizardView
from .forms import DetailsForm


class ContactWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        print(form_list)
        return HttpResponseRedirect("#")


@login_required
def home(request):
    return render(
        request=request,
        template_name="home.html",
        context={},
    )


@login_required
def submit(request):
    return redirect("/proposals/submit/details")


@login_required
def submit_details(request):
    if request.method == "POST":
        details_form = DetailsForm(request.POST)
        if details_form.is_valid():
            request.session["title"] = request.POST.get("title_of_proposal")
            details_form.save()
            messages.success(request, "Details saved successful.")
            return redirect("/proposals/submit/files")
        messages.error(request, "Details not saved. Invalid information.")
    details_form = DetailsForm()
    return render(
        request=request,
        template_name="submit.html",
        context={
            "details_form": details_form,
            "step": 1,
            "title": request.session["title"]
            if "title" in request.session
            else "No Title",
        },
    )


@login_required
def submit_files(request):
    print(request.session["page"] if "page" in request.session else "Doesn't exist yet")
    request.session["page"] = 2
    return render(
        request=request,
        template_name="submit.html",
        context={
            "step": 2,
            "title": request.session["title"]
            if "title" in request.session
            else "No Title",
        },
    )


@login_required
def submit_summary(request):
    return render(
        request=request,
        template_name="submit.html",
        context={"step": 3},
    )


@login_required
def submit_finish(request):
    return render(
        request=request,
        template_name="submit.html",
        context={"step": 4},
    )
