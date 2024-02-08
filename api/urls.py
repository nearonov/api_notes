from django.urls import path
from api.views import NoteListView, NoteDetailView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns =[
    path('notes/', NoteListView.as_view()),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='notes-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
