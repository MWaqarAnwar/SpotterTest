
from django.urls import path
from . import views


urlpatterns = [
    path('fetch_smart_route/', views.FetchSmartRouteAPIView.as_view(), name='fetch_smart_route'),
]