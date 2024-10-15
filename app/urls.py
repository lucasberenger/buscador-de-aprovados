from django.urls import path
from .views import SignupView, LoginView, LogoutView, HomeView, ProfileView, EditProfileView, DetailsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('editprofile/', EditProfileView.as_view(), name='edit_profile'),
    path('candidato/<int:pk>/', DetailsView.as_view(), name='candidato_detail'),
]