from . import views
from django.urls import path, include

urlpatterns = [
    path("", views.index, name="index"),
    path('reading-session/', views.sessionform, name='reading_session'),
    path("newsfeed/", views.newsfeed, name="newsfeed"),
    path('recent-sessions/', views.session_list, name='RecentSessions'),
    path('edit-session/<int:pk>/', views.edit_session, name='edit_session'),
    path("", include('django.contrib.auth.urls')),
    path("register/", views.register, name="register"),
    
    #path("nameform/", views.nameForm, name="nameform")
]