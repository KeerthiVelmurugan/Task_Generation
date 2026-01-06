from django.core.mail import send_mail
from django.utils import timezone
from .models import DailyTaskProgress, Task

def send_daily_tasks():
    today = timezone.now().date()
    progresses = DailyTaskProgress.objects.filter(is_active=True)

    for progress in progresses:
        if progress.last_sent_date == today:
            continue  # Already sent today

        tasks = Task.objects.filter(concept=progress.concept).order_by('id')
        if progress.current_task_index < len(tasks):
            task_to_send = tasks[progress.current_task_index]
            intern = progress.intern

            send_mail(
                subject=f"Today's Task: {task_to_send.title}",
                message=task_to_send.description,
                from_email='keerthi@gtcollege.in',
                recipient_list=[intern.email],
            )

            # Update progress
            progress.current_task_index += 1
            progress.last_sent_date = today
            progress.save()
        else:
            progress.is_active = False
            progress.save()
