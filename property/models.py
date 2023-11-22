from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Flat(models.Model):

    owner = models.CharField('ФИО владельца', max_length=200)
    owners_phonenumber = models.CharField('Номер владельца', max_length=20)
    owner_pure_phone = PhoneNumberField(verbose_name='Отформатированный Номер', blank=True, null=True, max_length=20)
    created_at = models.DateTimeField(
        'Когда создано объявление',
        default=timezone.now,
        db_index=True)

    description = models.TextField('Текст объявления', blank=True)
    price = models.IntegerField('Цена квартиры', db_index=True)

    town = models.CharField(
        'Город, где находится квартира',
        max_length=50,
        db_index=True)
    town_district = models.CharField(
        'Район города, где находится квартира',
        max_length=50,
        blank=True,
        help_text='Чертаново Южное')
    address = models.TextField(
        'Адрес квартиры',
        help_text='ул. Подольских курсантов д.5 кв.4')
    floor = models.CharField(
        'Этаж',
        max_length=3,
        help_text='Первый этаж, последний этаж, пятый этаж')

    rooms_number = models.IntegerField(
        'Количество комнат в квартире',
        db_index=True)
    living_area = models.IntegerField(
        'количество жилых кв.метров',
        null=True,
        blank=True,
        db_index=True)

    has_balcony = models.BooleanField('Наличие балкона', db_index=True, default=False)
    new_building = models.BooleanField(
        'Новостройка',
        db_index=True,
        max_length=5,
        null=True,
        blank=True)
    active = models.BooleanField('Активно-ли объявление', db_index=True)
    construction_year = models.IntegerField(
        'Год постройки здания',
        null=True,
        blank=True,
        db_index=True)
    liked_by = models.ManyToManyField(
        User,
        through='Like',
        related_name='liked_flats'
        )

    class Meta:
        verbose_name = "Квартира"
        verbose_name_plural = "Квартиры"

    def __str__(self):
        return f'{self.town}, {self.address} ({self.price}р.)'


class Сlaim(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    text = models.TextField(
        'Текст жалобы',
        help_text='Перечислите пожалуйста все аргументы, по которым Вы считаете свою жалобу обоснованой'
        )

    class Meta:
        verbose_name = "Жалоба"
        verbose_name_plural = "Жалобы"

    def __str__(self):
        return f'{self.flat} - {self.text}'


class Like(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, verbose_name='Квартира')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        unique_together = ('user', 'flat')
        verbose_name = "Like"
        verbose_name_plural = "Likes"


class Owner(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО владельца')
    phone = models.CharField(max_length=15, verbose_name='Телефон владельца')
    normalized_phone = PhoneNumberField(max_length=15, verbose_name='Нормализированный номер', blank=True, null=True)
    flats = models.ManyToManyField('Flat', related_name='owners', verbose_name='квартиры в собственности')

    class Meta:
        verbose_name = "Владелец"
        verbose_name_plural = "Владельцы"
        unique_together = ['full_name', 'normalized_phone']

    def __str__(self):
        return self.full_name
