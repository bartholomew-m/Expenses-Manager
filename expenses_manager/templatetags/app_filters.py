from django import template

register = template.Library()


@register.filter(name='customizeInput')
def set_css_class(value, data: str):
    """
    ... todo
    """
    def get_attr_key_val(attr: str):
        """
        ... todo
        """
        splited = attr.split('=')
        return (splited[0], splited[1])

    attrs = data.split(',')
    attrs_dict = {}
    for attr in attrs:
        k, v = get_attr_key_val(attr)
        attrs_dict[k] = v
    return value.as_widget(attrs=attrs_dict)
