{% set p = inventory.parameters %}
{% for class_name, class_data in p.knowledge_graph.items() %}
# {{ class_name }}
class {{ class_name }}(StructuredNode):
{% for property_name, property in class_data.items() %}
    {{ property_name -}} =
{%- if "type" in property and property.type|lower == "string" %}StringProperty()
{% elif "rel_to" in property %}
RelationshipTo('{{ property.rel_to.class }}', '{{ property.rel_to.type }}')
{% endif %}
{% endfor %}
{% endfor %}
