# Agent Instructions — Cargo Management

Maintenance reference: [Documentation normalization skill](../../frappe-app-standards/skills/frappe-app-docs-normalize/SKILL.md).
Technical app name: `cargo_management`.

These instructions apply throughout this repository. Module guides add specific instructions.
If they conflict with the root rules, ask the owner before proceeding.

<!-- BEGIN SHARED RULES: maintained from agents-templates.md -->
## General rules — shared across apps

### Working agreement

- Read the root README, root AGENTS, and applicable module guides before proposing or making changes.
  Read CONTRIBUTING.md, when present, before preparing a commit or pull request.
- Before working inside a module, locate and read its applicable local instructions.
  When creating or reorganizing documentation, consult the normalization skill linked by the root AGENTS.
  Keep template schemas in its references and do not repeat parent rules in module guides.
- Use available `frappe-app-dev` references for Frappe implementation and `frappe-code-review` for code reviews.
  External skills do not override repository/module rules or explicit owner decisions.
  Apply only compatible guidance within the authorized scope. Report conflicts and retain the applicable local rule.
  If a skill is unavailable, report it and continue with local instructions. Do not install it implicitly.
- Before editing, explain the objective, exact affected files, proposed behavior, material risks, and verification plan.
  Obtain explicit authorization for that scope.
  Honor authorization already given; do not request it again for the same work.
- Work in small, reviewable increments and follow the authorized phase literally.
  Completing a phase does not authorize the next one.
- Treat documentation normalization as an explicit task with one declared scope: entire app, root only,
  named module(s) only, or root plus named module(s).
  Entire app includes only root and existing meaningful module README.md and AGENTS.md files.
  Do not infer module inclusion from a root-only request.
  Include other technical docs explicitly in normalization scope before editing them.
  Reading linked references does not authorize editing them.
- Do not expand a focused task into a broader refactor, migration, or automation.
- Preserve unrelated worktree changes. Never discard, overwrite, or include them.
- Evaluate the business need before adding modules, screens, or forms.
  Generalize requirements across businesses when appropriate, without inventing future needs.
- Keep code understandable on first reading.
  Prefer direct solutions over unnecessary abstractions; remove real duplication without building speculative frameworks.
- Keep affected documentation current as part of authorized refactors, improvements, and behavior changes,
  before declaring the work complete or preparing its commit.
  Update README, technical references, and local instructions where their documented behavior or constraints changed;
  leave unrelated documentation intact.
- Keep detailed technical descriptions in the relevant README or linked technical reference.
  Use AGENTS for working instructions, brief context, and concise invariants; link to the canonical explanation
  instead of maintaining a second description of behavior, architecture, limitations, or verification status.
  Keep module models, invariants, phases, and detailed verification in their existing local guides.
  Do not centralize or replace them with a generic description of the app.
- Keep small pending work near its context in Issues, README sections, or code TODOs.
  When it becomes distributed, repetitive, or difficult to review, consider a backlog:
  keep app-wide work in `docs/backlog.md` and module-specific work in `docs/{module}-backlog.md`,
  both under the app root; use lowercase, hyphenated module names.
  Create a separate module backlog only when its independent work justifies it and the documentation scope authorizes it.
  Link related backlogs and avoid duplicate items.
- Before implementing a proposal that conflicts with a README or other documented decision, warn the owner,
  explain the conflict, and obtain approval for the new direction.
  Do not silently change code or rewrite documentation to conceal the disagreement.

### Decision quality

- Be direct and truthful. Challenge weak assumptions with evidence and explain their practical consequences.
  Do not agree merely to be agreeable.
- Distinguish implemented behavior, approved design, external documented behavior, inference, and unresolved decisions.
  State uncertainty instead of guessing.
- When explicitly evaluating an idea or design, give an honest score out of 10 with criteria.
  Do not attach arbitrary scores to routine implementation work.
- Do not infer business policy from field names, historical data, test fixtures, or unfinished documentation.
  Consult the relevant approved operational process.
- During authorized technical work, compare relevant documentation with the code in scope.
  Report discrepancies and distinguish implemented behavior, approved design, and pending decisions or verification.
  Do not change rules or code to resolve discrepancies without authorization, or expand the task into a repository-wide audit.
- When explicitly asked to audit technical documentation,
  verify every factual technical claim in the selected scope against relevant current evidence.
  This includes README.md files, AGENTS.md files, repository-specific rules, module guides, and other technical documentation.
