from django.urls import path
from . import views

urlpatterns = [
    # Athlete Profile URLs
    path('athletes/', views.AthleteProfileList.as_view(), name='athlete-profile-list'),
    path('athlete/new/', views.AthleteProfileCreate.as_view(), name='athlete-profile-create'),
    path('athletes/<int:pk>/', views.AthleteProfileDetail.as_view(), name='athlete-profile-detail'),

    # Pledge URLs
    path('pledges/', views.PledgeList.as_view(), name='pledge-list'),
    path('pledges/<int:pk>/', views.PledgeDetail.as_view(), name='pledge-detail'),

    # Progress Update URLs
    path('updates/', views.ProgressUpdateList.as_view(), name='progress-update-list'),
    path('updates/<int:pk>/', views.ProgressUpdateDetail.as_view(), name='progress-update-detail'),
]
