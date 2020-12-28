from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "myapp"

urlpatterns = [
    path('', views.index, name='index'),
    path('api/checked', views.result_list),
    path('api/site_check/<url>', views.detail),
]