- Report unsupported, contradicted, stale, duplicated, or ambiguous claims.
  Distinguish confirmed facts, approved design, business policy, and pending decisions.
  Do not silently rewrite policy or claim that missing evidence proves a feature is absent.
- A field, button, README, or scaffold test does not prove a workflow is implemented.
  When verifying behavior within a technical task, trace its controller and invocation, and inspect meaningful tests when available.
- Revalidation means checking available evidence first.
  Ask the owner when evidence conflicts or a business decision is missing;
  do not request repeated confirmation of an unchanged decision already approved.

### Language and documentation conventions

- Reflow Markdown paragraphs and list items around 120 characters per line, using flexible semantic line breaks.
  Keep short, related sentences together when they fit.
  When wrapping is needed, prefer sentence or natural clause boundaries and avoid short trailing fragments.
  Allow a modest overflow to keep a sentence or clause together rather than leave a few words on the next line.
  Keep complete Markdown links and URLs intact; allow longer lines for links, tokens, tables, or code examples.
  Preserve intentional Markdown line breaks and structure.
- Use English for code and documentation.
- Use the repository's configuration files for dependency requirements, code formatting, and lint settings.
  Follow `.editorconfig` and `pyproject.toml` where present; reference them instead of repeating their values in AGENTS.
  Apply the shared Markdown convention to documentation. Report conflicting settings before changing configuration.

### Localization and generated catalogs

- Mark user-facing text for Frappe i18n (`_()` in Python, `__()` in JavaScript).
- Inspect and reuse existing Frappe/ERPNext labels, message strings, and Select options when their meaning fits.
  Prefer exact existing wording to small variations that add custom strings and translation maintenance.
  Never reuse misleading wording just to avoid a translation.
- Suggest consolidating near-duplicate labels when they mean the same thing;
  do not merge distinct concepts or rename them without authorization for that change.
- Never manually create, edit, or patch `.pot` or `.mo` files, including through ad hoc scripts.
- For authorized localization updates, use official commands supported by the installed Frappe/Bench version,
  scoped to the requested app and locale: extract POT, synchronize PO, then compile MO.
  If they fail, report the blocker; do not patch generated output.
- Preserve existing translations and source keys.
  Edit `.po` translation values only when the user explicitly requests translation; otherwise, leave untranslated entries pending.

### Frappe UI and generated metadata

- Make UI structure and DocType metadata changes through the Frappe interface.
  This includes fields, labels, sections, columns, order, options, dependencies, properties, and permissions.
- Never implement structural changes through code, scripts, console commands, patches, or fixtures.
  Never manually create or edit Frappe-generated JSON files.
- Never manually edit blocks between `begin: auto-generated types` and `end: auto-generated types`.
  Inside a DocType controller, do not put manual attributes or methods before Frappe's initial generated type block.
- If the required interface is unavailable, ask the owner to make the change.
  Do not bypass the interface restriction through code.
- Inspect regenerated files to verify the configuration.
  Correct discrepancies through the interface, not by editing generated output.
- If the interface cannot express a requirement, present the limitation and alternatives for a decision before proceeding.
- Authorized JavaScript may provide non-structural form behavior and UI assistance; it must not construct, reorder,
  or replace declarative form structure.

### Core field names

- Follow core fieldname conventions for equivalent concepts.
  If no core term fits, explain the difference and propose accurate English wording rather than reusing a misleading label.

### Core functionality and business logic

- Inspect Frappe, ERPNext, declared dependencies, and existing app helpers before implementing new behavior.
  Verify the installed source rather than assuming compatibility from memory.
- Prefer existing DocTypes, APIs, functions, utilities, and business workflows over parallel custom implementations.
  Do not copy core logic when it can be reused.
- Use supported entry points and preserve validations, permissions, and document lifecycles.
  Do not bypass them merely to make an operation easier.
- Add custom behavior for a verified gap, and explain that gap before editing.
- Keep authoritative validation, calculations, state transitions, and data integrity in Python.
  JavaScript may orchestrate necessary UI interaction and feedback.
- Keep controllers focused. Introduce shared helpers when they remove real duplication.
- For workflows creating related documents, define ownership, retry behavior, cancellation,
  and recovery before implementing automation.

### Hooks and core overrides

- Every new hook requires the owner's explicit authorization, including document events, scheduled tasks,
  lifecycle hooks, and other hook registrations.
- Adding or changing core overrides also requires explicit authorization.
  Do not edit or bypass core behavior as an incidental part of a feature.
- Approval must cover the particular hook or override.
  A general feature request does not implicitly approve that mechanism.
