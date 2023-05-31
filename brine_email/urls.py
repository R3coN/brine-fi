from django.urls import path
from brine_email import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
]