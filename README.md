## ERPNext Cargo Management

Package Tracker for Local Courier Services.

Made in [Frappe Framework v13](https://github.com/frappe/frappe/) using [ERPNext](https://github.com/frappe/erpnext) for a fully fledged ERP.

[EasyPost](https://www.easypost.com/) as Tracking API([Source Code](https://github.com/EasyPost/easypost-python))

### App Includes:
- Parcel
  - Workspace
  - Dashboard View
  - Settings(Global Settings)
- Warehouse Receipt
- Cargo Shipment
- Cargo Packing List
- Cargo Shipment Receipt
- Reports
- Selling:
  - Custom Quotation
  - Settings(For Advance Selling Customizations)

### Extra Addons
- [ERPNext Delivery Management](https://github.com/AgileShift/erpnext_delivery)
- [Frappe Nextcloud](https://github.com/AgileShift/frappe_nextcloud)
- Warehouse Management

### Customizations to Frappe and ERPNext:
- Selling:
  - Quotation
  - Sales Invoice are used to invoice for Logistic services and items related to Business
  - Sales Order are the only choice to make purchases online on behalf of the customer:
    - WORKING(We must link the sales order with the package and content, later we must invoice the order and service.)
- Package can be linked in Issue:
  - WORKING(on the change of status)

### Description
This app allows you to track the packages sent by our customers to our warehouse.
Invoice and deliver them.

Currently we can track all carriers supported by the Tracking API Provider [EasyPost](https://www.easypost.com/carriers):
* eg: DHL, UPS, USPS, FedEx, and more.

The customizations allow us to:
- Invoice a **Customer** for the Logistic Services and Products in Stock offered.
- Link the **Sales Invoice** with a Package and update its statuses.

All while using all the core functionalities from ERPNext like Accounting, Stock, HR, Assets, Payroll.

### Flow
1. **Packages** are created and can be related to a specific customer
   1. Content of the package can be added and its related Item for invoice Purposes.
   2. It can be tracked by the API or not.
2. As the carrier updates the details the Tracking API send it via a webhook, we gather and update.
3. When the package is marked as delivered at warehouse by the carrier we stop the Tracking API webhook updates
4. A **Warehouse Receipt** doc its created to link the received package:
   1. Package related fields can be filled by the Warehouse: Content, Dimensions, Weight, Receipt Date
5. **Cargo Shipment** is created to export Packages in bulk:
   1. Warehouse Receipts are added in them.
   2. Related information: Transportation Type, Departure date, Est Arrival Date, Dimensions, Gross Weight

# WORKING on this flow
6. **Cargo Shipment Receipt** is created to receive the Cargo Shipment:
   1. A Receipt loads the data of all related **Packages** in the **Cargo Shipment** through the **Warehouse Receipts**
   2. All **Packages** are sorted by **Customer**, and its the moment to set all related data to Create Invoices.
   3. When all the **Packages** have been processed, the **Sales Invoices** can be created.
      1. A **Sales invoice** will be created for the customer, it will contain all the related **Packages**.
7. WORKING

#### List of Carriers:
- USPS(EasyPost)
- Amazon
- UPS(EasyPost)
- DHL(EasyPost)
- FedEx(EasyPost with carrier account)

- Drop Off
- Pick Up
- Unknown
-
- Cainiao
- SF Express
- Yanwen
- LaserShip


#### Helpers
- **Cargo Packing List**: is a "Packing List" for the **Cargo Shipment**:
  1. Gets all the content declared by the **Customer** and the content declared by the **Warehouse** of the packages in a **Cargo Shipment**
  2. It allows to modify the content and amount declared only for Print.
  3. WORKING

## This is work in progress. But it's stable for usage
- WORKING
  1. Packing Slip for customs:
  2. Fetching data of prices and quotations from packages to Cargo Shipment Receipt: WORKING
- FUTURE:
  1. Setting data of prices in CSR to Sales Invoice
  2. Working in the Sales Orders!



##### Code related TODO:
1. Add custom Doctypes to Global Search: https://github.com/frappe/erpnext/pull/24055/files
2. Migrate SQL to QueryBuilder? usign Pypika?
