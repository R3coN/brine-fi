from django.urls import path
from alerts import views
from alerts.models import Alert

urlpatterns = [
    path('', views.AlertView.as_view()),
    path('<str:pk>', views.AlertDetail.as_view())
]