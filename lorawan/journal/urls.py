from django.urls import path

from journal.views import *

urlpatterns = [
    path('page_journal/', page_journal),
]