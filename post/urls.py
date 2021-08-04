from django.urls import path
from .views import CobaView, CobaDetail

app_name = "post"
urlpatterns = [
    path("", CobaView.as_view(), name="coba"),
    path("<int:id>/", CobaDetail.as_view(), name="cobaid"),
]
