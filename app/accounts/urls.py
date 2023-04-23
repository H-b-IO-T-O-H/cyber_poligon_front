from accounts import views
from django.urls import path

app_name = 'accounts'
urlpatterns = [

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.registration_view, name='registration'),
    path('settings/', views.settings_view, name='settings'),

]


