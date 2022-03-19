from django.forms import widgets
from ugc.models import Profiler
from django import forms
from .models import Item, Profiler, ShoppingBasket


class ProfilerForm(forms.ModelForm):
    class Meta:
        model = Profiler
        fields = (
            'external_id',
            'name',
        )
        widgets = {
            'name': forms.TextInput,
        }