from django.contrib import admin

from . import models


@admin.register(models.Transformer)
class AdminTransformer(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'power', 'transformer_type', 'price')


@admin.register(models.HighVoltageDevice)
class AdminHighVoltageDevice(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'voltage', 'input_type', 'equipment_type', 'price')


class SectionInline(admin.TabularInline):
    model = models.Section


@admin.register(models.LowVoltageDevice)
class AdminLowVoltageDevice(admin.ModelAdmin):
    inlines = [SectionInline]
    list_display = ('name', 'manufacturer', 'voltage', 'input_type', 'input_device')


@admin.register(models.Client)
class AdminClient(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number')


@admin.register(models.Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ('client', 'transformer', 'lv_device', 'hv_device', 'create_date', 'substation', 'count_price')


@admin.register(models.Fiders)
class AdminFider(admin.ModelAdmin):
    list_display = ('amperage', 'price', 'documentation')


@admin.register(models.ComlexTransformerSubstation)
class AdminComlexTransformerSubstation(admin.ModelAdmin):
    list_display = ('type_station', 'price', 'documentation')
