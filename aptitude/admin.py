from django.contrib import admin
from .models import Concept, Question, PracticeSession, InternAttempt, TaskAnswer

@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("concept", "is_demo", "order", "correct_answer")
    list_filter = ("concept", "is_demo")

@admin.register(PracticeSession)
class PracticeSessionAdmin(admin.ModelAdmin):
    list_display = ("concept", "num_questions", "created_at")

@admin.register(InternAttempt)
class InternAttemptAdmin(admin.ModelAdmin):
    list_display = ("intern_name", "intern_email", "session", "submitted")

@admin.register(TaskAnswer)
class TaskAnswerAdmin(admin.ModelAdmin):
    list_display = ("attempt", "question", "intern_answer", "is_correct")
