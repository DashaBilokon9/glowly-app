from django.db import migrations


def seed(apps, schema_editor):
    Service = apps.get_model('salon', 'Service')
    Specialist = apps.get_model('salon', 'Specialist')

    manicure = Service.objects.create(
        name='Манікюр',
        description='Класичний манікюр і покриття.',
        price='450.00',
        duration_minutes=60,
    )
    haircut = Service.objects.create(
        name='Стрижка',
        description='Стрижка і укладка.',
        price='500.00',
        duration_minutes=45,
    )
    color = Service.objects.create(
        name='Фарбування',
        description='Фарбування в один тон.',
        price='1200.00',
        duration_minutes=120,
    )

    olena = Specialist.objects.create(
        name='Олена',
        bio='Майстер манікюру.',
    )
    olena.services.add(manicure)

    maria = Specialist.objects.create(
        name='Марія',
        bio='Перукар.',
    )
    maria.services.add(haircut, color)


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
