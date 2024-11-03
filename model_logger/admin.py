from django.contrib import admin
from .models import LogEntry

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'level', 'message')
    search_fields = ('message',)
    list_filter = ('level',)
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)

admin.site.register(LogEntry, LogEntryAdmin)