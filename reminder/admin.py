from django.contrib import admin
from reminder.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'due_date', 'is_finished', 'is_notified'
                    ]


admin.site.register(Task, TaskAdmin)
