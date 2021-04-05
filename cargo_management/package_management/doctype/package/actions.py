import frappe

""" API Methods to communicate with the model that holds our business logic. """


@frappe.whitelist()
def update_data_from_carrier(doc):
    """ Used as Action button in Doctype: Fetch new data from carrier if we can track and update the doc if its open """
    doc = frappe.parse_json(doc)
    package = frappe.get_doc('Package', doc.get('name'))

    # Verify if we can track, because .save() will update doc, even if we can't track. Then we would have to reload doc.
    if package.can_track():
        package.flags.requested_to_track = True  # Set bypass flag ON. See Package Doctype flags. Go directly to track.
        package.save()  # Trigger before_save() who checks for the bypass flag. We avoid revalidation checks.

    return {}  # FIX: To prevent reload_doc being called twice by: execute_action() called if using "Server Action"


@frappe.whitelist()
def update_data_from_carrier_bulk(names):
    # TODO: FINISH
    names = frappe.parse_json(names)

    # for name in names:
    #     update_data_from_carrier({
    #         'name': name
    #     })


@frappe.whitelist()
@frappe.read_only()
def get_carrier_detail_page_url(carrier: str):
    """ Util: Return the carrier detail page URL to append to a tracking number. Used in a Form Action Button """
    return \
        frappe.get_value('Package Carrier', carrier, 'carrier_detail_page_url', cache=True) or \
        frappe.db.get_single_value('Package Settings', 'default_carrier_detail_page_url', cache=True) # TODO: get_cached_doc?


@frappe.whitelist()
@frappe.read_only()
def get_explained_status(source_name: str):
    """ Util: Return explained status message from doc object """
    return frappe.get_doc('Package', source_name, cache=True).get_explained_status()  # TODO: get_cached_doc?


""" API Methods  to communicate with Package Doctype from Third Party Doctypes """


@frappe.whitelist()
def update_status(source_doc: str, action: str):
    """ Used as Action Button in Doctype. The Logic is related to work around Package Doctype and related Doctypes """
    doc = frappe.parse_json(source_doc)  # doc from which is requested the update

    print(doc.get('warehouse_receipt_lines'))

    frappe.flags.mute_emails = frappe.flags.in_import = doc.mute_emails  # Core: Silence all notifications and emails!

    def _get_doc_names_from_child_table(child_lines, link_field):
        return list(map(lambda child_line: child_line.get(link_field), child_lines))

    def _normalize_name(name):
        return name.replace('_', ' ').title()  # Make a more readable name

    def _docs_to_update(parent_doc_lines, options):
        for line in parent_doc_lines:
            package = frappe.get_doc('Package', line.get('package'))  # Getting Package Doc from Parent Doc Line

            if package.change_status(options['package']['new_status']):  # If status can be changed. Prevent unnecessary updates
                doctypes_to_update['package']['updated'] += 1
                package.flags.ignore_validate = True  # Set flag ON because Doc will be saved from bulk edit. No validations
                # package.save(ignore_permissions=True)  # Trigger before_save() who checks for the flag. We avoid all checks.

    if doc.doctype == 'Warehouse Receipt':
        if action == 'confirm_packages':  # If request is to confirm packages in Warehouse Receipt Doctype
            doctypes_to_update = {
                'Package': {
                    'new_status': 'Awaiting Departure',
                    'doc_names': doc.get('warehouse_receipt_lines'),
                    'child_doc_link_field': 'package',
                    'updated': 0
                }
            }
    elif doc.doctype == 'Cargo Shipment':
        if action == 'confirm_transit':  # If request is to confirm transit of warehouse receipt
            doctypes_to_update = {
                # 'Cargo Shipment': {
                #     'new_status': 'In Transit',
                #     'child_doc_lines': doc.get('cargo_shipment_lines'),
                # },
                'Warehouse Receipt': {
                    'new_status': 'In Transit',
                    'doc_names': doc.get('cargo_shipment_lines'),
                    'updated': 0
                },
                'Package': {
                    'new_status': 'In Transit',
                    'doc_names': doc.get('cargo_shipment_lines'),  # TODO: Gather this data!!
                    'updated': 0,
                }
            }
    elif doc.doctype == 'Cargo Shipment Receipt':
        doctypes_to_update = {}

    # Make the actual update data
    for doctype, opts in doctypes_to_update.items():
        print(doctype, opts)

        for line in opts.get('child_doc_lines'):
            print(line)
            doc = frappe.get_doc(doctype, line.get('package'))  # Getting Package Doc from Parent Doc Line

            if package.change_status(options['package']['new_status']):  # If status can be changed. Prevent unnecessary updates
                doctypes_to_update['package']['updated'] += 1
                package.flags.ignore_validate = True  # Set flag ON because Doc will be saved from bulk edit. No validations
                # package.save(ignore_permissions=True)  # Trigger before_save() who checks for the flag. We avoid all checks.

        # _docs_to_update(parent_doc_lines=doc.get('warehouse_receipt_lines'), options=doctypes_to_update)

    frappe.flags.mute_emails = frappe.flags.in_import = False  # Reset core flags.

    # Show message as dialog
    message = []  # Gathering Message and Title
    for doctype, opts in doctypes_to_update.items():
        message.append('{updated} out of {total} {doctype}s have been updated to {new_status}.'.format(
            updated=opts.get('updated'), total=len(opts.get('child_doc_lines')), doctype=doctype, new_status=opts.get('new_status')
        ))

    frappe.msgprint(msg=message, title='Confirm Packages', as_list=True, indicator='green')

#117 lineas y no puede actualizar mas de un tipo de Documento
#129 lineas aun no sabemos como pedir cada object to be updated!
# 79 lineas en codigo separado
