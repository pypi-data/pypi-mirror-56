import re
from uuid import uuid4

from django.core.paginator import Paginator
from django.http import QueryDict
from django.utils import formats
from django.utils.dateparse import parse_date
from django.utils.safestring import SafeText
from django.utils.translation import gettext_lazy as _

from rijkshuisstijl.templatetags.rijkshuisstijl import register

from .rijkshuisstijl_helpers import (
    get_field_label,
    get_recursed_field_value,
    merge_config,
    parse_kwarg,
)


@register.inclusion_tag("rijkshuisstijl/components/datagrid/datagrid.html", takes_context=True)
def datagrid(context, **kwargs):
    """
    Renders a table like component with support for filtering, ordering and  paginating. It's main use if to display
    data from a listview.

    .. code-block:: html

        {% datagrid config=config %}
        {% datagrid option1='foo' option2='bar' %}

    Available options
    =================

    Showing data
    ------------

    Data is shown based on a internal "object" list which can be populated by either a "queryset" or an
    "object_list option. Columns are specified by a "columns" option which may define an additional label to show in
    the table header. Columns match fields in the objects in the internal object_list.

    - object_list: Optional, A list containing the object_list to show. if possible, use queryset instead.
      The internally used object_list is obtained by looking for these values in order:

    .. code-block:: python

        kwargs['queryset']
        kwargs['object_list']
        context['queryset']
        context['object_list']

    - queryset: Optional, A queryset containing the objects to show.

    - columns: Required, a dict or a list defining which columns/values to show for each object in object_list or
      queryset.

      - If a dict is passed, each key will represent a field in an object to obtain the data from and each value
        will represent the label to use for the column heading.
        Example: {'author': 'Written by', 'title': 'Title'}

      - If a list is passed, each item will represent a field in an object to obtain the data from and will also
        represent the label to use for the column heading.
        Example: ['author', 'title']


    Filtering
    ---------

    If an (unpaginated) queryset is passed or obtained from the context, it can be filtered using controls.
    Pagination provided by the datagrid itself can be used in combination with filtering. The queryset's model is
    inspected to determince the type of the filters and optionally the choices.

    - filterable_columns: Optional, a list defining which columns should be filterable.


    Ordering
    --------

    An interface for ordering can be creating by defining the fields that should be made orderable. Orderable
    columns are specified by the "orderable_columns" option which may define a field lookup which defaults to the
    field. Inverted field lookups are proceeded with a dash "-" character and set to the GET parameter specified by
    the "ordering_key" setting.

    - order: Optional, if True, order queryset, if False rely on view/context to order queryset.
    - orderable_columns: Optional, a dict or a list defining which columns should be orderable.

      - If a dict is passed each key will map to a field (the key) in columns, each value will be used to describe
        a field lookup.
        Example: {"author": "author__first_name"}

      - If a list is passed each value will map to a field (the key) in columns and will also be used to describe
        a field lookup
        Example: ['author', 'title']

    - ordering_key: Optional, describes which query parameter should be used in hyperlinks
    (set on the table captions) to indicate which order the view should provide, defaults to "ordering".


    Pagination
    ----------

    Data can be paginated if needed. Pagination can either be performed by the datagrid itself, or an already
    available (Django) paginator may be used (since we need to support already paginated object lists).

    Paginate un-paginated object_list
    ---------------------------------

    - paginate: Optional, if True, paginate object_list (or queryset).
    - paginate_by: Optional, amount of results per page, defaults to 30.
    - page_key: Optional, The GET parameter to use for the page, defaults to 'page'.

    Use existing paginator
    ----------------------

    An existing Django Paginator instance can be used. Pagination details may be obtained from the context if not
    explicitly set.

    - is_paginated: Optional, if True, paginate based on paginator configuration, may be obtained from context.
    - paginator: Optional, A Django Paginator instance, may be obtained from context.
    - page_obj: Optional, The paginator page object, may be obtained from context.
    - page_number: Optional, The current page number.
    - page_key: Optional, The GET parameter to use for the page, defaults to 'page'.
    - paginator_zero_index: Optional, Use zero-based indexing for page numbers, not fully supported.


    Custom presentation (get_<field>_display)
    -----------------------------------------

    - get_<field>_display: Optional, allows a callable to be used to generate a custom cell display value. Replace
      <field> with a key which will map to a field (a key in columns) and set a callable as it's value.

    The callable will receive the row's object and should return SafeText.
    Example: `lambda object: mark_safe(<a href="{}">{}</a>.format(object.author.get_absolute_url, object.author))`


    Manipulating data (form)
    ------------------------

    A form can be generated POSTing data to the url specified by the "form_action" option. When a form is active
    each row gets a checkbox input with a name specified by the "form_checkbox_name" option. Various actions can be
    defined by the "form_buttons" option which are placed either in the top, bottom or at both position based on the
    value of the "toolbar_postion" option.

    - form: Optional, if True, adds a form to the datagrid, useful for allowing user manipulations on the dataset.
      Defaults to false, unless "form_action" or "form_buttons" is set.

    - form_action: Optional, specifies the url to submit form actions to. If set, form will default to True.

    - form_buttons: Optional, a list_of_dict (label, [href], [icon], [icon_src] [name], [target], [title]) defining
      which buttons to create (see rijkshuisstijl_form.button). The name attribute of the buttons should be used to
      specify the performed action.
      example: [{'name': 'delete', 'label': 'delete' 'class': 'button--danger'}]

    - toolbar_position: Optional, can be set to one of "top", "bottom", or "both" indicating the position of the
      toolbar containing the buttons specified by form_buttons.

    - form_checkbox_name: Optional, specifies the name for each checkbox input for an object in the table. This
      should be used for determining which objects should be manipulated by the performed action.


    Color coded rows
    ----------------

    Rows can be configured to show a color coded border and a colored cell value based on the value of a certain
    field. The field to look for is defined by the "modifier_key" option if this is any different than the column
    key it should color the cell for, the column can be specified by the "modifier_column" options. This defaults
    to the value of the "modifier_key" option. The field value is matched against a mapping (specified by the
    "modifier_mapping" options) to define the color. The value should contain the value in the mapping.

    - modifier_key Optional, a string defining the field in an object to get the value to match for.
    - modifier_column Optional, a string defining the column key to apply the colored styling for.
    - modifier_mapping, Optional, a dict containing a key which possibly partially matches an object's field value
      and which value is one of the supported colors.
      Example: [{'1984': 'purple'}]

    The supported colors are:

    - purple
    - purple-shade-1
    - purple-shade-2
    - violet
    - violet-shade-1
    - violet-shade-2
    - ruby
    - ruby-shade-1
    - ruby-shade-2
    - pink
    - pink-shade-1
    - pink-shade-2
    - red
    - red-shade-1
    - red-shade-2
    - orange
    - orange-shade-1
    - orange-shade-2
    - dark-yellow
    - dark-yellow-shade-1
    - dark-yellow-shade-2
    - yellow
    - yellow-shade-1
    - yellow-shade-2
    - dark-brown
    - dark-brown-shade-1
    - dark-brown-shade-2
    - brown
    - brown-shade-1
    - brown-shade-2
    - dark-green
    - dark-green-shade-1
    - dark-green-shade-2
    - green
    - green-shade-1
    - green-shade-2
    - moss-green
    - moss-green-shade-1
    - moss-green-shade-2
    - mint-green
    - mint-green-shade-1
    - mint-green-shade-2
    - dark-blue
    - dark-blue-shade-1
    - dark-blue-shade-2
    - heaven-blue
    - heaven-blue-shade-1
    - heaven-blue-shade-2
    - light-blue
    - light-blue-shade-1
    - light-blue-shade-2


    Additional options
    ------------------

    - class: Optional, a string with additional CSS classes.
    - id: Optional, a string specifying the datagrid id, defaults to a generated uuid4 string.
    - urlize: Optional, if True (default) cell values are passed to "urlize" template filter, automatically creating
      hyperlinks if applicable in every cell.
    - title: Optional, if set, a title will be shown above the datagrid.
    - url_reverse: Optional, A URL name to reverse using the object's 'pk' attribute as one and only attribute,
      creates hyperlinks in the first cell. If no url_reverse if passed get_absolute_url is tried in order to find
      a url.

    :param context:
    :param kwargs:
    """

    def get_id():
        """
        Gets the id to put on the datagrid based on kwargs["id'}, if no id is provided a uuid4 is created and prefixed
        with "datagrid-".
        :return: A str which should be unique to this datagrid.
        """
        return kwargs.get("id", "datagrid-" + str(uuid4()))

    def get_columns():
        """
        Gets the columns to show based on kwargs['columns']. If no label is provided an attempt is made to create it
        based on the model or a simple replacement of dashes and underscores.
        :return: A list_of_dict where each dict contains "key" and "label" keys.
        """
        columns = parse_kwarg(kwargs, "columns", [])
        columns = create_list_of_dict(columns)

        # Get column label.
        for column in columns:
            context_queryset = context.get("queryset")
            queryset = kwargs.get("queryset", context_queryset)

            column["label"] = get_field_label(queryset, column["label"])
        return columns

    def get_object_list():
        """
        Looks for the object_list to use based on the presence of these variables in order:

            1) kwargs['queryset']
            2) kwargs['object_list']
            3) context['queryset']
            4) context['object_list']

        Queryset filtering is applied if required.
        Ordering is applied if required.
        add_display() and add_modifier_class() are called for every object in the found object_list.
        :return: A list of objects to show data for.
        """

        # Get object list.
        context_object_list = context.get("object_list", [])
        context_queryset = context.get("queryset", context_object_list)
        object_list = kwargs.get("object_list", context_queryset)
        object_list = kwargs.get("queryset", object_list)

        # Filtering
        filters = get_filter_dict()
        if filters and hasattr(object_list, "filter") and callable(object_list.filter):
            try:
                active_filters = [
                    active_filter for active_filter in filters if active_filter.get("value")
                ]
                for active_filter in active_filters:
                    filter_key = active_filter.get("filter_key")
                    value = active_filter.get("value")
                    type = active_filter.get("type")

                    if type is "DateTimeField":
                        value = parse_date(value)
                        filter_kwargs = {
                            filter_key + "__year": value.year,
                            filter_key + "__month": value.month,
                            filter_key + "__day": value.day,
                        }
                    elif active_filter.get("is_relation"):
                        filter_kwargs = {filter_key: value}
                    else:
                        filter_kwargs = {filter_key + "__icontains": value}
                    object_list = object_list.filter(**filter_kwargs)
            except:
                object_list = object_list.none()

        # Ordering
        order = kwargs.get("order")
        if order and hasattr(object_list, "order_by") and callable(object_list.order_by):
            order_by = get_ordering()

            if order_by:
                object_list = object_list.order_by(order_by)
        return object_list

    def get_modifier_column():
        """
        Returns the key of the column to colorize the value of is a modifier configuration is set. Defaults to the value
        of the modifier_key option.
        :return: A string othe modifier column or False.
        """
        return kwargs.get("modifier_column", kwargs.get("modifier_key", False))

    def get_filter_dict():
        """
        Returns a list_of_dict for filter configuration, each dict (if present) contains:

        - filter_key: matching a column.
        - type: matching the field class name.
        - choices: a tuple containing choice tuples. Used to provide options/suggestions for filter.
        - value: The value of the filter.

        :return: list_of_dict.
        """
        filterable_columns = parse_kwarg(kwargs, "filterable_columns", [])
        filterable_columns = create_list_of_dict(filterable_columns)

        context_queryset = context.get("queryset")
        queryset = kwargs.get("queryset", context_queryset)

        if not queryset:  # Filtering is only supported on querysets.
            return {}

        for filterable_column in filterable_columns:
            if not "filter_key" in filterable_column:
                filterable_column["filter_key"] = filterable_column.get("key")

            field_key = filterable_column.get("key", "")
            field_name = field_key.split("__")[0]
            field = queryset.model._meta.get_field(field_name)

            if not "type" in filterable_column:
                filterable_column["type"] = type(field).__name__

            if not "choices" in filterable_column:
                choices = field.choices
                if filterable_column.get("type") == "BooleanField":
                    choices = ((True, _("waar")), (False, _("onwaar")))

                if field.is_relation:
                    filterable_column["is_relation"] = field.is_relation

                    if "__" in field_key:
                        remote_field_name = field_key.split("__")[-1]
                        choices = [
                            (value, value)
                            for value in field.remote_field.model.objects.values_list(
                                remote_field_name, flat=True
                            )
                        ]
                    else:
                        choices = field.remote_field.model.objects.all()

                if choices:
                    filterable_column["choices"] = [("", "---------")] + list(choices)

            request = context.get("request")
            filter_key = filterable_column["filter_key"]
            filterable_column["value"] = request.GET.get(filter_key)
        return filterable_columns

    def get_ordering():
        """
        Return the field to use for ordering the queryset.
        Only allows ordering by dict keys found in the orderable_columns option.
        :return: string or None
        """
        request = context["request"]
        ordering_key = get_ordering_key()
        ordering = request.GET.get(ordering_key)
        orderable_columns_keys = get_orderable_column_keys()

        if ordering and ordering.replace("-", "") in orderable_columns_keys:
            return ordering
        return None

    def get_ordering_key():
        """
        Returns the query parameter to use for ordering.
        :return: string
        """
        return parse_kwarg(kwargs, "ordering_key", "ordering")

    def get_orderable_column_keys():
        """
        Returns the keys of the fields which should be made orderable.
        :return: list_of_str
        """
        orderable_columns = parse_kwarg(kwargs, "orderable_columns", {})
        try:
            return [key for key in orderable_columns.keys()]
        except AttributeError:
            return orderable_columns

    def get_ordering_dict():
        """
        Returns a dict containing a dict with ordering information (direction, url) for every orderable column.
        :return: dict
        """
        request = context["request"]
        orderable_columns = parse_kwarg(kwargs, "orderable_columns", {})
        order_by_index = kwargs.get("order_by_index", False)
        ordering_dict = {}

        # Convert list to list_of_dict.
        if type(orderable_columns) is list or type(orderable_columns) is tuple:
            orderable_columns = {column: column for column in orderable_columns}

        try:
            i = 1
            for (orderable_column_key, orderable_column_field) in orderable_columns.items():
                querydict = QueryDict(request.GET.urlencode(), mutable=True)
                ordering_key = get_ordering_key()
                ordering_value = str(i) if order_by_index else orderable_column_field
                current_ordering = get_ordering()

                directions = {
                    "asc": ordering_value.replace("-", ""),
                    "desc": "-" + ordering_value.replace("-", ""),
                }

                direction_url = directions["asc"]
                direction = None

                if current_ordering == directions["asc"]:
                    direction = "asc"
                    direction_url = directions["desc"]
                elif current_ordering == directions["desc"]:
                    direction = "desc"
                    direction_url = directions["asc"]

                querydict[ordering_key] = direction_url
                ordering_dict[orderable_column_key] = {
                    "direction": direction,
                    "url": "?" + querydict.urlencode(),
                }

                i += 1
        except AttributeError:
            pass
        return ordering_dict

    def get_form_buttons():
        """
        Gets the buttons to use for the form based on kwargs['form_buttons'].
        :return: A list_of_dict where each dict contains at least "name" and "label" keys.
        """
        form_actions = parse_kwarg(kwargs, "form_buttons", {})

        # Convert dict to list_of_dict
        try:
            return [{"name": key, "label": value} for key, value in form_actions.items()]
        except AttributeError:
            return form_actions

    def add_paginator(datagrid_context):
        """
        Return datagrid_context with added paginator configuration.
        :param datagrid_context: A processed clone of kwargs.
        """
        paginator_context = datagrid_context.copy()
        paginator_context["is_paginated"] = kwargs.get("is_paginated", context.get("is_paginated"))

        if paginator_context.get("paginate"):
            """
            Paginate object_list.
            """
            request = paginator_context.get("request")
            paginate_by = paginator_context.get("paginate_by", 30)
            paginator = Paginator(paginator_context.get("object_list", []), paginate_by)
            page_key = paginator_context.get("page_key", "page")
            page_number = request.GET.get(page_key, 1)

            if str(page_number).upper() == "LAST":
                page_number = paginator.num_pages

            page_obj = paginator.get_page(page_number)
            object_list = page_obj.object_list

            paginator_context["is_paginated"] = True
            paginator_context["paginator"] = paginator
            paginator_context["page_key"] = page_key
            paginator_context["page_number"] = page_number
            paginator_context["page_obj"] = page_obj
            paginator_context["object_list"] = object_list
            return paginator_context

        if paginator_context["is_paginated"]:
            """
            Rely on view/context for pagination.
            """
            paginator_context["paginator"] = kwargs.get("paginator", context.get("paginator"))
            paginator_context["paginator_zero_index"] = kwargs.get("paginator_zero_index")
            paginator_context["page_key"] = kwargs.get("page_key", "page")
            paginator_context["page_number"] = kwargs.get("page_number")
            paginator_context["page_obj"] = kwargs.get("page_obj", context.get("page_obj"))
            return paginator_context
        return paginator_context

    def add_object_attributes(datagrid_context):
        """
        Calls add_display(obj) and add_modifier_class(obj) for every obj in (paginated) object_list.
        :param datagrid_context:
        :return: datagrid_context
        """
        object_list = datagrid_context.get("object_list", [])

        for obj in object_list:
            add_display(obj)
            add_modifier_class(obj)
        return datagrid_context

    def add_display(obj):
        """
        If a get_<field>_display callable is set, add the evaluated result to the datagrid_display_<field> field on the
        object passed to obj.
        :param obj:
        """
        for column in get_columns():
            key = column["key"]
            fn = kwargs.get("get_{}_display".format(key), None)
            if fn:
                setattr(obj, "datagrid_display_{}".format(key), fn(obj))

    def add_modifier_class(obj):
        """
        If a modifier configuration is set, add the result color as datagrid_modifier_class to the object passed to
        obj.
        :param obj:
        """
        try:
            key = parse_kwarg(kwargs, "modifier_key", None)

            if not key:
                return

            modifier_map = parse_kwarg(kwargs, "modifier_mapping", {})
            object_value = getattr(obj, key)

            for item_key, item_value in modifier_map.items():
                pattern = re.compile(item_key)
                if pattern.match(str(object_value)):
                    obj.datagrid_modifier_class = item_value
        except KeyError:
            pass

    def create_list_of_dict(obj, name_key="key", name_value="label"):
        """
        Converst obj to a list of dict containg name_key and name_value for every dict.
        :param obj: Value to convert
        :param name_key: Name for the key in every dict.
        :param name_value: Name for the value in every dict.
        :return: list_of_dict
        """
        try:
            # Convert dict to list_of_dict.
            return [{name_key: key, name_value: value} for key, value in obj.items()]
        except AttributeError:
            # Convert string to list_of_dict.
            if type(obj) == str or type(obj) == SafeText:
                return [{name_key: obj, name_value: obj}]

            # Convert list to list_of_dict.
            elif type(obj) is list or type(obj) is tuple:
                list_of_dict = []
                for column in obj:
                    # Already dict
                    if type(column) == dict:
                        list_of_dict.append(column)
                    # Not dict
                    else:
                        list_of_dict.append({name_key: column, name_value: column})
            return list_of_dict

    kwargs = merge_config(kwargs)
    datagrid_context = kwargs.copy()

    # i18n
    datagrid_context["label_result_count"] = parse_kwarg(
        kwargs, "label_result_count", _("resultaten")
    )
    datagrid_context["label_no_results"] = parse_kwarg(
        kwargs, "label_no_results", _("Geen resultaten")
    )

    # kwargs
    datagrid_context["class"] = kwargs.get("class", None)
    datagrid_context["columns"] = get_columns()
    datagrid_context["orderable_column_keys"] = get_orderable_column_keys()
    datagrid_context["filters"] = get_filter_dict()
    datagrid_context["form_action"] = parse_kwarg(kwargs, "form_action", "")
    datagrid_context["form_buttons"] = get_form_buttons()
    datagrid_context["form_checkbox_name"] = kwargs.get("form_checkbox_name", "objects")
    datagrid_context["form"] = (
        parse_kwarg(kwargs, "form", False)
        or bool(kwargs.get("form_action"))
        or bool(kwargs.get("form_buttons"))
    )
    datagrid_context["id"] = get_id()
    datagrid_context["modifier_column"] = get_modifier_column()
    datagrid_context["object_list"] = get_object_list()
    datagrid_context["ordering"] = get_ordering_dict()
    datagrid_context["urlize"] = kwargs.get("urlize", True)
    datagrid_context["title"] = kwargs.get("title", None)
    datagrid_context["toolbar_position"] = kwargs.get("toolbar_position", "top")
    datagrid_context["url_reverse"] = kwargs.get("url_reverse", "")
    datagrid_context["request"] = context["request"]
    datagrid_context = add_paginator(datagrid_context)
    datagrid_context = add_object_attributes(datagrid_context)

    datagrid_context["config"] = kwargs
    return datagrid_context


@register.filter
def datagrid_label(obj, column_key):
    """
    Formats field in datagrid, supporting get_<column_key>_display() and and date_format().
    :param obj: (Model) Object containing key column_key.
    :param column_key key of field to get label for.
    :return: Formatted string.
    """
    try:
        return getattr(obj, "datagrid_display_{}".format(column_key))
    except:
        if column_key == "__str__":
            return str(obj)
        try:
            val = get_recursed_field_value(obj, column_key)
            if not val:
                return ""
            return formats.date_format(val)
        except (AttributeError, TypeError) as e:
            try:
                if type(obj) is list:
                    val = obj.get(column_key)
                else:
                    val = get_recursed_field_value(obj, column_key)
                if val:
                    return val
            except:
                pass
            return obj
