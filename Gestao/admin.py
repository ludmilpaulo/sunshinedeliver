from django.contrib import admin

from .models import Restaurant, Customer, Driver, Meal, Order, OrderDetails, User, Category, OpeningHour

@admin.register(OpeningHour)
class OpeningHourAdmin(admin.ModelAdmin):
    pass

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('get_user_username', 'name', 'phone', 'address')
    list_filter = ('name', 'address')
    search_fields = ('name', 'user__username')

    def get_user_username(self, obj):
        return obj.user.username

    get_user_username.short_description = 'User'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_address')

    def get_address(self, obj):
        return obj.restaurant.address

    get_address.short_description = 'Address'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('get_user_username', 'phone', 'address')
    list_filter = ('address',)

    def get_user_username(self, obj):
        return obj.user.username

    get_user_username.short_description = 'User'

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('get_user_username', 'phone', 'address')
    list_filter = ('address',)

    def get_user_username(self, obj):
        return obj.user.username

    get_user_username.short_description = 'User'

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'name', 'price')
    list_filter = ('restaurant', 'name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'restaurant', 'driver', 'address', 'total', 'status', 'created_at', 'picked_at')
    list_filter = ('customer', 'restaurant', 'driver', 'address', 'total', 'status', 'created_at', 'picked_at')

@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('order', 'meal', 'quantity', 'sub_total')
    list_filter = ('order', 'meal', 'quantity', 'sub_total')
