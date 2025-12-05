from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Property, Inquiry
from .forms import PropertyForm, InquiryForm

from .choices import price_choices, bedroom_choices, state_choices, property_type_choices

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

def listing(request, listing_id):
    listing = get_object_or_404(Property, pk=listing_id)
    form = InquiryForm()

    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.property = listing
            if request.user.is_authenticated:
                inquiry.user = request.user
            inquiry.save()
            messages.success(request, 'Your inquiry has been submitted, a realtor will get back to you soon')
            return redirect('listing', listing_id=listing_id)
        else:
            messages.error(request, 'There was an error with your submission')

    context = {
        'listing': listing,
        'form': form
    }
    return render(request, 'listings/listing.html', context)

def search(request):
    queryset_list = Property.objects.order_by('-list_date')

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)
            
    # Property Type
    if 'property_type' in request.GET:
        property_type = request.GET['property_type']
        if property_type:
            queryset_list = queryset_list.filter(property_type__iexact=property_type)

    context = {
        'listings': queryset_list,
        'values': request.GET,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'property_type_choices': property_type_choices
    }
    return render(request, 'listings/search.html', context)

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from .forms import PropertyForm

@login_required
def create_listing(request):
    if not request.user.is_agent and not request.user.is_superuser:
        messages.error(request, 'Only agents can create listings')
        return redirect('index')
        
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.realtor = request.user
            listing.save()
            messages.success(request, 'Listing created successfully')
            return redirect('dashboard')
    else:
        form = PropertyForm()
    
    context = {'form': form, 'title': 'Create Listing'}
    return render(request, 'listings/listing_form.html', context)

@login_required
def update_listing(request, listing_id):
    listing = get_object_or_404(Property, pk=listing_id)
    if listing.realtor != request.user and not request.user.is_superuser:
        messages.error(request, 'You can only edit your own listings')
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Listing updated successfully')
            return redirect('dashboard')
    else:
        form = PropertyForm(instance=listing)
    
    context = {'form': form, 'title': 'Update Listing'}
    return render(request, 'listings/listing_form.html', context)

@login_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(Property, pk=listing_id)
    if listing.realtor != request.user and not request.user.is_superuser:
        messages.error(request, 'You can only delete your own listings')
        return redirect('dashboard')
        
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Listing deleted successfully')
        return redirect('dashboard')
        
    context = {'listing': listing}
    return render(request, 'listings/listing_confirm_delete.html', context)
