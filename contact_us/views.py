from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import ContactMessagesForm
from profiles.models import UserProfile


def contact_us(request):
    '''
    View that returns contact us page
    '''
    # If user is authenticated then the priority message will show
    if request.user.is_authenticated:
        messages_form = ContactMessagesForm(initial={
            'sender': UserProfile.objects.get(user=request.user)}
            )
    # If user is unregistered then the form will not show
    else:
        messages_form = ContactMessagesForm()

    if request.method == 'POST':
        messages_form = ContactMessagesForm(request.POST)
        sender = UserProfile.objects.get(user=request.user)

        if messages_form.is_valid():
            try:
                messages_form.save()
                messages.success(request, "Your message to us has been \
                                           successfully sent. We will be in \
                                           contact as soon as possible")
                return redirect(reverse('home'))
            except Exception as e:
                messages.error(request, "There was an error sending your \
                                         message, please try to send it \
                                         again")
                return redirect(reverse('contact_us'))
        else:
            messages.error(request, "There was an error sending your \
                                     message, please try to send it again")
            return redirect(reverse('contact_us'))

    template = 'contact_us/contact_us.html'
    context = {
        'form': messages_form
    }

    return render(request, template, context=context)
