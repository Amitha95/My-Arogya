# Generated by Django 3.2.12 on 2023-06-04 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_casesheet_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casesheet',
            name='status',
            field=models.TextField(default='added'),
        ),
    ]
