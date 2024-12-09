from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = "quotesapp"

urlpatterns = [
    path("", views.main, name="index"),
    path("authors/", views.authors, name="authors"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="quotesapp:index"),
        name="logout",
    ),
    path("authors/<int:author_id>/", views.author_detail, name="author_detail"),
    path('add-author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('change-password/', views.change_password, name='change_password'),
]
