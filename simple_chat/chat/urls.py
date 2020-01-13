from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<warning>', views.index, name='index'),
    path('send_message/', views.send_message, name='send_message'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]