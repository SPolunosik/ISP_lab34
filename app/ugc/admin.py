from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from .models import Item, Profiler, ShoppingBasket
from .forms import ProfilerForm


@admin.register(Profiler)
class ProfilerAdmin(admin.ModelAdmin):
    list_display = ("id", "external_id", "name")
    form = ProfilerForm


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "profiler", "name", "cost", "created_at")
