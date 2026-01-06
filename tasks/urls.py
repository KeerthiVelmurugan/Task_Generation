from django.urls import path
from .views import GenerateTasksDocumentView, export_random_tasks, TasksByConceptView,ConceptListCreateView,ConceptDetailView
from .views import RandomTasksFromAllConceptsView,RandomTasksExportView, SendTasksToEmailAPIView
urlpatterns = [
    path('generate-tasks/', GenerateTasksDocumentView.as_view(), name='generate_tasks'),
    path('export/<int:concept_id>/', export_random_tasks, name='export_random_tasks'),
    path('concept/<int:concept_id>/tasks/', TasksByConceptView.as_view(), name='tasks_by_concept_api'),
    path('concepts/', ConceptListCreateView.as_view(), name='concept-list-create'),
    path('concepts/<int:pk>/', ConceptDetailView.as_view(), name='concept-detail'),
    # path('all_tasks/random/', RandomTasksFromAllConceptsView.as_view(), name='random-tasks-all-concepts'),
    #GET /api/tasks/random/?count=3
     path('all_tasks/random/', RandomTasksExportView.as_view(), name='random_tasks_export'),
    #GET /api/tasks/random/?count=3&export=true
    path('send-tasks-email/', SendTasksToEmailAPIView.as_view(), name='send_tasks_email'),

] 
