# Generated by Django 3.2.3 on 2022-01-11 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('priority_monitoring', '0006_auto_20220111_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='priorityconsolidated',
            name='flag',
            field=models.BooleanField(default=False, verbose_name='Flag'),
        ),
    ]