# Generated by Django 3.2.12 on 2023-06-04 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='op_ticket',
            name='Staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.staff'),
        ),
        migrations.AddField(
            model_name='op_ticket',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.department'),
        ),
    ]