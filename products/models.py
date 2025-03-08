from django.db import models

from countries.models import Country
from customers.models import Store


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, related_name='countries')
    
    title = models.CharField(max_length=500, null=True)
    asin = models.CharField(max_length=150, null=True)
    url_amazon = models.CharField(max_length=255, null=True)
    image = models.URLField(max_length=1500, null=True, blank=True)
    
    buy_box_percentage_amazon_30_days = models.CharField(max_length=50, null=True, blank=True)
    buy_box_eligible_offer_count_new_fba = models.IntegerField(null=True, blank=True)
    amazon_current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amazon_stock = models.IntegerField(null=True, blank=True)
    list_price_current = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    list_price_30_days_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    live_offers_fba = models.IntegerField(null=True, blank=True)
    live_offers_fbm = models.IntegerField(null=True, blank=True)
    
    categories_root = models.CharField(max_length=255, null=True, blank=True)
    categories_sub = models.CharField(max_length=255, null=True, blank=True)
    categories_tree = models.TextField(null=True, blank=True)
    
    launchpad = models.CharField(max_length=100, null=True, blank=True)
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    unit_count_value = models.CharField(max_length=100, null=True, blank=True)
    unit_count_type = models.CharField(max_length=100, null=True, blank=True)
    material = models.CharField(max_length=255, null=True, blank=True)
    item_type = models.CharField(max_length=255, null=True, blank=True)
    number_of_items = models.IntegerField(null=True, blank=True)
    
    video_count = models.IntegerField(null=True, blank=True)
    has_main_video = models.BooleanField(null=True, blank=True)
    main_videos = models.TextField(null=True, blank=True)
    additional_videos = models.TextField(null=True, blank=True)
    
    package_dimension_cm3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    package_weight_g = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    package_quantity = models.IntegerField(null=True, blank=True)
    item_dimension_cm3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    item_length_cm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    item_width_cm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    item_height_cm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    item_weight_g = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    batteries_included = models.BooleanField(null=True, blank=True)
    hazardous_materials = models.CharField(max_length=255, null=True, blank=True)
    
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title if self.title else "Unnamed Product"
    def __str__(self):
        return self.title if self.title else "Unnamed Product"
