from django.shortcuts import render,redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from checkout.models import Order
from .forms import UserProfileForm
from .models import UserProfile


@login_required
def profile(request):
    '''
    Display user profile
    '''
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile has been successfully updated')
        else:
            messages.error(request, 'Profile update failed. Please ensure all \
                                     fields are valid!')
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
    }

    return render(request, template, context)

@login_required
def order_history(request, order_number):
    """
    Secure view: Only allow users to view THEIR OWN orders.
    """
    order = get_object_or_404(Order, order_number=order_number)

    # Get the logged in user profile
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # ADDED SECURITY TO CHECK does this order belong to this user profile
    if order.user_profile != user_profile:
        messages.warning(request, 'Sorry, you are not authorized to perform \
                                   that action')
        return redirect(reverse('home'))


    messages.info(request, ('All of the details for this order are listed \
                             here.'))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
