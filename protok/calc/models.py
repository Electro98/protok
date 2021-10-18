from django.db import models
from django.core.validators import MinValueValidator


class InputOutputType(models.IntegerChoices):
    AIR = 0, 'Воздух'
    CABLE = 1, 'Кабель'


class Transformer:
    """Модель трансформатора"""
    class Meta:
        verbose_name = "Силовой трансформатор"
        verbose_name_plural = "Силовые трансформаторы"

    class TransformerTypes(models.TextChoices):
        """Типы трансформаторов"""
        OIL = 'ТМ', 'ТМ'
        OIL_HERMETIC = 'ТМГ', 'ТМГ'
        DRY = 'ТС', 'ТС(3)'
        DRY_CAST = 'ТСЛ', 'ТСЛ(3)'

    class ConnectionSchemes(models.TextChoices):
        """Схемы подключения обмоток"""
        STAR_TRIA = 'Д/У', 'Д/У'
        STAR_STAR = 'У/У', 'У/У'
        STAR_ZIGZ = 'У/Z', 'У/Z'
        OTHER = 'Другое', 'Другое'

    name = models.CharField(verbose_name='Наименование', max_length=200)
    manufacturer = models.CharField(verbose_name='Производитель', max_length=200)
    transformer_type = models.CharField(
        verbose_name='Тип трансформатора', choices=TransformerTypes.choices,
        default=TransformerTypes.DRY, max_length=3
    )
    connection_scheme = models.CharField(
        verbose_name='Схема соединения обмоток', choices=ConnectionSchemes.choices,
        default=ConnectionSchemes.STAR_STAR, max_length=10
    )
    power = models.IntegerField(
        verbose_name='Мощность трансформатора',
        validators=[MinValueValidator(0)]
    )
    voltage = models.IntegerField(
        verbose_name='Напряжение трансформатора',
        validators=[MinValueValidator(0)]
    )
    price = models.FloatField(
        verbose_name='Стоимость', validators=[MinValueValidator(0)]
    )
    documentation = models.FileField(
        verbose_name='Конструкторская документация',
        upload_to='documentation/transformers'
    )
    # count = models.IntegerField(verbose_name='Количество трансформаторов')


class HighVoltageDevice(models.Model):
    """Модель устройства высокого напряжения"""
    class Meta:
        verbose_name = "Устройство ВН"
        verbose_name_plural = "Устройства ВН"

    class ArresterTypes(models.IntegerChoices):
        VALVE = 0, 'РВО'
        NONLINEAR = 1, 'ОПН'
        NO = 2, 'Нет'

    name = models.CharField(verbose_name='Наименование', max_length=200)
    manufacturer = models.CharField(verbose_name='Производитель', max_length=200)
    input_type = models.IntegerField(
        verbose_name='Ввод', choices=InputOutputType.choices,
        default=InputOutputType.CABLE
    )
    voltage = models.IntegerField(
        verbose_name='Номинальное напряжение на стороне ВН',
        validators=[MinValueValidator(0)]
    )
    arrester = models.IntegerField(
        verbose_name='Тип разрядника', choices=ArresterTypes.choices,
        default=ArresterTypes.NO
    )


class LowVoltageDevice(models.Model):
    """Модель устройства низкого напряжения"""
    class Meta:
        verbose_name = "Устройство НН"
        verbose_name_plural = "Устройства НН"

    name = models.CharField(verbose_name='Наименование', max_length=200)
    manufacturer = models.CharField(verbose_name='Производитель', max_length=200)
    input_type = models.IntegerField(
        verbose_name='Ввод', choices=InputOutputType.choices,
        default=InputOutputType.CABLE
    )
