# QuickBox Functional Backlog

This document preserves the useful functional vision from **QuickBox - Flujos Ideales - Crear PlayBook** (2019) without treating historical ideas as current behavior or approved policy.

Operational procedures belong in `grupo_real_docs`. This backlog describes desired capabilities for `cargo_management`; it does not assign priority, owner, deadline, commercial terms, or implementation design.

## Status labels

- **Existing:** the principal capability is present in the current application.
- **Partial:** a foundation exists, but the desired outcome is incomplete.
- **Not found:** no implementation was found in the current repository.
- **Business decision required:** the capability depends on policies or commercial rules that have not been approved.

## Current foundation

The current application models the operational chain through `Parcel`, `Warehouse Receipt`, `Cargo Shipment`, `Cargo Shipment Receipt`, and ERPNext sales documents.
EasyPost and 17Track provide external tracking integrations. In production, invoices are generated from `Cargo Shipment Receipt` and then reviewed manually for tariff and description errors.

## 1. Assisted purchases and parcel relationships

- **Problem:** purchases made on behalf of customers must remain connected to the quotation or sale, supplier purchase, payment, parcel, and final invoice.
- **Desired result:** trace an assisted purchase from the customer's request through acquisition, tracking, importation, invoicing, and delivery without duplicating data.
- **Status:** **Partial**.
- **Current basis:** `Parcel` identifies assisted purchases and can link to a `Sales Order`; sales documents can reference parcels.
- **Pending decisions:** define the authoritative document for the request, approval, deposit, supplier purchase, and completion of an assisted purchase.
- **Dependencies:** parcel registration, payments, purchasing, invoicing, and customer communication.

## 2. Tracking alerts and carrier exceptions

- **Problem:** staff must detect delays, failed deliveries, returns, unexpected signatures, and packages marked delivered but not confirmed by the warehouse.
- **Desired result:** create actionable alerts from normalized carrier events and route each exception to the appropriate follow-up process.
- **Status:** **Partial**.
- **Current basis:** EasyPost and 17Track integrations update carrier information; parcel states represent ordinary and extraordinary confirmation.
- **Pending decisions:** define alert events, business-hour calculations, recipients, escalation rules, and closure conditions.
- **Dependencies:** carrier integrations, parcel state transitions, issues, and notifications.

## 3. Customer portal and self-service

- **Problem:** customers repeatedly request package updates and cannot report tracking numbers, review balances, or submit evidence through a dedicated channel.
- **Desired result:** let authenticated customers report packages, view their shipment history and balances, submit payment evidence, request purchases, and follow incidents.
- **Status:** **Not found**.
- **Current basis:** parcel, customer, sales, payment, and issue records provide potential data sources, but no customer portal workflow was found.
- **Pending decisions:** authentication, exposed data, permissions, allowed actions, review controls, and the relationship with the future eCommerce application.
- **Dependencies:** permissions, customer identity, payments, assisted purchases, incidents, and notifications.

## 4. Automatic customer notifications

- **Problem:** operational events require repetitive manual communication and may expose inconsistencies when records are incomplete.
- **Desired result:** notify customers only after validated events such as warehouse confirmation, departure, delay, arrival, invoicing, payment, or availability for delivery.
- **Status:** **Not found**.
- **Current basis:** parcel and shipment states can provide event sources; no complete customer-facing notification channel was found.
- **Pending decisions:** events, recipients, templates, channels, retry rules, opt-out behavior, and safeguards against premature messages.
- **Dependencies:** reliable state transitions, customer contact data, incident handling, and audit logs.

## 5. Incidents, claims, and refunds

- **Problem:** wrong names, service changes, damage, missing contents, failed warehouse confirmation, and transport losses need consistent investigation and resolution.
- **Desired result:** register an incident against a parcel, collect evidence, assign follow-up, record the decision, and connect any approved refund or other resolution.
- **Status:** **Partial**.
- **Current basis:** ERPNext `Issue` can link to a `Parcel`, and issue types exist for service changes, missing instructions, follow-up, and receipt confirmation.
- **Pending decisions:** evidence requirements, responsibility, resolution types, approval authority, refund rules, and customer communication.
- **Dependencies:** parcel history, attachments, assignments, payments, accounting, and policies.

## 6. Deliveries, routes, and couriers

