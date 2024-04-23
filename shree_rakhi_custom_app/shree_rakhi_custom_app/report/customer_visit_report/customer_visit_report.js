// Copyright (c) 2024, Atul Sah and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Visit Report"] = {
	"filters": [
        {
            fieldname: "customer",
            label: __("Customer"),
            fieldtype: "Link",
            reqd: 0,
            options : 'Customer',

          },
          {
            fieldname: "from_date",
            label: __("From date"),
            fieldtype: "Date",
            reqd: 0,
          },
          {
            fieldname: "to_date",
            label: __("To date"),
            fieldtype: "Date",
            reqd: 0,
          },

    ]
};
