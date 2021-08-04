from django.urls import path
from .views import ExpenseListAPIView, ExpenseDetailAPIView

app_name = "expenses"
urlpatterns = [
    path("", ExpenseListAPIView.as_view(), name="list_expenses"),
    path("<int:id>", ExpenseDetailAPIView.as_view(), name="detail_expenses")
]
