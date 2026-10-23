# QuickBox Functional Backlog

This backlog evaluates the capabilities described in the [QuickBox Functional Playbook](playbook.md) against the current `cargo_management` application.

The Playbook preserves the functional intent. This document records implementation coverage and unresolved decisions; it does not establish operational procedures, commercial terms, priorities, owners, or deadlines.

## Evaluation labels

### Implementation coverage

- **Existing:** the principal capability is present in the current application.
- **Partial:** a technical foundation exists, but the expected result is incomplete.
- **Not found:** no implementation was found in the current repository.

### Functional definition

- **Defined:** the expected behavior is sufficiently described for further technical analysis.
- **Needs decision:** commercial, operational, accounting, legal, or permission rules remain unresolved.
- **Mixed:** part of the capability is defined and part still requires decisions.

## Current foundation

The current application models the operational chain through `Parcel`, `Warehouse Receipt`, `Cargo Shipment`, `Cargo Shipment Receipt`, and ERPNext sales documents.

EasyPost and 17Track provide external tracking integrations. In production, invoices are generated from `Cargo Shipment Receipt` and then reviewed manually for tariff and description errors.

Operational procedures remain in `grupo_real_docs`. Code evidence and confirmed operations must not be treated as interchangeable.

## 1. Assisted purchases and document traceability

