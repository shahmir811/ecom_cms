from django import forms
from .models import Customer, Store

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

class StoreForm(forms.ModelForm):
    owner = forms.ModelChoiceField(queryset=Customer.objects.all(), required=False, empty_label="Select a Customer")

    class Meta:
        model = Store
        fields = ['name', 'owner', 'wallmart_key']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Store.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A store with this name already exists.")
        return name