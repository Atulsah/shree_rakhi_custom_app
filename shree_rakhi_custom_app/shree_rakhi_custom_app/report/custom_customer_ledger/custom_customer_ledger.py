# Copyright (c) 2024, Atul Sah and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
	
	data=[]
	data = get_data(filters)
	columns = get_columns()

	return columns, data

def get_data(filters):
	return frappe.db.sql("""
		SELECT 
			inv.name, inv.customer, inv.customer_name, inv.custom_number_of_carton, 
			inv.base_total, inv.additional_discount_percentage, inv.discount_amount, 
			inv.rounded_total, sum(per.allocated_amount) as allocated, min(per.outstanding_amount) as outstanding
		FROM 
			`tabSales Invoice` inv 
		LEFT JOIN 
			`tabPayment Entry Reference` per
		ON 
			per.reference_name = inv.name
		WHERE 
			inv.posting_date BETWEEN %(from_date)s and %(to_date)s and 
			inv.docstatus=1 {itm_conditions} 
		group by
			inv.name, inv.customer, inv.customer_name, inv.custom_number_of_carton, 
			inv.base_total, inv.additional_discount_percentage, inv.discount_amount
		order by 
			customer_name, name Asc""".format(itm_conditions=get_item_conditions(filters)),
			{'from_date':filters.from_date,'to_date':filters.to_date,
			'customer':filters.customer},as_dict=1)
					  


def get_item_conditions(filters):
	conditions = []
	if filters.get("customer"):
		conditions.append("inv.customer=%(customer)s")	

	return "and {}".format(" and ".join(conditions)) if conditions else ""				




#Add columns in report
def get_columns():
	columns = [{
		"fieldname": "customer_name",
		"label": _("Customer"),  
		"fieldtype": "Link",
		"options": "Customer",
		"width": 150
	}]
	columns.append({
		"fieldname": "name",
		"label": _("Invoice No"),
		"fieldtype": "Link",
		"options": "Sales Invoice",
		"width": 200
	})
	columns.append({
		"fieldname": "custom_number_of_carton",
		"label": _("Cases"),
		"fieldtype": "Data",
		"width": 100
	})
	columns.append({
		"fieldname": "base_total",
		"label": _("Gross Amount"),
		"fieldtype": "Data",
		"width": 150
	})
	columns.append({
		"fieldname": "additional_discount_percentage",
		"label": _("Discount Pencent"),
		"fieldtype": "Data",
		"width": 100
	})
	columns.append({
		"fieldname": "discount_amount",
		"label": _("Discount"),
		"fieldtype": "Data",
		"width": 100
	})
	columns.append({
		"fieldname": "rounded_total",
		"label": _("Net Amount"),
		"fieldtype": "Data",
		"width": 100
	})
	columns.append({
		"fieldname": "allocated",
		"label": _("Amount Paid"),
		"fieldtype": "Data",
		"width": 100
	})
	columns.append({
		"fieldname": "outstanding",
		"label": _(" Outstanding Amount"),
		"fieldtype": "Data",
		"width": 100
	})

		
	return columns	


