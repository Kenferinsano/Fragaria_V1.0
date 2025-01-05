from django.db import migrations, models
from django.db import connections

def add_nombre_field(apps, schema_editor):
    # Realiza la alteración de la tabla directamente sin transacción
    with connections['default'].cursor() as cursor:
        cursor.execute('ALTER TABLE plantacion ADD COLUMN nombre VARCHAR(100);')

class Migration(migrations.Migration):
    dependencies = [
        ('usuarios', '0001_initial'),  # Reemplaza con tu última migración
    ]

    operations = [
        migrations.RunPython(add_nombre_field),
    ]
