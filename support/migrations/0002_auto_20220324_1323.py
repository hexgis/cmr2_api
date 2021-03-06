# Generated by Django 3.2.3 on 2022-03-24 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0001_initial'),
    ]

    def insertData(apps, schema_editor):
        CategoryLayersGroup = apps.get_model('support', 'CategoryLayersGroup')
        category = CategoryLayersGroup(id=1)
        category.save()

    operations = [
        migrations.CreateModel(
            name='CategoryLayersGroup',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, null=True, unique=True)),
                ('icon', models.CharField(blank=True, default='layers',
                 max_length=255, null=True, verbose_name='Icon')),
                ('description', models.CharField(
                    blank=True, max_length=1024, null=True)),
            ],
            options={
                'verbose_name': 'Category Groups Layers',
                'verbose_name_plural': 'Categorys Groups Layers',
                'ordering': ['name'],
            },
        ),
        migrations.RunPython(insertData),
        migrations.RemoveField(
            model_name='layersgroup',
            name='icon',
        ),
        migrations.AddField(
            model_name='layersgroup',
            name='category_groups',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING,
                                    related_name='category', to='support.categorylayersgroup'),
        ),
    ]