**Playbook source:** [ASC-01 · Assisted purchase](playbook.md#asc-01).

- **Problem:** purchases made on behalf of customers must remain connected to the request, quotation or sale, supplier purchase, payment, parcel, final invoice, and delivery.
- **Desired result:** trace an assisted purchase from the customer's request through acquisition, tracking, importation, invoicing, and completion without duplicating data.
- **Implementation coverage:** **Partial**.
- **Functional definition:** **Mixed**.
- **Confirmed operation:** QuickBox currently provides the assisted-purchase service and subsequently imports the resulting package.
- **Code evidence:** `Parcel.assisted_purchase` identifies assisted purchases; `Parcel.sales_order` can link a parcel to a `Sales Order`; sales items can reference a `Parcel`.
- **Important limit:** these fields do not demonstrate an automated end-to-end relationship with `Quotation`, `Payment Entry`, `Purchase Order`, supplier payment, final invoicing, or completion.

### Capability breakdown

| Capability | Coverage | Definition | Remaining work or decision |
|---|---|---|---|
| Customer request and product links | Not found | Needs decision | Define the authoritative request document and required inputs. |
| Quotation and customer approval | Partial | Defined | Confirm how the approved quotation becomes the authoritative sale. |
| Sales Order for the assisted purchase | Partial | Defined | Complete and validate its relationship with parcels and later invoices. |
| Advance payment | Partial | Mixed | Define the required amount, approval exceptions, and authoritative link to the purchase. |
| Customer credit | Partial | Needs decision | Define eligibility, limits, terms, approvals, and restrictions. |
| Supplier purchase | Not found | Mixed | Define and implement the relationship with `Purchase Order` and supplier payment. |
| Tracking number and Parcel | Partial | Defined | Ensure the parcel preserves its assisted-purchase origin without duplicated entry. |
| Origin and destination logistics | Existing | Defined | Preserve the relationship throughout the confirmed cargo flow. |
| Product and service invoicing | Partial | Mixed | Define which documents and amounts close the assisted purchase. |
| Remaining balance and completion | Partial | Needs decision | Define closure conditions and the final authoritative status. |

- **Dependencies:** quotations, selling, purchasing, payments, credit, parcels, invoicing, customer communication, and delivery.

## 2. Tracking alerts and carrier exceptions

**Playbook source:** [SEG-01 · Carrier tracking and exceptions](playbook.md#seg-01).

- **Problem:** staff must detect delays, failed deliveries, returns, unexpected signatures, and packages marked delivered but not confirmed at Origin.
- **Desired result:** convert normalized carrier events into actionable exceptions and route each case to the appropriate follow-up process.
- **Implementation coverage:** **Partial**.
- **Functional definition:** **Mixed**.
- **Code evidence:** EasyPost and 17Track integrations update carrier information; parcel states represent ordinary and extraordinary confirmation conditions.
- **Pending decisions:** alert events, business-hour calculations, recipients, escalation rules, confirmation windows, and closure conditions.
- **Dependencies:** carrier integrations, parcel state transitions, incidents, notifications, and audit history.

## 3. Customer portal and self-service

**Playbook source:** [POR-01 · Customer portal and self-service](playbook.md#por-01).

- **Problem:** customers cannot report tracking numbers, review balances, submit evidence, request purchases, or follow incidents through a dedicated authenticated channel.
- **Desired result:** provide controlled self-service actions over the customer's own records.
- **Implementation coverage:** **Not found**.
- **Functional definition:** **Mixed**.
- **Current basis:** parcel, customer, sales, payment, and issue records provide potential data sources, but no complete customer portal workflow was found.
- **Pending decisions:** authentication, exposed data, permissions, allowed actions, review controls, and the relationship with future eCommerce applications.
- **Dependencies:** permissions, customer identity, payments, assisted purchases, incidents, and notifications.

## 4. Automatic notifications

**Playbook source:** [NOT-01 · Automatic notifications](playbook.md#not-01).

- **Problem:** operational events require repetitive manual communication and can expose inconsistencies when records are incomplete.
- **Desired result:** notify staff or customers only after validated events.
- **Implementation coverage:** **Not found** for a complete customer-facing notification workflow.
- **Functional definition:** **Needs decision**.
- **Current basis:** parcel and shipment states can provide event sources.
- **Pending decisions:** events, recipients, templates, channels, retries, customer preferences, and safeguards against premature or duplicate messages.
- **Dependencies:** reliable state transitions, contact data, incidents, and audit logs.

## 5. Incidents, claims, and resolutions

**Playbook source:** [INC-01 · Incidents, claims, and resolutions](playbook.md#inc-01).

- **Problem:** wrong names, service changes, damage, missing contents, failed confirmation, and transport losses need consistent investigation and resolution.
- **Desired result:** register an incident against a parcel, collect evidence, assign follow-up, record the decision, and connect any approved resolution.
- **Implementation coverage:** **Partial**.
- **Functional definition:** **Needs decision**.
- **Code evidence:** ERPNext `Issue` can link to a `Parcel`, and issue types exist for service changes, missing instructions, follow-up, and receipt confirmation.
- **Pending decisions:** evidence, responsibility, resolution types, approval authority, refunds, charges, guarantees, and customer communication.
- **Dependencies:** parcel history, attachments, assignments, payments, accounting, policies, and legal review.

## 6. Deliveries, routes, and couriers

**Playbook source:** [ENT-01 · Pickups and deliveries](playbook.md#ent-01).

- **Problem:** pickups and local or national deliveries need scheduling, route preparation, collection instructions, change to carry, and proof of completion.
- **Desired result:** group ready packages into delivery runs and close each delivery with its financial and operational outcome.
- **Implementation coverage:** **Partial**.
- **Functional definition:** **Mixed**.
- **Current basis:** ERPNext delivery documents are exposed in the workspace and operational delivery rules exist in `grupo_real_docs`; no complete QuickBox route workflow was found here.
- **Pending decisions:** scheduling, assignment, failed attempts, proof of delivery, and courier settlement.
- **Dependencies:** invoicing, payment status, package readiness, customer address, and cash settlement.

## 7. Payments, cash, banks, and daily controls

**Playbook source:** [PAG-01 · Payments, advances, and credit](playbook.md#pag-01).

- **Problem:** advances, collections, supplier payments, expenses, and closing controls are distributed across ERPNext and manual procedures.
- **Desired result:** provide traceable payment application and daily controls without duplicating accounting records.
- **Implementation coverage:** **Partial**.
- **Functional definition:** **Mixed**.
- **Current basis:** ERPNext accounting documents and shared Grupo Real procedures cover payments, cash audits, deposit validation, and settlement controls.
- **Pending decisions:** authoritative links for assisted-purchase advances and supplier payments, plus which controls remain procedural or require automation.
- **Dependencies:** sales, purchases, payments, expenses, reconciliation, permissions, and auditability.

## 8. Customer credit and portfolio

**Playbook source:** [PAG-01 · Payments, advances, and credit](playbook.md#pag-01).

- **Problem:** purchases or import services provided on credit require limits, balances, delinquency follow-up, and controlled restrictions.
- **Desired result:** evaluate available credit before approval and provide a portfolio view with authorized follow-up.
- **Implementation coverage:** **Partial**, based on ERPNext accounts-receivable capabilities.
- **Functional definition:** **Needs decision**.
- **Pending decisions:** eligibility, limits, terms, grace periods, violations, restriction duration, and approval authority.
- **Dependencies:** customers, sales, payments, receivables, permissions, and notifications.

## 9. Optional services and loyalty

**Playbook source:** [SER-01 · Optional services](playbook.md#ser-01).

- **Problem:** insurance, memberships, prepaid pounds, preferred rates, delivery benefits, and loyalty require approved commercial and accounting definitions.
- **Desired result:** represent only approved services and apply their benefits consistently.
- **Implementation coverage:** **Not found** as a complete capability.
- **Functional definition:** **Needs decision**.
- **Pending decisions:** products offered, pricing, coverage, exclusions, expiration, transferability, claims, ratings, incentives, and accounting treatment.
- **Dependencies:** Items, pricing, subscriptions or balances, invoicing, incidents, policies, and legal review.

## 10. Administrative and operational reports

**Playbook source:** [REP-01 · Administrative and operational reports](playbook.md#rep-01).

- **Problem:** management and operations need visibility into unpaid documents, delayed packages, unresolved incidents, profitability, customer activity, and delivery costs.
- **Desired result:** provide reports derived from authoritative documents with clear definitions and reconciliation points.
- **Implementation coverage:** **Not found** as a complete report suite matching the Playbook.
- **Functional definition:** **Mixed**.
- **Current basis:** ERPNext and cargo documents contain part of the required data.
- **Pending decisions:** metric definitions, accounting sources, audiences, periods, refresh frequency, and required actions.
- **Dependencies:** reliable links among parcels, shipments, invoices, payments, deliveries, purchases, and incidents.

## 11. Storage and uncollected packages

**Playbook source:** [INV-01 · Inventory and storage](playbook.md#inv-01).

- **Problem:** uncollected packages consume space and require consistent follow-up.
- **Desired result:** identify aging packages, notify the customer, and apply only approved storage or disposition rules.
- **Implementation coverage:** **Partial** for identifying packages by state and date; **not found** for a complete automated charge workflow.
- **Functional definition:** **Needs decision**.
- **Pending decisions:** free period, charges, notification sequence, exceptions, abandoned-property handling, and authorization.
- **Dependencies:** package availability date, customer communication, pricing, invoicing, policies, and legal review.

## 12. Quotations, pricing, ratings, and feedback

**Playbook sources:** [FAC-01 · Invoicing and pricing](playbook.md#fac-01) and [SER-01 · Optional services](playbook.md#ser-01).

- **Problem:** estimated import costs can differ from final measured costs, while service and supplier quality are not captured consistently.
- **Desired result:** produce transparent estimates from approved inputs, preserve their assumptions, compare estimates with final charges, and collect structured feedback.
- **Implementation coverage:** **Partial** for quotations and pricing data; **not found** for structured ratings.
- **Functional definition:** **Needs decision**.
- **Current basis:** parcel weights, contents, Items, sales documents, and pricing data provide foundations.
- **Pending decisions:** formulas, minimums, dimensional rules, customs adjustments, validity, eligible reviewers, moderation, visibility, and incentives.
- **Dependencies:** pricing, routes, weights and dimensions, quotations, invoices, shipment costs, and customer identity.

## 13. Policies and digital acceptance

**Playbook source:** [POL-01 · Policies, terms, and pending decisions](playbook.md#pol-01).

- **Problem:** several capabilities depend on terms, restrictions, guarantees, responsibilities, and customer acceptance that the application must not invent.
- **Desired result:** implement controls only after the corresponding operational or legal policy is approved.
- **Implementation coverage:** **Not found** as an integrated digital-acceptance capability.
- **Functional definition:** **Needs decision**.
- **Pending decisions:** accepted terms, versioning, evidence of acceptance, restricted products, price variations, guarantees, storage, insurance, claims, and document integrity.
- **Dependencies:** approved policies in `grupo_real_docs`, permissions, customer identity, audit logs, and legal review.

## Historical-source treatment

The Playbook preserves historical ideas such as example charges, time windows, restrictions, guarantees, and service concepts as quoted references. They are not actionable requirements until approved and reflected here as defined capabilities.

Historical tracking numbers, individual carrier investigations, customer-identifying cases, and obsolete technical model sketches remain excluded.
