# Generated by Django 5.1.4 on 2024-12-19 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app3", "0002_publicacion_imagenpub_alter_comentario_autocom_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="datosusuario",
            name="apellido",
            field=models.CharField(blank=True, max_length=48, null=True),
        ),
        migrations.AddField(
            model_name="datosusuario",
            name="contra",
            field=models.CharField(blank=True, max_length=48, null=True),
        ),
        migrations.AddField(
            model_name="datosusuario",
            name="email",
            field=models.CharField(blank=True, max_length=48, null=True),
        ),
        migrations.AddField(
            model_name="datosusuario",
            name="nombre",
            field=models.CharField(blank=True, max_length=48, null=True),
        ),
        migrations.AddField(
            model_name="datosusuario",
            name="username",
            field=models.CharField(blank=True, max_length=48, null=True),
        ),
    ]
