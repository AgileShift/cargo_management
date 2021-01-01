from frappe.model.document import Document


class PackageCarrier(Document):
    """
    # TODO:
    We choose this Doctype to act as a child to PackageSettings and a Link for Package.

    Field:
    carrier_name: Is the readable carrier name for the customer
    carrier_code: Is the code chosen by the external API

    name is set to: field:carrier_code

    On any case, we change the carrier_code from the PackageSettings, the name field is not "renamed".
    Causing multiple discrepancies eg:
        carrier_code works with the API but the Package has a Link to an outdated code.

    Solution is to change the carrier_code from the PackageSettings and also rename:
        http://localhost/desk#Form/Package%20Carrier/{name}
        Here we can rename the field selected as name(carrier_code), and the frappe name id key.

    Workaround: When carrier_code is changed, automatically rename the name id field.
    """
    pass
