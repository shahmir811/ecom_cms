from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, UpdateView
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Customer
from .forms import CustomerForm

# Create your views here.
class CustomersListView(ListView):
    model = Customer
    template_name = 'customers/customers_list.html'
    context_object_name = 'customers'


class CustomerCreateView(View):
    template_name = 'customers/create.html'

    def get(self, request):
        form = CustomerForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer created successfully!")
            return redirect('customers:list')
        return render(request, self.template_name, {'form': form})

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/update.html'
    success_url = reverse_lazy('customers:list')

    def form_valid(self, form):
        messages.success(self.request, "Customer updated successfully!")
        return super().form_valid(form)
