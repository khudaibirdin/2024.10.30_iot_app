from django.urls import path

from web_app.views import *

urlpatterns = [
    path('about/', page_about, name='page_about'),
    path('sensors/', page_sensors, name='page_sensors'),
    path('sensors/single/', page_sensors_single, name='page_sensors_single'),
    path('variables/single/', page_variables_single, name='page_variables_single'),
    path('', page_main),
    path('variables', page_variables),
    path('variables/single/post', page_variables_single_post, name='page_variables_single_post'),
]