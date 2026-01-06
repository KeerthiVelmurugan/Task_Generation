# from apscheduler.schedulers.background import BackgroundScheduler
# from django.utils import timezone
# from django.core.mail import send_mail
# from .models import DailyTaskProgress, Task

# def send_daily_tasks():
#     print(f"🕘 Checking for daily tasks at {timezone.localtime()}")

#     progresses = DailyTaskProgress.objects.filter(active=True)

#     for progress in progresses:
#         try:
#             # ✅ Get all tasks for that concept in order
#             tasks = Task.objects.filter(concept=progress.concept).order_by("id")

#             if not tasks.exists():
#                 print(f"⚠️ No tasks found for concept: {progress.concept.name}")
#                 continue

#             intern = progress.intern
#             concept_name = progress.concept.name
#             language_name = progress.concept.language.name

#             # ✅ Get the next task index
#             index = progress.current_task_index or 0

#             # ✅ If we still have tasks to send
#             if index < len(tasks):
#                 task = tasks[index]

#                 subject = f"📚 Daily Task - {language_name} ({concept_name})"
#                 message = (
#                     f"Hello {intern.name},\n\n"
#                     f"Here’s your task for today in {language_name} - {concept_name}:\n\n"
#                     f"🔹 {task.description}\n\n"
#                     "All the best!\n\n"
#                     "— Task Assignment System"
#                 )

#                 # ✅ Send email
#                 send_mail(
#                     subject,
#                     message,
#                     "keerthi@gtcollege.in",  # Replace with your verified sender
#                     [intern.email],
#                     fail_silently=False,
#                 )

#                 # ✅ Move to next task
#                 progress.current_task_index = index + 1
#                 progress.last_sent_at = timezone.now()

#                 # ✅ If all tasks are completed, stop sending
#                 if progress.current_task_index >= len(tasks):
#                     progress.active = False

#                 progress.save()

#                 print(f"✅ Sent task {index + 1}/{len(tasks)} to {intern.email}")

#             else:
#                 print(f"🎉 All tasks completed for {intern.name}")

#         except Exception as e:
#             print(f"❌ Error sending email to {progress.intern.email}: {e}")

# # ✅ Initialize scheduler
# def start():
#     scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
#     a_hour=16
#     a_minutes=10
#     scheduler.add_job(send_daily_tasks, 'cron', day_of_week='mon-sat', hour=a_hour, minute=a_minutes)
#     scheduler.start()
#     print(f"🔁 Scheduler started (Mon–Sat) {a_hour}:{a_minutes}")

from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from django.core.mail import send_mail
from .models import DailyTaskProgress, Task
import os

def send_daily_tasks():
    print("🔥 JOB STARTED — APScheduler triggered the function in schedular!")
    print(f"🕘 Checking for daily tasks at {timezone.localtime()}")

    # Only active tasks
    progresses = DailyTaskProgress.objects.filter(active=True)

    for progress in progresses:
        try:
            # Skip if today's task already sent
            if progress.last_sent_at is not None and progress.last_sent_at.date() >= timezone.now().date():
                continue

            tasks = Task.objects.filter(concept=progress.concept).order_by("id")
            if not tasks.exists():
                print(f"⚠️ No tasks found for concept: {progress.concept.name}")
                continue

            index = progress.current_task_index
            if index >= len(tasks):
                progress.active = False
                progress.save()
                continue

            task = tasks[index]
            intern = progress.intern
            concept_name = progress.concept.name
            language_name = progress.concept.language.name

            subject = f"📚 Daily Task - {language_name} ({concept_name})"
            message = (
                f"Hello {intern.name},\n\n"
                f"Here’s your task for today in {language_name} - {concept_name}:\n\n"
                f"🔹 {task.description}\n\n"
                "All the best!\n\n"
                "— Task Assignment System"
            )

            send_mail(
                subject,
                message,
                "keerthi@gtcollege.in",
                [intern.email],
                fail_silently=False,
            )

            # Update progress
            progress.current_task_index += 1
            progress.last_sent_at = timezone.now()
            if progress.current_task_index >= len(tasks):
                progress.active = False
            progress.save()

            print(f"✅ Sent task {index + 1}/{len(tasks)} to {intern.email}")

        except Exception as e:
            print(f"❌ Error sending email to {progress.intern.email}: {e}")

# Only start scheduler in main process to avoid duplicates
def start():
    if os.environ.get('RUN_MAIN') == 'true':
        scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
        scheduler.add_job(send_daily_tasks, 'cron', day_of_week='mon-sat', hour=9, minute=37)
        scheduler.start()
        print(f"🔁 Scheduler started (Mon–Sat) 9:35")
       
