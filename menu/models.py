from django.db import models


class DishTypes(models.Model):

    type_id = models.AutoField(
        primary_key=True,
        verbose_name="ID типа блюда"
    )

    type_name = models.CharField(
        unique=True,
        max_length=100,
        verbose_name="Название типа блюда"
    )

    class Meta:
        managed = False
        db_table = "dish_types"
        verbose_name = "Тип блюда"
        verbose_name_plural = "Типы блюд"

    def __str__(self):
        return self.type_name


class Dishes(models.Model):

    dish_id = models.AutoField(primary_key=True)

    dish_name = models.CharField(
        max_length=150,
        verbose_name="Название блюда"
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Цена продажи (руб)"
    )

    cost_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Себестоимость (руб)"
    )

    calories_total = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Калорийность (руб)"
    )

    type = models.ForeignKey(
        "DishTypes",
        models.DO_NOTHING,
        verbose_name="Тип блюда"
    )

    class Meta:
        managed = False
        db_table = "dishes"

    def __str__(self):
        return self.dish_name

class Components(models.Model):

    component_id = models.AutoField(primary_key=True)

    component_name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Название компонента"
    )

    calories = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Калорийность (ккал на 100 г)"
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Цена (руб)"
    )

    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Вес упаковки (г)"
    )

    price_per_gram = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Цена за грамм (руб/г)"
    )

    class Meta:
        managed = False
        db_table = 'components'

    def __str__(self):
        return self.component_name


class DishComponents(models.Model):

    dish = models.ForeignKey(
        "Dishes",
        models.DO_NOTHING,
        verbose_name="Блюдо"
    )

    component = models.ForeignKey(
        "Components",
        models.DO_NOTHING,
        verbose_name="Компонент"
    )

    amount_grams = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Количество (г)"
    )

    class Meta:
        managed = False
        db_table = 'dish_components'


class Microelements(models.Model):

    microelement_id = models.AutoField(
        primary_key=True,
        verbose_name="ID микроэлемента"
    )

    microelement_name = models.CharField(
        unique=True,
        max_length=150,
        verbose_name="Название микроэлемента"
    )

    class Meta:
        managed = False
        db_table = "microelements"
        verbose_name = "Микроэлемент"
        verbose_name_plural = "Микроэлементы"

    def __str__(self):
        return self.microelement_name


class ComponentMicroelements(models.Model):

    id = models.AutoField(
        primary_key=True,
        verbose_name="ID записи"
    )

    component = models.ForeignKey(
        Components,
        models.DO_NOTHING,
        db_column="component_id",
        verbose_name="Компонент"
    )

    microelement = models.ForeignKey(
        Microelements,
        models.DO_NOTHING,
        db_column="microelement_id",
        verbose_name="Микроэлемент"
    )

    amount_per_100g = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        verbose_name="Количество (мг / 100 г)"
    )

    class Meta:
        managed = False
        db_table = "component_microelements"
        unique_together = (("component", "microelement"),)
        verbose_name = "Содержание микроэлемента"
        verbose_name_plural = "Содержание микроэлементов в компонентах"


class DailyMicroelementRequirements(models.Model):

    microelement = models.OneToOneField(
        "Microelements",
        models.DO_NOTHING,
        primary_key=True,
        verbose_name="Микроэлемент"
    )

    daily_amount_mg = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        verbose_name="Суточная норма (мг)"
    )

    class Meta:
        managed = False
        db_table = "daily_microelement_requirements"
        verbose_name = "Суточная норма"
        verbose_name_plural = "Суточные нормы"


class DishProfitView(models.Model):

    id = models.IntegerField(primary_key=True)

    dish_name = models.CharField(
        max_length=150,
        verbose_name="Название блюда"
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Цена продажи (руб)"
    )

    cost_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Себестоимость (руб)"
    )

    profit = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Прибыль (руб)"
    )

    type_id = models.IntegerField(
        verbose_name="Тип блюда"
    )

    class Meta:
        managed = False
        db_table = "dish_profit_view"
        verbose_name = "Прибыль блюда"
        verbose_name_plural = "Прибыль блюд"


class DishMicroelementCoverageView(models.Model):

    id = models.IntegerField(primary_key=True)

    dish_name = models.CharField(
        max_length=150,
        verbose_name="Название блюда"
    )

    microelement_id = models.IntegerField(
        verbose_name="ID микроэлемента"
    )

    microelement_name = models.CharField(
        max_length=150,
        verbose_name="Микроэлемент"
    )

    microelement_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Количество микроэлемента (мг)"
    )

    daily_amount_mg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Суточная норма (мг)"
    )

    coverage_percent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Процент покрытия нормы (%)"
    )

    class Meta:
        managed = False
        db_table = "dish_microelement_coverage_view"
        verbose_name = "Покрытие нормы микроэлемента"
        verbose_name_plural = "Покрытие нормы микроэлементов"


class DailyMicroelementMenuView(models.Model):

    id = models.IntegerField(primary_key=True)

    breakfast = models.CharField(
        max_length=150,
        verbose_name="Завтрак"
    )

    lunch = models.CharField(
        max_length=150,
        verbose_name="Обед"
    )

    dinner = models.CharField(
        max_length=150,
        verbose_name="Ужин"
    )

    microelement_name = models.CharField(
        max_length=150,
        verbose_name="Микроэлемент"
    )

    coverage_percent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Процент покрытия нормы (%)"
    )

    class Meta:
        managed = False
        db_table = "daily_microelement_menu_view"
        verbose_name = "Вариант меню"
        verbose_name_plural = "Варианты меню"


class DishTypeCaloriesReport(models.Model):

    id = models.IntegerField(primary_key=True)

    type_name = models.CharField(
        max_length=100,
        verbose_name="Тип блюда"
    )

    avg_calories = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Средняя калорийность (ккал)"
    )

    max_calories = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Максимальная калорийность (ккал)"
    )

    min_calories = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Минимальная калорийность (ккал)"
    )

    dishes_count = models.IntegerField(
        verbose_name="Количество блюд"
    )

    class Meta:
        managed = False
        db_table = "dish_type_calories_report"
        verbose_name = "Калорийность по типам блюд"
        verbose_name_plural = "Калорийность по типам блюд"