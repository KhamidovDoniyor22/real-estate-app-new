from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api_root'),
    path('listings/', views.PropertyList.as_view(), name='api_listings'),
    path('listings/<int:pk>/', views.PropertyDetail.as_view(), name='api_listing_detail'),
    path('inquiries/', views.InquiryCreate.as_view(), name='api_inquiry_create'),
]
