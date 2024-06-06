from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings

from django.contrib.auth.forms import User
from .forms import createUser_Form

from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from django.views import View
from .decorators import unauthenicated_user, allowed_users

from django.db.models import Sum, Count
from datetime import datetime, timedelta

from django.db.models import F, ExpressionWrapper
import random
import string

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt



# Create your views here.


@login_required(login_url='login')
def home(request):
	production 	= Production.objects.all()
	sale       	= Sales.objects.all()
	partial_sale 		= Partial_Sales.objects.all()
	debt_repayment 		= Debt_Repayment.objects.all()
	other_income   		= Other_Incomes.objects.all()
	cost_of_production 	= Cost_Of_Production.objects.all()
	maintenance         = Maintenance.objects.all()
	block_transportation 		= Block_Transportation.objects.all()
	material_transportation 	= Material_Transportation.objects.all()
	other_transportation 		= Other_Transportation.objects.all()
	other_expenses              = Other_Expenses.objects.all()
	fixed_cost              	= Fixed_Cost.objects.all()

	# Revenue 
	get_sale_total = 0
	for i in Sales.objects.all():
		get_sale_total += i.amount

	get_partial_sale_total = 0
	for i in Partial_Sales.objects.all():
		get_partial_sale_total += i.amount

	get_debt_total = 0
	for i in Debt_Repayment.objects.all():
		get_debt_total += i.amount_due

	get_other_income_total = 0
	for i in Other_Incomes.objects.all():
		get_other_income_total += i.amount

	get_total_revenue = get_sale_total + get_partial_sale_total + get_debt_total + get_other_income_total 

	# Sale
	sale_total = get_sale_total + get_partial_sale_total


	# Production
	get_total_production = 0

	for i in production:
		if i.amount:
			#get_total_production = i.amount + get_total_production
			get_total_production += i.amount
			#print('>>>>>', get_total_production)
		

	# General Expenses

	cost_of_production_total = 0
	for i in cost_of_production:
		cost_of_production_total += i.amount

	maintenance_total = 0
	for i in maintenance:
		maintenance_total += i.amount

	block_transportation_total = 0
	for i in block_transportation:
		block_transportation_total += i.amount

	material_transportation_total = 0
	for i in material_transportation:
		material_transportation_total += i.amount

	other_transportation_total = 0
	for i in other_transportation:
		other_transportation_total += i.amount

	other_expenses_total = 0
	for i in other_expenses:
		other_expenses_total += i.amount

	fixed_cost_total = 0
	for i in fixed_cost:
		fixed_cost_total += i.amount

	# General Expenses Total
	get_general_expense_total = cost_of_production_total + maintenance_total + block_transportation_total + material_transportation_total + other_transportation_total + other_expenses_total + fixed_cost_total


	context = {
		'production' : production,
		'get_total_production' : get_total_production,
		'get_total_revenue' : get_total_revenue,
		'get_other_income_total' : get_other_income_total,
		'get_debt_total' : get_debt_total,
		'sale_total' : sale_total,
		'general_expense_total' : get_general_expense_total,
	}

	return render(request,'backend/index.html', context)


def autocomplete_view(request):
	query = request.GET.get('query', '')
    
	# Query the database for products that match the user input
	suggestions = list(Block_Type.objects.filter(name__icontains=query).values('name'))

	return JsonResponse({'suggestions': suggestions})


