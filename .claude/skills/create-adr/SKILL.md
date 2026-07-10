---
name: create-adr
description: 'Create a new Architecture Decision Record (ADR) in this repository. Use when asked to create an ADR, document an architecture decision, capture a technical decision, or add a decision record for backend, frontend, or root-level architecture changes.'
argument-hint: 'target area and decision title, for example: backend auth refresh rotation'
user-invocable: true
---

# Create ADR

Create a new Architecture Decision Record that matches this repository's documentation conventions.

## When to Use

- The user asks to create an ADR.
- A change has architecture impact and must be documented.
- A backend, frontend, or shared technical decision needs an explicit decision record.

## Repository Conventions

- ADR files live under a component's `docs/adr/` directory.
- Current locations in this repository include `backend/docs/adr/` and `frontend/docs/adr/`.
- File naming uses sequential numbering and a short kebab-case slug, for example `ADR-001-frontend-foundation.md`.
- The preferred template in this repository is:
  - Title
  - Status
  - Context
  - Decision
  - Consequences

Use the template in [adr-template.md](./assets/adr-template.md).

## Procedure

1. Identify the target area for the ADR.
   - Use `backend/docs/adr/` for backend decisions.
   - Use `frontend/docs/adr/` for frontend decisions.
   - If neither exists for the requested area, ask the user where the ADR should live before creating it.

2. Inspect the existing ADR files in that target directory.
   - Find the highest existing ADR number.
   - Increment it by one.
   - Preserve the `ADR-XXX-meaningful-slug.md` naming pattern.

3. Gather the minimum required decision details.
   - Decision title
   - Status, unless `Accepted` is obvious from context
   - Context explaining the problem or constraint
   - Decision statement
   - Consequences as concise bullet points

4. Create the ADR file from the template.
   - Keep the title concise and specific.
   - Write consequences as short, concrete bullets.
   - Keep the document focused on one decision.

5. Validate the result.
   - Confirm the file path and numbering are correct.
   - Ensure markdown headings and lists are clean.
   - Keep the ADR consistent with existing repo ADR style.

## Output Expectations

- Create exactly one new ADR file unless the user explicitly asks for more.
- Prefer minimal, reviewable wording over long narrative text.
- If the requested decision is not architectural, push back and suggest a spec or regular documentation update instead.
