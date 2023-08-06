{% load modelsdoc_tags %}
{% autoescape off %}

.. contents::
   :local:

{% for model in models %}
{{ model.display_name }}
{{ model.display_name_length|str_repeat:'-' }}

::

 {{ model.doc }}

.. list-table::
   :header-rows: 1

   {% emptylineless %}
   {% for label, attr in display_fields %}
   {% if forloop.first %}*{% else %} {% endif %} - {{ label }}
   {% endfor %}

   {% for field in model.fields %}
   {% for label, attr in display_fields %}
   {% if forloop.first %}*{% else %} {% endif %} - {{ field|get_attr:attr }}
   {% endfor %}
   {% endfor %}
   {% endemptylineless %}

{% if model.model_options %}
Options::

 {% emptylineless %}
 {% for name, value in model.model_options.items %}
 {{ name }} : {{ value|safe }}
 {% endfor %}
 {% endemptylineless %}
{% endif %}
{% endfor %}
{% endautoescape %}
