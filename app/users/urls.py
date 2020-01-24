from django.urls import path
from . import views as user_views

app_name = "users"
urlpatterns = [
    path("login/", view=user_views.LoginView.as_view(), name="login"),
    path("trello/oauth/", view=user_views.TrelloOAuthView.as_view(), name="trello_oauth"),
    path("oauth/<str:platform_name>", view=user_views.OAuthView.as_view(), name="oauth"),
]
