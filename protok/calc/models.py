from django.db import models
from django.core.validators import MinValueValidator

from phonenumber_field.modelfields import PhoneNumberField


class InputOutputType(models.IntegerChoices):
    """Типы ввода/вывода"""
    AIR = 0, 'Воздух'
    CABLE = 1, 'Кабель'


class ArresterTypes(models.IntegerChoices):
    """Типы разрядников"""
    VALVE = 0, 'РВО'
    NONLINEAR = 1, 'ОПН'
    NO = 2, 'Нет'


class ConnectionTypes(models.IntegerChoices):
    CABLE = 0, 'Кабель'
    BUS = 1, 'Шина'


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
        DRY = 'ТС', 'Сухой(3)'
        DRY_CAST = 'ТСЛ', 'Сухой с изоляцией(3)'

    class ConnectionSchemes(models.TextChoices):
        """Схемы подключения обмоток"""
        STAR_TRIA = 'Д/У', 'Треугольник/Звезда'
        STAR_STAR = 'У/У', 'Звезда/Звезда'
        STAR_ZIGZ = 'У/Z', 'Звезда/Зигзаг'
        OTHER = 'Другое', 'Другое'

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
    # voltage = models.IntegerField(
    #     verbose_name='Напряжение трансформатора',
    #     validators=[MinValueValidator(0)]
    # )
    documentation = models.FileField(
        verbose_name='Конструкторская документация',
        upload_to='documentation/transformers'
    )

    # count = models.IntegerField(verbose_name='Количество трансформаторов')

    def __str__(self):
        return f'{self.name}'


class HighVoltageDevice(Product):
    """Модель устройства высокого напряжения"""

    class Meta:
        verbose_name = "Устройство ВН"
        verbose_name_plural = "Устройства ВН"

    class EquipmentTypes(models.IntegerChoices):
        INPUT_AUTOGAS = 0, 'Ввод/ВНА'
        INPUT_INNER = 1, 'Ввод/РВЗ'
        TRANSFORMER_AUTOGAS = 2, 'Трансформатор/ВНА'
        TRANSFORMER_INNER = 3, 'Трансформатор/РВЗ'
        LINE_AUTOGAS = 4, 'Линия/ВНА'
        LINE_INNER = 5, 'Линия/РВЗ'
        SECTION_AUTOGAS = 6, 'Секция/ВНА'
        SECTION_INNER = 7, 'Секция/РВЗ'

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

    input_type = models.IntegerField(
        verbose_name='Ввод', choices=InputOutputType.choices,
        default=InputOutputType.CABLE
    )
    voltage = models.IntegerField(
        verbose_name='Номинальное напряжение на стороне НН',
        validators=[MinValueValidator(0)]
    )
    arrester = models.IntegerField(
        verbose_name='Тип разрядника', choices=ArresterTypes.choices,
        default=ArresterTypes.NO
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


class Section(models.Model):
    """Модель секции"""

    class Meta:
        verbose_name = "Секция"
        verbose_name_plural = "Секции"

    power = models.IntegerField(
        verbose_name='Мощность',
        validators=[MinValueValidator(0)]
    )
    denomination = models.IntegerField(
        verbose_name='Номинальный ток',
        validators=[MinValueValidator(0)]
    )
    ll_device = models.ForeignKey(
        to=LowVoltageDevice, on_delete=models.CASCADE
    )


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

    # Состав
    transformer = models.ForeignKey(
        to=Transformer, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    lw_device = models.ForeignKey(
        to=LowVoltageDevice, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    hw_device = models.ForeignKey(
        to=HighVoltageDevice, on_delete=models.SET_NULL,
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

    # TODO: добавить метод определения итоговой стоимости
    # TODO: добавить метод получение всей конструкторской документации
    # TODO: добавить метод генерации pdf со сводной информацией
