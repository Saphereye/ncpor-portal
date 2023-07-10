from django.shortcuts import render, HttpResponse, redirect
from .forms import LoginForm, RegisterForm, DetailsForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser


def welcome(request) -> HttpResponse:
    # return render(request=request, template_name="welcome.html", context={})
    return redirect("/proposals/home")


def division_choose(request):
    if request.method == "POST":
        division = request.POST.get("division")
        request.session["division"] = division
    return redirect("/accounts/login")


# def login(request):
#     print("Login")
#     if request.method == "POST":
#         print("Post")
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             print("Form valid")
#             username = login_form.cleaned_data["username"]
#             password = login_form.cleaned_data["password"]
#             user = authenticate(request, username=username, password=password)
#             if user:
#                 login(request, user)
#                 messages.success(request, f"Hi {username.title()}, welcome back!")
#                 print("Signing in {}".format(request.user))
#                 return redirect("/home")
#             # form is not valid or user is not authenticated
#             messages.error(request, f"Invalid username or password")
#     login_form = LoginForm()
#     division = request.session["division"] if "division" in request.session else None
#     return render(
#         request=request,
#         template_name="login.html",
#         context={"division": division, "form": login_form},
#     )


def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/authentication/details")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    register_form = RegisterForm()
    return render(
        request=request,
        template_name="register.html",
        context={"register_form": register_form},
    )

def details(request):
    if request.method == "POST":
        details_form = DetailsForm(request.POST)
        if details_form.is_valid():
            details = details_form.save(commit=False)
            details.email = CustomUser.objects.get(email=request.user.email)
            details.save()
            messages.success(request, "Details saved successful.")
            return redirect("/proposals/home")
        messages.error(request, "Details not saved. Invalid information.")
    details_form = DetailsForm()
    return render(
        request=request,
        template_name="details.html",
        context={"details_form": details_form},
    )
