from . import views
from django.urls import path, include

urlpatterns = [
    path("", views.index, name="index"),
    path("", include('django.contrib.auth.urls')),
    path('reading-session/', views.sessionform, name='reading_session'),
    path("newsfeed/", views.newsfeed, name="newsfeed"),
    path('recent-sessions/', views.session_list, name='RecentSessions'),
    path('edit-session/<int:pk>/', views.edit_session, name='edit_session'),
    path("register/", views.register, name="register"),
    path("profile_form/", views.profile_form, name="profile_form"),
    path("profile/", views.profile, name="profile"),
    path("newbook/", views.new_book, name="new_book"),
    path("unapproved_books/", views.unapproved_books, name="unapproved_books"),
    path("approve_book/<int:pk>/", views.approve_book, name="approve_book"),
    path("deny_book/<int:pk>/", views.deny_book, name="deny_book"),
    path("delete_session/<int:pk>/", views.delete_session, name="delete_session"),
]