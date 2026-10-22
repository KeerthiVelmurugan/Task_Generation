from django.urls import path,include
from . import views

urlpatterns = [
    path('home/', views.generate_tasks, name='generate_tasks'),
    # path('generate-tasks/', views.generate_task, name='generate_task'),# new
    path('get-concepts/', views.get_concept, name='get_concept'), #new
    path('download-word/', views.download_word, name='download_word'),
    path('send-email/', views.send_email, name='send_email'),
    path('signup/', views.signup_view, name='signup_view'),
    path('', views.login_view, name='login_view'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
#     path('add-language/', views.add_language, name='add_language'),
#     path('add-concept/', views.add_concept, name='add_concept'),
#     path('add-task/', views.add_task, name='add_task'),
    # path('get-concepts/<int:language_id>/', views.get_concepts, name='get_concepts'),
#     path('get-tasks/<int:concept_id>/', views.get_tasks, name='get_tasks')
    path('add-language/', views.add_language, name='add_language'),
    path('delete-language/<int:lang_id>/', views.delete_language, name='delete_language'),
    
    path('add-concept/', views.add_concept, name='add_concept'),
    path('delete-concept/<int:concept_id>/', views.delete_concept, name='delete_concept'),

    path('add-task/', views.add_task, name='add_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),

    # AJAX endpoints
    path('get-concepts/<int:language_id>/', views.get_concepts, name='get_concepts'),
    path('get-tasks/<int:concept_id>/', views.get_tasks, name='get_tasks'),
    path('add-intern/', views.add_intern, name='add_intern'),
    path('delete-intern/<int:intern_id>/', views.delete_intern, name='delete_intern'),
    path('start-daily-tasks/', views.start_daily_tasks, name='start_daily_tasks'),

 ]
