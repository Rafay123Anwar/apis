# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import PatientViewSet,SignUpView, LoginView

# router = DefaultRouter()
# router.register(r'patients', PatientViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
#     path('signup/', SignUpView.as_view(), name='signup'),
#     path('login/', LoginView.as_view(), name='login'),
# ]

# # urlpatterns = [
# #     path('api/users/', include('users.urls')),
# # ]



# urls.py
from django.urls import path
from .views import SignupView, LoginView, ProfileView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:patient_id>/', ProfileView.as_view(), name='profile'),
]
