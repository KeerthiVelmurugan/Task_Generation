from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Task
from .forms import TaskGeneratorForms, TaskGeneratorForm
from django.core.mail import EmailMessage
import random
from io import BytesIO
from docx import Document

from django.contrib import messages
from django.shortcuts import render, redirect


# 🧠 Generate Tasks
from .models import Intern  # import your Intern model

# def generate_tasks(request):
#     try:
#         generated_tasks = []
#         interns = Intern.objects.filter(mentor=request.user)  # get all interns

#         if request.method == "POST":
#             form = TaskGeneratorForm(request.POST)
#             if form.is_valid():
#                 languages = form.cleaned_data['languages']
#                 concepts = form.cleaned_data['concepts']
#                 num = form.cleaned_data['number_of_tasks']

#                 all_tasks = Task.objects.filter(concept__language__in=languages)
#                 if concepts.exists():
#                     all_tasks = all_tasks.filter(concept__in=concepts)

#                 generated_tasks = random.sample(list(all_tasks), min(num, all_tasks.count()))
#                 request.session['task_data'] = [task.description for task in generated_tasks]
#         else:
#             form = TaskGeneratorForm()

#         return render(
#             request,
#             'generate_tasks.html',
#             {
#                 'form': form,
#                 'tasks': generated_tasks,
#                 'interns': interns,  # pass interns to template
#             }
#         )
#     except Exception as e:
#         return HttpResponse(f"❌ Error while generating tasks: {e}")




import random
import logging

from django.contrib import messages
from django.shortcuts import render

logger = logging.getLogger(__name__)


def generate_tasks(request):
    generated_tasks = []
    interns = Intern.objects.filter(mentor=request.user)

    if request.method == "POST":
        form = TaskGeneratorForm(request.POST)

        if form.is_valid():
            languages = form.cleaned_data["languages"]
            concepts = form.cleaned_data["concepts"]
            num = form.cleaned_data["number_of_tasks"]

            try:
                all_tasks = Task.objects.filter(
                    concept__language__in=languages
                )

                if concepts.exists():
                    all_tasks = all_tasks.filter(
                        concept__in=concepts
                    )

                # Remove duplicate tasks
                all_tasks = list(all_tasks.distinct())

                # Check whether tasks are available
                if not all_tasks:
                    messages.warning(
                        request,
                        "No tasks found under the selected concepts. "
                        "Please add tasks first."
                    )
                    request.session.pop("task_data", None)

                else:
                    # Generate the requested number of tasks,
                    # or all available tasks if fewer exist
                    count = min(num, len(all_tasks))
                    generated_tasks = random.sample(
                        all_tasks, count
                    )

                    request.session["task_data"] = [
                        task.description
                        for task in generated_tasks
                    ]

                    messages.success(
                        request,
                        f"{len(generated_tasks)} task(s) "
                        "generated successfully!"
                    )

                    if len(generated_tasks) < num:
                        messages.info(
                            request,
                            f"Only {len(generated_tasks)} task(s) "
                            "are available for your selection."
                        )

            except Exception:
                logger.exception("Error while generating tasks")
                messages.error(
                    request,
                    "Something went wrong while generating tasks. "
                    "Please try again."
                )

        else:
            messages.error(
                request,
                "Please select valid languages and concepts"
            )

    else:
        form = TaskGeneratorForm()

    return render(
        request,
        "generate_tasks.html",
        {
            "form": form,
            "tasks": generated_tasks,
            "interns": interns,
        }
    )


# def generate_task(request):
#     generated_tasks = []
#     interns = Intern.objects.filter(mentor=request.user)

#     if request.method == "POST":
#         form = TaskGeneratorForms(request.POST)
#         if form.is_valid():
#             languages = form.cleaned_data['languages']
#             concepts = form.cleaned_data['concepts']
#             num = form.cleaned_data['number_of_tasks']

#             all_tasks = Task.objects.filter(concept__language__in=languages)

#             if concepts:
#                 all_tasks = all_tasks.filter(concept__in=concepts)

#             generated_tasks = random.sample(
#                 list(all_tasks),
#                 min(num, all_tasks.count())
#             )

#             request.session['task_data'] = [t.description for t in generated_tasks]
#     else:
#         form = TaskGeneratorForms()

#     return render(request, 'generateTask.html', {
#         'form': form,
#         'tasks': generated_tasks,
#         'interns': interns
#     })

def get_concept(request):
    language_ids = request.GET.getlist('language_ids')

    concepts = Concept.objects.filter(language_id__in=language_ids)

    data = [{'id': c.id, 'name': c.name} for c in concepts]
    return JsonResponse(data, safe=False)






