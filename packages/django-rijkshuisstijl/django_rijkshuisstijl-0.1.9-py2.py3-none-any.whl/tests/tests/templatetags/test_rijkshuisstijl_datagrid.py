from django.core.paginator import Paginator
from django.template import Context, Template
from django.test import TestCase, RequestFactory

from ...models import Publisher, Author, Book


class DatagridTestCase(TestCase):
    def setUp(self):
        self.publisher_1 = Publisher.objects.create(name="Foo")
        self.publisher_2 = Publisher.objects.create(name="Bar")

        self.author_1 = Author.objects.create(first_name="John", last_name="Doe")
        self.author_2 = Author.objects.create(first_name="Joe", last_name="Average")

        self.book_1 = Book.objects.create(title="Lorem", publisher=self.publisher_1)
        self.book_1.authors.set((self.author_1,))

        self.book_2 = Book.objects.create(title="Ipsum", publisher=self.publisher_2)
        self.book_2.authors.set((self.author_2,))

        self.book_3 = Book.objects.create(title="Dolor", publisher=self.publisher_1)

    def template_render(self, config=None, data={}):
        config = config or {}
        config = Context({"config": config, "request": RequestFactory().get("/foo", data)})
        return Template("{% load rijkshuisstijl %}{% datagrid config=config %}").render(config)

    def test_render(self):
        self.assertTrue(self.template_render())

    def test_alternative_syntax(self):
        config = Context({"queryset": Book.objects.all(), "request": RequestFactory().get("/foo")})
        html = Template(
            '{% load rijkshuisstijl %}{% datagrid queryset=queryset columns="title,publisher__name:publisher name" orderable_columns="title,publisher__name" %}'
        ).render(config)
        self.assertInHTML(
            '<a class="datagrid__link" href="{}">{}</a>'.format("?ordering=title", "title"), html
        )
        self.assertInHTML(
            '<a class="datagrid__link" href="{}">{}</a>'.format(
                "?ordering=publisher__name", "publisher name"
            ),
            html,
        )
        self.assertInHTML("Lorem", html)
        self.assertInHTML("Foo", html)
        self.assertInHTML("Dolor", html)
        self.assertInHTML("Bar", html)

    def test_class(self):
        html = self.template_render()
        self.assertIn('class="datagrid"', html)

    def test_id(self):
        html = self.template_render({"id": "my-first-datagrid"})
        self.assertIn("my-first-datagrid", html)

    def test_auto_id_uuid4(self):
        html = self.template_render()
        self.assertRegex(
            html, r"datagrid-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
        )

    def test_no_results(self):
        html = self.template_render()
        self.assertInHTML("Geen resultaten", html)

    def test_columns(self):
        html = self.template_render({"columns": ("title", "publisher")})
        self.assertInHTML("title", html)
        self.assertInHTML("publisher", html)

    def test_rows(self):
        html = self.template_render(
            {"columns": ("title", "publisher"), "queryset": Book.objects.all()}
        )

        self.assertInHTML("Lorem", html)
        self.assertInHTML("Foo", html)
        self.assertInHTML("Dolor", html)
        self.assertInHTML("Bar", html)

    def test_filter(self):
        html = self.template_render(
            {
                "columns": ("title", "publisher"),
                "queryset": Book.objects.all(),
                "id": "my-first-datagrid",
                "filterable_columns": ["title"],
            },
            {"title": "m"},
        )

        self.assertInHTML(
            '<form id="datagrid-filter-form-my-first-datagrid" method="GET"><input class="input input--hidden" type="submit"></form>',
            html,
        )
        self.assertInHTML(
            '<input class="input" id="datagrid-filter-title-my-first-datagrid" form="datagrid-filter-form-my-first-datagrid" name="title" value="m" placeholder="title">',
            html,
        )
        self.assertInHTML("Lorem", html)
        self.assertInHTML("Ipsum", html)
        self.assertNotIn("Dolor", html)

    def test_orderable_columns_list(self):
        """
        Configure the table headers for ordering using a list.
        """
        html = self.template_render(
            {
                "columns": ("title", {"key": "publisher__name", "label": "publisher name"}),
                "orderable_columns": ["title", "publisher__name"],
            }
        )

        self.assertInHTML(
            '<a class="datagrid__link" href="{}">{}</a>'.format("?ordering=title", "title"), html
        )
        self.assertInHTML(
            '<a class="datagrid__link" href="{}">{}</a>'.format(
                "?ordering=publisher__name", "publisher name"
            ),
            html,
        )

    def test_orderable_columns_dict(self):
        """
        Configure the table headers for ordering using a dict.
        """
        html = self.template_render(
            {
                "columns": ("title", "author"),
                "orderable_columns": {"title": "title", "author": "author__first_name"},
            }
        )

        self.assertInHTML(
            '<a class="datagrid__link" href="{}">{}</a>'.format("?ordering=title", "title"), html
        )
        self.assertInHTML(
            '<a class="datagrid__link" href="{}">{}</a>'.format(
                "?ordering=author__first_name", "author"
            ),
            html,
        )

    def test_order_asc(self):
        """
        Let the datagrid order the queryset (ascending).
        :return:
        """
        html = self.template_render(
            {
                "columns": ("title", "publisher"),
                "queryset": Book.objects.all(),
                "order": True,
                "orderable_columns": ("title", "publisher"),
                "ordering_key": "o",
            },
            {"o": "title"},
        )

        book_1_pos = html.find(str(self.book_1))
        book_2_pos = html.find(str(self.book_2))
        book_3_pos = html.find(str(self.book_3))

        self.assertLess(book_3_pos, book_2_pos)
        self.assertLess(book_2_pos, book_1_pos)

    def test_order_desc(self):
        """
        Let the datagrid order the queryset (descending).
        :return:
        """
        html = self.template_render(
            {
                "columns": ("title", "publisher"),
                "queryset": Book.objects.all(),
                "order": True,
                "orderable_columns": ("title", "publisher"),
                "ordering_key": "o",
            },
            {"o": "-title"},
        )

        book_1_pos = html.find(str(self.book_1))
        book_2_pos = html.find(str(self.book_2))
        book_3_pos = html.find(str(self.book_3))

        self.assertGreater(book_3_pos, book_2_pos)
        self.assertGreater(book_2_pos, book_1_pos)

    def test_no_pagination(self):
        """
        Don't paginate the datagrid.
        """
        paginator = Paginator(Book.objects.all(), 2)
        page_number = 1
        page_obj = paginator.page(page_number)

        html = self.template_render(
            {
                "columns": ("title", "publisher"),
                "queryset": Book.objects.all(),
                "is_paginated": False,
                "paginator": paginator,
                "page_number": page_number,
                "page_obj": page_obj,
            }
        )

        self.assertNotIn("paginator", html)

    def test_paginate(self):
        """
        Let the datagrid paginate the queryset/object list.
        """

        # queryset
        html = self.template_render(
            {
                "columns": ("title", "publisher"),
                "queryset": Book.objects.all(),
                "paginate": True,
                "paginate_by": 2,
                "page_key": "p",
            },
            {"p": 2},
        )

        self.assertNotIn(str(self.book_1), html)
        self.assertNotIn(str(self.book_2), html)
        self.assertIn(str(self.book_3), html)
        self.assertIn("paginator", html)
        self.assertInHTML(
            '<input class="input" name="p" value="2" type="number" min="1" max="2">', html
        )

        # object_list
        html = self.template_render(
            {
                "columns": ("title", "publisher"),
                "object_list": [*Book.objects.all()],
                "paginate": True,
                "paginate_by": 2,
                "page_key": "p",
            },
            {"p": 2},
        )

        self.assertNotIn(str(self.book_1), html)
        self.assertNotIn(str(self.book_2), html)
        self.assertIn(str(self.book_3), html)
        self.assertIn("paginator", html)
        self.assertIn("paginator", html)
        self.assertInHTML(
            '<input class="input" name="p" value="2" type="number" min="1" max="2">', html
        )

    def test_pagination(self):
        """
        Pass an external paginator.
        """
        paginator = Paginator(Book.objects.all(), 2)
        page_number = 2
        page_obj = paginator.page(page_number)

        html = self.template_render(
            {
                "columns": ("title", "publisher"),
                "object_list": page_obj.object_list,
                "paginate": False,
                "is_paginated": True,
                "paginator": paginator,
                "page_key": "p",
                "page_number": page_number,
                "page_obj": page_obj,
            }
        )

        self.assertNotIn(str(self.book_1), html)
        self.assertNotIn(str(self.book_2), html)
        self.assertIn(str(self.book_3), html)
        self.assertIn("paginator", html)
        self.assertIn("paginator", html)
        self.assertInHTML(
            '<input class="input" name="p" value="2" type="number" min="1" max="2">', html
        )

    def test_custom_presentation(self):
        html = self.template_render(
            {
                "columns": ("title", "author"),
                "get_author_display": lambda book: book.authors.first(),
                "queryset": Book.objects.all(),
            }
        )

        self.assertInHTML("Lorem", html)
        self.assertInHTML("John Doe", html)
        self.assertInHTML("Dolor", html)
        self.assertInHTML("Joe Average", html)

    def test_form(self):
        html = self.template_render(
            {
                "columns": ("title"),
                "queryset": Book.objects.all(),
                "id": "my-first-datagrid",
                "form": True,
                "form_action": "/foo",
                "form_buttons": [
                    {"label": "Foo", "name": "Lorem", "icon_src": "data:image/png;base64,"},
                    {
                        "class": "button--danger",
                        "label": "Bar",
                        "name": "Ipsum",
                        "icon_src": "data:image/png;base64,",
                    },
                ],
                "form_checkbox_name": "bar",
            }
        )

        self.assertIn('id="my-first-datagrid"', html)
        self.assertIn('<form class="datagrid__form" method="post" action="/foo">', html)
        self.assertInHTML(
            '<button class="button button--small button--transparent" name="Lorem" title="Foo" ><span class="button__label">Foo</span><img class="icon icon--image" alt="Foo" src="data:image/png;base64,"></button>',
            html,
        )
        self.assertInHTML(
            '<button class="button button--small button--danger" name="Ipsum" title="Bar" ><span class="button__label">Bar</span><img class="icon icon--image" alt="Bar" src="data:image/png;base64,"></button>',
            html,
        )
        self.assertInHTML(
            '<input class="input select-all" type="checkbox" data-select-all="#my-first-datagrid .datagrid__cell--checkbox .input">',
            html,
        )
        self.assertInHTML('<input class="input" type="checkbox" name="bar" value="3">', html)

    def test_toolbar_position_top(self):
        html = self.template_render(
            {
                "columns": ("title"),
                "queryset": Book.objects.all(),
                "id": "my-first-datagrid",
                "form": True,
                "form_buttons": [
                    {"label": "Foo", "name": "Lorem", "icon_src": "data:image/png;base64,"},
                    {
                        "class": "button--danger",
                        "label": "Bar",
                        "name": "Ipsum",
                        "icon_src": "data:image/png;base64,",
                    },
                ],
                "toolbar_position": "top",
            }
        )

        header_html = '<header class="datagrid__header"><div class="toolbar toolbar--pad toolbar--justify"><ul class="toolbar__list"><li class="toolbar__list-item"><button class="button button--small button--transparent" name="Lorem" title="Foo" ><span class="button__label">Foo</span><img class="icon icon--image" alt="Foo" src="data:image/png;base64,"></button></li><li class="toolbar__list-item"><button class="button button--small button--danger" name="Ipsum" title="Bar" ><span class="button__label">Bar</span><img class="icon icon--image" alt="Bar" src="data:image/png;base64,"></button></li></ul><ul class="toolbar__list"><li class="toolbar__list-item"><div class="filter filter--class-only filter--filter" data-filter-target="#my-first-datagrid tbody tr"><input class="input filter__input" placeholder="Filteren op pagina" type="search" ></div></li></ul></div></header>'
        footer_html = '<footer class="datagrid__footer"><div class="toolbar toolbar--pad toolbar--justify"><ul class="toolbar__list"><li class="toolbar__list-item"><button class="button button--small button--transparent" name="Lorem" title="Foo" ><span class="button__label">Foo</span><img class="icon icon--image" alt="Foo" src="data:image/png;base64,"></button></li><li class="toolbar__list-item"><button class="button button--small button--danger" name="Ipsum" title="Bar" ><span class="button__label">Bar</span><img class="icon icon--image" alt="Bar" src="data:image/png;base64,"></button></li></ul></div></footer>'
        self.assertInHTML(header_html, html)
        self.assertNotIn(footer_html, html)

    def test_toolbar_position_bottom(self):
        html = self.template_render(
            {
                "columns": ("title"),
                "queryset": Book.objects.all(),
                "id": "my-first-datagrid",
                "form": True,
                "form_buttons": [
                    {"label": "Foo", "name": "Lorem", "icon_src": "data:image/png;base64,"},
                    {
                        "class": "button--danger",
                        "label": "Bar",
                        "name": "Ipsum",
                        "icon_src": "data:image/png;base64,",
                    },
                ],
                "toolbar_position": "bottom",
            }
        )

        header_html = '<header class="datagrid__header"><div class="toolbar toolbar--pad toolbar--justify"><ul class="toolbar__list"><li class="toolbar__list-item"><button class="button button--small button--transparent" name="Lorem" title="Foo" ><span class="button__label">Foo</span><img class="icon icon--image" alt="Foo" src="data:image/png;base64,"></button></li><li class="toolbar__list-item"><button class="button button--small button--danger" name="Ipsum" title="Bar" ><span class="button__label">Bar</span><img class="icon icon--image" alt="Bar" src="data:image/png;base64,"></button></li></ul><ul class="toolbar__list"><li class="toolbar__list-item"><div class="filter filter--class-only filter--filter" data-filter-target="#my-first-datagrid tbody tr"><input class="input filter__input" placeholder="Filteren op pagina" type="search" ></div></li></ul></div></header>'
        footer_html = '<footer class="datagrid__footer"><div class="toolbar toolbar--pad toolbar--justify"><ul class="toolbar__list"><li class="toolbar__list-item"><button class="button button--small button--transparent" name="Lorem" title="Foo" ><span class="button__label">Foo</span><img class="icon icon--image" alt="Foo" src="data:image/png;base64,"></button></li><li class="toolbar__list-item"><button class="button button--small button--danger" name="Ipsum" title="Bar" ><span class="button__label">Bar</span><img class="icon icon--image" alt="Bar" src="data:image/png;base64,"></button></li></ul></div></footer>'
        self.assertNotIn(header_html, html)
        self.assertInHTML(footer_html, html)

    def test_toolbar_position_both(self):
        html = self.template_render(
            {
                "columns": ("title"),
                "queryset": Book.objects.all(),
                "id": "my-first-datagrid",
                "form": True,
                "form_buttons": [
                    {"label": "Foo", "name": "Lorem", "icon_src": "data:image/png;base64,"},
                    {
                        "class": "button--danger",
                        "label": "Bar",
                        "name": "Ipsum",
                        "icon_src": "data:image/png;base64,",
                    },
                ],
                "toolbar_position": "both",
            }
        )

        header_html = '<header class="datagrid__header"><div class="toolbar toolbar--pad toolbar--justify"><ul class="toolbar__list"><li class="toolbar__list-item"><button class="button button--small button--transparent" name="Lorem" title="Foo" ><span class="button__label">Foo</span><img class="icon icon--image" alt="Foo" src="data:image/png;base64,"></button></li><li class="toolbar__list-item"><button class="button button--small button--danger" name="Ipsum" title="Bar" ><span class="button__label">Bar</span><img class="icon icon--image" alt="Bar" src="data:image/png;base64,"></button></li></ul><ul class="toolbar__list"><li class="toolbar__list-item"><div class="filter filter--class-only filter--filter" data-filter-target="#my-first-datagrid tbody tr"><input class="input filter__input" placeholder="Filteren op pagina" type="search" ></div></li></ul></div></header>'
        footer_html = '<footer class="datagrid__footer"><div class="toolbar toolbar--pad toolbar--justify"><ul class="toolbar__list"><li class="toolbar__list-item"><button class="button button--small button--transparent" name="Lorem" title="Foo" ><span class="button__label">Foo</span><img class="icon icon--image" alt="Foo" src="data:image/png;base64,"></button></li><li class="toolbar__list-item"><button class="button button--small button--danger" name="Ipsum" title="Bar" ><span class="button__label">Bar</span><img class="icon icon--image" alt="Bar" src="data:image/png;base64,"></button></li></ul></div></footer>'
        self.assertInHTML(header_html, html)
        self.assertInHTML(footer_html, html)

    def test_modifier_key(self):
        html = self.template_render(
            {
                "columns": ("publisher"),
                "queryset": Book.objects.all(),
                "modifier_key": "publisher",
                "modifier_column": "publisher",
                "modifier_mapping": {"Foo": "purple", "Bar": "violet"},
            }
        )
        foo_html = '<tr class="datagrid__row datagrid__row--purple"><td class="datagrid__cell datagrid__cell--modifier">Foo</td></tr>'
        bar_html = '<tr class="datagrid__row datagrid__row--violet"><td class="datagrid__cell datagrid__cell--modifier">Bar</td></tr>'
        self.assertInHTML(foo_html, html)
        self.assertInHTML(bar_html, html)

    def test_get_absolute_url(self):
        self.book_1.get_absolute_url = lambda: "/foo"
        self.book_2.get_absolute_url = lambda: "/bar"

        html = self.template_render(
            {"columns": ("title", "publisher"), "object_list": [self.book_1, self.book_2]}
        )

        foo_html = '<tr class="datagrid__row fake-link fake-link--double-click" data-href="/foo"><td class="datagrid__cell"><a class="datagrid__link" href="/foo">Lorem</a></td><td class="datagrid__cell">Foo</td></tr>'
        bar_html = '<tr class="datagrid__row fake-link fake-link--double-click" data-href="/bar"><td class="datagrid__cell"><a class="datagrid__link" href="/bar">Ipsum</a></td><td class="datagrid__cell">Bar</td></tr>'
        self.assertInHTML(foo_html, html)
        self.assertInHTML(bar_html, html)

    def test_url_reverse(self):
        html = self.template_render(
            {"columns": ("publisher"), "queryset": Book.objects.all(), "url_reverse": "detail"}
        )

        foo_html = '<tr class="datagrid__row fake-link fake-link--double-click" data-href="/1"><td class="datagrid__cell"><a class="datagrid__link" href="/1">Foo</a></td></tr>'
        bar_html = '<tr class="datagrid__row fake-link fake-link--double-click" data-href="/2"><td class="datagrid__cell"><a class="datagrid__link" href="/2">Bar</a></td></tr>'
        baz_html = '<tr class="datagrid__row fake-link fake-link--double-click" data-href="/3"><td class="datagrid__cell"><a class="datagrid__link" href="/3">Foo</a></td></tr>'
        self.assertInHTML(foo_html, html)
        self.assertInHTML(bar_html, html)
        self.assertInHTML(baz_html, html)
