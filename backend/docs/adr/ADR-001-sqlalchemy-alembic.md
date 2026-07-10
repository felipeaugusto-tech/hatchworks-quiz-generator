# ADR 001 - SQLAlchemy 2.0 + Alembic

Date: 2026-07-10 | Status: Accepted

## Context
Need an ORM with async support and versioned migrations for PostgreSQL in FastAPI.

## Decision
Use SQLAlchemy 2.0 async with Alembic.

## Consequences
+ Native async support through asyncpg.
+ Alembic can evolve the schema from ORM models.
+ Production-proven Python ecosystem.
- More setup than raw SQL.