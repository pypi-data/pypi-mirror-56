from django.test import TestCase, RequestFactory
from django.urls import reverse_lazy

from rijkshuisstijl.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView
from ...models import Book, Publisher, Author


class ViewTestCaseMixin:
    url_name = ""

    def client_get(self):
        url_name = self.url_name

        try:
            kwargs = {"pk": self.object.pk}
        except AttributeError:
            kwargs = None

        return self.client.get(reverse_lazy(url_name, kwargs=kwargs))

    def test_200(self):
        response = self.client_get()
        self.assertEqual(response.status_code, 200)

    def test_template_base(self):
        response = self.client_get()
        self.assertTemplateUsed(response, template_name="rijkshuisstijl/views/abstract/master.html")
        self.assertTemplateUsed(response, template_name="rijkshuisstijl/views/abstract/base.html")

    def test_script(self):
        response = self.client_get()
        self.assertContains(response, "rijkshuisstijl.js")

    def test_css(self):
        response = self.client_get()
        self.assertContains(response, "screen.css")


class FormTestCaseMixin:
    def setUp(self):
        Publisher.objects.create()
        Author.objects.create()

    def client_get_form(self, fields):
        kwargs = {"model": Book, "fields": fields}

        factory = RequestFactory()
        request = factory.get("/foo")
        view = self.view.as_view(**kwargs)

        try:
            return view(request, pk=self.object.pk)
        except AttributeError:
            return view(request)

    def test_template(self):
        response = self.client_get()
        self.assertTemplateUsed(response, template_name="rijkshuisstijl/views/abstract/form.html")

    def test_context_default(self):
        response = self.client_get()
        context = response.context_data.get("form_config")

        self.assertEqual(context.get("label"), None)
        self.assertEqual(context.get("status"), "info")
        self.assertEqual(context.get("title"), None)
        self.assertEqual(context.get("text"), None)
        self.assertEqual(context.get("wysiwyg"), None)

    def test_context_custom(self):
        kwargs = {
            "model": Book,
            "fields": ("title",),
            "label": "lorem ipsum",
            "status": "warning",
            "title": "foo",
            "text": "bar",
            "wysiwyg": "<p>baz</p>",
        }

        factory = RequestFactory()
        request = factory.get("/foo")
        view = self.view.as_view(**kwargs)

        try:
            response = view(request, pk=self.object.pk)
        except AttributeError:
            response = view(request)

        context = response.context_data.get("form_config")

        self.assertEqual(context.get("label"), "lorem ipsum")
        self.assertEqual(context.get("status"), "warning")
        self.assertEqual(context.get("title"), "foo")
        self.assertEqual(context.get("text"), "bar")
        self.assertEqual(context.get("wysiwyg"), "<p>baz</p>")

    def test_method(self):
        response = self.client_get()
        self.assertContains(response, 'method="post"')

    def test_enctype(self):
        response = self.client_get()
        self.assertContains(response, 'enctype="multipart/form-data"')

    def test_fields_visible(self):
        response = self.client_get_form(
            (
                "authors",
                "publisher",
                "available",
                "date_published",
                "last_updated",
                "stock",
                "title",
            )
        )
        form = response.context_data.get("form")

        for field_name in form._meta.fields:
            self.assertContains(response, 'name="{}"'.format(field_name))

    def test_fields_invisible(self):
        response = self.client_get_form(("title",))
        self.assertNotContains(response, 'name="{}"'.format("available"))

    def test_boolean_field(self):
        response = self.client_get_form(("available",))
        self.assertContains(response, 'type="{}"'.format("checkbox"))

    def test_decimal_field(self):
        response = self.client_get_form(("avg_rating",))
        self.assertContains(response, 'type="{}"'.format("number"))

    def test_date_field(self):
        response = self.client_get_form(("date_published",))
        self.assertContains(response, 'type="{}"'.format("date"))

    def test_datetime_field(self):
        response = self.client_get_form(("last_updated",))
        self.assertContains(response, 'type="{}"'.format("text"))

    def test_integer_field(self):
        response = self.client_get_form(("stock",))
        self.assertContains(response, 'type="{}"'.format("number"))

    def test_submit(self):
        response = self.client_get_form([])
        self.assertContains(response, 'type="{}"'.format("submit"))


class TemplateViewTestCase(ViewTestCaseMixin, TestCase):
    url_name = "template"
    view = TemplateView

    def test_context_default(self):
        response = self.client_get()
        context = response.context_data.get("textbox_config")

        self.assertEqual(context.get("status"), None)
        self.assertEqual(context.get("title"), None)
        self.assertEqual(context.get("text"), None)
        self.assertEqual(context.get("wysiwyg"), None)

    def test_context_custom(self):
        kwargs = {"status": "success", "title": "foo", "text": "bar", "wysiwyg": "<p>baz</p>"}

        factory = RequestFactory()
        request = factory.get("/foo")
        view = self.view.as_view(**kwargs)
        response = view(request)
        context = response.context_data.get("textbox_config")

        self.assertEqual(context.get("status"), "success")
        self.assertEqual(context.get("title"), "foo")
        self.assertEqual(context.get("text"), "bar")
        self.assertEqual(context.get("wysiwyg"), "<p>baz</p>")

    def test_template(self):
        response = self.client_get()
        self.assertTemplateUsed(
            response, template_name="rijkshuisstijl/views/generic/template.html"
        )

    def test_components(self):
        response = self.client_get()
        self.assertTemplateUsed(
            response, template_name="rijkshuisstijl/components/textbox/textbox.html"
        )


