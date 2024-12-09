from django import template

register = template.Library()


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def image_or_placeholder(image, placeholder=None):
    if image:
        if hasattr(image, 'url') and image.url:
            return image.url
        else:
            return image
    if placeholder:
        return f"https://placehold.co/{placeholder}"
    return "https://placehold.co/100"
