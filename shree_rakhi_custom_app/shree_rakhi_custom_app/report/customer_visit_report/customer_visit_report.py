# Copyright (c) 2024, Atul Sah and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
#import pandas as pd

def execute(filters=None):
	columns = get_columns()
	data=[]
	data = get_data(filters)
	"""
		if len(data) == 0:
			frappe.msgprint('No data!!!')
			return [], []
		else:
			dataframe = pd.DataFrame.from_records(data)
			data = dataframe.reset_index().to_dict('records')
	"""
	return columns, data

def get_data(filters):
	return frappe.db.sql("""select date, customer, customer_name, time_of_visit from `tabCustomer Visit` \
		WHERE date BETWEEN %(from_date)s and %(to_date)s and docstatus=1 {itm_conditions} order by date \
		Asc""".format(itm_conditions=get_item_conditions(filters)),{'from_date':filters.from_date,'to_date':filters.to_date,'customer':filters.customer},as_dict=1) 


def get_item_conditions(filters):
	conditions = []
	if filters.get("customer"):
		conditions.append("customer=%(customer)s")	

	return "and {}".format(" and ".join(conditions)) if conditions else ""															

#Add columns in report
def get_columns():
	columns = [{
		"fieldname": "customer",
		"label": _("Customer"),  
		"fieldtype": "Link",
		"options": "Customer",
		"width": 100

	}]
	columns.append({
		"fieldname": "date",
		"label": _("Date"),
		"fieldtype": "Date",
		"width": 100
	})	
	columns.append({
		"fieldname": "customer_name",
		"label": _("Customer Name"),
		"fieldtype": "Data",
		"width": 100
	})
	columns.append({
		"fieldname": "time_of_visit",
		"label": _("Time of Visit"),
		"fieldtype": "Data",
		"width": 100
	})
	
	return columns	
