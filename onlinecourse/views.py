from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Choice, Course, Learner, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course.objects.prefetch_related("lessons"), pk=course_id)
    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {"course": course},
    )


@login_required
def take_exam(request, course_id):
    course = get_object_or_404(
        Course.objects.prefetch_related("questions__choices"), pk=course_id
    )
    return render(request, "onlinecourse/take_exam.html", {"course": course})


@login_required
@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    learner, _ = Learner.objects.get_or_create(user=request.user)
    selected_ids = set()
    for question in course.questions.all():
        value = request.POST.get(f"question_{question.pk}", "")
        if value.isdecimal():
            selected_ids.add(int(value))
    selected_choices = Choice.objects.filter(
        pk__in=selected_ids, question__course=course
    ).select_related("question")
    questions = list(course.questions.all())
    correct_choice_by_question = {
        question.pk: question.choices.filter(is_correct=True).values_list(
            "pk", flat=True
        ).first()
        for question in questions
    }
    selected_by_question = {
        choice.question_id: choice.pk for choice in selected_choices
    }
    correct_count = sum(
        selected_by_question.get(question_id) == correct_choice_id
        for question_id, correct_choice_id in correct_choice_by_question.items()
    )

    submission = Submission.objects.create(
        learner=learner,
        course=course,
        score=correct_count,
        total_questions=len(questions),
    )
    submission.choices.set(selected_choices)
    return redirect("show_exam_result", submission_id=submission.pk)


@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission.objects.select_related("learner__user", "course").prefetch_related(
            "choices__question"
        ),
        pk=submission_id,
    )
    if submission.learner.user_id != request.user.pk and not request.user.is_staff:
        raise PermissionDenied
    return render(
        request,
        "onlinecourse/show_exam_result_bootstrap.html",
        {"submission": submission},
    )
