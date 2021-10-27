import enum

from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

from phonenumber_field.modelfields import PhoneNumberField


class InputOutputType(models.IntegerChoices):
    """Типы ввода/вывода"""
    AIR = 0, 'Воздух'
    CABLE = 1, 'Кабель'


class ArresterAvailabilityHighVoltage(models.IntegerChoices):
    """Типы разрядников"""
    VALVE = 0, 'РВО'
    NONLINEAR = 1, 'ОПН'
    NO = 2, 'Нет'


class ArresterAvailabilityLowVoltage(models.IntegerChoices):
    """Типы разрядников"""
    VALVE = 0, 'РВН'
    NONLINEAR = 1, 'ОПН'
    NO = 2, 'Нет'


class ConnectionTypes(models.IntegerChoices):
    CABLE = 0, 'Кабель'
    BUS = 1, 'Шина'


class StreetIllumination(models.IntegerChoices):
    NO = 0, 'Нет'
    YES = 1, 'Да'


class LineType(models.IntegerChoices):
    POWER = 25
    PRICE = 31.5


class Product(models.Model):
    """Модель продукта"""

    class Meta:
        abstract = True

    name = models.CharField(verbose_name='Наименование', max_length=200)
    manufacturer = models.CharField(verbose_name='Производитель', max_length=200)

    price = models.FloatField(
        verbose_name='Стоимость', validators=[MinValueValidator(0)]
    )
    documentation = models.FileField(
        verbose_name='Конструкторская документация',
        upload_to='documentation/other'
    )


