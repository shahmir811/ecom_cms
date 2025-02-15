from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, UpdateView, DetailView
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Customer, Store
from .forms import CustomerForm, StoreForm

# Create your views here.
class CustomersListView(ListView):
    model = Customer
    template_name = 'customers/customers_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return Customer.objects.prefetch_related('stores')    


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

class CustomerDetailsView(DetailView):
    model = Customer
    template_name = 'customers/view.html'
    context_object_name = 'customer'

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/update.html'
    success_url = reverse_lazy('customers:list')

    def form_valid(self, form):
        messages.success(self.request, "Customer updated successfully!")
        return super().form_valid(form)

class StoresListView(ListView):
    model = Store
    template_name = 'customers/stores/list.html'
    context_object_name = 'stores'


class StoreCreateView(View):
    template_name = 'customers/stores/create.html'

    def get(self, request):
        form = StoreForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Store created successfully!")
            return redirect('customers:stores_list')
        return render(request, self.template_name, {'form': form})

class StoreDetailsView(DetailView):
    model = Store
    template_name = 'customers/stores/view.html'
    context_object_name = 'store'


class StoreUpdateView(UpdateView):
    model = Store
    form_class = StoreForm
    template_name = 'customers/stores/update.html'
    success_url = reverse_lazy('customers:stores_list')

    def form_valid(self, form):
        messages.success(self.request, "Store updated successfully!")
        return super().form_valid(form)