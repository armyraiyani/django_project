from django.contrib import admin
from .models import Country, City, Food, Order, OrderItem, Restaurant, User

# Inline Restaurant inside Country
class RestaurantInline(admin.TabularInline):
    model = Restaurant
    extra = 0
    # Show city in inline
    fields = ('name', 'city', 'rating')
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')

# Country Admin
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_code', 'dial_code', 'currency_code')
    search_fields = ('name',)
    inlines = [RestaurantInline]


# City Admin
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name',)
    list_filter = ('country',)


# Restaurant Admin
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'city', 'owner', 'rating', 'slug')
    list_filter = ('country', 'city')
    search_fields = ('name', 'city__name', 'country__name', 'owner__username')


# Food Admin
@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'get_country', 'price')
    list_filter = ('restaurant__country',)
    search_fields = ('name', 'restaurant__name')

    def get_country(self, obj):
        return obj.restaurant.country.name
    get_country.short_description = "Country"


# Inline OrderItem inside Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'restaurant', 'total_amount', 'status', 'created_at')
    inlines = [OrderItemInline]
    list_filter = ('status', 'restaurant')


# OrderItem Admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'food', 'quantity')
    list_filter = ('food__restaurant__country',)