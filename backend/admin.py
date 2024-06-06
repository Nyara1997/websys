from django.contrib import admin
from . models import *
from django.contrib.auth.admin import UserAdmin


class Cost_of_Production_Admin_Display(admin.ModelAdmin):
	list_display = ['particulars', 'quantity','unit','currency','unit_price','discount','amount','pub_date']


class FixedCost_Admin_Display(admin.ModelAdmin):
	list_display = ['fixed_cost','quantity','unit','currency','unit_price','amount']

class Transportation_Cost_Detail_VariantInline(admin.TabularInline):
	model = Transportation_Cost_Detail


# class Block_Transportation_Admin_Display(admin.ModelAdmin):
# 	list_display = ['transportation_type','block','currency','quantity','transportation_damages','amount']


class Block_Variant(admin.ModelAdmin):
	list_display = ['transportation_type','block','currency','quantity','transportation_damages','amount']
	inlines = [Transportation_Cost_Detail_VariantInline]



class Maintenance_Expense_List_Variant(admin.TabularInline):
	model = Maintenance_Expense_List

class Sub_Maintenance_List(admin.ModelAdmin):
	list_display = ['maintenance_type','amount']
	inlines = [Maintenance_Expense_List_Variant]



# Register your models here.
admin.site.register(Particulars)
admin.site.register(Unit)
admin.site.register(Cost_Of_Production, Cost_of_Production_Admin_Display)
admin.site.register(Maintenance_Type)
admin.site.register(Maintenance, Sub_Maintenance_List)
admin.site.register(Fixed_Cost, FixedCost_Admin_Display)
admin.site.register(Transportation_Type)
admin.site.register(Block_Type)
admin.site.register(Cost_Type)
admin.site.register(Block_Transportation, Block_Variant)
admin.site.register(Other_Transportation)
admin.site.register(Other_Expenses)
admin.site.register(Transaction_Type)
admin.site.register(Sales)
admin.site.register(Partial_Sales)
admin.site.register(Debt_Repayment)
admin.site.register(Other_Incomes)
admin.site.register(Production)
admin.site.register(Piling_Damages)
admin.site.register(Opening_Stock)
admin.site.register(Material_Transportation)
admin.site.register(UserAccount)
admin.site.register(Transportation_Cost_Detail)
admin.site.register(Maintenance_Expense_List)






