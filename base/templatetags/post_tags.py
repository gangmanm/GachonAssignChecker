from django import template
register = template.Library()


@register.filter(name='split')
def split(str, key):
    return str.split(key)


@register.filter(name='times')
def times(number):
    return range(number)


@register.filter(name="comparetxt")
def comparetxt(str1, str2):
    if str1 in str2:
        return 1


@register.filter(name="index")
def index(indexable, i):
    return indexable[i]
