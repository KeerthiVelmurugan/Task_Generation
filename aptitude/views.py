from django.shortcuts import render, redirect, get_object_or_404
from .models import Concept, PracticeSession, InternAttempt, TaskAnswer, Question
import random


def home(request):
    return render(request, "aptitude/home.html")

# 1️⃣ Mentor assigns a test
def assign_test(request):
    concepts = Concept.objects.all()

    if request.method == "POST":
        concept_id = request.POST.get("concept")
        num_questions = int(request.POST.get("num_questions"))

        session = PracticeSession.objects.create(
            concept_id=concept_id,
            num_questions=num_questions
        )
        return redirect("session_list")

    return render(request, "aptitude/assign_test.html", {"concepts": concepts})


# 2️⃣ List all assigned tests
def session_list(request):
    sessions = PracticeSession.objects.all().order_by("-created_at")
    return render(request, "aptitude/session_list.html", {"sessions": sessions})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import PracticeSession

def delete_session(request, session_id):
    session = get_object_or_404(PracticeSession, id=session_id)
    session.delete()
    messages.success(request, "Assigned test deleted successfully!")
    return redirect('session_list')



# 3️⃣ View intern attempts for a test
def session_detail(request, session_id):
    session = get_object_or_404(PracticeSession, id=session_id)
    attempts = InternAttempt.objects.filter(session=session)

    return render(request, "aptitude/session_detail.html", {
        "session": session,
        "attempts": attempts
    })


# 4️⃣ Intern enters details before starting
def start_test(request, session_id):
    session = get_object_or_404(PracticeSession, id=session_id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")

        attempt = InternAttempt.objects.create(
            session=session,
            intern_name=name,
            intern_email=email
        )

        # Select random questions only once
        qns = list(session.concept.questions.filter(is_demo=False))
        random.shuffle(qns)
        selected = qns[:session.num_questions]

        attempt.selected_questions.set(selected)

        return redirect("demo_questions", attempt_id=attempt.id)

    return render(request, "aptitude/start_test.html", {"session": session})


# 5️⃣ Show demo questions first
def demo_questions(request, attempt_id):
    attempt = get_object_or_404(InternAttempt, id=attempt_id)
    demo_qns = attempt.session.concept.questions.filter(is_demo=True).order_by("order")

    if request.method == "POST":
        return redirect("task_questions", attempt_id=attempt_id)

    return render(request, "aptitude/demo_questions.html", {
        "attempt": attempt,
        "demo_qns": demo_qns
    })


# # 6️⃣ Show real task questions
# def task_questions(request, attempt_id):
#     attempt = get_object_or_404(InternAttempt, id=attempt_id)
#     questions = attempt.selected_questions.all()

#     if request.method == "POST":
#         for q in questions:
#             ans = request.POST.get(f"answer_{q.id}")
#             exp = request.POST.get(f"explanation_{q.id}")

#             TaskAnswer.objects.create(
#                 attempt=attempt,
#                 question=q,
#                 intern_answer=ans,
#                 intern_explanation=exp,
#                 is_correct=(ans.strip() == q.correct_answer.strip())
#             )

#         return redirect("final_submit", attempt_id=attempt.id)

#     return render(request, "aptitude/task_questions.html", {
#         "attempt": attempt,
#         "questions": questions
#     })


from django.shortcuts import render, get_object_or_404, redirect
from .models import InternAttempt, TaskAnswer, Question

def normalize_answer(ans):
    """
    Normalize answer for comparison:
    - Strip spaces
    - Remove trailing '%' symbols
    - Remove currency symbols (₹, $) and commas
    - Convert to float if possible
    """
    if ans is None:
        return None
    ans = str(ans).strip()
    # Remove trailing % symbol
    if ans.endswith('%'):
        ans = ans[:-1]
    # Remove currency symbols and commas
    for sym in ['₹', '$', ',']:
        ans = ans.replace(sym, '')
    try:
        return float(ans)
    except ValueError:
        return ans.lower()  # fallback to lowercase string comparison

# 6️⃣ Show real task questions
def task_questions(request, attempt_id):
    attempt = get_object_or_404(InternAttempt, id=attempt_id)
    questions = attempt.selected_questions.all()

    if request.method == "POST":
        for q in questions:
            ans = request.POST.get(f"answer_{q.id}")
            exp = request.POST.get(f"explanation_{q.id}")

            intern_ans_normalized = normalize_answer(ans)
            correct_ans_normalized = normalize_answer(q.correct_answer)

            # Determine correctness
            is_correct = False
            if isinstance(intern_ans_normalized, float) and isinstance(correct_ans_normalized, float):
                # Allow tiny differences due to rounding
                is_correct = abs(intern_ans_normalized - correct_ans_normalized) < 0.01
            else:
                is_correct = intern_ans_normalized == correct_ans_normalized

            TaskAnswer.objects.create(
                attempt=attempt,
                question=q,
                intern_answer=ans,
                intern_explanation=exp,
                is_correct=is_correct
            )

        return redirect("final_submit", attempt_id=attempt.id)

    return render(request, "aptitude/task_questions.html", {
        "attempt": attempt,
        "questions": questions
    })


# 7️⃣ Final submit page
def final_submit(request, attempt_id):
    attempt = get_object_or_404(InternAttempt, id=attempt_id)
    attempt.submitted = True
    attempt.save()

    return render(request, "aptitude/final_submit.html", {"attempt": attempt})


# 8️⃣ Mentor view intern answers with validation
def view_attempt(request, attempt_id):
    attempt = get_object_or_404(InternAttempt, id=attempt_id)
    answers = TaskAnswer.objects.filter(attempt=attempt).select_related("question")

    return render(request, "aptitude/view_attempt.html", {
        "attempt": attempt,
        "answers": answers
    })
