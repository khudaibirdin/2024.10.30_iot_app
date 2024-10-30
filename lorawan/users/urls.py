from django.urls import path, include
from users.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('page_auth/', page_auth),
    path('', include('django.contrib.auth.urls')),
    path('logout/', logout),
    path('account/', page_account),
    path('password/', password_change, name='password_change'),
]