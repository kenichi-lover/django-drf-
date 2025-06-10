# products/admin.py
from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from .models import Product, Category
from .forms import ProductForm

# Option 1: Basic registration for Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Option 2: Custom Admin View for Products (More Control)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active', 'created_at', 'updated_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    # Override change_list_view to render a custom template
    def changelist_view(self, request, extra_context=None):
        form = ProductForm()
        products = self.get_queryset(request) # Get filtered/searched queryset if any
        context = {
            'form': form,
            'products': products,
            'title': 'Manage Products (Custom Admin)',
            'site_header': self.admin_site.site_header,
            'site_title': self.admin_site.site_title,
            'index_title': self.admin_site.index_title,
            'app_list': self.admin_site.get_app_list(request),
            ** (extra_context or {})
        }
        return TemplateResponse(request, 'admin/product_list_custom.html', context)

    # You can also add custom views for add/edit if needed,
    # or override the default admin forms with your custom forms.

    # Example: If you want to use a custom form for adds/edits within the standard admin
    # def get_form(self, request, obj=None, **kwargs):
    #     return ProductForm


admin.site.register(Product, ProductAdmin)

# Optional: Customize Admin Site Title
admin.site.site_header = "Custom Product Management Admin"
admin.site.site_title = "Product Admin Portal"
admin.site.index_title = "Welcome to Product Management"