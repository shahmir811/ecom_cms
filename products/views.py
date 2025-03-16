from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

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
