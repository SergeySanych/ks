from django import template
from home.models import Topics, Components, Countries

register = template.Library()


# topics snippets
@register.inclusion_tag('tags/topics.html', takes_context=True)
def topics(context):
    return {
        'topics': Topics.objects.all(),
        'request': context['request'],
    }


# topics snippets
@register.inclusion_tag('tags/topics_en.html', takes_context=True)
def topics_en(context):
    return {
        'topics': Topics.objects.all(),
        'request': context['request'],
    }


# Components snippets
@register.inclusion_tag('tags/components.html', takes_context=True)
def components(context):
    return {
        'components': Components.objects.all(),
        'request': context['request'],
    }


# Components snippets
@register.inclusion_tag('tags/components_en.html', takes_context=True)
def components_en(context):
    return {
        'components': Components.objects.all(),
        'request': context['request'],
    }


# Components snippets for homepage
@register.inclusion_tag('tags/components_home.html', takes_context=True)
def components_homepage(context):
    return {
        'components': Components.objects.all(),
        'request': context['request'],
    }


# Components snippets for homepage_en
@register.inclusion_tag('tags/components_home_en.html', takes_context=True)
def components_homepage_en(context):
    return {
        'components': Components.objects.all(),
        'request': context['request'],
    }


# Countries snippets
@register.inclusion_tag('tags/countries.html', takes_context=True)
def countries(context):
    return {
        'countries': Countries.objects.all(),
        'request': context['request'],
    }


# Countries snippets for en
@register.inclusion_tag('tags/countries_en.html', takes_context=True)
def countries_en(context):
    return {
        'countries': Countries.objects.all(),
        'request': context['request'],
    }
