from django.db import models
from django.utils.translation import get_language


def localized(original, english):
    if get_language() == 'en' and english:
        return english
    return original


class Service(models.Model):
    name = models.CharField('назва', max_length=100)
    name_en = models.CharField('назва англійською', max_length=100, blank=True)
    description = models.TextField('опис', blank=True)
    description_en = models.TextField('опис англійською', blank=True)
    price = models.DecimalField('ціна, грн', max_digits=8, decimal_places=2)
    duration_minutes = models.PositiveIntegerField('тривалість, хв')

    class Meta:
        ordering = ['name']
        verbose_name = 'послуга'
        verbose_name_plural = 'послуги'

    def __str__(self):
        return self.name

    @property
    def localized_name(self):
        return localized(self.name, self.name_en)

    @property
    def localized_description(self):
        return localized(self.description, self.description_en)


class Specialist(models.Model):
    name = models.CharField("ім'я", max_length=100)
    name_en = models.CharField("ім'я англійською", max_length=100, blank=True)
    bio = models.TextField('про майстра', blank=True)
    bio_en = models.TextField('про майстра англійською', blank=True)
    services = models.ManyToManyField(
        Service,
        related_name='specialists',
        verbose_name='послуги',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'майстер'
        verbose_name_plural = 'майстри'

    def __str__(self):
        return self.name

    @property
    def localized_name(self):
        return localized(self.name, self.name_en)

    @property
    def localized_bio(self):
        return localized(self.bio, self.bio_en)


class Appointment(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='appointments',
        verbose_name='послуга',
    )
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.PROTECT,
        related_name='appointments',
        verbose_name='майстер',
    )
    client_name = models.CharField("ім'я", max_length=100)
    client_phone = models.CharField('телефон', max_length=20)
    starts_at = models.DateTimeField('початок')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['starts_at']
        verbose_name = 'запис'
        verbose_name_plural = 'записи'

    def __str__(self):
        return f'{self.client_name} — {self.service}'
