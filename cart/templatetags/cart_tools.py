from django import template

register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    '''
    This function is to return the subtotal of each row item in
    cart.html page
    '''
    return price * quantity