@login_required(login_url='login')
def user_register(request):

	form = createUser_Form()
	if request.method == 'POST':
		form = createUser_Form(request.POST)

		if form.is_valid():
			form.save()

			messages.success(request, 'Account was created!!')

		elif not form.is_valid():
			messages.success(request, 'Account was not created!!')

	context = {'form':form}
	return render(request,'backend/register_user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def user_lists(request):
	get_user = User.objects.all()

	context = {
		'get_user' : get_user,
	}
	return render(request,'backend/user_lists.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def user_reset_password(request):
	context = {}
	return render(request, 'backend/reset_password.html', context)

def login_user(request):

	if request.user.is_authenticated:
		return redirect('home')

	else :
		if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)

				return redirect('home')
			else:
				messages.info(request, 'Username or Password is Incorrect ')
				return redirect('login')

	context = {}
	return render(request, 'backend/login.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


#Opens up page as PDF
def ViewPDF(request, pk):
	data = Maintenance.objects.get(id=pk)
	context = {
		'data' : data,
	}

	pdf = render_to_pdf('backend/pdf_template.html', context)
	return HttpResponse(pdf, content_type='application/pdf')



@login_required
def cost_of_production(request):

	if request.user.is_authenticated:
		get_cost_of_production = Cost_Of_Production.objects.all()

		get__count = get_cost_of_production.count()

		cost_production_weekly_expenese_SSP = 0
		cost_production_weekly_expenese_USD = 0


		for i in get_cost_of_production:

			if i.amount and i.currency:

				if i.currency == "SSP":
					cost_production_weekly_expenese_SSP += i.amount - i.discount

				if i.currency == "USD":
					cost_production_weekly_expenese_USD += i.amount - i.discount

				if  i.currency == None:
					cost_production_weekly_expenese_SSP = 0
					cost_production_weekly_expenese_USD = 0

	else:	
		return redirect("login")

	context = {
		'get_cost_of_production' 			  : get_cost_of_production,
		'cost_production_weekly_expenese_SSP' : cost_production_weekly_expenese_SSP,
		'cost_production_weekly_expenese_USD' : cost_production_weekly_expenese_USD,
		'get__count' 						  : get__count,
	}

	return render(request, 'backend/cost_of_production/cost_of_production_table.html', context)



@login_required
def cost_of_production_status(request, pk):

	if request.user.is_authenticated:
		get_cost_of_production 	    = Cost_Of_Production.objects.get(id=pk)
		all_cost_of_production 	    = Cost_Of_Production.objects.all()
		get_particulars 			= Particulars.objects.all()
		get_units 					= Unit.objects.all()
		currency                   = Cost_Of_Production.CURRENCY

		if request.method == 'POST':

			if request.POST.get('add_particular'):
				particular = request.POST['add_particular']
				Particulars.objects.create(name=particular, user=request.user)

				return redirect('edit_cost_production', pk=get_cost_of_production.id)


			elif request.POST.get('add_units'):
				gt_unit = request.POST['add_units']
				Unit.objects.create(name=gt_unit, user=request.user)

				return redirect('edit_cost_production', pk=get_cost_of_production.id)

			
			elif request.POST['particulars'] or request.POST['quantity'] or request.POST['unit'] or request.POST['currency'] or request.POST['unit_price'] or request.POST['discount'] or request.POST['status'] or request.POST['reference_number']: 
				particular 			= request.POST.get('particulars')
				quantity 			= request.POST.get('quantity')
				unit 				= request.POST.get('unit')
				currency 			= request.POST.get('currency')
				unit_price			= request.POST.get('unit_price')
				discount 			= request.POST.get('discount')
				status          	= request.POST.get('status')
				reference_number 	= request.POST.get('reference_number')

				particular_id 	= Particulars.objects.get(id=particular)
				unit_id 		= Unit.objects.get(id=unit)
				amount 			= int(quantity) * float(unit_price)
				final_amount 	= float(amount) - float(discount) 	

				# saving the data to the database 
				get_cost_of_production.particulars 		= particular_id
				get_cost_of_production.quantity    		= quantity
				get_cost_of_production.unit        		= unit_id
				get_cost_of_production.currency    		= currency
				get_cost_of_production.unit_price  		= unit_price
				get_cost_of_production.discount    		= discount
				get_cost_of_production.amount      		= amount
				get_cost_of_production.final_amount  	= final_amount
				get_cost_of_production.status = status
				get_cost_of_production.reference_number = reference_number
				get_cost_of_production.save()


				messages.success(request, f'item status updated successfuly')
				return redirect('cost_production')

	else:
		return redirect('login')

	context = {
		'cost_of_production' : get_cost_of_production,
		'get_units' 	: get_units,
		'get_particulars' : get_particulars,
		'all_cost_of_production' : all_cost_of_production,
		'currency':currency, 
	}

	return render(request, 'backend/cost_of_production/cost_of_production_status.html', context)



@login_required
def add_cost_of_production(request):

	if request.user.is_authenticated:
		get_particulars 	= Particulars.objects.all()
		get_units 			= Unit.objects.all()
		get_cost_of_production 	   = Cost_Of_Production.objects.all()
		currency                   = Cost_Of_Production.CURRENCY

		if request.method == 'POST':

			if request.POST.get('add_particular'):
				particular = request.POST['add_particular']
				Particulars.objects.create(name=particular, user=request.user)

				return redirect('add_cost_production')

			elif request.POST.get('add_units'):
				gt_unit = request.POST['add_units']
				Unit.objects.create(name=gt_unit, user=request.user)

				return redirect('add_cost_production')

			else:

				try:

					for i in range(int(request.POST.get('formset-TOTAL_FORMS', 0))):
						particular 	= request.POST.get(f'formset-{i}-particulars')
						quantity    = request.POST.get(f'formset-{i}-quantity')
						unit      	= request.POST.get(f'formset-{i}-unit')
						currency 	= request.POST.get(f'formset-{i}-currency')
						unit_price 	= request.POST.get(f'formset-{i}-unit_price')
						discount 	= request.POST.get(f'formset-{i}-discount')

						if i == 0 and not (particular and quantity and unit and currency and unit_price and discount):
							messages.error(request, f'please fill in all required fields')
							return redirect('add_cost_production')

						elif i == 0 or i > 0 and (particular and quantity and unit and currency and unit_price and discount):
						
							particular_id 	= Particulars.objects.get(id=particular)
							unit_id 		= Unit.objects.get(id=unit)
							amount 			= int(quantity) * int(unit_price)
							final_amount 	= float(amount) - float(discount)

							Cost_Of_Production.objects.create(user=request.user,particulars=particular_id, quantity=quantity,unit=unit_id,
							currency=currency,unit_price=unit_price,discount=discount,amount=amount,final_amount=final_amount)
						
					messages.success(request, f'item submitted successfuly')
					return redirect('cost_production') 
						
			
				except Exception as e:
					messages.error(request, f'{str(e)}')
					return redirect('add_cost_production')

	else:	
		return redirect("login")

	context = {
		'get_particulars' : get_particulars,
		'get_units' : get_units,
		'cost_of_production' : get_cost_of_production,
		'currency':currency,
	}

	return render(request, 'backend/cost_of_production/add_cost_of_production.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['staff','admin'])
def edit_cost_of_production(request, pk):

	if request.user.is_authenticated:
		get_cost_of_production 	    = Cost_Of_Production.objects.get(id=pk)
		get_particulars 			= Particulars.objects.all()
		get_units 					= Unit.objects.all()
		currency                   = Cost_Of_Production.CURRENCY


		if request.method == 'POST':

			if request.POST.get('add_particular'):
				particular = request.POST['add_particular']
				Particulars.objects.create(name=particular, user=request.user)

				return redirect('edit_cost_production', pk=get_cost_of_production.id)


			elif request.POST.get('add_units'):
				gt_unit = request.POST['add_units']
				Unit.objects.create(name=gt_unit, user=request.user)

				return redirect('edit_cost_production', pk=get_cost_of_production.id)

			elif request.POST['particulars'] or request.POST['quantity'] or request.POST['unit'] or request.POST['currency'] or request.POST['unit_price'] or request.POST['discount'] : 
				
				particular 		= request.POST.get('particulars')
				quantity 		= request.POST.get('quantity')
				unit 			= request.POST.get('unit')
				currency 		= request.POST.get('currency')
				unit_price		= request.POST.get('unit_price')
				discount 		= request.POST.get('discount')


				particular_id 	= Particulars.objects.get(id=particular)
				unit_id 		= Unit.objects.get(id=unit)
				amount 			= int(quantity) * float(unit_price)
				final_amount 	= float(amount) - float(discount)


				# saving the data to the database 
				get_cost_of_production.particulars 		= particular_id
				get_cost_of_production.quantity    		= quantity
				get_cost_of_production.unit        		= unit_id
				get_cost_of_production.currency    		= currency
				get_cost_of_production.unit_price  		= unit_price
				get_cost_of_production.discount    		= discount
				get_cost_of_production.amount      		= amount
				get_cost_of_production.final_amount  	= final_amount
				get_cost_of_production.save()

				messages.success(request, f'item edited successfuly')
				return redirect('cost_production')

	else:
		return redirect('login')

	context = {
		'cost_of_production' : get_cost_of_production,
		'get_units' 	: get_units,
		'get_particulars' : get_particulars,
		'currency':currency, 
	}

	return render(request, 'backend/cost_of_production/edit_cost_of_production.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_cost_of_production(request, pk):

	if request.method == 'POST':
		cost_of_production_id = Cost_Of_Production.objects.get(id=pk)
		cost_of_production_id.delete()

		messages.success(request, f'item deleted successfuly')
		return redirect('cost_production')

	else:
		return redirect('login')

	context = {
		'cost_of_production_id' : cost_of_production_id,
	}
	
	return render(request, 'backend/cost_of_production/delete_cost_of_production.html', context)


def cost_of_production_report(request):


	get_cost_of_production = Cost_Of_Production.objects.all()

	# Weekly Data ....................................................................

	fixed_labels = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

	end_date 	= datetime.now()
	start_date 	= end_date - timedelta(days=end_date.weekday())  
	data 		= Cost_Of_Production.objects.filter(pub_date__range=[start_date, end_date]).values('pub_date') \
				.annotate(total_value=Sum('final_amount'))


	formatted_data  = [{'day': entry['pub_date'].strftime('%A'), 'value': entry['total_value']} for entry in data]

	values_dict = {entry['day']: entry['value'] for entry in formatted_data}
	values = [values_dict.get(label, 0) for label in fixed_labels]

	# print('>>>>>>>> Start Date - Past Week <<<<<<<<<', start_date)
	# print('>>>>>>>> End Date - Past Week <<<<<<<<<', end_date)


	# Monthly Data .................................................................
	
	month_end_date 	 = datetime.now()
	month_start_date = end_date.replace(day=1)  # Start of the current month

	month_data = Cost_Of_Production.objects.filter(pub_date__range=[month_start_date, month_end_date]) \
					.values('pub_date') \
					.annotate(total_value=Sum('final_amount'))

	month_labels = [entry['pub_date'].strftime('%b-%d') for entry in month_data]
	month_values = [entry['total_value'] for entry in month_data]


	# Yearly Data .................................................................
	
	year_labels = ['January','February','March','April','May','June','July','August','September','October','November','December']

	year_end_date = datetime.now()
	year_start_date = year_end_date.replace(month=1, day=1)  # Start of the current year


	year_data = Cost_Of_Production.objects.filter(pub_date__range=[year_start_date, year_end_date]).values('pub_date') \
				.annotate(total_value=Sum('final_amount'))

	formatted_data  = [{'year': entry['pub_date'].strftime('%B'), 'value': entry['total_value']} for entry in year_data]
	
	values_dict = {entry['year']: entry['value'] for entry in formatted_data}
	y_values = [values_dict.get(label, 0) for label in year_labels]

	# print('>>>>>>>> Start Date - <<<<<<<<<', year_start_date)
	# print('>>>>>>>> End Date -  <<<<<<<<<', year_end_date)


	context = {
		'get_cost_of_production' : get_cost_of_production,

		'labels' : fixed_labels,
		'values' : values,

		'year_labels':year_labels,
		'year_values':y_values,

		'month_labels' : month_labels,
		'month_values' : month_values,

	}

	return render(request, 'backend/cost_of_production/cost_of_production_report.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def cost_of_production_report_usd(request):
	get_cost_of_production_usd = Cost_Of_Production.objects.all()

	context = {
		'get_cost_of_production_usd' : get_cost_of_production_usd,
	}
	return render(request, 'backend/cost_of_production/cost_of_production_report_usd.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def cost_of_production_report_ssp(request):
	get_cost_of_production_ssp = Cost_Of_Production.objects.all()

	context = {
		'get_cost_of_production_ssp' : get_cost_of_production_ssp,
	}
	return render(request, 'backend/cost_of_production/cost_of_production_report_ssp.html', context)


@login_required(login_url='login')
def maintenance(request):
	get_maintenance = Maintenance.objects.all()
	
	maintenance_routine_expenese_SSP = 0
	maintenance_routine_expenese_USD = 0

	maintenance_breakdown_expenese_SSP = 0
	maintenance_breakdown_expenese_USD = 0

	for i in get_maintenance:

		# if i.amount and i.maintenance_type and i.currency:

		if i.amount and i.maintenance_type.name == "Routine" and i.currency == "SSP":
			maintenance_routine_expenese_SSP += i.amount 

		if i.amount and i.maintenance_type.name == "Routine" and i.currency == "USD":
			maintenance_routine_expenese_USD += i.amount 

		if i.amount and i.maintenance_type.name == "Break Down" and i.currency == "SSP":
			maintenance_breakdown_expenese_SSP += i.amount 

		if i.amount and i.maintenance_type.name == "Break Down" and i.currency == "USD":
			maintenance_breakdown_expenese_USD += i.amount

		if i.maintenance_type.name == None and i.currency == None :
			maintenance_routine_expenese_SSP   = 0
			maintenance_breakdown_expenese_USD = 0

	context = {
		'get_maintenance' : get_maintenance,
		'maintenance_routine_expenese_SSP' : maintenance_routine_expenese_SSP,
		'maintenance_routine_expenese_USD' : maintenance_routine_expenese_USD,
		'maintenance_breakdown_expenese_SSP' : maintenance_breakdown_expenese_SSP,
		'maintenance_breakdown_expenese_USD' : maintenance_breakdown_expenese_USD,
	}
	return render(request, 'backend/maintenance/maintenance_table.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def add_maintenance(request):
	get_maintenance_type 		= Maintenance_Type.objects.all()
	maintenance_id              = Maintenance.objects.all()
	currency       				= Maintenance.CURRENCY


	if request.method == 'POST':
		
		if request.POST.get('maintenance_type'):
			maintenance_type = request.POST['maintenance_type']
			Maintenance_Type.objects.create(name=maintenance_type, user=request.user)
			return redirect('add_maintenance')

		if request.POST['maintenance'] and request.POST['pub_date']  and request.POST['description1'] :
			form 					= request.POST
			maintenance_type 		= form['maintenance']
			pub_date 				= form['pub_date']
			description1      		= form['description1']
			total      				= form['total']

			formset_prefix = 'formset-'
			count = int(request.POST.get(f'formset-TOTAL_FORMS', 0))

			if count == 0 or count > 0 :

				try:
					amount = 0
					if total == "":
						total = int(amount) 

					maintenance_type_id = Maintenance_Type.objects.get(id=maintenance_type)

					parent_instance = Maintenance.objects.create(user=request.user, maintenance_type=maintenance_type_id, 
					pub_date=pub_date, description=description1, amount=total )

					for i in range(int(request.POST.get('formset-TOTAL_FORMS', 0))):
						data_description 	= request.POST.get(f'formset-{i}-description2')
						data_price 			= request.POST.get(f'formset-{i}-unit_price')
						data_quantity 		= request.POST.get(f'formset-{i}-quantity')
						data_discount 		= request.POST.get(f'formset-{i}-discount')
						data_amount 		= request.POST.get(f'formset-{i}-data_amount')
						data_currency 		= request.POST.get(f'formset-{i}-currency')

						if (data_description and data_price and data_quantity and data_discount and data_amount and data_currency):

							Maintenance_Expense_List.objects.create(sub_maintenance=parent_instance, description=data_description, quantity=int(data_quantity), 
							unit_price=data_price, discount=data_discount, currency=data_currency, amount=data_amount)
			
					messages.success(request, f'item added successfuly')
					return redirect('maintenance')

				except Exception as e:
					messages.error(request, f'{str(e)}')
					return redirect("add_maintenance")
			else:
				messages.error(request, f'the expense table is count : {count}')
				return redirect("add_maintenance")

		else:
			messages.error(request, f'the expense table is empty')
			return redirect("add_maintenance")
		
	context = {
		'maintenance_type' : get_maintenance_type,
		'currency':currency,
	}

	return render(request, 'backend/maintenance/add_maintenance.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def edit_maintenance(request, pk):

	if request.user.is_authenticated:
		get_maintenance 				= Maintenance.objects.get(id=pk)
		get_maintenance_type 			= Maintenance_Type.objects.all()
		get_units 						= Unit.objects.all()
		maintenance_expense				= Maintenance_Expense_List.objects.filter(sub_maintenance=get_maintenance)
		get_m_count                     = maintenance_expense.count()
		currency       					= Maintenance.CURRENCY

		if request.method == 'POST':

			if request.POST.get('maintenance_type'):
				maintenance_type = request.POST['maintenance_type']
				Maintenance_Type.objects.create(name=maintenance_type, user=request.user)

				return redirect('edit_maintenance', pk=get_maintenance.id)
	
			elif request.POST['maintenance__type'] or request.POST['pub_date'] or request.POST['total'] or request.POST['currency'] or request.POST['description1'] or request.POST['formset-MAX_NUM_FORM'] :
				maintenance__type 	= request.POST['maintenance__type']
				pub_date 			= request.POST['pub_date']
				amount  		 	= request.POST['total']
				currency       		= request.POST['currency']
				description1      	= request.POST['description1']

				maintenance_type_id 	= Maintenance_Type.objects.get(id=maintenance__type)

				get_maintenance.maintenance_type 	= maintenance_type_id
				get_maintenance.pub_date 			= pub_date
				get_maintenance.amount 				= amount
				get_maintenance.currency 			= currency
				get_maintenance.description 		= description1
				get_maintenance.save()


				for i in range(int(request.POST.get('formset-TOTAL_FORMS', 0))):
					data_description 	= request.POST.get(f'formset-{i}-description2')
					data_price 			= request.POST.get(f'formset-{i}-unit_price')
					data_quantity 		= request.POST.get(f'formset-{i}-quantity')
					data_discount 		= request.POST.get(f'formset-{i}-discount')
					data_amount 		= request.POST.get(f'formset-{i}-data_amount')

					
					if data_description or data_price or data_quantity or data_discount or data_amount:
						maintenance_exp = Maintenance_Expense_List.objects.create(
								sub_maintenance=get_maintenance, 
								description=data_description,
								quantity=data_quantity, 
								unit_price=data_price,
								discount=data_discount, 
								amount=data_amount
							)

				messages.success(request, f'item edited successfuly')
				return redirect('maintenance')
				

	else:
		return redirect('login')


	context = {
		'maintenance' 		: get_maintenance,
		'units'       		: get_units,
		'maintenance_type'  : get_maintenance_type,
		'maintenance_expense' : maintenance_expense,
		'get_m_count' : get_m_count,
		'currency':currency,
	}
	return render(request, 'backend/maintenance/edit_maintenance.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_maintenance(request, pk):

	if request.user.is_authenticated:
		get_maintenance 	= Maintenance.objects.get(id=pk)

		if request.method == 'POST':
			get_maintenance.delete()

			messages.success(request, f'item deleted successfuly')
			return redirect('maintenance')
	else:
		return redirect('login')

	context = {
		'get_maintenance' : get_maintenance,
	}
	return render(request, 'backend/maintenance/delete_maintenance.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def maintenance_status(request, pk):
	if request.user.is_authenticated:
		get_maintenance 			= Maintenance.objects.get(id=pk)
		get_maintenance_type 		= Maintenance_Type.objects.all()
		get_units 					= Unit.objects.all()
		currency       				= Maintenance.CURRENCY

		if request.method == 'POST':
			form = request.POST
			maintenance_type = form['maintenance_type']
			quantity 		 = form['quantity']
			unit 			 = form['units']
			currency  		 = form['currency']
			unit_price       = form['unit_price']
			description      = form['description']
			status           = form['status']

			total_amount = int(quantity) * float(unit_price)

			# print('>>> Maintenance Type <<<', maintenance_type)
			# print('>>> quantity <<<', quantity)
			# print('>>> unit <<<', unit)
			# print('>>> currency <<<', currency)
			# print('>>> unit price <<<', unit_price)
			# print('>>> amount <<<', total_amount)
			# print('>>> Description <<<', description)
			# print('>>> status <<<', status)

			maintenance_type_id 	= Maintenance_Type.objects.get(id=maintenance_type)
			unit_id					= Unit.objects.get(id=unit)

			get_maintenance.maintenance_type 	= maintenance_type_id
			get_maintenance.quantity 			= quantity
			get_maintenance.unit 				= unit_id
			get_maintenance.currency 			= currency
			get_maintenance.unit_price 			= unit_price
			get_maintenance.description 		= description
			get_maintenance.status 				= status
			get_maintenance.amount 				= total_amount
			get_maintenance.save()

			messages.success(request, f'item status updated successfuly ')
			return redirect('maintenance')	

	else:
		return redirect('login')

	context = {
		'maintenance' 		: get_maintenance,
		'units'       		: get_units,
		'maintenance_type'  : get_maintenance_type,
		'currency'          : currency,
	}
	return render(request, 'backend/maintenance/maintenance_status.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def maintenance_report(request):
	get_maintenance_report = Maintenance.objects.all()

	context = {
		'get_maintenance_report' : get_maintenance_report,
	}
	return render(request, 'backend/maintenance/maintenance_report.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def maintenance_report_routine_usd(request):
	get_maintenance_report_routine_usd = Maintenance.objects.all()

	context = {
		'get_maintenance_report_routine_usd' : get_maintenance_report_routine_usd,
	}
	return render(request, 'backend/maintenance/maintenance_report_routine_usd.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def maintenance_report_routine_ssp(request):
	get_maintenance_report_routine_ssp = Maintenance.objects.all()

	context = {
		'get_maintenance_report_routine_ssp' : get_maintenance_report_routine_ssp,
	}
	return render(request, 'backend/maintenance/maintenance_report_routine_ssp.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def maintenance_report_breakdown_usd(request):
	get_maintenance_report_breakdown_usd = Maintenance.objects.all()

	context = {
		'get_maintenance_report_breakdown_usd' : get_maintenance_report_breakdown_usd,
	}
	return render(request, 'backend/maintenance/maintenance_report_breakdown_usd.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def maintenance_report_breakdown_ssp(request):
	get_maintenance_report_breakdown_ssp = Maintenance.objects.all()

	context = {
		'get_maintenance_report_breakdown_ssp' : get_maintenance_report_breakdown_ssp,
	}
	return render(request, 'backend/maintenance/maintenance_report_breakdown_ssp.html', context)


# @login_required
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def fixed_cost(request):

	get_fixed_cost = Fixed_Cost.objects.all()

	get_count = get_fixed_cost.count()

	fixed_cost_weekly_expenese_SSP = 0
	fixed_cost_weekly_expenese_USD = 0

	for i in get_fixed_cost:

		if i.amount and i.currency:

			if i.currency == "SSP":
				fixed_cost_weekly_expenese_SSP += i.amount

			if i.currency == "USD":
				fixed_cost_weekly_expenese_USD += i.amount

			if i.currency == None:
				fixed_cost_weekly_expenese_SSP = 0
				fixed_cost_weekly_expenese_USD = 0

	context = {
		'fixed_cost' 		  			 : get_fixed_cost,
		'fixed_cost_weekly_expenese_SSP' : fixed_cost_weekly_expenese_SSP,
		'fixed_cost_weekly_expenese_USD' : fixed_cost_weekly_expenese_USD,
		'get_count' : get_count,
	}
	return render(request, 'backend/fixed_cost/fixed_cost_table.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def add_fixed_cost(request):

	if request.user.is_authenticated:
		get_units 		= Unit.objects.all()
		currency   		= Fixed_Cost.CURRENCY

		if request.method == 'POST':

			try:

				for i in range(int(request.POST.get('formset-TOTAL_FORMS', 0))):
					fixed_cost 	= request.POST.get(f'formset-{i}-fixed_cost')
					quantity    = request.POST.get(f'formset-{i}-quantity')
					unit      	= request.POST.get(f'formset-{i}-unit')
					currency 	= request.POST.get(f'formset-{i}-currency')
					unit_price 	= request.POST.get(f'formset-{i}-unit_price')
					amount 		= request.POST.get(f'formset-{i}-amount')

					if i == 0 and not (fixed_cost and quantity and unit and currency and unit_price and amount):
						messages.error(request, f'please fill in all required fields')
						return redirect('add_fixed_cost')

					elif i == 0 or i > 0 and (fixed_cost and quantity and unit and currency and unit_price and amount):

						unit_id = Unit.objects.get(id=unit) 

						Fixed_Cost.objects.create(user=request.user, fixed_cost=fixed_cost, quantity=quantity, unit=unit_id,
						currency=currency, unit_price=unit_price, amount=amount)

				messages.success(request, f'item added successfuly')
				return redirect('fixed_cost')

			except Exception as e:
				messages.error(request, f'{str(e)}')
				return redirect('add_fixed_cost')

	else:
		return redirect('login')

	context = {
		'units'    : get_units,
		'currency' : currency,
	}

	return render(request, 'backend/fixed_cost/add_fixed_cost.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def edit_fixed_cost(request, pk):

	if request.user.is_authenticated:
		fixed_cost_id  = Fixed_Cost.objects.get(id=pk)
		get_units 	   = Unit.objects.all()
		currency   		= Fixed_Cost.CURRENCY
		
		if request.method == 'POST':

			if request.POST.get('add_units'):
				gt_unit = request.POST['add_units']
				Unit.objects.create(name=gt_unit, user=request.user)

				return redirect('edit_fixed_cost', pk=fixed_cost_id.id)


			elif request.POST['fixed_cost'] or request.POST['quantity'] or request.POST['unit'] or request.POST['currency'] or request.POST['unit_price'] or request.POST['amount'] :
				fixed_cost    	= request.POST['fixed_cost']
				quantity      	= request.POST['quantity']
				unit          	= request.POST['unit']
				currency      	= request.POST['currency']
				unit_price    	= request.POST['unit_price']
				amount        	= request.POST['amount'] 

				# print('>>> Fixed Cost <<<', fixed_cost)
				# print('>>> quantity <<<', quantity)
				# print('>>> unit <<<', unit)
				# print('>>> currency <<<', currency)
				# print('>>> unit price <<<', unit_price)
				# print('>>> amount <<<', amount)
				unit_id        = Unit.objects.get(id=unit)

				fixed_cost_id.fixed_cost 	= fixed_cost
				fixed_cost_id.quantity   	= quantity
				fixed_cost_id.unit       	= unit_id
				fixed_cost_id.currency   	= currency
				fixed_cost_id.unit_price 	= unit_price
				fixed_cost_id.amount        = amount
				fixed_cost_id.save()

				messages.success(request, f'item edited successfuly')
				return redirect('fixed_cost')

	else:
		return redirect('login')

	context = {
		'fixed_cost'    : fixed_cost_id,
		'unit' 			: get_units,
		'currency'      : currency,
	}
	return render(request, 'backend/fixed_cost/edit_fixed_cost.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_fixed_cost(request, pk):

	if request.user.is_authenticated:

		fixed_cost_id  = Fixed_Cost.objects.get(id=pk)

		if request.method == 'POST':
			fixed_cost_id.delete()

			messages.success(request, f'item deleted successfuly')
			return redirect('fixed_cost')
	else:
		return redirect('login')

	context = {
		'fixed_cost_id' : fixed_cost_id,
	}
	return render(request, 'backend/fixed_cost/delete_fixed_cost.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def fixed_cost_report(request):
	get_fixed_cost_report = Fixed_Cost.objects.all()

	context = {
		'get_fixed_cost_report' : get_fixed_cost_report,
	}
	return render(request, 'backend/fixed_cost/fixed_cost_report.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def fixed_cost_report_ssp(request):
	get_fixed_cost_report_ssp = Fixed_Cost.objects.all()

	context = {
		'get_fixed_cost_report_ssp' : get_fixed_cost_report_ssp,
	}
	return render(request, 'backend/fixed_cost/fixed_cost_report_ssp.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def fixed_cost_report_usd(request):
	get_fixed_cost_report_usd = Fixed_Cost.objects.all()

	context = {
		'get_fixed_cost_report_usd' : get_fixed_cost_report_usd,
	}
	return render(request, 'backend/fixed_cost/fixed_cost_report_usd.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def fixed_cost_status(request, pk):
	
	if request.user.is_authenticated:
		fixed_cost_id  = Fixed_Cost.objects.get(id=pk)
		get_units 	   = Unit.objects.all()
		currency       = Fixed_Cost.CURRENCY
		
		if request.method == 'POST':

			if request.POST.get('add_units'):
				gt_unit = request.POST['add_units']
				Unit.objects.create(name=gt_unit, user=request.user)

				return redirect('fixed_cost_status', pk=fixed_cost_id.id)


			elif request.POST['fixed_cost'] or request.POST['quantity'] or request.POST['unit'] or request.POST['currency'] or request.POST['unit_price'] or request.POST['amount'] :

				fixed_cost    	= request.POST['fixed_cost']
				quantity      	= request.POST['quantity']
				unit          	= request.POST['unit']
				currency      	= request.POST['currency']
				unit_price    	= request.POST['unit_price']
				amount        	= request.POST['amount']
				status        	= request.POST['status']  

				# print('>>> Fixed Cost <<<', fixed_cost)
				# print('>>> quantity <<<', quantity)
				# print('>>> unit <<<', unit)
				# print('>>> currency <<<', currency)
				# print('>>> unit price <<<', unit_price)
				# print('>>> amount <<<', amount)
				# print('>>> status <<<', status)

				unit_id        = Unit.objects.get(id=unit)

				fixed_cost_id.fixed_cost 	= fixed_cost
				fixed_cost_id.quantity   	= quantity
				fixed_cost_id.unit       	= unit_id
				fixed_cost_id.currency   	= currency
				fixed_cost_id.unit_price 	= unit_price
				fixed_cost_id.status        = status
				fixed_cost_id.amount        = amount
				fixed_cost_id.save()

				messages.success(request, f'item status updated successfuly')
				return redirect('fixed_cost')

	else:
		return redirect('login')

	context = {
		'fixed_cost'    : fixed_cost_id,
		'unit' 			: get_units,
		'currency'      : currency,
	}
	return render(request, 'backend/fixed_cost/fixed_cost_status.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def block_transportation(request):

	if request.user.is_authenticated:
		get_block_transportation = Block_Transportation.objects.all()

		block_transportation_weekly_expenses_SSP = 0
		block_transportation_weekly_expenses_USD = 0
		get_transportation_damages = 0

		for i in get_block_transportation:

			if i.amount and i.currency == "SSP":
				block_transportation_weekly_expenses_SSP += i.amount

			if i.amount and i.currency == "USD":
				block_transportation_weekly_expenses_USD += i.amount

			if i.transportation_damages:
				get_transportation_damages += i.transportation_damages

	else:
		return redirect('login')

	context = {
		'block_transportation' : get_block_transportation,
		'block_transportation_weekly_expenses_SSP' : block_transportation_weekly_expenses_SSP,
		'block_transportation_weekly_expenses_USD' : block_transportation_weekly_expenses_USD,
		'get_transportation_damages' : get_transportation_damages,

	}
	return render(request, 'backend/transportation/blocks/block_transportation_table.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def add_block_transportation(request):

	if request.user.is_authenticated:
		get_transportation_type = Transportation_Type.objects.filter(name='Block')
		get_block_type 			= Block_Type.objects.all()
		get_cost_type           = Cost_Type.objects.all()

		if request.method == 'POST':
			client_name          = request.POST['client_name']
			transportation_type  = request.POST['transportation_type']
			block_type           = request.POST['block_type']
			currency_type        = request.POST['currency']
			quantity             = request.POST['quantity']
			# amount               = request.POST['amount']
			damages              = request.POST['damages']
			# cost_type            = request.POST['cost_type']
			c_quantity           = request.POST['c_quantity']
			c_amount             = request.POST['c_amount']

			# print('>>> Client <<<', client_name)
			# print('>>> Transportation Type <<<', transportation_type)
			# print('>>> Block Type <<<', block_type)
			# print('>>> currency <<<', currency_type)
			# print('>>> quantity <<<', quantity)
			# print('>>> Amount <<<', amount)
			# print('>>> Damage <<<', damages)

			# get_amount 		= int(quantity) * int(amount)
			# final_amount 	= float(get_amount)

			transportation_type_id 		= Transportation_Type.objects.get(id=transportation_type)
			block_type_id          		= Block_Type.objects.get(id=block_type)

			print(">>>>>>", request.POST)

			Block_Transportation.objects.create(user=request.user, client_name=client_name, transportation_type=transportation_type_id, 
				block=block_type_id, currency=currency_type, quantity=quantity, amount=0, 
				transportation_damages=damages)

			# Transportation_Cost_Detail.objects.create(block=block_transportation,cost_type=cost_type, quantity=c_quantity, amount=c_amount)

			messages.success(request, f'item added successfuly')
			return redirect('block_transportation')

	else:
		return redirect('login')

	
	context = {
		'transportation_type' : get_transportation_type,
		'block_type'          : get_block_type,
		'cost_type'           : get_cost_type,
	}
	
	return render(request, 'backend/transportation/blocks/add_block_transportation.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def edit_block_transportation(request, pk):

	if request.user.is_authenticated:
		get_block_transportation	 	= Block_Transportation.objects.get(id=pk)
		get_transportation_type 		= Transportation_Type.objects.all()
		get_block_type 					= Block_Type.objects.all()
		get_cost_type           		= Cost_Type.objects.all()

		if request.method == 'POST':
			client_name          = request.POST['client_name']
			transportation_type  = request.POST['transportation_type']
			block_type           = request.POST['block_type']
			cost_type            = request.POST['cost_type']
			currency_type        = request.POST['currency']
			quantity             = request.POST['quantity']
			amount               = request.POST['amount']
			damages              = request.POST['damages']

			transportation_type_id = Transportation_Type.objects.get(id=transportation_type)
			block_type_id          = Block_Type.objects.get(id=block_type)
			cost_type_id           = Cost_Type.objects.get(id=cost_type)

			# print('>>> Client <<<', client_name)
			# print('>>> Transportation Type <<<', transportation_type_id)
			# print('>>> Block Type <<<', block_type_id)
			# print('>>> Cost Type <<<', cost_type_id)
			# print('>>> currency <<<', currency_id)
			# print('>>> quantity <<<', quantity)
			# print('>>> Amount <<<', amount)
			# print('>>> Damage <<<', damages)

			get_block_transportation.client_name 				= client_name
			get_block_transportation.transportation_type 		= transportation_type_id
			get_block_transportation.block   					= block_type_id
			get_block_transportation.cost 						= cost_type_id
			get_block_transportation.currency 					= currency_type
			get_block_transportation.quantity 					= quantity
			get_block_transportation.amount   					= amount
			get_block_transportation.transportation_damages 	= damages
			get_block_transportation.save()

			messages.success(request, f'item edited successfuly')
			return redirect('block_transportation')

	else:
		return redirect('login')


	context = {
		'block_transportation' 	: get_block_transportation,
		'transportation_type' 	: get_transportation_type,
		'block_type'       		: get_block_type,
		'cost_type'             : get_cost_type,
	}

	return render(request, 'backend/transportation/blocks/edit_block_transportation.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_block_transportation(request, pk):

	if request.user.is_authenticated:
		get_block_transportation_id	 = Block_Transportation.objects.get(id=pk)

		if request.method == 'POST':
			get_block_transportation_id.delete()

			messages.success(request, f'item deleted successfuly')
			return redirect('block_transportation')

	else:
		return redirect('login')


	context = {
		'get_block_transportation_id' : get_block_transportation_id,
	}
	return render(request, 'backend/transportation/blocks/delete_block_transportation.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def material_transportation(request):

	material_transportation = Material_Transportation.objects.all()
	material_transportation_count = material_transportation.count()

	material_transportation_weekly_expenses_SSP = 0
	material_transportation_weekly_expenses_USD = 0

	for i in material_transportation:

		if i.amount and i.currency == "SSP":
			material_transportation_weekly_expenses_SSP += i.amount

		if i.amount and i.currency == "USD":
			material_transportation_weekly_expenses_USD += i.amount

	context = {
		'material_transportation' : material_transportation,
		'material_transportation_weekly_expenses_USD' : material_transportation_weekly_expenses_USD,
		'material_transportation_weekly_expenses_SSP' : material_transportation_weekly_expenses_SSP,
		'material_transportation_count' : material_transportation_count,
	}
	return render(request, 'backend/transportation/materials/material_transportation_table.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def add_material_transportation(request):

	if request.user.is_authenticated:
		get_transportation_type = Transportation_Type.objects.filter(name='Material')
		get_units 	   			= Unit.objects.all()
		currency                = Material_Transportation.CURRENCY

		if request.method == 'POST':
			transportation_type  = request.POST['transportation_type']
			unit                 = request.POST['unit']
			quantity             = request.POST['quantity']
			amount               = request.POST['amount']
			currency_type        = request.POST['currency']

			# print('>>> Transportation Type <<<', transportation_type)
			# print('>>> Unit <<<', unit)
			# print('>>> currency <<<', currency_type)
			# print('>>> quantity <<<', quantity)
			# print('>>> Amount <<<', amount)

			transportation_type_id = Transportation_Type.objects.get(id=transportation_type)
			unit_id                = Unit.objects.get(id=unit)

			Material_Transportation.objects.create(user=request.user, transportation_type=transportation_type_id,
				currency=currency_type, unit=unit_id, quantity=quantity, amount=amount )

			messages.success(request, f'item added successfuly')
			return redirect('material_transportation')

	else:
		return redirect('login')


	context = {
		'transportation_type' : get_transportation_type,
		'units'               : get_units,
		'currency'            : currency,
	}

	return render(request, 'backend/transportation/materials/add_material_transportation.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def edit_material_transportation(request, pk):

	if request.user.is_authenticated:
		material_transportation 	= Material_Transportation.objects.get(id=pk)
		get_transportation_type 	= Transportation_Type.objects.filter(name='Material')
		get_units 	   				= Unit.objects.all()

		if request.method == 'POST':
			transportation_type  = request.POST['transportation_type']
			unit                 = request.POST['unit']
			quantity             = request.POST['quantity']
			amount               = request.POST['amount']
			currency_type        = request.POST['currency']

			# print('>>> Transportation Type <<<', transportation_type)
			# print('>>> Unit <<<', unit)
			# print('>>> currency <<<', currency_type)
			# print('>>> quantity <<<', quantity)
			# print('>>> Amount <<<', amount)

			transportation_type_id = Transportation_Type.objects.get(id=transportation_type)
			unit_id                = Unit.objects.get(id=unit)

			material_transportation.transportation_type = transportation_type_id
			material_transportation.unit 				= unit_id
			material_transportation.quantity 			= quantity
			material_transportation.amount 				= amount
			material_transportation.currency 			= currency_type
			material_transportation.save()

			messages.success(request, f'item edited successfuly')
			return redirect('material_transportation')

	else:
		return redirect('login')

	context = {
		'material_transportation' : material_transportation,
		'transportation_type' : get_transportation_type,
		'units'               : get_units,

	}
	return render(request, 'backend/transportation/materials/edit_material_transportation.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_material_transportation(request, pk):

	if request.user.is_authenticated:
		material_transportation = Material_Transportation.objects.get(id=pk)

		if request.method == 'POST':
			material_transportation.delete()

			messages.success(request, f'item deleted successfuly')
			return redirect('material_transportation')
	else:
		return redirect('login')

	context = {
		'material_transportation' : material_transportation,
	}
	return render(request, 'backend/transportation/materials/delete_material_transportation.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def material_transportation_report(request):
	material_transportation_report = Material_Transportation.objects.all()

	context = {
		'material_transportation_report' : material_transportation_report, 
	}
	return render(request, 'backend/transportation/materials/material_transportation_report.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def material_transportation_report_ssp(request):
	material_transportation_report_ssp = Material_Transportation.objects.all()

	context = {
		'material_transportation_report_ssp' : material_transportation_report_ssp, 
	}
	return render(request, 'backend/transportation/materials/material_transportation_report_ssp.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def material_transportation_report_usd(request):
	material_transportation_report_usd = Material_Transportation.objects.all()

	context = {
		'material_transportation_report_usd' : material_transportation_report_usd, 
	}
	return render(request, 'backend/transportation/materials/material_transportation_report_usd.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def material_transportation_status(request, pk):
	if request.user.is_authenticated:
		material_transportation 	= Material_Transportation.objects.get(id=pk)
		get_transportation_type 	= Transportation_Type.objects.filter(name='Material')
		get_units 	   				= Unit.objects.all()

		if request.method == 'POST':
			transportation_type  = request.POST['transportation_type']
			unit                 = request.POST['unit']
			quantity             = request.POST['quantity']
			amount               = request.POST['amount']
			status               = request.POST['status']
			currency_type        = request.POST['currency']

			# print('>>> Transportation Type <<<', transportation_type)
			# print('>>> Unit <<<', unit)
			# print('>>> currency <<<', currency_type)
			# print('>>> quantity <<<', quantity)
			# print('>>> status <<<', status)
			# print('>>> Amount <<<', amount)

			transportation_type_id = Transportation_Type.objects.get(id=transportation_type)
			unit_id                = Unit.objects.get(id=unit)

			material_transportation.transportation_type = transportation_type_id
			material_transportation.unit 				= unit_id
			material_transportation.quantity 			= quantity
			material_transportation.amount 				= amount
			material_transportation.currency 			= currency_type
			material_transportation.status 			    = status
			material_transportation.save()

			messages.success(request, f'item status updated successfuly')
			return redirect('material_transportation')

	else:
		return redirect('login')

	context = {
		'material_transportation' : material_transportation,
		'transportation_type' : get_transportation_type,
		'units'               : get_units,

	}
	return render(request, 'backend/transportation/materials/material_transportation_status.html', context)

@login_required
def other_transportation(request):

	if request.user.is_authenticated:

		all_other_transportation = Other_Transportation.objects.all()
		get_other_transportation_count = all_other_transportation.count() 

		other_transportation_weekly_expenses_SSP = 0
		other_transportation_weekly_expenses_USD = 0

		for i in all_other_transportation:

			if i.amount and i.currency == "SSP":
				other_transportation_weekly_expenses_SSP += i.amount

			if i.amount and i.currency == "USD":
				other_transportation_weekly_expenses_USD += i.amount

	else:
		return redirect('login')

	context = {
		'all_other_transportation' : all_other_transportation,
		'other_transportation_weekly_expenses_SSP' : other_transportation_weekly_expenses_SSP,
		'other_transportation_weekly_expenses_USD' : other_transportation_weekly_expenses_USD,
		'get_other_transportation_count' : get_other_transportation_count,

	}
	return render(request, 'backend/transportation/others/other_transportation_table.html', context)


@login_required
def add_other_transportation(request):

	if request.user.is_authenticated:
		get_transportation_type 	= Transportation_Type.objects.filter(name='Other')
		get_units 	   				= Unit.objects.all()

		if request.method == 'POST':
			transportation_type  = request.POST['transportation_type']
			unit                 = request.POST['unit']
			quantity             = request.POST['quantity']
			amount               = request.POST['amount']
			currency_type        = request.POST['currency']
			description      	 = request.POST['description']

			# print('>>> Transportation Type <<<', transportation_type)
			# print('>>> Unit <<<', unit)
			# print('>>> currency <<<', currency_type)
			# print('>>> quantity <<<', quantity)
			# print('>>> Amount <<<', amount)
			# print('>>> Description <<<', description)


			transportation_type_id = Transportation_Type.objects.get(id=transportation_type)
			unit_id                = Unit.objects.get(id=unit)

			Other_Transportation.objects.create(user=request.user, transportation_type=transportation_type_id, quantity=quantity,
				unit=unit_id, currency=currency_type, amount=amount, description=description)
			
			messages.success(request, f'item added successfuly')
			return redirect('other_transportation')

	else:
		return redirect('login')

	context = {
		'transportation_type' : get_transportation_type,
		'units'               : get_units,
	}
	return render(request, 'backend/transportation/others/add_other_transportation.html', context)


@login_required
def edit_other_transportation(request, pk):

	if request.user.is_authenticated:
		other_transportation 		= Other_Transportation.objects.get(id=pk)
		get_transportation_type 	= Transportation_Type.objects.filter(name='Other')
		get_units 	   				= Unit.objects.all()

		if request.method == 'POST':
			transportation_type  = request.POST['transportation_type']
			unit                 = request.POST['unit']
			quantity             = request.POST['quantity']
			amount               = request.POST['amount']
			currency_type        = request.POST['currency']
			description      	 = request.POST['description']

			# print('>>> Transportation Type <<<', transportation_type)
			# print('>>> Unit <<<', unit)
			# print('>>> currency <<<', currency_type)
			# print('>>> quantity <<<', quantity)
			# print('>>> Amount <<<', amount)
			# print('>>> Description <<<', description)


			transportation_type_id = Transportation_Type.objects.get(id=transportation_type)
			unit_id                = Unit.objects.get(id=unit)

			other_transportation.transportation_type = transportation_type_id
			other_transportation.unit 				 = unit_id
			other_transportation.quantity 			 = quantity
			other_transportation.amount 			 = amount
			other_transportation.currency 			 = currency_type
			other_transportation.description 		 = description
			other_transportation.save()

			messages.success(request, f'item edited successfuly')
			return redirect('other_transportation')

	else:
		return redirect('login')

	context = {
		'transportation_type' : get_transportation_type,
		'units'               : get_units,
		'other_transportation' : other_transportation,
	}
	return render(request, 'backend/transportation/others/edit_other_transportation.html', context)


@login_required
def delete_other_transportation(request, pk):

	if request.user.is_authenticated:

		other_transportation_id = Other_Transportation.objects.get(id=pk)

		if request.method == 'POST':
			other_transportation_id.delete()

			messages.success(request, f'item deleted successfuly')
			return redirect('other_transportation')

	else:
		return redirect('login')


	context = {
		'other_transportation_id' : other_transportation_id,
	}
	return render(request, 'backend/transportation/others/delete_other_transportation.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def other_transportation_report(request):
	other_transportation_report = Other_Transportation.objects.all()

	context = {
		'other_transportation_report' : other_transportation_report,
	}
	return render(request, 'backend/transportation/others/other_transportation_report.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def other_transportation_report_usd(request):
	other_transportation_report_usd = Other_Transportation.objects.all()

	context = {
		'other_transportation_report_usd' : other_transportation_report_usd,
	}
	return render(request, 'backend/transportation/others/other_transportation_report_usd.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def other_transportation_report_ssp(request):
	other_transportation_report_ssp = Other_Transportation.objects.all()

	context = {
		'other_transportation_report_ssp' : other_transportation_report_ssp,
	}
	return render(request, 'backend/transportation/others/other_transportation_report_ssp.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def other_transportation_status(request, pk):
	
	if request.user.is_authenticated:
		other_transportation 		= Other_Transportation.objects.get(id=pk)
		get_transportation_type 	= Transportation_Type.objects.filter(name='Other')
		get_units 	   				= Unit.objects.all()

		if request.method == 'POST':
			transportation_type  = request.POST['transportation_type']
			unit                 = request.POST['unit']
			quantity             = request.POST['quantity']
			amount               = request.POST['amount']
			currency_type        = request.POST['currency']
			status               = request.POST['status']
			description      	 = request.POST['description']

			# print('>>> Transportation Type <<<', transportation_type)
			# print('>>> Unit <<<', unit)
			# print('>>> currency <<<', currency_type)
			# print('>>> quantity <<<', quantity)
			# print('>>> Amount <<<', amount)
			# print('>>> Status <<<', status)
			# print('>>> Description <<<', description)


			transportation_type_id = Transportation_Type.objects.get(id=transportation_type)
			unit_id                = Unit.objects.get(id=unit)

			other_transportation.transportation_type = transportation_type_id
			other_transportation.unit 				 = unit_id
			other_transportation.quantity 			 = quantity
			other_transportation.amount 			 = amount
			other_transportation.currency 			 = currency_type
			other_transportation.status 			 = status
			other_transportation.description 		 = description
			other_transportation.save()

			messages.success(request, f'item status updated successfuly')
			return redirect('other_transportation')

	else:
		return redirect('login')

	context = {
		'transportation_type' : get_transportation_type,
		'units'               : get_units,
		'other_transportation' : other_transportation,
	}
	return render(request, 'backend/transportation/others/other_transportation_status.html', context)

@login_required
def other_expenses(request):

	if request.user.is_authenticated:

		get_other_expenses = Other_Expenses.objects.all()
		get_other_expenses_count = get_other_expenses.count()

		other_expenses_weekly_expenses_SSP = 0
		other_expenses_weekly_expenses_USD = 0

		for i in get_other_expenses:

			if i.amount and i.currency == "SSP":
				other_expenses_weekly_expenses_SSP += i.amount

			if i.amount and i.currency == "USD":
				other_expenses_weekly_expenses_USD += i.amount

	else:
		return redirect('login')

	context = {
		'other_expenses' : get_other_expenses,
		'other_expenses_weekly_expenses_SSP' : other_expenses_weekly_expenses_SSP,
		'other_expenses_weekly_expenses_USD' : other_expenses_weekly_expenses_USD,
		'get_other_expenses_count' : get_other_expenses_count,
	}
	return render(request, 'backend/other_expenses/other_expenses_table.html', context)


@login_required
def add_other_expenses(request):

	if request.user.is_authenticated:
		get_units 		= Unit.objects.all()
		currency 		= Other_Expenses.CURRENCY

		if request.method == 'POST':
			description       = request.POST['description']
			quantity 		  = request.POST['quantity']
			unit 			  = request.POST['unit']
			currency_type  		  = request.POST['currency']
			unit_price        = request.POST['unit_price']

			total_amount 	  = int(quantity) * int(unit_price)

			# print('>>> quantity <<<', quantity)
			# print('>>> unit <<<', unit)
			# print('>>> currency <<<', currency)
			# print('>>> unit price <<<', unit_price)
			# print('>>> amount <<<', total_amount)
			# print('>>> Description <<<', description)

			unit_id			= Unit.objects.get(id=unit)

			Other_Expenses.objects.create(user=request.user, description=description, quantity=quantity, unit=unit_id, unit_price=unit_price,
				amount=total_amount, currency=currency_type)

			messages.success(request, f'item added successfuly')
			return redirect('other_expenses')

	else:
		return redirect('login')	

	context = {
		'units' : get_units,
		'currency':currency,
	}

	return render(request, 'backend/other_expenses/add_other_expenses.html', context)


@login_required
def edit_other_expenses(request, pk):

	if request.user.is_authenticated:
		other_expenses  			= Other_Expenses.objects.get(id=pk)
		get_units 					= Unit.objects.all()
		currency 					= Other_Expenses.CURRENCY

		if request.method == 'POST':
			description       = request.POST['description']
			quantity 		  = request.POST['quantity']
			unit 			  = request.POST['unit']
			currency  		  = request.POST['currency']
			unit_price        = request.POST['unit_price']

			total_amount 	  = int(quantity) * float(unit_price)

			# print('>>> quantity <<<', quantity)
			# print('>>> unit <<<', unit)
			# print('>>> currency <<<', currency)
			# print('>>> unit price <<<', unit_price)
			# print('>>> amount <<<', total_amount)
			# print('>>> Description <<<', description)

			unit_id			= Unit.objects.get(id=unit)

			other_expenses.description = description
			other_expenses.quantity    = quantity
			other_expenses.unit        = unit_id
			other_expenses.currency    = currency
			other_expenses.unit_price  = unit_price
			other_expenses.amount      = total_amount
			other_expenses.save()

			messages.success(request, f'item updated successfuly')
			return redirect('other_expenses')	

	else:
		return redirect('login')

	context = {
		'other_expenses'    : other_expenses,
		'units' 			: get_units,
		'currency'          : currency,
	}

	return render(request, 'backend/other_expenses/edit_other_expenses.html', context)

@login_required
def delete_other_expenses(request, pk):

	if request.user.is_authenticated:
		other_expenses_id  = Other_Expenses.objects.get(id=pk)

		if request.method == 'POST':
			other_expenses_id.delete()

			messages.success(request, f'item deleted successfuly')
			return redirect('other_expenses')
	else:
		return redirect('login')


	context = {
		'other_expenses_id' : other_expenses_id,
	}
	
	return render(request, 'backend/other_expenses/delete_other_expenses.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def other_expenses_status(request, pk):

	other_expenses  			= Other_Expenses.objects.get(id=pk)
	get_units 					= Unit.objects.all()
	currency 					= Other_Expenses.CURRENCY

	if request.method == 'POST':
		description       = request.POST['description']
		quantity 		  = request.POST['quantity']
		unit 			  = request.POST['unit']
		currency  		  = request.POST['currency']
		unit_price        = request.POST['unit_price']
		status            = request.POST['status']

		total_amount 	  = int(quantity) * float(unit_price)

		# print('>>> quantity <<<', quantity)
		# print('>>> unit <<<', unit)
		# print('>>> currency <<<', currency)
		# print('>>> unit price <<<', unit_price)
		# print('>>> amount <<<', total_amount)
		# print('>>> Description <<<', description)
		# print('>>> Status <<<', status)

		unit_id			= Unit.objects.get(id=unit)

		other_expenses.description = description
		other_expenses.quantity    = quantity
		other_expenses.unit        = unit_id
		other_expenses.currency    = currency
		other_expenses.unit_price  = unit_price
		other_expenses.status      = status
		other_expenses.amount      = total_amount
		other_expenses.save()

		messages.success(request, f'item updated successfuly')
		return redirect('other_expenses')	

	context = {
		'other_expenses'    : other_expenses,
		'units' 			: get_units,
		'currency'          : currency,
	}

	return render(request, 'backend/other_expenses/other_expenses_status.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def other_expenses_report(request):
	other_expenses_report = Other_Expenses.objects.all()

	context = {
		'other_expenses_report' : other_expenses_report,
	}
	return render(request, 'backend/other_expenses/other_expenses_report.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def other_expenses_report_ssp(request):
	other_expenses_report_ssp = Other_Expenses.objects.all()

	context = {
		'other_expenses_report_ssp' : other_expenses_report_ssp,
	}
	return render(request, 'backend/other_expenses/other_expenses_report_ssp.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
def other_expenses_report_usd(request):
	other_expenses_report_usd = Other_Expenses.objects.all()

	context = {
		'other_expenses_report_usd' : other_expenses_report_usd,
	}
	return render(request, 'backend/other_expenses/other_expenses_report_usd.html', context)

@login_required
def sale(request):

	if request.user.is_authenticated:

		all_sales = Sales.objects.all()

		credit_weekly_SSP = 0
		credit_weekly_USD = 0

		cash_weekly_SSP = 0
		cash_weekly_USD = 0

		for i in all_sales:

			if i.transaction.name == "credit" and i.amount and i.currency == "SSP":
				credit_weekly_SSP += i.amount - i.discount

			if i.transaction.name == "credit" and i.amount and i.currency == "USD":
				credit_weekly_USD += i.amount - i.discount

			if i.transaction.name == "cash" and i.amount and i.currency == "SSP":
				cash_weekly_SSP += i.amount - i.discount

			if i.transaction.name == "cash" and i.amount and i.currency == "USD":
				cash_weekly_USD += i.amount - i.discount

	else:
		return redirect('login')

	context = {
		'all_sales' : all_sales,
		'credit_weekly_SSP' : credit_weekly_SSP,
		'credit_weekly_USD' : credit_weekly_USD,
		'cash_weekly_SSP' : cash_weekly_SSP,
		'cash_weekly_USD' : cash_weekly_USD,

	}
	return render(request, 'backend/sale/sale_table.html', context)

def add_sale(request):

	if request.user.is_authenticated:
		get_transaction = Transaction_Type.objects.all().exclude(name='Partial')
		get_block       = Block_Type.objects.all()
		currency        = Sales.CURRENCY

		if request.method == 'POST':
			client_name         = request.POST['client_name']
			transaction   		= request.POST['transaction']
			block         		= request.POST['block']
			quantity_sold      	= request.POST['quantity_sold']
			unit_price      	= request.POST['unit_price']
			discount      		= request.POST['discount']
			currency      		= request.POST['currency']

			get_total           = int(quantity_sold) * float(unit_price)
			amount              = int(get_total) - float(discount)

			# print('>>> quantity <<<', transaction)
			# print('>>> block <<<', block)
			# print('>>> quantity sold <<<', quantity_sold)
			# print('>>> unit price <<<', unit_price)
			# print('>>> discount <<<', discount)
			# print('>>> currency <<<', currency)
			# print('>>> amount <<<', amount)

			transaction_id = Transaction_Type.objects.get(id=transaction)
			block_id       = Block_Type.objects.get(id=block)

			Sales.objects.create(user=request.user, transaction=transaction_id, block=block_id, quantity_Sold=quantity_sold, unit_price=unit_price,
				currency=currency, client_name=client_name, discount=discount, amount=amount)

			messages.success(request, f'item added successfuly')
			return redirect('sale')

	else:
		return redirect('login')


	context = {
		'transaction' 	  : get_transaction,
		'get_block'       : get_block,
		'currency'        : currency,
	}
	return render(request, 'backend/sale/add_sale.html', context)

@login_required
def edit_sale(request, pk):

	if request.user.is_authenticated:
		get_sale         	= Sales.objects.get(id=pk)
		get_transaction 	= Transaction_Type.objects.all().exclude(name='partial')
		get_block       	= Block_Type.objects.all()

		if request.method == 'POST':
			client_name         = request.POST['client_name']
			transaction   		= request.POST['transaction']
			block         		= request.POST['block']
			quantity_sold      	= request.POST['quantity_sold']
			unit_price      	= request.POST['unit_price']
			discount      		= request.POST['discount']
			currency      		= request.POST['currency']

			# print('>>> quantity <<<', transaction)
			# print('>>> block <<<', block)
			# print('>>> quantity sold <<<', quantity_sold)
			# print('>>> unit price <<<', unit_price)
			# print('>>> discount <<<', discount)
			# print('>>> currency <<<', currency)
			# print('>>> amount <<<', amount)

			transaction_id = Transaction_Type.objects.get(id=transaction)
			block_id       = Block_Type.objects.get(id=block)

			get_total           = int(quantity_sold) * float(unit_price)
			amount              = int(get_total) - float(discount)

			get_sale.client_name 		= client_name
			get_sale.transaction 		= transaction_id
			get_sale.block       		= block_id
			get_sale.quantity_sold 		= quantity_sold
			get_sale.unit_price         = unit_price
			get_sale.discount           = discount
			get_sale.currency           = currency
			get_sale.amount             = amount
			get_sale.save()

			messages.success(request, f'item edited successfuly')
			return redirect('sale')

	else:
		return redirect('login')

	context = {
		'transaction' 	  : get_transaction,
		'get_block'       : get_block,
		'sale'            : get_sale,
	}

	return render(request, 'backend/sale/edit_sale.html', context)


@login_required
def delete_sale(request, pk):

	if request.user.is_authenticated:
		get_sale_id         	= Sales.objects.get(id=pk)

		if request.method == 'POST':
			get_sale_id.delete()

			messages.success(request, f'item deleted successfuly')
			return redirect('sale')
	else:
		return redirect('login')

	context = {
		'get_sale_id' : get_sale_id,
	}
	return render(request, 'backend/sale/delete_sale.html', context)

@login_required
def partial_sale(request):

	if request.user.is_authenticated:
		all_partial_sale = Partial_Sales.objects.all()

		partial_sale_weekly_SSP = 0
		partial_sale_weekly_USD = 0

		for i in all_partial_sale:

			if i.transaction.name == "partial" and i.amount and i.currency == "SSP":
				partial_sale_weekly_SSP += i.amount - i.discount

			if i.transaction.name == "partial" and i.amount and i.currency == "USD":
				partial_sale_weekly_USD += i.amount - i.discount

	else:
		return redirect('login')

	context = {
		'partial_sale' : all_partial_sale,
		'partial_sale_weekly_SSP' : partial_sale_weekly_SSP,
		'partial_sale_weekly_USD' : partial_sale_weekly_USD,
	}
	return render(request, 'backend/sale/partial/partial_sale_table.html', context)

@login_required
def add_partial_sale(request):

	if request.user.is_authenticated:
		get_transaction = Transaction_Type.objects.filter(name='Partial')
		get_block       = Block_Type.objects.all()
		currency        = Partial_Sales.CURRENCY

		if request.method == 'POST':
			client_name         = request.POST['client_name']
			transaction   		= request.POST['transaction']
			block         		= request.POST['block']
			quantity_sold      	= request.POST['quantity_sold']
			unit_price      	= request.POST['unit_price']
			discount      		= request.POST['discount']
			amount_paid      	= request.POST['amount_paid']
			currency      		= request.POST['currency']

			get_total           = int(quantity_sold) * float(unit_price)
			amount              = int(get_total) - float(discount)
			balance             = float(amount) - float(amount_paid)

			# print('>>> quantity <<<', transaction)
			# print('>>> block <<<', block)
			# print('>>> quantity sold <<<', quantity_sold)
			# print('>>> unit price <<<', unit_price)
			# print('>>> discount <<<', discount)
			# print('>>> currency <<<', currency)
			# print('>>> amount <<<', amount)
			# print('>>> amount paid <<<', amount_paid)
			# print('>>> balance <<<', balance)

			#number = 'INV-'+ str(uuid4()).split('-')[4]
			last_invoice = Partial_Sales.objects.all()
			print(last_invoice)

			serial_number = 0
			if last_invoice:
				last_invoice = Partial_Sales.objects.all()

				i_number = "INV-" + str(serial_number+1).zfill(3)


			transaction_id = Transaction_Type.objects.get(id=transaction)
			block_id       = Block_Type.objects.get(id=block)

			Partial_Sales.objects.create(user=request.user, transaction=transaction_id, invoice_number=serial_number, block=block_id, quantity_Sold=quantity_sold, unit_price=unit_price,
				currency=currency, client_name=client_name, discount=discount, amount=amount, amount_paid=amount_paid,
				balance=balance)




			messages.success(request, f'item added successfuly')
			return redirect('partial_sale')

	else:
		return redirect('login')

	context = {
		'transaction' 	  : get_transaction,
		'get_block'       : get_block,
		'currency'        : currency,
	}

	return render(request, 'backend/sale/partial/add_partial_sale.html', context)

@login_required
def edit_partial_sale(request, pk):

	if request.user.is_authenticated:
		partial_sale    = Partial_Sales.objects.get(id=pk)
		get_transaction = Transaction_Type.objects.filter(name='partial')
		get_block       = Block_Type.objects.all()

		if request.method == 'POST':
			client_name         = request.POST['client_name']
			transaction   		= request.POST['transaction']
			block         		= request.POST['block']
			quantity_sold      	= request.POST['quantity_sold']
			unit_price      	= request.POST['unit_price']
			discount      		= request.POST['discount']
			amount_paid      	= request.POST['amount_paid']
			currency      		= request.POST['currency']

			get_total           = int(quantity_sold) * float(unit_price)
			amount              = int(get_total) - float(discount)
			balance             = float(amount) - float(amount_paid)

			# print('>>> quantity <<<', transaction)
			# print('>>> block <<<', block)
			# print('>>> quantity sold <<<', quantity_sold)
			# print('>>> unit price <<<', unit_price)
			# print('>>> discount <<<', discount)
			# print('>>> currency <<<', currency)
			# print('>>> amount <<<', amount)
			# print('>>> amount paid <<<', amount_paid)
			# print('>>> balance <<<', balance)

			transaction_id = Transaction_Type.objects.get(id=transaction)
			block_id       = Block_Type.objects.get(id=block)

			partial_sale.transaction 	= transaction_id
			partial_sale.block 		 	= block_id
			partial_sale.quantity_Sold  = quantity_sold
			partial_sale.unit_price     = quantity_sold
			partial_sale.currency       = currency
			partial_sale.client_name    = client_name
			partial_sale.amount_paid    = amount_paid
			partial_sale.discount       = discount
			partial_sale.amount         = get_total
			partial_sale.balance        = balance
			partial_sale.save()
			
			messages.success(request, f'item edited successfuly')
			return redirect('partial_sale')

	else:
		return redirect('login')

	context = {
		'transaction' 	  : get_transaction,
		'get_block'       : get_block,
		'partial_sale'    : partial_sale,
	}

	return render(request, 'backend/sale/partial/edit_partial_sale.html', context)

@login_required
def delete_partial_sale(request, pk):

	if request.user.is_authenticated:
		partial_sale_id    = Partial_Sales.objects.get(id=pk)

		if request.method == 'POST':
			partial_sale_id.delete()

			messages.success(request, f'item deleted successfuly')
			return redirect('partial_sale')

	else:
		return redirect('login')

	context = {
		'partial_sale_id' : partial_sale_id,
	}
	return render(request, 'backend/sale/partial/delete_partial_sale.html', context)

@login_required
def debt_repayment(request):

	if request.user.is_authenticated:

		all_debt_repayment = Debt_Repayment.objects.all()

		debt_repayment_USD = 0
		debt_repayment_balance_USD = 0
		debt_repayment_paid_USD = 0

		debt_repayment_SSP = 0
		debt_repayment_balance_SSP = 0
		debt_repayment_paid_SSP = 0

		for i in all_debt_repayment:

			if i.amount_due and i.currency == "USD":
				debt_repayment_USD += i.amount_due  

			if i.amount_due and i.amount_paid and i.currency == "USD":
				debt_repayment_balance_USD = i.amount_due - i.amount_paid 

			if i.amount_due and i.amount_paid and i.currency == "USD":
				debt_repayment_paid_USD += i.amount_paid 


			if i.amount_due and i.currency == "SSP":
				debt_repayment_SSP += i.amount_due  

			if i.amount_due and i.amount_paid and i.currency == "SSP":
				debt_repayment_balance_SSP = i.amount_due - i.amount_paid 

			if i.amount_due and i.amount_paid and i.currency == "SSP":
				debt_repayment_paid_SSP += i.amount_paid 

	else:
		return redirect('login')

	context = {
		'all_debt_repayment' : all_debt_repayment,
		'debt_repayment_USD' : debt_repayment_USD,
		'debt_repayment_balance_USD' : debt_repayment_balance_USD,
		'debt_repayment_paid_USD' : debt_repayment_paid_USD,

		'debt_repayment_SSP' : debt_repayment_SSP,
		'debt_repayment_balance_SSP' : debt_repayment_balance_SSP,
		'debt_repayment_paid_SSP' : debt_repayment_paid_SSP,
	}

	return render(request, 'backend/debt_repayment/debt_repayment_table.html', context)

@login_required
def add_debt_repayment(request):
	currency   = Debt_Repayment.CURRENCY

	if request.user.is_authenticated:

		if request.method == 'POST':
			client_name 	= request.POST['client_name']
			date_sale   	= request.POST['date_sale']
			amount_due  	= request.POST['amount_due']
			amount_paid 	= request.POST['amount_paid']
			currency    	= request.POST['currency']

			balance         = float(amount_paid) - float(amount_due)

			print('>>> Client Name <<<', client_name)
			print('>>> Date of Sale <<<', date_sale)
			print('>>> Amount Due <<<', amount_due)
			print('>>> Amount Paid <<<', amount_paid)
			print('>>> Balance <<<', balance)
			print('>>> Currency <<<', currency)


			Debt_Repayment.objects.create(user=request.user, client_name=client_name, date_of_sale=date_sale, amount_due=amount_due,
				amount_paid=amount_paid, balance=balance, currency=currency)

			messages.success(request, f'item added successfuly')
			return redirect('debt_repayment')

	else:
		return redirect('login')


	context = {
		'currency' : currency,
	}

	return render(request, 'backend/debt_repayment/add_debt_repayment.html', context)

@login_required
def edit_debt_repayment(request, pk):
	currency   = Debt_Repayment.CURRENCY

	if request.user.is_authenticated:
		get_debt_repayment 	= Debt_Repayment.objects.get(id=pk)

		if request.method == 'POST':
			client_name 	= request.POST['client_name']
			date_sale   	= request.POST['date_sale']
			amount_due  	= request.POST['amount_due']
			amount_paid 	= request.POST['amount_paid']
			currency    	= request.POST['currency']
			
			balance         = float(amount_paid) - float(amount_due)

			# print('>>> Client Name <<<', client_name)
			# print('>>> Date of Sale <<<', date_sale)
			# print('>>> Amount Due <<<', amount_due)
			# print('>>> Amount Paid <<<', amount_paid)
			# print('>>> Balance <<<', balance)
			# print('>>> Currency <<<', currency)


			get_debt_repayment.client_name 	= client_name
			get_debt_repayment.date_sale   	= date_sale
			get_debt_repayment.amount_due  	= amount_due
			get_debt_repayment.amount_paid 	= amount_paid
			get_debt_repayment.currency    	= currency
			get_debt_repayment.balance     	= balance
			get_debt_repayment.save()

			messages.success(request, f'item edited successfuly')
			return redirect('debt_repayment')

	else:
		return redirect('login')

	context = {
		'debt_repayment' : get_debt_repayment,
		'currency':currency,
	}
	return render(request, 'backend/debt_repayment/edit_debt_repayment.html', context)

@login_required
def delete_debt_repayment(request, pk):

	if request.user.is_authenticated:
		debt_repayment_id 	= Debt_Repayment.objects.get(id=pk)

		if request.method == 'POST':
			debt_repayment_id.delete()

			messages.success(request, f'item deleted successfuly')
			return redirect('debt_repayment')

	else:
		return redirect('login')

	context = {
		'debt_repayment_id' : debt_repayment_id,
	}
	return render(request, 'backend/debt_repayment/delete_debt_repayment.html', context)

@login_required
def other_income(request):

	if request.user.is_authenticated:


		all_other_income = Other_Incomes.objects.all()

		other_income_SSP = 0
		other_income_USD = 0

		for i in all_other_income:

			if i.amount and i.currency == "SSP":
				other_income_SSP += i.amount - i.discount

			if i.amount and i.currency == "USD":
				other_income_USD += i.amount - i.discount

	else:
		return redirect('login')


	context = {
		'all_other_income' : all_other_income,
		'other_income_SSP' : other_income_SSP,
		'other_income_USD' : other_income_USD,
	}
	return render(request, 'backend/other_income/other_income_table.html', context)

@login_required
def add_other_income(request):

	if request.user.is_authenticated:
		currency = Other_Incomes.CURRENCY

		if request.method == 'POST':
			description = request.POST['description']
			quantity    = request.POST['quantity']
			price       = request.POST['price']
			discount    = request.POST['discount']
			currency    = request.POST['currency']

			get_amount   	= int(quantity) * float(price)
			final_amount 	= float(get_amount) - float(discount)

			# print('>>> Description <<<', description)
			# print('>>> Quantity <<<', quantity)
			# print('>>> Price <<<', price)
			# print('>>> Discount <<<', discount)
			# print('>>> Currency <<<', currency)


			Other_Incomes.objects.create(user=request.user, description=description, quantity=quantity, price=price, discount=discount,
				currency=currency, amount=final_amount)
			messages.success(request, f'item added successfuly')
			return redirect('other_income')

	else:
		return redirect('login')


	context = {
		'currency':currency,
	}
	return render(request, 'backend/other_income/add_other_income.html', context)

@login_required
def edit_other_income(request, pk):

	if request.user.is_authenticated:
		other_income_id = Other_Incomes.objects.get(id=pk)
		other_income    = Other_Incomes.objects.get(id=pk)

		if request.method == 'POST':
			description = request.POST['description']
			quantity    = request.POST['quantity']
			price       = request.POST['price']
			discount    = request.POST['discount']
			currency    = request.POST['currency']

			get_amount   	= int(quantity) * float(price)
			final_amount 	= float(get_amount) - float(discount)

			# print('>>> Description <<<', description)
			# print('>>> Quantity <<<', quantity)
			# print('>>> Price <<<', price)
			# print('>>> Discount <<<', discount)
			# print('>>> Currency <<<', currency)

			other_income.description = description
			other_income.quantity    = quantity
			other_income.price       = price
			other_income.discount    = discount
			other_income.currency    = currency
			other_income.amount      = final_amount
			other_income.save()

			messages.success(request, f'item edited successfuly')
			return redirect('other_income')

	else:
		return redirect('login')

	context = {
		'other_income_id' : other_income_id,
	}

	return render(request, 'backend/other_income/edit_other_income.html', context)

@login_required
def delete_other_income(request, pk):

	if request.user.is_authenticated:
		other_income_id = Other_Incomes.objects.get(id=pk)

		if request.method == 'POST':
			other_income_id.delete()

			messages.success(request, f'item deleted successfuly')
			return redirect('other_income')

	else:
		return redirect('login')

	context = {
		'other_income_id' : other_income_id, 
	}
	return render(request, 'backend/other_income/delete_other_income.html', context)

@login_required
def production(request):

	if request.user.is_authenticated:
		all_production = Production.objects.all()

		get_big_hollow_number 	= 0
		get_small_hollow_number = 0
		get_pavers_number = 0
		get_damages = 0

		for i in all_production:
			if i.block.name == 'Big Hollow' and i.production_number :
				get_big_hollow_number += i.production_number

			if i.block.name == 'Small Hollow' and i.production_number :
				get_small_hollow_number += i.production_number

			if i.block.name == 'Pavers' and i.production_number :
				get_pavers_number += i.production_number

			if i.production_damages  :
				get_damages += i.production_damages
	else:
		return redirect('login')

	context = {
		'all_production' : all_production,
		'get_big_hollow_number' : get_big_hollow_number,
		'get_small_hollow_number' : get_small_hollow_number,
		'get_pavers_number' : get_pavers_number,
		'get_damages' : get_damages,
	}
	return render(request, 'backend/production/production_table.html', context)

@login_required
def add_production(request):

	if request.user.is_authenticated:
		block_type 	= Block_Type.objects.all()

		if request.method == 'POST':
			block_type 			= request.POST['block_type']
			production_number 	= request.POST['production_number']
			bag_of_cement       = request.POST['bag_of_cement']
			unit_price          = request.POST['unit_price']
			production_damages  = request.POST['production_damages']

			
			get_production_amount 		= float(unit_price) * float(production_number)
			final_production_damages 	= float(unit_price) * float(production_damages)

			amount 		= float(get_production_amount) - float(final_production_damages)

			# print('>>> Block Type <<<', block_type)
			# print('>>> Production Number <<<', production_number)
			# print('>>> Bag Of Cement <<<', bag_of_cement)
			# print('>>> Unit Price <<<', unit_price)
			# print('>>> Production Damages <<<', production_damages)
			# print('>>> Production Amount <<<', amount)

			block_type_id 	= Block_Type.objects.get(id=block_type)

			Production.objects.create(user=request.user, block=block_type_id, production_number=production_number,
				production_damages=production_damages, bags_of_cement=bag_of_cement, unit_price=unit_price, amount=amount)

			messages.success(request, f'item added successfuly')
			return redirect('production')

	else:
		return redirect('login')

	context = {
		'block_type' : block_type,
	}
	return render(request, 'backend/production/add_production.html', context)

@login_required
def edit_production(request, pk):

	if request.user.is_authenticated:
		get_production_id 	= Production.objects.get(id=pk)
		block_type 			= Block_Type.objects.all()
		get_production 		= Production.objects.get(id=pk)


		if request.method == 'POST':
			block_type 			= request.POST['block_type']
			production_number 	= request.POST['production_number']
			bag_of_cement       = request.POST['bag_of_cement']
			unit_price          = request.POST['unit_price']
			production_damages  = request.POST['production_damages']

			
			get_production_amount 		= float(unit_price) * float(production_number)
			final_production_damages 	= float(unit_price) * float(production_damages)

			amount 	= float(get_production_amount) - float(final_production_damages)

			# print('>>> Block Type <<<', block_type)
			# print('>>> Production Number <<<', production_number)
			# print('>>> Bag Of Cement <<<', bag_of_cement)
			# print('>>> Unit Price <<<', unit_price)
			# print('>>> Production Damages <<<', production_damages)
			# print('>>> Production Amount <<<', amount)

			block_type_id 	= Block_Type.objects.get(id=block_type)

			get_production.block 					= block_type_id
			get_production.production_number  		= production_number
			get_production.bags_of_cement        	= bag_of_cement
			get_production.unit_price           	= unit_price
			get_production.production_damages   	= production_damages
			get_production.amount                   = amount
			get_production.save()

			messages.success(request, f'item edited successfuly')
			return redirect('production')

	else:
		return redirect('login')


	context = {
		'get_production_id' : get_production_id,
		'block_type' : block_type,
	}

	return render(request, 'backend/production/edit_production.html', context)

@login_required
def delete_production(request, pk):

	if request.user.is_authenticated:
		get_production_id = Production.objects.get(id=pk)

		if request.method == 'POST':
			get_production_id.delete()

			messages.success(request, f'item deleted successfuly')
			return redirect('production')

	else:
		return redirect('login')


	context = {
		'get_production_id' : get_production_id,
	}
	return render(request, 'backend/production/delete_production.html', context)

@login_required
def piling_damages(request):

	if request.user.is_authenticated:

		get_piling_damages = Piling_Damages.objects.all()


		get_big_hollow_damages = 0
		get_small_hollow_damages = 0
		get_pavers_damages = 0

		for i in get_piling_damages:

			if i.block.name == 'Big Hollow' and i.damages :
				get_big_hollow_damages += i.damages

			if i.block.name == 'Small Hollow' and i.damages :
				get_small_hollow_damages += i.damages

			if i.block.name == 'Pavers' and i.damages :
				get_pavers_damages += i.damages

	else:
		return redirect('login')

	context = {
		'get_piling_damages' : get_piling_damages,
		'get_big_hollow_damages' : get_big_hollow_damages,
		'get_small_hollow_damages' : get_small_hollow_damages,
		'get_pavers_damages' : get_pavers_damages,

	}
	return render(request, 'backend/damages/damages_table.html', context)

@login_required
def add_piling_damages(request):

	if request.user.is_authenticated:
		get_block_type 			= Block_Type.objects.all()

		if request.method == 'POST':
			block_type = request.POST['block_type']
			damages    = request.POST['damages']

			# print('>>> Block Type <<<', block_type)
			# print('>>> Damages <<<', damages)

			block_id = Block_Type.objects.get(id=block_type)

			Piling_Damages.objects.create(user=request.user, block=block_id, damages=damages)
			messages.success(request, f'item added successfuly')
			return redirect('piling_damages')

	else:
		return redirect('login')

	context = {
		'block_type' : get_block_type,
	}
	return render(request, 'backend/damages/add_damages.html', context)

@login_required
def edit_piling_damages(request, pk):

	if request.user.is_authenticated:
		get_piling_damages_id   = Piling_Damages.objects.get(id=pk)
		get_block_type 			= Block_Type.objects.all()
		get_piling_damages      = Piling_Damages.objects.get(id=pk)

		if request.method == 'POST':
			block_type = request.POST['block_type']
			damages    = request.POST['damages']

			# print('>>> Block Type <<<', block_type)
			# print('>>> Damages <<<', damages)

			block_id = Block_Type.objects.get(id=block_type)

			get_piling_damages.block_type = block_id
			get_piling_damages.damages    = damages
			get_piling_damages.save()

			messages.success(request, f'item edited successfuly')
			return redirect('piling_damages')

	else:
		return redirect('login')

	context = {
		'block_type' : get_block_type,
		'piling_damages' : get_piling_damages_id,
	}
	return render(request, 'backend/damages/edit_damages.html', context)

@login_required
def delete_piling_damages(request, pk):

	if request.user.is_authenticated:
		get_piling_damages_id   = Piling_Damages.objects.get(id=pk)

		if request.method == 'POST':
			get_piling_damages_id.delete()

			messages.success(request, f'item deleted successfuly')
			return redirect('piling_damages')

	else:
		return redirect('login')

	context = {
		'get_piling_damages_id' : get_piling_damages_id,
	}
	return render(request, 'backend/damages/delete_damages.html', context)

@login_required
def opening_stock(request):

	if request.user.is_authenticated:

		get_opening_stock = Opening_Stock.objects.all()

		get_big_hollow 		= 0
		get_small_hollow 	= 0
		get_pavers 			= 0

		for i in get_opening_stock:

			if i.block.name == 'Big Hollow' and i.quantity :
				get_big_hollow += i.quantity

			if i.block.name == 'Small Hollow' and i.quantity :
				get_small_hollow += i.quantity

			if i.block.name == 'Pavers' and i.quantity :
				get_pavers += i.quantity

	else:
		return redirect('login')

	context = {
		'get_opening_stock'  : get_opening_stock,
		'get_big_hollow' : get_big_hollow,
		'get_small_hollow' : get_small_hollow,
		'get_pavers' : get_pavers,
	}
	return render(request, 'backend/opening_stock/opening_stock_table.html', context)

@login_required
def add_opening_stock(request):

	if request.user.is_authenticated:
		get_block_type 	= Block_Type.objects.all()

		if request.method == 'POST':
			block_type 	= request.POST['block_type']
			quantity    = request.POST['quantity']

			# print('>>> Block Type <<<', block_type)
			# print('>>> Quantity <<<', quantity)

			block_id = Block_Type.objects.get(id=block_type)

			Opening_Stock.objects.create(user=request.user, block=block_id, quantity=quantity)

			messages.success(request, f'item added successfuly')
			return redirect('opening_stock')

	else:
		return redirect('login')

	context = {
		'block_type' : get_block_type,
	}
	return render(request, 'backend/opening_stock/add_opening_stock.html', context)

@login_required
def edit_opening_stock(request, pk):

	if request.user.is_authenticated:
		get_block_type 			= Block_Type.objects.all()
		opening_stock           = Opening_Stock.objects.get(id=pk)

		if request.method == 'POST':
			block_type 	= request.POST['block_type']
			quantity    = request.POST['quantity']

			# print('>>> Block Type <<<', block_type)
			# print('>>> Quantity <<<', quantity)

			block_id = Block_Type.objects.get(id=block_type)
			opening_stock.block = block_id
			opening_stock.quantity = quantity
			opening_stock.save()

			messages.success(request, f'item edited successfuly')
			return redirect('opening_stock')

	else:
		return redirect('login')

	context = {
		'block_type' : get_block_type,
		'opening_stock' : opening_stock,
	}
	return render(request, 'backend/opening_stock/edit_opening_stock.html', context)

@login_required
def delete_opening_stock(request, pk):

	if request.user.is_authenticated:
		opening_stock_id = Opening_Stock.objects.get(id=pk)

		if request.method == 'POST':
			opening_stock_id.delete()

			messages.success(request, f'item deleted successfuly')
			return redirect('opening_stock')

	else:
		return redirect('login')

	context = {
		'opening_stock_id' : opening_stock_id,
	}
	return render(request, 'backend/opening_stock/delete_opening_stock.html', context)


@login_required
def block_type(request):

	if request.user.is_authenticated:
		get_block_types = Block_Type.objects.all()

	else:
		return redirect('login')

	context = {
		'get_block_types' : get_block_types,
	}

	return render(request, 'backend/component/block_type/block_type_table.html', context)

@login_required
def add_block_type(request):

	if request.user.is_authenticated:

		if request.method == 'POST':
			block_type = request.POST['block_type']

			Block_Type.objects.create(name=block_type, user=request.user)
			messages.success(request, f'item added successfuly')
			return redirect('block_type')

	else:
		return redirect('login')

	context = {}
	return render(request, 'backend/component/block_type/add_block_type.html', context)

@login_required
def edit_block_type(request, pk):

	if request.user.is_authenticated:
		block 			= Block_Type.objects.get(id=pk)
		get_block_id 	= Block_Type.objects.get(id=pk)

		if request.method == 'POST':
			get_block = request.POST['block_type']

			block.name = get_block
			block.save()

			messages.success(request, f'item edited successfuly')
			return redirect('block_type')

	else:
		return redirect('login')

	context = {
		'get_block_id' : get_block_id,
	}
	return render(request, 'backend/component/block_type/edit_block_type.html', context)

@login_required
def delete_block_type(request, pk):

	if request.user.is_authenticated:
		block_type_id = Block_Type.objects.get(id=pk)

		if request.method == 'POST':
			block_type_id.delete()

			messages.success(request, f'item deleted successfuly')
			return redirect('block_type')

	else:
		return redirect('login')

	context = {
		'block_type_id' : block_type_id,
	}
	return render(request, 'backend/component/block_type/delete_block_type.html', context)

# @login_required
# def currency(request):

# 	if request.user.is_authenticated:
# 		get_currencys = Currency.objects.all()

# 	else:
# 		return redirect('login')

# 	context = {
# 		'get_currencys' : get_currencys,
# 	}
# 	return render(request, 'backend/component/currency/currency_table.html', context)

# @login_required
# def add_currency(request):

# 	if request.user.is_authenticated:

# 		if request.method == 'POST':
# 			get_currency = request.POST['currency']

# 			Currency.objects.create(name=get_currency, user=request.user)
			
# 			messages.success(request, f'item added successfuly')
# 			return redirect('currency')

# 	else:
# 		return redirect('login')

# 	context = {}
# 	return render(request, 'backend/component/currency/add_currency.html', context)


# @login_required
# def edit_currency(request, pk):

# 	if request.user.is_authenticated:
# 		currency 		= Currency.objects.get(id=pk)
# 		currency_id 	= Currency.objects.get(id=pk)

# 		if request.method == 'POST':
# 			get_currency = request.POST['currency']

# 			currency.name = get_currency
# 			currency.save()
			
# 			messages.success(request, f'item edited successfuly')
# 			return redirect('currency')

# 	else:
# 		return redirect('login')

# 	context = {
# 		'currency_id' : currency_id,
# 	}

# 	return render(request, 'backend/component/currency/edit_currency.html', context)

# @login_required
# def delete_currency(request, pk):

# 	if request.user.is_authenticated:
# 		currency_id = Currency.objects.get(id=pk)

# 		if request.method == 'POST':
# 			currency_id.delete()

# 			messages.success(request, f'item deleted successfuly')
# 			return redirect('currency')

# 	else:
# 		return redirect('login')

# 	context = {
# 		'currency_id' : currency_id,
# 	}
# 	return render(request, 'backend/component/currency/delete_currency.html', context)


@login_required
def particulars_list(request):

	if request.user.is_authenticated:
		particulars = Particulars.objects.all()

	else:
		return redirect('login')

	context = {
		'particulars' : particulars,
	}
	return render(request, 'backend/component/particulars/particulars_table.html', context)

@login_required
def add_particulars(request):

	if request.user.is_authenticated:

		if request.method == 'POST':
			particular = request.POST['particular']

			Particulars.objects.create(name=particular, user=request.user)

			messages.success(request, f'item added successfuly')
			return redirect('particulars')

	else:
		return redirect('login')

	context = {}
	return render(request, 'backend/component/particulars/add_particulars.html', context)

@login_required
def edit_particulars(request, pk):

	if request.user.is_authenticated:
		particular 		= Particulars.objects.get(id=pk)
		particular_id 	= Particulars.objects.get(id=pk)

		if request.method == 'POST':
			get_particular = request.POST['particular']

			particular.name = get_particular
			particular.save()
			
			messages.success(request, f'item edited successfuly')
			return redirect('particulars')

	else:
		return redirect('login')

	context = {
		'particular_id' : particular_id,
	}
	return render(request, 'backend/component/particulars/edit_particulars.html', context)

@login_required
def delete_particulars(request, pk):

	if request.user.is_authenticated:
		particular = Particulars.objects.get(id=pk)

		if request.method == 'POST':
			particular.delete()

			messages.success(request, f'item deleted successfuly')
			return redirect('particulars')

	else:
		return redirect('login')

	context = {
		'particular' : particular,
	}
	return render(request, 'backend/component/particulars/delete_particulars.html', context)


def transaction_type(request):

	if request.user.is_authenticated:
		get_transaction = Transaction_Type.objects.all()

	else:
		return redirect('login')

	context = {
		'get_transaction' : get_transaction,
	}
	return render(request, 'backend/component/transaction_type/transaction_type_table.html', context)

def add_transaction_type(request):
	
	if request.user.is_authenticated:
		
		if request.method == 'POST':
			get_transaction = request.POST['transaction_type']

			Transaction_Type.objects.create(name=get_transaction, user=request.user)

			messages.success(request, f'item added successfuly')
			return redirect('transaction_type')

	else:
		return redirect('login')

	context = {}
	return render(request, 'backend/component/transaction_type/add_transaction_type.html', context)

def edit_transaction_type(request, pk):

	if request.user.is_authenticated:
		transaction_type 	= Transaction_Type.objects.get(id=pk)
		transaction_type_id = Transaction_Type.objects.get(id=pk)
		
		if request.method == 'POST':
			get_transaction = request.POST['transaction_type']

			transportation_type.user 	= request.user
			transaction_type.name 		= get_transaction
			transaction_type.save()

			messages.success(request, f'item updated successfuly')
			return redirect('transaction_type')

	else:
		return redirect('login')

	context = {
		'transaction_type_id' : transaction_type_id,
	}
	return render(request, 'backend/component/transaction_type/edit_transaction_type.html', context)

def delete_transaction_type(request, pk):

	if request.user.is_authenticated:
		transaction_type_id = Transaction_Type.objects.get(id=pk)
		
		if request.method == 'POST':
			transaction_type_id.delete()

			messages.success(request, f'item deleted successfuly')
			return redirect('transaction_type')

	else:
		return redirect('login')

	context = {
		'transaction_type_id' : transaction_type_id,
	}

	return render(request, 'backend/component/transaction_type/delete_transaction_type.html', context)



def transportation_type(request):

	if request.user.is_authenticated:
		transportation_type = Transportation_Type.objects.all()

	else:
		return redirect('login')

	context = {
		'transportation_type' : transportation_type,
	}

	return render(request, 'backend/component/transportation_type/transportation_type_table.html', context)


def add_transportation_type(request):

	if request.user.is_authenticated:
		
		if request.method == 'POST':
			get_transportation_type = request.POST['transportation_type']

			Transportation_Type.objects.create(name=get_transportation_type, user=request.user)

			messages.success(request, f'item added successfuly')
			return redirect('transportation_type')

	else:
		return redirect('login')

	context = {
		'transportation_type' : transportation_type,
	}

	return render(request, 'backend/component/transportation_type/add_transportation_type.html', context)
	

def edit_transportation_type(request, pk):

	if request.user.is_authenticated:
		transportation_type 	= Transportation_Type.objects.get(id=pk)
		
		if request.method == 'POST':
			get_transportation_type = request.POST['transportation_type']

			transportation_type.name = get_transportation_type
			transportation_type.save()
			
			messages.success(request, f'item edited successfuly')
			return redirect('transportation_type')

	else:
		return redirect('login')


	context = {
		'transportation_type' : transportation_type,
	}
	return render(request, 'backend/component/transportation_type/edit_transportation_type.html', context)

def delete_transportation_type(request, pk):

	if request.user.is_authenticated:
		transportation_type 	= Transportation_Type.objects.get(id=pk)
		
		if request.method == 'POST':
			transportation_type.delete()
			
			messages.success(request, f'item deleted successfuly')
			return redirect('transportation_type')

	else:
		return redirect('login')

	context = {
		'transportation_type' : transportation_type,
	}
	return render(request, 'backend/component/transportation_type/delete_transportation_type.html', context)


@login_required
def unit(request):

	if request.user.is_authenticated:
		units = Unit.objects.all()

	else:
		return redirect('login')

	context = {
		'units' : units,
	}
	return render(request, 'backend/component/unit/unit_table.html', context)

@login_required
def add_unit(request):
	
	if request.user.is_authenticated:
		
		if request.method == 'POST':
			gt_unit = request.POST['unit']

			Unit.objects.create(name=gt_unit, user=request.user)
			messages.success(request, f'item added successfuly')
			return redirect('unit')

	else:
		return redirect('login')

	context = {}
	return render(request, 'backend/component/unit/add_unit.html', context)

def edit_unit(request, pk):

	if request.user.is_authenticated:
		get_unit 	= Unit.objects.get(id=pk)
		unit_id 	= Unit.objects.get(id=pk)

		
		if request.method == 'POST':
			gt_unit = request.POST['unit']

			get_unit.name = gt_unit 
			get_unit.save()

			messages.success(request, f'item edited successfuly')
			return redirect('unit')

	else:
		return redirect('login')

	context = {
		'unit_id' : unit_id,
	}

	return render(request, 'backend/component/unit/edit_unit.html', context)

def delete_unit(request, pk):
	
	if request.user.is_authenticated:
		unit_id = Unit.objects.get(id=pk)

		if request.method == 'POST':
			unit_id.delete()

			messages.success(request, f'item deleted successfuly')
			return redirect('unit')

	else:
		return redirect('login')

	context = {
		'unit_id' : unit_id,
	}
	return render(request, 'backend/component/unit/delete_unit.html', context)


def income_statement(request):
	context = {}
	return render(request, 'backend/report/income_statement.html', context)

def profit_loss(request):
	context = {}
	return render(request, 'backend/report/profit_loss.html', context)

def charts(request):
	context = {}
	return render(request, 'backend/report/charts.html', context)