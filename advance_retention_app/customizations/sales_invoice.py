import frappe
from frappe import _
from frappe.utils import money_in_words

@frappe.whitelist()
def get_advance_sales_invoices(customer, invoice_type):
	if not customer:
		frappe.throw(_("Customer is required to fetch invoices"))

	if not invoice_type:
		frappe.throw(_("Invoice Type is required to fetch invoices"))
	
	sales_invoices = frappe.get_all('Sales Invoice', 
        filters={
            'customer': customer,
            'invoice_type': invoice_type,
            'docstatus': 1,
            'outstanding_amount': ['>', 0]
        },
        fields=['name', 'grand_total', 'total']
    )

	filtered_invoices = []
	for invoice in sales_invoices:
		allocated_sum = 0
		advance_money = 0;
		advance_payments = frappe.get_all('Advance Payments', 
        	filters={
            	'reference_name': invoice.name,
				'which_invoice' : 'sales_invoice',
        	},
        	fields=['reference_name', 'advance_amount', 'allocated']
    	)

		for advance_payment in advance_payments:
			allocated_sum += advance_payment.allocated
			advance_money = advance_payment.advance_amount

		if advance_money == 0:
			advance_money = invoice.grand_total

		remaining_advance = advance_money - allocated_sum
		invoice['remaining_advance'] = remaining_advance
        			
		# invoice['remaining_advance'] = advance_money - allocated_sum
		if remaining_advance > 0:
			tax_details = frappe.db.get_value('Sales Taxes and Charges', {'parent': invoice.name}, ['SUM(tax_amount)', 'rate'], as_dict=True)
		
			if tax_details:
				invoice['tax_amount'] = tax_details.get('SUM(tax_amount)', 0)
				invoice['rate'] = tax_details.get('rate', 0)
			else:
				invoice['tax_amount'] = 0
				invoice['rate'] = 0

			filtered_invoices.append(invoice)	
			
	return filtered_invoices


@frappe.whitelist()
def get_amount_in_english(amount_to_be_in_words, currency):
	if not amount_to_be_in_words:
		frappe.throw(_("Net Amount Due is Required"))

	amount = abs(float(amount_to_be_in_words))
	
	in_words = money_in_words(amount, currency if currency else "USD")
	
	currency_abbr = currency + " " if currency else ""
	
	return in_words.replace(currency_abbr, "", 1).strip()