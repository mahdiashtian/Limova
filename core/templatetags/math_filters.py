from django import template

register = template.Library()


@register.filter
def discount_percentage(original_price, discount_value):
    """Calculate the discount percentage."""
    try:

        discounted_price = original_price - (original_price * discount_value / 100)
        return round(discounted_price, 2)  # Round to 2 decimal places
    except (TypeError, ZeroDivisionError, ValueError):
        return 0  # Return 0 in case of error


@register.filter(name='multiply')
def multiply(value, arg):
    return float(value) * float(arg)