class Transformer(Product):
    """Модель трансформатора"""

    class Meta:
        verbose_name = "Силовой трансформатор"
        verbose_name_plural = "Силовые трансформаторы"

    class TransformerTypes(models.TextChoices):
        """Типы трансформаторов"""
        OIL = 'ТМ', 'Масляный'
        OIL_HERMETIC = 'ТМГ', 'Масляный герметичный'
        DRY = 'Сухой'

    class ConnectionSchemes(models.TextChoices):
        """Схемы подключения обмоток"""
        STAR_TRIA = 'Д/У', 'Треугольник/Звезда'
        STAR_STAR = 'У/У', 'Звезда/Звезда'

    transformer_type = models.CharField(
        verbose_name='Тип трансформатора', choices=TransformerTypes.choices,
        default=TransformerTypes.DRY, max_length=5
    )
    connection_scheme = models.CharField(
        verbose_name='Схема соединения обмоток', choices=ConnectionSchemes.choices,
        default=ConnectionSchemes.STAR_STAR, max_length=10
    )
    power = models.IntegerField(
        verbose_name='Мощность трансформатора',
        validators=[MinValueValidator(20), MaxValueValidator(630)]
    )
    voltage = models.IntegerField(
        verbose_name='Напряжение трансформатора',
        validators=[MinValueValidator(0)]
    )
    documentation = models.FileField(
        verbose_name='Конструкторская документация',
        upload_to='documentation/transformers'
    )
    count = models.IntegerField(
        verbose_name='Количество трансформаторов',
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f'{self.name}'


class HighVoltageDevice(Product):
    """Модель устройства высокого напряжения"""

    class Meta:
        verbose_name = "Устройство ВН"
        verbose_name_plural = "Устройства ВН"

    class EquipmentTypes(models.IntegerChoices):
        INPUT_AUTOGAS = 0, 'ВНА'
        INPUT_INNER = 1, 'РВЗ'
        SWITCH_AUTOGAS = 2, 'РЛНД'
        NO = 3, 'Нет'

    class WireType(models.IntegerChoices):
        COPPER = 0, 'Медь'
        ALUMINIUM = 1, 'Алюминий'

    class NominalVoltage(models.IntegerChoices):
        SIX = 6,
        TEN = 10,

    input_type = models.IntegerField(
        verbose_name='Ввод', choices=InputOutputType.choices,
        default=InputOutputType.CABLE
    )
    voltage = models.IntegerField(
        verbose_name='Номинальное напряжение на стороне ВН',
        validators=[MinValueValidator(0)]
    )
    arrester = models.IntegerField(
        verbose_name='Тип разрядника', choices=ArresterAvailabilityHighVoltage.choices,
        default=ArresterAvailabilityHighVoltage.NO
    )
    equipment_type = models.IntegerField(
        verbose_name='Тип оборудования РУНВ', choices=EquipmentTypes.choices,
        default=EquipmentTypes.INPUT_AUTOGAS
    )
    registration = models.BooleanField(
        verbose_name='Наличие учета по стороне ВН', default=True
    )
    connection_type = models.IntegerField(
        verbose_name='Тип соединения РУНВ-Трансформатор', choices=ConnectionTypes.choices,
        default=ConnectionTypes.CABLE
    )
    documentation = models.FileField(
        verbose_name='Конструкторская документация',
        upload_to='documentation/hv_devices'
    )

    def __str__(self):
        return f'{self.name}'


class LowVoltageDevice(Product):
    """Модель устройства низкого напряжения"""

    class Meta:
        verbose_name = "Устройство НН"
        verbose_name_plural = "Устройства НН"

    class InputDeviceTypes(models.IntegerChoices):
        DISCONNECTOR = 0, 'Разъединитель'
        CIRCUIT_BREAKER = 1, 'Автоматический выключатель'
        DISCONNECTOR_CB = 2, 'Разъединитель + Автоматический выключатель'

    class WireType(models.IntegerChoices):
        COPPER = 0, 'Медь'
        ALUMINIUM = 1, 'Алюминий'

    class CommuteDevice(models.IntegerChoices):
        MANUAL_INPUT = 0, 'Ручное включение'
        DISCONNECTOR = 1, 'Разъединитель'
        AUTOMATIC_SWITCHER = 2, 'Автоматический выключатель'

    input_type = models.IntegerField(
        verbose_name='Ввод', choices=InputOutputType.choices,
        default=InputOutputType.CABLE
    )
    arrester = models.IntegerField(
        verbose_name='Тип разрядника', choices=ArresterAvailabilityLowVoltage.choices,
        default=ArresterAvailabilityLowVoltage.NO
    )
    voltage = models.IntegerField(
        verbose_name='Номинальное напряжение на стороне НН',
        validators=[MinValueValidator(0)]
    )
    input_device = models.IntegerField(
        verbose_name='Вводное устройство', choices=InputDeviceTypes.choices,
        default=InputDeviceTypes.DISCONNECTOR
    )
    input_denomination = models.IntegerField(
        verbose_name='Номинал вводного устройства',
        default=100, validators=[MinValueValidator(0)]
    )
    registration = models.BooleanField(
        verbose_name='Наличие учета по стороне ВН', default=True
    )
    connection_type = models.IntegerField(
        verbose_name='Тип соединения Трансформатор-РУНН', choices=ConnectionTypes.choices,
        default=ConnectionTypes.CABLE
    )
    documentation = models.FileField(
        verbose_name='Конструкторская документация',
        upload_to='documentation/ll_devices'
    )

    def __str__(self):
        return f'{self.name}'


class ComlexTransformerSubstation(Product):
    class Meta:
        verbose_name = "Комплексная трансформаторная подстанция"
        verbose_name_plural = "Комплексные трансформаторные подстанции"

    class ComlexTransformerSubstationType(models.TextChoices):
        KIOSK_DEAD_END = "Киосковая тупиковая", "КТП/Т"
        KIOSK_ENTRANCE = "Киосковая проходная", "КТП/П"
        DEAD_END_INSULATED = "Тупиковая утепленная типа 'сэндвич'", "КТП/TC"
        ENTRANCE_INSULATED = "Проходная утепленная типа 'сэндвич'", "КТП/ПС"

    type_station = models.CharField(
        verbose_name='Тип подстанции', choices=ComlexTransformerSubstationType.choices,
        default=ComlexTransformerSubstationType.KIOSK_DEAD_END, max_length=124
    )
    documentation = models.FileField(
        verbose_name='Дополнительные файлы',
        upload_to='documentation/substations'
    )


class Fiders(Product):
    class Meta:
        verbose_name = "Фидер"
        verbose_name_plural = "Фидеры"

    amperage = models.FloatField(
        verbose_name="Сила тока, A",
        validators=[MinValueValidator(0)]
    )
    documentation = models.FileField(
        verbose_name='Дополнительные файлы',
        upload_to='documentation/fiders'
    )


class Section(models.Model):
    """Модель секции"""

    class Meta:
        verbose_name = "Секция"
        verbose_name_plural = "Секции"

    # power = models.IntegerField(
    #     verbose_name='Мощность',
    #     validators=[MinValueValidator(0)]
    # )
    denomination = models.IntegerField(
        verbose_name='Номинальный ток',
        validators=[MinValueValidator(0)]
    )
    lv_device = models.ForeignKey(
        to=LowVoltageDevice, on_delete=models.CASCADE
    )
    fider = models.ForeignKey(
        to=Fiders, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    count = models.IntegerField(
        verbose_name="Количество линий",
        validators=[MinValueValidator(0)]
    )

    @property
    def price(self):
        return self.count * self.fider.price


class Client(models.Model):
    """Модель клиента"""

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    full_name = models.CharField(verbose_name='ФИО', max_length=254)
    organization = models.CharField(verbose_name='Наименвоание организации', max_length=254)
    email = models.EmailField(verbose_name='E-mail', max_length=254)
    phone_number = PhoneNumberField(verbose_name='Номер телефона')

    def __str__(self):
        return f'{self.organization}'


class Order(models.Model):
    """Модель заказа"""

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    transformer = models.ForeignKey(
        to=Transformer, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    lv_device = models.ForeignKey(
        to=LowVoltageDevice, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    hv_device = models.ForeignKey(
        to=HighVoltageDevice, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    substation = models.ForeignKey(
        to=ComlexTransformerSubstation, on_delete=models.SET_NULL,
        null=True, blank=True
    )

    # Информация о клиенте
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    comment = models.TextField(
        verbose_name='Комментарий', max_length=1024,
        null=True, blank=True
    )
    create_date = models.DateField(verbose_name='Дата', auto_now_add=True)
    documentation = models.FileField(
        verbose_name='Дополнительные файлы',
        upload_to='orders/'
    )

    @property
    def count_price(self):
        substation_price = self.substation.price
        transformer_price = self.transformer.price
        hv_device_price = self.hv_device.price
        lv_device_price = self.lv_device.price
        all_section = self.lv_device.section_set.all()
        section_price = sum(item.price for item in all_section)
        return (substation_price + transformer_price +
                hv_device_price + lv_device_price + section_price)

    def documentation_assembling(self):
        substation_documentation = self.substation.documentation
        transformer_documentation = self.transformer.documentation
        hv_device_documentation = self.hv_device.documentation
        lv_device_documentation = self.lv_device.documentation
        all_section = self.lv_device.section_set.all()
        section_documentation = [item.documentation for item in all_section]
        return [substation_documentation, transformer_documentation,
                hv_device_documentation, lv_device_documentation] + section_documentation



