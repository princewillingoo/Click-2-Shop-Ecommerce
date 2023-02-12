from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    
    def order_payment(self, obj):
        url = obj.get_paystack_ref_url()
        if obj.paystack_payment_ref:
            html = f'<a href="{url}" target="_blank">{obj.paystack_payment_ref}</a>'
            return mark_safe(html)
        return ''

    order_payment.short_description = 'Paystack payment'
    
    list_display = [
        'id', 'first_name', 'last_name', 'email',
        'address', 'postal_code', 'city', 'paid',
        'order_payment', 'created', 'updated'
    ]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]