from django.contrib import admin
from notes.models import Note


@admin.register(Note)
class NoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'created']
