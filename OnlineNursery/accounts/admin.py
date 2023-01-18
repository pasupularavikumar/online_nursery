from django.contrib import admin

from .models import *


admin.site.register(Product)
admin.site.register(cartObject)
admin.site.register(cart)
admin.site.register(placedOrder)

# Register your models here.
