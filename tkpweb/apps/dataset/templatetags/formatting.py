from django import template


register = template.Library()


@register.filter
def prefixformat(value, arg):
    prefixes = {'M': 1e6, 'k': 1e3, 'G': 1e9, 'T': 1e12, 'P': 1e15, 'E': 1e18,
                'm': 1e-3, 'u': 1e-6, 'n': 1e-9, 'p': 1e-12, 'f': 1e-15}
    try:
        value /= prefixes[arg]
    except Exception:
        pass
    return value
