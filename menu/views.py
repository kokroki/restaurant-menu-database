from .models import Dishes
from .models import DailyMicroelementRequirements
from .models import ComponentMicroelements
from .models import DishComponents
from .models import Components
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelform_factory
from django.apps import apps
from .models import DishProfitView
from .models import DishTypes
from django.db.models import Sum
from .models import DishTypeCaloriesReport
from django.db.models import Avg
from .models import Microelements
from .forms import DishForm, DishComponentsFormSet
from django.shortcuts import redirect, render
from .models import DishMicroelementCoverageView

#БЛЮДА (dishes)
def dishes_list(request):

    search = request.GET.get("search")
    type_filter = request.GET.get("type_id")
    sort = request.GET.get("sort")

    dishes = Dishes.objects.all()

    if search:
        dishes = dishes.filter(
            dish_name__icontains=search
        )

    if type_filter:
        dishes = dishes.filter(
            type_id=type_filter
        )

    allowed_sort_fields = [
        "dish_name",
        "-dish_name",
        "price",
        "-price",
        "calories_total",
        "-calories_total",
        "cost_price",
        "-cost_price"
    ]

    if sort in allowed_sort_fields:
        dishes = dishes.order_by(sort)

    return render(
        request,
        "dishes.html",
        {
            "dishes": dishes,

            "filter_queryset": DishTypes.objects.all(),
            "filter_field": "type_id",
            "filter_label": "Тип блюда",
            "selected_filter": type_filter,

            "sort_fields": [
                ("dish_name", "Название ↑"),
                ("-dish_name", "Название ↓"),
                ("price", "Цена ↑"),
                ("-price", "Цена ↓"),
                ("calories_total", "Калорийность ↑"),
                ("-calories_total", "Калорийность ↓"),
                ("cost_price", "Себестоимость ↑"),
                ("-cost_price", "Себестоимость ↓"),
            ],

            "selected_sort": sort,

            "reset_url": "/dishes/"
        }
    )


#ТИПЫ БЛЮД (dish_types)
def dish_types_list(request):

    search = request.GET.get("search")
    sort = request.GET.get("sort")

    dish_types = DishTypes.objects.all()

    # поиск
    if search:
        dish_types = dish_types.filter(
            type_name__icontains=search
        )

    # сортировка
    allowed_sort_fields = [
        "type_name",
        "-type_name"
    ]

    if sort in allowed_sort_fields:
        dish_types = dish_types.order_by(sort)

    return render(
        request,
        "dish_types.html",
        {
            "dish_types": dish_types,

            "sort_fields": [
                ("type_name", "Название ↑"),
                ("-type_name", "Название ↓"),
            ],

            "reset_url": "/dish_types/"
        }
    )


#СОСТАВ БЛЮД(dish_components)
from django.db.models import Q

def dish_components_list(request):

    search = request.GET.get("search")
    dish_filter = request.GET.get("dish_id")
    component_filter = request.GET.get("component_id")
    sort = request.GET.get("sort")

    items = DishComponents.objects.select_related(
        "dish",
        "component"
    )

    if search:
        items = items.filter(
            Q(dish__dish_name__icontains=search) |
            Q(component__component_name__icontains=search)
        )

    if dish_filter:
        items = items.filter(dish_id=dish_filter)

    if component_filter:
        items = items.filter(component_id=component_filter)

    allowed_sort_fields = [
        "dish__dish_name",
        "-dish__dish_name",
        "component__component_name",
        "-component__component_name",
        "amount_grams",
        "-amount_grams",
    ]

    if sort in allowed_sort_fields:
        items = items.order_by(sort)

    return render(
        request,
        "dish_components.html",
        {
            "dish_components": items,

            "filter_queryset": Dishes.objects.all(),
            "filter_field": "dish_id",
            "filter_label": "Блюдо",
            "selected_filter": dish_filter,

            "second_filter_queryset": Components.objects.all(),
            "second_filter_field": "component_id",
            "second_filter_label": "Компонент",
            "selected_second_filter": component_filter,

            "sort_fields": [
                ("dish__dish_name", "Блюдо ↑"),
                ("-dish__dish_name", "Блюдо ↓"),
                ("component__component_name", "Компонент ↑"),
                ("-component__component_name", "Компонент ↓"),
                ("amount_grams", "Количество ↑"),
                ("-amount_grams", "Количество ↓"),
            ],

            "selected_sort": sort,

            "reset_url": "/dish_components/"
        }
    )


