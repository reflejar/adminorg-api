# Generated by Django 2.2.7 on 2024-02-27 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operative', '0006_auto_20220727_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='operacion',
            name='concepto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='conceptos', to='operative.Cuenta'),
        ),
    ]