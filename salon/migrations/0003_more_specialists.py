from django.db import migrations


def add_specialists(apps, schema_editor):
    Service = apps.get_model('salon', 'Service')
    Specialist = apps.get_model('salon', 'Specialist')
    manicure = Service.objects.get(name='Манікюр')
    haircut = Service.objects.get(name='Стрижка')
    color = Service.objects.get(name='Фарбування')

    people = [
        ('Софія', 'Майстер манікюру.', [manicure]),
        ('Андрій', 'Чоловічі та жіночі стрижки.', [haircut]),
        ('Катерина', 'Колорист.', [color]),
        ('Дарина', 'Стрижка і фарбування.', [haircut, color]),
    ]
    for name, bio, services in people:
        person, created = Specialist.objects.get_or_create(
            name=name,
            defaults={'bio': bio},
        )
        if created:
            person.services.set(services)


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0002_seed'),
    ]

    operations = [
        migrations.RunPython(add_specialists, migrations.RunPython.noop),
    ]
