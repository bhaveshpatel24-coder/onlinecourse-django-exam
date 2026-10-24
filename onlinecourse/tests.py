from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Choice, Course, Learner, Question, Submission


class ExamSubmissionTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="learner", password="test-password"
        )
        self.course = Course.objects.create(name="Python", description="Basics")
        self.question = Question.objects.create(
            course=self.course, content="Which is a Python keyword?"
        )
        self.correct = Choice.objects.create(
            question=self.question, content="def", is_correct=True
        )
        Choice.objects.create(
            question=self.question, content="define", is_correct=False
        )
        self.client.force_login(self.user)

    def test_correct_answer_creates_passing_submission_and_result(self):
        response = self.client.post(
            reverse("submit", args=[self.course.pk]),
            {f"question_{self.question.pk}": str(self.correct.pk)},
        )

        submission = Submission.objects.get()
        self.assertRedirects(
            response,
            reverse("show_exam_result", args=[submission.pk]),
        )
        self.assertEqual(submission.score, 1)
        self.assertEqual(submission.percentage, 100)
        self.assertTrue(submission.passed)
        result = self.client.get(
            reverse("show_exam_result", args=[submission.pk])
        )
        self.assertContains(result, "Congratulations!")
        self.assertContains(result, "Exam results")

    def test_result_is_not_visible_to_another_learner(self):
        learner, _ = Learner.objects.get_or_create(user=self.user)
        submission = Submission.objects.create(
            learner=learner,
            course=self.course,
            score=1,
            total_questions=1,
        )
        other_user = get_user_model().objects.create_user(
            username="other", password="test-password"
        )
        self.client.force_login(other_user)

        response = self.client.get(
            reverse("show_exam_result", args=[submission.pk])
        )

        self.assertEqual(response.status_code, 403)
