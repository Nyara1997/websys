from django.forms import ModelForm
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from . models import *
from django.contrib import admin

class createUser_Form(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','email','password1','password2']


class Maintenance_Expense_List_Variant(admin.TabularInline):
	model = Maintenance_Expense_List

class Maintenance_form(ModelForm):
	class Meta:
		model = Maintenance
		fields = '__all__'
		inlines = [Maintenance_Expense_List_Variant]