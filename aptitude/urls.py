from django.urls import path
from . import views

urlpatterns = [
    path("apt-home/",views.home,name="apt-home"),
    path("assign/", views.assign_test, name="assign_test"),
    path("sessions/", views.session_list, name="session_list"),
    path("sessions/<int:session_id>/", views.session_detail, name="session_detail"),
    path('sessions/delete/<int:session_id>/', views.delete_session, name='delete_session'),
    path("start/<int:session_id>/", views.start_test, name="start_test"),
    path("demo/<int:attempt_id>/", views.demo_questions, name="demo_questions"),
    path("tasks/<int:attempt_id>/", views.task_questions, name="task_questions"),
    path("submit/<int:attempt_id>/", views.final_submit, name="final_submit"),

    path("attempt/<int:attempt_id>/", views.view_attempt, name="view_attempt"),
]
