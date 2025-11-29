import json
from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
import stripe
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from cart.contexts import cart_contents
from products.models import Product
from .models import Order, OrderLineItem
from .forms import OrderForm


@require_POST
def cache_checkout_data(request):
    '''
    View to see if the user has the Save this address to my profile \
    box checked
    '''
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment is unable to be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    '''
    The logic below details how the checkout will work
    '''
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # If checkout form is a POST form
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        # Data from the checkout form
        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'eircode': request.POST['eircode'],
            'country': request.POST['country'],
        }
        order_form = OrderForm(form_data)
        # If order is valid
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()
            # Loop through items in cart
            for item_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                # If there is an error with the users cart the below message
                # will be generated
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found in \
                        our database. Please contact us for assistance."
                        )
                    )
                    # Order is deleted and user is redirected back to the
                    # shopping cart
                    order.delete()
                    return redirect(reverse('view_cart'))
            # If form posted successfully redirect to checkout success page
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
        # Error message if form is filled out incorrect
        else:
            messages.error(request, 'There was an error with your form. \
                                     Please recheck all the details entered.')
    # If shopping cart is empty the error message below will be generated
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "You've nothing in your cart at the moment, \
                                     but here's are all of our products for \
                                     you to browse \U0001F642")
            return redirect(reverse('products'))

        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        # Stripe intent referenced in docs:
        # https://stripe.com/docs/payments/accept-a-payment?platform=web&ui=elements#web-create-payment-intent
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # Auto populate the delivery details if the user is authenticated
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'town_or_city': profile.default_town_or_city,
                    'county': profile.default_county,
                    'eircode': profile.default_eircode,
                    'country': profile.default_country,
                })
            # User profile doesn't exist
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        # If user isn't authenticated generate a blank form
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing!')

    template = 'checkout/checkout.html'
    context = {
      'order_form': order_form,
      'stripe_public_key': stripe_public_key,
      'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    '''
    If the customer has successfully checked out
    '''
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the users profile to the order
        order.user_profile = profile
        order.save()

        if save_info:
            profile_data = {
                'default_email': order.email,
                'default_phone_number': order.phone_number,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_town_or_city': order.town_or_city,
                'default_county': order.county,
                'default_eircode': order.eircode,
                'default_country': order.country,
            }
            user_profile_form = UserProfileForm(profile_data,
                                                instance=profile
                                                )
            if user_profile_form.is_valid():
                user_profile_form.save()

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
