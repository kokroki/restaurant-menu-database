from django.contrib import admin
from django.urls import path
from menu import views
from menu.views import dishes_list
from menu.views import microelements_list
from menu.views import dish_types_list
from menu.views import daily_microelement_requirements_list
from menu.views import component_microelements_list
from menu.views import dish_components_list
from menu.views import components_list
from menu.views import report_profit
from menu.views import universal_add, universal_edit
from menu.views import universal_delete


urlpatterns = [
    path("", dishes_list),
    path('admin/', admin.site.urls),
    path('dishes/', dishes_list),
    path('components/', components_list),
    path('microelements/', microelements_list),
    path('dish_types/', dish_types_list),
    path('daily_microelement_requirements/',daily_microelement_requirements_list),
    path('component_microelements/',component_microelements_list),
    path('dish_components/',dish_components_list),
    path('reports/profit/', report_profit),
    path("add/<str:model_name>/", universal_add),
    path("edit/<str:model_name>/<int:pk>/",universal_edit),
    path("delete/<str:model_name>/<int:pk>/",universal_delete),
    path("reports/microelement-coverage/", views.report_microelement_coverage, name="report_microelement_coverage"),
    path( "add_dish_full/", views.add_dish_with_components, name="add_dish_full"),
    path("reports/calories-by-type/", views.report_calories_by_type, name="report_calories_by_type"),
]

