# Generated by Django 2.2.7 on 2021-03-17 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_auto_20190926_2106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comunidad',
            name='mercado_pago',
        ),
        migrations.AddField(
            model_name='comunidad',
            name='cierre',
            field=models.DateField(blank=True, null=True),
        ),
    ]
