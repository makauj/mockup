## Plan: Backend Stability and Security Review

Deliver a high-impact hardening pass on the FastAPI backend by first fixing import/runtime blockers, then correcting API-contract mismatches and validation gaps, followed by security and operability improvements (config, tests, migrations). This plan prioritizes items that currently prevent the service from running or behaving per README requirements.
**Status**
- Approved by user on 2026-03-16 for full implementation in coding mode.
- Execute all phases in order; do not skip verification.


**Steps**
1. Phase 1 - Runtime Blockers (must finish first)
1. Fix invalid/import-breaking module paths in backend package modules: replace invalid relative import syntax in main module and non-package imports in CRUD/model modules.
2. Correct Excel parsing fatal bug caused by accidental stdlib module usage instead of row email value and align parse function return annotation with actual tuple payload.
3. Resolve API-to-CRUD signature mismatch in update endpoint by passing current user and converting update schema to expected change mapping.
4. Fix optional query typing for collection filters to avoid static/runtime ambiguity when None defaults are used.

2. Phase 2 - Contract and Data Integrity
1. Align update contract so mutable fields are explicit and protected: use schema-driven allowed fields and prevent unintended attribute writes.
2. Reconcile read-only rule with requirements: read-only only when ID+Name+Contact are present; preserve editable rows when only partial data exists.
3. Validate upload inputs (extension/content-type and file-read failure handling) and return meaningful 400 errors for malformed sheets/missing required columns.
4. Review Date type consistency across model/schema/defaults so stored values match declared SQL and Pydantic types.

3. Phase 3 - Security and Operability
1. Move DATABASE_URL to environment configuration and add sane startup failure messaging for missing/invalid configuration.
2. Strengthen user identity handling in endpoints (avoid silent default identity in write operations).
3. Add structured error handling/logging around database write operations (integrity and operational failures).
4. Add API ergonomics: pagination on list endpoint, explicit status codes on write endpoints, and CORS policy if frontend is separate.

4. Phase 4 - Delivery Quality
1. Add tests: parser unit tests, CRUD update/read-only behavior tests, and API endpoint tests for upload/list/update negative and positive paths.
2. Confirm DB behavior for foreign-key target table dependency and trigger interactions with application-level checks.
3. Introduce migration workflow (Alembic) and stop relying solely on metadata.create_all for schema evolution.
4. Clean dependency manifest formatting/version intent and add container hygiene (.dockerignore, env handling).

**Relevant files**
- c:/Users/john/Downloads/Repos/mockup/backend/main.py - endpoint wiring, dependency injection, upload and update contracts.
- c:/Users/john/Downloads/Repos/mockup/backend/crud.py - create/read/update semantics, error handling, field mutability.
- c:/Users/john/Downloads/Repos/mockup/backend/utils.py - Excel parsing, read-only determination, tuple return contract.
- c:/Users/john/Downloads/Repos/mockup/backend/models.py - SQLAlchemy model imports, Date defaults, foreign-key reference.
- c:/Users/john/Downloads/Repos/mockup/backend/schemas.py - request/response schema constraints and update surface.
- c:/Users/john/Downloads/Repos/mockup/backend/database.py - DB configuration and engine/session setup.
- c:/Users/john/Downloads/Repos/mockup/backend/db.sql - trigger + FK behavior and consistency with ORM model.
- c:/Users/john/Downloads/Repos/mockup/backend/requirements.txt - dependency quality and reproducibility.
- c:/Users/john/Downloads/Repos/mockup/README.md - source-of-truth behavior requirements for import/editability.

**Verification**
1. Static checks pass for backend package (import resolution and type checking for endpoint/CRUD/parser signatures).
2. App boots successfully and OpenAPI docs load without import/runtime exceptions.
3. Upload tests verify: valid Excel rows inserted, malformed sheet rejected, date fallback applied, collected column ignored.
4. Read-only rule tests verify editable vs locked behavior per ID+Name+Contact completeness.
5. Update tests verify forbidden updates on read-only rows and correct audit fields/user propagation on editable rows.
6. List endpoint tests verify filters + pagination behavior and stable response schema.

**Decisions**
- Included scope: backend reliability, API correctness, security baseline, and test coverage for core flows.
- Excluded scope: frontend/UI implementation and full auth provider integration (can be follow-up after baseline hardening).
- Assumption: PostgreSQL is intended deployment target and foreign-key target table exists in same database lifecycle.

**Further Considerations**
1. Authentication path recommendation: quick header-based strict requirement now vs token-based OAuth2/JWT in follow-up.
2. Migration strategy recommendation: initialize Alembic immediately once schema contracts are corrected.
3. Data governance recommendation: decide whether email should be importable in future or remain API-only mutable.
