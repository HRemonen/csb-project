from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question


def index(request):
    recent_questions = Question.objects.order_by("-pub_date")[:5]

    ctx = {
        "recent_questions": recent_questions,
    }
    return render(request, "securepolls/index.html", ctx)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    ctx = {
        "question": question,
    }

    return render(request, "securepolls/detail.html", ctx)


def results(request, question_id):
    return HttpResponse(f"You're looking at the results of question {question_id}.")


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
