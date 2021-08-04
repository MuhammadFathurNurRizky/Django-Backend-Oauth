from django.urls import path
from .views import GoogleSocialAuthView

app_name = "social_auth"
urlpatterns = [
    path("google/", GoogleSocialAuthView.as_view(), name="google")
]