class CreateViewTestCase(ViewTestCaseMixin, FormTestCaseMixin, TestCase):
    url_name = "create"
    view = CreateView

    def test_template(self):
        response = self.client_get()
        self.assertTemplateUsed(response, template_name="rijkshuisstijl/views/generic/create.html")

    def test_components(self):
        response = self.client_get()
        self.assertTemplateUsed(response, template_name="rijkshuisstijl/components/form/form.html")


class DetailViewTestCase(ViewTestCaseMixin, TestCase):
    url_name = "detail"
    view = DetailView

    def setUp(self):
        self.publisher = Publisher.objects.create()
        self.author = Author.objects.create()
        self.object = Book.objects.create(publisher=self.publisher)
        self.object.authors.set((self.author,))

    def test_context_default(self):
        response = self.client_get()
        context_toolbar = response.context_data.get("toolbar_config")
        context_key_value_table = response.context_data.get("key_value_table_config")

        self.assertEqual(context_toolbar, None)

        self.assertEqual(context_key_value_table.get("class"), "key-value-table--justify")
        self.assertEqual(context_key_value_table.get("object"), self.object)
        self.assertEqual(
            context_key_value_table.get("fields"),
            ("title", "authors", "publisher", "date_published", "stock"),
        )

    def test_context_custom(self):
        author = self.author

        class View(self.view):
            def get_object(self):
                return author

        kwargs = {"fields": ("first_name", "last_name"), "model": Author}

        factory = RequestFactory()
        request = factory.get("/foo")

        view = View.as_view(**kwargs)

        response = view(request)
        context = response.context_data.get("key_value_table_config")

        self.assertEqual(context.get("fields"), ("first_name", "last_name"))
        self.assertEqual(context.get("object"), self.author)

    def test_template(self):
        response = self.client_get()
        self.assertTemplateUsed(response, template_name="rijkshuisstijl/views/generic/detail.html")

    def test_components(self):
        response = self.client_get()
        self.assertTemplateUsed(
            response, template_name="rijkshuisstijl/components/title-header/title-header.html"
        )
        self.assertTemplateUsed(
            response, template_name="rijkshuisstijl/components/key-value-table/key-value-table.html"
        )

    def test_toolbar(self):
        book = self.object

        class View(self.view):
            def get_object(self):
                return book

        kwargs = {
            "fields": ("title",),
            "model": Book,
            "toolbar_config": {
                "items": [
                    {
                        "href": "#",
                        "label": "Foo",
                        "title": "Bar",
                        "icon_src": "data:image/png;base64",
                    }
                ]
            },
        }

        factory = RequestFactory()
        request = factory.get("/foo")

        view = View.as_view(**kwargs)

        response = view(request)
        self.assertContains(response, "toolbar")

    def test_fields_visible(self):
        response = self.client_get()
        fields = ("title", "authors", "publisher", "date published", "stock")
        for field in fields:
            self.assertContains(response, field)

    def test_fields_invisible(self):
        response = self.client_get()
        self.assertNotContains(response, "last updated")
        self.assertNotContains(response, "last_updated")


class ListViewTestCase(ViewTestCaseMixin, TestCase):
    url_name = "list"
    view = ListView

    def setUp(self):
        self.publisher_1 = Publisher.objects.create(name="foo")
        self.publisher_2 = Publisher.objects.create(name="bar")

        self.author_1 = Author.objects.create(first_name="John", last_name="Doe")
        self.author_2 = Author.objects.create(first_name="Joe", last_name="Average")

        self.book_1 = Book.objects.create(title="Lorem", publisher=self.publisher_1)
        self.book_1.authors.set((self.author_1,))

        self.book_2 = Book.objects.create(title="Ipsum", publisher=self.publisher_2)
        self.book_2.authors.set((self.author_2,))

        self.book_3 = Book.objects.create(title="Dolor", publisher=self.publisher_1)
        self.book_3.authors.set((self.author_1, self.author_2))

    def test_context_default(self):
        response = self.client_get()
        context = response.context_data.get("datagrid_config")

        self.assertEqual(
            context.get("columns"), ("title", "authors", "publisher", "date_published", "stock")
        )
        self.assertEqual(context.get("queryset")[0], self.book_1)
        self.assertEqual(context.get("queryset")[1], self.book_2)
        self.assertEqual(context.get("queryset")[2], self.book_3)
        self.assertEqual(context.get("modifier_key"), None)
        self.assertEqual(context.get("modifier_column"), None)
        self.assertEqual(context.get("ordering_key"), "ordering")

    def test_template(self):
        response = self.client_get()
        self.assertTemplateUsed(response, template_name="rijkshuisstijl/views/generic/list.html")

    def test_components(self):
        response = self.client_get()
        self.assertTemplateUsed(
            response, template_name="rijkshuisstijl/components/datagrid/datagrid.html"
        )

    def test_paginator(self):
        response = self.client_get()
        self.assertContains(response, "paginator")

    def test_fields_visible(self):
        response = self.client_get()
        fields = ("title", "authors", "publisher", "date published", "stock")
        for field in fields:
            self.assertContains(response, field)

    def test_fields_invisible(self):
        response = self.client_get()
        self.assertNotContains(response, "last updated")
        self.assertNotContains(response, "last_updated")


class UpdateViewTestCase(ViewTestCaseMixin, FormTestCaseMixin, TestCase):
    url_name = "update"
    view = UpdateView

    def setUp(self):
        self.publisher = Publisher.objects.create()
        self.author = Author.objects.create()
        self.object = Book.objects.create(publisher=self.publisher)
        self.object.authors.set((self.author,))

    def test_template(self):
        response = self.client_get()
        self.assertTemplateUsed(response, template_name="rijkshuisstijl/views/generic/update.html")

    def test_components(self):
        response = self.client_get()
        self.assertTemplateUsed(response, template_name="rijkshuisstijl/components/form/form.html")
