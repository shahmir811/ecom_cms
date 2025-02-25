from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, UpdateView, DetailView
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
import openpyxl

from .models import Customer, Store
from .forms import CustomerForm, StoreForm
from products.models import Product
from countries.models import Country

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



class StoreProductExcelUploadView(View):
    template_name = 'customers/stores/upload-products.html'  # create this template

    def get(self, request, store_id):
        store = get_object_or_404(Store, id=store_id)
        countries = Country.objects.all()  # Fetch countries for context
        return render(request, self.template_name, {'store': store, 'countries': countries})

    def post(self, request, store_id):
        store = get_object_or_404(Store, id=store_id)
        countries = Country.objects.all()  # Fetch countries for context
        excel_file = request.FILES.get('excel_file')

        if not excel_file:
            messages.error(request, "No file uploaded. Please select an Excel file.")
            return render(request, self.template_name, {'store': store})

        try:
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active

            # Fetch existing ASINs for this store to avoid duplicates
            existing_asins = set(Product.objects.filter(store=store).values_list('asin', flat=True))
            count = 0
            duplicate_count = 0

            # Skip the first row (assuming it's the header)
            for row in sheet.iter_rows(min_row=2, values_only=True):  # Start from row 2
                asin = row[0]
                country_id = request.POST.get('country')  # Get the selected country ID from form
                country = Country.objects.get(id=country_id) if country_id else None

                if asin and asin not in existing_asins:
                    # Generate URL using the country's website and ASIN
                    product_url = f"{country.website}/dp/{asin}" if country and country.website else None                    
                    
                    # Add the new ASIN and link it to the store
                    Product.objects.create(
                        store=store, 
                        asin=asin, 
                        country=country,
                        url=product_url
                    )
                    existing_asins.add(asin)  # Update the set to avoid re-adding during the same upload
                    count += 1
                elif asin in existing_asins:
                    duplicate_count += 1

            messages.success(request, f"{count} new products added successfully! {duplicate_count} duplicates were ignored.")
        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")
            return render(request, self.template_name, {'store': store})

        # Redirect back to the store view
        return redirect('customers:stores_view', pk=store.id)
