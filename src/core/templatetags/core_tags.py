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


@register.filter
def check_null(value):
    if value:
        return value
    return "-"


@register.filter
def alert_type_class(value):
    if value in ['cod', 'delivery', 'in_transit', 'bank_account']:
        return 'primary'
    elif value in ['completed', 'success', 'approved', 'paid', 'online', 'card', 'accepted']:
        return 'success'
    elif value in ['pending']:
        return 'warning'
    elif value in ['online', 'cancel', 'rejected', 'cancelled', 'unpaid', 'failed']:
        return 'danger'
    else:
        return 'secondary'