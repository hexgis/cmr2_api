# Generated by Django 3.2.3 on 2022-04-05 23:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='monitoringconsolidated',
            options={'ordering': ('-dt_t_um',), 'verbose_name': 'Monitoring Consolidated', 'verbose_name_plural': 'Monitorings Consolidated'},
        ),
    ]
