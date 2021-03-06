#
# See http://djangosnippets.org/snippets/847/
# for the original posted code.
#
from django import template
from django.utils.encoding import force_text

register = template.Library()

@register.filter
def in_group(user,groups):
    """Checking is user is in the groups of the list.
    Usage:
        {% if user|in_group:"groupA" %}
        ...
        {% endif %}
        
    or:
        {% if user|in_group:"groupA,groupB" %}
        ...
        {% endif %}
    """
    if user and user.is_authenticated:
        group_list = force_text(groups).split(',')
        return bool(user.groups.filter(name__in=group_list).values('name'))
    return False

