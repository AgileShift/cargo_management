# Repository Agent Policy

These instructions apply to the entire repository. A module-level `AGENTS.md`
may add specialized context, but it must not weaken or contradict the mandatory rules in this file.

## Authority and working agreement

1. Read this file before proposing or making changes in this repository.
2. Do not modify files without explicit authorization from the owner.
3. Before editing, explain the exact behavior and files that will change.
4. Work in small, reviewable increments and follow the authorized phase literally.
5. Do not expand a focused task into a broader refactor, migration, or automation.
6. Preserve unrelated worktree changes. Never discard, overwrite, or include them.
7. After an authorized edit, inspect the complete scoped diff and run checks proportional to the risk.
8. Communicate with the owner in Spanish unless asked otherwise. Write code,
   identifiers, comments, and repository instructions in English.

## Frappe UI and DocType metadata

- The DocType UI in Desk is the sole source of truth for fields, labels,
  sections, columns, ordering, options, dependencies, properties, and permissions.
- Never create or modify DocType structure by manually editing JSON, using
  `apply_patch`, scripts, the console, fixtures, patches, JavaScript, or Python.
- Make structural changes in Desk. After saving, inspect the regenerated JSON
  only to verify that it represents the UI configuration correctly.
- Never manually edit blocks delimited by `begin: auto-generated types` and `end: auto-generated types`.
- Inside a DocType controller class, do not place manual attributes or methods
  before the auto-generated type block. Frappe owns that initial block.
- Do not use JavaScript to construct, reorder, or replace declarative form layout.
- If Desk cannot express a requirement, stop and present the limitation and alternatives before proposing code.

This does not prohibit authorized controller behavior or non-structural form
events. Python remains the final authority for business validation and data
integrity; JavaScript may provide UI triggers and data-entry assistance.

## Operational source of truth

- Operational documentation for QuickBox and Grupo Real lives in the sibling
  `grupo_real_docs` repository. Read its root `AGENTS.md`, the affected Space
  `README.md`, and the canonical page for the process before changing business behavior.
- Do not invent workflows, statuses, responsibilities, or business rules from
  field names, historical records, test data, or incomplete documentation.
- Distinguish confirmed current behavior, intended design, inference, and open decisions in every analysis.
- Technical documentation tied closely to this application belongs in this repository, not in `grupo_real_docs`.
- Do not edit or publish documentation in Frappe Wiki directly. Git is the source of truth for `grupo_real_docs`.

Relevant operational areas currently include:

- `quickbox/operaciones/paquetes/`
- `quickbox/operaciones/envio-de-carga/`
- `quickbox/operaciones/recepcion-de-carga/`

Some pages explicitly state that they are work in progress. Treat those pages
as incomplete context, not authorization to fill gaps by assumption.

## Application architecture boundaries

- DocType fields, layout, labels, options, and permissions: Desk.
- Validation, calculations, status transitions, synchronization, and data
  integrity: Python backend.
- Non-structural UI behavior, calls, refreshes, indicators, and optional
  data-entry helpers: JavaScript, only after approval.
- Shared backlink synchronization: reuse `cargo_management.engine.LinkSyncMixin`
  and `LinkSyncRule`; do not duplicate per-DocType query loops.
- Bulk status cascades: reuse `cargo_management.engine.BulkStatusUpdate` and its
  whitelisted engine endpoints; do not recreate repetitive action modules.
- Keep DocType controller classes small. Shared behavior belongs in the engine
  only when it removes real duplication across multiple DocTypes.
- Do not move business authority into JavaScript merely for convenience.

## Cargo invariants that require explicit revalidation

- A Parcel backlink conflict must block linking to another document.
- Duplicate Parcel rows are allowed in Cargo Shipment Receipt and must not be
  rejected merely because the same Parcel appears more than once there.
- Warehouse Receipt owns receipt-level weight, volume, pieces, parcels, package,
  and dimension behavior; do not assume child and parent dimensions must match.
- Parcel, Warehouse Receipt, Cargo Shipment, and Cargo Shipment Receipt have
  related but distinct status meanings. Do not add automatic cascades without
  confirming the operational event that authorizes them.
- Link synchronization and status transitions are separate responsibilities.

Revalidate these statements against current code and approved operational
documentation before extending them.

## Data and transaction safety

- Do not inspect production or restored production business data unless the
  owner explicitly requests it for the current task.
- Do not submit, cancel, or modify real business documents without explicit
  authorization.
- Tests that create accounting, inventory, shipment, receipt, or Parcel records
  must use controlled data and rollback whenever possible.
- Do not run destructive migrations or improvised schema changes.
- Prefer Frappe and ERPNext APIs and established application helpers over direct
  SQL. Direct database updates require a demonstrated batch or integrity need.

## Verification requirements

Before declaring an authorized change complete:

1. Review the complete scoped `git diff`.
2. Confirm that no unrelated changes were modified or included.
3. Run `git diff --check`.
4. Check Python or JavaScript syntax for every changed source file.
5. Run focused DocType tests when behavior changes.
6. For Desk metadata changes, verify the regenerated JSON without manually
   correcting it.
7. Report what was implemented, what was deliberately left unchanged, and any
   unresolved business decision.
