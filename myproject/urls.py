
from django.contrib import admin
from django.urls import path
from users.views import HomeView, LoginView, SignupView,UserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('home/<int:id>/user/', UserView.as_view(), name='home-detail'),

]
