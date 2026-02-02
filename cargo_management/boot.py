import frappe


def boot_session(bootinfo):
	# Build carriers and their tracking URLs

	carrier = frappe.qb.DocType('Carrier')
	carrier_urls = frappe.qb.DocType('Carrier Tracking URL')

	query = (
		frappe.qb.from_(carrier)
		.left_join(carrier_urls)
		.on(carrier.name == carrier_urls.parent)
		.select(carrier.name, carrier.api, carrier.regex, carrier_urls.label, carrier_urls.url)
		.run(as_dict=True)
	)

	carriers = {}
	for carrier in query:
		name = carrier['name']

		carriers.setdefault(
			name,
			{
				'api': carrier['api'],
				'regex': carrier['regex'],
				'tracking_urls': []
			}
		)

		if url := carrier.get('url'):  # Carrier Tracking URL
			carriers[name]['tracking_urls'].append({
				'label': carrier.get('label'),
				'url': url
			})

	bootinfo.carriers = carriers
