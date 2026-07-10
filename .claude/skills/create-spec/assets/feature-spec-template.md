# [Feature Name] - Spec

> **Status:** Draft | In Review | Approved | Deprecated
> **Author:** @username
> **Created:** YYYY-MM-DD
> **Last updated:** YYYY-MM-DD
> **Related ADRs:** [ADR-001](./adr/ADR-001.md)

---

## 1. Overview

One paragraph summarizing what this feature is, why it exists, and the problem it solves.

---

## 2. Goals

- What this spec aims to achieve as a user-facing or technical outcome.
- Keep each item specific and verifiable.

## 3. Non-Goals

- What is explicitly out of scope for this iteration.
- Use this section to prevent scope creep and set clear boundaries.

---

## 4. Background & Context

Why this is needed now. Link to relevant tickets, research, incident context, or prior discussion when available.

---

## 5. Functional Requirements

Use MUST, SHOULD, and MAY as defined by RFC 2119.

### 5.1 [Area / Flow Name]

| ID     | Requirement               | Priority |
| ------ | ------------------------- | -------- |
| REQ-01 | The system MUST ...       | P0       |
| REQ-02 | The system SHOULD ...     | P1       |
| REQ-03 | The system MAY ...        | P2       |

### 5.2 [Another Area / Flow Name]

| ID     | Requirement               | Priority |
| ------ | ------------------------- | -------- |
| REQ-04 | ...                       | P0       |

---

## 6. Non-Functional Requirements

| Category      | Requirement                                         |
| ------------- | --------------------------------------------------- |
| Performance   | p95 response time <= X ms under Y RPS               |
| Availability  | 99.9% uptime SLA                                    |
| Security      | All sensitive data encrypted at rest and in transit |
| Observability | Key flows must emit structured logs and metrics     |
| Scalability   | Must support X concurrent users without degradation |

---

## 7. User Stories / Scenarios

```text
As a [type of user],
I want [some goal],
So that [some reason / value].
```

### Acceptance Criteria

- [ ] Given [context], when [action], then [outcome].
- [ ] Given [context], when [action], then [outcome].

---

## 8. Technical Design

### 8.1 High-Level Architecture

Diagram or description of how the components fit together.

```text
[Client] -> [API Gateway] -> [Service A] -> [DB]
                      -> [Service B] -> [Queue]
```

### 8.2 Data Model

```ts
interface ExampleEntity {
  id: string;
}
```

### 8.3 API Contract

See the full Swagger or OpenAPI contract when applicable.

#### Example Endpoint

`POST /example`

```json
{
  "field": "value"
}
```

```json
{
  "id": "uuid",
  "field": "value"
}
```

### 8.4 Key Flows

Step-by-step description of the main happy path and important edge cases.

**Happy path:**

1. User does X.
2. System responds with Y.
3. Continue until completion.

**Edge cases:**

- What happens when Z is missing?
- What happens on timeout?

---

## 9. Error Handling

| Scenario                 | Behavior                             | HTTP Status |
| ------------------------ | ------------------------------------ | ----------- |
| Invalid input            | Return validation error with details | 400         |
| Resource not found       | Return standard not found error      | 404         |
| Upstream service timeout | Retry N times, then fail gracefully  | 503         |

---

## 10. Open Questions

| #   | Question                               | Owner     | Status   |
| --- | -------------------------------------- | --------- | -------- |
| 1   | Should we support X in this iteration? | @username | Open     |
| 2   | What is the retention policy for Y?    | @username | Resolved |

---

## 11. Out of Scope / Future Work

- Item that may be addressed in a future iteration.
- Known limitation being deferred intentionally.

---

## 12. References

- [Ticket / Epic](https://link)
- [Related Spec](./spec-other-feature.md)
- [External doc or RFC](https://link)
