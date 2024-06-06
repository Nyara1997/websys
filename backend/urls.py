from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_user, name='login'),
    path('user-reset_password/', views.user_reset_password, name='user_reset_password'),
    path('user-register/', views.user_register, name='user_register'),
    path('user-lists/', views.user_lists, name='user_lists'),
    path('logout/', views.logout_view, name="logout"),


    path('cost-production/', views.cost_of_production, name='cost_production' ),
    path('add-cost-production/', views.add_cost_of_production, name='add_cost_production' ),
    path('edit-cost-production/<str:pk>/', views.edit_cost_of_production, name='edit_cost_production' ),
    path('delete-cost-production/<str:pk>/', views.delete_cost_of_production, name='delete_cost_production'),
    path('cost-production-status/<str:pk>/', views.cost_of_production_status, name='cost_of_production_status'),
    path('cost-production-report/', views.cost_of_production_report, name='cost_production_report'),
    path('cost-production-report-ssp/', views.cost_of_production_report_ssp, name='cost_production_report_ssp'),
    path('cost-production-report-usd/', views.cost_of_production_report_usd, name='cost_production_report_usd'),

    path('pdf_view/<str:pk>/', views.ViewPDF, name="pdf_view"),

    path('maintenance/', views.maintenance, name='maintenance'),
    path('add-maintenance/', views.add_maintenance, name='add_maintenance'),
    path('edit-maintenance/<str:pk>/', views.edit_maintenance, name='edit_maintenance'),
    path('delete-maintenance/<str:pk>/', views.delete_maintenance, name='delete_maintenance'),
    path('maintenance-status/<str:pk>/', views.maintenance_status, name='maintenance_status'),
    path('maintenance-report/', views.maintenance_report, name='maintenance_report'),
    path('maintenance-report-routine-usd/', views.maintenance_report_routine_usd, name='maintenance_report_routine_usd'),
    path('maintenance-report-routine-ssp/', views.maintenance_report_routine_ssp, name='maintenance_report_routine_ssp'),
    path('maintenance-report-breakdown-usd/', views.maintenance_report_breakdown_usd, name='maintenance_report_breakdown_usd'),
    path('maintenance-report-breakdown-ssp/', views.maintenance_report_breakdown_ssp, name='maintenance_report_breakdown_ssp'),

    path('fixed-cost/', views.fixed_cost, name='fixed_cost'),
    path('add-fixed-cost/', views.add_fixed_cost, name='add_fixed_cost'),
    path('edit-fixed-cost/<str:pk>/', views.edit_fixed_cost, name='edit_fixed_cost'),
    path('delete-fixed-cost/<str:pk>/', views.delete_fixed_cost, name='delete_fixed_cost'),
    path('fixed-cost-report/', views.fixed_cost_report, name='fixed_cost_report'),
    path('fixed-cost-report-ssp/', views.fixed_cost_report_ssp, name='fixed_cost_report_ssp'),
    path('fixed-cost-report-usd/', views.fixed_cost_report_usd, name='fixed_cost_report_usd'),
    path('fixed-cost-status/<str:pk>/', views.fixed_cost_status, name='fixed_cost_status'),

    path('material-transportation/', views.material_transportation, name='material_transportation'),
    path('add-material-transportation/', views.add_material_transportation, name='add_material_transportation'),
    path('edit-material-transportation/<str:pk>/', views.edit_material_transportation, name='edit_material_transportation'),
    path('delete-material-transportation/<str:pk>/', views.delete_material_transportation, name='delete_material_transportation'),
    path('material-transportation-report/', views.material_transportation_report, name='material_transportation_report'),
    path('material-transportation-report-ssp/', views.material_transportation_report_ssp, name='material_transportation_report_ssp'),
    path('material-transportation-report-usd/', views.material_transportation_report_usd, name='material_transportation_report_usd'),
    path('material-transportation-status/<str:pk>/', views.material_transportation_status, name='material_transportation_status'),

    path('block-transportation/', views.block_transportation, name='block_transportation'),
    path('add-block-transportation/', views.add_block_transportation, name='add_block_transportation'),
    path('edit-block-transportation/<str:pk>/', views.edit_block_transportation, name='edit_block_transportation'),
    path('delete-block-transportation/<str:pk>/', views.delete_block_transportation, name='delete_block_transportation'),

    path('other-transportation/', views.other_transportation, name='other_transportation'),
    path('add-other-transportation/', views.add_other_transportation, name='add_other_transportation'),
    path('edit-other-transportation/<str:pk>/', views.edit_other_transportation, name='edit_other_transportation'),
    path('delete-other-transportation/<str:pk>/', views.delete_other_transportation, name='delete_other_transportation'),
    path('other-transportation-status/<str:pk>/', views.other_transportation_status, name='other_transportation_status'),
    path('other-transportation-report/', views.other_transportation_report, name='other_transportation_report'),
    path('other-transportation-report-usd/', views.other_transportation_report_usd, name='other_transportation_report_usd'),
    path('other-transportation-report-ssp/', views.other_transportation_report_ssp, name='other_transportation_report_ssp'),

    path('other-expenses/', views.other_expenses, name='other_expenses'),
    path('add-other-expenses/', views.add_other_expenses, name='add_other_expenses'),
    path('edit-other-expenses/<str:pk>/', views.edit_other_expenses, name='edit_other_expenses'),
    path('delete-other-expenses/<str:pk>/', views.delete_other_expenses, name='delete_other_expenses'),
    path('other-expenses-status/<str:pk>/', views.other_expenses_status, name='other_expenses_status'),
    path('other-expenses-report/', views.other_expenses_report, name='other_expenses_report'),
    path('other-expenses-report-ssp/', views.other_expenses_report_ssp, name='other_expenses_report_ssp'),
    path('other-expenses-report-usd/', views.other_expenses_report_usd, name='other_expenses_report_usd'),

    path('sale/', views.sale, name='sale'),
    path('add-sale/', views.add_sale, name='add_sale'),
    path('edit-sale/<str:pk>/', views.edit_sale, name='edit_sale'),
    path('delete-sale/<str:pk>/', views.delete_sale, name='delete_sale'),

    path('partial-sale/', views.partial_sale, name='partial_sale'),
    path('add-partial-sale/', views.add_partial_sale, name='add_partial_sale'),
    path('edit-partial-sale/<str:pk>/', views.edit_partial_sale, name='edit_partial_sale'),
    path('delete-partial-sale/<str:pk>/', views.delete_partial_sale, name='delete_partial_sale'),

    path('debt-repayment/', views.debt_repayment, name='debt_repayment'),
    path('add-debt-repayment/', views.add_debt_repayment, name='add_debt_repayment'),
    path('edit-debt-repayment/<str:pk>/', views.edit_debt_repayment, name='edit_debt_repayment'),
    path('delete-debt-repayment/<str:pk>/', views.delete_debt_repayment, name='delete_debt_repayment'),

    path('other-income/', views.other_income, name='other_income'),
    path('add-other-income/', views.add_other_income, name='add_other_income'),
    path('edit-other-income/<str:pk>/', views.edit_other_income, name='edit_other_income'),
    path('delete-other-income/<str:pk>/', views.delete_other_income, name='delete_other_income'),

    path('production/', views.production, name='production'),
    path('add-production/', views.add_production, name='add_production'),
    path('edit-production/<str:pk>/', views.edit_production, name='edit_production'),
    path('delete-production/<str:pk>/', views.delete_production, name='delete_production'),

    path('piling-damages/', views.piling_damages, name='piling_damages'),
    path('add-piling-damages/', views.add_piling_damages, name='add_piling_damages'),
    path('edit-piling-damages/<str:pk>/', views.edit_piling_damages, name='edit_piling_damages'),
    path('delete-piling-damages/<str:pk>/', views.delete_piling_damages, name='delete_piling_damages'),

    path('opening-stock/', views.opening_stock, name='opening_stock'),
    path('add-opening-stock/', views.add_opening_stock, name='add_opening_stock'),
    path('edit-opening-stock/<str:pk>/', views.edit_opening_stock, name='edit_opening_stock'),
    path('delete-opening-stock/<str:pk>/', views.delete_opening_stock, name='delete_opening_stock'),


    path('block-type/', views.block_type, name='block_type'),
    path('add-block-type/', views.add_block_type, name='add_block_type'),
    path('edit-block-type/<str:pk>/', views.edit_block_type, name='edit_block_type'),
    path('delete-block-type/<str:pk>/', views.delete_block_type, name='delete_block_type'),

    # path('currency/', views.currency, name='currency'),
    # path('add-currency/', views.add_currency, name='add_currency'),
    # path('edit-currency/<str:pk>/', views.edit_currency, name='edit_currency'),
    # path('delete-currency/<str:pk>/', views.delete_currency, name='delete_currency'),

    path('particulars/', views.particulars_list, name='particulars'),
    path('add-particulars/', views.add_particulars, name='add_particulars'),
    path('edit-particulars/<str:pk>/', views.edit_particulars, name='edit_particulars'),
    path('delete-particulars/<str:pk>/', views.delete_particulars, name='delete_particulars'),

    path('transaction-type/', views.transaction_type, name='transaction_type'),
    path('add-transaction_type/', views.add_transaction_type, name='add_transaction_type'),
    path('edit-transaction-type/<str:pk>/', views.edit_transaction_type, name='edit_transaction_type'),
    path('delete-transaction-type/<str:pk>/', views.delete_transaction_type, name='delete_transaction_type'),

    path('unit/', views.unit, name='unit'),
    path('add-unit/', views.add_unit, name='add_unit'),
    path('edit-unit/<str:pk>/', views.edit_unit, name='edit_unit'),
    path('delete-unit/<str:pk>/', views.delete_unit, name='delete_unit'),

    path('transportation-type/', views.transportation_type, name='transportation_type'),
    path('add-transportation-type/', views.add_transportation_type, name='add_transportation_type'),
    path('edit-transportation-type/<str:pk>/', views.edit_transportation_type, name='edit_transportation_type'),
    path('delete-transportation-type/<str:pk>/', views.delete_transportation_type, name='delete_transportation_type'),

    path('income-statement/', views.income_statement, name='income_statement'),
    path('profit-and-loss/', views.profit_loss, name='profit_loss'),
    path('charts-report/', views.charts, name="charts"),
  
]
