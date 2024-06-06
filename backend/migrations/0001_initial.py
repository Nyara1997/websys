# Generated by Django 4.1.5 on 2023-11-13 13:07

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Block_Transportation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('client_name', models.CharField(max_length=200)),
                ('quantity', models.IntegerField(default=0)),
                ('amount', models.FloatField(default=0)),
                ('transportation_damages', models.IntegerField(default=0)),
                ('pub_date', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Block_Type',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('price', models.CharField(max_length=200)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance_Type',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('pub_date', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_allowed', models.BooleanField(default=False)),
                ('profile', models.FloatField(default=0)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transportation_Type',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transportation_Cost_Detail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('cost_type', models.CharField(max_length=200)),
                ('quantity', models.IntegerField(default=0)),
                ('amount', models.FloatField(default=0)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.block_transportation')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction_Type',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('quantity_Sold', models.IntegerField(default=0)),
                ('unit_price', models.FloatField(blank=True, default=0)),
                ('client_name', models.CharField(max_length=200)),
                ('discount', models.FloatField(blank=True, default=0)),
                ('amount', models.FloatField(default=0)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.block_type')),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.currency')),
                ('transaction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.transaction_type')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('production_number', models.IntegerField(default=0)),
                ('production_damages', models.IntegerField(default=0)),
                ('bags_of_cement', models.FloatField(blank=True, default=0)),
                ('unit_price', models.FloatField(blank=True, default=0)),
                ('amount', models.FloatField(default=0)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.block_type')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Piling_Damages',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('damages', models.IntegerField(default=0)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.block_type')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Particulars',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Partial_Sales',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('invoice_number', models.CharField(max_length=200)),
                ('quantity_Sold', models.IntegerField(default=0)),
                ('unit_price', models.FloatField(blank=True, default=0)),
                ('client_name', models.CharField(max_length=200)),
                ('amount_paid', models.FloatField(blank=True, default=0)),
                ('discount', models.FloatField(blank=True, default=0)),
                ('amount', models.FloatField(default=0)),
                ('balance', models.FloatField(default=0)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.block_type')),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.currency')),
                ('transaction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.transaction_type')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Other_Transportation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('quantity', models.IntegerField(default=0)),
                ('amount', models.FloatField(default=0)),
                ('description', models.TextField(max_length=500)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Complete', 'Complete')], default='Pending', max_length=100)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.currency')),
                ('transportation_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.transportation_type')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.unit')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Other_Incomes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('description', models.TextField(max_length=500)),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.FloatField(blank=True, default=0)),
                ('discount', models.FloatField(blank=True, default=0)),
                ('amount', models.FloatField(default=0)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.currency')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Other_Expenses',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('description', models.TextField(max_length=500)),
                ('quantity', models.IntegerField(default=0)),
                ('unit_price', models.FloatField(blank=True, default=0)),
                ('amount', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Complete', 'Complete')], default='Pending', max_length=100)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.currency')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.unit')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Opening_Stock',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('quantity', models.IntegerField(default=0)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.block_type')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Material_Transportation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('quantity', models.IntegerField(default=0)),
                ('amount', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Complete', 'Complete')], default='Pending', max_length=100)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.currency')),
                ('transportation_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.transportation_type')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.unit')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('quantity', models.IntegerField(default=0)),
                ('unit_price', models.FloatField(default=0)),
                ('amount', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Complete', 'Complete')], default='Pending', max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.currency')),
                ('maintenance_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.maintenance_type')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.unit')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Fixed_Cost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('fixed_cost', models.CharField(max_length=200)),
                ('quantity', models.IntegerField(default=0)),
                ('unit_price', models.FloatField(default=0)),
                ('amount', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Complete', 'Complete')], default='Pending', max_length=100)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.currency')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.unit')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Debt_Repayment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('client_name', models.CharField(max_length=200)),
                ('date_of_sale', models.DateField()),
                ('amount_due', models.FloatField(default=0)),
                ('amount_paid', models.FloatField(default=0)),
                ('balance', models.FloatField(default=0)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.currency')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cost_Type',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cost_Of_Production',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('quantity', models.IntegerField(default=0)),
                ('unit_price', models.FloatField(default=0)),
                ('discount', models.FloatField(blank=True, default=0)),
                ('amount', models.FloatField(default=0)),
                ('final_amount', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Complete', 'Complete')], default='Pending', max_length=100)),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.currency')),
                ('particulars', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.particulars')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.unit')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='block_transportation',
            name='block',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.block_type'),
        ),
        migrations.AddField(
            model_name='block_transportation',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.currency'),
        ),
        migrations.AddField(
            model_name='block_transportation',
            name='transportation_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.transportation_type'),
        ),
        migrations.AddField(
            model_name='block_transportation',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
