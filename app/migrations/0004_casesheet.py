# Generated by Django 3.2.12 on 2023-06-04 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_patient_room'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseSheet',
            fields=[
                ('casesheet_id', models.AutoField(primary_key=True, serialize=False)),
                ('patient', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('symptoms', models.TextField()),
                ('diagnosis', models.TextField()),
                ('treatment', models.TextField()),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.staff')),
            ],
        ),
    ]