#КОМПОНЕНТЫ (components)
def components_list(request):

    search = request.GET.get("search")

    microelement_filter = request.GET.get("microelement_id")

    calories_min = request.GET.get("calories_min")
    calories_max = request.GET.get("calories_max")

    sort = request.GET.get("sort")

    components = Components.objects.all()

    if search:
        components = components.filter(
            component_name__icontains=search
        )

    if microelement_filter:
        components = components.filter(
            componentmicroelements__microelement_id=microelement_filter
        )

    if calories_min:
        components = components.filter(
            calories__gte=calories_min
        )

    if calories_max:
        components = components.filter(
            calories__lte=calories_max
        )

    allowed_sort_fields = [
        "component_name",
        "-component_name",
        "calories",
        "-calories",
        "price",
        "-price",
        "weight",
        "-weight",
        "price_per_gram",
        "-price_per_gram"
    ]

    if sort in allowed_sort_fields:
        components = components.order_by(sort)

    return render(
        request,
        "components.html",
        {

            "components": components,

            "filter_queryset": Microelements.objects.all(),
            "filter_field": "microelement_id",
            "filter_label": "Микроэлемент",
            "selected_filter": microelement_filter,

            "sort_fields": [
                ("component_name", "Название ↑"),
                ("-component_name", "Название ↓"),
                ("calories", "Калории ↑"),
                ("-calories", "Калории ↓"),
                ("price", "Цена ↑"),
                ("-price", "Цена ↓"),
                ("weight", "Вес ↑"),
                ("-weight", "Вес ↓"),
                ("price_per_gram", "Цена за грамм ↑"),
                ("-price_per_gram", "Цена за грамм ↓"),
            ],

            "selected_sort": sort,

            "reset_url": "/components/"
        }
    )


#СОСТАВ КОМПОНЕНТОВ (components_microelements)
def component_microelements_list(request):

    search = request.GET.get("search")
    sort = request.GET.get("sort")

    items = ComponentMicroelements.objects.select_related(
        "component",
        "microelement"
    )

    if search:
        items = items.filter(
            Q(component__component_name__icontains=search) |
            Q(microelement__microelement_name__icontains=search)
        )

    allowed_sort_fields = [
        "component__component_name",
        "-component__component_name",
        "microelement__microelement_name",
        "-microelement__microelement_name",
        "amount_per_100g",
        "-amount_per_100g",
    ]

    if sort in allowed_sort_fields:
        items = items.order_by(sort)

    return render(
        request,
        "component_microelements.html",
        {

            "component_microelements": items,

            "sort_fields": [
                ("component__component_name", "Компонент ↑"),
                ("-component__component_name", "Компонент ↓"),
                ("microelement__microelement_name", "Микроэлемент ↑"),
                ("-microelement__microelement_name", "Микроэлемент ↓"),
                ("amount_per_100g", "Количество ↑"),
                ("-amount_per_100g", "Количество ↓"),
            ],

            "selected_sort": sort,

            "reset_url": "/component_microelements/"
        }
    )


#МИКРОЭЛЕМЕНТЫ (microelements)
def microelements_list(request):

    search = request.GET.get("search")
    sort = request.GET.get("sort")

    microelements = Microelements.objects.all()

    if search:
        microelements = microelements.filter(
            microelement_name__icontains=search
        )

    allowed_sort_fields = [
        "microelement_name"
    ]

    if sort in allowed_sort_fields:
        microelements = microelements.order_by(sort)

    return render(
        request,
        "microelements.html",
        {
            "microelements": microelements,
            "sort_fields": [
                ("microelement_name", "Название")
            ],
            "reset_url": "/microelements/"
        }
    )


#СУТОЧНЫЕ НОРМЫ (daily_components_requirem)
def daily_microelement_requirements_list(request):

    search = request.GET.get("search")
    sort = request.GET.get("sort")

    items = DailyMicroelementRequirements.objects.select_related(
        "microelement"
    )

    if search:
        items = items.filter(
            microelement__microelement_name__icontains=search
        )

    allowed_sort_fields = [
        "microelement__microelement_name",
        "-microelement__microelement_name",
        "daily_amount_mg",
        "-daily_amount_mg",
    ]

    if sort in allowed_sort_fields:
        items = items.order_by(sort)

    return render(
        request,
        "daily_microelement_requirements.html",
        {
            "requirements": items,

            "sort_fields": [
                ("microelement__microelement_name", "Микроэлемент ↑"),
                ("-microelement__microelement_name", "Микроэлемент ↓"),
                ("daily_amount_mg", "Норма ↑"),
                ("-daily_amount_mg", "Норма ↓"),
            ],

            "selected_sort": sort,

            "reset_url": "/daily_microelement_requirements/"
        }
    )


