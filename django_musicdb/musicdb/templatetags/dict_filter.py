from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def hash(h, key):
    #print 'return' + h[key]
    return h[key]