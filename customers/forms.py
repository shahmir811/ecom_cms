from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address', 'city', 'state']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        customer_id = self.instance.pk  # Get the current customer ID
        
        # Exclude the current customer from the uniqueness check
        if Customer.objects.filter(email=email).exclude(pk=customer_id).exists():
            raise forms.ValidationError("A customer with this email already exists.")
        return email

