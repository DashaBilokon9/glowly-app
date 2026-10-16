from django.db import migrations


def split_staff(apps, schema_editor):
    Service = apps.get_model('salon', 'Service')
    Specialist = apps.get_model('salon', 'Specialist')

    manicure = Service.objects.get(name='Манікюр')
    haircut = Service.objects.get(name='Стрижка')
    color = Service.objects.get(name='Фарбування')
    pedicure, _created = Service.objects.get_or_create(
        name='Педікюр',
        defaults={
            'description': 'Класичний педікюр.',
            'price': '500.00',
            'duration_minutes': 75,
        },
    )

    nails = [manicure, pedicure]
    hair = [haircut, color]
    groups = {
        'Олена': ('Манікюр і педікюр.', nails),
        'Софія': ('Манікюр і педікюр.', nails),
        'Катерина': ('Манікюр і педікюр.', nails),
        'Марія': ('Стрижка і фарбування.', hair),
        'Дарина': ('Стрижка і фарбування.', hair),
        'Андрій': ('Стрижка і фарбування.', hair),
    }
    for name, (bio, services) in groups.items():
        person = Specialist.objects.get(name=name)
        person.bio = bio
        person.save()
        person.services.set(services)


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0003_more_specialists'),
    ]

    operations = [
        migrations.RunPython(split_staff, migrations.RunPython.noop),
    ]
