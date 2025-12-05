from django.shortcuts import render
from django.http import HttpResponse
from listings.choices import price_choices, bedroom_choices, state_choices, property_type_choices
from listings.models import Property

def index(request):
    listings = Property.objects.order_by('-list_date').filter(is_published=True)[:3]

    context = {
        'listings': listings,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'property_type_choices': property_type_choices
    }
    return render(request, 'pages/index.html', context)
