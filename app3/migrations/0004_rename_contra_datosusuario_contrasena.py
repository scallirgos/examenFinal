# Generated by Django 5.1.4 on 2024-12-19 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app3", "0003_datosusuario_apellido_datosusuario_contra_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="datosusuario",
            old_name="contra",
            new_name="contrasena",
        ),
    ]
