from django import template

register = template.Library()


@register.filter(name="pic")
def get_picture_url(obj, size=None):
    return obj.get_pic_url(size=size)


@register.filter(name="runtime")
def minutes_to_hours_minutes(runtime):
    hours = runtime // 60
    minutes = runtime % 60
    return f"{hours}h {minutes}m"
