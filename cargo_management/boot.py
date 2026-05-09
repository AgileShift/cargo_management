import frappe


def boot_session(bootinfo):
	# Build carriers and their tracking URLs

	carrier = frappe.qb.DocType('Carrier')
	carrier_urls = frappe.qb.DocType('Carrier Tracking URL')

	query = (
		frappe.qb.from_(carrier)
		.left_join(carrier_urls)
		.on(carrier.name == carrier_urls.parent)
		.select(
			carrier.name, carrier.api, carrier.regex,
			carrier_urls.idx, carrier_urls.label, carrier_urls.url, carrier_urls.type
		).orderby(carrier_urls.idx)
	).run(as_dict=True)

	carriers = {}
	for carrier in query:
		carrier_name = carrier['name']

		carriers.setdefault(
			carrier_name,
			{
				'api': carrier['api'],
				'regex': carrier['regex'],
				'tracking_urls': []
			}
		)

		if url := carrier.get('url'):  # Carrier Tracking URL
			carriers[carrier_name]['tracking_urls'].append({
				'idx': carrier.get('idx'),
				'label': carrier.get('label'),
				'url': url,
				'type': carrier.get('type')
			})

	bootinfo.carriers = carriers
