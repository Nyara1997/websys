from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import date
import uuid
from django.contrib.auth.models import AbstractBaseUser
from django.utils.crypto import get_random_string
import random
import string




# Create your models here.
class UserAccount(models.Model):
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	is_staff    = models.BooleanField(default=False)
	is_admin    = models.BooleanField(default=False)
	is_allowed 	= models.BooleanField(default=False)
	profile     = models.FloatField(default=0, blank=False )
	pub_date 	= models.DateField(default=date.today)


class Particulars(models.Model):

	def generate_reference_number():
		prefix = 'P'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'


	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	name 				= models.CharField(max_length=200, blank=False)
	pub_date 			= models.DateField(default=date.today)

	def __str__(self):
		return self.name

class Unit(models.Model):
	def generate_reference_number():
		prefix = 'U'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'

	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	name 				= models.CharField(max_length=200, blank=False)
	pub_date 			= models.DateField(default=date.today)

	def __str__(self):
		return self.name


class Cost_Of_Production(models.Model):

	STATUS = (
	    ('Pending', 'Pending'),
	    ('Processing', 'Processing'),
	    ('Complete', 'Complete'),  
	 )

	CURRENCY = (
	    ('USD', 'USD'),
	    ('SSP', 'SSP'),
	 )

	def generate_reference_number():
		prefix = 'COP'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'

	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=False, null=True)
	particulars 		= models.ForeignKey(Particulars, on_delete=models.SET_NULL, null=True)
	quantity 			= models.IntegerField(default=0, blank=False )
	unit 				= models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
	currency 			= models.CharField(choices=CURRENCY, default='SSP', max_length=200, null=True)
	unit_price 			= models.FloatField(default=0, blank=False )
	discount 			= models.FloatField(default=0, blank=True )
	amount 				= models.FloatField(default=0, blank=False )
	final_amount 		= models.FloatField(default=0, blank=False )
	status				= models.CharField(choices=STATUS, default='Pending', max_length=100)
	pub_date 			= models.DateField(default=date.today)


class Maintenance_Type(models.Model):

	def generate_reference_number():
		prefix = 'MT'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'

	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	name 				= models.CharField(max_length=200, blank=False)
	pub_date 			= models.DateField(default=date.today)

	def __str__(self):
		return self.name


class Maintenance(models.Model):
	
	STATUS = (
	    ('Pending', 'Pending'),
	    ('Processing', 'Processing'),
	    ('Complete', 'Complete'),    
	 )

	CURRENCY = (
	    ('USD', 'USD'),
	    ('SSP', 'SSP'),
	)

	def generate_reference_number():
		prefix = 'M'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'

	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	maintenance_type 	= models.ForeignKey(Maintenance_Type, on_delete=models.SET_NULL, null=True)
	amount 				= models.FloatField(default=0, blank=False )
	currency 			= models.CharField(choices=CURRENCY, default='SSP', max_length=200, null=True)
	status			    = models.CharField(choices=STATUS, default='Pending', max_length=100)
	description 		= models.TextField(max_length=500, blank=False )
	pub_date 			= models.DateField(default=date.today)


class Maintenance_Expense_List(models.Model):

	CURRENCY = (
	    ('USD', 'USD'),
	    ('SSP', 'SSP'),
	)

	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	sub_maintenance     = models.ForeignKey(Maintenance, on_delete=models.SET_NULL, null=True)
	description 		= models.CharField(max_length=200, blank=False)
	quantity 			= models.IntegerField(default=0, blank=False )
	unit_price 			= models.FloatField(default=0, blank=False )
	discount 			= models.FloatField(default=0, blank=True )
	amount 				= models.FloatField(default=0, blank=False )
	currency 			= models.CharField(choices=CURRENCY, default='SSP', max_length=200, null=True)
	pub_date 			= models.DateField(default=date.today)


class Fixed_Cost(models.Model):

	STATUS = (
	    ('Pending', 'Pending'),
	    ('Processing', 'Processing'),
	    ('Complete', 'Complete'),    
	 )

	CURRENCY = (
	    ('USD', 'USD'),
	    ('SSP', 'SSP'),
	 
	 )

	def generate_reference_number():
		prefix = 'FC'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'

	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	fixed_cost 			= models.CharField(max_length=200, blank=False)
	quantity 			= models.IntegerField(default=0, blank=False )
	unit 				= models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
	currency 			= models.CharField(choices=CURRENCY, default='SSP', max_length=200, null=True)
	unit_price 			= models.FloatField(default=0, blank=False )
	amount 				= models.FloatField(default=0, blank=False )
	status			    = models.CharField(choices=STATUS, default='Pending', max_length=100)
	pub_date 			= models.DateField(default=date.today)

class Transportation_Type(models.Model):

	def generate_reference_number():
		prefix = 'TT'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'

	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	name 				= models.CharField(max_length=200, blank=False)
	pub_date 			= models.DateField(default=date.today)

	def __str__(self):
		return self.name

