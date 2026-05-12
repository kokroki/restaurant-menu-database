from django.contrib import admin
from .models import *
from django.contrib import admin

admin.site.site_header = "Меню ресторана"
admin.site.site_title = "Система меню"
admin.site.index_title = "Панель управления"

class DishComponentsInline(admin.TabularInline):
    model = DishComponents
    extra = 1


class DishesAdmin(admin.ModelAdmin):
    inlines = [DishComponentsInline]
    list_display = ('dish_name', 'price', 'type')
    search_fields = ('dish_name',)
    list_filter = ('type',)


admin.site.register(Dishes, DishesAdmin)
admin.site.register(DishTypes)
admin.site.register(Components)
admin.site.register(DishComponents)
admin.site.register(Microelements)
admin.site.register(ComponentMicroelements)
admin.site.register(DailyMicroelementRequirements)