from django.urls import path
from .views import SignUpView, CustomUserList, CustomUserDetail

urlpatterns = [
    # User-related endpoints
    path('', SignUpView.as_view(), name='user-sign-up'),  # Now accessible at /users/
    path('athletes/', CustomUserList.as_view(), name='custom-user-list'),
    path('athletes/<int:pk>/', CustomUserDetail.as_view(), name='custom-user-detail'),
]
