from django import template
from django.core.paginator import Paginator

register = template.Library()


@register.filter("elided_pages")
def get_elided_pages(paginator: Paginator, page_num: int):
    for page in paginator.get_elided_page_range(page_num, on_each_side=2, on_ends=1):
        yield page
