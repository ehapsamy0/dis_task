from django.urls import path
from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),

    path('register/', views.RegisterUser.as_view(), name='register'),
    path('create-status/', views.CreateStatusAPIView.as_view(), name='CreateStatusAPIView'),
]