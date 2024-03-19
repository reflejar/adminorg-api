# Generated by Django 2.2.7 on 2024-03-19 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('communications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='addressee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.Perfil'),
        ),
    ]
