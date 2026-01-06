from django.contrib import admin
from full_stack.models import *
# Register your models here.
admin.site.register(Language)
admin.site.register(Concept)
# admin.site.register(Task)
admin.site.register(DailyTaskProgress)

class TaskAdmin(admin.ModelAdmin):
    list_display = ["id","concept", "description"]
    list_filter = ["concept"] 
    ordering = [ "-concept", "id",] 
    
admin.site.register(Task,TaskAdmin)