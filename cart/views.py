from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from products.models import Product


# Create your views here.
MAX_ITEM_NUMBER = 20 # Number to stop Crazy high dos attack numbers

def view_cart(request):
    '''
    A view that will render the contents of the users shopping cart
    '''
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    cart = request.session.get('cart', {})

    redirect_url = request.POST.get('redirect_url', reverse('view_cart'))

    qty_str = request.POST.get('quantity')
    try:
        quantity = int(qty_str)
    except (TypeError, ValueError):
        messages.error(request, "Quantity Outside Of Bounds")
        return redirect(redirect_url)

    if quantity < 1:
        messages.error(request, "Products must be at least one")
        return redirect(redirect_url)

    if quantity > MAX_ITEM_NUMBER:
        messages.error(request, f"You can't add more than {MAX_ITEM_NUMBER}.")
        quantity = MAX_ITEM_NUMBER

    # Update cart if item already in cart
    if item_id in cart:
        new_qty = cart[item_id] + quantity

        if new_qty > MAX_ITEM_NUMBER:
            new_qty = MAX_ITEM_NUMBER
            messages.warning(
                request,
                f"Maximum quantity of {MAX_ITEM_NUMBER} for {product.name} applied."
            )
        else:
            messages.success(
                request,
                f"Quantity of {product.name} updated to {new_qty}."
            )

        # ALWAYS update the cart
        cart[item_id] = new_qty

    else:
        cart[item_id] = quantity
        messages.success(request, f"{product.name} added to cart")

    request.session['cart'] = cart
    return redirect(redirect_url)


def update_cart(request, item_id):
    """
    Adjust the number of items in the cart with validation
    """
    product = get_object_or_404(Product, pk=item_id)
    cart = request.session.get('cart', {})

    qty_str = request.POST.get('quantity')

    try:
        quantity = int(qty_str)
    except (TypeError, ValueError):
        messages.error(request, "Invalid quantity submitted.")
        return redirect(reverse('view_cart'))

    if quantity < 1:
        # Remove item if quantity < 1
        cart.pop(item_id, None)
        messages.success(request, f"{product.name} removed from cart")
    else:
        if quantity > MAX_ITEM_NUMBER:
            messages.warning(
                request,
                f"Maximum quantity of {MAX_ITEM_NUMBER} for {product.name} applied."
            )
            quantity = MAX_ITEM_NUMBER

        cart[item_id] = quantity
        messages.success(
            request,
            f"Quantity of {product.name} in cart is now {cart[item_id]} "
        )

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """
    To remove an item from the shopping cart safely
    """
    product = get_object_or_404(Product, pk=item_id)
    cart = request.session.get('cart', {})

    if item_id in cart:
        cart.pop(item_id, None)
        messages.success(request, f"{product.name} removed from cart ")
    else:
        messages.error(request, f"{product.name} is not in your cart.")

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))
