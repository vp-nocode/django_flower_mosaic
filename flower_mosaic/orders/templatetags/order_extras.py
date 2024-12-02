from django import template

register = template.Library()

@register.filter
def sum_total(order_items):
    return sum(item.total_price for item in order_items)