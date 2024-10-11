from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("print_labels/", PrintLabelsView.as_view(), name="print-barcode"),
    # path("", HomeView.as_view(), name="home"),
]
