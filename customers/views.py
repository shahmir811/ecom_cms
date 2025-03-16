import re  # Import the re module for regular expressions

import openpyxl
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView, UpdateView

from countries.models import Country
from products.models import Product

from .forms import CustomerForm, StoreForm
from .models import Customer, Store


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_count'] = self.object.products.count() # products count

        # Paginate products
        products = self.object.products.all()  # Assuming a reverse relation named 'products'
        paginator = Paginator(products, 25)  # Show 25 products per page

        page = self.request.GET.get('page')
        context['products'] = paginator.get_page(page)
        
        return context    


class StoreUpdateView(UpdateView):
    model = Store
    form_class = StoreForm
    template_name = 'customers/stores/update.html'
    success_url = reverse_lazy('customers:stores_list')

    def form_valid(self, form):
        messages.success(self.request, "Store updated successfully!")
        return super().form_valid(form)


class StoreProductExcelUploadView(View):
    template_name = 'customers/stores/upload-products.html'  # Ensure this template exists

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
            return render(request, self.template_name, {'store': store, 'countries': countries})

        try:
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active

            # Fetch existing ASINs for this store to avoid duplicates
            existing_asins = set(Product.objects.filter(store=store).values_list('asin', flat=True))
            count = 0
            duplicate_count = 0

            # Get the header row (first row) to map column names to indices
            headers = [cell.value for cell in sheet[1]]  # Assuming the first row contains headers

            # Define a mapping of Excel column names to Product model fields
            column_mapping = {
                'Image': 'image',
                'Title': 'title',
                'Buy Box: % Amazon 30 days': 'buy_box_percentage_amazon_30_days',
                'Buy Box Eligible Offer Count: New FBA': 'buy_box_eligible_offer_count_new_fba',
                'Amazon: Current': 'amazon_current_price',
                'Amazon: Stock': 'amazon_stock',
                'List Price: Current': 'list_price_current',
                'List Price: 30 days avg.': 'list_price_30_days_avg',
                'Count of retrieved live offers: New, FBA': 'live_offers_fba',
                'Count of retrieved live offers: New, FBM': 'live_offers_fbm',
                'URL: Amazon': 'url_amazon',
                'Categories: Root': 'categories_root',
                'Categories: Sub': 'categories_sub',
                'Categories: Tree': 'categories_tree',
                'Launchpad': 'launchpad',
                'ASIN': 'asin',
                'Manufacturer': 'manufacturer',
                'Unit Count: Unit Value': 'unit_count_value',
                'Unit Count: Unit Type': 'unit_count_type',
                'Material': 'material',
                'Item Type': 'item_type',
                'Number of Items': 'number_of_items',
                'Video Count': 'video_count',
                'Has Main Video': 'has_main_video',
                'Main Videos': 'main_videos',
                'Additional Videos': 'additional_videos',
                'Package: Dimension (cm³)': 'package_dimension_cm3',
                'Package: Weight (g)': 'package_weight_g',
                'Package: Quantity': 'package_quantity',
                'Item: Dimension (cm³)': 'item_dimension_cm3',
                'Item: Length (cm)': 'item_length_cm',
                'Item: Width (cm)': 'item_width_cm',
                'Item: Height (cm)': 'item_height_cm',
                'Item: Weight (g)': 'item_weight_g',
                'Batteries Included': 'batteries_included',
                'Hazardous Materials': 'hazardous_materials',
            }

            # Create a dictionary to map column names to their indices
            column_indices = {name: idx for idx, name in enumerate(headers)}

            # Skip the first row (header) and process the data rows
            for row in sheet.iter_rows(min_row=2, values_only=True):  # Start from row 2
                asin = row[column_indices['ASIN']]  # Get ASIN value using the column index
                country_id = request.POST.get('country')  # Get the selected country ID from form
                country = Country.objects.get(id=country_id) if country_id else None

                if asin and asin not in existing_asins:
                    # Map Excel columns to Product model fields dynamically
                    product_data = {
                        'store': store,
                        'country': country,
                        'title': row[column_indices['Title']],
                        'buy_box_percentage_amazon_30_days': row[column_indices['Buy Box: % Amazon 30 days']],
                        'buy_box_eligible_offer_count_new_fba': row[column_indices['Buy Box Eligible Offer Count: New FBA']],
                        'amazon_current_price': self._parse_decimal(row[column_indices['Amazon: Current']]),
                        'amazon_stock': self._parse_integer(row[column_indices['Amazon: Stock']]),
                        'list_price_current': self._parse_decimal(row[column_indices['List Price: Current']]),
                        'list_price_30_days_avg': self._parse_decimal(row[column_indices['List Price: 30 days avg.']]),
                        'live_offers_fba': self._parse_integer(row[column_indices['Count of retrieved live offers: New, FBA']]),
                        'live_offers_fbm': self._parse_integer(row[column_indices['Count of retrieved live offers: New, FBM']]),
                        'url_amazon': row[column_indices['URL: Amazon']],
                        'categories_root': row[column_indices['Categories: Root']],
                        'categories_sub': row[column_indices['Categories: Sub']],
                        'categories_tree': row[column_indices['Categories: Tree']],
                        'launchpad': row[column_indices['Launchpad']],
                        'asin': asin,
                        'manufacturer': row[column_indices['Manufacturer']],
                        'unit_count_value': row[column_indices['Unit Count: Unit Value']],
                        'unit_count_type': row[column_indices['Unit Count: Unit Type']],
                        'material': row[column_indices['Material']],
                        'item_type': row[column_indices['Item Type']],
                        'number_of_items': self._parse_integer(row[column_indices['Number of Items']]),
                        'video_count': self._parse_integer(row[column_indices['Video Count']]),
                        'has_main_video': self._parse_boolean(row[column_indices['Has Main Video']]),
                        'main_videos': row[column_indices['Main Videos']],
                        'additional_videos': self._clean_text(row[column_indices['Additional Videos']]),  # Clean text
                        'package_dimension_cm3': self._parse_decimal(row[column_indices['Package: Dimension (cm³)']]),
                        'package_weight_g': self._parse_decimal(row[column_indices['Package: Weight (g)']]),
                        'package_quantity': self._parse_integer(row[column_indices['Package: Quantity']]),
                        'item_dimension_cm3': self._parse_decimal(row[column_indices['Item: Dimension (cm³)']]),
                        'item_length_cm': self._parse_decimal(row[column_indices['Item: Length (cm)']]),
                        'item_width_cm': self._parse_decimal(row[column_indices['Item: Width (cm)']]),
                        'item_height_cm': self._parse_decimal(row[column_indices['Item: Height (cm)']]),
                        'item_weight_g': self._parse_decimal(row[column_indices['Item: Weight (g)']]),
                        'batteries_included': self._parse_boolean(row[column_indices['Batteries Included']]),
                        'hazardous_materials': row[column_indices['Hazardous Materials']],
                        'image': self._truncate_url(row[column_indices['Image']], max_length=500),
                    }

                    # Create the Product instance
                    Product.objects.create(**product_data)
                    existing_asins.add(asin)  # Update the set to avoid re-adding during the same upload
                    count += 1
                elif asin in existing_asins:
                    product_data = {
                        'amazon_current_price': self._parse_decimal(row[column_indices['Amazon: Current']]),
                        'amazon_stock': self._parse_integer(row[column_indices['Amazon: Stock']]),
                        'list_price_current': self._parse_decimal(row[column_indices['List Price: Current']]),
                        'list_price_30_days_avg': self._parse_decimal(row[column_indices['List Price: 30 days avg.']]),
                    }
                    Product.objects.update(**product_data)
                    duplicate_count += 1

            messages.success(request, f"{count} new products added successfully! {duplicate_count} duplicates records were found.")
        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")
            return render(request, self.template_name, {'store': store, 'countries': countries})

        # Redirect back to the store view
        return redirect('customers:stores_view', pk=store.id)

    def _parse_decimal(self, value):
        """Helper method to parse decimal values from Excel."""
        if value is None or value == "":
            return None
        try:
            return float(value)  # Convert to float first, then Django will handle it as Decimal
        except (ValueError, TypeError):
            return None

    def _parse_integer(self, value):
        """Helper method to parse integer values from Excel."""
        if value is None or value == "":
            return None
        try:
            return int(value)  # Convert to integer
        except (ValueError, TypeError):
            return None

    def _parse_boolean(self, value):
        """Helper method to parse boolean values from Excel."""
        if value is None or value == "":
            return None
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            value = value.lower().strip()
            if value in ("true", "yes", "1", "t", "y"):
                return True
            elif value in ("false", "no", "0", "f", "n"):
                return False
        if isinstance(value, (int, float)):
            return bool(value)
        return None

    def _truncate_url(self, url, max_length=500):
        """Helper method to truncate URLs to a maximum length."""
        if url is None or url == "":
            return None
        if len(url) > max_length:
            return url[:max_length]  # Truncate the URL to the maximum length
        return url

    def _clean_text(self, text):
        """Helper method to remove unsupported characters (e.g., emojis)."""
        if text is None or text == "":
            return None
        # Remove non-ASCII characters
        return re.sub(r'[^\x00-\x7F]+', '', text)