class Block_Type(models.Model):

	def generate_reference_number():
		prefix = 'BT'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'

	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	reference_number 	= models.CharField(max_length=10, blank=False, editable=False)
	name 				= models.CharField(max_length=200, blank=False)
	price 		        = models.CharField(max_length=200, blank=False)
	pub_date 			= models.DateField(default=date.today)

	def __str__(self):
		return self.name

class Cost_Type(models.Model):

	def generate_reference_number():
		prefix = 'CT'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'


	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	name 				= models.CharField(max_length=200, blank=False)
	pub_date 			= models.DateField(default=date.today)

	def __str__(self):
		return self.name

class Block_Transportation(models.Model):

	def generate_reference_number():
		prefix = 'BT'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'

	CURRENCY = (
	    ('USD', 'USD'),
	    ('SSP', 'SSP'),
	)


	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	client_name 		= models.CharField(max_length=200, blank=False)
	transportation_type = models.ForeignKey(Transportation_Type, on_delete=models.SET_NULL,null=True)
	block 				= models.ForeignKey(Block_Type, on_delete=models.SET_NULL, null=True)
	currency 			= models.CharField(choices=CURRENCY, default='SSP', max_length=200, null=True)
	quantity 			= models.IntegerField(default=0, blank=False )
	amount 					= models.FloatField(default=0, blank=False )
	transportation_damages 	= models.IntegerField(default=0, blank=False )
	pub_date 				= models.DateField(default=date.today)


class Material_Transportation(models.Model):
	
	STATUS = (
	    ('Pending', 'Pending'),
	    ('Processing', 'Processing'),
	    ('Complete', 'Complete'),    
	 )

	def generate_reference_number():
		prefix = 'MT'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'


	CURRENCY = (
	    ('USD', 'USD'),
	    ('SSP', 'SSP'),
	)


	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	transportation_type = models.ForeignKey(Transportation_Type, on_delete=models.SET_NULL,null=True)
	currency 			= models.CharField(choices=CURRENCY, default='SSP', max_length=200, null=True)
	unit 				= models.ForeignKey(Unit, on_delete=models.SET_NULL,null=True)
	quantity 			= models.IntegerField(default=0, blank=False )
	amount 				= models.FloatField(default=0, blank=False )
	status			    = models.CharField(choices=STATUS, default='Pending', max_length=100)
	pub_date 			= models.DateField(default=date.today)

class Other_Transportation(models.Model):

	STATUS = (
	    ('Pending', 'Pending'),
	    ('Processing', 'Processing'),
	    ('Complete', 'Complete'),    
	 )

	def generate_reference_number():
		prefix = 'OT'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'


	CURRENCY = (
	    ('USD', 'USD'),
	    ('SSP', 'SSP'),
	)

	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	transportation_type = models.ForeignKey(Transportation_Type, on_delete=models.SET_NULL,null=True)
	quantity 			= models.IntegerField(default=0, blank=False )
	unit 				= models.ForeignKey(Unit, on_delete=models.SET_NULL,null=True)
	currency 			= models.CharField(choices=CURRENCY, default='SSP', max_length=200, null=True)
	amount 				= models.FloatField(default=0, blank=False )
	description 		= models.TextField(max_length=500, blank=False )
	status			    = models.CharField(choices=STATUS, default='Pending', max_length=100)
	pub_date 			= models.DateField(default=date.today)

class Other_Expenses(models.Model):
	
	STATUS = (
	    ('Pending', 'Pending'),
	    ('Processing', 'Processing'),
	    ('Complete', 'Complete'),    
	 )

	CURRENCY = (
	    ('USD', 'USD'),
	    ('SSP', 'SSP'),
	)

	def generate_reference_number():
		prefix = 'OE'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'

	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	description 		= models.TextField(max_length=500, blank=False )
	quantity 			= models.IntegerField(default=0, blank=False )
	unit 				= models.ForeignKey(Unit, on_delete=models.SET_NULL,null=True)
	unit_price 			= models.FloatField(default=0, blank=True )
	amount 				= models.FloatField(default=0, blank=False )
	currency 			= models.CharField(choices=CURRENCY, default='SSP', max_length=200, null=True)
	status			    = models.CharField(choices=STATUS, default='Pending', max_length=100)
	pub_date 			= models.DateField(default=date.today)


class Transportation_Cost_Detail(models.Model):

	def generate_reference_number():
		prefix = 'TCD'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'


	id 				= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	block        		= models.ForeignKey(Block_Transportation, on_delete=models.SET_NULL, null=True)
	cost_type 		= models.CharField(max_length=200, blank=False)
	quantity 		= models.IntegerField(default=0, blank=False )
	amount 			= models.FloatField(default=0, blank=False )
	pub_date 		= models.DateField(default=date.today)

	def get_cost_id(self):
		return self.id


class Transaction_Type(models.Model):

	def generate_reference_number():
		prefix = 'TT'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'

	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	name 				= models.CharField(max_length=200, blank=False)
	pub_date 			= models.DateField(default=date.today)

	def __str__(self):
		return self.name

