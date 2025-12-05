from django import forms
from django import forms
from .models import Property, Inquiry
from .choices import state_choices, property_type_choices

class PropertyForm(forms.ModelForm):
    state = forms.ChoiceField(choices=list(state_choices.items()))
    property_type = forms.ChoiceField(choices=list(property_type_choices.items()))

    class Meta:
        model = Property
        fields = '__all__'
        exclude = ('realtor', 'list_date', 'is_published')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ('name', 'email', 'phone', 'message')
