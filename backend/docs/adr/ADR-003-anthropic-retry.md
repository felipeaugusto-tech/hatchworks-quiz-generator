# ADR 003 - Anthropic JSON Retry Strategy

Date: 2026-07-10 | Status: Accepted

## Context
Anthropic responses can occasionally include malformed JSON despite strict
prompting.

## Decision
Retry once in the same conversation thread when the first response cannot be
parsed as JSON. Return HTTP 502 if the second attempt also fails.

## Consequences
+ Handles transient formatting failures.
+ Adds no extra latency when the first response is valid.
- Failure cases can still consume two API calls.