from django.contrib import admin

from . import models


@admin.register(models.Transformer)
class AuthorTransformer(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'power', 'transformer_type', 'price')


@admin.register(models.HighVoltageDevice)
class AuthorHighVoltageDevice(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'voltage', 'input_type', 'equipment_type', 'price')


class SectionInline(admin.TabularInline):
    model = models.Section


@admin.register(models.LowVoltageDevice)
class AuthorLowVoltageDevice(admin.ModelAdmin):
    inlines = [SectionInline]
    list_display = ('name', 'manufacturer', 'voltage', 'input_type', 'input_device', 'price')


@admin.register(models.Client)
class AuthorClient(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number')


@admin.register(models.Order)
class AuthorOrder(admin.ModelAdmin):
    list_display = ('client', 'transformer', 'lw_device', 'hw_device', 'create_date')
