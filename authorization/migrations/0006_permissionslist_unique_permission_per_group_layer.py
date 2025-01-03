# Generated by Django 3.2.3 on 2024-09-05 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0005_alter_permissionslist_options'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='permissionslist',
            constraint=models.UniqueConstraint(fields=('group_id', 'permission_layer_id'), name='unique_permission_per_group_layer'),
        ),
    ]
