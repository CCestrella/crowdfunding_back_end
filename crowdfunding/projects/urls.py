from django.urls import path
from . import views

urlpatterns = [
    # Athlete Profile URLs
    path('athletes/', views.AthleteProfileList.as_view(), name='athlete-profile-list'),  # List athletes
    path('athlete/new/', views.AthleteProfileCreate.as_view(), name='athlete-profile-create'),  # Create a new athlete
    path('athletes/<int:pk>/', views.AthleteProfileDetail.as_view(), name='athlete-profile-detail'),  # Specific athlete details

    # Pledge URLs
    path('pledges/', views.PledgeList.as_view(), name='pledge-list'),
    path('pledges/<int:pk>/', views.PledgeDetail.as_view(), name='pledge-detail'),

    # Progress Update URLs
    path('updates/', views.ProgressUpdateList.as_view(), name='progress-update-list'),
    path('updates/<int:pk>/', views.ProgressUpdateDetail.as_view(), name='progress-update-detail'),

    # Badge URLs
    path('badges/', views.BadgeList.as_view(), name='badge-list'),
    path('badges/<int:pk>/', views.BadgeDetail.as_view(), name='badge-detail'),
]
