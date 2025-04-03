from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .models import Product


# Create your views here.
def productDetails(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        data = {
            "success": True,
            "title": product.title,
            "asin": product.asin,
            "image": product.image if product.image else None,
            "amazon_current_price": str(product.amazon_current_price) if product.amazon_current_price else None,
            "amazon_stock": product.amazon_stock,
            "list_price_current": str(product.list_price_current) if product.list_price_current else None,
            "list_price_30_days_avg": str(product.list_price_30_days_avg) if product.list_price_30_days_avg else None,
            "live_offers_fba": product.live_offers_fba,
            "live_offers_fbm": product.live_offers_fbm,
            "categories_root": product.categories_root,
            "categories_sub": product.categories_sub,
            "additional_videos": product.additional_videos,
            "manufacturer": product.manufacturer,
            "unit_count_value": product.unit_count_value,
            "unit_count_type": product.unit_count_type,
            "material": product.material,
            "item_type": product.item_type,
            "number_of_items": product.number_of_items,
            "video_count": product.video_count,
            "has_main_video": product.has_main_video,
            "package_weight_g": str(product.package_weight_g) if product.package_weight_g else None,
            "item_length_cm": str(product.item_length_cm) if product.item_length_cm else None,
            "item_width_cm": str(product.item_width_cm) if product.item_width_cm else None,
            "item_height_cm": str(product.item_height_cm) if product.item_height_cm else None,
            "batteries_included": product.batteries_included,
            "hazardous_materials": product.hazardous_materials,
            "description": product.description or "No description available",
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
    

class ProductsListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 25  # This will be our page size for infinite scroll

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(asin__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX request - return JSON data
            page_obj = context['page_obj']
            products = []
            
            for product in page_obj.object_list:
                product_data = {
                    'id': product.id,
                    'title': product.title,
                    'asin': product.asin,
                    'image': product.image,
                    'amazon_current_price': str(product.amazon_current_price) if product.amazon_current_price else None,
                    'amazon_stock': product.amazon_stock,
                    'url_amazon': product.url_amazon,
                    'store_name': product.store.name if product.store else None
                }
                products.append(product_data)
            
            data = {
                'products': products,
                'has_next': page_obj.has_next(),
                'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None
            }
            return JsonResponse(data)
        # Regular request - return HTML
        return super().render_to_response(context, **response_kwargs)