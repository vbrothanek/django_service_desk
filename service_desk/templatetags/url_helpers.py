from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Takes GET params and rewrites/append selected.
    {% url_replace page=3 per_page=20 %}

    Used for pagination in tickets.html
    """
    request = context['request']
    params = request.GET.copy()

    for key, value in kwargs.items():
        params[key] = value

    return params.urlencode()