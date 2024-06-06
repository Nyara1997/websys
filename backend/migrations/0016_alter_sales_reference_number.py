# Generated by Django 5.0 on 2024-01-15 17:47

import backend.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_alter_block_transportation_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='reference_number',
            field=models.CharField(default=backend.models.Sales.generate_reference_number, editable=False, max_length=200),
        ),
    ]
