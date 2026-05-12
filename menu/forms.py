from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Dishes, DishComponents


class DishForm(ModelForm):

    class Meta:
        model = Dishes
        fields = ["dish_name", "price", "type"]


DishComponentsFormSet = inlineformset_factory(
    Dishes,
    DishComponents,
    fields=("component", "amount_grams"),
    extra=3,
    can_delete=True
)