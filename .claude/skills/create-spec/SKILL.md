---
name: create-spec
description: 'Create a new feature spec in this repository. Use when asked to create a spec, document a feature, write a product or technical specification, capture functional and non-functional requirements, or add a sequential spec file for backend or frontend work.'
argument-hint: 'target area and feature name, for example: backend poll deletion'
user-invocable: true
---

# Create Spec

Create a new feature specification that matches this repository's documentation conventions while using the richer spec structure defined by this skill.

## When to Use

- The user asks to create a spec.
- A feature needs written requirements before or alongside implementation.
- A backend or frontend capability needs a reviewable functional and technical design document.

## Repository Conventions

- Spec files live under a component's `docs/specs/` directory.
- Current locations in this repository include `backend/docs/specs/` and `frontend/docs/specs/`.
- Existing files use sequential numbering.
- Feature specs should preserve the current naming approach: `NN-feature-name-spec.md`.
- Technical overview files may use `00-overview-technical-implementation.md`, but this skill is for feature specs, not overview documents.

Use the template in [feature-spec-template.md](./assets/feature-spec-template.md).

## Procedure

1. Identify the target area for the spec.
   - Use `backend/docs/specs/` for backend features.
   - Use `frontend/docs/specs/` for frontend features.
   - If neither fits, ask the user where the spec should live before creating it.

2. Inspect the existing spec files in that target directory.
   - Ignore overview files such as `00-overview-technical-implementation.md` when choosing the next feature number.
   - Find the highest existing numbered feature spec.
   - Increment it by one.
   - Preserve the `NN-feature-name-spec.md` naming pattern.

3. Gather the minimum required inputs.
   - Feature name
   - Status
   - Author
   - Related ADRs, if any
   - Goals and non-goals
   - Functional requirements
   - Non-functional requirements that matter for this feature
   - User stories or scenarios
   - Technical design details that are already known
   - Open questions and future work, if applicable

4. Create the spec from the template.
   - Keep the overview to one concise paragraph.
   - Use RFC 2119 language for requirements: MUST, SHOULD, MAY.
   - Keep requirement IDs sequential within the document.
   - Prefer concrete acceptance criteria over vague statements.
   - If some sections are not yet known, keep them explicitly marked instead of inventing details.

5. Validate the result.
   - Confirm the path, numbering, and file name are correct.
   - Ensure markdown headings, tables, and code fences are clean.
   - Keep the spec focused on one feature or vertical slice.

## Output Expectations

- Create exactly one new spec file unless the user explicitly asks for more.
- Prefer reviewable, implementation-guiding content over long product prose.
- The resulting spec should be usable for spec-driven development in this repository.
