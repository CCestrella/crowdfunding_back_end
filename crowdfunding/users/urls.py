from django.urls import path
from . import views

urlpatterns = [
    path('athletes/', views.CustomUserList.as_view()),
    path('athletes/<int:pk>/', views.CustomUserDetail.as_view()),
]
