from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('refresh', TokenRefreshView.as_view(), name='refresh'),
    path('users', views.UserListView.as_view(), name='user-list'),
    path('uavs', views.UAVListCreateView.as_view(), name='uav-list-create'),
    path('uavs/<int:pk>', views.UAVRetrieveUpdateDestroyView.as_view(), name='uav-detail'),
    path('rentals', views.RentalListView.as_view(), name='rental-list'),
    path('rentals/<int:pk>', views.RentalRetrieveUpdateDestroyView.as_view(), name='rental-detail'),
    path('uavs/<int:pk>/rent', views.RentUAVView.as_view(), name='uav-rent')
]
