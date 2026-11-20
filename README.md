# Cargo Management

An ERPNext app for QuickBox parcel and freight operations, including tracking, warehouse receipts, shipments, and invoicing.

## Scope

The app supports QuickBox freight forwarding. See Technical documentation for operational context and Backlog for ongoing work.

The documented ERPNext foundation includes Accounting, Stock.
This overview does not verify the app’s integration with each area.

## Features

- **Parcel Management:** manages parcels, integrates tracking APIs, and handles notifications.
- **Warehouse Management:** handles receipt of parcels in warehouses.
- **Shipment Management:** manages shipments and receipts.
- **Support Management:** customizes ERPNext support for parcels and orders.
- **Custom views:** workspaces, dashboards, settings, and reports.
- **Parcel tracking integrations:** [EasyPost](https://www.easypost.com/tracking-guide)
  ([Python client](https://github.com/EasyPost/easypost-python)) and [17Track](https://api.17track.net).

## Requirements

This app requires [Frappe Framework](https://github.com/frappe/frappe/) and [ERPNext](https://github.com/frappe/erpnext)
at `>=16.60.0,<17.0.0`.
See [pyproject.toml](pyproject.toml) for the full dependency requirements, including Python.

## Configuration

### API keys and webhooks

#### EasyPost Configuration

1. Get Your [EasyPost API Key](https://www.easypost.com/docs/api#authentication)
2. Set the **API Key**: `$ bench set-config easypost_api_key API_KEY`
3. Create and set your **Webhook Secret**(hmac): `$ bench set-config easypost_webhook_secret SECRET`
4. Set up your **Webhook Secret** and the **Webhook URL** on EasyPost:
   `{HOST}/api/method/cargo_management.parcel_management.doctype.parcel.api.easypost_api.easypost_webhook`

#### 17Track Configuration

1. Get Your [17Track Security Key](https://api.17track.net/en/doc?anchor=get-security-key)
2. Set the **API Key**: `$ bench set-config 17track_api_key API_KEY`
3. Set up the **Webhook URL** on 17Track:
   `{HOST}/api/method/cargo_management.parcel_management.doctype.parcel.api.17track_api.17track_webhook`

### Carrier support snapshot

Last checked: 24 Sept 2026

| Carrier    |    EasyPost    | 17Track |
|:-----------|:--------------:|:-------:|
| Amazon     |       ❌️       |   ❌️    |
| USPS       |       ✅️       |   ✅️    |
| UPS        |       ✅️       |   ✅️    |
| DHL        |       ✅️       |   ✅️    |
| FedEx      | ❗️With Account |   ✅️    |
| OnTrac     | ❗️With Account |   ✅️    |
| Cainiao    | ❌️ Deprecated  |   ✅️    |
| SpeedX     |       ❌️       |   ✅️    |
| SF Express | ❗️With Account |   ✅️    |
| Yanwen     |   ⁉️ Limited    |   ✅️    |
| YunExpress | ❌️ Deprecated  |   ✅️    |
| SunYou     |       ❌️       |   ✅️    |
| Veho       | ❗️With Account |   ✅️    |
| GOFO       |    Pending     |   ✅️    |

## Technical documentation

- [QuickBox functional playbook](docs/playbook.md)
- [Carrier support snapshot](#carrier-support-snapshot)

## Backlog

- [QuickBox functional backlog](docs/functional-backlog.md)
- [GitHub project](https://github.com/orgs/AgileShift/projects/1/)

- **Cargo Core:** the existing TODO refers to adding the new engines.
- **Selling Management:** draft refactor name for parcel invoicing and customer import orders.
- **Purchase Management:** TODO.
- **Related add-ons in progress:** [ERPNext Delivery Management](https://github.com/AgileShift/erpnext_delivery)
  and [Frappe Nextcloud](https://github.com/AgileShift/frappe_nextcloud).

### Parcel flow in progress

1. Create a **Parcel**, optionally linked to a customer.
   1. Its contents and related Item can be added for invoicing.
   2. Tracking through an API is optional.
2. As the carrier updates the details, the Tracking API sends it via a webhook, we gather and update.
3. When the parcel is marked as delivered at the warehouse by the carrier, we stop the Tracking API webhook updates
4. Create a **Warehouse Receipt** to link the received parcel:
   1. The Warehouse can fill parcel-related fields: Content, Dimensions, Weight, Receipt Date
5. **Cargo Shipment** is created to export parcels in bulk:
   1. Warehouse Receipts are added to them.
   2. Related information: Transportation Type, Departure date, Est Arrival Date, Dimensions, Gross Weight
6. **Cargo Shipment Receipt** is created to receive the Cargo Shipment:
   1. A Receipt loads the data of all related **Parcels** in the **Cargo Shipment** through the **Warehouse Receipts**
   2. Sort **Parcels** by **Customer** and set the related data needed to create invoices.
   3. When all the **Parcels** have been processed, the **Sales Invoices** can be created.
      1. A **Sales invoice** will be created for the customer, it will contain all the related **Parcels**.

### Frappe and ERPNext customizations in progress

- Selling:
  - Quotation
  - Sales Invoices are used to invoice for Logistic services and items related to Business
  - Sales Orders are the only choice to make purchases online on behalf of the customer:
    - WORKING (We must link the sales order with the parcel and content, later we must invoice the order and service.)
- Parcel can be linked in Issue:
  - WORKING (on the change of status)
- The customizations allow us to:
  - Invoice a **Customer** for the Logistic Services and Products in Stock offered.
  - Link the **Sales Invoice** with a Parcel and update its statuses.

## Contributing

Read [AGENTS.md](AGENTS.md) before proposing changes.

This app uses `pre-commit` for code formatting and linting.
Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/cargo_management
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

## License

[AGPLv3](LICENSE.txt).
