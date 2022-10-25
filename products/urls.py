from django.urls import path

from .views import (
    product_details_view,
    product_create_view,
)

app_name = "products"
urlpatterns = [
    path("<int:pk>/", product_details_view, name="product_details"),
    path("create/", product_create_view, name="product_create"),
]
