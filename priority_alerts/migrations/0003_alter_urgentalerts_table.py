# Generated by Django 3.2.3 on 2022-06-10 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('priority_alerts', '0002_alter_urgentalerts_options'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='urgentalerts',
            table='funai"."vw_img_alerta_urgente_consolidado_a',
        ),
    ]