# Generated by Django 3.2.3 on 2024-09-03 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0007_alter_userdata_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('department', models.CharField(max_length=255)),
                ('registration', models.CharField(max_length=100)),
                ('coordinator_name', models.CharField(max_length=255)),
                ('coordinator_email', models.EmailField(max_length=254)),
                ('coordinator_department', models.CharField(max_length=255)),
                ('siape_registration', models.CharField(max_length=100)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='attachments/')),
                ('status', models.BooleanField(default=False)),
                ('dt_solicitation', models.DateTimeField(auto_now_add=True)),
                ('dt_approvement', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Access Request',
                'verbose_name_plural': 'Access Requests',
            },
        ),
        migrations.RemoveField(
            model_name='userdata',
            name='institution',
        ),
    ]