from django.contrib import admin
from .models import JoggingEntry
# Register your models here.

class JoggingEntryAdmin(admin.ModelAdmin):
    class Meta:
        model = JoggingEntry

admin.site.register(JoggingEntry, JoggingEntryAdmin)