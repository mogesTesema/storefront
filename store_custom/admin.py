from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from tags.models import TaggedItem
from store.models import Product
# Register your models here.
class TageInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']



class CustomProductAdmin(ProductAdmin):
    inlines = [TageInline] 

admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)