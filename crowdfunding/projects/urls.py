from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # API routes
    path('api/', include([
        path('athletes/', views.AthleteProfileList.as_view(), name='athlete-profile-list'),
        path('athlete/new/', views.AthleteProfileCreate.as_view(), name='athlete-profile-create'),
        path('athletes/<int:pk>/', views.AthleteProfileDetail.as_view(), name='athlete-profile-detail'),
        path('my-athletes/', views.UserAthletesList.as_view(), name='user-athletes-list'),
        path('my-athletes/<int:pk>/', views.UserAthleteDetail.as_view(), name='user-athlete-detail'),

        # Pledge URLs
        path('pledges/', views.PledgeList.as_view(), name='pledge-list'),
        path('pledges/<int:pk>/', views.PledgeDetail.as_view(), name='pledge-detail'),

        # Progress Update URLs
        path('updates/', views.ProgressUpdateList.as_view(), name='progress-update-list'),
        path('updates/<int:pk>/', views.ProgressUpdateDetail.as_view(), name='progress-update-detail'),
    ])),

    # Catch-all route for React frontend
    path('', TemplateView.as_view(template_name="index.html"), name="react-app"),
]
