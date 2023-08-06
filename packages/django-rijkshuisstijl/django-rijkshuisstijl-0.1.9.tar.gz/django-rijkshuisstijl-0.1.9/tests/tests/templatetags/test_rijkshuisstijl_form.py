from django import forms
from django.template import Context, Template
from django.test import RequestFactory, TestCase

from tests.models import Author, Book, Publisher


class FormTestCase(TestCase):
    def test_select_multiple(self):
        publisher = Publisher.objects.create(name="Foo")

        author_1 = Author.objects.create(first_name="Jane", last_name="Doe", pk=1)
        author_2 = Author.objects.create(first_name="John", last_name="Doe", pk=2)
        Author.objects.create(first_name="Joe", last_name="Average")

        book = Book.objects.create(publisher=publisher)
        book.authors.set((author_1, author_2))

        class BookForm(forms.ModelForm):
            class Meta:
                model = Book
                fields = ("authors",)

        form = BookForm(instance=book)

        config = Context({"form": form, "request": RequestFactory().get("/foo", {})})
        html = Template("{% load rijkshuisstijl %}{% form form %}").render(config)

        self.assertInHTML(
            '<option class="select__option" value="1" selected>Jane Doe</option>', html
        )
        self.assertInHTML(
            '<option class="select__option" value="2" selected>John Doe</option>', html
        )
