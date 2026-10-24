from django.conf import settings
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons"
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "pk"]

    def __str__(self):
        return self.title


class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    total_learners = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.get_username()


class Learner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, related_name="learners", blank=True)

    def __str__(self):
        return self.user.get_username()


class Question(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="questions"
    )
    content = models.CharField(max_length=500)

    def __str__(self):
        return self.content


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    content = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class Submission(models.Model):
    learner = models.ForeignKey(
        Learner, on_delete=models.CASCADE, related_name="submissions"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="submissions"
    )
    choices = models.ManyToManyField(Choice, related_name="submissions")
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    @property
    def percentage(self):
        if not self.total_questions:
            return 0
        return round(self.score * 100 / self.total_questions)

    @property
    def passed(self):
        return self.percentage >= 60

    def __str__(self):
        return f"{self.learner} - {self.course} ({self.percentage}%)"
