from django.contrib import admin

from stock.models.category_model import Category
from stock.models.items_model import Items
from stock.models.units_model import Units

# Register your models here.
admin.site.register(Category)
admin.site.register(Items)
admin.site.register(Units)
