from django.db import models


# 1️⃣ Concept (Topic)
class Concept(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


# 2️⃣ Question (Demo + Practice)
class Question(models.Model):
    concept = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question = models.TextField()
    explanation = models.TextField()
    correct_answer = models.CharField(max_length=255)
    is_demo = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.concept.name} - {'Demo' if self.is_demo else 'Practice'}"


# 3️⃣ Mentor creates a session
class PracticeSession(models.Model):
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    num_questions = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.concept.name} - {self.num_questions} Questions"


# 4️⃣ Intern starts a test (NO LOGIN)
class InternAttempt(models.Model):
    session = models.ForeignKey(PracticeSession, on_delete=models.CASCADE)
    intern_name = models.CharField(max_length=120)
    intern_email = models.EmailField()
    started_at = models.DateTimeField(auto_now_add=True)
    submitted = models.BooleanField(default=False)

    # ⭐ IMPORTANT: store selected questions so they don't reshuffle
    selected_questions = models.ManyToManyField(Question, blank=True)

    def __str__(self):
        return f"{self.intern_name} ({self.session})"


# 5️⃣ Intern answers
class TaskAnswer(models.Model):
    attempt = models.ForeignKey(InternAttempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    intern_answer = models.TextField()
    intern_explanation = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer by {self.attempt.intern_name}"
