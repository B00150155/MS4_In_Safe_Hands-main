from django.shortcuts import render, get_object_or_404
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


def order_history(request, order_number):
    '''
    A view to display the users order history
    '''
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, ('All of the details for this order are listed \
                             here.'))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
