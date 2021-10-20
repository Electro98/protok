from django.contrib import admin

from . import models


@admin.register(models.Transformer)
class AuthorTransformer(admin.ModelAdmin):
    pass


@admin.register(models.HighVoltageDevice)
class AuthorHighVoltageDevice(admin.ModelAdmin):
    pass


@admin.register(models.LowVoltageDevice)
class AuthorLowVoltageDevice(admin.ModelAdmin):
    pass


@admin.register(models.Client)
class AuthorClient(admin.ModelAdmin):
    pass


@admin.register(models.Order)
class AuthorOrder(admin.ModelAdmin):
    pass