- **Problem:** pickups and local or national deliveries need scheduling, route preparation, collection instructions, and proof of completion.
- **Desired result:** group ready packages into delivery runs, assign them, record amounts to collect or change to carry, and close each delivery with its outcome.
- **Status:** **Partial**.
- **Current basis:** ERPNext delivery documents are exposed in the workspace and operational delivery rules exist outside this repository; no complete QuickBox route workflow was found here.
- **Pending decisions:** delivery coverage, scheduling, assignment, failed attempts, proof of delivery, and settlement with couriers.
- **Dependencies:** invoicing, payment status, package readiness, customer address, and cash settlement.

## 7. Cash, banks, and daily controls

- **Problem:** openings, collections, supplier payments, expenses, and closing controls are distributed across ERPNext and manual procedures.
- **Desired result:** provide a controlled daily view of cash and bank activities without duplicating accounting records.
- **Status:** **Partial**.
- **Current basis:** ERPNext accounting documents and shared Grupo Real procedures cover payments and cash controls; no QuickBox-specific daily control module was found.
- **Pending decisions:** which controls remain operational checklists, which require automation, and which documents are authoritative.
- **Dependencies:** payments, expenses, purchases, reconciliation, permissions, and auditability.

## 8. Customer credit and portfolio

- **Problem:** purchases or import services provided on credit require limits, balances, delinquency follow-up, and temporary restrictions.
- **Desired result:** evaluate available credit before approval and provide a portfolio view with controlled follow-up and restriction decisions.
- **Status:** **Business decision required**.
- **Current basis:** ERPNext provides customer credit and accounts receivable capabilities; no approved QuickBox-specific credit workflow was found.
- **Pending decisions:** eligibility, limits, terms, grace periods, violations, restriction duration, and authorization.
- **Dependencies:** customer records, sales, payments, receivables, permissions, and notifications.

## 9. Insurance, memberships, prepaid pounds, and loyalty

- **Problem:** optional service packages require clear coverage, balances, eligibility, billing, and claims.
- **Desired result:** represent approved optional services and apply their benefits consistently to eligible transactions.
- **Status:** **Business decision required**.
- **Current basis:** no complete implementation was found for insurance, memberships, prepaid pounds, or loyalty rewards.
- **Pending decisions:** products offered, pricing, coverage, exclusions, expiration, transferability, claims, and accounting treatment.
- **Dependencies:** Items, pricing, subscriptions or balances, invoicing, incidents, and policies.

## 10. Administrative and operational reports

- **Problem:** management and operations need visibility into pending invoices, unpaid orders, delayed packages, unresolved incidents, shipment profitability, customer activity, and delivery costs.
- **Desired result:** provide reports derived from authoritative documents, with clear definitions and reconciliation points.
- **Status:** **Not found**.
- **Current basis:** the underlying ERPNext and cargo documents contain part of the required data; no complete report suite matching the historical vision was found.
- **Pending decisions:** metric definitions, accounting sources, audiences, refresh frequency, and required actions.
- **Dependencies:** reliable links among parcels, shipments, invoices, payments, deliveries, and issues.

## 11. Storage and uncollected packages

- **Problem:** packages that remain uncollected consume space and require consistent follow-up.
- **Desired result:** identify aging packages, notify the responsible customer, and apply only approved storage or disposition rules.
- **Status:** **Business decision required**.
- **Current basis:** parcel states and dates can support aging analysis; no approved automated storage-charge workflow was found.
- **Pending decisions:** free period, charges, notification sequence, exceptions, abandoned-property handling, and authorization.
- **Dependencies:** package availability date, customer communication, pricing, invoicing, and legal review.

## 12. Quotations, tariffs, ratings, and feedback

- **Problem:** estimated import costs can differ from final measured costs, while service and shipper quality are not captured consistently.
- **Desired result:** produce transparent estimates from approved tariff inputs, preserve the assumptions shown to the customer, compare estimates with final charges, and collect structured feedback after completion.
- **Status:** **Partial** for quotations and tariff data; **not found** for structured ratings.
- **Current basis:** parcel weights, contents, Items, sales documents, and pricing data provide foundations, but a complete approved estimation and feedback workflow was not found.
- **Pending decisions:** tariff formulas, minimums, dimensional rules, customs adjustments, estimate validity, eligible reviewers, visibility, and incentives.
- **Dependencies:** pricing, weights and dimensions, quotations, invoices, shipment costs, and customer identity.

## Historical ideas deliberately excluded

This backlog does not preserve historical tracking numbers, individual USPS investigations, example penalties, unapproved guarantees, obsolete model sketches, or customer-identifying cases. Those records are not requirements and must not be recreated as policy or test data.
