from django.urls import path

from . import views


urlpatterns = [
    path("courses/<int:course_id>/", views.course_details, name="course_details"),
    path(
        "courses/<int:course_id>/exam/",
        views.take_exam,
        name="take_exam",
    ),
    path("submit/<int:course_id>/", views.submit, name="submit"),
    path(
        "exam-results/<int:submission_id>/",
        views.show_exam_result,
        name="show_exam_result",
    ),
]