# 💾 Download as Word File
def download_word(request):
    try:
        task_data = request.session.get('task_data', [])
        if not task_data:
            return redirect('generate_tasks')

        doc = Document()
        doc.add_heading('Generated Tasks', 0)
        for i, task in enumerate(task_data, 1):
            doc.add_paragraph(f"{i}. {task}")

        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        response = HttpResponse(
            buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = 'attachment; filename="generated_tasks.docx"'
        return response
    except Exception as e:
        return HttpResponse(f"❌ Error while downloading file: {e}")


# 📧 Send Tasks via Email
# def send_email(request):
#     try:
#         task_data = request.session.get('task_data', [])
#         if not task_data:
#             return redirect('generate_tasks')

#         # Get selected interns (can be multiple)
#         intern_emails = request.POST.getlist('interns')  # note getlist() for multi-select
#         print(intern_emails)
#         if not intern_emails:
#             return redirect('generate_tasks')

#         # Prepare message
#         message = "\n".join([f"{i+1}. {t}" for i, t in enumerate(task_data)])
#         email = EmailMessage(
#             'Your Generated Tasks',
#             message,
#             'mkeerthilakshmi@gmail.com',  # your sender email
#             to=[],  # leave 'to' empty
#             bcc=intern_emails  # send to all selected interns
#         )
#         email.send(fail_silently=False)

#         return redirect('generate_tasks')

#     except Exception as e:
#         print("Email send error:", e)
#         return redirect('/generate-tasks?email_sent=false')


import logging
import resend

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


def send_email(request):
    if request.method != "POST":
        return redirect("generate_tasks")

    task_data = request.session.get("task_data", [])
    intern_emails = request.POST.getlist("interns")

    if not task_data:
        messages.error(
            request,
            "No generated tasks found. Please generate tasks first."
        )
        return redirect("generate_tasks")

    if not intern_emails:
        messages.warning(
            request,
            "Please select at least one intern."
        )
        return redirect("generate_tasks")

    # Only allow emails belonging to this mentor's interns
    allowed_emails = set(
        Intern.objects.filter(
            mentor=request.user
        ).values_list("email", flat=True)
    )

    intern_emails = list(dict.fromkeys(
        email for email in intern_emails
        if email in allowed_emails
    ))

    if not intern_emails:
        messages.error(
            request,
            "No valid intern email addresses were selected."
        )
        return redirect("generate_tasks")

    if not settings.RESEND_API_KEY:
        messages.error(
            request,
            "Email service is not configured. Please contact the administrator."
        )
        return redirect("generate_tasks")

    task_message = "\n".join(
        f"{i + 1}. {task}"
        for i, task in enumerate(task_data)
    )

    resend.api_key = settings.RESEND_API_KEY
    sent_count = 0

    try:
        for recipient in intern_emails:
            resend.Emails.send({
                "from": settings.RESEND_FROM_EMAIL,
                "to": [recipient],
                "subject": "Your Generated Tasks",
                "text": (
                    "Hello,\n\n"
                    "Here are your generated tasks:\n\n"
                    f"{task_message}\n\n"
                    "Please complete the assigned tasks."
                ),
            })

            sent_count += 1

        messages.success(
            request,
            f"Tasks emailed successfully to {sent_count} intern(s)!"
        )

    except Exception:
        logger.exception(
            "Resend email delivery request failed"
        )

        if sent_count:
            messages.warning(
                request,
                f"Email requests succeeded for {sent_count} intern(s), "
                "but sending stopped because another request failed. "
                "Check the server logs."
            )
        else:
            messages.error(
                request,
                "Unable to send emails. Check your Resend API key, "
                "sender verification, and Render logs."
            )

    return redirect("generate_tasks")



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, LoginForm

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Signup successful! Please login.")
            return redirect('login_view')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('generate_tasks')
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login_view')

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def profile_view(request):
    try:
        user = request.user

        if request.method == 'POST':
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')

        return render(request, 'profile.html', {'user': user})
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('profile')


@login_required
def change_password(request):
    try:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
        else:
            form = PasswordChangeForm(request.user)

        return render(request, 'change_password.html', {'form': form})
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('profile')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Language, Concept, Task
from .forms import LanguageForm, ConceptForm, TaskForm

# ✅ Add Language
@login_required
def add_language(request):
    try:
        if request.method == 'POST':
            form = LanguageForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Language added successfully!')
                return redirect('add_language')
        else:
            form = LanguageForm()
        languages = Language.objects.all()
        return render(request, 'add_language.html', {'form': form, 'languages': languages})
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('generate_tasks')


# ✅ Add Concept
@login_required
def add_concept(request):
    try:
        # Get selected language from GET for filtering concepts
        selected_lang_id = request.GET.get('language')
        if selected_lang_id:
            concepts = Concept.objects.filter(language_id=selected_lang_id)
        else:
            concepts = Concept.objects.none()

        if request.method == 'POST':
            form = ConceptForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Concept added successfully!')
                # Redirect to preserve selected language
                return redirect(f"{request.path}?language={form.cleaned_data['language'].id}")
        else:
            form = ConceptForm()

        languages = Language.objects.all()
        return render(request, 'add_concept.html', {
            'form': form,
            'languages': languages,
            'concepts': concepts,
            'selected_lang_id': selected_lang_id
        })
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('generate_tasks')

# ✅ Add Task
# @login_required
# def add_task(request):
#     try:
#         if request.method == 'POST':
#             form = TaskForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, 'Task added successfully!')
#                 return redirect('add_task')
#         else:
#             form = TaskForm()
#         tasks = Task.objects.select_related('concept', 'concept__language').all()
#         return render(request, 'add_task.html', {'form': form, 'tasks': tasks})
#     except Exception as e:
#         messages.error(request, f"Error: {str(e)}")
#         return redirect('generate_tasks')
@login_required
def add_task(request):
    try:
        if request.method == 'POST':
            concept_id = request.POST.get('concept')
            description = request.POST.get('description')
            if concept_id and description:
                concept = Concept.objects.get(id=concept_id)
                Task.objects.create(concept=concept, description=description)
                messages.success(request, 'Task added successfully!')
                return redirect('add_task')

        languages = Language.objects.all()
        return render(request, 'add_task.html', {'languages': languages})
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('generate_tasks')

    
    
from django.http import JsonResponse

# Get concepts for selected language
def get_concepts(request, language_id):
    try:
        concepts = Concept.objects.filter(language_id=language_id).values('id', 'name')
        return JsonResponse({'concepts': list(concepts)})
    except Exception as e:
        return JsonResponse({'error': str(e)})

# Get tasks for selected concept
def get_tasks(request, concept_id):
    try:
        tasks = Task.objects.filter(concept_id=concept_id).values('id', 'description')
        return JsonResponse({'tasks': list(tasks)})
    except Exception as e:
        return JsonResponse({'error': str(e)})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Language, Concept, Task
from .forms import LanguageForm, ConceptForm, TaskForm
from django.http import JsonResponse

# Delete Language
def delete_language(request, lang_id):
    lang = get_object_or_404(Language, id=lang_id)
    lang.delete()
    messages.success(request, 'Language deleted successfully!')
    return redirect('add_language')

# Delete Concept
def delete_concept(request, concept_id):
    concept = get_object_or_404(Concept, id=concept_id)
    concept.delete()
    messages.success(request, 'Concept deleted successfully!')
    return redirect('add_concept')

# Delete Task
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('add_task')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Intern
from .forms import InternForm

@login_required
def add_intern(request):
    """
    Add a new intern and display existing interns for the logged-in mentor.
    """
    if request.method == 'POST':
        form = InternForm(request.POST)
        if form.is_valid():
            intern = form.save(commit=False)
            intern.mentor = request.user  # Assign the logged-in user as mentor
            intern.save()
            messages.success(request, "Intern added successfully!")
            return redirect('add_intern')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = InternForm()

    # Display interns under this mentor; superuser sees all
    if request.user.is_superuser:
        interns = Intern.objects.all()
    else:
        interns = Intern.objects.filter(mentor=request.user)

    return render(request, 'add_intern.html', {'form': form, 'interns': interns})


@login_required
def delete_intern(request, intern_id):
    """
    Delete an intern. Mentor can only delete their own interns; superuser can delete all.
    """
    intern = get_object_or_404(Intern, id=intern_id)

    # Security check: only mentor or superuser can delete
    if intern.mentor != request.user and not request.user.is_superuser:
        messages.error(request, "You do not have permission to delete this intern.")
        return redirect('add_intern')

    intern.delete()
    messages.success(request, "Intern deleted successfully!")
    return redirect('add_intern')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Intern, Language, Concept, Task, DailyTaskProgress
from django.utils import timezone


def start_daily_tasks(request):
    
    print("🔥 JOB STARTED — APScheduler triggered the function! in views")
    print(f"🕘 Checking for daily tasks at {timezone.localtime()}")
    languages = Language.objects.all()
    interns = Intern.objects.filter(mentor=request.user)

    if request.method == "POST":
        language_id = request.POST.get("language")
        concept_id = request.POST.get("concept")
        intern_ids = request.POST.getlist("interns")

        language = Language.objects.get(id=language_id)
        concept = Concept.objects.get(id=concept_id)

        for intern_id in intern_ids:
            intern = Intern.objects.get(id=intern_id)

            # Create or reset progress
            DailyTaskProgress.objects.update_or_create(
                intern=intern,
                concept=concept,
                language=language,
                defaults={"current_task_index": 0, "active": True},
            )

        messages.success(request, "✅ Daily tasks started for selected interns!")
        return redirect("start_daily_tasks")

    return render(request, "start_daily_tasks.html", {"languages": languages, "interns": interns})
