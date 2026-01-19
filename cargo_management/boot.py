import frappe

def extend_bootinfo(bootinfo):
	carriers = frappe.get_all('Carrier', fields=['name', 'api'])

	print(carriers)

	bootinfo.carriers = carriers