- Explain the trigger, affected behavior, scope, and why existing supported mechanisms are insufficient.
  Preserve existing hooks during documentation normalization.

### Data and transaction safety

- Do not inspect production or restored production business data unless the owner explicitly requests it for the current task.
  Use only the necessary data.
- Do not create, submit, cancel, or modify real business documents without explicit authorization.
  Documentation of an existing production practice is not permission.
- Use controlled test data and rollback whenever possible for accounting, inventory, shipment, receipt,
  and other transactional tests.
- Do not run destructive migrations or improvised schema changes.
- Prefer Frappe document APIs, database APIs, and query builder over raw SQL.
  Use raw SQL only for a demonstrated need, preserving integrity within the authorized scope.
- Never commit or expose credentials, tokens, sensitive payloads, or unnecessary personal data in documentation, logs,
  examples, or tool output.
- Access to code or a database provides evidence, not authority to redefine business policy.

### Verification and completion

- Before declaring a task complete, verify the authorized scope, full scoped diff, and preservation of unrelated work.
  The coordinating agent is responsible for this final verification.
- Run `git diff --check`. Check syntax for changed Python and JavaScript source.
- Run focused checks and meaningful tests appropriate to the changed behavior, plus the requirements of applicable module guides.
- Prefer Frappe-native test tools and existing test files for relevant business cases.
  Test framework-dependent behavior through real document APIs and lifecycles instead of recreating it in test doubles.
  Keep isolated unit tests for pure logic and mock external services when needed.
- For UI changes, verify the actual interaction and Frappe-regenerated files.
- For transactional behavior, verify relevant retries, cancellation, and rollback using controlled data.
  Do not treat empty test scaffolds as coverage.
- Report what changed, why, what was tested, what was intentionally left out, and pending limitations or decisions.
  Do not claim untested behavior is verified.
- Deployment and production data changes require their own applicable authorization;
  a successful local check or documentation update does not grant it.
<!-- END SHARED RULES -->

## Repository rules — Cargo Management

### Purpose and scope

Cargo Management supports QuickBox freight forwarding and parcel operations.
Apply the shared instructions and the following Cargo-specific constraints throughout this repository.

### Required reading

- Read [README.md](README.md) for scope, features, and documentation entry points.
- Before changing business behavior, read the sibling `grupo_real_docs` repository's root AGENTS.md,
  the affected Space README.md, and the canonical process page.
- Relevant QuickBox operational areas include `quickbox/operaciones/paquetes/`,
  `quickbox/operaciones/envio-de-carga/`, and `quickbox/operaciones/recepcion-de-carga/`.
- Treat work-in-progress pages as incomplete context.
  Do not invent workflows, statuses, or responsibilities from incomplete documentation, field names, or test and historical data.

### Architecture and dependencies

- See [pyproject.toml](pyproject.toml) and [.editorconfig](.editorconfig) for dependency and tooling configuration.
- Reuse `cargo_management.engine.LinkSyncMixin` and `LinkSyncRule` for shared backlink synchronization.
  Do not duplicate per-DocType query loops.
- Reuse `cargo_management.engine.BulkStatusUpdate` and its whitelisted engine endpoints for bulk status cascades.
  Do not recreate repetitive action modules.
- Keep the app's technical documentation here; the sibling documentation repo owns canonical operating procedures.

### Repository-wide constraints

- Communicate with the owner in Spanish unless asked otherwise. Write identifiers and comments in English.
- Obtain approval before adding non-structural JavaScript calls, refreshes, indicators, or data-entry helpers.
- Use direct database updates only for a demonstrated batch or integrity need.
- Run focused DocType tests when behavior changes.
- Do not edit or publish documentation directly in Frappe Wiki. Git is the source of truth for `grupo_real_docs`.

#### Cargo invariants requiring explicit revalidation

Revalidate these statements against current code and approved operational documentation before extending them:

- A Parcel backlink conflict must block linking to another document.
- Allow duplicate Parcel rows in Cargo Shipment Receipt; do not reject a row solely because the Parcel repeats.
- Warehouse Receipt owns receipt-level weight, volume, pieces, parcels, package, and dimensions.
  Do not assume that child and parent dimensions must match.
- Parcel, Warehouse Receipt, Cargo Shipment, and Cargo Shipment Receipt have distinct status meanings.
  Confirm the operational event that authorizes a cascade before adding one.
- Keep link synchronization and status transitions separate.

### Module guides

There are no separate module AGENTS files in the current checkout. Use the root instructions and the Cargo invariants above.
