from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from datetime import date

from .models import Choice, Question


@login_required(login_url="/login")
def index_view(request):
    recent_questions = Question.objects.order_by("-pub_date")[:5]

    ctx = {
        "recent_questions": recent_questions,
    }
    return render(request, "securepolls/index.html", ctx)


@csrf_exempt
def create_view(request):
    if request.method == "POST":
        question = Question(
            question_text=request.POST["question"],
            creator=request.user,
            pub_date=date.today(),
        )
        question.save()

        choices = request.POST.getlist("choices")
        for choice_text in choices:
            choice = Choice(
                question=question,
                choice_text=choice_text,
            )
            choice.save()

        return HttpResponseRedirect(reverse("securepolls:index"))

    return render(request, "securepolls/create.html")


@csrf_exempt
def register_view(request):
    if request.method == "POST":
        try:
            user = User.objects.create_user(
                username=request.POST["username"], password=request.POST["password"]
            )
        except IntegrityError:
            return render(
                request,
                "securepolls/register.html",
                {"error_message": "Username already exists."},
            )
        else:
            user.save()

            return HttpResponseRedirect(reverse("securepolls:login"))

    return render(request, "securepolls/register.html")


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"]
        )

        if user is not None:
            login(request, user)

            return HttpResponseRedirect(reverse("securepolls:index"))

    return render(request, "securepolls/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("securepolls:login"))


@csrf_exempt
def reset_password_view(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST["username"])
        except User.DoesNotExist:
            return render(
                request,
                "securepolls/reset_password.html",
                {"error_message": "User does not exist."},
            )
        else:
            # FIX: This is a security vulnerability, the password should come from the user
            # password = request.POST["password"]
            # user.set_password(password)

            user.set_password("password")
            user.save()
            return HttpResponseRedirect(reverse("securepolls:login"))

    return render(request, "securepolls/reset_password.html")


def detail_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    ctx = {
        "question": question,
    }

    return render(request, "securepolls/detail.html", ctx)


def results_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    ctx = {
        "question": question,
    }

    return render(request, "securepolls/results.html", ctx)


@csrf_exempt
def vote_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "securepolls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("securepolls:results", args=(question.id,)))


def users_view(request):
    # FIX: This is a security vulnerability. We should not be exposing all users.
    # We should check if user is admin before showing anything. But it is still flaky.
    # if not request.user.is_superuser:
    #     return HttpResponseRedirect(reverse("securepolls:index"))

    users = User.objects.all()

    ctx = {
        "users": users,
    }

    return render(request, "securepolls/users.html", ctx)
