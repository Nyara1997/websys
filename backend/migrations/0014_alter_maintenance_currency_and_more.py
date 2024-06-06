# Generated by Django 5.0 on 2024-01-12 19:12

import backend.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_maintenance_type_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenance',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('SSP', 'SSP')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cost_of_production',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('SSP', 'SSP')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='other_transportation',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('SSP', 'SSP')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='other_expenses',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('SSP', 'SSP')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='other_incomes',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('SSP', 'SSP')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sales',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('SSP', 'SSP')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='fixed_cost',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('SSP', 'SSP')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='material_transportation',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('SSP', 'SSP')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='debt_repayment',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('SSP', 'SSP')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='block_transportation',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('SSP', 'SSP')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='partial_sales',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('SSP', 'SSP')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='block_transportation',
            name='reference_number',
            field=models.CharField(default=backend.models.Block_Transportation.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='cost_of_production',
            name='reference_number',
            field=models.CharField(default=backend.models.Cost_Of_Production.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='cost_type',
            name='reference_number',
            field=models.CharField(default=backend.models.Cost_Type.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='debt_repayment',
            name='reference_number',
            field=models.CharField(default=backend.models.Debt_Repayment.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='fixed_cost',
            name='reference_number',
            field=models.CharField(default=backend.models.Fixed_Cost.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='reference_number',
            field=models.CharField(default=backend.models.Maintenance.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='maintenance_type',
            name='reference_number',
            field=models.CharField(default=backend.models.Maintenance_Type.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='material_transportation',
            name='reference_number',
            field=models.CharField(default=backend.models.Material_Transportation.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='opening_stock',
            name='reference_number',
            field=models.CharField(default=backend.models.Opening_Stock.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='other_expenses',
            name='reference_number',
            field=models.CharField(default=backend.models.Other_Expenses.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='other_incomes',
            name='reference_number',
            field=models.CharField(default=backend.models.Other_Incomes.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='other_transportation',
            name='reference_number',
            field=models.CharField(default=backend.models.Other_Transportation.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='partial_sales',
            name='reference_number',
            field=models.CharField(default=backend.models.Partial_Sales.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='particulars',
            name='reference_number',
            field=models.CharField(default=backend.models.Particulars.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='piling_damages',
            name='reference_number',
            field=models.CharField(default=backend.models.Piling_Damages.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='production',
            name='reference_number',
            field=models.CharField(default=backend.models.Production.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='transaction_type',
            name='reference_number',
            field=models.CharField(default=backend.models.Transaction_Type.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='transportation_cost_detail',
            name='reference_number',
            field=models.CharField(default=backend.models.Transportation_Cost_Detail.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='transportation_type',
            name='reference_number',
            field=models.CharField(default=backend.models.Transportation_Type.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.AlterField(
            model_name='unit',
            name='reference_number',
            field=models.CharField(default=backend.models.Unit.generate_reference_number, editable=False, max_length=200),
        ),
        migrations.DeleteModel(
            name='Currency',
        ),
    ]
