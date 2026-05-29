"""Django admin customization with filters and inlines."""

from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html

from shop.models import (
    Article,
    ClientProfile,
    CompanyHistory,
    CompanyInfo,
    ContactPerson,
    Coupon,
    EmployeeProfile,
    FAQEntry,
    Manufacturer,
    Order,
    OrderItem,
    PickupPoint,
    Product,
    ProductCategory,
    PromoCode,
    Review,
    Vacancy,
)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('line_total_display',)

    @admin.display(description='Line total')
    def line_total_display(self, obj):
        if obj.pk:
            return obj.line_total
        return '—'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'sale_date', 'delivery_date', 'delivery_cost', 'items_total_display', 'grand_total_display')
    list_filter = ('sale_date', 'delivery_date', 'employee')
    search_fields = ('client__user__username', 'client__phone', 'notes')
    inlines = [OrderItemInline]
    date_hierarchy = 'sale_date'
    autocomplete_fields = ('client', 'employee', 'pickup_point', 'promo_code')

    @admin.display(description='Items total')
    def items_total_display(self, obj):
        return obj.items_total

    @admin.display(description='Grand total')
    def grand_total_display(self, obj):
        return obj.grand_total


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'unit', 'manufacturer', 'is_available')
    list_filter = ('category', 'unit', 'is_available', 'manufacturer')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_available')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'email', 'birth_date', 'age_display')
    search_fields = ('user__username', 'phone', 'email')
    list_filter = ('created_at',)

    @admin.display(description='Age')
    def age_display(self, obj):
        return obj.age


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'phone')
    filter_horizontal = ('clients',)
    search_fields = ('user__username',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    search_fields = ('name', 'country')


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'is_active', 'valid_from', 'valid_until')
    list_filter = ('is_active',)
    search_fields = ('code', 'description')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)


@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    search_fields = ('name', 'address')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'published_at')
    list_filter = ('is_published',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'rating', 'review_date', 'user')
    list_filter = ('rating', 'review_date')


admin.site.register(CompanyInfo)
admin.site.register(CompanyHistory)
admin.site.register(FAQEntry)
admin.site.register(ContactPerson)
admin.site.register(Vacancy)
