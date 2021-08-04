from django.urls import path
from .views import IncomeListAPIView, IncomeDetailAPIView

app_name = "income"
urlpatterns = [
    path("", IncomeListAPIView.as_view(), name="list_income"),
    path("<int:id>", IncomeDetailAPIView.as_view(), name="list_income")
]
