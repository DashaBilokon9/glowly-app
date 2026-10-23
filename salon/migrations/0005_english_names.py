from django.db import migrations, models


def fill_english(apps, schema_editor):
    Service = apps.get_model('salon', 'Service')
    Specialist = apps.get_model('salon', 'Specialist')

    services = {
        'Манікюр': ('Manicure', 'Classic manicure and polish.'),
        'Педікюр': ('Pedicure', 'Classic pedicure.'),
        'Стрижка': ('Haircut', 'Haircut and styling.'),
        'Фарбування': ('Color', 'Single-process color.'),
    }
    for service in Service.objects.all():
        english = services.get(service.name)
        if english:
            service.name_en, service.description_en = english
            service.save()

    specialists = {
        'Олена': ('Olena', 'Manicure and pedicure.'),
        'Софія': ('Sofiia', 'Manicure and pedicure.'),
        'Катерина': ('Kateryna', 'Manicure and pedicure.'),
        'Марія': ('Mariia', 'Haircut and color.'),
        'Дарина': ('Daryna', 'Haircut and color.'),
        'Андрій': ('Andrii', 'Haircut and color.'),
    }
    for specialist in Specialist.objects.all():
        english = specialists.get(specialist.name)
        if english:
            specialist.name_en, specialist.bio_en = english
            specialist.save()


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0004_split_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='name_en',
            field=models.CharField(blank=True, max_length=100, verbose_name='назва англійською'),
        ),
        migrations.AddField(
            model_name='service',
            name='description_en',
            field=models.TextField(blank=True, verbose_name='опис англійською'),
        ),
        migrations.AddField(
            model_name='specialist',
            name='name_en',
            field=models.CharField(blank=True, max_length=100, verbose_name="ім'я англійською"),
        ),
        migrations.AddField(
            model_name='specialist',
            name='bio_en',
            field=models.TextField(blank=True, verbose_name='про майстра англійською'),
        ),
        migrations.RunPython(fill_english, migrations.RunPython.noop),
    ]
