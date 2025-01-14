# Copyright (c) 2025, BOT Solutions and Contributors

import frappe

def after_install():
    createRetentionsAndDeductionsAccount()


def createRetentionsAndDeductionsAccount():
    print("creating Deductions and Retentions Account......")
    company = frappe.get_all("Company", fields=["name", "abbr"])

    if not company:
        print("No company exists to create the account.")
        return

    for comp in company:
        parent_account = f"Indirect Expenses - {comp.abbr}"
        try:
            account_doc = frappe.get_doc({
                "doctype": "Account",
                "root_type": "Expense",
                "account_name": "Deductions And Retentions",
                "parent_account": parent_account,
                "freeze_account": "No",
                "is_group": 0,
                "company": comp.get("name"),
            })

            account_doc.insert(ignore_permissions=True)
            print(f"Account 'Deductions And Retentions' created successfully for company: {comp.name}")
        except Exception as e:
            print(f"Failed to create account for company {comp.name}")

    frappe.db.commit()
