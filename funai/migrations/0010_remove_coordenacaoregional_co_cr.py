# Generated by Django 3.2.3 on 2022-01-03 23:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funai', '0009_auto_20220103_2244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coordenacaoregional',
            name='co_cr',
        ),
    ]