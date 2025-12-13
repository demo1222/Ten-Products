# TenProducts - Lessons Learned

## What Went Well
- **Clear separation of concerns** between frontend pages/components and backend routers/services made onboarding easier for new contributors.
- **FastAPI + Pydantic** provided great developer experience and auto-generated documentation, accelerating backend validation and testing.
- **Next.js App Router** paired with SCSS modules allowed us to deliver a polished, responsive UI quickly and keep styles scoped per component.
- **Database first approach** helped us validate the schema early and ensure relationships were well defined before building business logic.

## Key Challenges
- **CORS configuration** initially blocked frontend requests; developing with wildcard origins solved it but highlighted the need for different production vs. development configs.
- **SQLite locking** occurred during reseeding because multiple async sessions were open; reseeding via the provided script and ensuring sessions close solved it temporarily.
- **Lack of automated tests** slowed confidence in regression-free changes; manual testing is documented but automation will be essential next.

## Recommendations for Future Work
1. **Automate testing** – Add pytest coverage for routers/services and component tests (Storybook/Cypress) for the frontend.
2. **Migrate to production-grade DB** – Adopt PostgreSQL with Alembic migrations for structured releases and easier rollbacks.
3. **Improve DevOps readiness** – Add CI/CD pipelines, monitoring (Sentry/Prometheus), and environment-specific configurations (dev/prod).  
4. **Security hardening** – Move secrets to `.env`, tighten CORS, support refresh tokens, and enable HTTPS in staging.
5. **Expand documentation** – Include user manuals, API changelog, and runbooks for on-call/resolution guidance.

**Document Date**: December 2025  
**Author**: TenProducts Delivery Team