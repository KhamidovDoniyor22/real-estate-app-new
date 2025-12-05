from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from listings.models import Property, Inquiry
from .serializers import PropertySerializer, InquirySerializer

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_root(request, format=None):
    return Response({
        'listings': reverse('api_listings', request=request, format=format),
        'inquiries': reverse('api_inquiry_create', request=request, format=format),
    })

class PropertyList(generics.ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Property.objects.filter(is_published=True).order_by('-list_date')
        
        # Filtering
        property_type = self.request.query_params.get('property_type')
        if property_type:
            queryset = queryset.filter(property_type__iexact=property_type)

        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__iexact=city)

        state = self.request.query_params.get('state')
        if state:
            queryset = queryset.filter(state__iexact=state)

        price = self.request.query_params.get('price')
        if price:
            queryset = queryset.filter(price__lte=price)

        bedrooms = self.request.query_params.get('bedrooms')
        if bedrooms:
            queryset = queryset.filter(bedrooms__lte=bedrooms)
            
        return queryset

class PropertyDetail(generics.RetrieveAPIView):
    queryset = Property.objects.filter(is_published=True)
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]

class InquiryCreate(generics.CreateAPIView):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    permission_classes = [permissions.AllowAny]
