from django.shortcuts import render


# Create your views here.
def covid_numbers(request):
    '''
    View that returns the covid numbers page
    '''
    return render(request, 'covid_numbers/covid_numbers.html')