#отчеты
def report_profit(request):

    type_filter = request.GET.get("type_id")
    sort = request.GET.get("sort")

    report = DishProfitView.objects.all()

    if type_filter:
        report = report.filter(type_id=type_filter)

    allowed_sort = [
        "profit",
        "-profit",
        "price",
        "-price",
        "cost_price",
        "-cost_price",
        "dish_name",
        "-dish_name"
    ]

    if sort in allowed_sort:
        report = report.order_by(sort)

    total_profit = report.aggregate(
        Sum("profit")
    )

    return render(
        request,
        "report_profit.html",
        {
            "report": report,
            "dish_types": DishTypes.objects.all(),
            "total_profit": total_profit["profit__sum"]
        }
    )


def report_calories_by_type(request):

    min_calories = request.GET.get("min_calories")
    max_calories = request.GET.get("max_calories")
    sort = request.GET.get("sort", "")

    report = DishTypeCaloriesReport.objects.all()

    if min_calories:
        report = report.filter(avg_calories__gte=min_calories)

    if max_calories:
        report = report.filter(avg_calories__lte=max_calories)

    allowed_sort = [
        "type_name",
        "-type_name",
        "avg_calories",
        "-avg_calories",
        "max_calories",
        "-max_calories",
        "min_calories",
        "-min_calories",
        "dishes_count",
        "-dishes_count",
    ]

    if sort in allowed_sort:
        report = report.order_by(sort)

    return render(
        request,
        "report_calories_by_type.html",
        {
            "report": report,
            "min_calories": min_calories,
            "max_calories": max_calories,
            "sort": sort,
            "reset_url": "/reports/calories-by-type/"
        }
    )


def report_microelement_coverage(request):

    microelement_filter = request.GET.get("microelement_id")
    sort = request.GET.get("sort")

    report = DishMicroelementCoverageView.objects.all()

    if microelement_filter:
        report = report.filter(
            microelement_id=microelement_filter
        )

    allowed_sort = [
        "dish_name",
        "-dish_name",
        "coverage_percent",
        "-coverage_percent"
    ]

    if sort in allowed_sort:
        report = report.order_by(sort)

    avg_coverage = report.aggregate(
        Avg("coverage_percent")
    )["coverage_percent__avg"]

    return render(
        request,
        "report_microelement_coverage.html",
        {
            "report": report,
            "avg_coverage": avg_coverage,
            "filter_queryset": Microelements.objects.all(),
        }
    )


#добавление
def universal_add(request, model_name):

    model = apps.get_model("menu", model_name)

    Form = modelform_factory(model, fields="__all__")

    if request.method == "POST":
        form = Form(request.POST)

        if form.is_valid():
            form.save()
            return redirect(request.GET.get("next", "/dishes/"))

    else:
        form = Form()

    return render(
        request,
        "form.html",
        {
            "form": form,
            "title": "Добавить запись"
        }
    )


#редактирование
def universal_edit(request, model_name, pk):

    model = apps.get_model("menu", model_name)

    obj = get_object_or_404(model, pk=pk)

    Form = modelform_factory(model, fields="__all__")

    if request.method == "POST":
        form = Form(request.POST, instance=obj)

        if form.is_valid():
            form.save()
            return redirect(request.GET.get("next", "/dishes/"))

    else:
        form = Form(instance=obj)

    return render(
        request,
        "form.html",
        {
            "form": form,
            "title": "Редактирование записи"
        }
    )


#удаление
def universal_delete(request, model_name, pk):

    model = apps.get_model("menu", model_name)

    obj = get_object_or_404(model, pk=pk)

    obj.delete()

    return redirect(request.META.get("HTTP_REFERER", "/dishes/"))


def add_dish_with_components(request):

    if request.method == "POST":

        form = DishForm(request.POST)
        formset = DishComponentsFormSet(request.POST)

        if form.is_valid():
            dish = form.save()

            formset = DishComponentsFormSet(
                request.POST,
                instance=dish
            )

            if formset.is_valid():
                formset.save()
                return redirect("/dishes/")

    else:
        form = DishForm()
        formset = DishComponentsFormSet()

    return render(
        request,
        "add_dish_with_components.html",
        {
            "form": form,
            "formset": formset
        }
    )

