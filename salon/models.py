from django.db import models


class Service(models.Model):
    name = models.CharField('назва', max_length=100)
    description = models.TextField('опис', blank=True)
    price = models.DecimalField('ціна, грн', max_digits=8, decimal_places=2)
    duration_minutes = models.PositiveIntegerField('тривалість, хв')

    class Meta:
        ordering = ['name']
        verbose_name = 'послуга'
        verbose_name_plural = 'послуги'

    def __str__(self):
        return self.name


class Specialist(models.Model):
    name = models.CharField("ім'я", max_length=100)
    bio = models.TextField('про майстра', blank=True)
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
