from django.urls import path

from rijkshuisstijl.views.generic import CreateView, DetailView, ListView, UpdateView, TemplateView
from tests.models import Book

app_name = "test"
fields = ("title", "authors", "publisher", "date_published", "stock")

urlpatterns = [
    path("template", TemplateView.as_view(), name="template"),
    path("create", CreateView.as_view(model=Book, fields=fields), name="create"),
    path("<int:pk>", DetailView.as_view(model=Book, fields=fields), name="detail"),
    path("", ListView.as_view(model=Book, fields=fields, paginate_by=2), name="list"),
    path("<int:pk>/update", UpdateView.as_view(model=Book, fields=fields), name="update"),
]