class Sales(models.Model):

	def generate_reference_number():
		prefix = 'S'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'

	CURRENCY = (
	    ('USD', 'USD'),
	    ('SSP', 'SSP'),
	)

	Transaction_type = (
	    ('Cash', 'Cash'),
	    ('Credit', 'Credit'),
	    ('Partial', 'Partial'),
	 )

	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	transaction 		= models.ForeignKey(Transaction_Type, on_delete=models.SET_NULL, null=True)
	block 				= models.ForeignKey(Block_Type, on_delete=models.SET_NULL, null=True)
	quantity_Sold 		= models.IntegerField(default=0, blank=False )
	unit_price 			= models.FloatField(default=0, blank=True )
	currency 			= models.CharField(choices=CURRENCY, default='SSP', max_length=200, null=True)
	client_name 		= models.CharField(max_length=200, blank=False)
	discount 			= models.FloatField(default=0, blank=True )
	amount 				= models.FloatField(default=0, blank=False )
	pub_date 			= models.DateField(default=date.today)

class Partial_Sales(models.Model):

	def generate_reference_number():
		prefix = 'PS'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'

	CURRENCY = (
	    ('USD', 'USD'),
	    ('SSP', 'SSP'),
	)

	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	invoice_number 		= models.CharField(max_length=200, blank=False)
	transaction 		= models.ForeignKey(Transaction_Type, on_delete=models.SET_NULL, null=True)
	block 				= models.ForeignKey(Block_Type, on_delete=models.CASCADE)
	quantity_Sold 		= models.IntegerField(default=0, blank=False )
	unit_price 			= models.FloatField(default=0, blank=True )
	currency 			= models.CharField(choices=CURRENCY, default='SSP', max_length=200, null=True)
	client_name 		= models.CharField(max_length=200, blank=False)
	amount_paid 		= models.FloatField(default=0, blank=True )
	discount 			= models.FloatField(default=0, blank=True )
	amount 				= models.FloatField(default=0, blank=False )
	balance 			= models.FloatField(default=0, blank=False )
	pub_date 			= models.DateField(default=date.today)


	# def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
	# 	if not self.invoice_number and self.pk is None:
	# 		last_invoice = Partial_Sales.objects.all().order_by("-pk").first()
	# 		last_pk = 0

	# 		if last_invoice:
	# 			last_pk = last_invoice.pk 

	# 		self.invoice_number = "INV-" + str(last_pk+1).zfill(3)

	# 	super(Partial_Sales, self).save(force_insert, force_update, using, update_fields)


class Debt_Repayment(models.Model):

	def generate_reference_number():
		prefix = 'DRM'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'

	CURRENCY = (
	    ('USD', 'USD'),
	    ('SSP', 'SSP'),
	)

	id 				= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	client_name 		= models.CharField(max_length=200, blank=False)
	date_of_sale 		= models.DateField()
	amount_due 		= models.FloatField(default=0, blank=False )
	amount_paid 	= models.FloatField(default=0, blank=False )
	balance 		= models.FloatField(default=0, blank=False )
	currency 		= models.CharField(choices=CURRENCY, default='SSP', max_length=200, null=True)

class Other_Incomes(models.Model):

	def generate_reference_number():
		prefix = 'OI'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'

	CURRENCY = (
	    ('USD', 'USD'),
	    ('SSP', 'SSP'),
	)

	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	description 	= models.TextField(max_length=500, blank=False )
	quantity 		= models.IntegerField(default=0, blank=False )
	price 			= models.FloatField(default=0, blank=True )
	currency 		= models.CharField(choices=CURRENCY, default='SSP', max_length=200, null=True)
	discount 		= models.FloatField(default=0, blank=True )
	amount 			= models.FloatField(default=0, blank=False )
	pub_date 		= models.DateField(default=date.today)


class Production(models.Model):

	def generate_reference_number():
		prefix = 'PD'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'


	id 					= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	block 				= models.ForeignKey(Block_Type, on_delete=models.CASCADE)
	production_number 	= models.IntegerField(default=0, blank=False )
	production_damages 	= models.IntegerField(default=0, blank=False )
	bags_of_cement		= models.FloatField(default=0, blank=True )
	unit_price			= models.FloatField(default=0, blank=True )
	amount 				= models.FloatField(default=0, blank=False )
	pub_date 			= models.DateField(default=date.today)

	def __str__(self):
		return self.block.name

class Piling_Damages(models.Model):

	def generate_reference_number():
		prefix = 'PD'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'

	id 				= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	block 				= models.ForeignKey(Block_Type, on_delete=models.SET_NULL, null=True)
	damages 			= models.IntegerField(default=0, blank=False )
	pub_date 			= models.DateField(default=date.today)

class Opening_Stock(models.Model):

	def generate_reference_number():
		prefix = 'OS'
		unique_digits = ''.join(random.sample(string.digits, k=6))

		return f'{prefix}-{unique_digits}'

	id 				= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False)
	reference_number 	= models.CharField(max_length=200, default=generate_reference_number, blank=False, editable=False)
	block 				= models.ForeignKey(Block_Type, on_delete=models.SET_NULL, null=True)
	quantity 			= models.IntegerField(default=0, blank=False )
	pub_date 			= models.DateField(default=date.today) 
